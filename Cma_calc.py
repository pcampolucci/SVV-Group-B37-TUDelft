import matplotlib.pyplot as plt
import numpy as np
from Cmd_calc import Cmd

alphas = np.array([5.3,6.3,7.3,8.5,4.5,4.1,3.4])

deltas = np.array([0,-0.4,-0.9,-1.5,0.4,0.6,1])

A = np.vstack([alphas, np.ones(len(alphas))]).T
c1, c2 = np.linalg.lstsq(A, deltas, rcond=None)[0]


Cma = -c1*Cmd
plt.scatter(alphas,deltas)
plt.xlabel('Alpha [deg]')
plt.ylabel(r'd$\delta_e$')
plt.title(r'd$\alpha')

plt.grid()
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')

plt.show()

plt.show()

print("Cma is:", Cma)