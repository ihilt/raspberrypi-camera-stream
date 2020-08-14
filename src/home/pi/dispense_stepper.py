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

def motor_control():
    DIR = 20   # Direction GPIO Pin
    STEP = 21  # Step GPIO Pin
    CW = 1     # Clockwise Rotation
    CCW = 0    # Counterclockwise Rotation
    SPR = 1036 # Steps per Revolution (360 / 1.8) * 5.18

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.output(DIR, CW)

    MODE = (14, 15, 18) # Microstep Resolution GPIO Pins

    GPIO.setup(MODE, GPIO.OUT)
    RESOLUTION = {'Full': (0,0,0),
                  'Half': (1,0,0),
                  '1/4':  (0,1,0),
                  '1/8':  (1,1,0),
                  '1/16': (0,0,1),
                  '1/32': (1,0,1)}
    GPIO.output(MODE, RESOLUTION['Half'])

    delay = .001 / 2

    full_rev = SPR * 2

    for x in range(full_rev):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)

    sleep(.1)

    GPIO.output(DIR, CCW)

    for x in range(full_rev / 5):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)

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
            motor_control()
            set_dispense_status()
        sleep(5)


if __name__=='__main__':
    do_main()
