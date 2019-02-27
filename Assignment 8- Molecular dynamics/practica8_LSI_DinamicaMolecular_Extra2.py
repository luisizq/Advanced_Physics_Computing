# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 21:57:36 2018

@author: luiss

DINAMICA MOLECULAR- Extra 2
"""

from numpy import sqrt, array, zeros, sign, histogram, linspace, exp
from numpy.random import uniform, random, seed
from pylab import plot,figure,xlabel, ylabel, title, show, legend
from matplotlib.pyplot import hist


# INICIALIZAR
seed(3)

N = 2           # numero de particulas por lado
NT = N*N        # numero de particulas total

#distancias
sigma = 1       # distancia que define el potencial de Lennard-Jones
a = 2 * sigma   # distancia inicial entre partículas
L = N * a       # tamaño de la caja
L2 = L/2        # es útil

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


# asegurarnos que las distancias están entre 0 y + L
rx -= (rx//L) * L
ry -= (ry//L) * L


rxini = rx
ryini = ry

v0 = 1

vx=[]
vy=[]

for i in range(NT):
    # uniform = valor aleatorio uniforme entre -v0 y v0
    vx.append(uniform(-v0,v0))
    vy.append(uniform(-v0,v0))
    
vx = array(vx)
vy = array(vy)

# posiciones anteriores
rxprev = rx - vx * dt
ryprev = ry - vy * dt

# asegurarnos que las distancias están entre 0 y + L
rxprev -= (rxprev//L) * L
ryprev -= (ryprev//L) * L



# vectores de posición para el segundo sistema
rx_2 = []
ry_2 = []

#Calculo de las posiciones:
ddr = sigma/100    # distancia de variación aleatoria con respecto al caso inicial
for i in range(NT):        
    rx_2.append(rx[i] + 2*(random()-0.5)*ddr)
    ry_2.append(ry[i] + 2*(random()-0.5)*ddr) 

rx_2 = array(rx_2)
ry_2 = array(ry_2)

# asegurarnos que las distancias están entre 0 y L
rx_2 -= (rx_2//L) * L
ry_2 -= (ry_2//L) * L

vx_2 = vx
vy_2 = vy

# posiciones anteriores
rxprev_2 = rx_2 - vx_2 * dt
ryprev_2 = ry_2 - vy_2 * dt

# asegurarnos que las distancias están entre 0 y + L
rxprev_2 -= (rxprev_2//L) * L
ryprev_2 -= (ryprev_2//L) * L


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
    
    # asegurarnos que las distancias están entre 0 y L
    xnext -= (xnext//L) * L
    ynext -= (ynext//L) * L

    # se devuelven: pos. antiguas, pos. nuevas y vel. nuevas
    return x, y, xnext, ynext, vxnext, vynext



### ACTUALIZACION
Npasos = 1000    # Numero de tiempos

figure(1)
DR = []

nn = 4

for i in range(Npasos):
    print(i)
    
    rxprev, ryprev, rx, ry, vx, vy = Verlet(rxprev,ryprev,rx,ry,vx,vy)
    rxprev_2, ryprev_2, rx_2, ry_2, vx_2, vy_2 = Verlet(rxprev_2,ryprev_2,rx_2,ry_2,vx_2,vy_2)
    
    DR.append( sqrt((rx-rx_2)**2 + (ry-ry_2)**2))
    
    figure(1)
    plot(rx  ,ry  ,'.b',markersize=nn)
    plot(rx_2,ry_2,'.r',markersize=nn)
    

figure(1)
plot(rxini,ryini,'ok',label="Inicio")
plot(rx,ry,'ob',label="Sistema 1")
plot(rx_2,ry_2,'or',label="Sistema 2")


plot([0,L,L,0,0],[0,0,L,L,0],'g')      # para pintar la caja
xlabel("Posiciones eje X")
ylabel("Posiciones eje Y")
title("Evolución de 2 sistemas con pequeña variación en C. Iniciales")
legend()


figure()
plot(DR)
xlabel("Tiempo t")
ylabel("Separacion")
title("Ejemplo del caos")
