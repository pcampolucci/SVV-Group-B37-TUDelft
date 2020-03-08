from flight_data import *


""" Determine Flight Conditions from given flight data """
p = p_0 * (1+Tgrad*hp/T_0)**(-g/(Tgrad*R))              # True Air Pressure
M = np.sqrt(2/(gamma-1)*((1+p_0/p*((1+(gamma-1)/2/gamma*rho_0/p_0*Vi**2)**(gamma/(gamma-1))-1))**((gamma-1)/gamma)-1))      # Mach Number
T = Tm/(1+(gamma-1)/2*M**2)                             # True Air Temperature
rho = p/T/R                                             # True Air Density
Vt = M*np.sqrt(gamma*R*T)                               # True Airspeed
Tisa = T_0 + Tgrad * hp                                 # ISA Temperature
dT = T-Tisa                                             # T-Tisa
Veq = Vt * np.sqrt(rho/rho_0)                           # Equivalent Airspeed

thrust_input = np.array([hp, M, dT, FFl, FFr]).T
np.savetxt("matlab.dat", thrust_input, delimiter=" ")


