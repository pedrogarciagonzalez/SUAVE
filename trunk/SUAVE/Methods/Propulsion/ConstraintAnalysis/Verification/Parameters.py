import numpy as np
import matplotlib as plt

# Basic thermodynamic parameters (SI units)
Rgas = 287
g = 9.81
cpgas = 1004
gamma = 1.4
T_SL = 288
P_SL = 101325
rho_SL = 1.225
h_tropopause = 11000
T_tropopause = 216.7
P_tropopause = P_SL * (1 - 0.0065 * h_tropopause / T_SL)**(5.2561)
rho_tropopause = P_tropopause/(Rgas*T_tropopause)

# Aircraft performance design requirements
Range = 2873000
V_stall = 64.3
M_cruise = 0.74
M_max = 0.78
h_cruise = 37000 * 0.3048
S_TO = 2270
timetoclimbtoFL350=18*60
ROC = 35000*0.3048/timetoclimbtoFL350
h_service_ceiling=37000*0.3048
ROC_service_ceiling=0.5
LandingDistance = 1400

# Atmospheric operation condition and speed of the aircraft
if h_cruise <= h_tropopause:
    T_cruise = T_SL-0.0065*h_cruise
    P_cruise = P_SL*(1-0.0065*h_cruise/T_SL)**(5.2561)
else:
    T_cruise = T_tropopause
    P_cruise = P_tropopause * np.exp(-g / (Rgas * T_tropopause) * (h_cruise - h_tropopause))
rho_cruise = P_cruise / (Rgas * T_cruise)
sigma_cruise = rho_cruise / rho_SL
if h_service_ceiling <= h_tropopause:
    T_service_ceiling = T_SL-0.0065*h_service_ceiling
    P_service_ceiling = P_SL*(1-0.0065*h_service_ceiling/T_SL)**(5.2561)
else:
    T_service_ceiling = T_tropopause
    P_service_ceiling = P_tropopause*np.exp(-g/(Rgas*T_tropopause)*(h_service_ceiling-h_tropopause))
rho_service_ceiling = P_service_ceiling/(Rgas*T_service_ceiling)
sigma_service_ceiling = rho_service_ceiling/rho_SL
V_cruise = M_cruise * np.sqrt(gamma * Rgas * T_cruise)
V_max = M_max * np.sqrt(gamma * Rgas * T_cruise)

# Aircraft geometric design parameters
S_wing = 51.2
AspectRatio = 7.8
cV_ClimbGradient = 0.03 #Assumption for AR=7.8

# Aircraft aerodynamic design parameters
clmax = 2.5
cd0 = 0.034
Oswald = 0.8
K_aerodynamics = 1 / (np.pi * Oswald * AspectRatio)
mu = 0.05
cl_cruise = 0.3
delta_cl_flap_takeoff = 0.6
cd0_LG = 0.01
cd0_HLD = 0.006
cdG = cd0 + cd0_LG + cd0_HLD + K_aerodynamics*(cl_cruise + delta_cl_flap_takeoff)**2 + mu*(cl_cruise + delta_cl_flap_takeoff)
clR= clmax/1.21
LD_max = 15
clmax_landing = 2.8 #Assumption
nmax=1.3

# Aircraft weight characteristics
MTOW = 22000*g #Estimation
MLW = 19300*g #Estimation
FractionWeightLanding = MLW/MTOW
NumberEngines = 2

# Range of values of wing loading
WS = list(range(1000,9000,1))

# Efficiencies for constraint analysis matrix (change by input from PyCycle analysis)
eta_valve = 0.99
eta_gasturbine_1 = 0.5
eta_gasturbine_2 = 0.4
eta_powermanagement_1 = 0.98
eta_powermanagement_2 = 0.98
eta_electricmotor = 0.9
eta_propulsive_1 = 0.8
eta_propulsive_2 = 0.8