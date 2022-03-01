import time
import serial
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate = 9600,
    parity=serial.PARITY_ODD,
    stopbits = serial.STOPBITS_ONE,
    bytesize=serial.SEVENBITS,
    timeout=None
    )

while 1:
    x=ser.readline()
    x=x[3:10]
    print(x)