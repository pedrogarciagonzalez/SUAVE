## @ingroup Components-Energy-Converters
# SOFC.py
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
from SUAVE.Attributes.Propellants import Liquid_H2, Gaseous_H2
from SUAVE.Methods.Power.Fuel_Cell.Discharge import SOFC_Discharge
from SUAVE.Methods.Power.Fuel_Cell.Sizing import sizing_SOFC, plot_sizing_SOFC


# ----------------------------------------------------------------------
#  Fuel_Cell Class
# ----------------------------------------------------------------------
## @ingroup Components-Energy-Converters
class SOFC(Energy_Component): #Here, the energy component is defined, so that the inputs are obtained from the main code
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
        # Inputs and outputs
        self.inputs.stagnation_temperature = 0.
        self.inputs.stagnation_pressure = 0.
        self.inputs.power_required = 0.
        self.inputs.yO2_cathode = 0.
        self.inputs.yN2_cathode = 0.
        self.inputs.yH2_anode = 0.
        self.inputs.yH2O_anode = 0.

        self.outputs.yO2_cathode = 0.
        self.outputs.yN2_cathode = 0.
        self.outputs.yH2_anode = 0.
        self.outputs.yH2O_anode = 0.
        self.outputs.stagnation_temperature = 0.
        self.outputs.stagnation_pressure = 0.
        self.outputs.stagnation_enthalpy = 0.

        # Constants
        self.Faraday = 96485.3329  # C / mol
        self.Rgas = 8.31446261815324  # J / molK
        self.LHV = Gaseous_H2.LHV #J/kg
        self.M_H2 = Gaseous_H2.molecular_mass*10**(-3)  # kg / mol
        self.M_O2 = 0.032  # kg / mol
        self.M_H2O = 0.01801528  # kg / mol
        self.M_N2 = 0.0280134  # kg / mol

        # Performance design variables
        self.fuelutilization = 0.75
        self.operatingtemperature = 1173  # Assume constant operating temperature
        self.operatingpressure = 2000000  # Assume no pressure losses
        self.geometricarea = 20  # m^2
        self.activeinterfaceratio = 500  # Relation between active area and interface area, obtain from manufacturer data, CHECK
        self.active_area = SOFC.activeinterfaceratio * SOFC.geometricarea

        # Geometric design variables
        self.channelwidth_total = 1000
        self.anodethickness = 0.0009
        self.cathodethickness = 0.00006
        self.electrolytethickness = 0.000015
        self.interconnectthickness = 0.01
        self.additionalthickness = 0.01
        self.channelheight = 0.001
        self.channellength = 10
        self.interconnectcontactwidth = 0.05
        self.channelwidth = 0.005
        self.interconnectcontactwidth = 0.00002

        # Parameters
        self.EnthalpyChange = -SOFC.LHV * M_H2  # J / mol
        self.V_max = -EnthalpyChange / (2 * Faraday)  # V
        self.EntropyChange = -49.6  # H2O - H2 - O2, J / molK
        self.yH2_mean = 0.5
        self.yO2_mean = 0.15
        self.yH2O_mean = 0.5

        # Ohmic losses
        self.sigmacathode = 42000000 * operatingtemperature ** (-1) * np.exp(-1200 / operatingtemperature)
        self.sigmaanode = 95000000 * operatingtemperature ** (-1) * np.exp(-1150 / operatingtemperature)
        self.sigmaelectrolyte = 33400 * np.exp(-10300 / operatingtemperature)
        self.sigmainterconnect = 9300000 * operatingtemperature ** (-1) * np.exp(-1100 / operatingtemperature)

        # Activation losses - - Selimovic model
        self.gammaanode = 550000000  # A / m ** 2
        self.gammacathode = 700000000  # A / m ** 2
        self.i0Anode = 5300
        self.i0Cathode = 2000
        self.Eactanode = 100000  # J / mol
        self.Eactcathode = 117000  # J / mol
        self.Pref = 100000
        self.ne = 1

        # Concentration losses
        self.m = 0.00003
        self.n = 0.008

        # Geometric and sizing parameters
        self.total_thickness = anodethickness + cathodethickness + electrolytethickness + interconnectthickness + 2 * channelheight + additionalthickness
        self.anode_density = 4800
        self.cathode_density = 4600
        self.electrolyte_density = 6000
        self.interconnect_density = 7800
        self.cell_density = (anode_density * anodethickness + cathode_density * cathodethickness + electrolyte_density * electrolytethickness + interconnect_density * anodethickness) / total_thickness
        self.porosity_coefficient = 0.6

        # Power per cell
        self.powerpercell = 2000  # W

        # Discharge model
        self.discharge_model=SOFC_Discharge

    def compute(self,conditions):
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
        self.discharge_model(self, conditions)
        """           
        [v, current_density, power, efficiency, mdot_fuel_total, mdot_fuel_consumed, mdot_fuel_not_consumed, mdot_air_total] = self.discharge_model(self, conditions)
        self.outputs.operating_voltage = v
        self.outputs.operating_current_density = current_density
        self.outputs.power = power
        self.outputs.efficiency = efficiency
        self.outputs.mdot_fuel_total = mdot_fuel_total
        self.outputs.mdot_fuel_consumed = mdot_fuel_consumed
        self.outputs.mdot_fuel_not_consumed = mdot_fuel_not_consumed
        self.outputs.mdot_air_total = mdot_air_total
        self.outputs.stagnation_temperature =
        self.outputs.stagnation_pressure =

    def sizing(self,conditions,numerics):
        """This calls the sizing method for SOFC.

                Assumptions:
                None

                Source:
                N/A

                Inputs:
                see properties used

                Outputs:
                SOFC_mass  [kg]
                SOFC_number_cells [-]
                SOFC_volume     [m^3]

                Properties Used:
                self.discharge_model(self, conditions, numerics)
                """
        [SOFC_mass, SOFC_volume, SOFC_number_cells] = sizing_SOFC(self,conditions,numerics,power)
        return [SOFC_mass, SOFC_number_cells, SOFC_volume, SOFC.number_channels_per_cell]

    def geometry_plot(self,conditions,numerics):
        """This calls the geometry plotting method for SOFC.

                        Assumptions:
                        None

                        Source:
                        N/A

                        Inputs:
                        see properties used

                        Outputs:
                        Plot of SOFC geometry.

                        Properties Used:
                        SOFC geometric characteristics
                        """
        plot_sizing_SOFC(SOFC,conditions,numerics)

    __call__ = compute