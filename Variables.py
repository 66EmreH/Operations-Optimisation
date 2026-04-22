#Flight & Time variables
F = {} #set of flights
A = {} #set of arrival flights
D = {} #set of departure flights
ai = {} #scheduled arrival time i
di = {} #scheduled departure time for flight i

TA = {}      # arrival taxi time: TA[(i, k)]
TD = {}      # departure taxi time: TD[(i, k, gamma)]


#Gates & Aprons variables
W = {} #set of aprons
G = {} #set of gates, Gn+1 is remote gate set, G0 is contact gate set
K = {} #set of gate types
H_k = {} #set of gates of type k



Q = {} #set of airline types
Gamma = {} #set of runways
Gammai = {} #set of runways available for flight i
ek = {} #upper limit of number of available gates for gate type k

#Relations between flights
compat = {}      # compat[i] = list of gates compatible with flight i
overlaps = {}    # overlaps[i] = list of flights overlapping with flight i

#Subsets
gate_to_k = {}        # gate_id -> gate type k
F_k = {}              # F_k[k] = flights compatible with gate type k
Gamma_i = {}          # Gamma_i[i] = departure runways available for flight i
arrival_runway = {}   # fixed arrival runway for flight i (parameter)

#Times
ai = {}   # scheduled arrival time of flight i
di = {}   # scheduled departure time of flight i

#Objective weights
C1 = 1.0   # taxi / fuel weight
C2 = 1.0   # robustness weight
C3 = 1.0   # remote gate penalty weight

#Objective parameters
fi = {}      # fuel factor per flight i

Tmin = {}    # minimum taxi time per flight i
lk = {}      # remote penalty per gate type k


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


mu_sgamma = np.zeros((len(S_r), gamma))
for s in range(len(S_r)):
    for g in range(gamma):
        mu_sgamma[s][g] = A[s][g] + sum(()/
                                        (t_a+d[g])
                                        )

#Reset of everything
def reset():
    """Clear all variables (useful when re-running models)."""
    global F, A, D, G, K, Gamma
    global compat, overlaps
    global gate_to_k, F_k, Gamma_i, arrival_runway
    global ai, di
    global C1, C2, C3
    global fi, TA, TD, Tmin, lk

    F.clear()
    A.clear()
    D.clear()
    G.clear()
    K.clear()
    Gamma.clear()

    compat.clear()
    overlaps.clear()

    gate_to_k.clear()
    F_k.clear()
    Gamma_i.clear()
    arrival_runway.clear()

    ai.clear()
    di.clear()

    fi.clear()
    TA.clear()
    TD.clear()
    Tmin.clear()
    lk.clear()
