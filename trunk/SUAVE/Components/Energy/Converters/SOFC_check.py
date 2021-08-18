## @ingroup Components-Energy-Converters
# SOFC_check.py
#
# Created:  February 2021 Pedro Garcia Gonzalez (TU Delft)

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# suave imports
import SUAVE
import numpy as np

# package imports
from SUAVE.Core import Units
from SUAVE.Components.Energy.Energy_Component import Energy_Component
from SUAVE.Attributes.Gases import Air
from SUAVE.Attributes.Propellants import Liquid_H2
import SUAVE.Methods.Power.Fuel_Cell.Discharge


# ----------------------------------------------------------------------
#  Fuel_Cell Class
# ----------------------------------------------------------------------
## @ingroup Components-Energy-Converters
class SOFC(Energy_Component):
    """This is a fuel cell component.
    
    Assumptions:
    None

    Source:
    None
    """    
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
        None

        Source:
        Some default values come from a Nissan 2011 fuel cell

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """
        #Calibrating values for power calculations

        #CONSTANT VALUES
        Faraday = 96485.3329
        Rgas = 8.31446261815324

        #FUEL AND OXIDIZER
        self.propellant     = Liquid_H2()
        self.oxidizer       = Air()
        self.fuel_utilization = 0.85 #CHECK VALUES, MAYBE DEFINE AS DESIGN VARIABLE

        # USE CHEMICAL BALANCE FOR REACTIONS AND OBTAIN VALUE OF CONCENTRATION
        # CHECK POSSIBLE ASSUMPTIONS
        # CHECK PARAMETERS FROM MANUFACTURERS

        #PARAMETERS FOR OCV CALCULATIONS
        self.EnthalpyChange = -241830  # For Gibbs energy calculation, J/mol
        self.EntropyChange = -49.6  # H2O - H2 - O2, J/molK
        self.yH2 = 1  # Molar concentration of hydrogen in inlet fuel (pure H2)
        self.yO2 = 0.21  # Molar concentration of oxygen in inlet oxidant (air)
        self.yH2O = 0.05  # Molar concentration of water vapor in inlet flows (assumption)
        self.operatingtemperature = 1173 * Units.K
        self.operatingpressure = 2000000 * Units.Pa  # THE PRESSURE HAS TO BE GIVEN IN BAR FOR NERNST EQUATION TO APPLY

        #OHMIC LOSSES
        self.anodethickness=9E-4*Units.m #Based on typical values
        self.cathodethickness=6E-5*Units.m #Based on typical values
        self.electrolytethickness=1.5E-5*Units.m #Based on typical values
        self.interconnectthickness=1.5E-5*Units.m #CHECK FOR VALUES


        #ACTIVATION LOSSES
        self.A1 = .03  # slope of the Tafel line (models activation losses) (V), CHECK VALUE FOR SOFC

        #CONCENTRATION LOSSES
        self.m = 0.00003  # constant in mass-transfer overvoltage equation (V), CHECK VALUE FOR SOFC
        self.n = 8E-3  # constant in mass-transfer overvoltage equation, CHECK VALUE FOR SOFC

        #IDEAL VOLTAGE FOR EFFICIENCY COMPUTATIONS
        self.ideal_voltage = 1.25 #LHV-based at standard pressure and temperature

        # GEOMETRIC AND SIZING PARAMETERS
        self.number_of_cells = 0.0  # number of fuel cells in the stack
        self.interface_area = 875.0 * (Units.cm ** 2.)  # area of the fuel cell interface
        self.additionalthickness = 0.0 #Consider additional thickness apart from MEA
        self.total_thickness = self.anodethickness +  self.cathodethickness + self.electrolytethickness + self.interconnectthickness + self.additionalthickness # thickness of cell wall in meters
        self.anode_density = 4800 #Ni-YSZ
        self.cathode_density = 4600 #LSM
        self.electrolyte_density = 6000 #YSZ
        self.interconnect_density = 7800 #Iron-based
        self.cell_density = (self.anode_density*self.anodethickness + self.cathode_density*self.cathodethickness + self.electrolyte_density*self.electrolytethickness + self.interconnect_density*self.anodethickness)/self.total_thickness
        self.porosity_coefficient = 0.6  # CHECK FOR TYPICAL VALUES

        #MODEL SELECTION
        self.discharge_model = SOFC_Discharge
        
    def energy_calc(self,conditions,numerics):
        """This call the assigned discharge method.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        see properties used

        Outputs:
        mdot     [kg/s] (units may change depending on selected model)

        Properties Used:
        self.discharge_model(self, conditions, numerics)
        """
        self.inputs.power_in = 2000*Units.W
        mdot = self.discharge_model(self, conditions, numerics)
        return mdot

    