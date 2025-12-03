import numpy as np

F = {}
A = {} #set of arrival flights
D = {} #set of departure flights
ai = {} #scheduled arrival time i
di = {} #scheduled departure time for flight i 
W = {} #set of aprons
G = {} #set of gates, Gn+1 is remote gate set, G0 is contact gate set
K = {} #set of gate types

X_kw = np.zeros((len(K), len(W))) #binary variable, 1 if gate type k is in apron w, 0 otherwise
l_k = np.zeros((len(K), len(W))) #binary variable, 1 if gate type k belongs to remote gate, 0 otherwise

for i in range(len(K)):
    for j in range(len(W)):
        if K[i].apron == W[j]:
            X_kw[i][j] = 1
            
F_k = np.zeros((len(F), len(K))) #binary variable, 1 if flight i can be assigned to gate k, 0 otherwise
for i in range(len(F)):
    for j in range(len(K)):
        if ord(F[i].aircraft_size) <= ord(K[j].gate_size):
            if F[i].entity == K[j].entity:
                if F[i].arrival_destination == K[j].terminal_proximity and F[i].departure_destination == K[j].terminal_proximity or K[j].terminal_proximity == "convertible" or K[j].terminal_proximity == "remote":
                    F_k[i][j] = 1

