from time import sleep
from dotenv import load_dotenv

import urllib, json, RPi.GPIO as GPIO, os

load_dotenv(dotenv_path='/home/pi/.env')

SITE_URL=os.getenv('SITE_URL')
STREAM_ID=os.getenv('STREAM_ID')

PID=str(os.getpid())
f = open('/var/run/dispense.pid', 'w')
f.write(PID)
f.close

def dispense_control():
    VIB = 20
    SOL = 21

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SOL, GPIO.OUT)
    GPIO.setup(VIB, GPIO.OUT)

    GPIO.output(VIB, GPIO.HIGH)
    sleep(1)
    GPIO.output(SOL, GPIO.HIGH)
    sleep(.2)
    GPIO.output(SOL, GPIO.LOW)
    sleep(1)
    GPIO.output(VIB, GPIO.LOW)
    GPIO.cleanup()

def set_dispense_status():
    try:
        url = SITE_URL + '?action=stream_and_dispense_controller_set_dispense_status'
        post_data = urllib.urlencode({'stream_id': STREAM_ID})
        response = urllib.urlopen(url, post_data)
        data = json.loads(response.read())
    except:
        data = False
    return data

def get_dispense_status():
    try:
        url = SITE_URL + '?action=stream_and_dispense_controller_get_dispense_status'
        post_data = urllib.urlencode({'stream_id': STREAM_ID})
        response = urllib.urlopen(url, post_data)
        data = json.loads(response.read())
    except:
        data = False
    return data

def do_main():
    while True:
        if get_dispense_status() == True:
            dispense_control()
            set_dispense_status()
        sleep(5)


if __name__=='__main__':
    do_main()
