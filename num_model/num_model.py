import control as c
import complete_par as par
import numpy as np
import matplotlib.pyplot as plt

#check if output makes sense
#for a impulse everything explodes and then goes back to 0
#velocity should not go back to 0
#aoa, pitch and pitch rate make sense to go to 0

C1 = np.matrix([[-2*par.muc*par.c, 0, 0, 0],
                [0, (par.CZadot - 2*par.muc)*par.c/par.V0, 0, 0],
                [0,0, -par.c/par.V0, 0],
                [0, par.Cmadot, 0, -2*par.muc*par.KZ2]])
C2 = - np.matrix([[-par.CXu*par.V0, -par.CXa*par.V0, -par.CZ0, 0],
                  [-par.CZu, -par.CZa, par.CX0, -par.CZq - 2*par.muc],
                  [0, 0, 0, -1],
                  [-par.Cmu*par.V0/par.c, -par.Cma*par.V0/par.c, 0, -par.Cmq*par.V0/par.c]])
C3 = - np.matrix([[-par.CXde*par.V0],
                  [-par.CZde*par.V0],
                  [0],
                  [-par.Cmde*par.V0/par.c]])


C1_inv = np.linalg.inv(C1)
C2_inv = np.linalg.inv(C2)
A = - np.matmul(C1_inv, C2)
B = - np.matmul(C2_inv, C3)
B[0,0] = 0.
C = np.matrix([[1, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1]])
D = np.matrix([[0], [0], [0], [0]])

t = np.linspace(0,5, 500)
sys = c.ss(A,B,C,D)
sys_response = c.impulse_response(sys, t)
print('u', sys_response[1][0][-1],'a', sys_response[1][1][-1],'t', sys_response[1][2][-1],'q', sys_response[1][3][-1],)

plt.plot(sys_response[0], sys_response[1][1])
plt.show()