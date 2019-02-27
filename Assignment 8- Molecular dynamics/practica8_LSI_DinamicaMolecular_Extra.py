# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 21:37:00 2018

@author: luiss

DINAMICA MOLECULAR- Extra 1
"""

from numpy import sqrt, array, zeros, sign, histogram, linspace, exp
from numpy.random import uniform, random, seed
from pylab import plot,figure,xlabel, ylabel, title, show, legend
from matplotlib.pyplot import hist


# INICIALIZAR
seed(1)

N = 4          # numero de particulas por lado
NT = N*N        # numero de particulas total

#distancias
sigma = 1       # distancia que define el potencial de Lennard-Jones
a = 2 * sigma   # distancia inicial entre partículas
L = N * a       # tamaño de la caja

rcorte = 4 * sigma      # distancia a partir de la cual no hay interacción
rcorte2 = rcorte**2     # es útil

dt = 0.02               # paso de tiempo en la integración
d2t = 2 * dt            # es útil
dt2 = dt**2             # es útil


# vectores de posición
rx = []
ry = []

#Calculo de las posiciones:
dr = sigma/2    # distancia de variación aleatoria
for i in range(N):
    for j in range(N):        
        rx.append(i*a + 2*(random()-0.5)*dr)
        ry.append(j*a + 2*(random()-0.5)*dr) 
       

rx = array(rx)
ry = array(ry)

rxini = rx
ryini = ry

# asegurarnos que las distancias están entre 0 y L
rx -= (rx//L) * L
ry -= (ry//L) * L


v0 = 1

vx=[]
vy=[]

for i in range(NT):
    # uniform = valor aleatorio uniforme entre -v0 y v0
    vx.append(uniform(-v0,v0))
    vy.append(uniform(-v0,v0))
    
vx = array(vx)
vy = array(vy)
v  = sqrt(vx**2 + vy**2)

# posiciones anteriores
rxprev = rx - vx * dt
ryprev = ry - vy * dt

# asegurarnos que las distancias están entre 0 y + L
rxprev -= (rxprev//L) * L
ryprev -= (ryprev//L) * L




### FUNCIONES
def Force(x,y,L):
    #vectores de fuerza
    fx, fy = zeros(NT,float), zeros(NT,float)
    #recorrer todos los pares
    for i in range (NT):
        for j in range(i+1,NT):   # condición para recorrer los pares
            r2min = (x[i]-x[j])**2 + (y[i]-y[j])**2
            dx, dy = x[i]-x[j], y[i]-y[j]
            # aplicar las condiciones de contorno
            for dlx in [-L,0,L]:
                for dly in [-L,0,L]:
                    r2 = (x[i]-x[j] + dlx)**2 + (y[i]-y[j] + dly)**2
                    if r2 < r2min:
                        r2min = r2
                        dx, dy = x[i]-x[j] + dlx, y[i]-y[j] + dly
            r2 = r2min

            # calculo para las que si que interactúan
            if r2 < rcorte2:
                # formula de la fuerza 
                # (depende de si son discos rígidos o Lennard-Jones)
                # Caso1 : interacción de Lennard-Jones
                rm8 = 1 / r2**4         
                aux = 24 * rm8 * ( 2 / r2**3 - 1 )        
                fx[i] += aux * dx   # coseno
                fy[i] += aux * dy   # seno
                fx[j] -= aux * dx   # coseno
                fy[j] -= aux * dy   # seno
                
    return fx, fy

def Verlet(xold,yold,x,y,vx,vy):
    #calculo de la fuerza
    Fx, Fy = Force(x,y,L)
    
    # calculo de las nuevas posiciones
    xnext = 2 * x - xold + Fx * dt2
    ynext = 2 * y - yold + Fy * dt2
    
    # calculo de las nuevas velocidades
    vxnext = (xnext - xold) / d2t
    vynext = (ynext - yold) / d2t
    
    # aplicar las condiciones de contorno
    xnext -= xnext//L * L
    ynext -= ynext//L * L
    
    # se devuelven: pos. antiguas, pos. nuevas y vel. nuevas
    return x, y, xnext, ynext, vxnext, vynext



### ACTUALIZACION
Npasos = 100    # Numero de tiempos

figure()
#calcular la ida
for i in range(Npasos):
    print(i)
    rxprev, ryprev, rx, ry, vx, vy = Verlet(rxprev,ryprev,rx,ry,vx,vy)
    plot(rx,ry,'.b',markersize=1)

#plot(rx,ry,'.b',markersize=1, label="IDA")
plot(rxini,ryini,'oc',label="Inicio Ida")
plot(rx,ry,'ok',label="Fin Ida - Inicio Vuelta")

plot([0,L,L,0,0],[0,0,L,L,0],'g')      # para pintar la caja
xlabel("Posiciones eje X")
ylabel("Posiciones eje Y")
title("Dinámica molecular IDA")
legend()

#dar la vuelta
vx = -vx
vy = -vy

rx_aux = rx
ry_aux = ry

rx = rxprev
ry = ryprev

rxprev = rx_aux
ryprev = ry_aux

rxini = rx
ryini = ry

#calcular la vuelta
figure()
for i in range(Npasos):
    print(i)
    rxprev, ryprev, rx, ry, vx, vy = Verlet(rxprev,ryprev,rx,ry,vx,vy)
    plot(rx,ry,'.r',markersize=1)

#plot(rx,ry,'.r',markersize=1, label="VUELTA")    
plot(rxini,ryini,'ok',label="Fin Ida- Inicio Vuelta")
plot(rx,ry,'og',label="Fin vuelta")

plot([0,L,L,0,0],[0,0,L,L,0],'g')      # para pintar la caja
xlabel("Posiciones eje X")
ylabel("Posiciones eje Y")
title("Dinámica molecular VUELTA")
legend()
