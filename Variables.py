F = []        #Flights
G = []        #Gates
K = []        #Gate types
Gamma = []    #runways

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
TA = {}      # arrival taxi time: TA[(i, k)]
TD = {}      # departure taxi time: TD[(i, k, gamma)]
Tmin = {}    # minimum taxi time per flight i
lk = {}      # remote penalty per gate type k

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
push ding