from flight_data import *

measurements = [measurement_1, measurement_3]

""" Determine Flight Conditions for each flight dataset """

for m in measurements:
    m.ps = p_0 * (1+Tgrad*m.hps/T_0)**(-g/(Tgrad*R))
    m.Ms = np.sqrt(2/(gamma-1)*((1+p_0/m.ps*((1+(gamma-1)/2/gamma*rho_0/p_0*m.VCAs**2)**(gamma/(gamma-1))-1))**((gamma-1)/gamma)-1))      # Mach Number
    m.Ts = m.Tms/(1+(gamma-1)/2*m.Ms**2)                             # True Air Temperature
    m.rhos = m.ps/m.Ts/R                                             # True Air Density
    m.VTASs = m.Ms*np.sqrt(gamma*R*m.Ts)                             # True Airspeed
    m.TISAs = T_0 + Tgrad * m.hps                                    # ISA Temperature
    m.dTs = m.Ts-m.TISAs                                             # T-Tisa
    m.VEASs = m.VTASs * np.sqrt(m.rhos / rho_0)                      # Equivalent Airspeed

thrust_input = np.array([measurement_1.hps, measurement_1.Ms, measurement_1.dTs, measurement_1.FFls, measurement_1.FFrs]).T
np.savetxt("matlab.dat", thrust_input, delimiter=" ")


