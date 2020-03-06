# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 11:12:06 2020

@author: rodri
"""


import control as c
import complete_par as par
import numpy as np
import matplotlib.pyplot as plt

C1 = np.matrix([[(par.CYbdot-2*par.mub)*par.b/par.V0, 0, 0, 0],
                [0, -par.b/(2*par.V0), 0, 0],
                [0,0, -2*par.mub*par.KX2*(par.b**2)/(par.V0**2), 2*par.mub*par.KXZ*(par.b**2)/(par.V0**2)],
                [par.Cnbdot*(par.b)/(par.V0), 0, 2*par.mub*par.KXZ*(par.b**2)/(par.V0**2), -2*par.mub*par.KZ2* (par.b**2)/(par.V0**2)]])
C2 =  np.matrix([[par.CYb, par.CL, par.CYp*(par.b)/(2*par.V0), (par.CYr-4*par.mub)*(par.b)/(2*par.V0)],
                  [0, 0, 1, 0],
                  [par.Clb, 0, par.Clp*(par.b)/(2*par.V0), par.Clr*(par.b)/(2*par.V0) ],
                  [par.Cnb, 0, par.Cnp*(par.b)/(2*par.V0), par.Cnr*(par.b)/(2*par.V0) ]])
C3 =  np.matrix([[par.CYda, par.CYdr],
                  [0, 0],
                  [par.Clda, par.Cldr],
                  [par.Cnda, par.Cndr]])

C1_inv = np.linalg.inv(C1)
C2_inv = np.linalg.inv(C2)

A = - np.matmul(C1_inv, C2)
B = - np.matmul(C1_inv, C3)

C = np.matrix([[1, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1]])
D = np.matrix([[0, 0], [0, 0], [0, 0], [0, 0]])

t_sim = 120
dt_sim = 0.05
num_dts = int(t_sim/dt_sim)
t = np.linspace(0,t_sim, num_dts)
sys = c.ss(A,B,C,D)
print(sys)

sys_response = c.impulse_response(sys, t)
# print('u', sys_response[1][0][-1],'a', sys_response[1][1][-1],'t', sys_response[1][2][-1],'q', sys_response[1][3][-1],)
print(sys_response[1][1])
plt.plot(sys_response[0], sys_response[1][0])
plt.show()
print(sys_response[1][0][0])