# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 15:13:02 2018

@author: luiss
"""

from numpy import empty
from pylab import legend
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def lorenz(x, y, z, s=10, r=26, b=8/3):
    vx = s*(y - x)
    vy = r*x - y - x*z
    vz = x*y - b*z
    return vx, vy, vz


dt = 1e-4
tfinal=50
N = int(tfinal/dt)

x = empty((N + 1,))
y = empty((N + 1,))
z = empty((N + 1,))
t = empty((N + 1,))


# Crear los valores iniciales
x[0], y[0], z[0] = (1.,0.,0.)

# Obtener la evolución en el tiempo
for i in range(N):
    vx, vy, vz = lorenz(x[i], y[i], z[i])
    x[i+1] = x[i] + vx*dt
    y[i+1] = y[i] + vy*dt
    z[i+1] = z[i] + vz*dt
    t[i+1] = t[i] + dt


# 3D plot

fig = plt.figure(1)
ax = fig.gca(projection='3d')
ax.plot(x, y, z, lw=0.5, \
        label=("r(0)=(%d, %d, %d)" % (x[0], y[0], z[0])))
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("Lorenz Attractor")
plt.show()
legend()



"""
#Extra: calcular la sección de Poincaré

tol = 2*dt

# en el eje y=0
xPoincare_y0 = []
zPoincare_y0 = []
for i in range(N):
    if abs(y[i]) < tol:
        zPoincare_y0.append(z[i])
        xPoincare_y0.append(x[i])
                
figure()
xlabel("X")
ylabel("Z")
title("Atractor Lorentz eje Y")
plot(xPoincare_y0,zPoincare_y0,'.', label=("Condiciones iniciales: r=(%d, %d, %d)" % (x[0], y[0], z[0])))
legend()



# en el eje x=0
yPoincare_x0 = []
zPoincare_x0 = []
for i in range(N):
    if abs(x[i]) < tol:
        yPoincare_x0.append(y[i])
        zPoincare_x0.append(z[i])

figure()
xlabel("Y")
ylabel("Z")
title("Atractor Lorentz eje Z")
plot(yPoincare_x0,zPoincare_x0,'.',label=("Condiciones iniciales: r=(%d, %d, %d)" % (x[0], y[0], z[0])))
legend()
"""