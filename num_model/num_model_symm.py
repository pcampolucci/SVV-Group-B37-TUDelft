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
    C2 = np.matrix([[par.CXu/par.V0, par.CXa, par.CZ0, par.CXq*par.c/par.V0],
                      [par.CZu/par.V0, par.CZa, -par.CX0, (par.CZq + 2*par.muc)*(par.c/par.V0)],
                      [0, 0, 0, par.c/par.V0],
                      [par.Cmu/par.V0, par.Cma, 0, par.Cmq*par.c/par.V0]])
    C3 =  np.matrix([[par.CXde],
                      [par.CZde],
                      [0],
                      [par.Cmde]])
elif case == 'asymmetric':
    C1 = np.matrix([[(par.CYbdot - 2 * par.mub) * par.b / par.V0, 0, 0, 0],
                    [0, -par.b / (2 * par.V0), 0, 0],
                    [0, 0, -2 * par.mub * par.KX2 * (par.b ** 2) / (par.V0 ** 2),
                     2 * par.mub * par.KXZ * (par.b ** 2) / (par.V0 ** 2)],
                    [par.Cnbdot * (par.b) / (par.V0), 0, 2 * par.mub * par.KXZ * (par.b ** 2) / (par.V0 ** 2),
                     -2 * par.mub * par.KZ2 * (par.b ** 2) / (par.V0 ** 2)]])
    C2 = np.matrix([[par.CYb, par.CL, par.CYp * (par.b) / (2 * par.V0), (par.CYr - 4 * par.mub) * (par.b) / (2 * par.V0)],
                    [0, 0, par.b/(2*par.V0), 0],
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
print(A)
# B = 0*B     #uncommet to get stick fixed stability
eigenvalues = np.linalg.eigvals(A)
print('The eigenvalues are: ', eigenvalues)
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
# print('1', C1)
# print('2', C2)
# print('3', C3)

t_sim = 60
dt_sim = 0.05
num_dts = int(t_sim/dt_sim)
dts = dt_sim*np.ones(num_dts)
t = np.linspace(0, t_sim, num_dts)
if case == 'symmetric':
    t_input = 4
    input_nums = int(t_input//dt_sim)
    elev_def1 = np.ones(input_nums)/3000
    # elev_def2 = np.flip(np.cumsum(elev_def1))
    elev_def2 = np.zeros(t.shape[0] - input_nums)
    elev_def1 = np.cumsum(elev_def1)
    # elev_def3 = np.zeros(300*3//5)
    elev_defs = np.hstack([elev_def1, elev_def2])
# elif case == 'asymmetric':
#     continue

else:
    print('eskere')
#create state space linear system and compute system response
sys = c.ss(A,B,C,D)
########################################
########### if we want to add feedback
# if case == 'symmetric':
#     K = np.matrix([0, 0, 0, 0])
# elif case == 'asymmetric':
#     K = np.matrix([[0, 0, 0, 0], [0, 0, 0, 0]])
# sys1 = c.feedback(sys, K, 1)
#########################################
# sys_response = c.forced_response(sys, t, elev_defs)
sys_response = c.impulse_response(sys, t)
##########################################
########### convert stuff
sys_response[1][0] = sys_response[1][0] + par.V0
# print(sys_response[1][0][-1])
# for i in range(1,4):
#     sys_response[1][i] = sys_response[1][i]*180/np.pi
########### plotting stuff
'''
#
plt.plot(sys_response[0], sys_response[1][2]*180/np.pi, sys_response[0], elev_defs*180/np.pi)
plt.plot(sys_response[0], sys_response[1][0], sys_response[0], elev_defs*180/np.pi)
plt.grid(color='b', linestyle='-', linewidth=0.2)
plt.show()
print('Max elevator deflection is: ',elev_defs[input_nums-1]*180/np.pi)
'''