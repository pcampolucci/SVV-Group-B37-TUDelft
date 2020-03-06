from mass_and_balance import *
import matplotlib.pyplot as plt

import numpy as np

g = 9.807   # Gravity
S = 30      # Surface Area [m^2]
c = 2.0569  # Chord [m]
b = 15.911  # Span [m]

t_measurements_1 = [19*60+17, 21*60+37, 23*60+46, 26*60+4, 29*60+47, 32*60]

for t in t_measurements_1:
    components['FL'].mass_ = np.interp(t, time, fuel_mass)

lifts_1 = []
drags_1 = np.array([3665.24 + 3771.16, 2995.55 + 3057.45, 2399.82 + 2526.26, 1863.51 + 2016.01, 1892.34 + 2070.9, 2208.97 + 2405.43])     # From Thrust Calculations
veloc_1 = np.array([137.0604074, 121.7487625, 105.8604072, 89.9308298, 71.78343604, 65.23538907])
rhos_1 =  np.array([1.062730604, 1.062438499, 1.062053816, 1.061838962, 1.061235067, 1.059017416])
alpha_1 = np.array([1.7, 2.4, 3.6, 5.4, 8.7, 10.6])

for t in t_measurements_1:
    components['FL'].mass_ = np.interp(t, time, fuel_mass)
    lifts_1.append(components['TM'].weight())


lifts_1 = np.array(lifts_1)
CLs = lifts_1/(0.5*rhos_1*veloc_1**2*S)
CDs = drags_1/(0.5*rhos_1*veloc_1**2*S)

A = np.vstack([alpha_1, np.ones(len(alpha_1))]).T
CLa, CL0 = np.linalg.lstsq(A, CLs, rcond=None)[0]
print('CLa: ', CLa, 'CL0: ', CL0)

A = np.vstack([CLs**2, np.ones(len(CLs))]).T
slope, CD0 = np.linalg.lstsq(A, CDs, rcond=None)[0]
e = 1/slope/(b/c)/np.pi

print('CD0: ', CD0, 'Oswald: ', e)

alpha_1_ = np.linspace(-5, 15, 100)
CLs_ = CL0 + CLa * alpha_1_
CDs_ = CD0 + slope*CLs_**2

plt.scatter(alpha_1, CLs)
plt.plot(alpha_1_, CLs_)
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