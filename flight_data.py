import numpy as np
from conversions import *

""" Constants """
gamma = 1.4
p_0 = 101325
rho_0 =  1.225
T_0 = 288.15

g = 9.807
R = 287
Tgrad = -0.0065

Ws = 60500    #[N]
mfs = 0.048   #[kg/sec]

""" Flight Data """
timestamps = np.array([19*60+17, 21*60+37, 23*60+46, 26*60+4, 29*60+47, 32*60])
hp = feet_to_m(np.array([5010, 5020, 5020, 5030, 5020, 5110]))
Vi = kt_to_ms(np.array([249, 221, 192, 163, 130, 118]))
alpha = np.array([1.7, 2.4, 3.6, 5.4, 8.7, 10.6])
FFl = lbshr_to_kgsec(np.array([798, 673, 561, 463, 443, 474]))
FFr = lbshr_to_kgsec(np.array([813, 682, 579, 484, 467, 499]))
Fused = pounds_to_kg(np.array([360, 412, 447, 478, 532, 570]))
Tm = cdeg_to_kdeg(np.array([12.5, 10.5, 8.8, 7.2, 6, 5.2]))

