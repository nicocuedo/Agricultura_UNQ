#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 20:21:33 2019

@author: braso
"""


import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy import cos ,sin , pi 


# %%
# Print de las coordenadas en el mundo de un punto de interes en la imagen

A=np.load('tl_v2.npy')
p0=np.load('p0_l_v2.npy')

u0=p0[0]
v0=p0[1]
lat0_deg=p0[2]
lon0_deg=p0[3]

img=cv2.imread("/home/braso/Agricultura_UNQ/CorrecDeDist/Edit_new.jpg", cv2.IMREAD_GRAYSCALE)
plt.figure('Seleccionar campo de trabajo')
plt.imshow(img,'gray')

print('ELegir un punto de interés:\t\n',end=' ')
cy1,cx1=np.array(np.round(plt.ginput()[0]),dtype=np.int32)

vec=np.array([[cx1],[cy1],[cx1*cy1],[1]])

Coord_Mundo=np.dot(A,vec)
X_mundo=Coord_Mundo[0][0]
Y_mundo=Coord_Mundo[1][0]

print('Latitud y longitud :\t\n',np.round(Coord_Mundo,6))

# %%
#geodetic

a = 6378.1370#Equatorial radius in km
b = 6356.7523#Polar radius in km

lat0=np.deg2rad(lat0_deg)
lon0=np.deg2rad(lon0_deg)
lat1=np.deg2rad(X_mundo)
lon1=np.deg2rad(Y_mundo)

a_cos_cuad = (a*cos(lat0))**2
b_sin_cuad = (b*sin(lat0))**2
Rm = (a*b)**2/np.power(a_cos_cuad+b_sin_cuad,3/2) *1000#in meters
Rn = a**2 / np.sqrt(a_cos_cuad+b_sin_cuad)*1000#in meters

dlat= lat1-lat0
dlon= lon1-lon0
theta=np.arctan2(dlon,dlat)
deltaX=(dlon*cos(lat0)*Rn)/sin(theta) # en metros
deltaY=(dlat*Rm)/sin(theta)#cos(theta) # en metros

dist=np.linalg.norm([deltaX,deltaY]) # en metros
print('la distancia es {:.4f}\n en x {:.4f} \n en y {:.4f}'.format(dist,deltaX,deltaY))


# %%
#Elipsoidal Earth projected to a plane

a = 6378.1370#Equatorial radius in km
b = 6356.7523#Polar radius in km

lat0=np.deg2rad(lat0_deg)
lon0=np.deg2rad(lon0_deg)
lat1=np.deg2rad(X_mundo)
lon1=np.deg2rad(Y_mundo)

K1=111.13209-0.56605*cos((lat1+lat0))+0.00120*cos(2*(lat1+lat0))
K2=111.41513*cos((lat1+lat0)/2)-0.09455*cos((3*(lat1+lat0))/2)+0.00012*cos((5*(lat1+lat0))/2)
deltaY2=(K1*(lat1-lat0)*(180/pi))**2
deltaX2=(K2*(lon1-lon0)*(180/pi))**2

D=np.sqrt(deltaX2+deltaY2)*1000
X=np.sqrt(deltaX2)*1000
Y=np.sqrt(deltaY2)*1000

print('la distancia es {:.4f}\n en x {:.4f} \n en y {:.4f}'.format(D,X,Y))

