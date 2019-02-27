# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 16:50:55 2018
@author: luiss

CALCULO ENTROPIA
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
N = 300      # numero de paseantes
m = 400      # numero de pasos de cada paseante
dr = 10
r = dr
drmargin = int( 1 * dr)

mm = int(m/2)
C=mm+1       # posicion del centro
L=mm*2+1     # longitud de las posiciones
posiciones = full((L,L), False)


#vecinos
nx = [-1, -1, -1, 0,  0, 1, 1,  1]
ny = [ 1,  0, -1, 1, -1, 1, 0, -1]
# randint(7)

def rand_move(raux):
    phi = random()*2*pi   
    return int(cos( phi ) * raux), int(sin( phi ) * raux)

seed(11)
posiciones[C,C] = True   #semilla inicial

i = 0
j = 0

# Entropia
Entropy = [0]
lenentropy = 30
divS = int(N/lenentropy)
NN = 4 #longitud del tamaño donde calcularemos la entropia
indmax = L//NN
    

def Entropia(Npart):        
    entropia = zeros(indmax**2)
    for i in range(L):
        for j in range(L):
            if posiciones[i,j] == True:
                entropia[i//NN + indmax*(j//NN)] += 1
    S = 0
    for k in entropia:
        if k != 0:
            S += (k/Npart) * log(k/Npart)
    return S


while i < N:
    print("paso ",i)
    rx, ry = rand_move(r)
    x = rx
    y = ry
    j = 0
    while j < m:
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
                if(i%divS == 0):
                    Entropy.append(-Entropia(i))
                break
        j += 1


# print DAL
xplot=[]
yplot=[]
for i in range(L):
    for j in range(L):
        if posiciones[i,j] == True:
            xplot.append(i-C)
            yplot.append(j-C)
plot(xplot,yplot,'s')
title("DAL")
xlabel("Posicion X")
ylabel("Posicion Y")

# print Entropy
figure()
plot(range(len(Entropy)),Entropy,'o-')
title("Entropía por parícula S")
xlabel("Tiempo")
ylabel("Entropía S")
