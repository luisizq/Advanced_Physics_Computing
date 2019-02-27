# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 13:54:32 2018

@author: luiss

VIDEO
"""

from numpy import empty, zeros, full, delete, array, sqrt, cos, sin, pi
from numpy.random import random, randint, seed
from pylab import figure, plot, pause, subplot, title, xlabel, ylabel

m = 30                  # Tamaño de la caja
C=m+1                   # posicion del centro
L=m*2+1                 # longitud de las posiciones
posiciones = full((L,L), False)
posiciones[C,C] = 1     #semilla inicial
xplot, yplot = [0], [0] 

nx = array([-1, -1, -1, 0,  0, 1, 1,  1])
ny = array([ 1,  0, -1, 1, -1, 1, 0, -1])

x, y = [], []
espaciado = 2
lx = 0
while lx < L:
    ly = 0
    while ly < L:
        x.append(lx), y.append(ly)
        ly += espaciado
    lx += espaciado
x = array(x)
y = array(y)

N = len(x)      # numero de paseantes
M = 100         # numero de pasos

seed(1)
figure()
title("DAL")
xlabel("Posicion X")
ylabel("Posicion Y")
steps = 1000
for i in range(steps):
    # numero aleatorio
    a = randint(8, size = len(x))
    # moverlo
    x += nx[a]
    y += ny[a]
    # que esté dentro de los limites
    x = x%L
    y = y%L
    # analizar si se tiene que quedar fija
    indexlist = []

    for index in range(len(x)):
        for k in range(8):
            if (x[index]+nx[k])>0 and (x[index]+nx[k])<L and (y[index]+ny[k])>0 and (y[index]+ny[k])<L:
                if posiciones[x[index] + nx[k], y[index] + ny[k]] == True:
                    posiciones[x[index],y[index]]=True
                    xplot.append(x[index] - C)
                    yplot.append(y[index] - C)
                    indexlist.append(index)
                    break
    x=delete(x,indexlist)
    y=delete(y,indexlist)
    
    print(steps-i)
    
    # print
    subplot(111).clear()
    subplot(111)
    title("DAL")
    xlabel("Posicion X")
    ylabel("Posicion Y")
    plot(x-C,y-C,".b")
    plot(xplot, yplot,"sr",markersize=4)
    pause(0.001) 
    
    if len(x) == 0:
        break
 
