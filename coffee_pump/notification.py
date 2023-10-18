import json
import requests
import threading
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from config import FLASK_URL
from logger import log_debug, log_error



def send_data_in_background(data):
    thread = threading.Thread(target=send_data, args=(data,))
    thread.start()


def send_data(data):
    # Water Level OK , Sensor Error! , Water pouring , Overflow! , Low Water Level , No water,
    try:
        log_debug(f"Send data: {data}")
        response = requests.post(FLASK_URL, json=data)

        if response.status_code == 200:
            print("updata success!")
        else:
            print("updata failed!")
            print(response)
    except HTTPError as e:
        log_error('Request failed: %d %s' % (e.code, e.reason))
    except URLError as e:
        log_error('Server connection failed: %s' % e.reason)
    except Exception as e:
        log_error(f'Error while sending data: {str(e)}')
