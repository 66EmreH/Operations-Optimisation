F = {}
A = {} #set of arrival flights
D = {} #set of departure flights
ai = {} #scheduled arrival time i
di = {} #scheduled departure time for flight i 
W = {} #set of aprons
G = {} #set of gates, Gn+1 is remote gate set, G0 is contact gate set
K = {} #set of gate types

for i in range(len(F)):
    for j in range(len(k)):
        if ord(F[i].aircraft_size) <= ord(k[j].gate_size):
            if F[i].entity == k[j].entity:
                F_k[i][j] = 1
        
        

        else:
            F_k[i][j] = 0
