# --------------------------------------
# Constraints
# --------------------------------------



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