# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 15:13:02 2018

@author: luiss
"""

from numpy import empty
from pylab import plot, figure, title, xlabel, ylabel, legend
from time import time


def lorenz(x, y, z, s=10, r=26, b=8/3):
    vx = s*(y - x)
    vy = r*x - y - x*z
    vz = x*y - b*z
    return vx, vy, vz


dt = 1e-4
tol = 2*dt

tfinal=150
N = int(tfinal/dt)

figure()

x = empty((N + 1,))
y = empty((N + 1,))
z = empty((N + 1,))
t = empty((N + 1,))

# Setting initial values


x_0 = [1.0, 0.1, 0.2, 1]
y_0 = [0.0, 1.0, 1.2, 1.5]
z_0 = [0.0, 1.0, 0.8, 12]

ini=time()

for j in range(len(x_0)):
    #estableciendo los valores iniciales
    x[0] = x_0[j]
    y[0] = y_0[j]
    z[0] = z_0[j]        
    
    for i in range(N):
        vx, vy, vz = lorenz(x[i], y[i], z[i])
        x[i+1] = x[i] + vx*dt
        y[i+1] = y[i] + vy*dt
        z[i+1] = z[i] + vz*dt
        t[i+1] = t[i] + dt

    # en el eje x=0
    yPoincare_x0 = []
    zPoincare_x0 = []
    for i in range(N):
        if abs(x[i]) < tol:
            yPoincare_x0.append(y[i])
            zPoincare_x0.append(z[i])
    if j==0:
        plot(yPoincare_x0,zPoincare_x0,'or',label=("r(0)=(%.1f, %.1f, %.1f)" % (x[0], y[0], z[0])))
    if j==1:
        plot(yPoincare_x0,zPoincare_x0,'^g',label=("r(0)=(%.1f, %.1f, %.1f)" % (x[0], y[0], z[0])))
    if j==2:
        plot(yPoincare_x0,zPoincare_x0,'sb',label=("r(0)=(%.1f, %.1f, %.1f)" % (x[0], y[0], z[0])))
    if j==3:
        plot(yPoincare_x0,zPoincare_x0,'+m',label=("r(0)=(%.1f, %.1f, %.1f)" % (x[0], y[0], z[0])))
    

fin = time()
compu_time=fin-ini
print(compu_time)

# en el eje X
xlabel("Y")
ylabel("Z")
title("Atractor Lorentz plano X=0")

legend()