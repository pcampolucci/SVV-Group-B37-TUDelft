from mass_and_balance import *
from clcd_clalpha_plots import S,c

moved_pax = 'Seat 7'    #which passenger was moved?
moved_to  =  134        #to which position?
VEAS      =  82.6843    # [m/s]
rho_0       =  1.225      # [kg/m3]

#first measurement
de1 = 0
t1  = 51*60 + 2
#second measurement
de2 = -0.5
t2  = 52*60 + 46

dde = (de2-de1)*2*np.pi/360

update_fuel_balance(t1)
xcg1 = components['TM'].xcg()

components[moved_pax].xcg_ = inches_to_m(moved_to)
update_fuel_balance(t2)
xcg2 = components['TM'].xcg()

dxcg = xcg2-xcg1
W = components['TM'].weight()

CN = W/(1/2*rho_0*VEAS**2*S)
Cmd = -1/dde * CN * dxcg / c

print("Cn is: ", CN)
print("Cmd is:", Cmd)

