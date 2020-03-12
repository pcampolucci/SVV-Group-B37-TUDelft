import numpy as np
import matplotlib.pyplot as plt
import scipy.io

############## Grab data ####################
data = scipy.io.loadmat('matlab.mat')
flightdata = data['flightdata']

AoAs = flightdata[0][0][0][0][0][0][:,0]
dtes = flightdata[0][0][1][0][0][0][:,0]
delta_a = flightdata[0][0][15][0][0][0][:,0]
delta_e = flightdata[0][0][16][0][0][0][:,0]
delta_r = flightdata[0][0][17][0][0][0][:,0]
pitchrate = flightdata[0][0][26][0][0][0][:,0]
pitch_angle = flightdata[0][0][21][0][0][0][:,0]
roll_angle = flightdata[0][0][20][0][0][0][:,0]
rollrate = flightdata[0][0][25][0][0][0][:,0]
yawrate = flightdata[0][0][27][0][0][0][:,0]
time = flightdata[0][0][47][0][0][0][0]

dts = 0.1*np.ones(time.shape[0])

######################################################
######################################################

''' PLOTTING STUFF'''

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
start = 32400
step = 20
stop = start + step*10

# plt.plot(time[start:stop], pitch_angle[start:stop], label = 'Pitch angle [deg]')
# plt.plot(time[start:stop], pitchrate[start:stop], label = 'Pitch rate [deg]')
plt.plot(time[start:stop]-start/10-9, delta_r[start:stop], label = 'Rudder deflection [deg]')
plt.plot(time[start:stop]-start/10-9, delta_a[start:stop], label = 'Aileron deflection [deg]')
plt.legend()
plt.show()