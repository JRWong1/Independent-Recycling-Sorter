#Abhishek Hariharan & Jonathan Wong
#Independent Recycling Sorter
#Credits to a Wide Variety of Sources, as shown in the shortcuts file
#Big Credit to Dexter Industries too
#Let's Make Recycling Great Again!


############################### declarations
import argparse
import base64
import picamera
import json
import os

import argparse
import io

import RPi.GPIO as GPIO, time, os

from time import sleep
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
GPIO.setmode(GPIO.BOARD)

import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
############################### Declarations End


############################### Motor Related
a1 = 3 # blue
a2 = 5 # pink
a3 = 7 # yellow
a4 = 11 # orange

b1 = 13
b2 = 15
b3 = 19
b4 = 21

c1 = 23
c2 = 29
c3 = 31
c4 = 33

d1 = 8
d2 = 10
d3 = 12
d4 = 16

StepCount = 8
Seq = range(0, StepCount)
Seq[0] = [0,1,0,0]
Seq[1] = [0,1,0,1]
Seq[2] = [0,0,0,1]
Seq[3] = [1,0,0,1]
Seq[4] = [1,0,0,0]
Seq[5] = [1,0,1,0]
Seq[6] = [0,0,1,0]
Seq[7] = [0,1,1,0]
 

GPIO.setup(a1 , GPIO.OUT)
GPIO.setup(a2 , GPIO.OUT)
GPIO.setup(a3 , GPIO.OUT)
GPIO.setup(a4 , GPIO.OUT)
GPIO.setup(b1 , GPIO.OUT)
GPIO.setup(b2 , GPIO.OUT)
GPIO.setup(b3 , GPIO.OUT)
GPIO.setup(b4 , GPIO.OUT)
GPIO.setup(c1 , GPIO.OUT)
GPIO.setup(c2 , GPIO.OUT)
GPIO.setup(c3 , GPIO.OUT)
GPIO.setup(c4 , GPIO.OUT)
GPIO.setup(d1 , GPIO.OUT)
GPIO.setup(d2 , GPIO.OUT)
GPIO.setup(d3 , GPIO.OUT)
GPIO.setup(d4 , GPIO.OUT)

 
def setStep1(w1, w2, w3, w4):
    GPIO.output(a2 , w1)
    GPIO.output(a4 , w2)
    GPIO.output(a1 , w3)
    GPIO.output(a3 , w4)

def setStep2(w1, w2, w3, w4):
    GPIO.output(b2 , w1)
    GPIO.output(b4 , w2)
    GPIO.output(b1 , w3)
    GPIO.output(b3 , w4)

def setStep4(w1, w2, w3, w4):
    GPIO.output(d2 , w1)
    GPIO.output(d4 , w2)
    GPIO.output(d1 , w3)
    GPIO.output(d3 , w4)
 
def forward(t,a):
    q = 50
    if t==1:
        q=50
    if a==1 and t==1:
        q=47
    if a == 3 and t==4:
        q=50
    if a==4 and t==4:
        q=30
    for i in range(q):
        for j in range(StepCount):
            if t == 1:
                setStep1(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            if t == 2:
                setStep2(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            if t == 3:
                setStep3(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            if t == 4:
                setStep4(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(1.0/1000.0)

def back(t,a):
    q = 50
    if t==1:
        q=48
    if t==1 and a ==1:
        q=50
    if a == 3 and t == 4:
        q=40
    if a == 4 and t==4:
        q=29
    for i in range(q):
        for j in reversed(range(StepCount)):
            if t == 1:
                setStep1(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            if t == 2:
                setStep2(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            if t == 3:
                setStep3(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            if t == 4:
                setStep4(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(1.0/1000.0)


############################### Motor Related End

############################### Camera


def takephoto():
    camera = picamera.PiCamera()
    camera.vflip = True
    camera.hflip = True
    camera.sensor_mode = 6
    camera.brightness = 55
    
    time.sleep(1)
    
    camera.capture('/home/pi/testimage.jpg')
   
    camera.close()
############################### Camera End


############################### FSR
def RCtime (RCpin):
        reading = 0

        GPIO.setup(RCpin, GPIO.OUT)
        
        GPIO.output(RCpin, GPIO.LOW)
        time.sleep(0.1)
 
        GPIO.setup(RCpin, GPIO.IN)
    
        while (GPIO.input(RCpin) == GPIO.LOW):
                reading += 1
        return reading
 


def touch():
    print "\n\nPlease push an object on the sensor so that this thing can finna be operational k thx"
    test = 0
    
    while (test < 1):                                     
        print RCtime(40) 
        GPIO.output(38,GPIO.HIGH)
        print "\n\n\n\nWoohoo the led turned on yee\n\n\n"
        
        test = 1
############################### FSR End
   
        
############################### Program Main
def main():
    rejectcounter = 0  
    GPIO.setup(38, GPIO.OUT)
    GPIO.output(38, GPIO.LOW)
    
    while True:
        t = 99 
        touch()
        while rejectcounter != 3 and t > 80:
            takephoto() 
            """Run a label request on a single image"""

            credentials = GoogleCredentials.get_application_default()
            service = discovery.build('vision', 'v1', credentials=credentials)

            with open('testimage.jpg', 'rb') as image:
                image_content = base64.b64encode(image.read())
                service_request = service.images().annotate(body={
                    'requests': [{
                        'image': {
                            'content': image_content.decode('UTF-8')
                        },
                        'features': [{
                            'type': 'WEB_DETECTION',
                            'maxResults': 10
                        }]
                    }]
                })
                response = service_request.execute()
                k = json.dumps(response, indent=4, sort_keys=True)

            
            
                
                with open('jsonfile.txt', 'w') as f:
                    f.write(k)
                if 'Kirkland' in open('jsonfile.txt').read() or 'Milk' in open('jsonfile.txt').read():
                    print("Carton")
                    print ("case a")
                    t = 1
                elif 'Poland' in open('jsonfile.txt').read():
                    print("Plastic Bottle")
                    t = 3
                elif 'kirkland' in open ('jsonfile.txt').read() or 'MILK' in open('jsonfile.txt').read() or 'KIRKLAND' in open('jsonfile.txt').read():
                    print("Carton")
                    print ("case a up/lower case")
                    t = 1
                elif 'Cattle' in open('jsonfile.txt').read() or 'cattle' in open('jsonfile.txt').read() or 'Axxis Consulting' in open('jsonfile.txt').read() or 'Dairy' in open('jsonfile.txt').read():
                    print("Carton")
                    print ("case b")
                    t = 1
                elif 'Cola' in open('jsonfile.txt').read() or 'Fire' in open('jsonfile.txt').read() or 'coca cola' in open('jsonfile.txt').read() or 'Coca' in open('jsonfile.txt').read():
                    print("Aluminum Can")
                    t = 2
                elif 'Soft Drink' in open('jsonfile.txt').read() or 'Lip' in open('jsonfile.txt').read() or 'Soft drink' in open('jsonfile.txt').read() or 'Carbonated water' in open('jsonfile.txt').read():
                    print("Aluminum Can")
                    t = 2
                elif 'Water' in open('jsonfile.txt').read() or 'Plastic' in open('jsonfile.txt').read():
                    print("Plastic Bottle")
                    t = 3
                elif 'Cylinder' in open('jsonfile.txt').read():
                    print("Plastic Bottle")
                    t = 3
                elif 'Bottle' in open('jsonfile.txt').read():
                    print("Plastic Bottle")
                    t = 3
                elif 'Pound' in open('jsonfile.txt').read() or 'Chicken' in open('jsonfile.txt').read() or 'chicken' in open('jsonfile.txt').read() or 'Ounce' in open('jsonfile.txt').read():
                    print("Carton")
                    print ("case c")
                    t = 1
		elif 'Carton' in open('jsonfile.txt').read() or 'Font' in open('jsonfile.txt').read():
                    print("Carton")
                    print ("case omega")
                    t = 1
                else:
                    print("Reject")
                    rejectcounter += 1
                    if rejectcounter == 3:
                        t = 4
                    
        if rejectcounter == 3:
            print("True Reject")
            t = 4
                
        if t == 1:
            back(2,t)
            back(1,t)
            time.sleep(3)
            forward(1,t)
            forward(2,t)
        elif t == 2:
            forward(2,t)
            back(1,t)
            time.sleep(3)
            forward(1,t)
            back(2,t)
        elif t == 3:
            back(4,t)
            forward(1,t)
            time.sleep(3)
            back(1,t)
            forward(4,t)
        elif t == 4:
            forward(4,t)
            forward(1,t)
            time.sleep(3)
            back(1,t)
            back(4,t)
            
        rejectcounter = 0
        t = 99
        f.close()
            
        time.sleep(5)
        GPIO.output(38, GPIO.LOW)
    GPIO.cleanup()

        

if __name__ == '__main__':

    main()

############################### Program Main End
