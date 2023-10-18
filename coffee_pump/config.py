# Configuration settings and constants
# FLASK configurations
FLASK_URL = "http://127.0.0.1:5000/upload_data"  

# GPIO Pins (BCM)
GPIO_PUMP = 4
GPIO_TRIGGER = 17
GPIO_ECHO = 27
GPIO_BOTTOM = 13

# Pump control settings (Reserved)
START_PUMP = 0
STOP_PUMP = 1

# Distance from the sensor to the water level
# based on the coffee-machine's water tank
MIN_DISTANCE = 3  # cm
MAX_DISTANCE = 17  # cm
DELTA_DISTANCE = 0.1  # cm

# Based on the water level
START_PUMP_PERCENTAGE = 30  # %
STOP_PUMP_PERCENTAGE = 80  # %

# Error codes
SENSOR_ERROR = 1
NO_WATER_ERROR = 2

# Time intervals
POLLING_INTERVAL = 5  # secs
SOURCE_CHECK_INTERVAL = 30  # secs

# Max retries to get distance
MAX_RETRIES = 5



