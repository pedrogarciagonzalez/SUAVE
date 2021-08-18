## @ingroup Methods-Power-Fuel_Cell-Sizing
# sizing_SOFC.py
#
# Created : 04/2021: Pedro Garcia Gonzalez

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import scipy as sp
import numpy as np
import matplotlib as plt
from SUAVE.Core import Units

# ----------------------------------------------------------------------
#  Methodology for sizing of SOFC
# ----------------------------------------------------------------------

## @ingroup Methods-Power-Fuel_Cell-Sizing

def sizing_SOFC(SOFC,conditions,numerics,power):

    SOFC.required_power = power
    SOFC.number_cells=np.round(SOFC.required_power/SOFC.powerpercell)
    SOFC.number_channels_per_cell = np.round(SOFC.channelwidth_total / SOFC.channelwidth)
    SOFC.volume = SOFC.number_cells*SOFC.channel_length*SOFC.channelwidth_total*SOFC.channelheight
    SOFC.mass = SOFC.volume * SOFC.cell_density

    return [SOFC.mass, SOFC.volume, SOFC.number_cells, SOFC.number_channels_per_cell]

def plot_sizing_SOFC(SOFC,conditions,numerics):

    SOFC.electrolytex = np.array([0, SOFC.channelwidth + SOFC.interconnectcontactwidth, SOFC.channelwidth + SOFC.interconnectcontactwidth, 0, 0])
    SOFC.electrolytey = np.array([0, 0, SOFC.electrolytethickness, SOFC.electrolytethickness, 0])
    SOFC.anodex = np.array([0, SOFC.channelwidth + SOFC.interconnectcontactwidth, SOFC.channelwidth + SOFC.interconnectcontactwidth, 0, 0])
    SOFC.anodey = np.array([0, 0, SOFC.anodethickness, SOFC.anodethickness, 0]) + np.array([SOFC.electrolytethickness,SOFC.electrolytethickness,SOFC.electrolytethickness,SOFC.electrolytethickness,SOFC.electrolytethickness])
    SOFC.cathodex = np.array([0, SOFC.channelwidth + SOFC.interconnectcontactwidth, SOFC.channelwidth + SOFC.interconnectcontactwidth, 0, 0])
    SOFC.cathodey = np.array([0, 0, - SOFC.cathodethickness, - SOFC.cathodethickness, 0])
    SOFC.cathodechannelx = np.array([0, SOFC.channelwidth, SOFC.channelwidth, 0, 0]) + np.array([SOFC.interconnectcontactwidth,SOFC.interconnectcontactwidth,SOFC.interconnectcontactwidth,SOFC.interconnectcontactwidth,SOFC.interconnectcontactwidth])
    SOFC.cathodechannely = np.array([0, 0, - SOFC.channelheight, -SOFC.channelheight, 0]) - np.array([SOFC.cathodethickness,SOFC.cathodethickness,SOFC.cathodethickness,SOFC.cathodethickness,SOFC.cathodethickness])
    SOFC.anodechannelx = np.array([0, SOFC.channelwidth, SOFC.channelwidth, 0, 0]) + np.array([SOFC.interconnectcontactwidth,SOFC.interconnectcontactwidth,SOFC.interconnectcontactwidth,SOFC.interconnectcontactwidth,SOFC.interconnectcontactwidth])
    SOFC.anodechannely = np.array([0, 0, SOFC.channelheight, SOFC.channelheight, 0]) + np.array([SOFC.anodethickness + SOFC.electrolytethickness,SOFC.anodethickness + SOFC.electrolytethickness,SOFC.anodethickness + SOFC.electrolytethickness,SOFC.anodethickness + SOFC.electrolytethickness,SOFC.anodethickness + SOFC.electrolytethickness])
    SOFC.interconnectanodex = np.array([0, SOFC.interconnectcontactwidth, SOFC.interconnectcontactwidth, SOFC.interconnectcontactwidth + SOFC.channelwidth, SOFC.interconnectcontactwidth + SOFC.channelwidth, 2 * SOFC.interconnectcontactwidth + SOFC.channelwidth, 2 * SOFC.interconnectcontactwidth + SOFC.channelwidth, 0, 0])
    SOFC.interconnectanodey = np.array([0, 0, SOFC.channelheight, SOFC.channelheight, 0, 0, SOFC.channelheight + SOFC.interconnectthickness, SOFC.channelheight + SOFC.interconnectthickness, 0])
    SOFC.interconnectcathodex = np.array([0, SOFC.interconnectcontactwidth, SOFC.interconnectcontactwidth, SOFC.interconnectcontactwidth + SOFC.channelwidth, SOFC.interconnectcontactwidth + SOFC.channelwidth, 2 * SOFC.interconnectcontactwidth + SOFC.channelwidth, 2 * SOFC.interconnectcontactwidth + SOFC.channelwidth, 0, 0])
    SOFC.interconnectcathodey = np.array([0, 0, - SOFC.channelheight, - SOFC.channelheight, 0, 0, - SOFC.channelheight -SOFC.interconnectthickness, - SOFC.channelheight - SOFC.interconnectthickness, 0])

    index_vector=list(range(0,int(numbercells)-1,1))
    index2_vector=list(range(0,int(numberchannels)-1,1))

    for index2 in index2_vector:
        for index in index_vector:
            plt.pyplot.plot(SOFC.electrolytex + index2 * (2 * SOFC.interconnectcontactwidth + SOFC.channelwidth)*np.ones_like(SOFC.electrolytex), SOFC.electrolytey + 2 * index * (SOFC.anodethickness + SOFC.electrolytethickness + SOFC.channelheight + SOFC.interconnectthickness)*np.ones_like(SOFC.electrolytey), label="Electrolyte")
            plt.pyplot.plot(SOFC.anodex + index2 * (2 * SOFC.interconnectcontactwidth + SOFC.channelwidth)*np.ones_like(SOFC.anodex), SOFC.anodey + 2 * index * (SOFC.anodethickness + SOFC.electrolytethickness + SOFC.channelheight + SOFC.interconnectthickness)*np.ones_like(SOFC.anodey), label="Anode")
            plt.pyplot.plot(SOFC.cathodex + index2 * (2 * SOFC.interconnectcontactwidth + SOFC.channelwidth)*np.ones_like(SOFC.cathodex), SOFC.cathodey + 2 * index * (SOFC.anodethickness + SOFC.electrolytethickness + SOFC.channelheight + SOFC.interconnectthickness)*np.ones_like(SOFC.cathodey), label="Cathode")
            plt.pyplot.plot(SOFC.anodechannelx + index2 * (2 * SOFC.interconnectcontactwidth + SOFC.channelwidth)*np.ones_like(SOFC.anodechannelx), SOFC.anodechannely + 2 * index * (SOFC.anodethickness + SOFC.electrolytethickness + SOFC.channelheight + SOFC.interconnectthickness)*np.ones_like(SOFC.anodechannely), label="Anode channel")
            plt.pyplot.plot(SOFC.cathodechannelx + index2 * (2 * SOFC.interconnectcontactwidth + SOFC.channelwidth)*np.ones_like(SOFC.cathodechannelx),SOFC.cathodechannely + 2 * index * (SOFC.anodethickness + SOFC.electrolytethickness + SOFC.channelheight + SOFC.interconnectthickness)*np.ones_like(SOFC.cathodechannely), label="Cathode channel")
            plt.pyplot.plot(SOFC.interconnectanodex + index2 * (2 * SOFC.interconnectcontactwidth + SOFC.channelwidth)*np.ones_like(SOFC.interconnectanodex), SOFC.interconnectanodey + 2 * index * (SOFC.anodethickness + SOFC.electrolytethickness + SOFC.channelheight + SOFC.interconnectthickness)*np.ones_like(SOFC.interconnectanodey), label="Anode interconnect")
            plt.pyplot.plot(SOFC.interconnectcathodex + index2 * (2 * SOFC.interconnectcontactwidth + SOFC.channelwidth)*np.ones_like(SOFC.interconnectcathodex), SOFC.interconnectcathodey + 2 * index * (SOFC.anodethickness + SOFC.electrolytethickness + SOFC.channelheight + SOFC.interconnectthickness)*np.ones_like(SOFC.interconnectcathodey), label="Cathode interconnect")
            plt.pyplot.xlabel('Width (m)')
            plt.pyplot.ylabel('Thickness (m)')
            plt.pyplot.title('SOFC sizing')
            plt.pyplot.legend()
            plt.pyplot.show()