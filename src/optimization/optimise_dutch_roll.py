"""
Title: Optimization Script for Dutch Roll Method

Description: The values to optimize will be
             - Kz
             - Cnr
             - Cyb

author: Pietro Campolucci
"""

# import dependencies
from src.input.parameters_citation import motions
import src.simulation.response_flightest as data
import src.input.parameters_citation as par
import numpy as np
import control as c
from scipy.optimize import minimize


def optimise_dutch_roll():

    def dutch_roll_error(params):

        # define derivatives for dutch roll
        KZ2, Cnr, CYb = params

        # input parameters
        motion = motions["DR"]
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
                                 -2 * par.mub * KZ2 * (par.b ** 2) / (V0 ** 2)]])

        C2 = np.matrix([[CYb, par.CL, par.CYp * (par.b) / (2 * V0), (par.CYr - 4 * par.mub) * (par.b) / (2 * V0)],
                        [0, 0, par.b / (2 * V0), 0],
                        [par.Clb, 0, par.Clp * (par.b) / (2 * V0), par.Clr * (par.b) / (2 * V0)],
                        [par.Cnb, 0, par.Cnp * (par.b) / (2 * V0), Cnr * (par.b) / (2 * V0)]])

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

        error = sum(abs(ra - ra_g)) + sum(abs(rr - rr_g)) + sum(abs(yr - yr_g))

        return error


    # EXECUTE OPTIMIZATION
    print("=" * 100)
    print("Optimisation for Dutch roll motion")
    print("=" * 100, "\n")

    values = ["KZ2", "Cnr", "CYb"]
    x0 = np.array([par.KZ2, par.Cnr, par.CYb])

    print(f"Current error for Dutch roll is: {dutch_roll_error(x0)}\n")

    res = minimize(dutch_roll_error, x0, method='nelder-mead', options={'xatol': 1e-8, 'disp': True})

    optimised_values = res.x

    print()
    for i in range(len(optimised_values)):
        print(f"{values[i]} gets from {x0[i]} to {optimised_values[i]}")
