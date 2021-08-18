import numpy as np
import matplotlib as plt
from SUAVE.Methods.Propulsion.ConstraintAnalysis.Verification.PlotConstraintAnalysis import *
from SUAVE.Methods.Propulsion.ConstraintAnalysis.Verification.SolutionPointConstraintAnalysis import *

##### Define power management schedule for propulsion system
# Takeoff
phi_takeoff = 0.6 # Gas turbine power/Total power
psi_takeoff = 0.9 # SOFC power/SOFC+Battery power
lambdaa_takeoff = 0.1 # Electric payload power/Total electric power

# Climb
phi_climb = 0.6 # Gas turbine power/Total power
psi_climb = 0.9 # SOFC power/SOFC+Battery power
lambdaa_climb = 0.1 # Electric payload power/Total electric power

# Cruise
phi_cruise = 0.6 # Gas turbine power/Total power
psi_cruise = 0.9 # SOFC power/SOFC+Battery power
lambdaa_cruise = 0.1 # Electric payload power/Total electric power

# Descent
phi_descent = 0.6 # Gas turbine power/Total power
psi_descent = 0.9 # SOFC power/SOFC+Battery power
lambdaa_descent = 0.1 # Electric payload power/Total electric power

# Landing
phi_landing = 0.6 # Gas turbine power/Total power
psi_landing = 0.9 # SOFC power/SOFC+Battery power
lambdaa_landing = 0.1 # Electric payload power/Total electric power


# Define power management schedule

select_design_point_constraint_analysis()