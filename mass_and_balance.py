
import numpy as np
import scipy.io as sio
from scipy import integrate


FW = 4050      # [lbs]

""" Conversions """
def inches_to_m(inches):
    return inches*0.0254


def pounds_to_kg(pounds):
    return pounds*0.453592


def lbshr_to_kgsec(lbshr):
    return lbshr/7936.64


def t_to_idx(t, A):
    return (np.abs(A-t)).argmin()


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
components['Nose'] = Component(inches_to_m(131), pounds_to_kg(220))
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












