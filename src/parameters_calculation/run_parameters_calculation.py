"""
Title: Main Parameters Calculations Launcher

Author: Pietro Campolucci
"""

# importing dependencies
from src.parameters_calculation.get_mass_and_balance import time, x_cgs, mass, path
from src.parameters_calculation.get_coefs_mom import measurement_3, Cma, Cmd
from src.parameters_calculation.get_polars import CLa, CL0, CD0, e, plot_polars
from src.parameters_calculation.get_trim_control_curves import plot_trim_control_curves
from src.helpers.plot import plot


def run_parameters_calculation(show_plot=True):

    # get mass and balance information
    plot(time, x_cgs, 'c.g. change', "Change in c.g. position during flight", ['time [s]', 'c.g. location [m]'],
         path + '/src/parameters_calculation/plots/cg_time', show=show_plot)

    print(f"Total aircraft mass: {round(mass, 3)} kg")

    # get coefficients concerning momentum
    plot(measurement_3.alphas, measurement_3.des, r'd$\alpha$', r'd$\alpha$', ['Alpha [deg]', r'd$\delta_e$'],
         path + '/src/parameters_calculation/plots/deflection', show=show_plot, scatter=True, coordinate=True)

    print("Cma is:", round(Cma, 3))
    print("Cmd is:", round(Cmd, 3))

    # get polars information
    print('CLa: ', round(CLa, 3), 'CL0: ', round(CL0, 3))
    print('CD0: ', round(CD0, 3), 'Oswald: ', round(e, 3))
    plot_polars(path + '/src/parameters_calculation/plots/polar', show=show_plot)

    # get trim control curves
    plot_trim_control_curves(path + '/src/parameters_calculation/plots/control', show=show_plot)

    print(f"\nPlots written to {path}/src/parameters_calculation/plots")

