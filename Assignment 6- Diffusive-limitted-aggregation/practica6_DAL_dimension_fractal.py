# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 15:59:01 2018

@author: luiss
CALCULO DIMENSION FRACTAL
"""


from numpy import linspace, zeros, full, sqrt, log, cos, sin, pi, array
from random import random, randint, seed
from pylab import figure, plot, show, polyfit, xlabel, ylabel, title



# pasos(m) distancia(dr)
#   100      5-20
#   200      5-60
#   300     10-30
#   500     20-40
#   1000    30-60
N = 800      # numero de paseantes
m = 400      # numero de pasos de cada paseantedr = 10
dr = 10
r = dr
drmargin = int( 1 * dr)

m = 400         # numero de pasos de cada paseantedr = 10
C=m+1           # posicion del centro
L=m*2+1         # longitud de las posiciones
posiciones = full((L,L), False)

posiciones[C,C] = True   #semilla inicial
posiciones[C+1,C] = True   #semilla inicial
posiciones[C,C+1] = True   #semilla inicial
posiciones[C+1,C+1] = True   #semilla inicial

#vecinos
nx = [-1, -1, -1, 0,  0, 1, 1,  1]
ny = [ 1,  0, -1, 1, -1, 1, 0, -1]

def rand_move(raux):
    phi = random()*2*pi   
    return int(cos( phi ) * raux), int(sin( phi ) * raux)

seed(9)


i = 0
j = 0
while i < N:
    print("paso ",i)
    #posicion inicial
    rx, ry = rand_move(r)
    x = rx
    y = ry
    j = 0       #indice del paso
    while j < m:    #realizar el camino aleatorio
        ran = randint(0,7)
        x += nx[ran]
        y += ny[ran]
        if x*x + y*y > (r + drmargin)*(r + drmargin):
            j=m
        for k in range(7):
            if posiciones[x + C + nx[k], y + C + ny[k]] == True:
                posiciones[x + C, y + C] = True
                i += 1
                j = m
                r = max(sqrt(x*x + y*y) + dr, r)
                break
        j += 1


# Dibujar el cúmulo 
xplot=[]
yplot=[]
for i in range(L):
    for j in range(L):
        if posiciones[i,j] == True:
            xplot.append(i-C)
            yplot.append(j-C)
figure()
title("Cumulo DAL")
xlabel("Posicion X")
ylabel("Posicion Y")
plot(xplot,yplot,'s')


# obtener la dimension fractal
x = array(xplot)
y = array(yplot)
r = sqrt( x*x + y*y )       #vector de distancias al centro

rmax =  max(r)
Ndiv = 30
rplot = linspace(0,rmax, Ndiv)
count = zeros(Ndiv)

for i in r:
    # posicion de la particula i con respecto a rmax
    nn = int(i / rmax * Ndiv)   
    # dicha partícula contribuye a la masa a partir de nn hasta Ndiv
    for j in range(nn, Ndiv):   
        count[j] += 1
        
#representación de los datos
figure()
auxx=log(rplot)
auxy=log(count)
plot(auxx, auxy,'.-')
title("Obtención de la dimensión fractal")
xlabel("log(r)")
ylabel("log(m)")

p,r=polyfit(auxx[2:9],auxy[2:9],1)
xfit = linspace(1,log(rmax),1000)
yfit = p * xfit + r
plot(xfit,yfit,'-r')

