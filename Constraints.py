import gurobipy as gp
from Variables import F, G, Gamma, K, A, D, F_k, H_k
import numpy as np


f = len(F) #number of flights
g = len(G) #number of gates
gamma = len(Gamma) #number of runways
k = len(K) #number of gate types
a = len(A) #number of arriving filghts
d = len(D) #number of departing flights
fk = len(F_k) #number of flights allowed at gate type k
hk = len(H_k) #number of gates of type k
m = gp.Model('Gate_Assignment')

#Variables that need to be added
xi = None #time interval treshold, we still need to define this
t_A_jk = None #Arrival time of flight j at gate type k @Emre is making this variable
t_D_ik = None #Departure time of flight i at gate type k @Emre is making this variable
M = 10000 #A big M constant
#H_k is al toegevoegd
S_r = np.arange(96) #set 15 minutes time slots in total 96 in one day
t_a = None #average departure time of flight F_D^s
d = None #average safety interval on runway Gamma
alpha_is = None #equals 1 if flight arrives or departs in runway time window 


# --------------------------------------
# Constraints
# --------------------------------------

x_ijh = m.addVar(shape=(f, f, g), vtype=gp.GRB.BINARY, name='flights_i_and_j_are_assigned_to_gate_h_successively')
y_igamma =m.addVar(shape=(gamma, f), vtype=gp.GRB.BINARY, name='flight_i_takes_off_on_runway_gamma')

#13
m.addConstrs(gp.quicksum(
    x_ijh[i][j][h] == 1
for k in K 
for h in hk[k]
for j in fk
)
for i in range(a)

)

#14
m.addConstrs(gp.quicksum(
    y_igamma[gamma][i]
for gamma in range(gamma))== 1
for i in range(d)
)

#15
m.addConstrs(t_A_jk[j][k] - t_D_ik[i][k] + M * (1 - x_ijh[i][j][h]) >= - xi 
             for i,j in fk 
             for h in hk[k] 
             for k in K
)




#21
mu_sgamma = np.zeros((len(S_r), gamma))
for s in range(len(S_r)):
    for g in range(gamma):
        mu_sgamma[s][g] = A[s][g] + sum(()/
                                        (t_a+d[g])
                                        )


#20

m.addConstrs(gp.quicksum(
    alpha_is[i][s] * y_igamma[gamma][i]) for i in D + A[s][g] <= 
    mu_sgamma[s][g] for s in S_r for g in Gamma)

