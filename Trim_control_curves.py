from mass_and_balance import *
from clcd_clalpha_plots import S,c
from flight_data import *
from conversions import *
import matplotlib.pyplot as plt
import numpy as np

W = []

for t in measurements_3.timestamps:
    update_fuel_balance(t)
    W.append(components['TM'].weight())

Veq_tilde = Veq*np.sqrt(Ws/W)
Fe_star = Fe*Ws/W

plt.scatter(Veq_tilde, Fe_star)
plt.show()