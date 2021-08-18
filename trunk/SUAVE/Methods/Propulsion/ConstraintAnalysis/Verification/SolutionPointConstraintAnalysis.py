import SUAVE
import numpy as np
import matplotlib as plt
from SUAVE.Core import Data
from SUAVE.Methods.Propulsion.ConstraintAnalysis.Verification.Parameters import *
from SUAVE.Methods.Propulsion.ConstraintAnalysis.Verification.ConstraintAnalysisEquations import *
from SUAVE.Methods.Propulsion.ConstraintAnalysis.Verification.PlotConstraintAnalysis import *
from SUAVE.Methods.Propulsion.ConstraintAnalysis.Verification.intersect import intersection

def select_design_point_constraint_analysis():
    plot_constraint_analysis()
    print("Select a design point (recommended: minimum T/W or minimum W/S)")

#def optimize_design_point_constraint_analysis_minTW():