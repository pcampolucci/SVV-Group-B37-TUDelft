"""
Title: Main Optimisation Launcher

Author: Pietro Campolucci
"""

# import dependencies
from src.optimization.optimise_dutch_roll import optimise_dutch_roll


def run_optimisation():

    print("If not done already, change the values in parameters_citation.py to the ones obtained below\n")

    optimise_dutch_roll()
