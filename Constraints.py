import gurobipy as gp
from Variables import M

def Constraints(m, sets, x_ijh, y_igamma):

    #Unpack sets 
    F          = sets["F"]
    G          = sets["G"]
    K          = sets["K"]
    A          = sets["A"]
    D          = sets["D"]
    Lambda     = sets["Lambda"]
    Lambda_i   = sets["Lambda_i"]
    H_k        = sets["H_k"]
    F_k        = sets["F_k"]
    ksi        = sets["ksi"]
    virtual_0  = sets["virtual_0"]
    virtual_n1 = sets["virtual_n1"]
    chi_kw     = sets["chi_kw"]
    N_w_tau    = sets["N_w_tau"]
    W          = sets["W"]
    S_w        = sets["S_w"]
    Alpha_is   = sets["Alpha_is"]
    mu_sgamma  = sets["mu_sgamma"]
    S_r        = sets["S_r"]
    F_s_gamma_A  = sets["F_s_gamma_A"]
    overlaps_set = sets["overlaps_set"]
    t_A_ik       = sets["t_A_ik"]
    t_D_ik       = sets["t_D_ik"]

    # 1 if flight fid occupies the apron during 30-min window u, else 0
    rho = {
        (fid, u, k): 1 if t_A_ik[fid, k] < u + 30 and t_D_ik[fid, k] > u else 0
        for fid in F for k in K for u in S_w
    }

    #13 only one gate selected per arriving flight
    # j != virtual_0 skips arcs removed from valid_x (no incoming arc into source).
    m.addConstrs((gp.quicksum(x_ijh[i, j, h]
        for k in K if i in F_k[k]
        for h in H_k[k]
        for j in F_k[k] if j != i and j != virtual_0 and (i, j, h) in x_ijh
        ) == 1
        for i in A),
    name="13"
    )

    #14 only one runway selected per departing flight
    m.addConstrs((gp.quicksum(
        y_igamma[i, gamma]
        for gamma in Lambda_i[i]) == 1
        for i in D),
    name="14"
    )

    #15 gap between consecutive flights at the same gate must meet the threshold ksi
    # i != virtual_n1 and j != virtual_0: skip arcs removed from valid_x.
    m.addConstrs((t_A_ik[j, k] - t_D_ik[i, k] + M * (1 - x_ijh[i, j, h]) >= ksi[i]
        for k in K
        for i in F_k[k] if i != virtual_n1 and i != virtual_0
        for j in F_k[k] if i != j and j != virtual_0 and j != virtual_n1
        for h in H_k[k]
        if (i, j, h) in x_ijh and t_A_ik[j, k] - t_D_ik[i, k] < ksi[i]),
    name="15"
    )

    #16 flow conservation: flight i has equally many predecessors and successors at each gate
    # l != virtual_n1 and j != virtual_0 skip arcs removed from valid_x.
    m.addConstrs((
        gp.quicksum(x_ijh[l, i, h] for l in F_k[k] if l != i and l != virtual_n1 and (l, i, h) in x_ijh) -
        gp.quicksum(x_ijh[i, j, h] for j in F_k[k] if j != i and j != virtual_0 and (i, j, h) in x_ijh) == 0
        for k in K
        for h in H_k[k]
        for i in F_k[k] if i != virtual_0 and i != virtual_n1),
    name="16"
    )

    #17a number of chains starting at gate h equals number ending (one chain per gate)
    # i != virtual_0 on LHS and i != virtual_n1 on RHS prevent self-loops on virtuals.
    m.addConstrs((
        gp.quicksum(x_ijh[virtual_0, i, h] for i in F_k[k] if i != virtual_n1 and i != virtual_0) ==
        gp.quicksum(x_ijh[i, virtual_n1, h] for i in F_k[k] if i != virtual_0 and i != virtual_n1)
        for k in K
        for h in H_k[k]),
    name="17a"
    )

    #17b at most one chain starts at each gate
    m.addConstrs((
        gp.quicksum(x_ijh[virtual_0, i, h] for i in F_k[k] if i != virtual_n1 and i != virtual_0) <= 1
        for k in K
        for h in H_k[k]),
    name="17b"
    )

    #18 apron capacity: total flights parked at apron w during window u <= N_w_tau
    # j != virtual_0 skips arcs removed from valid_x.
    m.addConstrs((gp.quicksum(
        chi_kw[k, w] * gp.quicksum(x_ijh[i, j, h] * rho[i, u, k] for j in F_k[k] if j != i and j != virtual_0 and (i, j, h) in x_ijh)
        for k in K
        for h in H_k[k]
        for i in F_k[k] if i != virtual_0 and i != virtual_n1
        ) <= N_w_tau
        for w in W
        for u in S_w),
    name="18"
    )

    #20 — y_igamma only exists when gamma is a valid departure runway for flight i
    m.addConstrs((gp.quicksum(
        Alpha_is[i, s] * y_igamma[i, gamma] for i in D if gamma in Lambda_i[i]) + len(F_s_gamma_A[s, gamma]) <=
        mu_sgamma[s, gamma]
        for s in S_r
        for gamma in Lambda),
    name="20")
