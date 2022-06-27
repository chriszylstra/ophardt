import time
import _thread
#import wifimgr
import machine
import network
#import urequests
try:
  import usocket as socket
except:
  import socket
from micropython import const
from machine import Pin, ADC, Signal, PWM, mem32
from hx711 import HX711

#constants
duty_c = 0.75 #starting duty cycle, this changes with feedback. 
cooldown_ms = 5000
target_cycle_time = 400
machine.freq(80000000)
loadcell_offset = None

mem32[const(0x60043018)] = 0x0
        

#i/o setup
#ledG = Pin(21, Pin.OUT)
#ledG.off()
#ledR = Pin(20, Pin.OUT)
#ledR.off() 
motorEnable = PWM(Pin(7, Pin.OUT),freq=100000, duty_u16=0)
motorEnable.duty_u16(0)
motorBrake = Pin(6, Pin.OUT)
motorBrake.value(1)

cam_home = Pin(18, Pin.IN)
cover_detect = Pin(19, Pin.IN)
aux_en = Pin(4, Pin.OUT)
batt = ADC(Pin(0, Pin.IN))
batt.atten(ADC.ATTN_2_5DB)
ir_sense = ADC(Pin(1, Pin.IN))
ir_sense.atten(ADC.ATTN_11DB)
ir_en = Pin(3, Pin.OUT)
load_cell = HX711(d_out=10, pd_sck=8)
load_cell.channel=HX711.CHANNEL_A_128
load_cell.power_off()
wlan = network.WLAN(network.STA_IF)
wlan.active(False)
    

def motor_en(duty):
    global duty_c
    if duty < 0:
        duty_c = 0
        duty = 0
    if duty > 1:
        duty_c = 1
        duty = 1
    motorBrake.value(0)
    motorEnable.duty_u16(int(duty*65535))
    return
    
def motor_dis():
    motorEnable.duty_u16(0)
    motorBrake.value(1)
    return
    
def check_cover():
    aux_en.value(1)
    time.sleep_us(100)
    val = cover_detect.value()
    aux_en.value(0)
    return val

def check_home():
    global duty_c
    motor_en(1)
    time.sleep_us(50)
    val = cam_home.value()
    motor_en(duty_c)
    return val

def measure_batt():
    aux_en.value(1)
    time.sleep_us(50)
    val = batt.read_u16() * 1.12 / 65535
    aux_en.value(0)
    ans = ((val*(17.8+4.02))/4.02)
    ans = round(ans,3)
    return ans


def measure_IR():
    aux_en.value(1)
    time.sleep_us(50)
    val = ir_sense.read()
    aux_en.value(0)
    return val
    
def hand_sense():
    ir_en.on()
    if measure_IR() > 1500:
        ir_en.off()
        return True
    else:
        ir_en.off()
        return False       
    
def post_data(string):
    global wlan, count
    wlan.active(True)
    if not wlan.isconnected():
        #wlan.connect('OPGuest','OHTI2019')
        wlan.connect('OPCA','7$nEpTuNe4!')
        while not wlan.isconnected():
            pass
    r = urequests.post("https://ptsv2.com/t/p0mnd-1654279985/post",data=string+" " +str(count))
    wlan.active(False)
    r.close()
    count = 0
    return

def recalculate_duty_cycle(real_cycle_time, target):
    global duty_c
    if (real_cycle_time > (target*1.05) and real_cycle_time > 100):
        return duty_c*1.05;
    elif (real_cycle_time < (target/1.05) and real_cycle_time > 100):
        return duty_c/1.05;      
    else:
        return duty_c

def flash_version():
    ledR.on()
    time.sleep(0.15)
    ledR.off()
    time.sleep(1)
    x = 4
    while x:
        ledR.on()
        time.sleep(0.15)
        ledR.off()
        time.sleep(0.3)
        x -= 1

def flicker():
    start_t = time.ticks_ms()
    delta = 0
    while check_cover():
        delta = time.ticks_diff(time.ticks_ms(), start_t)
        print(delta)
        if delta > 100:
            ledR.on()
        if delta > 200:
            ledR.off()
            ledG.on()
        if delta > 300:
            ledG.off()
        if delta > 400:
            delta = 0
            start_t = time.ticks_ms()
    ledR.off()
    ledG.off()
    return
    
    
def interpret_load_cell(data):
    if data < 350_000:
        return "No bottle"
    elif data > 400_000:
        return "Full bottle"
    elif data >375_000 and data < 400_000:
        return "Empty bottle"
    else:
        return "Other"

def pump_inserted(v1, v2):
    print(v1, v2)
    if (v2 / v1) > 0.90:
        return False
    else:
        return True
    
def calibrate_load_cell():
    print("No bottle detected.... performing load cell calibration!")
    loadcell_offset = load_cell.read()
    
def updateLoadCell():
    f = open('data.txt', 'a')
    load_cell.power_on()
    f.write(str(load_cell.read()) + '\n')
    load_cell.power_off()
    f.close()


dt = 0
start_time = time.ticks_ms()
count = 0
endTime= time.ticks_ms()
activated = False

while True:
    #if check_cover(): #cover open
    #    machine.lightsleep(1000)
    #    continue
    #else: #cover closed
    machine.lightsleep(140)
    if (time.ticks_diff(time.ticks_ms(),endTime) > 3000) and activated: #measure the loadcell
        updateLoadCell()
        activated = False
        endTime = time.ticks_ms()
    
    dt = time.ticks_diff(time.ticks_ms(),start_time)
    if (dt < cooldown_ms): # or (not hand_sense()):
        continue
    
    #If you got to here, a hand was detected:
    #ledG.on()
    activated = True
    start_time = time.ticks_ms()
    motor_en(duty_c)
    start_pos = check_home()
    while start_pos == check_home():
        light_delay = time.ticks_diff(time.ticks_ms(),start_time)
        #if light_delay > 300: ledG.off()
        continue

    while not start_pos == check_home():
        light_delay = time.ticks_diff(time.ticks_ms(),start_time)  
        #if light_delay > 300: ledG.off()
        continue
    motor_dis()
    endTime = time.ticks_ms()
    duty_c = recalculate_duty_cycle(time.ticks_diff(time.ticks_ms(),start_time), target_cycle_time)

    