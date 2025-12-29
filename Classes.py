#Define the flight and gate classes.
class Gate:
    def __init__(self, gate_id, terminal_proximity, gate_size, entity, apron, corridor):
        self.gate_id = gate_id
        self.terminal_proximity = terminal_proximity #Proximity to terminal bridge
        self.gate_size = gate_size #Size of the gate Maximum aircraft size that can be accommodate classified as B,C,D,E,F
        self.entity = entity #Entities served by gate (passengers or cargo)
        self.apron = apron #Apron location of the gate
        self.corridor = corridor #Corridor location of the gate

    def __repr__(self):
        return (
            f"Gate({self.gate_id}), Size:{self.gate_size}, {self.entity} gate"
        )

class Flight:
    def __init__(self, flight_id, aircraft_size, entity, arrival_time, arrival_destination, departure_time, departure_destination, airline):
        self.flight_id = flight_id
        self.aircraft_size = aircraft_size
        self.entity = entity
        self.arrival_time = arrival_time #Minutes
        self.arrival_destination = arrival_destination #Int or dom
        self.departure_time = departure_time #Minutes
        self.departure_destination = departure_destination #Int or dom
        self.airline = airline

    def is_international(self):
        return (
            self.arrival_destination == "international"
            or self.departure_destination == "international"
        )

    def occupancy_window(self):
        return (self.arrival_time, self.departure_time)

    def __repr__(self):
        return (
            f"Flight({self.flight_id}, "
            f"{self.arrival_destination}@{self.arrival_time} -> "
            f"{self.departure_destination}@{self.departure_time}, "
            f"size={self.aircraft_size})"
        )
