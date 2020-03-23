"""
Title: Main Simulation Launcher

Author: Pietro Campolucci
"""

# import executables
from src.parameters_calculation.run_parameters_calculation import run_parameters_calculation
from src.simulation.run_simulation import run_simulation
from src.verification.run_verification import run_verification
from src.optimization.run_optimisation import run_optimisation

# TWEAK THESE VALUES TO CHOOSE THE OUTPUT
width = 13  # plots width
height = 13  # plots height
yes_verbose = False
yes_plot = False
yes_parameters = False
yes_simulation = True
yes_verification = False
yes_optimisation = False
yes_full_optimisation = False  # don't run this one

if yes_parameters:
    print("=" * 100)
    print("Starting Parameters Retrieval")
    print("=" * 100, "\n")
    run_parameters_calculation(show_plot=yes_plot)

if yes_simulation:
    print("=" * 100)
    print("Starting Asymmetric and Symmetric Motion Simulator")
    print("=" * 100, "\n")
    run_simulation(width, height)

if yes_verification:
    print("=" * 100)
    print("Starting Verification of Static Parameters")
    print("=" * 100)
    run_verification(show_plot=yes_plot)

if yes_optimisation:
    print("=" * 100)
    print("Starting Optimisation Session")
    print("=" * 100, "\n")
    run_optimisation(debug=yes_verbose, full=yes_full_optimisation)
