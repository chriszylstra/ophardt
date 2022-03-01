import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
relay = 4
GPIO.setup(relay, GPIO.OUT)

while True:
    GPIO.output(relay, GPIO.LOW)
    time.sleep(1)
    GPIO.output(relay,GPIO.HIGH)
    time.sleep(1)