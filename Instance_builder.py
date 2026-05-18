import random
import pandas as pd
from Classes import Flight, Gate
from Instances import test_case, Paper_case_manuel
from Variables import *


#See which case we want to run
def get_case(case_name):
    if case_name == "test_case":
        return test_case
    if case_name == "paper_case_manuel":
        return Paper_case_manuel
    raise ValueError("Unknown case_name")
#get weights from probabilities
def weighted_choice(prob_dict):
    # prob_dict: {"C":0.7, "D":0.2, ...}
    r = random.random()
    s = 0.0
    for k, p in prob_dict.items():
        s += p
        if r <= s:
            return k
    # fallback if probs don't sum perfectly (due to 0.699999999)
    return list(prob_dict.keys())[-1]


#Build flights with combinations based on probability distributions
def build_flights(cfg):
    flights_cfg = cfg["flights"]

    if flights_cfg["mode"] == "fixed":
        flights = []
        for t in flights_cfg["list"]:
            flights.append(Flight(*t))
        return flights

    #generated
    n = flights_cfg["n_flights"]
    start = flights_cfg["horizon_start"]
    end = flights_cfg["horizon_end"]

    sizes = flights_cfg["sizes"]
    entities = flights_cfg["entities"]
    intl_share = flights_cfg["international_share"]
    turnaround = flights_cfg["turnaround"]
    airlines = flights_cfg["airlines"]
    arrival_runways = flights_cfg["Arrival_runways"]

    max_turnaround = max(turnaround.values())

    flights = []
    for i in range(1, n + 1):
        flight_id = f"F{i}"

        size = weighted_choice(sizes)
        entity = weighted_choice(entities)

        arr_time = random.randint(start, end - max_turnaround)

        #destination types
        if random.random() < intl_share:
            arr_dest = "international"
        else:
            arr_dest = "domestic"

        #for now assume arrival and destination are both the same 
        dep_dest = arr_dest
        dep_time = arr_time + turnaround[size]

        airline = random.choice(airlines)
        arrival_runway = random.choice(arrival_runways)

        flights.append(
            Flight(flight_id, size, entity, arr_time, arr_dest, dep_time, dep_dest, airline, arrival_runway)
        )

    return flights
#Build gates
def build_gates(cfg):
    gates_cfg = cfg["gates"]

    if gates_cfg["mode"] == "fixed":
        gates = []
        for t in gates_cfg["list"]:
            gates.append(Gate(*t))
        return gates

    #apron_template
    apron_counts = gates_cfg["apron_counts"]
    prox_share = gates_cfg["terminal_proximity_share"]
    size_share = gates_cfg["gate_sizes"]
    entity_share = gates_cfg["entities"]
    gates = []
    g = 1

    for apron, corridor_list in apron_counts.items():
        for corridor_index, n_gates in enumerate(corridor_list, start=1):
            for _ in range(n_gates):
                gate_id = f"G{g}"
                g += 1

                prox = weighted_choice(prox_share)
                gate_size = weighted_choice(size_share)
                entity = weighted_choice(entity_share)

                gates.append(Gate(gate_id, prox, gate_size, entity, apron, corridor_index))
    return gates

#Model_Helpers---------------------------------------------------
#Check for compatibility of gates and flights
def build_compatibility(flights, gates):
    size_order = {"B": 1, "C": 2, "D": 3, "E": 4, "F": 5}

    compat = {}  # flight_id -> list of gate_id
    for f in flights:
        allowed = []
        f_intl = f.is_international()

        for g in gates:
            if f.entity != g.entity:
                continue

            if size_order[f.aircraft_size] > size_order[g.gate_size]:
                continue

            if f_intl and g.terminal_proximity == "domestic":
                continue

            allowed.append(g.gate_id)

        compat[f.flight_id] = allowed

    return compat
#Chef for overlapping flights
def build_overlaps(flights):
    # overlap if time windows intersect:
    # [a1,d1] overlaps [a2,d2] when not (d1 <= a2 or d2 <= a1)

    overlaps = []  # list of (flight_id_1, flight_id_2)
    n = len(flights)

    for i in range(n):
        f1 = flights[i]
        a1, d1 = f1.occupancy_window()

        for j in range(i + 1, n):
            f2 = flights[j]
            a2, d2 = f2.occupancy_window()

            if not (d1 <= a2 or d2 <= a1):
                overlaps.append((f1.flight_id, f2.flight_id))

    return overlaps


#Export-----------------------------------------------------------
#Save flights and gates to an Excel file (one sheet each)
def save_to_excel(flights, gates, filename="instance_data.xlsx"):
    flight_data = [{
        "flight_id": f.flight_id,
        "aircraft_size": f.aircraft_size,
        "entity": f.entity,
        "arrival_time": f.arrival_time,
        "arrival_destination": f.arrival_destination,
        "departure_time": f.departure_time,
        "departure_destination": f.departure_destination,
        "airline": f.airline,
        "arrival_runway": f.arrival_runway,
    } for f in flights]

    gate_data = [{
        "gate_id": g.gate_id,
        "terminal_proximity": g.terminal_proximity,
        "gate_size": g.gate_size,
        "entity": g.entity,
        "apron": g.apron,
        "corridor": g.corridor,
    } for g in gates]

    with pd.ExcelWriter(filename) as writer:
        pd.DataFrame(flight_data).to_excel(writer, sheet_name="Flights", index=False)
        pd.DataFrame(gate_data).to_excel(writer, sheet_name="Gates", index=False)

    print(f"Saved to {filename}")

#Main-------------------------------------------------------------
#Construct the instace
def build_instance(case_name, seed=None):
    cfg = get_case(case_name)

    if seed is None:
        seed = cfg.get("seed", 1)

    random.seed(seed)

    flights = build_flights(cfg)
    gates = build_gates(cfg)

    compat = build_compatibility(flights, gates)
    overlaps = build_overlaps(flights)

    instance = {
        "case_name": case_name,
        "seed": seed,
        "flights": flights,
        "gates": gates,
        "compat": compat,
        "overlaps": overlaps,
    }

    #Check if a plane has any compatible gates
    for fid, allowed in compat.items():
        if len(allowed) == 0:
            print("No compatible gates for", fid)

    return instance

def populate_sets(instances):
    #use global variables
    global F, G, A, D, W, Lambda

    
    overlaps_set = set(instances["overlaps"])

    F = {f.flight_id: f for f in instances["flights"]}
    """
    flight_id
    aircraft_size
    entity
    arrival_time            #Integers
    arrival_destination
    departure_time          #Integer
    departure_destination
    airline
    arrival_runway          #integer
    """

    real_flight_ids = list(F.keys())
    n = len(real_flight_ids)

    #virtual source and sink flights
    virtual_0  = "F0"
    virtual_n1 = f"F{n+1}"
    F[virtual_0]  = Flight(virtual_0,  "F", "passenger", -1,        "convertible", -1,        "convertible", "virtual", 1)
    F[virtual_n1] = Flight(virtual_n1, "F", "passenger", 24*60+1,   "convertible", 24*60+1,   "convertible", "virtual", 1)

    G = {g.gate_id: g for g in instances["gates"]}
    """
    gate_id
    terminal_proximity
    gate_size
    entity
    apron
    corridor                #Integer
    """

    A = {fid: F[fid] for fid in real_flight_ids}  # arrival flights
    D = {fid: F[fid] for fid in real_flight_ids}  # departure flights

    #unique apron types
    W = set(g.apron for g in G.values())

    #Set of gate types
    K = set((g.terminal_proximity, g.gate_size, g.entity, g.apron, g.corridor) for g in G.values())

    #Set of runways 
    Lambda = [1,2,3,4]

    #Set of apron time windows with u in S_w
    S_w = set(range(0, 24*60, 30)) #every 30 minutes in a day

    #Set of gates belonging to gate type k
    H_k = {k: [g.gate_id for g in G.values() if (g.terminal_proximity, g.gate_size, g.entity, g.apron, g.corridor) == k] for k in K}

    #Set of runway time windows with s in S_r
    S_r = set(range(0, 24*60, 15)) #every 15 minutes in a day

    #Set of arrival flights landing on runway gamma within time window s
    F_s_gamma_A = {(s, gamma): [f.flight_id for f in A.values() if f.arrival_runway == gamma and s <= f.arrival_time < s + 15] for s in S_r for gamma in Lambda}

    #Set of time intervals available between two successive approach flights on runway gamma in time window s, with p in P
#TODO    #P = {(s, gamma): [f.arrival_time for f in A.values() if f.arrival_runway == gamma and s <= f.arrival_time < s + 15] for s in S_r for gamma in Lambda}

    #Set of scheduled departure times within window s
    F_s_D = {s: [f.flight_id for f in D.values() if s <= f.departure_time < s + 15] for s in S_r}

    #F_k[k] = flights compatible with gate type k
    # k = (terminal_proximity, gate_size, entity, apron, corridor)
    _size_order = {"B": 1, "C": 2, "D": 3, "E": 4, "F": 5}
    F_k = {k: [f.flight_id for f in A.values()
               if _size_order[f.aircraft_size] <= _size_order[k[1]]
               and (f.arrival_destination == k[0] or k[0] in ["convertible", "remote"])
               and (f.departure_destination == k[0] or k[0] in ["convertible", "remote"])
               and (f.entity == k[2])] for k in K}
    for k in K:
        F_k[k] += [virtual_0, virtual_n1]

#TODO Determine which runways we want to make available for each flight i   
    #set of runways available for flight i
    Lambda_i = {fid: [1, 2, 3, 4] for fid in F}

    #Boolean parameter, if the gate type k is in apron w , it is 1, and otherwise, it is 0
    chi_kw = {(k, w): 1 if k[3] == w else 0 for k in K for w in W}

    #TODO, seems unnecessary since we don't use Q
    #Boolean parameter, if the flight i is belong to the airline type q, it is 1, and otherwise, it is 0
    #eta_iq

    #Boolean parameter, if the gate type k belongs to remote gate, it is 1, and otherwise, it is 0
    # k = (terminal_proximity, gate_size, entity, apron, corridor); remote stands use apron="REMOTE"
    l_k = {k: 1 if k[3] == "REMOTE" else 0 for k in K}

    #TODO - currently computed in Constraints.py from flight times; populate here once TA/TD are calibrated
    #t_A_ik = {} #start of parking time window for flight i at gate type k
    #t_D_ik = {} #end of parking time window for flight i at gate type k

    #TODO: replace with actual values per aircraft type
    engine_data = {"B": (2, 3.0), "C": (2, 6.0), "D": (2, 9.0), "E": (2, 12.0), "F": (4, 15.0)}
    NE_i = {fid: engine_data[F[fid].aircraft_size][0] for fid in real_flight_ids}
    FF_i = {fid: engine_data[F[fid].aircraft_size][1] for fid in real_flight_ids}
    f_i  = {fid: NE_i[fid] * FF_i[fid] for fid in real_flight_ids}


    #parameter is affected by the gate type k assigned to the flight and the arrival and departure taxiing times
    #rho = {(i,k,u): 1 if t_A_ik in u or t_D_ik in u else 0 for i in F for k in K for u in S_w}

    #Boolean parameter, 1 if flight i arrives or deperatures in time window s, and otherwise 0
    Alpha_is = {(i, s): 1 if s <= F[i].arrival_time < s + 15 or s <= F[i].departure_time < s + 15 else 0 for i in real_flight_ids for s in S_r}

    #upper limit of number of available gates for gate type k
    e_k = {k: len(H_k[k]) for k in K}

    #Time interval treshold between aircraft at a gate
    #TODO, we need to define this, for now we set it to 30 minutes
    ksi = 30

    #Capacity limit of apron w at time u
    N_w_tau = 5

    #Maximum number of flights allowed on the runway during time window s
    mu_sgamma = {(s, gamma): 4 for s in S_r for gamma in Lambda}  #TODO: calibrate per runway

    return {
        "F": F, "G": G, "A": A, "D": D,
        "W": W, "K": K, "Lambda": Lambda,
        "S_w": S_w, "S_r": S_r,
        "H_k": H_k,
        "F_s_gamma_A": F_s_gamma_A,
        "F_s_D": F_s_D,
        "F_k": F_k,
        "Lambda_i": Lambda_i,
        "chi_kw": chi_kw,
        "l_k": l_k,
        "Alpha_is": Alpha_is,
        "e_k": e_k,
        "ksi": ksi,
        "N_w_tau": N_w_tau,
        "mu_sgamma": mu_sgamma,
        "NE_i": NE_i,
        "FF_i": FF_i,
        "f_i": f_i,
        "virtual_0": virtual_0,
        "virtual_n1": virtual_n1,
        "real_flight_ids": real_flight_ids,
        "overlaps_set": overlaps_set,
    }


def print_sets(sets):
    F, G = sets["F"], sets["G"]
    print("=" * 60)
    real_flight_ids = sets.get("real_flight_ids", list(F.keys()))
    virtual_0  = sets.get("virtual_0")
    virtual_n1 = sets.get("virtual_n1")
    print(f"F  (flights, n={len(F)}, real={len(real_flight_ids)}):")
    for fid, f in F.items():
        tag = " [virtual]" if fid in (virtual_0, virtual_n1) else ""
        print(f"  {fid}{tag}: size={f.aircraft_size}, entity={f.entity}, "
              f"arr_time={f.arrival_time}, arr_dest={f.arrival_destination}, "
              f"dep_time={f.departure_time}, dep_dest={f.departure_destination}, "
              f"airline={f.airline}, runway={f.arrival_runway}")

    print(f"\nG  (gates, n={len(G)}):")
    for g in G.values():
        print(f"  {g.gate_id}: proximity={g.terminal_proximity}, size={g.gate_size}, "
              f"entity={g.entity}, apron={g.apron}, corridor={g.corridor}")

    print(f"\nA  (arrival flights)  = same as F ({len(sets['A'])} flights)")
    print(f"D  (departure flights) = same as F ({len(sets['D'])} flights)")

    print(f"\nW  (aprons): {sorted(sets['W'])}")

    print(f"\nK  (gate types, n={len(sets['K'])}):")
    for k in sorted(sets["K"]):
        print(f"  {k}")

    print(f"\nLambda (runways): {sets['Lambda']}")

    print(f"\nH_k (gates per gate type):")
    for k, gates in sorted(sets["H_k"].items()):
        print(f"  {k}: {gates}")

    print(f"\nF_k (compatible flights per gate type):")
    for k, flights in sorted(sets["F_k"].items()):
        print(f"  {k}: {flights}")

    print(f"\nLambda_i (runways per flight):")
    for fid, runways in sets["Lambda_i"].items():
        print(f"  {fid}: {runways}")

    print(f"\ne_k (gate count per gate type):")
    for k, count in sorted(sets["e_k"].items()):
        print(f"  {k}: {count}")

    non_empty_arrivals = {key: v for key, v in sets["F_s_gamma_A"].items() if v}
    print(f"\nF_s_gamma_A (non-empty arrival windows, n={len(non_empty_arrivals)}):")
    for (s, gamma), fids in sorted(non_empty_arrivals.items()):
        print(f"  window {s}-{s+15} min, runway {gamma}: {fids}")

    non_empty_dep = {s: v for s, v in sets["F_s_D"].items() if v}
    print(f"\nF_s_D (non-empty departure windows, n={len(non_empty_dep)}):")
    for s, fids in sorted(non_empty_dep.items()):
        print(f"  window {s}-{s+15} min: {fids}")

    print(f"\nchi_kw (gate type in apron — non-zero entries):")
    for (k, w), val in sorted(sets["chi_kw"].items()):
        if val:
            print(f"  k={k}, w={w}: {val}")

    print(f"\nl_k (remote gate flag):")
    for k, val in sorted(sets["l_k"].items()):
        print(f"  {k}: {val}")

    print(f"\nksi (gate gap threshold): {sets['ksi']} min")
    print(f"N_w_tau (apron capacity): {sets['N_w_tau']}")
    print("=" * 60)

#run the instance only here
if __name__ == "__main__":
    inst = build_instance("paper_case_manuel", seed=38)
    print("Instance built with", len(inst["flights"]), "flights and", len(inst["gates"]), "gates.")
    sets = populate_sets(inst)
    print_sets(sets)