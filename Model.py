import pandas as pd
from Data import flights
import gurobipy as gp
from Constraints import AddConstraints #still to be added
from Variables import F, G, Gamma, K, A, F_k, C1, C2, C3

def build_model():
    #Define model and model name---------------------------------------------------
    m = gp.Model('Gate_Assignment')

    #Decision variables------------------------------------------------------------
    x_ijh = m.addVars(f, f, g, vtype=gp.GRB.BINARY, name='flights_i_and_j_are_assigned_to_gate_h_successively')
    y_igamma =m.addVars(gamma, f, vtype=gp.GRB.BINARY, name='flight_i_takes_off_on_runway_gamma')

    #Model Objective---------------------------------------------------------------
    #Taxi loss Z1, robust loss Z2, remote loss Z3
    taxi_loss = gp.quicksum(f_i*T_ik*X_ijh) #voeg nog de for loops toe 
    robust_los = gp.quicksum(f(Delta_ijk)*x_ijh) #voeg loops toe
    remote_loss = gp.quicksum(l_k * x_ijh) #voeg loops toe

    #Main objective function------------------------------------------------------
    m.setObjective((C1*taxi_loss) + (C2*robust_los) + (C3 * remote_loss), gp.GRB.MINIMIZE)

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