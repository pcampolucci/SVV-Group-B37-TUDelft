from mass_and_balance import *
from clcd_clalpha_plots import S,c
from flight_data import *
from conversions import *
import matplotlib.pyplot as plt
import numpy as np

W = []

for t in measurement_3.timestamps:
    update_fuel_balance(t)
    W.append(components['TM'].weight())

Veq_tilde = measurement_3.VEASs*np.sqrt(Ws/np.array(W))
Fe_star = measurement_3.Fes*Ws/W

plt.scatter(Veq_tilde, Fe_star)
plt.ylim(np.max(Fe_star)+10,np.min(Fe_star)-10)
plt.show()