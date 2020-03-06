from mass_and_balance import *
import matplotlib.pyplot as plt
import scipy.io as sio
from scipy import integrate
import numpy as np

g = 9.807   # Gravity
S = 30      # Surface Area [m^2]
c = 2.0569  # Chord [m]
b = 15.911  # Span [m]


""" Import data from matlab """
matlab_data = sio.loadmat('matlab.mat')
fuel_flow_left  = np.array(matlab_data['flightdata']['lh_engine_FMF'][0][0][0][0][0]).reshape(48321)*lbshr_to_kgsec(1)
fuel_flow_right = np.array(matlab_data['flightdata']['rh_engine_FMF'][0][0][0][0][0]).reshape(48321)*lbshr_to_kgsec(1)
fuel_out_left = np.array(matlab_data['flightdata']['rh_engine_FU'][0][0][0][0][0]).reshape(48321)*pounds_to_kg(1)
fuel_out_right = np.array(matlab_data['flightdata']['rh_engine_FU'][0][0][0][0][0]).reshape(48321)*pounds_to_kg(1)
# fuel_out = np.array([0.]+ list(integrate.cumtrapz(fuel_flow_left+fuel_flow_right, time)))
fuel_out = fuel_out_right + fuel_out_left
fuel_mass = pounds_to_kg(4050)-fuel_out
time = np.array(matlab_data['flightdata']['time'][0][0][0][0][0][0])


""" From: Table E.2. Citation II fuel moments with respect to the datum line """

fuel_loads = np.array([pounds_to_kg(100), pounds_to_kg(200), pounds_to_kg(300), pounds_to_kg(400),
                        pounds_to_kg(500), pounds_to_kg(600), pounds_to_kg(700), pounds_to_kg(800),
                        pounds_to_kg(900), pounds_to_kg(1000), pounds_to_kg(1100), pounds_to_kg(1200),
                        pounds_to_kg(1300), pounds_to_kg(1400), pounds_to_kg(1500), pounds_to_kg(1600),
                        pounds_to_kg(1700), pounds_to_kg(1800), pounds_to_kg(1900), pounds_to_kg(2000),
                        pounds_to_kg(2100), pounds_to_kg(2200), pounds_to_kg(2300), pounds_to_kg(2400),
                        pounds_to_kg(2500), pounds_to_kg(2600), pounds_to_kg(2700), pounds_to_kg(2800),
                        pounds_to_kg(2900), pounds_to_kg(3000), pounds_to_kg(3100), pounds_to_kg(3200),
                        pounds_to_kg(3300), pounds_to_kg(3400), pounds_to_kg(3500), pounds_to_kg(3600),
                        pounds_to_kg(3700), pounds_to_kg(3800), pounds_to_kg(3900), pounds_to_kg(4000),
                        pounds_to_kg(4100), pounds_to_kg(4200), pounds_to_kg(4300), pounds_to_kg(4400)])

fuel_moments = np.array([298.16, 591.18, 879.08, 1165.42,
                         1448.40, 1732.53, 2014.80, 2298.84,
                         2581.92, 2866.30, 3150.18, 3434.52,
                         3718.52, 4003.23, 4287.76, 4572.24,
                         4856.56, 5141.16, 5425.64, 5709.90,
                         5994.04, 6278.47, 6562.82, 6846.96,
                         7131.00, 7415.33, 7699.60, 7984.34,
                         8269.06, 8554.05, 8839.04, 9124.80,
                         9410.62, 9696.97, 9983.40, 10270.08,
                         10556.84, 10843.87, 11131.00, 11418.20,
                         11705.50, 11993.31, 12281.18, 12569.04])

fuel_xcgs = fuel_moments/fuel_loads


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