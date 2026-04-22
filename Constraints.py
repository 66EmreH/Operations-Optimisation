import gurobipy as gp
from Variables import F, G, Gamma, K, A, D, F_k, H_k, mu_sgamma
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
ksi = None #time interval treshold, we still need to define this
t_A_jk = None #Arrival time of flight j at gate type k @Emre is making this variable
t_D_ik = None #Departure time of flight i at gate type k @Emre is making this variable
M = 10000 #A big M constant
#H_k is al toegevoegd
S_r = np.arange(96) #set 15 minutes time slots in total 96 in one day
t_a = None #average departure time of flight F_D^s
d = None #average safety interval on runway Gamma
alpha_is = None #equals 1 if flight arrives or departs in runway time window 
chi = None #equals 1 if gate type k is on apron w
N_w_tau = None #capacity limit of apron w in the apron time window u, = 5
rho = None #equals 1 if flight i is in apron time window u when parked at apron h of type k, else 0
W = None #set of aprons
S_w = None #set of time windows on apron w
Lamba = None #set of runways available for flight i

# --------------------------------------
# Constraints
# --------------------------------------

#time window on apron w as u, u set of S_w
#S_w = {all time windows on apron w}
#N_wtau = capacity limit of apron w in the apron time window u, = 5
#apron time window = 30 min
#type of gate
def Constraints(m):

    x_ijh = m.addVar(shape=(f, f, g), vtype=gp.GRB.BINARY, name='flights_i_and_j_are_assigned_to_gate_h_successively')
    y_igamma =m.addVar(shape=(gamma, f), vtype=gp.GRB.BINARY, name='flight_i_takes_off_on_runway_gamma')

    #13 only one gate selected per arriving flight
    m.addConstrs(gp.quicksum(
        x_ijh[i][j][h] 
    for k in K 
    for h in hk[k]
    for j in fk
    ) == 1
    for i in range(a)

    )

    #14 only one runway selected per departing flight
    m.addConstrs(gp.quicksum(
        y_igamma[gamma][i]
    for gamma in Lamba[i])== 1
    for i in range(d)
    )

    #15  flights i and j parked continuously at the same gate cannot overlap in time and must meet a certain time interval threshold
    m.addConstrs(t_A_jk[j][k] - t_D_ik[i][k] + M * (1 - x_ijh[i][j][h]) >=  ksi 
                    for i in F_k[k] 
                    for j in F_k[k] 
                    for h in range(hk[k]) 
                    for k in range(K)
        )

    #16 
    m.addConstrs(gp.quicksum(x_ijh[l][i][h] for l in F_k[k]) - gp.quicksum(x_ijh[i][j][h] for j in F_k[k]) == 0
    for h in H_k[k]
    for k in K
    for i in F_k[k]
    #if i not in (start, end)
    )

    #17a
    m.addConstrs(gp.quicksum(x_ijh[0][i][h] for i in F_k[k] if i != K) ==
                gp.quicksum(x_ijh[i][-1][h] for i in F_k[k] if i != 0)
            for h in G
    )

    #17b
    m.addConstrs(gp.quicksum(x_ijh[0][i][h] for i in F_k[k] if i != K) <= 1
            for h in G
    )

    #18
    m.addConstrs(gp.quicksum(chi[k][w] *
        gp.quicksum(x_ijh[i][j][h] * rho[h][i][u] for j in F_k[k] if j != 0 and j != K) 
        for i in F_k[k]
        for h in G) <= N_w_tau[u]
    for w in W
    for u in S_w
    )

    # taxiing start time
    tA[i,k] = a_i + TA[k,gamma_arrival]

    # taxiing end time
    tD[i,k] = d_i - sum(
        y[i,gamma] * TD[i,k,gamma] for gamma in runways
    )



    #20

    m.addConstrs(gp.quicksum(
        alpha_is[i][s] * y_igamma[gamma][i]) + A[s][g] for i in D<= 
        mu_sgamma[s][g] 
        for s in S_r
        for g in Gamma)


    #21

