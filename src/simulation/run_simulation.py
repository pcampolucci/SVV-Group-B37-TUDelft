"""
Title: Main Simulation Launcher

Author: Pietro Campolucci
"""

# import dependencies
import tkinter
from src.input.parameters_citation import motions
from src.simulation.numerical_model import Simulate


def run_simulation():

    window = tkinter.Tk()

    window.geometry("%dx%d+%d+%d" % (330, 80, 200, 150))
    window.title("Flight Motion Simulator")

    data = {
        "Phugoid Motion": "PGH",
        "Short Period Motion": "SP",
        "Dutch Roll Motion": "DR",
        "Dutch Roll Motion (Yaw, Damping)": "DRY",
        "Aperiodic Roll": "APR"
    }


    def plot_motion(motion):
        init_plotting = Simulate(motions[data[motion]])
        init_plotting.motion_report()
        display.config(text=f"Plotting for {motion}")


    # execute program
    var = tkinter.StringVar()
    var.set('Phugoid Motion')
    p = tkinter.OptionMenu(window, var, *data, command=plot_motion)
    p.pack()

    display = tkinter.Label(window)
    display.pack()

    window.mainloop()