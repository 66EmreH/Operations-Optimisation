from Classes import *

#Sets
#F = {} #set of flights
#A = {} #set of arrival flights
#D = {} #set of departure flights
#W = {} #set of aprons
#G = {} #set of gates, Gn+1 is remote gate set, G0 is contact gate set
#K = {} #set of gate types
#Q = {} #set of airline types
#Lambda = {} #set of runways
#S_w = {} #Set of apron time windows with u in S_w
#H_k = {} #Set of gates belonging to gate type k
#S_r = {} #Set of runway time windows with s in S_r
#F_s_gamma_A = {} #Set of arrival flights landing on runway gamma within time window s
#P = {} #Set of time intervals available between two successive approach flights on runway gamma in time window s, with p in P
#F_s_D = {} #Set of scheduled departure times within window s

#Subsets
#F_k = {}       # F_k[k] = flights compatible with gate type k
#Lambda_i = {}  # set of runways available for flight i

#Boolean
#chi_kw = {}    #Boolean parameter, if the gate type k is in apron w , it is 1, and otherwise, it is 0
#eta_iq = {}    #Boolean parameter, if the flight i is belong to the airline type q, it is 1, and otherwise, it is 0
#l_k = {}       #Boolean parameter, if the gate type k belongs to remote gate, it is 1, and otherwise, it is 0
#rho = {}       #Boolean parameter, 1 if flight i is in apron time window u when parked at apron h of type k, else 0
#Alpha_is = {}  #Boolean parameter, 1 if flight i arrives or departs in time window s, and otherwise 0

#Parameters
#e_k = {}       #upper limit of number of available gates for gate type k
#ksi = {}       #Time interval threshold between aircraft at a gate
#t_A_ik = {}    #start of parking time window for flight i at gate type k
#t_D_ik = {}    #end of parking time window for flight i at gate type k
#N_w_tau = {}   #Capacity limit of apron w at time u
#mu_sgamma = {} #Maximum number of flights allowed on the runway during time window s
#delta_tp = {}  #Time interval between two successive flights on runway gamma in time window s
#t_a = {}       #average departure time of flight i in F^s_D
#d_safety = 0   #average safety interval on runway gamma

TA = {} #taxiing time from runway γ to gate type k for arriving flight i
TD = {} #taxiing time from gate type k to runway γ for departing flight i

#Times
#ai = {}   # scheduled arrival time of flight i
#di = {}   # scheduled departure time of flight i

#Derived parameters
#f_i = {}       #Fuel consumption per unit taxi time for flight i
#delta_ijk = {} #Time interval between flight i and flight j for gate type k

#Airplane parameters
#FF_i = {}  #fuel flow rate of flight i
#NE_i = {}  #number of engines of flight i

#Taxi time related
#T_mini = {} #Potential minimum total taxiing time of flight i when any available runway-gate type combination is selected
#T_ki = {}   #Additional taxi time for flight i if assigned to gate type k
#Time_i = {} #Taxiing time for flight i

M = 10e6   #Big M

#Objective weights
C1 = 1.0   # taxi / fuel weight
C2 = 1.0   # robustness weight
C3 = 1.0   # remote gate penalty weight
