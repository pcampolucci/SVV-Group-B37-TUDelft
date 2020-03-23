"""
Title: Optimization Script for Phugoid

Description: The values to optimize will be: CXu, CZu, Cmu, CXa

author: Pietro Campolucci
"""

# import dependencies
from src.input.parameters_citation import motions
import src.simulation.response_flightest as data
import src.input.parameters_citation as par
import numpy as np
import control as c
from scipy.optimize import minimize


def optimise_phugoid(debug=False):

    def phugoid_error(params):

        # define derivatives for dutch roll
        CXu, CZu, Cmu, CXa = params

        # input parameters
        TAS = data.TAS
        motion = motions['PGH']
        start = motion['time']
        step = motion['step']
        stop = start + step * 10

        # Stationary flight condition
        V0 = data.TAS[start]  # true airspeed in the stationary flight condition [m/sec]

        elev_defs = data.delta_e * np.pi / 180
        elev_defs = elev_defs[start:stop] - elev_defs[start]  # normalise elevator input

        C1 = np.matrix([[-2 * par.muc * par.c / (V0 ** 2), 0, 0, 0],
                        [0, (par.CZadot - 2 * par.muc) * par.c / V0, 0, 0],
                        [0, 0, -par.c / V0, 0],
                        [0, par.Cmadot * par.c / V0, 0, -2 * par.muc * par.KY2 * (par.c / V0) ** 2]])
        C2 = np.matrix([[CXu / V0, CXa, par.CZ0, par.CXq * par.c / V0],
                        [CZu / V0, par.CZa, -par.CX0, (par.CZq + 2 * par.muc) * (par.c / V0)],
                        [0, 0, 0, par.c / V0],
                        [Cmu / V0, par.Cma, 0, par.Cmq * par.c / V0]])
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
        ra_g = sys_response[1][2]
        rr_g = sys_response[1][3]
        yr_g = sys_response[1][1]

        # plot error and normalise
        # plot error and normalise
        error_a = sum(abs((ra - ra_g)/(max(ra) - min(ra))))/len(ra) # pitch
        error_b = sum(abs((rr - rr_g)/(max(rr) - min(rr))))/len(rr)  # pitchrate
        error_c = sum(abs((yr - yr_g)/(max(yr) - min(yr))))/len(yr)  # aoa
        error_d = sum(abs((tas - tas_g)/(max(tas) - min(tas))))/len(tas)  #vtas

        error = (error_a + error_b + error_c + error_d)/4

        if debug:
            print(f"Single values errors: pitch = {error_a}, pitch rate = {error_b}, AoA = {error_c}, VTAS = {error_d}")

        return error


    # EXECUTE OPTIMIZATION
    print("=" * 100)
    print("Optimisation for Phugoid motion")
    print("=" * 100, "\n")

    values = ["CXu", "CZu", "Cmu", "CXa"]
    x0 = np.array([par.CXu, par.CZu, par.Cmu, par.CXa])

    start_error = phugoid_error(x0)

    res = minimize(phugoid_error, x0, method='nelder-mead',  options={'xatol': 1e-12})

    optimised_values = res.x

    print(f"Ran {res.nit} iterations\n")
    print(f"Error went down from {start_error} to {res.fun}\n")
    for i in range(len(optimised_values)):
        print(f"{values[i]} gets from {x0[i]} to {optimised_values[i]}")
