###############################################################
# Ophardt Hygiene Technologies Inc.
# Written by Chris Zylstra, February 2022.
# This software is provided under "The BEER-WARE LICENSE":
# czylstra@ophardt.com wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day,
# and you think its worth it, you can buy me a beer in return.
# The following code is provided with NO WARRANTY WHATSOEVER.
# Made with love, and midi-chlorians:
# -Chris Zylstra (engineer, not a programmer)
###############################################################

try:
    from guizero import *
except ImportError:
    print("You need guizero. Install it with 'pip3 install guizero'")
    exit()
try:
    import cv2
except ImportError:
    print(
        "You need cv2. Install it with 'pip install opencv-python --prefer-binary'"
    )
    exit()
try:
    import board
    from adafruit_ina219 import *
except ImportError:
    print(
        "You need adafruit_ina219. Install it with 'sudo pip3 install adafruit-circuitpython-ina219'"
    )
    exit()

from datetime import date
from datetime import datetime
import time
import RPi.GPIO as GPIO
import csv
import serial
import re
import os
import pathlib
from pathlib import Path

GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.LOW)

usb_status = False
scale_status = False
camera_status = False
voltmeter_status = False
today = date.today()
d1 = today.strftime("%d-%b-%Y")
filename = ""
diff = 0
prev = 0

app = App(title="###", layout="grid")
app.set_full_screen()

#Setting up i2c multimeter
try:
    GPIO.output(17, GPIO.HIGH)
    time.sleep(5 / 1000)
    i2c_bus = board.I2C()
    ina219 = INA219(i2c_bus)
    ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    ina219.bus_voltage_range = BusVoltageRange.RANGE_16V
    GPIO.output(17, GPIO.LOW)
    voltmeter_status = True
except:
    GPIO.output(17, GPIO.LOW)
    pass

# Setting up serial connection
try:
    # Sartorious Scale
    ser = serial.Serial(
        port="/dev/ttyUSB0",
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.SEVENBITS,
        timeout=2,
    )
    # Kern Scale
    ser = serial.Serial(port='/dev/ttyUSB0',
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=2)
    scale_status = True
except:
    app.warn("Warning", "Scale not connected. Continuing without data.")
    scale_status = False


# Not used right now, working on integrating a webcam into the station.
def checkCam():
    cam1 = cv2.VideoCapture(0)
    if not (cam1.isOpened()):
        info("InfoBox", "Error opening camera.")
        return
    cam1.set(3, 1920)
    cam1.set(4, 1080)
    now = datetime.now()
    dt = now.strftime("%d_%m_%Y")
    delay = input("Enter the delay time (seconds) between photos: ")
    Path("/home/pi/Pictures/images/" + dt).mkdir(parents=True, exist_ok=True)
    filepath = "images/" + dt + "/"


# Extend the arm


def activate():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.HIGH)


# Retract the arm


def deactivate():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.LOW)


# Exit button code


def exit_but():
    GPIO.output(17, GPIO.LOW)
    activate()
    app.destroy()
    exit()


# Called when "Start" button is clicked.


def start_prog():
    global filename
    global remaining
    global usb_status
    global serial_status

    # if camera.value:
    #     checkCam()

    if delay.value == "":
        app.warn("Warning", "Please enter delay value.")
        delay.focus()
    elif dwell.value == "":
        app.warn("Warning", "Please enter dwell value.")
        dwell.focus()
    elif length.value == "":
        app.warn("Warning", "Please enter total cycles.")
        length.focus()
    elif programName.value == "":
        app.warn("Warning", "Please enter a filename.")
        programName.focus()
    else:
        try:
            num = int(delay.value)
            num2 = int(length.value)
            num3 = int(dwell.value)
        except ValueError:
            app.warn("Warning", "Only integers in delay/dwell/cycles.")
            return
        if int(delay.value) < 2:
            app.warn("Warning",
                     "Min delay is 2 seconds due to scale communication.")
            delay.focus()
            return
        if int(dwell.value) < 2:
            app.warn("Warning",
                     "Min dwell is 2 seconds due to scale communication.")
            dwell.focus()
            return
        buttonStart.disable()
        buttonStop.enable()
        buttonPause.enable()
        length.disable()
        delay.disable()
        dwell.disable()
        programName.disable()
        cb.disable()
        print("Start")
        calculateMins()
        filename = programName.value + "_" + d1 + ".csv"
        # info("InfoBox", "Program Started:\n\n" + length.value + " cycles\nat " + delay.value + "s delay / "+ dwell.value + "s dwell."+ " \n\n" + "Filename: " +  filename)
        headerList = ["Number", "Timestamp", "Total", "Difference", "Voltage"]
        try:
            with open("/media/pi/USB/" + filename, "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=",")
                csv_writer.writerow(headerList)
            usb_status = True
        except Exception as e:
            app.warn(
                "Warning",
                "USB not found. Data will not be saved.\n(Drive must be named exactly 'USB')\n\n"
                + str(e),
            )
            usb_status = False
        print("USB: " + str(usb_status))
        print("Scale: " + str(scale_status))
        remaining = 0
        print(cb.value_text)
        if cb.value_text == "Touchless":
            app.repeat((int(delay.value) + int(dwell.value)) * 1000,
                       deactivate)
            time.sleep(int(delay.value))
            app.repeat((int(delay.value) + int(dwell.value)) * 1000, cycle)
        else:
            app.repeat((int(delay.value) + int(dwell.value)) * 1000, cycle)
            time.sleep(int(delay.value))
            app.repeat((int(delay.value) + int(dwell.value)) * 1000,
                       deactivate)


# Loop for each cycle


def cycle():
    global remaining
    global diff
    global usb_status
    global voltmeter_status
    dashboard.value = ("Cycles Remaining: " +
                       str(int(length.value) - remaining) + " (" + str(
                           round(
                               (int(length.value) - remaining) *
                               (int(delay.value) + int(dwell.value)) / 60,
                               1,
                           )) + " minutes)")
    last.value = "Last Dose: " + str(diff) + " grams"
    if remaining < int(length.value):
        remaining += 1
        # measure the voltage before activation
        voltage = 0
        if voltmeter_status:
            voltage = volt_measure()

        GPIO.output(17, GPIO.LOW)
        activate()
        if usb_status:
            writedata(remaining, voltage)
    else:
        stop_prog()


def volt_measure():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    try:
        GPIO.output(17, GPIO.HIGH)
        time.sleep(5 / 1000)
        bus_voltage = ina219.bus_voltage  # voltage on V- (load side)
        GPIO.output(17, GPIO.LOW)
        bus_voltage = round(bus_voltage, 2)
        voltage.value = "Battery voltage: " + str(bus_voltage) + " Volts"
        # print("voltage: " + str(bus_voltage))
        return bus_voltage
    except Exception as e:
        voltage.value = "Battery voltage: error"
        return 0


def stop_prog():
    GPIO.output(17, GPIO.LOW)
    global remaining
    length.enable()
    delay.enable()
    dwell.enable()
    programName.enable()
    cb.enable()
    buttonStart.enable()
    buttonStop.disable()
    buttonPause.disable()
    buttonPause.text = "Pause"
    app.cancel(cycle)
    app.cancel(deactivate)
    activate()
    remaining = 0
    print("stop")


# Pause Button Code


def pause_prog():
    buttonStart.disable()
    buttonStop.enable()
    if buttonPause.text == "Pause":
        activate()
        app.cancel(cycle)
        app.cancel(deactivate)
        buttonPause.text = "Resume"
        print("pause")
    else:
        if cb.value_text == "Touchless":
            app.repeat((int(delay.value) + int(dwell.value)) * 1000,
                       deactivate)
            time.sleep(int(delay.value))
            app.repeat((int(delay.value) + int(dwell.value)) * 1000, cycle)
        else:
            app.repeat((int(delay.value) + int(dwell.value)) * 1000, cycle)
            time.sleep(int(delay.value))
            app.repeat((int(delay.value) + int(dwell.value)) * 1000,
                       deactivate)
        buttonPause.text = "Pause"
        print("Resume")


def calculateMins():
    global minutes
    minutes = int(length.value) / (int(delay.value) + int(dwell.value))
    minutes = round((minutes / 60), 1)


# Used to capture the scale data and write to usb.


def writedata(count, volts):
    global diff
    global prev
    global usb_status
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if scale_status:
        x = ser.readline()
        try:
            parsed_x = float(x[3:12])
            diff = parsed_x - prev
            diff = round(diff, 2)
            prev = parsed_x
        except ValueError:
            parsed_x = prev
            diff = 0
        ser.reset_input_buffer()
    else:
        parsed_x = 0

    # print(parsed_x)
    scale.value = "Current Weight: " + str(parsed_x) + " grams"
    data = (str(count) + "," + current_time + "," + str(parsed_x) + "," +
            str(diff) + "," + str(volts) + "\n")
    if usb_status:
        with open("/media/pi/USB/" + filename, "a") as fd:
            fd.write(data)


# Code following this line is used to draw the GUI and buttons.
activate()

blanktext1 = Text(app, text="", size=20, grid=[0, 0])

box1 = Box(app, border=True, grid=[0, 1], align="left")
text_delay = Text(box1, text="Delay:          ", align="left", size=50)
delay = TextBox(box1, align="left", width=15)

delay.text_size = 50
delay.focus()
text_delay2 = Text(box1, text="seconds", align="left", size=50)
box12 = Box(app, border=True, grid=[0, 2], align="right")
cb = ButtonGroup(box12, options=["Touchless", "Manual"], selected="Manual")
cb.text_size = 25
# camera = CheckBox(box12, text=" Use Camera ", align = "right")
# camera.text_size = 25
# camera.value = 0

# photoDelay = TextBox(box12, width = 3, align = "right")

box11 = Box(app, border=True, grid=[0, 3], align="left")
text_dwell = Text(box11, text="Dwell:          ", align="left", size=50)
dwell = TextBox(box11, align="left", width=15)
dwell.text_size = 50
text_dwell2 = Text(box11, text="seconds", align="left", size=50)

blanktext11 = Text(app, text="", size=40, grid=[0, 4])

box2 = Box(app, border=True, grid=[0, 5], align="left")
text_length = Text(box2, text="Total Cycles:", align="left", size=50)
length = TextBox(box2, align="left", width=15)
length.text_size = 50

blanktext2 = Text(app, text="", size=40, grid=[0, 6])

box3 = Box(app, border=True, grid=[0, 7], align="left")
text_programName = Text(box3, text="Filename:    ", size=50, align="left")
programName = TextBox(box3, width=15, align="left")
text_programName2 = Text(box3,
                         text="_" + d1 + ".csv        ",
                         size=50,
                         align="left")
programName.text_size = 50
text_fileLocation = Text(app,
                         grid=[0, 8],
                         text="Data file saved at: /media/pi/USB/",
                         size=15,
                         align="left")
blanktext3 = Text(app, text="", size=30, grid=[0, 8])

box5 = Box(app, grid=[0, 9], width="fill")
buttonStart = PushButton(box5,
                         command=start_prog,
                         text="Start Pumpdown",
                         width=20,
                         height=2,
                         align="left")
buttonStart.bg = "lightgreen"
buttonStart.text_size = 20
buttonStart.enable()
boxGap = Box(box5, width=30, height=3, align="left")
buttonPause = PushButton(box5,
                         command=pause_prog,
                         text="Pause",
                         width=20,
                         height=2,
                         align="left")
buttonPause.bg = "gold"
buttonPause.text_size = 20
buttonPause.disable()
boxGap2 = Box(box5, width=30, height=3, align="left")
buttonStop = PushButton(box5,
                        command=stop_prog,
                        text="Stop",
                        width=20,
                        height=2,
                        align="left")
buttonStop.bg = "tomato"
buttonStop.text_size = 20
buttonStop.disable()

box6 = Box(app, grid=[0, 11], width="fill")
buttonIn = PushButton(box6,
                      command=deactivate,
                      text="Extend Arm",
                      width=10,
                      height=1,
                      align="left")
buttonIn.bg = "royal blue"
buttonOut = PushButton(box6, command=activate, text="Retract Arm")
buttonOut.bg = "royal blue"

blanktext4 = Text(app, text="", size=40, grid=[0, 10])

box4 = Box(app, layout="grid", border=True, grid=[0, 10], align="left")
dashboard = Text(box4,
                 text="Cycles Remaining: " + length.value,
                 grid=[0, 0],
                 size=20,
                 align="left")
scale = Text(box4, text="Scale Value: ", grid=[0, 1], size=20, align="left")
last = Text(box4, text="Last Dose: ", grid=[0, 2], size=20, align="left")
voltage = Text(box4,
               text="Battery voltage: ",
               grid=[0, 3],
               size=20,
               align="left")

box41 = Box(app, layout="grid", border=True, grid=[0, 11], align="left")
scaleStatus = Text(box41,
                   text="Scale Status: ",
                   grid=[0, 0],
                   size=20,
                   align="left")
usbStatus = Text(box41,
                 text="USB Status: ",
                 grid=[0, 1],
                 size=20,
                 align="left")
multimeterStatus = Text(box41,
                        text="Multimeter Status: ",
                        grid=[0, 2],
                        size=20,
                        align="left")
cameraStatus = Text(box41,
                    text="Camera Status: ",
                    grid=[0, 3],
                    size=20,
                    align="left")
# blanktext5 = Text(app, text="", size =30, grid = [0,12])

exiter = PushButton(app,
                    command=exit_but,
                    text="Exit",
                    width=20,
                    height=2,
                    grid=[0, 13],
                    align="bottom")
exiter.text_size = 20
exiter.bg = "indian red"

# No code allowed past this line.
app.display()
