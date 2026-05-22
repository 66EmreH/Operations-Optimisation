from Instance_builder import build_instance, save_to_excel, populate_sets
from collections import Counter
from Model import build_model


#Model parameters to set and possibly change if needed/wanted
Case = "paper_case_manuel" # "test_case" or "paper_case_manuel"



#See what instance to use
if Case == "test_case":
    instance = build_instance("test_case", seed=1)
elif Case == "paper_case_manuel":
    instance = build_instance("paper_case_manuel", seed=1)

#Populate sets from instances
flights = instance["flights"]
gates = instance["gates"]
compat = instance["compat"]


#Save the instance data to an Excel file
save_to_excel(flights, gates, filename=f"{Case}_instance.xlsx")

#Run model, first by filling in all required sets and parameters, then building and running the model
sets  = populate_sets(instance)
model = build_model(sets)