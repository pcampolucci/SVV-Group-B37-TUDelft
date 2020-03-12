"""
Title: Verification script for asymmetrical maneuvers. It will cover:
       - aperiodic roll
       - dutch roll (simplified)
       - dutch roll (oversimlified)
       - spiral motion

Author: Pietro Campolucci
"""

# importing packages
import numpy as np
import math as m
from src.input.parameters_citation import *

# define class and functions


def aperiodic_roll():

    # get eigenvalue from report simplification
    eigenvalue_ap_roll = Clp / (4 * mub * KX2)

    print(f"Eigenvalues for aperiodic roll: {eigenvalue_ap_roll}")

    return eigenvalue_ap_roll


def dutch_roll_1():

    # motion coefficients from characteristic equation
    A = 8 * mub**2 * KZ2
    B = -2 * mub * (Cnr + 2 * KZ2 * CYb)
    C = 4 * mub * Cnb + CYb * Cnr

    eigenvalue_dutch_roll_1 = (-B + m.sqrt(B**2 - A*C))/(2*A*C)
    eigenvalue_dutch_roll_2 = (-B - m.sqrt(B**2 - A*C))/(2*A*C)

    print(f"Eigenvalues for simplified dutch roll: {eigenvalue_dutch_roll_1, eigenvalue_dutch_roll_2}")

    return eigenvalue_dutch_roll_1, eigenvalue_dutch_roll_2


def dutch_roll_2():

    A = -2 * mub * KZ2
    B = 0.5 * Cnr
    C = - Cnb

    eigenvalue_dutch_roll_1 = (-B + m.sqrt(B**2 - A*C))/(2*A*C)
    eigenvalue_dutch_roll_2 = (-B - m.sqrt(B**2 - A*C))/(2*A*C)

    print(f"Eigenvalues for oversimplified dutch roll: {eigenvalue_dutch_roll_1, eigenvalue_dutch_roll_2}")

    return eigenvalue_dutch_roll_1, eigenvalue_dutch_roll_2


def spiral_motion():

    eigenvalue_spiral_motion = (2 * CL * (Clb*Cnr - Cnb*Clr)) / \
                               (Clp * (CYb*Cnr + 4*mub*Cnb) - Cnb * (CYb*Clr + 4*mub*Clb))

    print(f"Eigenvalues for spiral motion: {eigenvalue_spiral_motion}")

    return eigenvalue_spiral_motion


# EXECUTE

aperiodic_roll()
dutch_roll_1()
dutch_roll_2()
spiral_motion()


