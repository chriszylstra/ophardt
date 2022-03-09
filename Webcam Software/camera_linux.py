#LINUX VERSION
try:
    import cv2
except ImportError:
    print("You need cv2. Install it with 'pip install opencv-python --prefer-binary'")
    exit()
    
import time
import os
import pathlib
from datetime import datetime
from pathlib import Path

cam = cv2.VideoCapture(0)

now = datetime.now()
dt = now.strftime("%d_%m_%Y")
os.system('clear')
delay = input("Enter the delay time (seconds) between photos: ")
os.system('clear')
Path("/home/pi/Pictures/images/").mkdir(parents=True, exist_ok = True)
filepath = "images/" + dt + "/"

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
print ("Photos location: /home/pi/Pictures/" + filepath)
print ("Capturing every: " + delay + " seconds.")
print("*****")



try:
    while True:
        now = datetime.now()
        dt_string = now.strftime("%H_%M_%S")
        ret, image = cam.read()
        cv2.imwrite('/home/pi/Pictures/images/'+ str(dt_string) + '.jpg',image)
        time.sleep(int(delay))
except KeyboardInterrupt:   
    cam.release()
    cv2.destroyAllWindows()
except Exception as e:
    print(e)