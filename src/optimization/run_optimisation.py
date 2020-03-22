"""
Title: Main Optimisation Launcher

Author: Pietro Campolucci
"""

# import dependencies
from src.optimization.optimise_dutch_roll import optimise_dutch_roll
from src.optimization.optimise_short_period import optimise_short_period
from src.optimization.optimise_phugoid import optimise_phugoid
from src.optimization.optimise_aperiodic_roll import optimise_aperiodic_roll
from src.optimization.optimise_all import optimise_all


def run_optimisation(debug=False, full=False):

    print("If not done already, change the values in parameters_citation.py to the ones obtained below\n")

    if full:
        optimise_all()

    else:
        optimise_dutch_roll(debug=debug)
        optimise_short_period(debug=debug)
        optimise_phugoid(debug=debug)
        optimise_aperiodic_roll(debug=debug)


# NOTE: Full takes some time
run_optimisation()
