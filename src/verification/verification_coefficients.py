"""
Title: Verification tool for flight performance coefficients

Author: Pietro Campolucci
"""

# importing packages
from src.helpers.plot import plot
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
    correction = math.sqrt(1 - mach**2)
    CL_lst = np.array(CL_lst)/correction
    Cm_lst = np.array(Cm_lst)/correction

    return alpha_lst, CL_lst, CD_lst, Cm_lst, names


def plot_simulation(filename, mach):

    alpha_lst, CL_lst, CD_lst, Cm_lst, names = open_simulation(filename, mach)

    # plot CL-a
    plot(alpha_lst, CL_lst, "CL alpha curve", "CL_a")

    # plot CL-CD
    plot(CD_lst, CL_lst, "CL CD curve", "CL_CD")

    # plot Cm-a
    plot(alpha_lst, Cm_lst, "Cm alpha curve", "Cm_a")

    # get slopes and regression
    cla = sm.OLS(CL_lst, alpha_lst).fit().params
    cma = sm.OLS(Cm_lst, alpha_lst).fit().params

    print("\nSLOPES FROM SIMULATION \n")
    print(f"CL_alpha slope: {cla}\n")
    print(f"Cm_alpha slope: {cma}\n")

    return 0


# debugging
DEBUG = True

if DEBUG:
    plot_simulation("verification_xflr.txt", 0.8)