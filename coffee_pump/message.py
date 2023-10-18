from config import SENSOR_ERROR, NO_WATER_ERROR, START_PUMP_PERCENTAGE, STOP_PUMP_PERCENTAGE


def calc_status(error_code, percentage, pump_on):
    return 'Sensor Error!' if error_code == SENSOR_ERROR \
        else 'Empty Water Source!' if error_code == NO_WATER_ERROR \
        else 'Water pouring' if pump_on \
        else 'Low Water Level' if percentage < START_PUMP_PERCENTAGE \
        else 'Overflow!' if percentage > 100 \
        else 'Water Level OK'


def calc_alert(error_code):
    sensor_msg = 'WARNING! The sensor probably is out of order'
    no_water_msg = 'ACTION REQUIRED! Replace a water bottle and enable the pump by adding water manually.'
    return sensor_msg if error_code == SENSOR_ERROR \
        else no_water_msg if error_code == NO_WATER_ERROR \
        else ''
