from Data import flights
import gurobipy as gp
from Variables import *

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

x_ijh = m.addVar(shape=(f, f, g), vtype=gp.GRB.BINARY, name='flights_i_and_j_are_assigned_to_gate_h_successively')
y_igamma =m.addVar(shape=(gamma, f), vtype=gp.GRB.BINARY, name='flight_i_takes_off_on_runway_gamma')


f_i, T

#Model Objective---------------------------------------------------------------
#Taxi loss
f_i = {}
for i in F:
    f_i[i] = FF_i[i] * NE_i[i]

T_ki = {}
for i in F:
    T_ki[i] = TA[i, k, Flight.arrival_runway[i]] + gp.quicksum(TD[i, k, gamma] for gamma in lambda) * y_igamma[gamma, i] - T_mini[i]


for i in F:
    T_mini[i] = min(
        TA[i, k, Flight.arrival_runway[i]] + TD[i, k, gamma]
        for k in G
        for gamma in Lambda
    )

delta_ijk = {}
for i in F:
    for j in F:
        for k in K:
            delta_ijk[i, j, k] = TA[j, k, Flight.arrival_runway[j]] - TD[i, k, gamma]

taxi_loss = gp.quicksum(f_i[i]*T_ik[i,k]*X_ijh[i,j,h] for k in K for h in H_k[k] for i in F_k[k] for j in F_k[k])
robust_loss = gp.quicksum(delta_ijk[i,j,k] * X_ijh[i,j,h] for k in K for h in H_k[k] for i in F_k[k] for j in F_k[k])
remote_loss = gp.quicksum(l_k[k] * X_ijh[i, j, h] for k in K for h in H_k[k] for i in F_k[k] for j in F_k[k])


m.setObjective((C1*taxi_loss) + (C2*robust_loss) + (C3 * remote_loss), GRB.MINIMIZE)

 #Setup model for running and testing------------------------------------------
m.Params.TimeLimit = 172800  #2 days
m.optimize()

#Save results of the model----------------------------------------------------
#Write the LP file for inspection
m.write("gate_assignment.lp")

#print results
if m.SolCount > 0:
    rows = [{"variable": v.VarName, "value": v.X} for v in m.getVars() if v.X > 0.5]
    pd.DataFrame(rows).to_excel("gate_assignment_results.xlsx", index=False)
    print("Results saved to gate_assignment_results.xlsx")
else:
    print(f"No feasible solution. Status: {m.Status}")