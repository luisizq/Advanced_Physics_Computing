# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 14:33:02 2018

@author: luiss

DINAMICA MOLECULAR
"""

from numpy import sqrt, array, zeros, sign, histogram, linspace, exp
from numpy.random import uniform, random, seed
from pylab import plot,figure,xlabel, ylabel, title, show, legend
from matplotlib.pyplot import hist


# INICIALIZAR
seed(1)

N = 20          # numero de particulas por lado
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
#                # Caso1 : interacción de Lennard-Jones
#                rm8 = 1 / r2**4         
#                aux = 24 * rm8 * ( 2 / r2**3 - 1 )        
#                fx[i] += aux * dx   # coseno
#                fy[i] += aux * dy   # seno
#                fx[j] -= aux * dx   # coseno
#                fy[j] -= aux * dy   # seno
                
                # Caso2: interacción de cuerpos rígidos
                aux = 1 / r2**14       
                fx[i] += aux * dx
                fy[i] += aux * dy
                fx[j] -= aux * dx
                fy[j] -= aux * dy
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

for i in range(Npasos):
    print(i)
    rxprev, ryprev, rx, ry, vx, vy = Verlet(rxprev,ryprev,rx,ry,vx,vy)
    #plot(rx,ry,'.b')

plot(rxini,ryini,'oc',label="Inicio")
plot(rx,ry,'or',label="Fin")
plot([0,L,L,0,0],[0,0,L,L,0],'g')      # para pintar la caja
xlabel("Posiciones eje X")
ylabel("Posiciones eje Y")
title("Dinámica molecular Discos Rígidos")
legend()

#%%

# CALCULO DE LA FUNCIÓN DE DISTRIBUCIÓN DE VELOCIDADES
v = sqrt(vx**2+vy**2)

# realizar el histograma
nn = 15         # numero de intervalos
figure()
hist(v, nn, normed=1, facecolor='green',label="histograma")
xlabel('Intervalos de velocidad')
ylabel('Conteo de partículas por intervalo')
title('Distribución de velocidades')
show()

# obtención de los datos del histograma
yh, xhaux = histogram(v, bins=linspace(0,max(v),nn), density=True)
xh = []
for i in range(len(yh)):
    xh.append( (xhaux[i] + xhaux[i+1]) / 2 )

# representar el histograma
plot(xh,yh,'-o',label="Datos")

# CALCULO DEL AJUSTE
# http://www.sc.ehu.es/sbweb/fisica3/datos/ajuste/nolineal.html

# Obtención de las sumas
S1, S2 = 0, 0
for i in range(len(yh)):
    S1 += 2*xh[i]**2 * exp(-2*xh[i]**2)
    S2 += 2*xh[i]* yh[i] * exp(-xh[i]**2)    

# obtención de A
A = S2 / S1

# representación del ajuste
xplot = linspace(0,max(v),100)
yplot = A * xplot * exp(-xplot**2)
plot(xplot+0.1, yplot, 'b',label="Ajuste")
legend()



