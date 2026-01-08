# --------------------------------------
# Constraints
# --------------------------------------

#time window on apron w as u, u set of S_w
#S_w = {all time windows on apron w}
#N_wtau = capacity limit of apron w in the apron time window u, = 5
#apron time window = 30 min
#type of gate



#13
m.addConstrs(gp.quicksum(
    X_ijh[i][j][h]
for j in range
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








