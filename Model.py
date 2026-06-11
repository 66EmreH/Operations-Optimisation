import math
import gurobipy as gp
from gurobipy import GRB
import pandas as pd
from Variables import C1, C2, C3
from Constraints import Constraints


def f_robust(delta):
    return 53.19 * math.exp(-((delta + 38.24) / 51.55) ** 2)

def build_model(sets, pinned=None):
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
    TA         = sets["TA"]
    TD         = sets["TD"]
    ksi        = sets["ksi"]

    real_flight_ids     = sets["real_flight_ids"]
    real_flight_ids_set = set(real_flight_ids)

    m = gp.Model('Gate_Assignment')

    #--------------------------------------
    #Decision variables

    #x_ijh for all valid (i,j,h) combinations. Valid combinations are those that respect the compatibility and sequencing rules, as well as the virtual source/sink constraints. This is done to avoid creating unnecessary variables that would only be forced to zero by the constraints, which can help with model size and solve time.
    valid_x = [
        (i, j, h)
        for k in K
        for h in H_k[k]
        for i in F_k[k]
        for j in F_k[k]
        if i != j
        and not (i == virtual_0 and j == virtual_n1)
        and i != virtual_n1
        and j != virtual_0
        and (i not in real_flight_ids_set or j not in real_flight_ids_set
             or F[j].arrival_time >= F[i].departure_time + ksi[i])
    ]
    x_ijh    = m.addVars(valid_x, vtype=GRB.BINARY, name='x_ijh')

    # y only for real flights and only for runways available as departures (Lambda_i).
    y_igamma = m.addVars(
        [(fid, gamma) for fid in real_flight_ids for gamma in Lambda_i[fid]],
        vtype=GRB.BINARY, name='y_igamma',
    )


    #Model Objective---------------------------------------------------------------
    #Taxi loss

    #T_mini must be computed before T_ki (T_ki uses T_mini)
    T_mini = {}
    for i in real_flight_ids:
        T_mini[i] = min(
            TA.get((i, k, F[i].arrival_runway), 0) + TD.get((i, k, gamma), 0)
            for k in K
            for gamma in Lambda_i[i]
        )

    T_ki = {}
    for i in real_flight_ids:
        for k in K:
            T_ki[i, k] = TA.get((i, k, F[i].arrival_runway), 0) + gp.quicksum(TD.get((i, k, gamma), 0) * y_igamma[i, gamma] for gamma in Lambda_i[i]) - T_mini[i]

    # Δ_ijk per Eqs (3),(4),(8): Δ = (a_j - d_i) + TA_j^{k,γ0_j} + TD_i^{k,γ}.
    # Indexed by γ (flight i's departure runway) so f(Δ) is a numeric coefficient
    # on the bilinear product x_ijh · y_iγ.
    delta_ijk = {}
    for k in K:
        real_in_k = [fid for fid in F_k[k] if fid in real_flight_ids_set]
        ta_jk = {j: TA.get((j, k, F[j].arrival_runway), 0) for j in real_in_k}
        # representative departure runway per flight: the shortest taxi-out
        td_i = {i: min(TD.get((i, k, g), 0) for g in Lambda_i[i]) for i in real_in_k}
        for i in real_in_k:
            base_i = -F[i].departure_time + td_i[i]
            for j in real_in_k:
                if i == j:
                    continue
                delta_ijk[i, j, k] = base_i + F[j].arrival_time + ta_jk[j]


    gate_to_k = {h: k for k in K for h in H_k[k]}

    taxi_loss   = gp.quicksum(f_i[i]*T_ki[i, gate_to_k[h]]*x_ijh[i, j, h] for (i, j, h) in valid_x if i in f_i)
    robust_loss = gp.quicksum(f_robust(delta_ijk[i, j, gate_to_k[h]]) * x_ijh[i, j, h] for (i, j, h) in valid_x if i in real_flight_ids_set and j in real_flight_ids_set)
    remote_loss = gp.quicksum(l_k[gate_to_k[h]] * x_ijh[i, j, h] for (i, j, h) in valid_x if i not in (virtual_0, virtual_n1))


    m.setObjective((C1*taxi_loss) + (C2*robust_loss) + (C3 * remote_loss), GRB.MINIMIZE)

    Constraints(m, sets, x_ijh, y_igamma)

    #Pin carried-over flights to the gate they were assigned in an earlier window,
    #so the gate they still occupy cannot be reused by flights in this window.
    if pinned:
        for i, h in pinned.items():
            k = gate_to_k[h]
            m.addConstr(
                gp.quicksum(x_ijh[i, j, h] for j in F_k[k] if j != i and (i, j, h) in x_ijh) == 1,
                name=f"pin_{i}",
            )

     #Setup model for running and testing------------------------------------------
    m.Params.TimeLimit = 28000  
    m.optimize()

    #Save results of the model----------------------------------------------------
    #Write the LP file for inspection
    m.write("gate_assignment.lp")

    #Map each real flight to the gate it was assigned (its single outgoing arc).
    assignments = {}
    if m.SolCount > 0:
        for (i, j, h), var in x_ijh.items():
            if var.X > 0.5 and i in real_flight_ids_set:
                assignments[i] = h
        print(f"Solved window: {len(assignments)} flights assigned.")
    else:
        print(f"No feasible solution. Status: {m.Status}")

    return m, assignments
