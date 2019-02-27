# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 14:34:50 2018

@author: luiss
"""

# EXPONENTE DE LYAPUNOV

import random
from numpy import empty
from pylab import plot, figure, title, xlabel, ylabel, legend, xlim, ylim, semilogy

#función de lorenz
def lorenz(x, y, z, s=10, r=30, b=8/3):
    vx = s*(y - x)
    vy = r*x - y - x*z
    vz = x*y - b*z
    return vx, vy, vz

#incremento de tiempo
dt = 1e-4
tfinal=50
N = int(tfinal/dt)

#variables dependientes del tiempo
x = empty((N + 1,))
y = empty((N + 1,))
z = empty((N + 1,))

x1 = empty((N + 1,))
y1 = empty((N + 1,))
z1 = empty((N + 1,))

t = empty((N + 1,))


# Condiciones iniciales del sistema 1
x[0] = 1.
y[0] = 0.
z[0] = 0.

size2 = 0.0001
# Condiciones iniciales del sistema 2
x1[0] = x[0] + size2 * (random.random()*2 - 1)
y1[0] = y[0] + size2 * (random.random()*2 - 1)
z1[0] = z[0] + size2 * (random.random()*2 - 1)

# Calculo de la evolución del movimiento.
for i in range(N):
    vx, vy, vz = lorenz(x[i], y[i], z[i])
    x[i+1] = x[i] + vx*dt
    y[i+1] = y[i] + vy*dt
    z[i+1] = z[i] + vz*dt
    
    vx1, vy1, vz1 = lorenz(x1[i], y1[i], z1[i])
    x1[i+1] = x1[i] + vx1*dt
    y1[i+1] = y1[i] + vy1*dt
    z1[i+1] = z1[i] + vz1*dt
    
    t[i+1] = t[i] + dt


#gráfica del exponente de Lyapunov
figure()
semilogy(t,abs(x1-x),lw=0.5)
xlabel("t (s)") 
ylabel(r'$|x_{0}(t) - x_{1}(t)|$')
title('lyapunov exponent (x-axis)')

"""
figure()
semilogy(t,abs(y1-y))
xlabel("t (s)") 
ylabel(r'$|y_{0}(t) - y_{1}(t)|$')
title('lyapunov exponent (y-axis)')


figure()
semilogy(t,abs(z1-z))
xlabel("t (s)") 
ylabel(r'$|z_{0}(t) - z_{1}(t)|$')
title('lyapunov exponent (z-axis)')
"""