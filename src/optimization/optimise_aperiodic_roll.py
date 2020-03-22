"""
Title: Optimization Script for Aperiodic Roll

Description: The values to optimize will be
             - Clp

author: Pietro Campolucci
"""

# import dependencies
from src.input.parameters_citation import motions
import src.simulation.response_flightest as data
import src.input.parameters_citation as par
import numpy as np
import control as c
from scipy.optimize import minimize


def optimise_aperiodic_roll(debug=False):

    def aperiodic_roll_error(params):

        # define derivatives for dutch roll
        Clp, dummy = params

        # input parameters
        motion = motions["APR"]
        start = motion['time']
        step = motion['step']
        stop = start + step * 10

        # Stationary flight condition
        V0 = data.TAS[start]  # true airspeed in the stationary flight condition [m/sec]

        delta_a = data.delta_a * np.pi / 180 - 0.005479673656854227  # normalise aileron input
        delta_r = data.delta_r * np.pi / 180 + 0.006386078365702277  # normalise rudder input
        inputs = np.vstack([delta_a, delta_r])
        inputs = inputs[:, start:stop]

        # compute state spaces with 3 tunable derivatives
        C1 = np.matrix([[(par.CYbdot - 2 * par.mub) * par.b / V0, 0, 0, 0],
                        [0, -par.b / (2 * V0), 0, 0],
                        [0, 0, -2 * par.mub * par.KX2 * (par.b ** 2) / (V0 ** 2),
                         2 * par.mub * par.KXZ * (par.b ** 2) / (V0 ** 2)],
                        [par.Cnbdot * (par.b) / (V0), 0, 2 * par.mub * par.KXZ * (par.b ** 2) / (V0 ** 2),
                         -2 * par.mub * par.KZ2 * (par.b ** 2) / (V0 ** 2)]])

        C2 = np.matrix([[par.CYb, par.CL, par.CYp * (par.b) / (2 * V0), (par.CYr - 4 * par.mub) * (par.b) / (2 * V0)],
                        [0, 0, par.b / (2 * V0), 0],
                        [par.Clb, 0, Clp * (par.b) / (2 * V0), par.Clr * (par.b) / (2 * V0)],
                        [par.Cnb, 0, par.Cnp * (par.b) / (2 * V0), par.Cnr * (par.b) / (2 * V0)]])

        C3 = -np.matrix([[par.CYda, par.CYdr],
                         [0, 0],
                         [par.Clda, par.Cldr],
                         [par.Cnda, par.Cndr]])

        # get state space matrices
        A = - np.matmul(np.linalg.inv(C1), C2)

        B = - np.matmul(np.linalg.inv(C1), C3)

        C = np.matrix([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])

        D = np.matrix([[0, 0], [0, 0], [0, 0], [0, 0]])

        # create state space linear system and compute system response
        sys = c.ss(A, B, C, D)

        # generate input values
        t = data.time[start:stop]
        sys_response = c.forced_response(sys, t, inputs)

        # get comparison values from flight test
        roll_angle = data.roll_angle
        roll_rate = data.rollrate
        yaw_rate = data.yawrate

        # extract simulated response
        sys_response[1][1][:] = sys_response[1][1][:] * 180 / np.pi + roll_angle[start]
        sys_response[1][2][:] = sys_response[1][2][:] * 180 / np.pi + roll_rate[start]
        sys_response[1][3][:] = sys_response[1][3][:] * 180 / np.pi + yaw_rate[start]

        # retrieve error among all measured maneuvers
        ra = roll_angle[start:stop]
        rr = roll_rate[start:stop]
        yr = yaw_rate[start:stop]

        ra_g = sys_response[1][1]
        rr_g = sys_response[1][2]
        yr_g = sys_response[1][3]

        # plot error and normalise
        error_a = sum(abs((ra - ra_g)/(max(ra) - min(ra))))/len(ra) # pitch
        error_b = sum(abs((rr - rr_g)/(max(rr) - min(rr))))/len(rr)  # pitchrate
        error_c = sum(abs((yr - yr_g)/(max(yr) - min(yr))))/len(yr)  # aoa

        error = (error_a + error_b + error_c) / 3

        if debug:
            print(f"Single values errors: roll angle = {error_a}, roll rate = {error_b}, yaw rate = {error_c}")

        return error


    # EXECUTE OPTIMIZATION
    print("=" * 100)
    print("Optimisation for Aperiodic roll motion")
    print("=" * 100, "\n")

    dummy = 0

    values = ["Clp", "dummy"]
    x0 = np.array([par.Clp, dummy])
    start_error = aperiodic_roll_error(x0)

    res = minimize(aperiodic_roll_error, x0, method='nelder-mead', options={'xatol': 1e-12})

    optimised_values = res.x

    print(f"Ran {res.nit} iterations\n")
    print(f"Error went down from {start_error} to {res.fun}\n")
    for i in range(len(optimised_values)):
        print(f"{values[i]} gets from {x0[i]} to {optimised_values[i]}")
