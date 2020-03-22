"""
Title: Data for computations, fixed and derived from flight test data

Author: B37
"""

# importing packages
import numpy as np
import src.simulation.response_flightest as data

# types of motion to extrapolate
motions = {
    "PGH": {'time': 32490, 'step': 150, 'type': "SYM", 'name': "Phugoid Motion"},
    "SP": {'time': 30390, 'step': 14, 'type': "SYM", 'name': "Short Period Motion"},
    "DR": {'time': 34397, 'step': 15, 'type': "ASYM", 'name': "Dutch Roll Motion"},
    "DRY": {'time': 35210, 'step': 15, 'type': "ASYM", 'name': "Dutch Roll Motion (YawDamping)"},
    "APR": {'time': 31606, 'step': 14, 'type': "ASYM", 'name': "Aperiodic Roll"},
    "SPI": {'time': 36760, 'step': 140, 'type': "ASYM", 'name': "Spiral Motion"}
}

# default, to be changed
start  = 30390
step   = 14

# Stationary flight condition
hp0    =  data.pressalt[start]     	# pressure altitude in the stationary flight condition [m]
V0     =  data.TAS[start]           # true airspeed in the stationary flight condition [m/sec]
alpha0 =  0.0                       # angle of attack in the stationary flight condition [rad]
th0    =  0                         # pitch angle in the stationary flight condition [rad]

# Aircraft mass
cabin  = 102+90+78+74+79+82+80+87+68
fuel0  = 4100*0.453592
fuel_b = np.cumsum(0.1 * np.ones(data.FMF.shape[0]) * data.FMF)
fuel   = fuel0 - fuel_b
m      = 4157.174 + cabin + fuel           # mass [kg] 4157.174
m      = m[start]

# aerodynamic properties
e      = 0.78         # Oswald factor [ ]
CD0    = 0.021        # Zero lift drag coefficient [ ]
CLa    = 0.08       # Slope of CL-alpha curve [ ]

# Longitudinal stability
Cma    =  -0.725           # longitudinal stabilty [ ]
Cmde   =  -1.512           # elevator effectiveness [ ]

# Aircraft geometry

S      = 30.00	          # wing area [m^2]
Sh     = 0.2 * S         # stabiliser area [m^2]
Sh_S   = Sh / S	          # [ ]
lh     = 0.71 * 5.968    # tail length [m]
c      = 2.0569	          # mean aerodynamic cord [m]
xcg    = 0.05 * c
lh_c   = lh / c	          # [ ]
b      = 15.911	          # wing span [m]
bh     = 5.791	          # stabilser span [m]
A      = b ** 2 / S      # wing aspect ratio [ ]
Ah     = bh ** 2 / Sh    # stabilser aspect ratio [ ]
Vh_V   = 1	          # [ ]
ih     = -2 * np.pi / 180   # stabiliser angle of incidence [rad]

# Constant values concerning atmosphere and gravity

rho0   = 1.2250          # air density at sea level [kg/m^3]
lam    = -0.0065         # temperature gradient in ISA [K/m]
Temp0  = 288.15          # temperature at sea level in ISA [K]
R      = 287.05          # specific gas constant [m^2/sec^2K]
g      = 9.81            # [m/sec^2] (gravity constant)

# air density [kg/m^3]
rho    = rho0 * np.power( ((1+(lam * hp0 / Temp0))), (-((g / (lam*R)) + 1)))
W      = m * g            # [N]       (aircraft weight)

# Constant values concerning aircraft inertia

muc    = m / (rho * S * c)
mub    = m / (rho * S * b)
KX2    = 0.019
KZ2    = 0.042
KXZ    = 0.002
KY2    = 1.25 * 1.114

# Aerodynamic constants

Cmac   = 0                      # Moment coefficient about the aerodynamic centre [ ]
CNwa   = CLa                    # Wing normal force slope [ ]
CNha   = 2 * np.pi * Ah / (Ah + 2) # Stabiliser normal force slope [ ]
depsda = 4 / (A + 2)            # Downwash gradient [ ]

# Lift and drag coefficient

CL = 2 * W / (rho * V0 ** 2 * S)              # Lift coefficient [ ]
CD = CD0 + (CLa * alpha0) ** 2 / (np.pi * A * e) # Drag coefficient [ ]

# Stabiblity derivatives subjected to optimisation

CX0    = W * np.sin(th0) / (0.5 * rho * V0 ** 2 * S)  # do not tweak
CXu    = -0.08368199988749644 # -0.095
CXa    = -0.07763650050760139 # +0.47966		# Positive! (has been erroneously negative since 1993)
CXadot = +0.08330
CXq    = -0.28170
CXde   = -0.03728

CZ0    = -W * np.cos(th0) / (0.5 * rho * V0 ** 2 * S)  # do not tweak
CZu    = -0.9895177921517261 # -0.37616
CZa    = -5.795166947573803  # -5.74340
CZadot = -0.00350
CZq    = -5.66290
CZde   = -0.69612

Cmu    = 0.05997299778919825 # +0.06990
Cmadot = 1.9647153421455705 # +0.17800
Cmq    = -10.44375502346348 # -8.79415

CYb    = -3.8969164196214683 # -0.7500
CYbdot =  0
CYp    = -0.0304
CYr    = +0.8495
CYda   = -0.0400
CYdr   = +0.2300

Clb    = -0.10260
Clp    = -0.9420970769486041  # -0.71085
Clr    = +0.23760
Clda   = -0.23088
Cldr   = +0.03440

Cnb    =  +0.1348
Cnbdot =   0
Cnp    =  -0.0602
Cnr    =  0.10798041327461753 # 0.00330453
Cnda   =  -0.0120
Cndr   =  -0.0939