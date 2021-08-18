## @ingroup Methods-Power-Fuel_Cell-Sizing
# initialize_SOFC_from_power.py
#
# Created : 02/2021

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import scipy as sp
import numpy as np
from SUAVE.Core import Units
from SUAVE.Methods.Power.Fuel_Cell.Discharge.SOFC_find_power import SOFC_find_power

# ----------------------------------------------------------------------
#  Initialize SOFC from Power
# ----------------------------------------------------------------------

## @ingroup Methods-Power-Fuel_Cell-Sizing
def initialize_SOFC_from_power(SOFC,power):
    '''
    Initializes extra parameters for the fuel cell when using the Larminie method
    Determines the number of stacks
    
    Inputs:
    power                 [W]
    fuel_cell
    
    Outputs:
    
    fuel_cell.
        power_per_cell    [W]
        number_of_cells
        max_power         [W]
        volume            [m**3]
        specific_power    [W/kg]
        mass_properties.
            mass          [kg]
       
        
    '''
    
    
    
    fc                      = SOFC
    lb                      = .1*Units.mA/(Units.cm**2.)    #lower bound on fuel cell current density
    ub                      = 1200.0*Units.mA/(Units.cm**2.)
    sign                    = -1. #used to minimize -power
    current_density         = sp.optimize.fminbound(SOFC_find_power, lb, ub, args=(fc, sign)) #Finds the current denstiy that matches the power, given by aircraft performance requirements
    power_per_cell          = SOFC_find_power(current_density,fc) #Obtain back power from current density
    
    fc.number_of_cells      = np.ceil(power/power_per_cell)
    fc.max_power            = fc.number_of_cells*power_per_cell #Need to recompute due to
    fc.volume               = fc.number_of_cells*fc.interface_area*fc.total_thickness
    fc.mass_properties.mass = fc.volume*fc.cell_density*fc.porosity_coefficient #fuel cell mass in kg
    fc.mass_density         = fc.mass_properties.mass/fc.volume
    fc.specific_power       = fc.max_power/fc.mass_properties.mass #fuel cell specific power in W/kg