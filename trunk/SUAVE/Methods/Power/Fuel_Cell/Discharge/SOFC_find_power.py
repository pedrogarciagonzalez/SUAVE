## @ingroup Methods-Power-Fuel_Cell-Discharge
# find_power_larminie.py
#
# Created : Apr 2015, M. Vegh 
# Modified: Sep 2015, M. Vegh
#           Feb 2016, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np
from SUAVE.Core import Units
from .SOFC_find_voltage import SOFC_find_voltage

# ----------------------------------------------------------------------
#  Find Power Larminie
# ----------------------------------------------------------------------

## @ingroup Methods-Power-Fuel_Cell-Discharge
def SOFC_find_power(current_density, SOFC, sign=1.0):
    '''
    Function that determines the power output per cell, based on in 
    input current density
    
    Assumptions:
    None(calls other functions)
    
    Inputs:
    current_density      [Amps/m**2]
    fuel cell.
        interface area   [m**2]
        
    Outputs:
    power_out            [W]
    
    '''
    
    # sign variable is used so that you can maximize the power, by minimizing the -power
    i1            = current_density
    A             = SOFC.interface_area
    v             = SOFC_find_voltage(SOFC,current_density)  #useful voltage vector
    power_out     = sign*np.multiply(v,i1)*A       #obtain power output in W/cell
    
    #want to minimize
    return power_out