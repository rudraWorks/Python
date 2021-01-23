passwrd='###@@@777rps'


from cv2 import cv2
import pymsgbox
import time as t
import numpy as np
import smtplib 
from os import system as s
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os 
from email.mime.multipart import MIMEMultipart
import winsound as beep
s('cls')

   
############### security survilliance for house ###############

def sendmail(file):
    pymsgbox.alert(text="Process Initiated",title="OpenCV Hawk",timeout=1200)
    print('process initiated')
    img_data=open(file,'rb').read()
    msg=MIMEMultipart()
    msg['Subject']='Attention!!!! '
    msg['From']='merudra754'
    msg['To']='rudra'

    text=MIMEText(f'An unwanted event has just happened!\nTimestamp:{t.ctime(t.time())}\nHere is the picture of the burglar:')
    msg.attach(text)
    image=MIMEImage(img_data,name=os.path.basename(file))
    msg.attach(image)



    send=smtplib.SMTP_SSL("smtp.gmail.com",465)
    send.login('merudra754@gmail.com',passwrd)
    send.sendmail('merudra754@gmail.com','srudra754@gmail.com',msg.as_string())
    print('success')
    pymsgbox.alert(text="Success",title="OpenCV Hawk",timeout=1200)
    send.quit()

cam=cv2.VideoCapture(0)

flag=True
while cam.isOpened():
       ret,frame1=cam.read()
       ret,frame2=cam.read()
       
       cv2.imshow('original frame',frame1)
       
       emailImg=cam.read()[1]
       frame1=frame1[290:480,320:490]
       frame2=frame2[290:480,320:490]
       black=np.zeros(frame1.shape,np.uint8)

       diff=cv2.absdiff(frame1,frame2)
       diff=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
       diff=cv2.GaussianBlur(diff,(5,5),0)
       ret,diff=cv2.threshold(diff,34,255,cv2.THRESH_BINARY)
       diff=cv2.dilate(diff,None,iterations=3)
       contours,_=cv2.findContours(diff,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
       cv2.drawContours(frame1,contours,-1,(0,255,255),2)
       
       path=f'opencv tut/{t.ctime(t.time())[11:19]}.png'.replace(':','')
       for c in contours:
            if cv2.contourArea(c)<7000:
               continue
            x,y,w,h=cv2.boundingRect(c)
            cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,255),4)
            cv2.rectangle(black,(x,y),(x+w,y+h),(0,255,255),-1) 

            if flag:
               pass
               cv2.imwrite(path,emailImg)
               sendmail(path) 
            flag=False
            #cv2.imwrite('hi.png',emailImg)
              
       mask_stack=np.hstack((frame1,black))
       cv2.imshow('colored mask',mask_stack)
       #cv2.imshow('black mask',black)
       #cv2.imwrite(path,mask_stack)

       if cv2.waitKey(1)==27:
           break
cam.release
cv2.destroyAllWindows()        
