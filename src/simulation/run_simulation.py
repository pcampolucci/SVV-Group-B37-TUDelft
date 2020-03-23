"""
Title: Main Simulation Launcher

Author: Pietro Campolucci
"""

# import dependencies
import tkinter
from src.input.parameters_citation import motions
from src.simulation.numerical_model import Simulate


def run_simulation(width, height):

    get_eigenvalues_symmetric = Simulate(motions['PGH'], width, height)
    eigenvalues_symmetric = get_eigenvalues_symmetric.motion_report(show=False)

    get_eigenvalues_asymmetric = Simulate(motions['DR'], width, height)
    eigenvalues_asymmetric = get_eigenvalues_asymmetric.motion_report(show=False)

    print(f"Eigenvalues for symmetric EOM are: \n")
    for ev in eigenvalues_symmetric:
        print(ev, "\n")

    print(f"Eigenvalues for asymmetric EOM are: \n")
    for ev in eigenvalues_asymmetric:
        print(ev, "\n")

    window = tkinter.Tk()

    window.geometry("%dx%d+%d+%d" % (330, 80, 200, 150))
    window.title("Flight Motion Simulator")

    data = {
        "Phugoid Motion": "PGH",
        "Short Period Motion": "SP",
        "Dutch Roll Motion": "DR",
        "Dutch Roll Motion (YawDamping)": "DRY",
        "Aperiodic Roll": "APR",
        "Spiral Motion": "SPI"
    }

    def plot_motion(motion):
        display.config(text=f"Plotting for {motion}")
        init_plotting = Simulate(motions[data[motion]], width, height)
        init_plotting.motion_report()


    # execute program
    var = tkinter.StringVar()
    var.set('Phugoid Motion')
    p = tkinter.OptionMenu(window, var, *data, command=plot_motion)
    p.pack()

    display = tkinter.Label(window)
    display.pack()

    window.mainloop()

    print("\n... exiting")