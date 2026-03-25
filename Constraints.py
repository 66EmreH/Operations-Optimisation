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

#time window on apron w as u, u set of S_w
#S_w = {all time windows on apron w}
#N_wtau = capacity limit of apron w in the apron time window u, = 5
#apron time window = 30 min
#type of gate


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

#16 
m.addConstrs(gp.quicksum(X_ijh[l][i][h] for l in compat[k]) - gp.quicksum(X_ijh[i][j][h] for j in compat[k]) == 0
for h in Hk[k]
for k in K
for i in compat[k]
if i not in (start, end)
)

#17a
m.addConstrs(gp.quicksum(X_ijh[start][i][h] for i in compat[type_of_gate[h]] if i != end) == gp.quicksum(X_ijh[i][end][h] for i in compat[type_of_gate[h]] if i != start)
        for h in G
)

#17b
m.addConstrs(gp.quicksum(X_ijh[start][i][h] for i in compat[type_of_gate[h]] if i != end) <= 1
        for h in G
)

#18
m.addConstrs(gp.quicksum(chi[gate_type[h],w] * gp.quicksum(
    gp.quicksum(X_ijh[i][j][h] for j in compat[gate_type[h]]) * rho[gate_type[h], i, u]
    for i in compat[gate_type[h]]
    if i not in (start, end))
    for h in G) <= N_wtau
for w in W
for u in S_w[w]
)

# taxiing start time
tA[i,k] = a_i + TA[i,k,gamma_arrival[i]]

# taxiing end time
tD[i,k] = d_i - sum(
    y[i,gamma] * TD[i,k,gamma] for gamma in runways
)

all_windows = set()
for w in W:
    for (u_id, u_start, u_end) in S_w[w]:
        all_windows.add((u_id, u_start, u_end))

rho = {}  # rho[(k, i, u_id)] = 0 or 1

for k in K:
    for i in F:
        for (u_id, u_start, u_end) in all_windows:

            arrival_in_u = (
                liftA[i, k] >= u_start and liftA[i, k] < u_end
            )
            departure_in_u = (
                liftD[i, k] >= u_start and liftD[i, k] < u_end
            )

            rho[(k, i, u_id)] = 1 if (arrival_in_u or departure_in_u) else 0
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

