"""
Title: Verification tool for flight performance coefficients

Author: Pietro Campolucci
"""

# importing packages
from src.helpers.plot import plot
from src.parameters_calculation.clcd_clalpha_plots import CLa, alpha_, CLs_, CDs_
from src.parameters_calculation.Moment_coefs_calc import Cma, measurement_3
import statsmodels.api as sm
import math
import numpy as np


# open file from XFLR5 simulation
def open_simulation(filename, mach):

    f = open(filename, "r")
    first_line = True

    names = ['alpha', 'CL', 'CD', 'Cm']
    alpha_lst = []
    CL_lst = []
    CD_lst = []
    Cm_lst = []

    for line in f:
        if not first_line:

            line_lst = line.split("  ")

            # get values for alpha, CL, CD, Cm
            indexes = [0, 2, 5, 8]

            line_pos = 0
            for item in line_lst:
                if item != '' and not first_line:
                    if line_pos == indexes[0]:
                        alpha_lst.append(float(item))
                    if line_pos == indexes[1]:
                        CL_lst.append(float(item))
                    if line_pos == indexes[2]:
                        CD_lst.append(float(item))
                    if line_pos == indexes[3]:
                        Cm_lst.append(float(item))

                    line_pos += 1

        first_line = False

    # add Prandtl-Glauert correction
    correction = 1  # math.sqrt(1 - mach**2)
    CL_lst = np.array(CL_lst)/correction
    Cm_lst = np.array(Cm_lst)/correction

    return alpha_lst, CL_lst, CD_lst, Cm_lst, names


def plot_simulation(filename, mach):

    alpha_lst, CL_lst, CD_lst, Cm_lst, names = open_simulation(filename, mach)

    # plot CL-a
    plot([alpha_lst, alpha_], [CL_lst, CLs_], ["XFLR5", "Numerical Model"],
         "CL - a", ["alpha [deg]", "CL"], "verification/CL - a", multi=True)

    # plot CL-CD
    plot([np.array(CD_lst), CDs_], [CL_lst, CLs_], ["XFLR5", "Numerical Model"],
         "CL - CD", ["CD", "CL"], "verification/CL - CD", multi=True)

    # plot Cm-a
    plot([alpha_lst, measurement_3.alphas], [Cm_lst, measurement_3.des], ["XFLR5", "Numerical Model"],
         "Cm - a", ["alpha [deg]", "Cm"],  "verification/Cm - a", multi=True)

    # get slopes and regression
    cla = sm.OLS(CL_lst, alpha_lst).fit().params
    cma = sm.OLS(Cm_lst, alpha_lst).fit().params

    print("\nSLOPES FROM SIMULATION \n")
    print(f"CL_alpha slope, XFLR5 vs numerical model: {cla} => {CLa}\n")
    print(f"Cm_alpha slope, XFLR5 vs numerical model: {cma} => {Cma}\n")

    return 0


# debugging
plot_simulation("verification/verification_xflr.txt", 1)