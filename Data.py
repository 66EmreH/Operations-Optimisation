import random
from Classes import Flight, Gate
from Instances import test_case, paper_case

#Functions to construct data from the instances
#Build instance runs all other functions inside of it.


#Helpers---------------------------------------------------------
#See which case we want to run
def get_case(case_name):
    if case_name == "test_case":
        return test_case
    if case_name == "paper_case":
        return paper_case
    raise ValueError("Unknown case_name")
#Perform a weighted choice
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


#Building Data---------------------------------------------------
#Build flights
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

        flights.append(
            Flight(flight_id, size, entity, arr_time, arr_dest, dep_time, dep_dest, airline)
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
    # Hard rules:
    # 1) entity must match - cargo or pax
    # 2) aircraft size must fit in gate size
    # 3) international flights cannot use domestic gates

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
