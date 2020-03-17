"""
Title: General plotting function
    - Created so that plots in the report will be consistent

Author: Casper Kanaar 
"""
# =============================================================================
import numpy as np 
from matplotlib import pyplot as plt 
import seaborn as sns 
sns.set() 


def plot(x_array, y_array, labels, title, axis, filename, multi=False):
    """
    Inputs:
        - x_array: a two dimensional array containing the different x datasets
        - y_array: a two dimensional array containing the different y datasets 
        - labels: a list of strings which will be the labels of the individual line 
    
    Outputs: 
        - A single plot which will be saved with dpi 250 
    """ 
    # Some random colors 
    colors = ["black", "blue", "red", "orange", "green", "yellow", "pink", "purple"]

    plt.figure(figsize=(10, 5))
    plt.title(title)

    if multi:

        for i in range(len(x_array)):
            with sns.color_palette("rocket_r", len(x_array)):
                plt.plot(np.array(x_array[i]), np.array(y_array[i]), label=labels[i])

    else:
        plt.plot(x_array, y_array, color=colors[0], label=labels)

    plt.xlabel(axis[0])
    plt.ylabel(axis[1])
    plt.legend()
    plt.savefig(filename, dpi=250)
