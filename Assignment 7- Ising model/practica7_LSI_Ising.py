# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:38:47 2018

@author: luiss
"""

from pylab import imshow, colorbar, gray, plot, figure, xlabel, ylabel, title
from numpy import zeros, exp, array
from numpy.random import choice, randint, random

N = 7
NT = N * N
espin = zeros([N,N],int)

for i in range(N):
    for j in range(N):
        espin[i,j]=choice([int(-1),int(1)])
        

# imshow(espin), colorbar(), gray()

E = [0]     # energía
M = [0]     # magnetizacion
P = [0]     # pasos

Tc = 2.27
T = 1.5

#def Energia():      # con CC
#    # j!=N and i!=N
#    for i in range(N-1):
#        for j in range(N-1):
#            energy = espin[i,j] * ( espin[i,j+1] + espin[i,j-1]     \
#                + espin[i+1,j+1]  + espin[i+1,j] + espin[i+1,j-1]   \
#                + espin[i-1,j+1] + espin[i-1,j]  + espin[i-1,j-1] )
#    # j=N and i!=N
#    for i in range(N-1):      
#        energy += espin[i,N-1] * ( espin[i,0] + espin[i,N-2]      \
#            + espin[i+1,0]  + espin[i+1,N-1] + espin[i+1,N-2]       \
#            + espin[i-1,0] + espin[i-1,N-1]  + espin[i-1,N-2] )
#    # i!=N and j=N
#    for j in range(N-1):    
#        energy += espin[N-1,j] * ( espin[N-1,j+1] + espin[N-1,j-1]     \
#            + espin[0,j+1]  + espin[0,j] + espin[0,j-1]          \
#            + espin[N-2,j+1] + espin[N-2,j]  + espin[N-2,j-1] )
#    # j=N and i=N 
#    energy += espin[N-1,N-1] * ( espin[N-1,0] + espin[N-1,N-2]     \
#        + espin[0,0]  + espin[0,N-1] + espin[0,N-2]          \
#        + espin[N-2,0] + espin[N-2,N-1]  + espin[N-2,N-2] )
#    
#    return -energy

#def Energia():      # con CC
#    # j!=N and i!=N
#    for i in range(N-1):
#        for j in range(N-1):
#            energy = espin[i,j] * ( espin[i,j+1] + espin[i,j-1]     \
#                + espin[i+1,j]   \
#                + espin[i-1,j])
#    # j=N and i!=N
#    for i in range(N-1):      
#        energy += espin[i,N-1] * ( espin[i,0] + espin[i,N-2]      \
#            + espin[i+1,N-1]    \
#            + espin[i-1,N-1])
#    # i!=N and j=N
#    for j in range(N-1):    
#        energy += espin[N-1,j] * ( espin[N-1,j+1] + espin[N-1,j-1]     \
#            + espin[0,j]    \
#            + espin[N-2,j] )
#    # j=N and i=N 
#    energy += espin[N-1,N-1] * ( espin[N-1,0] + espin[N-1,N-2]     \
#        + espin[0,N-1]  \
#        + espin[N-2,N-1] )
#    return - energy/2

def Energia():      # con CC
    energy = 0
    # j!=N and i!=N
    for i in range(N-1):
        for j in range(N-1):
            energy += espin[i,j] * ( espin[i,j+1] + espin[i+1,j] )
    # j=N and i!=N
    for i in range(N-1):      
        energy += espin[i,N-1] * ( espin[i,0] + espin[i+1,N-1] )
    # i!=N and j=N
    for j in range(N-1):    
        energy += espin[N-1,j] * ( espin[N-1,j+1] + espin[0,j] )
    # j=N and i=N 
    energy += espin[N-1,N-1] * ( espin[N-1,0] + espin[0,N-1] )
    return -energy

def Magnetizacion():
    Maux = 0
    for i in range(N):
        for j in range(N):
            Maux += espin[i,j]
    return (Maux + 0.0) / NT


E[0] = Energia()
M[0] = Magnetizacion()
Em = []
Mm = []

cambios = 0
nocambios = 0

NMC = 100
for k in range(NMC):
    print(k)
    Eaux = 0
    Maux = 0
    cambiosaux = 0
    for i in range(NT):
        indx = randint(N)
        indy = randint(N)
        
        espin[indx,indy] *= (-1)
        Ef = Energia()
        
#        E.append(Ef)
#        M.append(Magnetizacion())
#        P.append(P[-1]+1)
#        cambios += 1

        DE = Ef - E[-1]
        if DE < 0: 
            E.append(Ef)
            M.append(Magnetizacion())
            P.append(P[-1]+1)
            Eaux += Ef
            Maux += M[-1]
            cambiosaux += 1
            cambios += 1
            
        elif random() < exp ( -DE/T):
            E.append(Ef)
            M.append(Magnetizacion())
            P.append(P[-1]+1)
            Eaux += Ef
            Maux += M[-1]
            cambiosaux += 1
            cambios += 1
        else:
            espin[indx,indy] *= (-1)
            E.append(E[-1])
            M.append(M[-1])
            P.append(P[-1]+1)
            Eaux += Ef
            Maux += M[-1]
            cambiosaux += 1
            nocambios += 1
    
    if(cambiosaux != 0):
        Em.append(Eaux/cambiosaux)
        Mm.append(Maux/cambiosaux)
    else:
        Em.append(Em[-1])
        Mm.append(Mm[-1])


E = array(E) / NT
Em = array(Em) / NT
print("Cambios ",cambios)
print("No cambios ",nocambios)

figure()
plot(P,E)
xlabel("pasos microestados")
ylabel("energia")

figure()
plot(P,M)
xlabel("pasos microestados")
ylabel("Magnetizacion")

#figure()
#plot(range(NMC),Em,'o-')
#xlabel("pasos MC")
#ylabel("energia")
#
#figure()
#plot(range(NMC),Mm,'o-')
#xlabel("pasos MC")
#ylabel("Magnetizacion")        