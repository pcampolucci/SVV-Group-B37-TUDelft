"""
Title: Optimization Script for all maneuvers

Description: The values to optimize will be
             for aperiodic roll: Clp
             for dutch roll: Cnr, CYb, Cnb
             for aperiodic spiral: Clb, Clr, CYb, Cnp
             for short period: CZa, Cmadot, Cmq, Cma
             for phugoid: CXu, CZu, Cmu, CXa

             all of them: Clp, Cnr, CYb, Cnb, Clb, Clr, CYb, Cnp, CZa, Cmadot, Cmq, CXu, CZu, Cmu, CXa

author: Pietro Campolucci
"""

# import dependencies
from src.input.parameters_citation import motions
import src.simulation.response_flightest as data
import src.input.parameters_citation as par
import numpy as np
import control as c
from scipy.optimize import minimize


def optimise_all():

    x0 = np.array([par.Clp, par.Cnr, par.CYb, par.Cnb, par.Clb, par.Clr, par.CYb, par.Cnp,
                   par.CZa, par.Cmadot, par.Cmq, par.CXu, par.CZu, par.Cmu, par.CXa])

    def get_total_error(params):

        # define derivatives
        Clp, Cnr, CYb, Cnb, Clb, Clr, CYb, Cnp, \
        CZa, Cmadot, Cmq, CXu, CZu, Cmu, CXa = params

        def error_asymmetric(motion):

            # input parameters
            motion = motions[motion]
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
            C2 = np.matrix([[CYb, par.CL, par.CYp * (par.b) / (2 * V0), (par.CYr - 4 * par.mub) * (par.b) / (2 * V0)],
                            [0, 0, par.b/(2*V0), 0],
                            [Clb, 0, Clp * (par.b) / (2 * V0), Clr * (par.b) / (2 * V0)],
                            [Cnb, 0, Cnp * (par.b) / (2 * V0), Cnr * (par.b) / (2 * V0)]])
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
            error_a = sum(abs((ra - ra_g) / (max(ra) - min(ra)))) / len(ra)  # pitch
            error_b = sum(abs((rr - rr_g) / (max(rr) - min(rr)))) / len(rr)  # pitchrate
            error_c = sum(abs((yr - yr_g) / (max(yr) - min(yr)))) / len(yr)  # aoa

            error = (error_a + error_b + error_c) / 3

            return error

        def error_symmetric(motion):

            # input parameters
            TAS = data.TAS
            motion = motions[motion]
            start = motion['time']
            step = motion['step']
            stop = start + step * 10

            # Stationary flight condition
            V0 = data.TAS[start]  # true airspeed in the stationary flight condition [m/sec]

            elev_defs = data.delta_e * np.pi / 180
            elev_defs = elev_defs[start:stop] + 0.006609799562442952  # normalise elevator input

            C1 = np.matrix([[-2 * par.muc * par.c / (V0 ** 2), 0, 0, 0],
                            [0, (par.CZadot - 2 * par.muc) * par.c / V0, 0, 0],
                            [0, 0, -par.c / V0, 0],
                            [0, Cmadot * par.c / V0, 0, -2 * par.muc * par.KY2 * (par.c / V0) ** 2]])
            C2 = np.matrix([[CXu / V0, CXa, par.CZ0, par.CXq * par.c / V0],
                            [CZu / V0, CZa, -par.CX0, (par.CZq + 2 * par.muc) * (par.c / V0)],
                            [0, 0, 0, par.c / V0],
                            [Cmu / V0, par.Cma, 0, Cmq * par.c / V0]])
            C3 = np.matrix([[par.CXde],
                            [par.CZde],
                            [0],
                            [par.Cmde]])

            A = - np.matmul(np.linalg.inv(C1), C2)
            B = - np.matmul(np.linalg.inv(C1), C3)

            C = np.matrix([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
            D = np.matrix([[0], [0], [0], [0]])

            # create state space linear system and compute system response
            sys = c.ss(A, B, C, D)

            # generate input values
            t = data.time[start:stop]

            sys_response = c.forced_response(sys, t, elev_defs)

            pitch_angle = data.pitch_angle
            pitchrate = data.pitchrate
            AoAs = data.AoAs

            sys_response[1][0][:] = sys_response[1][0][:] + TAS[start]
            sys_response[1][2][:] = sys_response[1][2][:] * 180 / np.pi + pitch_angle[start]
            sys_response[1][3][:] = sys_response[1][3][:] * 180 / np.pi + pitchrate[start]
            sys_response[1][1][:] = sys_response[1][1][:] * 180 / np.pi + AoAs[start]

            # retrieve error among all measured maneuvers
            tas = TAS[start:stop]
            ra = pitch_angle[start:stop]
            rr = pitchrate[start:stop]
            yr = AoAs[start:stop]

            tas_g = sys_response[1][0]
            ra_g = sys_response[1][1]
            rr_g = sys_response[1][2]
            yr_g = sys_response[1][3]

            # plot error and normalise
            error_a = sum(abs((ra - ra_g) / (max(ra) - min(ra)))) / len(ra)  # pitch
            error_b = sum(abs((rr - rr_g) / (max(rr) - min(rr)))) / len(rr)  # pitchrate
            error_c = sum(abs((yr - yr_g) / (max(yr) - min(yr)))) / len(yr)  # aoa
            error_d = sum(abs((tas - tas_g) / (max(tas) - min(tas)))) / len(tas)  # vtas

            error = (error_a + error_b + error_c + error_d) / 4

            return error

        total_error = 0

        asym = ["DR", "APR", "SPI"]
        sym = ["PGH", "SP"]

        for motion_type in asym:
            asym_case_error = error_asymmetric(motion_type)
            total_error += asym_case_error

        for motion_type in sym:
            sym_case_error = error_symmetric(motion_type)
            total_error += sym_case_error

        return total_error/5

    print(f"Current error for all maneuvers is: {get_total_error(x0)}\n")

    values = ["Clp", "Cnr", "CYb", "Cnb", "Clb", "Clr", "CYb", "Cnp",
              "CZa", "Cmadot", "Cmq", "CXu", "CZu", "Cmu", "CXa"]

    start_error = get_total_error(x0)

    res = minimize(get_total_error, x0, method='nelder-mead',  options={'xatol': 1e-12})

    optimised_values = res.x

    print(f"Ran {res.nit} iterations\n")
    print(f"Error went down from {start_error} to {res.fun}\n")
    for i in range(len(optimised_values)):
        print(f"{values[i]} gets from {x0[i]} to {optimised_values[i]}")
