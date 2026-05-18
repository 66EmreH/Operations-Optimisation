import gurobipy as gp
from gurobipy import GRB
import pandas as pd
from Variables import C1, C2, C3, TA, TD
from Constraints import Constraints

def build_model(sets):
    #Unpack sets
    F        = sets["F"]
    G        = sets["G"]
    K        = sets["K"]
    A        = sets["A"]
    D        = sets["D"]
    Lambda   = sets["Lambda"]
    Lambda_i = sets["Lambda_i"]
    H_k      = sets["H_k"]
    F_k      = sets["F_k"]
    l_k        = sets["l_k"]
    virtual_0  = sets["virtual_0"]
    virtual_n1 = sets["virtual_n1"]
    f_i        = sets["f_i"]

    real_flight_ids = sets["real_flight_ids"]

    m = gp.Model('Gate_Assignment')

    #--------------------------------------
    #Decision variables

    # Only create x[i,j,h] for triples valid under some gate type k.
    # Exclude the direct virtual_0→virtual_n1 edge: that would represent an "empty gate"
    # with no real flight, is excluded from both sides of constraints 17a/17b, and would
    # otherwise be a completely unconstrained free binary variable.
    valid_x = [
        (i, j, h)
        for k in K
        for h in H_k[k]
        for i in F_k[k]
        for j in F_k[k]
        if i != j                                      # no self-loops
        and not (i == virtual_0 and j == virtual_n1)  # no direct empty-gate chain
    ]
    x_ijh    = m.addVars(valid_x, vtype=GRB.BINARY, name='x_ijh')

    # y only for real flights — virtual source/sink have no physical runway assignment.
    y_igamma = m.addVars(real_flight_ids, Lambda, vtype=GRB.BINARY, name='y_igamma')


    #Model Objective---------------------------------------------------------------
    #Taxi loss

    #T_mini must be computed before T_ki (T_ki uses T_mini)
    T_mini = {}
    for i in real_flight_ids:
        T_mini[i] = min(
            TA.get((i, k, F[i].arrival_runway), 0) + TD.get((i, k, gamma), 0)
            for k in K
            for gamma in Lambda
        )

    T_ki = {}
    for i in real_flight_ids:
        for k in K:
            T_ki[i, k] = TA.get((i, k, F[i].arrival_runway), 0) + gp.quicksum(TD.get((i, k, gamma), 0) * y_igamma[i, gamma] for gamma in Lambda_i[i]) - T_mini[i]

    delta_ijk = {}
    for i in real_flight_ids:
        for j in real_flight_ids:
            for k in K:
                delta_ijk[i, j, k] = TA.get((j, k, F[j].arrival_runway), 0) - gp.quicksum(TD.get((i, k, gamma), 0) * y_igamma[i, gamma] for gamma in Lambda_i[i])

    # NOTE: T_ki and delta_ijk are linear in y_igamma, so multiplying by x_ijh makes these
    # bilinear (quadratic). Currently safe only because TA=TD={} forces both to 0.
    # When TA/TD are calibrated, linearise using auxiliary variables or reformulate.
    taxi_loss   = gp.quicksum(f_i[i]*T_ki[i, k]*x_ijh[i, j, h] for k in K for h in H_k[k] for i in F_k[k] for j in F_k[k] if i != j and i in f_i)
    robust_loss = gp.quicksum(delta_ijk[i, j, k] * x_ijh[i, j, h] for k in K for h in H_k[k] for i in F_k[k] for j in F_k[k] if i != j and i in real_flight_ids and j in real_flight_ids)
    remote_loss = gp.quicksum(l_k[k] * x_ijh[i, j, h] for k in K for h in H_k[k] for i in F_k[k] for j in F_k[k] if i != j and i not in (virtual_0, virtual_n1))


    m.setObjective((C1*taxi_loss) + (C2*robust_loss) + (C3 * remote_loss), GRB.MINIMIZE)

    Constraints(m, sets, x_ijh, y_igamma)

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

    return m
