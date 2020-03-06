from mass_and_balance import *
from clcd_clalpha_plots import S,c

moved_pax = 'Seat 7'    #which passenger was moved?
moved_to  =  134        #to which position?
V_m       =
rho       =

#first measurement
de1 = 0
t1  = 51*60 + 2
#second measurement
de2 = -0.5
t2  = 52*60 + 46

dde = de2-de1

xcg1 = components['TM'].xcg()

components[moved_pax].xcg_ = inches_to_m(moved_to)

xcg2 = components['TM'].xcg()

W = 
dxcg = xcg2-xcg1
CN = W/(1/2*rho*V_m**2*S)
Cmd = -1/dde * CN * dxcg / c

