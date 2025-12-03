for i in range(len(F)):
    for j in range(len(k)):
        if ord(F[i].aircraft_size) <= ord(k[j].gate_size):
            if F[i].entity == k[j].entity:
                F_k[i][j] = 1
        
        

        else:
            F_k[i][j] = 0