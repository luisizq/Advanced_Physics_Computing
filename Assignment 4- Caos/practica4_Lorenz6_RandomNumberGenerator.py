# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 15:13:02 2018

@author: luiss
"""

from numpy import empty
from pylab import plot, figure, title, xlabel, ylabel, legend, xlim, ylim
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def lorenz(x, y, z, s=10, r=26, b=8/3):
    vx = s*(y - x)
    vy = r*x - y - x*z
    vz = x*y - b*z
    return vx, vy, vz


dt = 1e-4
tfinal=200
N = int(tfinal/dt)

x = empty((N + 1,))
y = empty((N + 1,))
z = empty((N + 1,))
t = empty((N + 1,))
r = empty((N + 1,))
r[0] = 0

# Setting initial values
x[0], y[0], z[0] = (1, 0, 0)

# Stepping through "time".
for i in range(N):
    # Derivatives of the X, Y, Z state
    vx, vy, vz = lorenz(x[i], y[i], z[i])
    x[i+1] = x[i] + vx*dt
    y[i+1] = y[i] + vy*dt
    z[i+1] = z[i] + vz*dt
    r[i+1] = x[i+1]*y[i+1]*z[i+1]
    t[i+1] = t[i] + dt

randx=(x*1)%1
index = [i for i in range(N+1)]
     
"""       
figure()
xlabel("Index")
ylabel("X")
title("Rand")
#xlim((0, int(N/10)))

plot(index,randx, label=("Condiciones iniciales: r=(%d, %d, %d)" % (x[0], y[0], z[0])))
legend()
"""

plt.hist(randx, 10000, normed=1, facecolor='green', alpha=0.75)

#plot
plt.xlabel('Range')
plt.ylabel('Probability')
plt.title('Probabilidad randx')

plt.show()