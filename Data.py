import numpy as np
from Classes import Flight
import matplotlib.pyplot as plt
from collections import Counter

#Generation of example data to use
#-------------------------------------------------------------------------------------------
#Set the parameters of the data, such as distribution of domestic/int etc...
Flight_Distribution = {
    # Domestic 
    "p_domestic_arrival":   0.85,
    "p_domestic_departure": 0.85,
    # Passenger vs Cargo
    "p_passenger": 0.95,
    # Aircraft size distribution
    "aircraft_size_probs": {
        "B": 0.10,
        "C": 0.55,
        "D": 0.20,
        "E": 0.10,
        "F": 0.05,
    },
    # Airline distribution 
    "airline_probs": {
        "CZ": 0.50,
        "ZH": 0.10,
        "CA": 0.10,
        "FM": 0.08,
        "JD": 0.07,
        "AK": 0.05,
        "OQ": 0.05,
        "GJ": 0.05,
    },
}

Gate_distribution = {
    #Gate size
    "gate_size": {
        "B": 0.05,
        "C": 0.45,
        "D": 0.20,
        "E": 0.25,
        "F": 0.05,
    },

    #Gate entitity
    "gate_pax": 0.75,

    #Terminal proximity
    "terminal_proximity": {
        "Domestic": 0.5,
        "International": 0.4,
        "Convertible": 0.10,
    },

    #Gates att apron (237 total) MENTION SIMPLIFICATION THAT THERE IS NO CORRELATION APPRON AND TYPE OF GATE
    "Appron_gates": {
        "1": 8,
        "2": 12,
        "3": 11,
        "4": 16,
        "5": 15,
        "6": 10,
        "7": 9,
        "8": 13,
        "9": 9,
        "10": 17,
        "11": 22,
        "12": 20,
        "13": 8,
        "14": 6,
        "15": 21,
        "16": 18,
        "17": 20,
        "18": 24,
    }
}

#-------------------------------------------------------------------------------------------
#sample randomly
def _sample_from_dict(rng, prob_dict, n):
    labels = list(prob_dict.keys())
    probs  = np.array(list(prob_dict.values()), dtype=float)
    probs /= probs.sum()
    return rng.choice(labels, size=n, p=probs)

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#Flight generator
#We do this by making a list of aircraft sizes randomly, and attributing it to the flight with the same rank
def generate_flights(n_flights: int,cfg: dict | None = None,seed: int | None = 42):
    if cfg is None:
        cfg = Flight_Distribution
    rng = np.random.default_rng(seed)

    #Sample categorical attributes
    aircraft_sizes = _sample_from_dict(rng, cfg["aircraft_size_probs"], n_flights)
    airlines = _sample_from_dict(rng, cfg["airline_probs"], n_flights)

    #Domestic / international for arrival & departure
    arrival_destinations = np.where(rng.random(n_flights) < cfg["p_domestic_arrival"],"domestic","international")
    departure_destinations = np.where(rng.random(n_flights) < cfg["p_domestic_departure"],"domestic","international")

    #Passenger / cargo
    entities = np.where(rng.random(n_flights) < cfg["p_passenger"],"passenger","cargo")

    #Simple time model: minutes in day
    arrival_times = rng.integers(0, 1400, size=n_flights)
    
    #departure 30–180 minutes after arrival
    departure_times = arrival_times + rng.integers(30, 180, size=n_flights)

    #build Flight objects
    flights = []
    for i in range(n_flights):
        f = Flight(
            aircraft_size       = aircraft_sizes[i],
            entity              = entities[i],
            arrival_time        = int(arrival_times[i]),
            arrival_destination = arrival_destinations[i],
            departure_time      = int(departure_times[i]),
            departure_destination = departure_destinations[i],
            airline             = airlines[i],
        )
        flights.append(f)
    return flights

flights = generate_flights(1200)

#-------------------------------------------------------------------------------------------
#Plotting the flight data to verify by visual inspection
def plot_flight_distributions(flights):
    # ---------- Domestic vs International (arrival) ----------
    labels_dom = ["Domestic", "International"]
    counts_dom = [
        sum(f.arrival_destination == "domestic" for f in flights),
        sum(f.arrival_destination == "international" for f in flights),
    ]

    plt.figure()
    plt.pie(counts_dom, labels=labels_dom, autopct="%1.1f%%")
    plt.title("Arrival destination: Domestic vs International")
    plt.show()

    # ---------- Passenger vs Cargo ----------
    labels_ent = ["Passenger", "Cargo"]
    counts_ent = [
        sum(f.entity == "passenger" for f in flights),
        sum(f.entity == "cargo" for f in flights),
    ]

    plt.figure()
    plt.pie(counts_ent, labels=labels_ent, autopct="%1.1f%%")
    plt.title("Entity: Passenger vs Cargo")
    plt.show()

    # ---------- Aircraft size distribution (B–F) ----------
    sizes = [f.aircraft_size for f in flights]
    size_counts = Counter(sizes)
    size_labels = sorted(size_counts.keys())
    size_values = [size_counts[s] for s in size_labels]

    plt.figure()
    plt.bar(size_labels, size_values)
    plt.xlabel("Aircraft size class")
    plt.ylabel("Number of flights")
    plt.title("Aircraft size distribution")
    plt.show()

    # ---------- Airline distribution + % domestic (like Fig. 11) ----------
    airlines_all = [f.airline for f in flights]
    airlines_dom = [f.airline for f in flights
                    if f.arrival_destination == "domestic"]

    total_counts = Counter(airlines_all)
    dom_counts = Counter(airlines_dom)

    # ---- SORT airlines by descending total flight count ----
    sorted_airlines = sorted(
        total_counts.keys(),
        key=lambda a: total_counts[a],
        reverse=True
    )

    nums = [total_counts[a] for a in sorted_airlines]
    domestic_pct = [
        100 * dom_counts[a] / total_counts[a]
        for a in sorted_airlines
    ]

    # ---- Plot ----
    fig, ax1 = plt.subplots()

    ax1.bar(sorted_airlines, nums)
    ax1.set_xlabel("Airline (IATA)")
    ax1.set_ylabel("Number of flights")

    ax2 = ax1.twinx()
    ax2.plot(sorted_airlines, domestic_pct, marker="o")
    ax2.set_ylabel("Percentage of domestic flights (%)")

    plt.title("Airline attributes (count + % domestic)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_flight_distributions(flights)


#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
#Gate generator
