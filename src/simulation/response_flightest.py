"""
Title: Extract Data and Responses from flight test data

Author: Marco Desiderio
"""

# importing packages
import matplotlib.pyplot as plt
import scipy.io
from src.helpers.path import path

# decide if plotting or not
DEBUG = False

# get data from .mat file
data = scipy.io.loadmat(path + '/src/simulation/flight-test-data.mat')
flight_data = data['flightdata']
start = 36760  #s/10
step = 140  #s
stop = start + step * 10  #s/10

# label flight test data
AoAs = flight_data[0][0][0][0][0][0][:, 0]
dtes = flight_data[0][0][1][0][0][0][:, 0]
lh_engine_FMF = flight_data[0][0][3][0][0][0][:, 0] * 0.453592 / 3600  #kg/s
rh_engine_FMF = flight_data[0][0][4][0][0][0][:, 0] * 0.453592 / 3600
delta_a = flight_data[0][0][16][0][0][0][:, 0]
delta_e = flight_data[0][0][17][0][0][0][:, 0]
delta_r = flight_data[0][0][18][0][0][0][:, 0]
roll_angle = flight_data[0][0][21][0][0][0][:, 0]
pitch_angle = flight_data[0][0][22][0][0][0][:, 0]
rollrate = flight_data[0][0][26][0][0][0][:, 0]
pitchrate = flight_data[0][0][27][0][0][0][:, 0]
yawrate = flight_data[0][0][28][0][0][0][:, 0]
pressalt = flight_data[0][0][37][0][0][0][:, 0] * 0.3048
TAS = flight_data[0][0][42][0][0][0][:, 0] * 0.5144  #m/s
time = flight_data[0][0][48][0][0][0][0]

FMF = lh_engine_FMF+lh_engine_FMF


# plot information
def plot_response():

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
    plt.plot(time[start:stop] - start / 10 - 9, delta_a[start:stop], label='Aileron deflection [deg]')
    plt.plot(time[start:stop] - start / 10 - 9, delta_r[start:stop], label='Rudder deflection [deg]')
    plt.legend()
    plt.show()


# execute for debugging
if DEBUG:
    plot_response()
