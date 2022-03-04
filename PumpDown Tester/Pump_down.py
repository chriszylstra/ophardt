from guizero import App, Text, TextBox, PushButton, info, Box, CheckBox, ButtonGroup
from datetime import date
from datetime import datetime
import time
import RPi.GPIO as GPIO
import csv
import serial
import re

GPIO.setwarnings(False)

app = App(title= "Pump Down Tester", layout = "grid")
app.set_full_screen()
usb_status = False
scale_status = False

def activate():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.HIGH)
    

def deactivate():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.LOW)

def exit_but():
    activate()
    app.destroy()
    exit()

try:
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate = 9600, parity=serial.PARITY_ODD, stopbits = serial.STOPBITS_ONE, bytesize=serial.SEVENBITS)
    scale_status = True
except:
    print("No scale connected!")
    app.warn("Warning", "Scale not connected. Continuing without capturing data.")
    scale_status = False
    
today = date.today()
d1=today.strftime("%d-%b-%Y")
filename = ""
diff = 0
prev = 0


def start_prog():
    buttonStart.disable()
    buttonStop.enable()
    buttonPause.enable()
    length.disable()
    delay.disable()
    dwell.disable()
    programName.disable()
    cb.disable()
    print("Start")
    global filename
    global remaining
    global usb_status
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
            buttonStart.enable()
            buttonStop.disable()
            buttonPause.disable()
            return
        calculateMins()
        filename = programName.value + "_"+ d1 + ".csv"
        #info("InfoBox", "Program Started:\n\n" + length.value + " cycles\nat " + delay.value + "s delay / "+ dwell.value + "s dwell."+ " \n\n" + "Filename: " +  filename)
        headerList = ['Number', 'Timestamp', 'Total', 'Difference']
        try:
            with open('/media/pi/USB/'+filename, 'w') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',')
                csv_writer.writerow(headerList)
            usb_status = True;
        except:
            app.warn("Warning", "No USB connected. Data will not be saved.\n(Drive must be named exactly 'USB')")
            usb_status = False;
        remaining = 0
        print(cb.value_text)
        if cb.value_text == "Touchless":
            app.repeat((int(delay.value)+int(dwell.value))*1000, deactivate);
            time.sleep(int(delay.value));
            app.repeat((int(delay.value)+int(dwell.value))*1000, cycle);
        else:
            app.repeat((int(delay.value)+int(dwell.value))*1000, cycle);
            time.sleep(int(delay.value))
            app.repeat((int(delay.value)+int(dwell.value))*1000, deactivate);
 
def cycle():
    global remaining
    global diff
    dashboard.value = "Cycles Remaining: " + str(int(length.value)-remaining) + " (" + str(round((int(length.value)-remaining)*(int(delay.value)+int(dwell.value))/60,1)) + " minutes)"
    last.value = "Last Dose: " + str(diff) + " grams"
    if remaining<int(length.value):
        remaining+=1
        activate()
        if (scale_status):
            writedata(remaining)
    else:
        activate()
        app.cancel(cycle)
        app.cancel(deactivate)
        buttonStart.enable()
        buttonPause.disable()
        buttonStop.disable()

def stop_prog():
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
    GPIO.cleanup()
    
def pause_prog():
    
    buttonStart.disable()
    buttonStop.enable()
    if buttonPause.text == "Pause":
        activate()
        app.cancel(cycle)
        app.cancel(deactivate)
        buttonPause.text= "Resume"
        print("pause")
    else:
        if cb.value_text == "Touchless":
            app.repeat((int(delay.value)+int(dwell.value))*1000, deactivate);
            time.sleep(int(delay.value));
            app.repeat((int(delay.value)+int(dwell.value))*1000, cycle);
        else:
            app.repeat((int(delay.value)+int(dwell.value))*1000, cycle);
            time.sleep(int(delay.value))
            app.repeat((int(delay.value)+int(dwell.value))*1000, deactivate);
        buttonPause.text = "Pause"
        print("Resume")

def calculateMins():
    global minutes
    minutes = int(length.value) / (int(delay.value) + int(dwell.value))
    minutes = round((minutes/60),1)

def writedata(count):
    global diff
    global prev
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    x = ser.readline()
    #print(x)
    try:
        x = float(x[3:10])
        diff = x-prev
        diff = round(diff,2)
        prev = x
    except ValueError:
        x = prev
        diff = 0
    global usb_status
    print(x)
    scale.value = "Current Weight: " +str(x) + " grams"
    data = str(count) + ","+ current_time + ","+ str(x) + "," + str(diff) + "\n"
    if (usb_status):
        with open("/media/pi/USB/" + filename, 'a') as fd:
            fd.write(data)
    ser.reset_input_buffer()
        


activate()



blanktext1 = Text(app, text="", size= 20, grid=[0,0])

box1= Box(app,border = True, grid=[0,1],align="left")
text_delay = Text(box1, text = "Delay:          ", align="left", size=50)
delay = TextBox(box1, align="left", width = 15)

delay.text_size = 50
delay.focus()
text_delay2 = Text(box1, text = "seconds", align="left", size = 50)

cb = ButtonGroup(app, options=["Touchless","Manual"], selected="Manual", align= "right", grid=[0,2])
cb.text_size = 25

box11 = Box(app,border = True, grid=[0,3],align="left")
text_dwell = Text(box11, text = "Dwell:          ", align = "left", size= 50)
dwell = TextBox(box11, align="left", width = 15)
dwell.text_size = 50
text_dwell2 = Text(box11, text = "seconds", align = "left", size=50)


blanktext11 = Text(app, text="", size = 40, grid=[0,4])

box2 = Box(app, border = True, grid=[0,5], align="left")
text_length = Text(box2, text ="Total Cycles:", align="left", size=50)
length = TextBox(box2, align="left", width = 15)
length.text_size= 50

blanktext2 = Text(app, text="", size= 40, grid=[0,6])

box3 = Box(app, border = True, grid=[0,7],align="left")
text_programName = Text (box3, text = "Filename:    ",size =50,align="left")
programName = TextBox(box3, width = 15, align="left")
text_programName2 = Text(box3, text = "_"+ d1 + ".csv        ", size = 50,align="left")
programName.text_size = 50

blanktext3 = Text(app, text="", size= 40, grid=[0,8])

box5 = Box(app, grid=[0,9], width="fill")
buttonStart = PushButton(box5, command=start_prog, text = "Start Pumpdown", width=20, height=2, align="left")
buttonStart.bg = "lightgreen"
buttonStart.text_size = 20
buttonStart.enable()
boxGap = Box(box5, width = 30, height = 3, align="left")
buttonPause = PushButton(box5, command=pause_prog, text = "Pause", width = 20, height=2, align = "left")
buttonPause.bg = "gold"
buttonPause.text_size = 20
buttonPause.disable()
boxGap2 = Box(box5, width = 30, height = 3, align="left")
buttonStop = PushButton(box5, command=stop_prog, text = "Stop", width=20, height=2, align="left")
buttonStop.bg = "tomato"
buttonStop.text_size = 20
buttonStop.disable()

box6 = Box(app, grid=[0,11], width = "fill")
buttonIn = PushButton(box6, command=deactivate, text = "Extend Arm", width = 10, height = 1, align = "left")
buttonIn.bg = "royal blue"
buttonOut = PushButton(box6, command=activate, text = "Retract Arm", width = 10, height = 1, align = "left")
buttonOut.bg = "royal blue"
blanktext4 = Text(app, text="", size= 40, grid=[0,10])

box4 = Box(app, layout = "grid", border = True, grid=[0,10], align = "left")
dashboard = Text(box4, text = "Cycles Remaining: " + length.value, grid=[0,0], size = 20,align= "left")
scale = Text(box4, text = "Scale Value: ", grid=[0,1], size = 20, align = "left")
last = Text(box4, text = "Last Dose: ", grid = [0,2], size = 20, align = "left")
blanktext5 = Text(app, text="", size =40, grid = [0,12])

exiter = PushButton(app, command=exit_but, text = "Exit", width = 20, height = 2, grid=[0,13], align = "bottom")
exiter.text_size = 20
exiter.bg = "indian red"

app.display()