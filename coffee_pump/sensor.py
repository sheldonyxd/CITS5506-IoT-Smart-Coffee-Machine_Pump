import RPi.GPIO as GPIO
from hcsr04sensor import sensor as hcsr04sensor
from config import GPIO_TRIGGER, GPIO_ECHO, MAX_RETRIES
from logger import log_debug, log_error, log_info

hcsr04 = hcsr04sensor.Measurement(trig_pin=GPIO_TRIGGER, echo_pin=GPIO_ECHO)


def get_distance():
    retries = 0
    while retries < MAX_RETRIES:
        try:
            distance = round(hcsr04.raw_distance(), 1)
            if distance is not None:
                return distance
        except Exception as e:
            log_error(f"Unexpected sensor error:{e}")
            retries += 1
    return None
            

