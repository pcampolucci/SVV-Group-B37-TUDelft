import control as c
import maximo_pars as par
import numpy as np
import matplotlib.pyplot as plt
import response_flightest as data

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

#create state space linear system and compute system response
sys = c.ss(A,B,C,D)
#########################################
############# DEFINE INPUTS
start = 37070
step = 18
stop = start + step*10
t = data.time[start:stop]
if case == 'symmetric':
    elev_defs = data.delta_e*np.pi/180
    elev_defs = elev_defs[start:stop]
elif case == 'asymmetric':
    delta_a = data.delta_a*np.pi/180
    delta_r = data.delta_r*np.pi/180
    inputs = np.vstack([delta_a, delta_r])
    print(inputs.shape)
    inputs = inputs[:,start:stop]


if case == 'symmetric':
    sys_response = c.forced_response(sys, t, elev_defs)
    delta_e = elev_defs
elif case == 'asymmetric':
    sys_response = c.forced_response(sys, t, inputs)

# sys_response = c.impulse_response(sys, t)
##########################################
########### convert stuff
pitch_angle = data.pitch_angle
pitchrate = data.pitchrate
AoAs = data.AoAs
roll = data.roll_angle


sli = -1
if case == 'symmetric':
    sys_response[1][2][:sli] = sys_response[1][2][:sli]*180/np.pi + pitch_angle[start]
    sys_response[1][3][:sli] = sys_response[1][3][:sli]*180/np.pi + pitchrate[start]
    sys_response[1][1][:sli] = sys_response[1][1][:sli]*180/np.pi + AoAs[start]
elif case == 'asymmetric':
    # sys_response[1][2][:sli] = sys_response[1][2][:sli]*180/np.pi + pitch_angle[start]
    # sys_response[1][3][:sli] = sys_response[1][3][:sli]*180/np.pi + pitchrate[start]
    sys_response[1][2][:sli] = sys_response[1][2][:sli]*180/np.pi + roll[start]

########################################################################
########################################################################
########### PLOT STUFF
tableau20 = [(255, 87, 87), (137, 255, 87), (87, 255, 249), (0, 0, 0),
             (255, 33, 33), (255, 192, 33), (244, 255, 33), (64, 255, 175),
             (225, 107, 255), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)
ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
# ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
# ax.spines["left"].set_visible(False)

ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# Show the major grid lines with dark grey lines
plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)

# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.1)
plt.rcParams.update({'font.size': 9})

t = t-start/10 - 9


# plt.plot(t[:sli], sys_response[1][0][:sli], label = 'Yaw angle sim [deg]', color = tableau20[8])
# plt.plot(t[:sli], sys_response[1][3][:sli], label = 'Pitch rate sim [deg/s]', color = tableau20[5])
plt.plot(t[:sli], sys_response[1][2][:sli], label = 'Roll angle sim [deg]', color = tableau20[1])
# plt.plot(t[:], pitch_angle[start:stop], label = 'Pitch angle data [deg]', color = tableau20[3])
# plt.plot(t[:], pitchrate[start:stop], label = 'Pitch rate data [deg/s]', color = tableau20[4])
# plt.plot(t[:], AoAs[start:stop], label = 'Angle of attack data [deg]', color = tableau20[10])
plt.plot(t[:], roll[start:stop], label = 'Roll angle data [deg]', color = tableau20[0])
plt.legend()
plt.savefig('Asymm.pdf', dpi = 1600)
plt.show()
