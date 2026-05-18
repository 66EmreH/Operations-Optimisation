from Instance_builder import build_instance, save_to_excel, populate_sets
from collections import Counter
from Model import build_model



#---------- TEST CASE ----------
print("=== TEST CASE ===")
test_inst = build_instance("test_case", seed=1)

# ---------- PAPER CASE ----------
inst = build_instance("paper_case_manuel", seed=38)

#Populate sets from instances
flights = inst["flights"]
gates = inst["gates"]
compat = inst["compat"]

#Save the instance data to an Excel file
save_to_excel(flights, gates, filename="paper_case_data.xlsx")

#
sets  = populate_sets(test_inst)
model = build_model(sets)