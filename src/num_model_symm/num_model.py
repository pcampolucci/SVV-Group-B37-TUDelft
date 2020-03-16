import control as c
import complete_par as par
import numpy as np
import matplotlib.pyplot as plt

#check if output makes sense
#for a impulse everything explodes and then goes back to 0
#velocity should not go back to 0
#aoa, pitch and pitch rate make sense to go to 0

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

# print(C1)
# print(C2)
# print(C3)
C1_inv = np.linalg.inv(C1)
C2_inv = np.linalg.inv(C2)
A = - np.matmul(C1_inv, C2)
B = - np.matmul(C1_inv, C3)

print(A)
print(B)

C = np.matrix([[1, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1]])

D = np.matrix([[0], [0], [0], [0]])
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