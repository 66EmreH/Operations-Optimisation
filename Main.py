from Data import build_instance

# ---------- TEST CASE ----------
print("=== TEST CASE ===")
inst = build_instance("test_case", seed=1)

print("Number of flights:", len(inst["flights"]))
print("Number of gates:", len(inst["gates"]))
print("Number of overlaps:", len(inst["overlaps"]))

print("\nFlights:")
for f in inst["flights"]:
    print(f)

print("\nCompatible gates per flight:")
for fid, gates in inst["compat"].items():
    print(fid, "->", len(gates), gates)

# ---------- PAPER CASE ----------
print("\n=== PAPER CASE ===")
inst = build_instance("paper_case", seed=38)

print("Number of flights:", len(inst["flights"]))
print("Number of gates:", len(inst["gates"]))
print("Number of overlaps:", len(inst["overlaps"]))

# quick sanity checks
max_dep = max(f.departure_time for f in inst["flights"])
print("Max departure time:", max_dep)

print("\nFirst 5 flights:")
for f in inst["flights"][:5]:
    print(f)

print("\nFirst 5 gates:")
for g in inst["gates"][:5]:
    print(g)

from collections import Counter

flights = inst["flights"]
gates = inst["gates"]
compat = inst["compat"]

print("\n--- paper_case diagnostics ---")

flight_sizes = Counter(f.aircraft_size for f in flights)
gate_sizes = Counter(g.gate_size for g in gates)
print("Flight sizes:", flight_sizes)
print("Gate sizes:", gate_sizes)

flight_entities = Counter(f.entity for f in flights)
gate_entities = Counter(g.entity for g in gates)
print("Flight entities:", flight_entities)
print("Gate entities:", gate_entities)

intl_flights = sum(1 for f in flights if f.is_international())
dom_flights = len(flights) - intl_flights
print("Flights intl/dom:", intl_flights, "/", dom_flights)

dom_gates = sum(1 for g in gates if g.terminal_proximity == "domestic")
intl_gates = sum(1 for g in gates if g.terminal_proximity == "international")
conv_gates = sum(1 for g in gates if g.terminal_proximity == "convertible")
print("Gates dom/intl/conv:", dom_gates, "/", intl_gates, "/", conv_gates)

zero_compat = [fid for fid, allowed in compat.items() if len(allowed) == 0]
print("Flights with 0 compatible gates:", len(zero_compat))
if len(zero_compat) > 0:
    print("Example:", zero_compat[:10])
