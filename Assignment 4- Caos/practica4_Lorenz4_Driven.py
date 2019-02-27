# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 14:34:50 2018

@author: luiss
"""

# DRIVEN LORENZ MODEL

import random
from numpy import empty
from pylab import plot, figure, title, xlabel, ylabel, legend, xlim, ylim
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# función de lorenz
def lorenz(x, y, z, s=10, r=26, b=8/3):
    vx = s*(y - x)
    vy = r*x - y - x*z
    vz = x*y - b*z
    return vx, vy, vz

#incremento temporal
dt = 1e-4
tfinal=50
N = int(tfinal/dt)
#N = 80000

#variables temporales
x1 = empty((N + 1,))
y1 = empty((N + 1,))
z1 = empty((N + 1,))

x2 = empty((N + 1,))
y2 = empty((N + 1,))
z2 = empty((N + 1,))

t = empty((N + 1,))



size = 30
# condiciones iniciales del sistema 1
x1[0] = size * (random.random()*2 - 1)
y1[0] = size * (random.random()*2 - 1)
z1[0] = size * (random.random()*2 - 1)

# condiciones iniciales del sistema 2
x2[0] = x1[0]   #importante: x2(t=0)=x1(t=0)
y2[0] = size * (random.random()*2 - 1)
z2[0] = size * (random.random()*2 - 1)

# Stepping through "time".
for i in range(N):
    vx1, vy1, vz1 = lorenz(x1[i], y1[i], z1[i])
    x1[i+1] = x1[i] + vx1*dt
    y1[i+1] = y1[i] + vy1*dt
    z1[i+1] = z1[i] + vz1*dt
    
    vx2, vy2, vz2 = lorenz(x2[i], y2[i], z2[i])
    x2[i+1] = x1[i+1]
    y2[i+1] = y2[i] + vy2*dt
    z2[i+1] = z2[i] + vz2*dt
    
    t[i+1] = t[i] + dt
    

    
    
# encontrar el momento en que son iguales
tol = size/500

y_1 = []
z_1 = []
y_2 = []
z_2 = []
y_eq = []
z_eq = []

# si la distancia entre ambos sistemas es menor que la tolerancia
# entonces a partir de ese momento tendrán trayectorias muy cercanas 
for i in range(len(x1)):
    if abs(z1[i]-z2[i])<tol and abs(y1[i]-y2[i])<tol:
        j=i
        break

for i in range(j,N+1):
    y_eq.append(y1[i])
    z_eq.append(z1[i])
    
for i in range(0,j):
    y_1.append(y1[i])
    z_1.append(z1[i])
    y_2.append(y2[i])
    z_2.append(z2[i])

"""
# 3d plot
fig = plt.figure(1)
ax = fig.gca(projection='3d')
ax.plot(x1, y1, z1, lw=0.5)        #, label=("Condiciones iniciales: r=(%d, %d, %d)" % (x[0], y[0], z[0]))
ax.plot(x2, y2, z2, lw=0.5)     #, label=("Condiciones iniciales: r=(%d, %d, %d)" % (x[0], y[0], z[0]))
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("Driven Lorenz Attractor")
plt.show()
legend()

"""


"""
figure()
xlabel("t")
ylabel(r'$\Delta x$')
plot(t,y-y1,'.')
"""

#graficarlo

figure()
title("Driven Lorentz Atractor (x-axis)")
xlabel("y")
ylabel(r'$z$')
plot(y_1,z_1,'r',label='trayectoria 1')
plot(y_2,z_2,'b',label='trayectoria 2')
plot(y_eq,z_eq,'g',label='se juntan las trayectorias')
legend()
