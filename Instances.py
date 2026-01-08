#List of flight and gate instances that the model can run.

#manually make a few flights and gates, for bug fixing
test_case = {"seed": 1,
    "flights": {"mode": "fixed",
        "list": [
            # flight_id, aircraft_size, entity, arr_time, arr_dest, dep_time, dep_dest, airline, arrival runway
            ("F1", "C", "passenger",  60, "domestic",      120, "domestic",      "A1", "01"),
            ("F2", "C", "passenger",  80, "international", 140, "international", "A1", "01"),
            ("F3", "B", "cargo",     100, "domestic",      160, "domestic",      "C1", "01"),
        ],
    },

    "gates": {"mode": "fixed",
        "list": [
            # gate_id, terminal_proximity, gate_size, entity, apron, corridor
            ("G1", "domestic",      "C", "passenger", "A", 1),
            ("G2", "international", "C", "passenger", "A", 1),
            ("G3", "convertible",   "F", "cargo",     "B", 1),
        ],
    },
}

#Reconstruct the case as in the paper
paper_case = {"seed": 42,
    "flights": {
        "mode": "generated",
        "horizon_start": 0,
        "horizon_end": 24 * 60,

        "n_flights": 1200,
        "sizes": {"B": 0.02, "C": 0.80, "D": 0.0, "E": 0.17, "F": 0.01},
        "entities": {"passenger": 0.90, "cargo": 0.10},
        "international_share": 0.20,
        "turnaround": {"B": 25, "C": 35, "D": 50, "E": 110, "F": 150,},
        "airlines": ["A1", "A2", "A3", "B1", "B2", "C1"],
        "Arrival_runways": ["01"]
    },

    "gates": {
        "mode": "apron_template",
        "apron_counts": {"A1": [8], 
                         "A2": [12], 
                         "A3": [11], 
                         "A4": [16],
                         "A5": [15],
                         "A6": [11],
                         "A7": [10],
                         "A8": [13],
                         "A9": [10],
                         "A10": [17],
                         "A11": [21],
                         "A12": [19],
                         "A13": [9],
                         "A14": [6],
                         "A15": [20],
                         "A16": [18],
                         "A17": [19],
                         "A18": [24],
                          }, 
        "terminal_proximity_share": {"domestic": 0.45, "international": 0.4, "convertible": 0.15,},
        "gate_sizes": {"B": 0.05, "C": 0.45, "D": 0.2, "E": 0.25, "F": 0.05}, #Dist of gate sizes
        "entities": {"passenger": 0.8, "cargo": 0.20},
    },

}