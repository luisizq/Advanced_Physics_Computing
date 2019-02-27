# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 14:58:31 2018

@author: luiss

Practica 6
"""

from numpy import empty, zeros, sqrt, cos, sin, pi
from random import random, seed
from random import random, seed
from pylab import figure, plot, show

n = 10000       # numero de particulas
NS = 8      # Numero de lados del cuadrante
N = 100   # numero de pasos de cada paseante

#xdal=[]
#ydal=[]
#xdal.append(0)
#ydal.append(0)
dal=[(0,0)]
dr=10
r0= 0 + dr;

#x=zeros(N)
#y=zeros(N)

def rand_move(r):
    phi = random()*pi*2   
    return int(cos( phi ) * r), int(sin( phi ) * r)

for j in range(n):
    x, y = rand_move(r0)   
    for i in range(N):
        r=random()
        if r>0.75:
            x+=1
        elif r>0.5:
            x-=1
        elif r>0.25:
            y+=1
        else:
            y-=1
        
        
        if (x,y) in dal:
            if r>0.75:
                x-=1
            elif r>0.5:
                x+=1
            elif r>0.25:
                y-=1
            else:
                y+=1
            dal.append((x,y))
            aux=sqrt(x*x + y*y)
            if  aux + dr > r0:
                r0 = aux + dr

xplot=[]
yplot=[]
for i in range(len(dal)):
    xplot.append(dal[i][0])
    yplot.append(dal[i][1])
plot(xplot, yplot, 'o')   
        
"""
                if r>0.75:
            x[i+1]=x[j]+1
            y[j+1]=y[j]
        elif r>0.5:
            x[i+1]=x[i]-1
            y[i+1]=y[i]
        elif r>0.25:
            y[i+1]=y[i]+1
            x[i+1]=x[i]
        else:
            y[i]=y[i]-1
            x[i]=x[i]            
"""