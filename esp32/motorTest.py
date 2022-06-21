#motor test
from machine import Pin, ADC
import time

motorEnable = Pin(7, Pin.OUT)
motorEnable.value(0)
motorBrake = Pin(6, Pin.OUT)
motorBrake.value(1)
cam_home = Pin(18, Pin.IN)
cover_detect = Pin(19, Pin.IN)
aux_en = Pin(4, Pin.OUT)
adc = ADC(Pin(0, Pin.IN))

def motor_en():
    motorBrake.value(0)
    motorEnable.value(1)
    
def motor_dis():
    motorEnable.value(0)
    motorBrake.value(1)
    

def check_home():
    motor_en()
    time.sleep(0.1)
    print(cam_home.value())
    if (cam_home.value()):
        print("cam home")
    else:
        print("cam away")
    motor_dis()
        
def check_cover():
    print(cover_detect.value())
    if (cover_detect.value()):
        print("cover open")
    else:
        print("cover close")
    #aux_en.value(0)
    
    
def measure_batt():
    #aux_en.value(1)
    time.sleep(0.1)
    print (adc.read())
    time.sleep(1)

while(1):
    #check for cover open
    #if cover open, exit while loop
    #check for hand sense
    #if hand sense - turn on motor until optointerruptor
    #motor_on()
    #motor_dis()
    aux_en.value(1)
    check_cover()
    check_home()
    time.sleep(2)
    #measure_batt()
    #check_home()
    #time.sleep(1)
    #wait 100mS
    #return to start.