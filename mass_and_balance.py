
import numpy as np
import scipy.io as sio
from conversions import *
from scipy import integrate


FW = 4050      # [lbs]




def update_fuel_balance(t):
    components['FL'].mass_ = np.interp(t, time, fuel_mass)
    components['FL'].xcg_  = np.interp(components['FL'].mass(), fuel_loads, fuel_xcgs)


""" Represents an object having a mass and a center of gravity. Used for stability calculations """
class Component:
    def __init__(self, xcg, mass):
        self.xcg_ = xcg
        self.mass_ = mass

    def mass(self):
        return self.mass_

    def xcg(self):
        return self.xcg_

    def moment(self):
        return self.mass()*self.xcg()

    def weight(self):
        return self.mass()*9.807


""" Represents an object having a mass and a center of gravity. Used for stability calculations """
class Group:
    def __init__(self, cs):
        self.components = cs

    def mass(self):
        m = 0
        for component in self.components:
            m += component.mass()
        return m

    def xcg(self):
        p = 0
        m = 0

        for component in self.components:

            p += component.moment()           # Moment contribution of sub component
            m += component.mass()             # Mass contribution of sub component

        return p / m

    def moment(self):
        return self.xcg() * self.mass()

    def weight(self):
        return self.mass()*9.807


components = {}

""" Seats """
components['Seat 1'] = Component(inches_to_m(131), 95)
components['Seat 2'] = Component(inches_to_m(131), 92)
components['Seat 3'] = Component(inches_to_m(214), 74)
components['Seat 4'] = Component(inches_to_m(214), 66)
components['Seat 5'] = Component(inches_to_m(251), 61)
components['Seat 6'] = Component(inches_to_m(251), 75)
components['Seat 7'] = Component(inches_to_m(288), 78)
components['Seat 8'] = Component(inches_to_m(288), 86)
components['Seat 10'] = Component(inches_to_m(170), 68)

""" Baggage """
components['Nose'] = Component(inches_to_m(131), pounds_to_kg(0))
components['Aft 1'] = Component(inches_to_m(131), 0)
components['Aft 2'] = Component(inches_to_m(131), 0)

""" Payload """
components['Payload'] = Group([components['Seat 1'], components['Seat 2'], components['Seat 3'], components['Seat 4'],
                               components['Seat 5'], components['Seat 6'], components['Seat 7'], components['Seat 8'],
                               components['Seat 10'], components['Nose'], components['Aft 1'], components['Aft 2']])

""" Basic Emtpy Mass """
components['BEM'] = Component(inches_to_m(291.65), pounds_to_kg(9165))

""" Zero Fuel Mass """
components['ZFM'] = Group([components['BEM'],components['Payload']])

""" Fuel Load """
components['FL'] = Component(inches_to_m(287.58), pounds_to_kg(4050))

""" Total Mass """
components['TM'] = Group([components['ZFM'], components['FL']])

"""
components[name].mass() to get mass     [kg]
components[name].weight() to get weight [N]
components[name].moment() to get moment [N*m]
components[name].xcg() to get xcg       [m]
"""


""" From: Table E.2. Citation II fuel moments with respect to the datum line """

fuel_loads = pounds_to_kg( np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200,
                        1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400,
                        2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500, 3600,
                        3700, 3800, 3900, 4000, 4100, 4200, 4300, 4400]))

fuel_moments = lbsinch_to_kgm(np.array([298.16, 591.18, 879.08, 1165.42, 1448.40, 1732.53, 2014.80, 2298.84, 2581.92, 2866.30, 3150.18, 3434.52,
                         3718.52, 4003.23, 4287.76, 4572.24, 4856.56, 5141.16, 5425.64, 5709.90, 5994.04, 6278.47, 6562.82, 6846.96,
                         7131.00, 7415.33, 7699.60, 7984.34, 8269.06, 8554.05, 8839.04, 9124.80, 9410.62, 9696.97, 9983.40, 10270.08,
                         10556.84, 10843.87, 11131.00, 11418.20, 11705.50, 11993.31, 12281.18, 12569.04]))*100

fuel_xcgs = fuel_moments/fuel_loads


""" Import data from matlab """
matlab_data = sio.loadmat('matlab.mat')
fuel_flow_left  = np.array(matlab_data['flightdata']['lh_engine_FMF'][0][0][0][0][0]).reshape(48321)*lbshr_to_kgsec(1)
fuel_flow_right = np.array(matlab_data['flightdata']['rh_engine_FMF'][0][0][0][0][0]).reshape(48321)*lbshr_to_kgsec(1)
fuel_out_left = np.array(matlab_data['flightdata']['rh_engine_FU'][0][0][0][0][0]).reshape(48321)*pounds_to_kg(1)
fuel_out_right = np.array(matlab_data['flightdata']['rh_engine_FU'][0][0][0][0][0]).reshape(48321)*pounds_to_kg(1)
# fuel_out = np.array([0.]+ list(integrate.cumtrapz(fuel_flow_left+fuel_flow_right, time))) # To verify
fuel_out = fuel_out_right + fuel_out_left                                               # Fuel burnt along time [kg]
fuel_mass = pounds_to_kg(FW)-fuel_out                                                 # Fuel Mass along time  [kg]
time = np.array(matlab_data['flightdata']['time'][0][0][0][0][0][0])                    # Time values           [s]


""" 
To update Fuel Component mass:

components['FL'].mass_ = np.interp(t, time, fuel_mass)


Where t is a specific time

"""













