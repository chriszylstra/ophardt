"""pumpdown.py"""
# Ophardt Hygiene Technologies Inc.
# Written by Chris Zylstra, February 2022.
# This software is provided under "The BEER-WARE LICENSE":
# If we meet some day, you can buy me a beer in return.
# The following code is provided with NO WARRANTY WHATSOEVER.
# Made with love, and midi-chlorians:
# -Chris Zylstra (engineer, not a programmer)


import time
import sys
import csv
import os
import socket
from datetime import date
from datetime import datetime
from pathlib import Path
import serial

try:
    import RPi.GPIO as GPIO
except ImportError:
    sys.exit("This software only runs on Raspberry Pi.\
Feel free to modify it to run on something else! :)")

try:
    from guizero import App, Window, PushButton, Text, TextBox, Box, ButtonGroup
except ImportError:
    sys.exit("You need guizero. Install it with 'pip3 install guizero'")

try:
    import cv2
except ImportError:
    sys.exit("You need cv2. Install it with 'pip install opencv-python \
--prefer-binary'")

try:
    import board
    from adafruit_ina219 import INA219, ADCResolution, BusVoltageRange
except ImportError:
    sys.exit("You need adafruit_ina219. Install it with 'sudo \
pip3 install adafruit-circuitpython-ina219'")

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

app = App(title=str(socket.gethostname()), layout="grid")
window = Window(app, title="Information")
window.hide()
# app.set_full_screen()

# Setting up i2c multimeter
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

# Setting up serial connection


# Not used right now, working on integrating a webcam into the station.
try:
    cam1 = cv2.VideoCapture(0)
    if not cam1.isOpened():
        raise ValueError('Borked Camera')
    cam1.set(3, 1920)
    cam1.set(4, 1080)
    now = datetime.now()
    dt = now.strftime("%d_%m_%Y")
    # delay = input("Enter the delay time (seconds) between photos: ")
    Path("/home/pi/Pictures/images/" + dt).mkdir(parents=True, exist_ok=True)
    filepath = "images/" + dt + "/"
    camera_status = True
except:
    pass

# testing USB
try:
    with open("/media/pi/USB/test.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
    usb_status = True
    os.remove("/media/pi/USB/test.csv")
except Exception as e:
    app.warn("Warning",
             "USB not found. Data will not be saved.\n(Drive must be named exactly 'USB')\n\n" +
             str(e))


def activate():
    """Extends the arm."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.HIGH)


def deactivate():
    """Retracts the arm."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.LOW)


def exit_but():
    """Safetly exits the program"""
    GPIO.output(17, GPIO.LOW)
    activate()
    app.destroy()
    sys.exit(0)


def start_prog():
    """Called when 'start' button is clicked."""
    global filename
    global remaining
    global usb_status
    global voltmeter_status
    global camera_status

    # if camera.value:
    #     checkCam()

    if delay_input.value == "":
        app.warn("Warning", "Please enter delay value.")
        delay_input.focus()
    elif dwell_input.value == "":
        app.warn("Warning", "Please enter dwell value.")
        dwell_input.focus()
    elif length_input.value == "":
        app.warn("Warning", "Please enter total cycles.")
        length_input.focus()
    elif filename_input.value == "":
        app.warn("Warning", "Please enter a filename.")
        filename_input.focus()
    else:
        try:
            num = int(delay_input.value)
            num2 = int(length_input.value)
            num3 = int(dwell_input.value)
        except ValueError:
            app.warn("Warning", "Only integers in delay/dwell/cycles.")
            return
        if int(delay_input.value) < 2:
            app.warn("Warning", "Min delay is 2 seconds due to scale communication.")
            delay_input.focus()
            return
        if int(dwell_input.value) < 2:
            app.warn("Warning", "Min dwell is 2 seconds due to scale communication.")
            dwell_input.focus()
            return
        button_start.disable()
        button_stop.enable()
        button_pause.enable()
        length_input.disable()
        delay_input.disable()
        dwell_input.disable()
        filename_input.disable()
        scale_selector_kern.disable()
        scale_selector_sart.disable()
        touchless_selector.disable()
        manual_selector.disable()

        calculateMins()
        filename = filename_input.value + "_" + d1 + ".csv"
        headerList = ["Number", "Timestamp", "Total", "Difference", "Voltage"]
        if usb_status:
            with open("/media/pi/USB/" + filename, "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=",")
                csv_writer.writerow(headerList)
        usbStatus.value = "USB: " + str(usb_status)
        remaining = 0
        if touchless_selector.bg == "pale green":
            app.repeat(
                (int(delay_input.value) + int(dwell_input.value)) * 1000,
                deactivate)
            time.sleep(int(delay_input.value))
            app.repeat(
                (int(delay_input.value) + int(dwell_input.value)) * 1000, cycle)
        else:
            app.repeat(
                (int(delay_input.value) + int(dwell_input.value)) * 1000, cycle)
            time.sleep(int(delay_input.value))
            app.repeat(
                (int(delay_input.value) + int(dwell_input.value)) * 1000,
                deactivate)


# Loop for each cycle


def cycle():
    """Main loop for each activation"""
    global remaining
    global diff
    global usb_status
    global voltmeter_status
    dashboard.value = (
        "Cycles Remaining: " + str(int(length_input.value) - remaining) + " (" +
        str(round((int(length_input.value) - remaining) * (int(delay_input.value) +
                                                           int(dwell_input.value)) / 60, 1,)) + " minutes)")
    last.value = "Last Dose: " + str(diff) + " grams"
    if remaining < int(length_input.value):
        remaining += 1

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
    """Get the value of the i2c voltmeter."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    try:
        GPIO.output(17, GPIO.HIGH)
        time.sleep(5 / 1000)
        bus_voltage = ina219.bus_voltage
        GPIO.output(17, GPIO.LOW)
        bus_voltage = round(bus_voltage, 2)
        voltage.value = "Battery voltage: " + str(bus_voltage) + " Volts"

        return bus_voltage
    except Exception as e:
        voltage.value = "Battery voltage: error"
        return 0


def stop_prog():
    """Called when the 'stop' button is pressed."""
    GPIO.output(17, GPIO.LOW)
    global remaining
    length_input.enable()
    delay_input.enable()
    dwell_input.enable()
    filename_input.enable()
    scale_selector_kern.enable()
    scale_selector_sart.enable()
    touchless_selector.enable()
    manual_selector.enable()
    button_start.enable()
    button_stop.disable()
    button_pause.disable()
    button_pause.text = "Pause"
    app.cancel(cycle)
    app.cancel(deactivate)
    activate()
    remaining = 0


def pause_prog():
    """Called when the pause button is pressed."""
    button_start.disable()
    button_stop.enable()
    if button_pause.text == "Pause":
        activate()
        app.cancel(cycle)
        app.cancel(deactivate)
        button_pause.text = "Resume"
        print("pause")
    else:
        if touchless_selector.bg == "pale green":
            app.repeat(
                (int(delay_input.value) + int(dwell_input.value)) * 1000,
                deactivate)
            time.sleep(int(delay_input.value))
            app.repeat(
                (int(delay_input.value) + int(dwell_input.value)) * 1000, cycle)
        else:
            app.repeat(
                (int(delay_input.value) + int(dwell_input.value)) * 1000, cycle)
            time.sleep(int(delay_input.value))
            app.repeat(
                (int(delay_input.value) + int(dwell_input.value)) * 1000,
                deactivate)
        button_pause.text = "Pause"
        print("Resume")


def calculateMins():
    """Calculates the number of minutes from the cycles and the delay/dwell time."""
    """Remove this function maybe?"""
    global minutes
    minutes = int(length_input.value) / (int(delay_input.value) +
                                         int(dwell_input.value))
    minutes = round((minutes / 60), 1)


def writedata(count, volts):
    """Used to capture the scale data and write to usb."""
    global diff
    global prev
    global usb_status
    global scale_status
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
    scale.value = "Current Weight: " + str(parsed_x) + " grams"
    data = (
        str(count) + "," + current_time + "," + str(parsed_x) + "," + str(diff) + "," +
        str(volts) + "\n")
    if usb_status:
        with open("/media/pi/USB/" + filename, "a") as fd:
            fd.write(data)


def open_window():
    """Opens the information window."""
    window.show()


def activate_kern():
    scale_selector_kern.bg = "pale green"
    scale_selector_sart.bg = "white"
    global ser
    global scale_status
    try:
        ser = serial.Serial(
            port='/dev/ttyUSB0', baudrate=9600, parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=2)
        scale_status = True
        scaleStatus.value = "Scale: " + str(scale_status)
        scaleStatus.text_color = "green"
    except:
        scale_status = False
        app.warn("Warning", "Scale not connected. Continuing without data.")
        scaleStatus.value = "Scale: " + str(scale_status)
        scaleStatus.text_color = "red"


def activate_sart():
    scale_selector_kern.bg = "white"
    scale_selector_sart.bg = "pale green"
    global ser
    global scale_status
    try:
        ser = serial.Serial(
            port="/dev/ttyUSB0", baudrate=9600, parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_ONE, bytesize=serial.SEVENBITS, timeout=2)
        scale_status = True
        scaleStatus.value = "Scale: " + str(scale_status)
        scaleStatus.text_color = "green"
    except:
        scale_status = False
        app.warn("Warning", "Scale not connected. Continuing without data.")
        scaleStatus.value = "Scale: " + str(scale_status)
        scaleStatus.text_color = "red"


def activate_manual():
    touchless_selector.bg = "white"
    manual_selector.bg = "pale green"


def activate_touchless():
    touchless_selector.bg = "pale green"
    manual_selector.bg = "white"


blank0 = Text(app, text="", size=1, align="left", grid=[0, 0])

box0 = Box(app, border=True, grid=[0, 1], align="left")
delay_front = Text(box0, text="Delay:          ", align="left", size=50)
delay_input = TextBox(box0, align="left", width=15)
delay_input.text_size = 50
delay_input.focus()
delay_back = Text(box0, text="seconds", align="left", size=50)

box1 = Box(app, border=True, grid=[0, 3], align="right")
settings_header = Text(box1, text="Settings", align="top")
box11 = Box(box1, border=False)
scale_selector_kern = PushButton(
    box11, text="Kern", command=activate_kern, width=7,
    height=1, align="left")
scale_selector_kern.bg = "pale green"
scale_selector_kern.text_size = "10"
scale_selector_sart = PushButton(
    box11, text="Sartorious", command=activate_sart,
    width=7, height=1, align="left")
scale_selector_sart.bg = "white"
scale_selector_sart.text_size = "10"
manual_selector = PushButton(box1, text="Manual", command=activate_manual,
                             width=7, height=1, align="left")
manual_selector.bg = "pale green"
touchless_selector = PushButton(
    box1, text="Touchless", command=activate_touchless, width=7, height=1, align="left")
touchless_selector.bg = "white"

blank2 = Text(app, text="", size=20, grid=[0, 2])

box2 = Box(app, border=True, grid=[0, 3], align="left")
dwell_front = Text(box2, text="Dwell:          ", align="left", size=50)
dwell_input = TextBox(box2, align="left", width=15)
dwell_input.text_size = 50
dwell_back = Text(box2, text="seconds", align="left", size=50)

blank3 = Text(app, text="", size=40, grid=[0, 4])

box3 = Box(app, border=True, grid=[0, 5], align="left")
length_front = Text(box3, text="Total Cycles:", align="left", size=50)
length_input = TextBox(box3, align="left", width=15)
length_input.text_size = 50

blank4 = Text(app, text="", size=40, grid=[0, 6])

box4 = Box(app, border=True, grid=[0, 7], align="left")
filename_front = Text(box4, text="Filename:    ", size=50, align="left")
filename_input = TextBox(box4, width=15, align="left")
filename_input.text_size = 50
filename_back = Text(
    box4, text="_" + d1 + ".csv        ", size=50, align="left")

file_location = Text(
    app, grid=[0, 8],
    text="Data file saved at: /media/pi/USB/", size=15, align="left")

blank5 = Text(app, text="", size=30, grid=[0, 8])

box5 = Box(app, grid=[0, 9], border=True, layout="grid", align="left")
header = Text(box5, text="Device Status", grid=[0, 0], align="left")
scaleStatus = Text(box5, text="Scale: " + str(scale_status),
                   color="red", grid=[0, 1], align="left")
if scale_status:
    scaleStatus.text_color = "green"

usbStatus = Text(box5, text="USB: " + str(usb_status),
                 color="red", grid=[0, 2], align="left")
if usb_status:
    usbStatus.text_color = "green"
multimeterStatus = Text(
    box5, text="Multimeter: " + str(voltmeter_status),
    color="red", grid=[0, 3],
    align="left")
if voltmeter_status:
    multimeterStatus.text_color = "green"
cameraStatus = Text(box5, text="Camera: " + str(camera_status),
                    color="red", grid=[0, 4], align="left")
if camera_status:
    cameraStatus.text_color = "green"

box6 = Box(app, border=False, grid=[0, 9])
boxGap0 = Box(box6, width=60, height=3, align="left")
button_start = PushButton(box6, command=start_prog, text="Start Pumpdown",
                          width=20, height=2, align="left")
button_start.bg = "lightgreen"
button_start.text_size = 20
button_start.enable()
boxGap = Box(box6, width=30, height=3, align="left")
button_pause = PushButton(box6, command=pause_prog, text="Pause",
                          width=20, height=2, align="left")
button_pause.bg = "gold"
button_pause.text_size = 20
button_pause.disable()
boxGap2 = Box(box6, width=30, height=3, align="left")
button_stop = PushButton(box6, command=stop_prog, text="Stop",
                         width=20, height=2, align="left")
button_stop.bg = "tomato"
button_stop.text_size = 20
button_stop.disable()

box6 = Box(app, grid=[0, 10], width="fill")
button_deactivate = PushButton(box6, text="Extend Arm", command=deactivate,
                               width=10, height=1, align="left")

button_deactivate.bg = "light blue"
button_activate = PushButton(box6, command=activate, text="Retract Arm")
button_activate.bg = "light blue"

box7 = Box(app, layout="grid", border=True, grid=[0, 10], align="left")
dashboard = Text(box7, text="Cycles remaining: " + length_input.value,
                 grid=[0, 0], size=20, align="left")
scale = Text(box7, text="Scale value: ", grid=[0, 1], size=20, align="left")
last = Text(box7, text="Last dose: ", grid=[0, 2], size=20, align="left")
voltage = Text(box7, text="Battery voltage: ",
               grid=[0, 3], size=20, align="left")

blank6 = Text(app, text="", size=20, grid=[0, 11])

exiter = PushButton(app, command=exit_but, text="Exit", width=20,
                    height=2, grid=[0, 12], align="bottom")
exiter.text_size = 20
exiter.bg = "indian red"

date = Text(app, text="Build Date: 1 April 2022",
            size=15, align="left", grid=[0, 13])
box41 = Box(app, layout="grid", border=False, grid=[0, 14], align="left")
version = Text(box41, text="Version: 1.0.5",
               size=15, align="left", grid=[0, 0])
information = PushButton(box41, command=open_window, text="Info",
                         width=2, height=1, grid=[1, 0], align="left")
infotext = Text(
    window, text="Ophardt Hygiene Technologies Inc.\nWritten by Chris Zylstra,\
 February 2022.\nThis software is provided under The BEER-WARE LICENSE:\
\nIf we meet some day, you can buy me a beer in return.\nThe following code\
is provided with NO WARRANTY WHATSOEVER.\nMade with love, and midi-chlorians:\
\n-Chris Zylstra (engineer, not a programmer)", align="left", width="fill")
information.bg = "light blue"
activate_sart()
app.display()
