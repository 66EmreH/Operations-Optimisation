from Data import flights
import gurobipy as gp
from Variables import F, G, Gamma, K, A, F_k

f = len(F) #number of flights
g = len(G) #number of gates
gamma = len(Gamma) #number of runways
k = len(K) #number of gate types
a = len(A) #number of arriving filghts
d = len(D) #number of departing flights
fk = len(F_k) #number of flights allowed at gate type k


m = gp.Model('Gate_Assignment')

# --------------------------------------
# Decision variables
# --------------------------------------


X_ijh = m.addVar(shape=(f, f, g), vtype=gp.GRB.BINARY, name='flights_i_and_j_are_assigned_to_gate_h_successively')
y_igamma =m.addVar(shape=(gamma, f), vtype=gp.GRB.BINARY, name='flight_i_takes_off_on_runway_gamma')





