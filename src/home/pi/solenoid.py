from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

GPIO.output(20, GPIO.HIGH)
GPIO.output(21, GPIO.HIGH)
sleep(2)
GPIO.output(21, GPIO.LOW)
sleep(1)
GPIO.output(20, GPIO.LOW)
GPIO.cleanup()
