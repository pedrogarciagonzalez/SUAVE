## @ingroup Methods-Power-Fuel_Cell-Discharge
# setup_larminie.py
#
# Created : May 2021 Pedro Garcia Gonzalez
#
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import SUAVE
from SUAVE.Core import Units
from .SOFC_Discharge import SOFC_Discharge

# ----------------------------------------------------------------------
#  Setup SOFC Performance
# ----------------------------------------------------------------------

## @ingroup Methods-Power-Fuel_Cell-Discharge
#default values representative of a hydrogen fuel cell
def SOFC_setup(SOFC):
   """ sets up additional values of SOFC required for the performance model, to obtain the V-i curve and operating point.
   
   Inputs:
       SOFC object
    
   Outputs:
       SOFC.parameters_for_model


   """

   # Constants
   SOFC.Faraday = 96485.3329  # C / mol
   SOFC.Rgas = 8.31446261815324  # J / molK
   SOFC.LHV = 120000000  # J / kg
   SOFC.M_H2 = 0.00201568  # kg / mol
   SOFC.M_O2 = 0.032  # kg / mol
   SOFC.M_H2O = 0.01801528  # kg / mol
   SOFC.M_N2 = 0.0280134  # kg / mol

   # Performance design variables
   SOFC.fuelutilization = 0.75
   SOFC.operatingtemperature = 1173  # Assume constant operating temperature
   SOFC.operatingpressure = 2000000  # Assume no pressure losses
   SOFC.geometricarea = 20 #m^2
   SOFC.activeinterfaceratio = 500  # Relation between active area and interface area, obtain from manufacturer data, CHECK
   SOFC.interfacearea = SOFC.activeinterfaceratio * SOFC.geometricarea

   # Geometric design variables
   SOFC.channelwidth_total = 1000
   SOFC.anodethickness = 0.0009
   SOFC.cathodethickness = 0.00006
   SOFC.electrolytethickness = 0.000015
   SOFC.interconnectthickness = 0.01
   SOFC.additionalthickness = 0.01
   SOFC.channelheight = 0.001
   SOFC.channellength = 10
   SOFC.interconnectcontactwidth = 0.05
   SOFC.channelwidth = 0.005
   SOFC.interconnectcontactwidth = 0.00002

   # Parameters
   SOFC.EnthalpyChange = -LHV * M_H2  # J / mol
   SOFC.V_max = -EnthalpyChange / (2 * Faraday)  # V
   SOFC.EntropyChange = -49.6  # H2O - H2 - O2, J / molK
   SOFC.yH2_mean = 0.5
   SOFC.yO2_mean = 0.15
   SOFC.yH2O_mean = 0.5

   # Ohmic losses
   SOFC.sigmacathode = 42000000 * operatingtemperature ** (-1) * np.exp(-1200 / operatingtemperature)
   SOFC.sigmaanode = 95000000 * operatingtemperature ** (-1) * np.exp(-1150 / operatingtemperature)
   SOFC.sigmaelectrolyte = 33400 * np.exp(-10300 / operatingtemperature)
   SOFC.sigmainterconnect = 9300000 * operatingtemperature ** (-1) * np.exp(-1100 / operatingtemperature)

   # Activation losses - - Selimovic model
   SOFC.gammaanode = 550000000  # A / m ** 2
   SOFC.gammacathode = 700000000  # A / m ** 2
   SOFC.i0Anode = 5300
   SOFC.i0Cathode = 2000
   SOFC.Eactanode = 100000  # J / mol
   SOFC.Eactcathode = 117000  # J / mol
   SOFC.Pref = 100000
   SOFC.ne = 1

   # Concentration losses
   SOFC.m = 0.00003
   SOFC.n = 0.008

   # Geometric and sizing parameters
   SOFC.total_thickness = anodethickness + cathodethickness + electrolytethickness + interconnectthickness + 2 * channelheight + additionalthickness
   SOFC.anode_density = 4800
   SOFC.cathode_density = 4600
   SOFC.electrolyte_density = 6000
   SOFC.interconnect_density = 7800
   SOFC.cell_density = (anode_density * anodethickness + cathode_density * cathodethickness + electrolyte_density * electrolytethickness + interconnect_density * anodethickness) / total_thickness
   SOFC.porosity_coefficient = 0.6

   # Power per cell
   SOFC.powerpercell = 2000  # W
   
   return