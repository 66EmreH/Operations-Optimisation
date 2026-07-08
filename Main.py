from Instance_builder import build_instance, save_to_excel, populate_sets, build_compatibility, build_overlaps
from Model import build_model
import pandas as pd

#Model parameters to set and possibly change if needed/wanted
Case = "paper_case_manuel_fixed" # "test_case" or "paper_case_manuel"
WINDOW_MIN = 240   #Length of each rolling-horizon window in minutes (4 hours)

def solve_rolling_horizon(all_flights, gates, case, seed, window_min, max_windows=None):
    if not all_flights:
        print("No flights to schedule; nothing to do.")
        return []
    if window_min <= 0:
        raise ValueError(f"window_min must be positive, got {window_min}")
    all_flights = sorted(all_flights, key=lambda f: f.arrival_time)
    flight_by_id = {f.flight_id: f for f in all_flights}

    t_start = all_flights[0].arrival_time
    t_end   = all_flights[-1].arrival_time

    carried_pins = {}   #flight_id -> gate_id, occupants held from earlier windows
    results = []        #one row per flight for the whole day
    window_count = 0
    window_objectives = []   #(label, objective) per solved window
    total_objective = 0.0

    lo = t_start
    while lo <= t_end:
        if max_windows is not None and window_count >= max_windows:
            break
        hi = lo + window_min

        #Drop pins of flights that already departed (covers empty windows too).
        carried_pins = {fid: h for fid, h in carried_pins.items()
                        if flight_by_id[fid].departure_time > lo}
        #Flights arriving in this window, plus carried-over occupants still parked.
        window_flights = [f for f in all_flights if lo <= f.arrival_time < hi]
        carried_flights = [flight_by_id[fid] for fid in carried_pins]
        sub_flights = carried_flights + window_flights

        #print hi and low hour in hour:minute format
        hi_hour = hi // 60
        hi_minute = hi % 60
        lo_hour = lo // 60
        lo_minute = lo % 60
        if window_flights:
            window_count += 1
            print(f"\n=== Window {lo_hour}:{lo_minute:02d}-{hi_hour}:{hi_minute:02d} min: {len(window_flights)} new + {len(carried_flights)} carried flights ===")

            #Build the sub-instance for this window and solve it.
            sub_instance = {
                "case_name": case, "seed": seed,
                "flights": sub_flights, "gates": gates,
                "compat": build_compatibility(sub_flights, gates),
                "overlaps": build_overlaps(sub_flights),
            }
            sets = populate_sets(sub_instance)
            m, assignments, window_obj = build_model(sets, pinned=carried_pins)

            label = f"{lo_hour}:{lo_minute:02d}-{hi_hour}:{hi_minute:02d}"

            #No solution in this window: save what we have and stop the whole run.
            if m.SolCount == 0:
                pd.DataFrame(results).to_excel("gate_assignment_results.xlsx", index=False)
                raise SystemExit(
                    f"ERROR: window {label} produced no solution (Gurobi status {m.Status}). "
                    f"Stopping. Partial results for {len(results)} flights were saved to "
                    f"gate_assignment_results.xlsx.")

            #Objective counting each flight only in the window it was first assigned.
            window_objectives.append((label, window_obj))
            total_objective += window_obj

            #Record the flights newly decided in this window (carried ones were already recorded in the window where they first arrived).
            for f in window_flights:
                if f.flight_id in assignments:
                    results.append({"flight_id": f.flight_id, "gate_id": assignments[f.flight_id]})

            #Carry forward every flight still parked at the window end.
            carried_pins = {fid: assignments[fid] for fid in assignments
                            if flight_by_id[fid].departure_time > hi}

        lo = hi

    pd.DataFrame(results).to_excel("gate_assignment_results.xlsx", index=False)
    print(f"\nRolling horizon done: {len(results)} flights assigned across {window_count} window(s).")

    print("\n=== Final objective values ===")
    for label, obj in window_objectives:
        print(f"   Window {label}: {obj:.2f}")
    print(f"   Total objective across {window_count} window(s): {total_objective:.2f}")
    return results

#See what instance to use
if Case == "test_case":
    instance = build_instance("test_case", seed=1)
elif Case == "paper_case_manuel":
    instance = build_instance("paper_case_manuel", seed=1)
elif Case == "paper_case_manuel_fixed":
    instance = build_instance("paper_case_manuel_fixed", seed=1)
elif Case ==  "paper_case_manuel_instance_updated":
    instance = build_instance("paper_case_manuel_instance_updated", seed=1)

#Populate sets from instances
flights = instance["flights"]
gates = instance["gates"]

#Save the instance data to an Excel file
if Case != "paper_case_manuel_fixed": #Don't overwrite the fixed instance, which is used for testing
    save_to_excel(flights, gates, filename=f"{Case}_instance.xlsx")

#Run the model with rolling horizon over WINDOW_MIN-minute windows.
solve_rolling_horizon(flights, gates, Case, instance["seed"], WINDOW_MIN)