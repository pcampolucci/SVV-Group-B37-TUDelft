import numpy as np
import matplotlib.pyplot as plt
import scipy.io

############## Grab data ####################
data = scipy.io.loadmat('FTISxprt-20200309_flight1.mat')
flightdata = data['flightdata']
plotting = 'on'
start = 36810 #s/10
step = 200 #s
stop = start + step * 10 #s/10

AoAs = flightdata[0][0][0][0][0][0][:,0]
dtes = flightdata[0][0][1][0][0][0][:,0]
lh_engine_FMF = flightdata[0][0][3][0][0][0][:,0]*0.453592/3600 #kg/s
rh_engine_FMF = flightdata[0][0][4][0][0][0][:,0]*0.453592/3600
delta_a = flightdata[0][0][16][0][0][0][:,0]
delta_e = flightdata[0][0][17][0][0][0][:,0]
delta_r = flightdata[0][0][18][0][0][0][:,0]
roll_angle = flightdata[0][0][21][0][0][0][:,0]
pitch_angle = flightdata[0][0][22][0][0][0][:,0]
rollrate = flightdata[0][0][26][0][0][0][:,0]
pitchrate = flightdata[0][0][27][0][0][0][:,0]
yawrate = flightdata[0][0][28][0][0][0][:,0]
pressalt = flightdata[0][0][37][0][0][0][:,0]*0.3048
TAS = flightdata[0][0][42][0][0][0][:,0]*0.5144 #m/s
time = flightdata[0][0][48][0][0][0][0]


FMF = lh_engine_FMF+lh_engine_FMF

######################################################
######################################################

''' PLOTTING STUFF'''
if plotting == 'on':
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    # ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    # ax.spines["left"].set_visible(False)

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    # ratio = 800
    # xleft, xright = ax.get_xlim()
    # ybottom, ytop = ax.get_ylim()
    # # the abs method is used to make sure that all numbers are positive
    # # because x and y axis of an axes maybe inversed.
    # ax.set_aspect(abs((xright - xleft)) / abs((ytop - ybottom)) * ratio)

    # Show the major grid lines with dark grey lines
    plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)

    # Show the minor grid lines with very faint and almost transparent grey lines
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.1)
    plt.rcParams.update({'font.size': 9})

    # plt.plot(time[start:stop], pitch_angle[start:stop], label = 'Pitch angle [deg]')
    # plt.plot(time[start:stop], pitchrate[start:stop], label = 'Pitch rate [deg]')
    plt.plot(time[start:stop] - start / 10 - 9, delta_a[start:stop], label='Aileron deflection [deg]')
    plt.plot(time[start:stop] - start / 10 - 9, delta_r[start:stop], label='Rudder deflection [deg]')
    plt.legend()
    plt.show()
elif plotting == 'off':
    print('No plots')
else:
    print('Plotting must be either on or off')


