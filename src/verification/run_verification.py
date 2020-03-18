"""
Title: Main Verification Launcher

Author: Pietro Campolucci
"""

# import dependencies
from src.verification.verification_coefficients import plot_xflr_simulation
from src.helpers.path import path


def run_verification():

    xflr_path = path + "/src/verification/xflr_verification_data.txt"

    plot_xflr_simulation(xflr_path, path)
