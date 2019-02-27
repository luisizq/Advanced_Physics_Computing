# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 15:01:57 2018

@author: luiss

apartado 3
"""


from pylab import plot, figure, xlabel, ylabel, title
from numpy import zeros, exp, array
from numpy.random import choice, randint, random, seed
from time import time

ini  = time()
N = 14       # numero de espines por lado
NT = N * N  # numero total de espines
Nm1 = N - 1
seed(1)


# inicializar espines
espin = zeros([N,N],int)
espin_ini = zeros([N,N],int)
# asignar valores aleatorios
for i in range(N):
    for j in range(N):
        espin_ini[i,j]=choice([int(-1),int(1)])
        
# Temperaturas
Tc = 2.27
Tmin, T1, T2, Tmax = 1, 1.7, 3, 4
N1, N2, N3 = 6, 20, 8
NTemp = N1 + N2 + N3 +1
Tlist=[]

for i in range(N1):
    Tlist.append(Tmin + (T1 - Tmin)/N1*i)
for i in range(N2):
    Tlist.append(T1 + (T2 - T1)/N2*i)
for i in range(N3+1):
    Tlist.append(T2 + (Tmax - T2)/N3*i)
    
Emedia = []
E2media = []

# Función para calcular la energía
def EnergiaTotal():      # con CC
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

Etot = EnergiaTotal()

def EnergiaSpin(i,j):      # con CC
    # i!=Nm1 and j!=Nm1
    if (i != Nm1 and j != Nm1):
        return - espin[i,j] * \
    ( espin[i,j+1] + espin[i+1,j] + espin[i,j-1] + espin[i-1,j] )
    # i=Nm1 and j!=Nm1
    elif (i != Nm1):      
        return - espin[i,j] * \
    ( espin[i,0] + espin[i+1,j] + espin[i,j-1] + espin[i-1,j] )
    # i!=Nm1 and j=Nm1
    elif (j != Nm1):      
        return - espin[i,j] * \
    ( espin[i,j+1] + espin[0,j] + espin[i,j-1] + espin[i-1,j] )
    # j=Nm1 and i=Nm1 
    #elif (i == Nm1 and j == Nm1)
    return - espin[i,j] * \
    ( espin[i,0] + espin[0,j] + espin[i-1,j] + espin[i,j-1] )


NMC = 1000    # numero de pasos de MonteCarlo
NMCini = 100
total1 = (NMC-NMCini)*NT

for indT in range(NTemp):
    seed(indT)
    T = Tlist[indT]
    
    d = { 4:exp(-4/T) , 8:exp(-8/T) }
    
    # inicializar espines
    for i in range(N):
        for j in range(N):
            espin[i,j]=espin_ini[i,j]
       
    # Variables del sistema
    E = Etot   # energía total 
    Eaux = 0
    E2aux = 0
    
    total = 0
    
    for k in range(NMCini):
        for kk in range(NT):
            indx = randint(N)
            indy = randint(N)
            Ei = EnergiaSpin(indx,indy)
            DE = -2 * Ei
            if DE <= 0: 
                espin[indx,indy] *= (-1)
                E += DE
            elif random() < d[DE]:
                espin[indx,indy] *= (-1)
                E += DE
                
    for k in range(NMCini,NMC):
        for kk in range(NT):
            
            indx = randint(N)
            indy = randint(N)
            
            Ei = EnergiaSpin(indx,indy)
            DE = -2 * Ei

            if DE <= 0: 
                espin[indx,indy] *= (-1)
                E += DE
                Eaux += E
                E2aux += E*E
                total += 1
            elif random() < d[DE]:
                espin[indx,indy] *= (-1)
                E += DE
                Eaux += E
                E2aux += E*E
                total += 1

            
    Eaux /= total      # Energía media y por partícula
    E2aux /= total

    Emedia.append( Eaux )
    E2media.append( E2aux )
    
    fin = time()
    print("P: "+str(indT)+"/"+str(NTemp)+"   T: "+str(Tlist[indT]//0.1/10) \
         + "    t: "+str((fin-ini)//0.1/10))

    
# para cada temperatura distinta
Emedia = array(Emedia)
E2media = array(E2media)
DE2media = E2media - Emedia*Emedia
Tlist = array(Tlist)
T2list = Tlist*Tlist
C = DE2media / T2list / NT

fin = time()
print ("Tiempo de ejecucion: "+str(fin-ini)+" s")

figure()
title("Calor Específico")
xlabel("Temperatura")
ylabel("Calor específico por espín")
plot(Tlist,C,'-o')