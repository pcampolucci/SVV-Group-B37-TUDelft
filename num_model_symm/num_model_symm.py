import control as c
import complete_par as par
import numpy as np
import matplotlib.pyplot as plt

#check if the results make sense and if feedback is needed.

case = 'a'+'symmetric'
if case == 'symmetric':
    C1 = np.matrix([[-2*par.muc*par.c/(par.V0**2), 0, 0, 0],
                    [0, (par.CZadot - 2*par.muc)*par.c/par.V0, 0, 0],
                    [0,0, -par.c/par.V0, 0],
                    [0, par.Cmadot*par.c/par.V0, 0, -2*par.muc*par.KY2*(par.c/par.V0)**2]])
    C2 = - np.matrix([[-par.CXu/par.V0, -par.CXa, -par.CZ0, 0],
                      [-par.CZu/par.V0, -par.CZa, par.CX0, (-par.CZq - 2*par.muc)*(par.c/par.V0)],
                      [0, 0, 0, -(par.c/par.V0)],
                      [-par.Cmu/par.V0, -par.Cma, 0, -par.Cmq*par.c/par.V0]])
    C3 = - np.matrix([[-par.CXde],
                      [-par.CZde],
                      [0],
                      [-par.Cmde]])
elif case == 'asymmetric':
    C1 = np.matrix([[(par.CYbdot - 2 * par.mub) * par.b / par.V0, 0, 0, 0],
                    [0, -par.b / (2 * par.V0), 0, 0],
                    [0, 0, -2 * par.mub * par.KX2 * (par.b ** 2) / (par.V0 ** 2),
                     2 * par.mub * par.KXZ * (par.b ** 2) / (par.V0 ** 2)],
                    [par.Cnbdot * (par.b) / (par.V0), 0, 2 * par.mub * par.KXZ * (par.b ** 2) / (par.V0 ** 2),
                     -2 * par.mub * par.KZ2 * (par.b ** 2) / (par.V0 ** 2)]])
    C2 = np.matrix([[par.CYb, par.CL, par.CYp * (par.b) / (2 * par.V0), (par.CYr - 4 * par.mub) * (par.b) / (2 * par.V0)],
                    [0, 0, 1, 0],
                    [par.Clb, 0, par.Clp * (par.b) / (2 * par.V0), par.Clr * (par.b) / (2 * par.V0)],
                    [par.Cnb, 0, par.Cnp * (par.b) / (2 * par.V0), par.Cnr * (par.b) / (2 * par.V0)]])
    C3 = np.matrix([[par.CYda, par.CYdr],
                    [0, 0],
                    [par.Clda, par.Cldr],
                    [par.Cnda, par.Cndr]])

else:
    print('Case must be either symmetric or asymmetric')

C1_inv = np.linalg.inv(C1)
C2_inv = np.linalg.inv(C2)
A = - np.matmul(C1_inv, C2)
B = - np.matmul(C1_inv, C3)

#outputs
if case == 'symmetric':
    C = np.matrix([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    D = np.matrix([[0], [0], [0], [0]])
elif case == 'asymmetric':
    C = np.matrix([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    D = np.matrix([[0, 0], [0, 0], [0, 0], [0, 0]])
else:
    print('Case must be either symmetric or asymmetric')
#define simulation time and time steps
t_sim = 120
dt_sim = 0.05
num_dts = int(t_sim/dt_sim)
dts = dt_sim*np.ones(num_dts)
t = np.linspace(0,t_sim, num_dts)

#create state space linear system and compute system response
sys = c.ss(A,B,C,D)
sys_response = c.impulse_response(sys, t)

#plotting stuff
plt.plot(sys_response[0], sys_response[1][0])
plt.show()
print(sys_response[1][0][0])