# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 14:25:26 2018

@author: luiss

apartado 2
"""


from pylab import imshow, colorbar, gray, plot, figure, xlabel, ylabel, title, legend
from numpy import zeros, exp, array, linspace, mean
from numpy.random import choice, randint, random, seed
from time import time

ini  = time()
N = 10       # numero de espines por lado
NT = N * N  # numero total de espines
seed(2)


# inicializar espines
espin = zeros([N,N],int)
espin_ini = zeros([N,N],int)
# asignar valores aleatorios
for i in range(N):
    for j in range(N):
        espin_ini[i,j]=choice([int(-1),int(1)])
        
# Temperaturas
Tc = 2.27
Tmin = 0.5
Tmax = 10
NTemp = 20
Tlist = linspace(Tmin, Tmax, NTemp )

Emedia = []


# Función para calcular la energía
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

# Función para calcular la magnetización
def Magnetizacion():
    Maux = 0
    for i in range(N):
        for j in range(N):
            Maux += espin[i,j]
    return (Maux + 0.0) / NT

figure()
title("Magnetización")
xlabel("Tiempo de Montecarlo")
ylabel("Magnetización (por spin)")

for indT in range(NTemp):
    T = Tlist[indT]
    
    # inicializar espines
    for i in range(N):
        for j in range(N):
            espin[i,j]=espin_ini[i,j]
            
    # Variables del sistema
    E = [0]     # energía
    M = [0]     # magnetizacion
    P = [0]     # pasos
    Em = []
    Mm = []
    
    E[0] = Energia()
    M[0] = Magnetizacion()

    
    cambios = 0
    nocambios = 0

    NMC = 1000    # numero de pasos de MonteCarlo
    
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

            DE = Ef - E[-1]
            if DE < 0: 
                E.append(Ef)
                M.append(Magnetizacion())
                P.append(P[-1]+1)
                Eaux += Ef
                Maux += M[-1]
                cambios += 1
                
            elif random() < exp ( -DE/T):
                E.append(Ef)
                M.append(Magnetizacion())
                P.append(P[-1]+1)
                Eaux += Ef
                Maux += M[-1]
                cambios += 1
            else:
                espin[indx,indy] *= (-1)
                E.append(E[-1])
                M.append(M[-1])
                P.append(P[-1]+1)
                Eaux += E[-1]
                Maux += M[-1]
                nocambios += 1
                
            cambiosaux += 1
        
        if(cambiosaux != 0):
            Em.append(Eaux/cambiosaux)
            Mm.append(Maux/cambiosaux)
        else:
            Em.append(Em[-1])
            Mm.append(Mm[-1])
    
    E = array(E) / NT
    Em = array(Em) / NT
    
    Emedia.append( mean(Em[100:]) )
    
    plot(range(NMC),Em, label="Temp = "+str(T))
legend()   


fin = time()
print ("Tiempo de ejecucion: "+str(fin-ini)+" s")

figure()
title("Energía")
xlabel("Temperatura")
ylabel("Energía media")
plot(Tlist,Emedia,'-o')