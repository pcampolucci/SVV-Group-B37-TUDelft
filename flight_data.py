import numpy as np
from conversions import *

""" Constants """
gamma = 1.4
p_0 = 101325
rho_0 =  1.225
T_0 = 288.15
mu = 1.7E-5 # Dynamic viscosity for T = -10 to -5 deg

g = 9.80665
R = 287
Tgrad = -0.0065

""" Aircraft Data """
S = 30          # Surface Area [m^2]
c = 2.0569      # Chord [m]
b = 15.911      # Span [m]
CmTc = -0.0064  # Dimensionless Arm Thrust Coefficient

# From: https://en.wikipedia.org/wiki/Pratt_%26_Whitney_Canada_JT15D
D = 0.686       # Engine Diameter [m]

Ws = 60500    #[N]
mfs = 0.048   #[kg/sec]

""" Flight Data """

class MeasurementSet:
    def __init__(self, timestamps, hps, VCASs, alphas, FFls, FFrs, Fused, Tms, de = np.zeros(1), detr = np.zeros(1), Fe = np.zeros(0)):
        self.timestamps = timestamps
        self.hps = hps
        self.VCAs = VCASs
        self.alphas = alphas
        self.FFls = FFls
        self.FFrs = FFrs
        self.Fused = Fused
        self.Tms = Tms
        self.des = de
        self.detrs = detr
        self.Fes = Fe

""" Stationary Measurements CL-CD Series 1 """

timestamps = np.array([19*60+17, 21*60+37, 23*60+46, 26*60+4, 29*60+47, 32*60])
hps = feet_to_m(np.array([5010, 5020, 5020, 5030, 5020, 5110]))
VCASs = kt_to_ms(np.array([249, 221, 192, 163, 130, 118]))
alphas = np.array([1.7, 2.4, 3.6, 5.4, 8.7, 10.6])
FFls = lbshr_to_kgsec(np.array([798, 673, 561, 463, 443, 474]))
FFrs = lbshr_to_kgsec(np.array([813, 682, 579, 484, 467, 499]))
Fused = pounds_to_kg(np.array([360, 412, 447, 478, 532, 570]))
Tms = cdeg_to_kdeg(np.array([12.5, 10.5, 8.8, 7.2, 6, 5.2]))

measurement_1 = MeasurementSet(timestamps, hps, VCASs, alphas, FFls, FFrs, Fused, Tms)


""" Stationary Measurements Elevator Trim curve (Series 3)"""
timestamps = np.array([37*60+19, 39*60+11, 41*60+24, 42*60+56, 45*60+41, 47*60+20, 48*60+40])
hps = feet_to_m(np.array([6060,6350,6550,6880,6160,5810,5310]))
VCASs = kt_to_ms(np.array([161, 150, 140, 130, 173, 179, 192]))
alphas = np.array([5.3, 6.3, 7.3, 8.5, 4.5, 4.1, 3.4])
des = np.array([0, -0.4, -0.9, -1.5, 0.4, 0.6, 1])
detrs = np.array([2.8, 2.8, 2.8, 2.8, 2.8, 2.8, 2.8])
Fes = np.array([0, -23, -29, -46, 26, 40, 83])
FFls = lbshr_to_kgsec(np.array([462, 458, 454, 449, 465, 472, 482]))
FFrs = lbshr_to_kgsec(np.array([486, 482,477, 473, 489, 496, 505]))
Fused = pounds_to_kg(np.array([664, 694, 730, 755, 798, 825, 846]))
Tms = cdeg_to_kdeg(np.array([5.5, 4.5, 3.5, 2.5, 5.0, 6.2, 8.2]))

measurement_3 = MeasurementSet(timestamps, hps, VCASs, alphas, FFls, FFrs, Fused, Tms, des, detrs, Fes)


""" Stationary Measurements Elevator Trim curve (Stand. Mass Flow)"""
timestamps = np.array([37*60+19, 39*60+11, 41*60+24, 42*60+56, 45*60+41, 47*60+20, 48*60+40])
hps = feet_to_m(np.array([6060,6350,6550,6880,6160,5810,5310]))
VCASs = kt_to_ms(np.array([161, 150, 140, 130, 173, 179, 192]))
alphas = np.array([5.3, 6.3, 7.3, 8.5, 4.5, 4.1, 3.4])
des = np.array([0, -0.4, -0.9, -1.5, 0.4, 0.6, 1])
detrs = np.array([2.8, 2.8, 2.8, 2.8, 2.8, 2.8, 2.8])
Fes = np.array([0, -23, -29, -46, 26, 40, 83])
FFls = np.array([0.048, 0.048, 0.048, 0.048, 0.048, 0.048, 0.048])
FFrs = np.array([0.048, 0.048, 0.048, 0.048, 0.048, 0.048, 0.048])
Fused = pounds_to_kg(np.array([664, 694, 730, 755, 798, 825, 846]))
Tms = cdeg_to_kdeg(np.array([5.5, 4.5, 3.5, 2.5, 5.0, 6.2, 8.2]))


measurement_3s = MeasurementSet(timestamps, hps, VCASs, alphas, FFls, FFrs, Fused, Tms, des, detrs, Fes)
