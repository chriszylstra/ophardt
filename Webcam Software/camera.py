import cv2
import os
import time
import pathlib
from pathlib import Path
from datetime import datetime

now = datetime.now()
dt = now.strftime("%d_%m_%Y")
Path("images\\" + dt).mkdir(parents=True, exist_ok = True)
filepath = "images\\" + dt + "\\"


camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)
    
clearConsole()
delay = input("Enter the delay time (seconds) between photos: ")
clearConsole()

print("----------------------------Webcam Autocapture-----------------------------")
print("")
print("Software written by Chris Zylstra. February 2022.")
print("")
print("")
print("WARNING: Leaving this program running may consume large amounts of disk space.")
print("Images are ~70KB each. (1GB = ~ 14,000 photos)")
print("")
print("This program captures and saves the webcam and saves it to a directory.")
print("Used for Pumpdown testers in creating timelapses.")
print("")
print("*****")
print ("Press CTRL+C in this window to quit.")
print ("Photos location: " + str(pathlib.Path(__file__).parent.resolve()) + "\\"+ filepath)
print ("Capturing every: " + delay + " seconds.")
print("*****")



try:
    while True:
        now = datetime.now()
        dt_string = now.strftime("%H_%M_%S")
        return_value, image = camera.read()
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        cv2.imwrite(filepath + dt_string+".jpg",image)
        time.sleep(int(delay))
except KeyboardInterrupt:
    camera.release()
    cv2.destroyAllWindows()
except Exception as e:
    print(e)

