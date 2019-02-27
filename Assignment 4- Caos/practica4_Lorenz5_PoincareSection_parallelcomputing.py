# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 15:16:05 2018

@author: luiss
"""

from numpy import empty
from pylab import plot, figure, title, xlabel, ylabel, legend
from time import time

def lorenz(r, s=10, R=26, b=8/3):
    vx = s*(r[1] - r[0])
    vy = R*r[0] - r[1] - r[0]*r[2]
    vz = r[0]*r[1] - b*r[2]
    return (vx, vy, vz)


dt = 1e-4
tfinal=50
tol = 4*dt

N = int(tfinal/dt)

figure()

r = empty((N+1,3))
t = empty((N + 1,))

# Setting initial values


x_0 = [1.0, 0.0, 0.2, 1]
y_0 = [0.0, 1.0, 1.2, 1.5]
z_0 = [0.0, 1.0, 0.8, 12]

ini=time()

for j in [0]:#range(len(x_0)):
    #estableciendo los valores iniciales
    r[0] = (x_0[j], y_0[j], z_0[j])     
    
    for i in range(N):
        vx, vy, vz = lorenz(r[i])
        r[i+1] = r[i] + (vx*dt, vy*dt, vz*dt)
        t[i+1] = t[i] + dt

    # en el eje x=0
    yPoincare_x0 = []
    zPoincare_x0 = []
    
    
    for i in range(N):
        if abs(r[i,0]) < tol:
            yPoincare_x0.append(r[i,1])
            zPoincare_x0.append(r[i,2])
    
    
    plot(yPoincare_x0,zPoincare_x0,'.',label=("Condiciones iniciales: r=(%d, %d, %d)" % (r[0,0], r[0,1], r[0,2])))

fin = time()
compu_time=fin-ini
print(compu_time)
 

# en el eje X
xlabel("Y")
ylabel("Z")
title("Atractor Lorentz eje Z")
 
legend()