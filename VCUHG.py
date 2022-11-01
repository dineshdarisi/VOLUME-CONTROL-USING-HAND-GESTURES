#VOLUME CONTROL USING HAND GESTURE
#edited by: DINESH DARISI
#Dt. 26/10/22
'''-------------------------------------------------'''

#importing all neccesary modules, do install protobuf
#protobuf stands for Protocol Buffers and is used widely for video applications and to store data in sequence
#pip install opencv-python 
import cv2 

#mediapipe library has the body parts recognition librarires. e.g.: it loactes 21 points on the palm 
import mediapipe as mp

import math
import numpy as np

#importing the pycaw module with its boiler plate directly from GitHub 
#pycaw is the audio library in python
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volumeRANGE=volume.GetVolumeRange()
print(volumeRANGE)
minvol=volumeRANGE[0]
maxvol=volumeRANGE[1]
#volume.SetMasterVolumeLevel(-65.25, None)           

mphands=mp.solutions.hands

#detect a hand and track it
hands=mphands.Hands()        
mpDraw=mp.solutions.drawing_utils

#opening camera and capturing videos
camera = cv2.VideoCapture(0)

while True:
    ret, img = camera.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)          
    results=hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:

            #enumerate: (0,seq[0])
            for id, lm in enumerate(handlms.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w), int(lm.y*h)          #landmark is ratio and multiplying it wil give exact point on hands


                #location of tip of thumb in hands unction of mediapipe, can change this value, 
                # visit:https://www.analyticsvidhya.com/blog/2021/07/building-a-hand-tracking-system-using-opencv/   
                             
                if id==4: 
                    x1,y1=cx,cy
                    #on image draw a circle with center cx,cy thickness 25, color code
                    cv2.circle(img, (x1,y1), 15, (255,255,255), cv2.FILLED)            

                #location of tip of index finger                                                                             
                if id==8:
                    x2,y2=cx,cy
                    cv2.circle(img, (x2,y2), 15, (255,255,255), cv2.FILLED)      

            #distance formula to create a representation of level of volume in accordance with the distance between fingers
            #hypot gives sqrt[(x2-x1)^2+(y2-y1)^2]
            distance=math.hypot(x2-x1, y2-y1)
            print(distance)

            #creating line which gives the representation 
            cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 5)
            vol=np.interp(distance, [10, 290], [minvol,maxvol])
            per=np.interp(distance, [10,290], [0,100])
            print (per)

            volume.SetMasterVolumeLevel(vol,None)
                        
            #since we are using inside for loop, circle will be below mediapipe outputs 

            print(id,cx,cy)            
            mpDraw.draw_landmarks(img,handlms,mphands.HAND_CONNECTIONS)   

    print(results)
    cv2.imshow("frame",img)
    
    #to break out of while true statement and close the application press q 
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cv2.destroyAllWindows()
camera.release()


