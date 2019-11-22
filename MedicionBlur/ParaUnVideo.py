# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 16:46:10 2019

@author: BraianSoullier
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt 
from glob import glob
import pandas as pd 

videos=glob("/home/braso/Escritorio/Videos calib 191113/*.MP4")
videos.sort()
strings=np.load('/home/braso/Agricultura_UNQ/MedicionBlur/shutters.npy')
heights=np.round(np.load('/home/braso/Agricultura_UNQ/MedicionBlur/list_Height.npy'))


# %%   Ver todo los videos con el umbral del patron

starts=np.load('/home/braso/Agricultura_UNQ/MedicionBlur/starts.npy')
ends=np.load('/home/braso/Agricultura_UNQ/MedicionBlur/ends.npy')

for counter,file in enumerate(videos):
    cap = cv2.VideoCapture(file)
    print("Archivo=",file)
    if(strings[counter]=="1/60."):
        umbral=200-((heights[counter]-min(heights))*5)
    if(strings[counter]=="1/120"):
        umbral=160-((heights[counter]-min(heights))*5)
    if(strings[counter]=="1/240"):
        umbral=120-((heights[counter]-min(heights))*5)
    if(strings[counter]=="1/160"):
        umbral=140
    print("umbral",umbral)
    print("Counter",counter)
    cap.set(cv2.CAP_PROP_POS_FRAMES,starts[counter]+40)
    cont=starts[counter]
    while(cap.isOpened()):
        ret, frame = cap.read()
        cont+=1
        if (cont==ends[counter]):
            break
        if(ret!=False):
            img=cv2.resize(frame,(1240,640))
            cv2.imshow('frame',img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame',img)
            ja,imgB=cv2.threshold(gray,umbral,255,cv2.THRESH_BINARY)
            kernel=np.array(([0,1,0],[1,1,1],[0,1,0]),np.uint8)
#            kernel= np.ones([5,5])
            imgB=cv2.morphologyEx(imgB,cv2.MORPH_OPEN,kernel)
            imgC,cnt,hr=cv2.findContours(imgB,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(imgB,cnt,-1,(127,0,0),5)
            cv2.imshow("Contorno",imgB)
            print('\r' , cap.get(cv2.CAP_PROP_POS_FRAMES),end='')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            cap.release()
    cap.release()
    cv2.destroyAllWindows()
    print('\n')



# %%
def umbralDetection(counter):
    umbral=0
    if(strings[counter]=="1/60."):
        umbral=190
    if(strings[counter]=="1/120"):
        umbral=150
    if(strings[counter]=="1/240"):
        umbral=110
    if(strings[counter]=="1/160"):
        umbral=110
    return umbral 






























# %%
LapALL=[]
for vid in videos :
    cap = cv2.VideoCapture(vid)
    if (cap.isOpened()== True): 
        print("Opening video stream or file")
    counter=0
    Laplacian=[]
    while(cap.isOpened()):
        ret, frame = cap.read()
        counter+=1
        if( ret == True):
            lap=cv2.Laplacian(frame,cv2.CV_64F).var()
            Laplacian.append(lap)
#  counter+=1
#  img=cv2.resize(frame,(1240,640))
##  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#  cv2.imshow('frame',img)   
        print("contador",counter)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    LapALL.append(Laplacian)
    cap.release()
    cv2.destroyAllWindows()


#end_time= time.time()
#
#print("Elapsed time: %.10f seconds." % (end_time - start_time))






























# %% Buscando el patron de puntos para hacer una mascara y calcular el laplaciano solo donde aparece el patron
file=videos[28]
cap = cv2.VideoCapture(file)
#cap.set(cv2.CAP_PROP_POS_FRAMES,570)
while(cap.isOpened()):
    ret, frame = cap.read()
    img=cv2.resize(frame,(1240,640))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#gray=cv2.resize(gray,(1240,640))
#    cv2.imshow('frame',img)
#    ja,imgB=cv2.threshold(gray,120,255,cv2.THRESH_BINARY)
#    ret,th1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,2001,2)
    th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,2001,2)
    cv2.imshow("C1",th2)
    cv2.imshow("C2",th3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
                break
cap.release()
cv2.destroyAllWindows()




