"""
Title: Main Simulation Launcher

Author: Pietro Campolucci
"""

# import executables
from src.simulation.run_simulation import run_simulation

yes_simulation = True
yes_verification = False

if yes_simulation:
    run_simulation()
