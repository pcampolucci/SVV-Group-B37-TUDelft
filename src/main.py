"""
Title: Main Simulation Launcher

Author: Pietro Campolucci
"""

# import executables
from src.simulation.run_simulation import run_simulation
from src.verification.run_verification import run_verification

yes_simulation = True
yes_verification = True

if yes_simulation:
    print("=" * 100)
    print("Starting Asymmetric and Symmetric Motion Simulator")
    print("=" * 100, "\n")
    run_simulation()

if yes_verification:
    print("=" * 100)
    print("Starting Verification of Static Parameters")
    print("=" * 100)
    run_verification()


