"""
Title: Main Verification Launcher

Author: Pietro Campolucci
"""

# import dependencies
from src.verification.verification_coefficients import plot_xflr_simulation
from src.helpers.path import path


def run_verification(show_plot=True):

    xflr_path = path + "/src/verification/xflr_verification_data.txt"

    plot_xflr_simulation(xflr_path, path, show_plot=show_plot)

    print(f"Saving plots to {path}/src/verification/verification_plots")
