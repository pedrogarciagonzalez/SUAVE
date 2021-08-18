## @ingroup Methods-Power-Fuel_Cell-Discharge
# larminie.py
#
# Created : Apr 2015, M. Vegh 
# Modified: Feb 2016, E. Botero
  
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np
import scipy as sp
from SUAVE.Core import Units
from .SOFC_find_voltage import SOFC_find_voltage
from .SOFC_find_power_diff import SOFC_find_power_diff

# ----------------------------------------------------------------------
#  SOFC discharge model
# ----------------------------------------------------------------------

## @ingroup Methods-Power-Fuel_Cell-Discharge
def SOFC_Discharge(SOFC,conditions):
    '''
    function that determines the mass flow rate based on a required power input
    
    Assumptions:
    None (calls other functions)
    
    Inputs:
    fuel_cell.
        inputs.
            power_in       [W]
        ideal_voltage      [V] 
    
    Outputs:
        mdot               [kg/s]
     
    
    
    
    '''
    
    
    power           = SOFC.inputs.power_required #WHERE IS THIS GIVEN AS AN INPUT???

    lb              = .1*Units.mA/(Units.cm**2.)    #lower bound on fuel cell current density
    ub              = 1200.0*Units.mA/(Units.cm**2.)
    current_density = sp.optimize.fminbound(SOFC_find_power_diff, lb, ub, args=(SOFC, power))

    v          = SOFC_find_voltage(SOFC,current_density)
    SOFC.number_cells = np.round(SOFC.required_power/SOFC.powerpercell)
    power = v*current_density*SOFC.active_area*SOFC.number_cells
    efficiency = np.divide(v, SOFC.ideal_voltage)
    heat_out = power*(1-efficiency)/efficiency

    mdot_fuel_total       = current_density*SOFC.active_area*SOFC.M_H2/(2*SOFC.Faraday*SOFC.fuelutilization)
    mdot_fuel_consumed = mdot_fuel_total*SOFC.fuelutilization
    mdot_fuel_not_consumed = mdot_fuel_total - mdot_fuel_consumed
    mdot_O2_total = current_density*SOFC.active_area*SOFC.M_O2/(4*SOFC.Faraday)
    mdot_air_total = mdot_O2_total/0.23 #CHECK AGAIN
   
    return [v, current_density, power, efficiency, mdot_fuel_total, mdot_fuel_consumed, mdot_fuel_not_consumed, mdot_air_total, heat_out]