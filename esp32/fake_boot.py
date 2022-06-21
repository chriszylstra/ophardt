import network
import machine
import esp
import time
import ntptime
from machine import Pin, ADC, WDT, RTC


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect('OPGuest', 'OHTI2019')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    print("Time before synch: %s" %str(time.localtime()))
    ntptime.settime()
    print("time after synch: %s" %str(time.localtime()))

    
def create_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='Chris', password='password')

ledR = machine.Pin(5, machine.Pin.OUT)
ledG = machine.Pin(6, machine.Pin.OUT)
ledB = machine.Pin(7, machine.Pin.OUT)

#adc = ADC(machine.Pin(0, machine.Pin.IN))
#val = adc.read_u16()
#print("ADC Value: " + str(val))

rtc1 = machine.RTC()
rtc1.datetime((2000,1,1,0,0,0,0,0))
start = time.ticks_ms()
do_connect()
delta = time.ticks_diff(time.ticks_ms(), start)
print("Time to connect to Wifi: " + str(delta))

    

