class Gate:
    def __init__(self, terminal_proximity, gate_size, entity, apron, corridor):
        self.terminal_proximity = terminal_proximity #Proximity to terminal bridge
        self.gate_size = gate_size #Size of the gate Maximum aircraft size that can be accommodate classified as B,C,D,E,F
        self.entity = entity #Entities served by gate (passengers or cargo)
        self.apron = apron #Apron location of the gate
        self.corridor = corridor #Corridor location of the gate

class Flight:
    def __init__(self, aircraft_size, entity, arrival_time, arrival_destination, departure_time, departure_destination, airline):
        self.aircraft_size = aircraft_size #Size of the aircraft classified as B,C,D,E,F
        self.entity = entity #Entities of the flight (passengers or cargo)
        self.arrival_time = arrival_time #Arrival time of the flight
        self.arrival_destination = arrival_destination #Arrival destination of the flight (domestic or international)
        self.departure_time = departure_time #Departure time of the flight
        self.departure_destination = departure_destination #Departure destination of the flight (domestic or international)
        self.airline = airline #Airline operating the flight
    
    def __repr__(self):
        return (
            f"Flight("
            f"size={self.aircraft_size}, "
            f"entity={self.entity}, "
            f"arr={self.arrival_destination}@{self.arrival_time}, "
            f"dep={self.departure_destination}@{self.departure_time}, "
            f"airline={self.airline})"
        )
