## @ingroup Methods-Power-Fuel_Cell-Discharge
# SOFC_find_voltage.py
#
# Created : May 2021 Pedro Garcia Gonzalez
  
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np
from SUAVE.Core import Units
from scipy.optimize import fminbound

# ----------------------------------------------------------------------
#  Find Voltage SOFC
# ----------------------------------------------------------------------

## @ingroup Methods-Power-Fuel_Cell-Discharge
def SOFC_find_voltage(SOFC,current_density):
    '''
    function that determines the fuel cell voltage based on an input
    current density and some semi-empirical values to describe the voltage
    drop off with current
    
    Assumptions:
    Voltage curve is a function of current density. Use of several empirical models to determine the operating curve of the SOFC
    
    Inputs:
    current_density           [A/m**2]
    SOFC.parameters
   
    Outputs:
        V                     [V]
         
    
    '''

    # OCV calculation
    GibbsEnergy = SOFC.EnthalpyChange - SOFC.operatingtemperature * SOFC.EntropyChange
    ReversibleVoltage = -GibbsEnergy / (2 * SOFC.Faraday)
    OCV = ReversibleVoltage + SOFC.Rgas * SOFC.operatingtemperature * np.log(SOFC.yH2_mean * np.sqrt(SOFC.yO2_mean) / SOFC.yH2O_mean) / (2 * SOFC.Faraday) + SOFC.Rgas * SOFC.operatingtemperature * np.log(SOFC.operatingpressure / SOFC.Pref) / (4 * SOFC.Faraday)

    # Ohmic losses
    VOhmicLoss = current_density * (SOFC.anodethickness / (SOFC.sigmaanode * SOFC.interfacearea) + SOFC.cathodethickness / (SOFC.sigmacathode * SOFC.interfacearea) + SOFC.electrolytethickness / (SOFC.sigmaelectrolyte * SOFC.interfacearea) + SOFC.interconnectthickness / (SOFC.sigmainterconnect * SOFC.interfacearea))

    # Activation losses
    def fcnAnode(VActivationLoss):
        return abs(2 * SOFC.i0Anode * np.sinh(SOFC.ne * SOFC.Faraday * SOFC.VActivationLoss / (2 * SOFC.Rgas * SOFC.operatingtemperature)) - current_density) ** 2
    def fcnCathode(VActivationLoss):
        return abs(2 * SOFC.i0Cathode * np.sinh(SOFC.ne * SOFC.Faraday * SOFC.VActivationLoss / (2 * SOFC.Rgas * SOFC.operatingtemperature)) - current_density) ** 2
    VActivationLossAnode = sp.optimize.fminbound(fcnAnode, 0.00001, 10)
    VActivationLossCathode = sp.optimize.fminbound(fcnCathode, 0.00001, 10)
    VActivationLoss = VActivationLossAnode + VActivationLossCathode

    # Concentration losses
    VConcentrationLoss = SOFC.m * np.exp(SOFC.n * current_density / 10)

    # Final voltage
    V = OCV - VOhmicLoss - VConcentrationLoss - VActivationLoss

    return V