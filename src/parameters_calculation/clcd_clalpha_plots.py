from src.parameters_calculation.mass_and_balance import *
import matplotlib.pyplot as plt
from src.parameters_calculation.flight_conditions import *
import numpy as np
from src.helpers.path import path

thrusts = np.loadtxt(path + '/src/parameters_calculation/matlab_measurements/measurement_1_thrust.dat')
drags = thrusts[:,0] + thrusts[:,1]

weights = []

for t in measurement_1.timestamps:
    update_fuel_balance(t)
    weights.append(components['TM'].weight())

lifts = np.array(weights)

CLs = lifts/(0.5*measurement_1.rhos*measurement_1.VTASs**2*S)
CDs = drags/(0.5*measurement_1.rhos*measurement_1.VTASs**2*S)

A = np.vstack([measurement_1.alphas, np.ones(len(measurement_1.alphas))]).T
CLa, CL0 = np.linalg.lstsq(A, CLs, rcond=None)[0]
print('CLa: ', CLa, 'CL0: ', CL0)

A = np.vstack([CLs**2, np.ones(len(CLs))]).T
slope, CD0 = np.linalg.lstsq(A, CDs, rcond=None)[0]
e = 1/slope/(b/c)/np.pi
print('CD0: ', CD0, 'Oswald: ', e)

alpha_ = np.linspace(-5, 15, 100)
CLs_ = CL0 + CLa * alpha_
CDs_ = CD0 + slope*CLs_**2

if __name__ == '__main__':
    plt.scatter(measurement_1.alphas, CLs)
    plt.plot(alpha_, CLs_)
    plt.xlabel('Alpha [deg]')
    plt.ylabel('CL [-]')
    plt.title('CL - Alpha')
    plt.grid()
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    plt.show()

    plt.scatter(CDs, CLs)
    plt.plot(CDs_, CLs_)
    plt.xlabel('CD [-]')
    plt.ylabel('CL [-]')
    plt.title('CL - CD')
    plt.grid()
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    plt.show()

print('Mach Range: ')
