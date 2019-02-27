# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 14:38:22 2018

@author: luiss
"""


from numpy import empty, zeros, full, sqrt, cos, sin, pi
from random import random, randint, seed
from pylab import figure, plot, show

# subplot(111)
# subplot(111).clear()
# pause


# pasos(m) distancia(dr)
#   100      5-20
#   200      5-60
#   300     10-30
#   500     20-40
#   1000    30-60
N = 1000      # numero de paseantes
m = 400      # numero de pasos de cada paseantedr = 10
dr = 10
r = dr
margin = 1

C=m+1       # posicion del centro
L=m*2+1     # longitud de las posiciones
posiciones = full((L,L), False)



#vecinos
nx = [-1, -1, -1, 0,  0, 1, 1,  1]
ny = [ 1,  0, -1, 1, -1, 1, 0, -1]
# randint(7)

def rand_move(raux):
    phi = random()*2*pi   
    return int(cos( phi ) * raux), int(sin( phi ) * raux)

seed(10)
posiciones[C,C] = True   #semilla inicial

i = 0
j = 0
while i < N:
    print("paso ",i)
    rx, ry = rand_move(r)
    x = C + rx
    y = C + ry
    j = 0
    while j < m:
        ran = randint(0,7)
        x += nx[ran]
        y += ny[ran]
        if (x-C)*(x-C) + (y-C)*(y-C) > (r + margin*dr)*(r + margin*dr):
            j=m
        for k in range(7):
            if posiciones[x + nx[k], y + ny[k]] == True:
                posiciones[x,y] = True
                i += 1
                j = m
                r = max(sqrt((C-x)*(C-x) + (C-y)*(C-y)) + dr, r)
                break
        j += 1


# print 
xplot=[]
yplot=[]
for i in range(L):
    for j in range(L):
        if posiciones[i,j] == True:
            xplot.append(i-C)
            yplot.append(j-C)
plot(xplot,yplot,'s')


"""
plot(range(N),x[:,1],'.-')
plot(range(N),x[:,2],'.-')
plot(range(N),x[:,3],'.-')

figure()
plot(x[:,1],y[:,1],'s-')
"""

