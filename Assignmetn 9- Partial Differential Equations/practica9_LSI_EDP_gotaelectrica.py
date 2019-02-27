# -*- coding: utf-8 -*-
"""
Created on Wed May  9 14:53:52 2018

@author: luiss
"""

from numpy import zeros, full
from pylab import imshow,show, jet, colorbar, figure, gray, xlabel, ylabel, title
from time import time
start = time()

# Constants
M = 100         # Grid squares on a side
V = 1.0         # Voltage at top wall
target = 1e-5   # Target accuracy

# Condiciones de la esfera
R = M/2.2;
H = R/3;

# Create arrays to hold potential values
phi = zeros([M+1,M+1],float)

# Sin cargas
rho = zeros([M+1,M+1],float)
rho[20:25, 60:65] = -1
rho[40:45, 50:55] = -1
rho[50:55, 70:75] = 1
rho[80:85, 30:35] = -1
rho[50:55, 60:65] = 1
rho[80:85, 85:90] = 1
rho[60:65, 30:35] = 1
rho[90:95, 50:55] = 1
rho[60:65, 60:65] = -1
rho[40:45, 30:35] = 1
rho[30:35, 85:90] = -1
rho[40:45, 80:85] = -1

pos = full((M+1,M+1), False)

for i in range(M+1):
    for j in range(M+1):
        if (i-M/2-H)**2 + (j-M/2)**2 <= R**2:
            pos[i,j]=True
            

geom = zeros((M+1,M+1))             # para mostrar la geometría
borde = full((M+1,M+1), False)      # borde con el aire
borde2 = full((M+1,M+1), False)     # borde con el suelo
interior = full((M+1,M+1), False)   # zona interior

for i in range(1,M):
    for j in range(1,M):
        if pos[i,j] == True:
            if pos[i-1,j] == False or pos[i+1,j] == False \
                or pos[i,j-1] == False or pos[i,j+1] == False:
                    borde[i,j] = True
                    geom[i,j] = 1
            if rho[i,j] == 1:
                geom[i,j] = 1
            elif rho[i,j] == -1:
                geom[i,j] = -1
                    
                    
for j in range(1,M):
    if pos[M,j]==True:
        borde2[M,j] = True
        borde[M,j] = True
        geom[M,j] = -1

for i in range(M+1):
    for j in range(M+1):
        if pos[i,j] == True and borde[i,j]==False:
            interior[i,j]=True
            
figure()
imshow(geom)
xlabel("X axis")
ylabel("Y axis")
title("Contorno")

figure()
imshow(pos)

#CC 
#phi[0,:] = 0
#phi[:,0] = 0
#phi[M,:] = V
#phi[:,M] = 0

# CONDICIONES DE CONTORNO
for i in range(M):
    if borde[M,i] == True:
        phi[M,i] = V

a = 1
c= a**2 / (4 * 1)

omega = 0.9

# Main loop
delta = 1.0
while delta>target:

    # Calculate new values of the potential
    delta = 0
    for i in range(M,1,-1):
        for j in range(M,1,-1):
            if interior[i,j] == True:
                phi_aux = phi[i,j]
                phi[i,j] = (1+omega)*(phi[i+1,j] + phi[i-1,j] + phi[i,j+1] + phi[i,j-1])/4 \
                            - omega * phi[i,j] + c *rho[i,j]
                if abs(phi[i,j]-phi_aux)>delta:
                    delta = abs(phi[i,j]-phi_aux)

    # Calculate maximum difference from old values
    print("delta: ", delta)
    
elapsed = time() - start
print("Elapsed time: ", elapsed, "seconds")


# Make a plot
figure()
imshow(phi)
jet()
colorbar()
xlabel("X axis")
ylabel("Y axis")
title("Potencial")

#imshow(~borde, alpha=0.1) #,  interpolation='bilinear'
#gray()

"""
for i in range(M+1):
    for j in range(M+1):
        if pos[i,j]==False:
            phi[i,j]=-1
imshow(phi)
colorbar
"""

show()