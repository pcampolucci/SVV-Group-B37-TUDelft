"""
Title: Numerical Model for symmetric and asymmetric response

Author: Marco Desiderio, Eneko Rodriguez
Review: Pietro Campolucci
"""

# import packages
import numpy as np
import matplotlib.pyplot as plt
import control as c
from src.helpers.path import path

# import dependencies
import src.simulation.response_flightest as data
import src.input.parameters_citation as par

# debugging options
DEBUG = False


class Simulate:
    """ class for simulation of symmetric and asymmetric periods """

    def __init__(self, motion, width, height):
        self.start = motion['time']
        self.step = motion['step']
        self.case = motion['type']
        self.title = motion['name']
        self.w = width
        self.h = height

    def motion_report(self, show=True):

        # input parameters
        case = self.case
        start = self.start
        step = self.step
        stop = start + step * 10
        TAS = data.TAS

        # Stationary flight condition
        V0 = data.TAS[start]  # true airspeed in the stationary flight condition [m/sec]

        # Aircraft mass
        cabin = 102 + 90 + 78 + 74 + 79 + 82 + 80 + 87 + 68
        fuel0 = 4100 * 0.453592
        fuel_b = np.cumsum(0.1 * np.ones(data.FMF.shape[0]) * data.FMF)
        fuel = fuel0 - fuel_b
        m = 4157.174 + cabin + fuel  # mass [kg] 4157.174
        m = m[start]

        # build model
        if case == 'SYM':
            elev_defs = data.delta_e*np.pi/180
            elev_defs = elev_defs[start:stop] - elev_defs[start]  #+ 0.006609799562442952  # normalise elevator input

        elif case == 'ASYM':
            delta_a = data.delta_a * np.pi / 180 - data.delta_a[start]*np.pi/180 - 0.015*np.pi/180 # normalise aileron input
            delta_r = data.delta_r*np.pi/180 + 0.006386078365702277  # normalise rudder input
            inputs = np.vstack([delta_a, delta_r])
            inputs = inputs[:, start:stop]

        else:
            print('Case must be either symmetric or asymmetric')

        if case == 'SYM':
            C1 = np.matrix([[-2*par.muc*par.c/(V0**2), 0, 0, 0],
                            [0, (par.CZadot - 2*par.muc)*par.c/V0, 0, 0],
                            [0,0, -par.c/V0, 0],
                            [0, par.Cmadot*par.c/V0, 0, -2*par.muc*par.KY2*(par.c/V0)**2]])
            C2 = np.matrix([[par.CXu/V0, par.CXa, par.CZ0, par.CXq*par.c/V0],
                              [par.CZu/V0, par.CZa, -par.CX0, (par.CZq + 2*par.muc)*(par.c/V0)],
                              [0, 0, 0, par.c/V0],
                              [par.Cmu/V0, par.Cma, 0, par.Cmq*par.c/V0]])
            C3 =  np.matrix([[par.CXde],
                              [par.CZde],
                              [0],
                              [par.Cmde]])

        elif case == 'ASYM':
            C1 = np.matrix([[(par.CYbdot - 2 * par.mub) * par.b / V0, 0, 0, 0],
                            [0, -par.b / (2 * V0), 0, 0],
                            [0, 0, -2 * par.mub * par.KX2 * (par.b ** 2) / (V0 ** 2),
                             2 * par.mub * par.KXZ * (par.b ** 2) / (V0 ** 2)],
                            [par.Cnbdot * (par.b) / (V0), 0, 2 * par.mub * par.KXZ * (par.b ** 2) / (V0 ** 2),
                             -2 * par.mub * par.KZ2 * (par.b ** 2) / (V0 ** 2)]])
            C2 = np.matrix([[par.CYb, par.CL, par.CYp * (par.b) / (2 * V0), (par.CYr - 4 * par.mub) * (par.b) / (2 * V0)],
                            [0, 0, par.b/(2*V0), 0],
                            [par.Clb, 0, par.Clp * (par.b) / (2 * V0), par.Clr * (par.b) / (2 * V0)],
                            [par.Cnb, 0, par.Cnp * (par.b) / (2 * V0), par.Cnr * (par.b) / (2 * V0)]])
            C3 = -np.matrix([[par.CYda, par.CYdr],
                            [0, 0],
                            [par.Clda, par.Cldr],
                            [par.Cnda, par.Cndr]])

        else:
            print('Case must be either symmetric or asymmetric')

        A = - np.matmul(np.linalg.inv(C1), C2)
        B = - np.matmul(np.linalg.inv(C1), C3)

        # get eigenvalues of state space
        eigenvalues = np.linalg.eigvals(A)

        if show:

            # specify requested output
            if case == 'SYM':
                C = np.matrix([[1, 0, 0, 0],
                               [0, 1, 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])
                D = np.matrix([[0], [0], [0], [0]])

            elif case == 'ASYM':
                C = np.matrix([[1, 0, 0, 0],
                               [0, 1, 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])
                D = np.matrix([[0, 0], [0, 0], [0, 0], [0, 0]])

            else:
                print('Case must be either symmetric or asymmetric')


            # create state space linear system and compute system response
            sys = c.ss(A, B, C, D)

            # generate input values
            t = data.time[start:stop]

            if case == 'SYM':
                sys_response = c.forced_response(sys, t, elev_defs)

            elif case == 'ASYM':
                sys_response = c.forced_response(sys, t, inputs)

            # get comparison values from flight test
            pitch_angle = data.pitch_angle
            pitchrate = data.pitchrate
            AoAs = data.AoAs
            roll_angle = data.roll_angle
            roll_rate = data.rollrate
            yaw_rate = data.yawrate

            if case == 'SYM':
                sys_response[1][0][:] = sys_response[1][0][:] + TAS[start]
                sys_response[1][2][:] = sys_response[1][2][:]*180/np.pi + pitch_angle[start]
                sys_response[1][3][:] = sys_response[1][3][:]*180/np.pi + pitchrate[start]
                sys_response[1][1][:] = sys_response[1][1][:]*180/np.pi + AoAs[start]

            elif case == 'ASYM':
                sys_response[1][1][:] = sys_response[1][1][:]*180/np.pi + roll_angle[start]
                sys_response[1][2][:] = sys_response[1][2][:]*180/np.pi + roll_rate[start]
                sys_response[1][3][:] = sys_response[1][3][:]*180/np.pi + yaw_rate[start]

            t = t-start/10 - 9

            tableau20 = [(255, 87, 87), (237, 198, 0), (87, 255, 249), (0, 0, 0),
                         (255, 33, 33), (255, 192, 33), (0, 148, 247), (64, 255, 175),
                         (225, 107, 255), (197, 176, 213), (140, 86, 75), (196, 156, 148),
                         (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
                         (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

            for i in range(len(tableau20)):
                r, g, b = tableau20[i]
                tableau20[i] = (r / 255., g / 255., b / 255.)

            plt.figure(figsize=[self.w, self.h])

            # do the plotting for symmetric
            if case == 'SYM':
                ax1 = plt.subplot(511)
                ax1.spines["top"].set_visible(False)
                ax1.spines["right"].set_visible(False)
                ax1.get_xaxis().tick_bottom()
                ax1.get_yaxis().tick_left()
                ax2 = plt.subplot(512)
                ax2.spines["top"].set_visible(False)
                ax2.spines["right"].set_visible(False)
                ax2.get_xaxis().tick_bottom()
                ax2.get_yaxis().tick_left()
                ax3 = plt.subplot(513)
                ax3.spines["top"].set_visible(False)
                ax3.spines["right"].set_visible(False)
                ax3.get_xaxis().tick_bottom()
                ax3.get_yaxis().tick_left()
                ax4 = plt.subplot(514)
                ax4.spines["top"].set_visible(False)
                ax4.spines["right"].set_visible(False)
                ax4.get_xaxis().tick_bottom()
                ax4.get_yaxis().tick_left()
                ax5 = plt.subplot(515)
                ax5.spines["top"].set_visible(False)
                ax5.spines["right"].set_visible(False)
                ax5.get_xaxis().tick_bottom()
                ax5.get_yaxis().tick_left()


                ax1.plot(t[:], elev_defs[:]*180/np.pi, color = tableau20[1])
                ax1.set(ylabel = r'$\delta_e$ [deg]')
                ax1.set_xlim(xmin=0,xmax=t[-1])

                ax2.plot(t[:], sys_response[1][0], label = 'Simulated response', color = tableau20[4], marker = '1', markevery = 20)
                ax2.plot(t[:], TAS[start:stop], label = 'Measured response', color = tableau20[6], marker = '2', markevery = 20)
                ax2.set(ylabel = r'$V_{TAS}$ [m/s]')
                ax2.set_xlim(xmin=0,xmax=t[-1])
                ax2.legend(loc = 'upper right')

                ax3.plot(t[:], sys_response[1][1], label = 'Simulated response', color = tableau20[4], marker = '1', markevery = 20)
                ax3.plot(t[:], AoAs[start:stop], label = 'Measured response', color = tableau20[6], marker = '2', markevery = 20)
                ax3.set(ylabel = r'$\alpha$ [deg]')
                ax3.set_xlim(xmin=0,xmax=t[-1])

                ax4.plot(t[:], sys_response[1][2], label = 'Simulated response', color = tableau20[4], marker = '1', markevery = 20)
                ax4.plot(t[:], pitch_angle[start:stop], label = 'Measured response', color = tableau20[6], marker = '2', markevery = 20)
                ax4.set(ylabel = r'$\theta$ [deg]')
                ax4.set_xlim(xmin=0,xmax=t[-1])

                ax5.plot(t[:], sys_response[1][3], label = 'Simulated response', color = tableau20[4], marker = '1', markevery = 20)
                ax5.plot(t[:], pitchrate[start:stop], label = 'Measured response', color = tableau20[6], marker = '2', markevery = 20)
                ax5.set(ylabel = r'q [deg/s]')
                ax5.set_xlim(xmin=0,xmax=t[-1])

                # plot grids
                ax1.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)
                ax1.minorticks_on()
                ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.1)
                ax2.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)
                ax2.minorticks_on()
                ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.1)
                ax3.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)
                ax3.minorticks_on()
                ax3.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.1)
                ax4.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)
                ax4.minorticks_on()
                ax4.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.1)
                ax5.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)
                ax5.minorticks_on()
                ax5.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.1)

            elif case == 'ASYM':
                ax1 = plt.subplot(511)
                ax1.spines["top"].set_visible(False)
                ax1.spines["right"].set_visible(False)
                ax1.get_xaxis().tick_bottom()
                ax1.get_yaxis().tick_left()
                ax2 = plt.subplot(512)
                ax2.spines["top"].set_visible(False)
                ax2.spines["right"].set_visible(False)
                ax2.get_xaxis().tick_bottom()
                ax2.get_yaxis().tick_left()
                ax3 = plt.subplot(513)
                ax3.spines["top"].set_visible(False)
                ax3.spines["right"].set_visible(False)
                ax3.get_xaxis().tick_bottom()
                ax3.get_yaxis().tick_left()
                ax4 = plt.subplot(514)
                ax4.spines["top"].set_visible(False)
                ax4.spines["right"].set_visible(False)
                ax4.get_xaxis().tick_bottom()
                ax4.get_yaxis().tick_left()
                ax5 = plt.subplot(515)
                ax5.spines["top"].set_visible(False)
                ax5.spines["right"].set_visible(False)
                ax5.get_xaxis().tick_bottom()
                ax5.get_yaxis().tick_left()

                ax1.plot(t[:], delta_a[start:stop] * 180 / np.pi, color=tableau20[1])
                ax1.set(ylabel=r'$\delta_a$ [deg]')
                ax1.set_xlim(xmin=0, xmax=t[-1])

                ax2.plot(t[:], delta_r[start:stop] * 180 / np.pi, color=tableau20[1])
                ax2.set(ylabel=r'$\delta_r$ [deg]')
                ax2.set_xlim(xmin=0, xmax=t[-1])

                ax3.plot(t[:], sys_response[1][1], label='Simulated response', color=tableau20[4], marker='1', markevery=20)
                ax3.plot(t[:], roll_angle[start:stop], label='Measured response', color=tableau20[6], marker='2', markevery=20)
                ax3.set(ylabel=r'$\phi$ [deg]')
                ax3.set_xlim(xmin=0, xmax=t[-1])
                ax3.legend(loc='upper right')

                ax4.plot(t[:], sys_response[1][2], label='Simulated response', color=tableau20[4], marker='1', markevery=20)
                ax4.plot(t[:], roll_rate[start:stop], label='Measured response', color=tableau20[6], marker='2', markevery=20)
                ax4.set(ylabel=r'$p$ [deg/s]')
                ax4.set_xlim(xmin=0, xmax=t[-1])

                ax5.plot(t[:], sys_response[1][3], label='Simulated response', color=tableau20[4], marker='1', markevery=20)
                ax5.plot(t[:], yaw_rate[start:stop], label='Measured response', color=tableau20[6], marker='2', markevery=20)
                ax5.set(ylabel=r'$r$ [deg/s]')
                ax5.set_xlim(xmin=0, xmax=t[-1])

                # plot grids
                ax1.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)
                ax1.minorticks_on()
                ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.1)
                ax2.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)
                ax2.minorticks_on()
                ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.1)
                ax3.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)
                ax3.minorticks_on()
                ax3.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.1)
                ax4.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)
                ax4.minorticks_on()
                ax4.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.1)
                ax5.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)
                ax5.minorticks_on()
                ax5.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.1)

            else:
                print('Case should be either symmetric or asymmetric')

            plt.xlabel('Time [s]')
            ax1.set_title(f'{self.title}, m = {round(m, 2)} kg', fontweight = 'bold')
            plt.savefig(path + "/src/plots/optimised_plots/" + self.title + ".pdf", dpi=250)
            plt.show()

        return eigenvalues


# test the code here
if DEBUG:
    # types of motion to extrapolate
    motions = {
        "APR": {'time': 31606, 'step': 14, 'type': "ASYM", 'name': "Aperiodic Roll"}
    }

    init_simulation = Simulate(motions['APR'])
    init_simulation.motion_report()
