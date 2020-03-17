from mass_and_balance import *
from clcd_clalpha_plots import S,c
from flight_data import *
from conversions import *
import matplotlib.pyplot as plt


VEAS      =  measurement_shift.VEASs[0]    # [m/s]


#first measurement
de1 = measurement_shift.des[0]
t1  = measurement_shift.timestamps[0]

#second measurement
de2 = measurement_shift.des[1]
t2  = measurement_shift.timestamps[1]

print("de1 de2", measurement_shift.des, de1, de2)
dde = (de2-de1)*2*np.pi/360

update_fuel_balance(t1)
xcg1 = components['TM'].xcg()

components[moved_pax].xcg_ = inches_to_m(moved_to)
update_fuel_balance(t2)
xcg2 = components['TM'].xcg()



dxcg = xcg2-xcg1
print("dxcg:",xcg1,xcg2)
W = components['TM'].weight()

CN = W/(1/2*measurement_shift.rhos[0]*measurement_shift.VTASs[0]**2*S)
Cmd = -1/dde * CN * dxcg / c

print("Cn is: ", CN)
print("Cmd is:", Cmd)


A = np.vstack([measurement_3.alphas, np.ones(len(measurement_3.alphas))]).T
c1, c2 = np.linalg.lstsq(A, measurement_3.des, rcond=None)[0]


Cma = -c1*Cmd

if __name__ == '__main__':
    plt.scatter(measurement_3.alphas,measurement_3.des)
    plt.xlabel('Alpha [deg]')
    plt.ylabel(r'd$\delta_e$')
    plt.title(r'd$\alpha')

    plt.grid()
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')

    plt.show()

    plt.show()

print("Cma is:", Cma)