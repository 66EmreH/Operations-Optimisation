F = {} #set of flights
A = {} #set of arrival flights
D = {} #set of departure flights
ai = {} #scheduled arrival time i
di = {} #scheduled departure time for flight i 
W = {} #set of aprons
G = {} #set of gates, Gn+1 is remote gate set, G0 is contact gate set
K = {} #set of gate types
Q = {} #set of airline types
Gamma = {} #set of runways
Gammai = {} #set of runways available for flight i
ek = {} #upper limit of number of available gates for gate type k

for i in range(len(F)):
    for j in range(len(k)):
        if ord(F[i].aircraft_size) <= ord(k[j].gate_size):
            if F[i].entity == k[j].entity:
                F_k[i][j] = 1
        
        else:
            F_k[i][j] = 0

#define set of gate types K based on terminal proximity and gate size
def gate_type(Gate):
    return (Gate.terminal_proximity, Gate.gate_size)

K = [gate_type(g) for g in G] 
K = list({gate_type(g) for g in G})

def gate_type(gate):
    return (gate.terminal_proximity, gate.gate_size)

def allowed_park(gate, flight):
    # Check gate size compatibility
    if flight.size > gate.gate_size:
        return False
    
    # Check terminal proximity rules
    if flight.is_international and gate.terminal_proximity != "international":
        return False
    
    # You can add more logic here if needed
    # e.g. arrival/departure restrictions

    return True

def flights_allowed_at_type(k, G, F):
    # k = (terminal_proximity, gate_size)
    prox, size = k
    
    allowed_flights = []
    
    for flight in F:
        # create a fake gate with type k to test compatibility
        test_gate = Gate(prox, size, None, None, None)
        if allowed_park(test_gate, flight):
            allowed_flights.append(flight)
    
    return allowed_flights
