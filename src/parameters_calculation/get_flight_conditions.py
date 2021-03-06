from src.parameters_calculation.get_flight_data import *
from src.helpers.path import path

measurements = [measurement_1, measurement_3, measurement_3s, measurement_shift]


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
    m.Res = m.rhos*m.VTASs*c/mu
    # print('---------------')
    # print('Mach Number Range: ', np.min(m.Ms), np.max(m.Ms))
    # print('Reynolds Number Range: ', np.min(m.Res), np.max(m.Res))


thrust_input_m1 = np.array([measurement_1.hps, measurement_1.Ms, measurement_1.dTs, measurement_1.FFls, measurement_1.FFrs]).T
thrust_input_m3 = np.array([measurement_3.hps, measurement_3.Ms, measurement_3.dTs, measurement_3.FFls, measurement_3.FFrs]).T
thrust_input_m3s = np.array([measurement_3s.hps, measurement_3s.Ms, measurement_3s.dTs, measurement_3s.FFls, measurement_3s.FFrs]).T
thrust_input_shift = np.array([measurement_shift.hps, measurement_shift.Ms, measurement_shift.dTs, measurement_shift.FFls, measurement_shift.FFrs]).T

np.savetxt(path + "/src/parameters_calculation/matlab_measurements/matlab_m1.dat", thrust_input_m1, delimiter=" ")
np.savetxt(path + "/src/parameters_calculation/matlab_measurements/matlab_m3.dat", thrust_input_m3, delimiter=" ")
np.savetxt(path + "/src/parameters_calculation/matlab_measurements/matlab_m3s.dat", thrust_input_m3s, delimiter=" ")

