# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 14:42:19 2018

@author: luiss

apartado 4
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 15:01:57 2018

@author: luiss

apartado 3
"""


from pylab import plot, figure, xlabel, ylabel, title, legend
from numpy import zeros, exp, linspace, concatenate
from numpy.random import choice, randint, random, seed
from time import time

ini  = time()
N = 10       # numero de espines por lado
NT = N * N  # numero total de espines
Nm1 = N - 1

seed(2)

# inicializar espines
espin = zeros([N,N],int)
espin_ini = zeros([N,N],int)
# asignar valores aleatorios
for i in range(N):
    for j in range(N):
        espin_ini[i,j] = choice([int(-1),int(1)])
        
# inicializar espines
for i in range(N):
    for j in range(N):
        espin[i,j] = espin_ini[i,j]
            

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


# Función para calcular la magnetización total
def MagnetizacionTotal():
    Maux = 0
    for i in range(N):
        for j in range(N):
            Maux += espin[i,j]
    return (Maux + 0.0)



# Temperaturas
Tc = 2.27
T = 1

# Valor del campo magnético
NH_2 = 30
NH = 2 * NH_2
Hlist = linspace (-10,10,NH_2)
Hlist_aux = linspace (10,-10,NH_2 )
Hlist = concatenate((Hlist,Hlist_aux))

Mmedia = []

NMC = 100    # numero de pasos de MonteCarlo

for indH in range(NH):
    
    H = Hlist[indH]
    
    M = MagnetizacionTotal()
    E = EnergiaTotal() + M*H  # energía total
    
    Maux = 0    
    total = 0
    
    for k in range(0,NMC):
        for kk in range(NT):
            
            indx = randint(N)
            indy = randint(N)
            
            Ei = EnergiaSpin(indx,indy)
            DM = - 2*espin[indx, indy]
            DE = - 2 * Ei + DM * H

            if DE <= 0: 
                espin[indx,indy] *= (-1)
                M += DM
                Maux += M
                total += 1
            elif random() < exp(-DE/T):
                espin[indx,indy] *= (-1)
                M += DM
                Maux += M
                total += 1
            else:
                Maux += M
                total += 1
            
    Maux /= total      # Energía media y por partícula
    Maux /= NT
    
    Mmedia.append( -Maux )
    
    fin = time()
    print("P: "+str(indH+1)+"/"+str(NH) + \
          "   H: "+str(Hlist[indH]//0.1/10) + \
          "   t: "+str((fin-ini)//0.1/10)+"s" + \
          "   tot: "+ str(total))
    

fin = time()
print ("Tiempo de ejecucion: "+str(fin-ini)+" s")

figure()
title("Ciclo de Histéresis")
xlabel("H")
ylabel("Magnetización media por espín")
plot(Hlist, Mmedia,'-o',label="Temp = "+str(T))
legend()

