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


cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(2)





if not(cam1.isOpened()):
    print("")
    print("Error opening camera. Exiting...")
    time.sleep(5)
    exit()
if not (cam2.isOpened()):
    print("")
    print("Detected only 1 camera. Continuing....")
    time.sleep(2)

    
cam1.set(3,1920)
cam1.set(4,1080)
cam2.set(3,1920)
cam2.set(4,1080)



now = datetime.now()
dt = now.strftime("%d_%m_%Y")

os.system('clear')
delay = input("Enter the delay time (seconds) between photos: ")
os.system('clear')
Path("/home/pi/Pictures/images/"+dt).mkdir(parents=True, exist_ok = True)
filepath = "images/" + dt + "/"

print("----------------------------Webcam Autocapture-----------------------------")
print("")
print("Software written by Chris Zylstra. February 2022.")
print("")
print("")
print("WARNING: Leaving this program running may consume large amounts of disk space.")
print("Images are ~400KB each. (1GB = ~ 2,500 photos)")
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
        ret, image = cam1.read()
        ret2, image2 = cam2.read()
        cv2.normalize(image,image,0,255,cv2.NORM_MINMAX)
        cv2.normalize(image2,image2,0,255,cv2.NORM_MINMAX)
        cv2.imwrite('/home/pi/Pictures/'+ filepath + str(dt_string) + '.jpg',image)
        #missing a line here for writing camera two. I can figure it out tho. 
        time.sleep(int(delay))
except KeyboardInterrupt:   
    cam1.release()
    cam2.release()
    cv2.destroyAllWindows()
except Exception as e:
    print(e)
