# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 16:27:26 2018

@author: luiss

Apartados 1, 2, 3 y 4
"""



from pylab import plot, figure, xlabel, ylabel, title, legend
from numpy import zeros, exp, array, linspace, mean, absolute
from numpy.random import choice, randint, random, seed
from time import time

N = 10          # numero de espines por lado
Nm1 =N -1       # es útil
NT = N * N      # numero total de espines

# inicializar espines
espin = zeros([N,N],int)
espin_ini = zeros([N,N],int)

# asignar valores aleatorios
for i in range(N):
    for j in range(N):
        espin_ini[i,j]=choice([int(-1),int(1)])

# Función para calcular la energía total
def EnergiaTotal():
    energy = 0
    # Paso 1
    # i!=Nm1 and j!=Nm1
    for i in range(Nm1):
        for j in range(Nm1):
            energy += espin[i,j] * ( espin[i,j+1] + espin[i+1,j] )
    # Paso 2
    # i=!Nm1 and j=Nm1
    for i in range(Nm1):      
        energy += espin[i,Nm1] * ( espin[i,0] + espin[i+1,Nm1] )
    # Paso 3
    # i=Nm1 and j!=Nm1
    for j in range(Nm1):    
        energy += espin[Nm1,j] * ( espin[Nm1,j+1] + espin[0,j] )
    # Paso 4
    # j=Nm1 and i=Nm1 
    energy += espin[Nm1,Nm1] * ( espin[Nm1,0] + espin[0,Nm1] )
    return -energy


# Función para calcular la variación de energía al cambiar un spin
def DEnergiaSpin(i,j):      # con CC
    # Posibilidad 1: que esté en la zona 1
    # i!=Nm1 and j!=Nm1
    if (i != Nm1 and j != Nm1):
        return (-2) * ( - espin[i,j]) * ( espin[i,j+1] + espin[i+1,j] + espin[i,j-1] + espin[i-1,j] )
    # Posibilidad 2: que esté en la zona 2
    # i!=Nm1 and j=Nm1
    elif (i != Nm1):      
        return (-2) * ( - espin[i,Nm1]) * ( espin[i,0] + espin[i+1,Nm1] + espin[i,Nm1-1] + espin[i-1,Nm1] )
    # Posibilidad 3: que esté en la zona 3
    # i=Nm1 and j!=Nm1
    elif (j != Nm1):      
        return (-2) * ( - espin[Nm1,j]) * ( espin[Nm1,j+1] + espin[0,j] + espin[Nm1,j-1] + espin[Nm1-1,j] )
    # Posibilidad 4: que esté en la zona 4
    # j=Nm1 and i=Nm1 
    return (-2) * ( - espin[Nm1,Nm1]) * ( espin[Nm1,0] + espin[0,Nm1] + espin[Nm1-1,Nm1] + espin[Nm1,Nm1-1] )

# Función para calcular la magnetización por espin
def Magnetizacion():
    Maux = 0
    for i in range(N):
        for j in range(N):
            Maux += espin[i,j]
    return Maux / NT











###### APARTADO 1
print("Apartado 1")
ini = time()

# Temperaturas
Tc = 2.27
Tmin = 1
Tmax = 3.5
NTemp = 6
Tlist = linspace(Tmin, Tmax, NTemp )

NMC = 300    # numero de pasos de MonteCarlo

figure()
title("Magnetización")
xlabel("Tiempo de Montecarlo")
ylabel("Magnetización (por spin)")

seed(2)

for ind_T in range(NTemp):
    T = Tlist[ind_T]
    
    # inicializar espines
    for i in range(N):
        for j in range(N):
            espin[i,j]=espin_ini[i,j]
            
    # Variables del sistema
    M = []     # magnetizacion
    P = [0]     # pasos
    Mm = []
    
    M.append( Magnetizacion() )
    
    for k in range(NMC):
        
        Eaux = 0
        Maux = 0
        
        for i in range(NT):     # realizar un total de NT cambios (1 paso Montecarlo)
            # escoger una partícula al azar
            indx = randint(N)
            indy = randint(N)
            
            DE = DEnergiaSpin(indx,indy)    # hallar la variación en energía
            DM = -2 * espin[indx,indy] / NT # variacion en magnetización
            
            if DE <= 0:                     # se acepta el cambio
                espin[indx,indy] *= (-1)
                M.append(M[-1]+DM)
                Maux += M[-1]
                
            elif random() < exp (-DE/T):    # también se acpeta el cambio
                espin[indx,indy] *= (-1)
                M.append(M[-1]+DM)
                Maux += M[-1]
                
            else:                           # no se acepta el cambio
                M.append(M[-1])
                Maux += M[-1]
                
            P.append(P[-1]+1)
            
        # hacer la media
        Mm.append(Maux/NT)
    
    plot(range(NMC),Mm, label="Temp = "+str(T))
    legend()

fin = time()
print ("Tiempo de ejecucion: "+str((fin-ini)//0.1/10)+" s")











###### APARTADO 2
print("Apartado 2")

ini = time()

# Temperaturas
Tc = 2.27
Tmin = 0.1
Tmax = 10
NTemp = 30
Tlist = linspace(Tmin, Tmax, NTemp )

E_Tot = EnergiaTotal()
M_Tot = Magnetizacion()
    
Emedia = []
Mmedia = []

NMC = 400

for ind_T in range(NTemp):
    seed(1)
    print( "Paso "+str(ind_T+1)+"/"+str(NTemp) )
    
    T = Tlist[ind_T]
    d = { 4:exp(-4/T) , 8:exp(-8/T) }

    # inicializar espines
    for i in range(N):
        for j in range(N):
            espin[i,j]=espin_ini[i,j]
            
    # Variables del sistema
    #E = E_Tot
    #M = M_Tot
    E = EnergiaTotal()
    M = Magnetizacion()
    Em = []
    Mm = []
    
    for k in range(NMC):
        
        Eaux = 0
        Maux = 0
        
        for i in range(NT):
            indx = randint(N)
            indy = randint(N)
            
            DE = DEnergiaSpin(indx,indy)
            DM = -2 * espin[indx,indy] / NT
            
            if DE <= 0: 
                espin[indx,indy] *= (-1)
                M += DM
                E += DE
                Maux += M
                Eaux += E    
#            elif random() < exp (-DE/T):
            elif random() < d[DE]:
                espin[indx,indy] *= (-1)
                M += DM
                E += DE
                Maux += M
                Eaux += E
            else:
                Maux += M
                Eaux += E
                
        # hacer la media
        Mm.append(Maux/NT)
        Em.append(Eaux/NT)
        
    Em = array(Em)/NT   #energia por particula
    Mm = array(Mm)
    
    Emedia.append( mean(Em[50:]) )
    Mmedia.append( absolute( mean(Mm[50:]) ) )

figure()
title("Energía")
xlabel("Temperatura")
ylabel("Energía media")
plot(Tlist,Emedia,'-o')

figure()
title("Magnetizacion")
xlabel("Temperatura")
ylabel("Magnetizacion media")
plot(Tlist,Mmedia,'-o')

fin = time()
print ("Tiempo de ejecucion: "+str((fin-ini)//0.1/10)+" s")