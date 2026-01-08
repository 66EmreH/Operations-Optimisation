from Data import flights
import gurobipy as gp
from Variables import F, G, Gamma, K, A, F_k, C1, C2, C3

f = len(F) #number of flights
g = len(G) #number of gates
gamma = len(Gamma) #number of runways
k = len(K) #number of gate types
a = len(A) #number of arriving filghts
d = len(D) #number of departing flights
fk = len(F_k) #number of flights allowed at gate type k


m = gp.Model('Gate_Assignment')

#--------------------------------------
#Decision variables

X_ijh = m.addVar(shape=(f, f, g), vtype=gp.GRB.BINARY, name='flights_i_and_j_are_assigned_to_gate_h_successively')
y_igamma =m.addVar(shape=(gamma, f), vtype=gp.GRB.BINARY, name='flight_i_takes_off_on_runway_gamma')


f_i, T

#Model Objective---------------------------------------------------------------
#Taxi loss
f_i 

taxi_loss = gp.quicksum(f_i*T_ik*X_ijh)


gp.model.setObjective((C1*taxi_loss) + (C2*robust_los) + (C3 * remote_loss))