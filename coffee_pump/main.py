import RPi.GPIO as GPIO
import time
from config import *
from sensor import get_distance   # Use the instance you've created in the sensor.py
from notification import send_data_in_background
from message import calc_status, calc_alert
from logger import log_info, log_error, log_debug
from rpi_utils import os_name, host_name, ip_address


# Global variables
system_pause = False
last_check_distance = None
last_check_time = None


def pump_is_on():
    if GPIO.input(GPIO_PUMP) == START_PUMP:
        return True
    else:
        return False


def turn_pump_on():
    GPIO.output(GPIO_PUMP, START_PUMP)
    log_info("Pump is ON, waiting for water to flow...")
    # Wait for 10 seconds to let the water flow
    time.sleep(10)


def turn_pump_off():
    global last_check_distance, last_check_time
    GPIO.output(GPIO_PUMP, STOP_PUMP)
    log_info("Pump is OFF.")
    last_check_distance = None
    last_check_time = None


def pump_reboot(channel):  # Don't forget to accept the channel argument, as it's passed by the event callback
    global system_pause
    system_pause = False
    log_info(f"System rebooted. System_Pause: {system_pause}")


def get_water_level_percentage(distance):
    if distance is None:
        return None
    percentage = (MAX_DISTANCE - distance) / (MAX_DISTANCE - MIN_DISTANCE) * 100
    return round(percentage, 0)


def create_data_dict(distance, percentage, error_code):
    """Create a dictionary containing system data for sending."""
    return {
        "distance": distance,
        "status": calc_status(error_code, percentage, pump_is_on()),
        "waterlevel": percentage
    }


def gpio_setup():
    log_info("Starting coffee pump monitoring system...")
    log_info(f"Running on: {os_name()}")
    log_info(f"Host Name: {host_name()}")
    log_info(f"IP Address: {ip_address()}")
    log_info('Setting up GPIO...')

    # Set GPIO mode to BCM
    GPIO.setmode(GPIO.BCM)

    # Setup GPIO pins for the pump and initial state to OFF
    GPIO.setup(GPIO_PUMP, GPIO.OUT)
    GPIO.output(GPIO_PUMP, STOP_PUMP)

    # Setup GPIO pin for the bottom switch
    GPIO.setup(GPIO_BOTTOM, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(GPIO_BOTTOM, GPIO.BOTH, callback=pump_reboot, bouncetime=300)
    log_info('Connecting HCSR04 sensor...')
    distance = get_distance()
    log_info(f"Initial distance: {distance} cm")


def handle_alert(distance, percentage, error_code):
    global system_pause
    turn_pump_off()
    system_pause = True
    log_info("Pump stops and system pause. Waiting for manual reset.")
    log_debug(f"System_Pause: {system_pause}")
    send_data_in_background(create_data_dict(distance, percentage, error_code))


def main():
    global system_pause, last_check_distance, last_check_time
    data_timer = 0

    # Setup GPIO
    gpio_setup()

    try:
        log_info('Start monitoring...')
        while True:
            log_debug(f"Pump_On: {pump_is_on()}, System_Pause: {system_pause}")

            # Check if system is paused
            if system_pause:
                time.sleep(POLLING_INTERVAL)
                continue

            distance = get_distance()
            percentage = get_water_level_percentage(distance)
            log_debug(f"Distance: {distance} cm, Percentage: {percentage} %")
            now = time.time()

            # Check sensor error
            if distance is None:
                log_error("Distance is None. Sensor error!")
                handle_alert(distance, percentage, SENSOR_ERROR)
                break

            # Determine sending interval
            if pump_is_on():

                # Check water source empty error
                if last_check_distance is None:
                    last_check_distance = distance
                    last_check_time = time.time()

                if now - last_check_time >= SOURCE_CHECK_INTERVAL:
                    if distance - last_check_distance <= DELTA_DISTANCE:
                        log_error("Water level not change for long. Water source empty!")
                        handle_alert(distance, percentage, NO_WATER_ERROR)
                        continue
                    last_check_distance = distance
                    last_check_time = now

            # Check water level
            # If percentage is less than START_PUMP_PERCENTAGE, turn on the pump
            if percentage <= START_PUMP_PERCENTAGE and not pump_is_on():
                turn_pump_on()

            # If percentage is greater than STOP_PUMP_PERCENTAGE, turn off the pump
            elif percentage >= STOP_PUMP_PERCENTAGE and pump_is_on():
                turn_pump_off()

            # Send data every interval
            send_data_in_background(create_data_dict(distance, percentage, 0))
            time.sleep(POLLING_INTERVAL)

    except KeyboardInterrupt:
        log_error("Process interrupted.")

    except Exception as e:
        log_error(f"Unexpected error: {e}")

    finally:
        GPIO.cleanup()
        log_info("Cleanup done.")


if __name__ == "__main__":
    main()

