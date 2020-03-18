"""
Title: verification script for symmetrical maneuvers. It will cover:
       - Short period motion 
       - Phugoid motion

Author: Casper Kanaar
"""
import numpy as np 
from parameters_citation import * 
import math as m

# =============================================================================
# Function definitions 

def short_period_oscillation_a():
    A = 4*(muc**2)*KY2
    B = -2*muc*(KY2*CZa + Cmadot + Cmq)
    C = CZa*Cmq - 2*muc*Cma
    
    eigenvalue_short_period_oscillation_a_1 = (-B + np.sqrt(B**2 - A*C))/(2*A*C)
    eigenvalue_short_period_oscillation_a_2 = (-B - np.sqrt(B**2 - A*C))/(2*A*C)
    
    print(f"Eigenvalues for simplified short period oscillation (V = constant)(Case A): {eigenvalue_short_period_oscillation_a_1, eigenvalue_short_period_oscillation_a_2}")
    
    return eigenvalue_short_period_oscillation_a_1,eigenvalue_short_period_oscillation_a_2

def short_period_oscillation_b():
    A = -2*muc*KY2
    B = Cmadot + Cmq
    C = Cma
    
    eigenvalue_short_period_oscillation_b_1 = (-B + np.sqrt(B**2 - A*C)/(2*A*C))
    eigenvalue_short_period_oscillation_b_2 = (-B - np.sqrt(B**2 - A*C))/(2*A*C)
    
    print(f"Eigenvalues for simplified short period oscillation (V = constant, flight path angle = constant)(Case B): {eigenvalue_short_period_oscillation_b_1, eigenvalue_short_period_oscillation_b_2}")
    
    return eigenvalue_short_period_oscillation_b_1,eigenvalue_short_period_oscillation_b_2

def phugoid_oscillation_a():
    A = -4*muc**2
    B = 2*muc*CXu
    C = -CZu*CZ0
    
    eigenvalue_phugoid_oscillation_a_1 = (-B + np.sqrt(B**2 - A*C))/(2*A*C)
    eigenvalue_phugoid_oscillation_a_2 = (-B - np.sqrt(B**2 - A*C))/(2*A*C)

    
    print(f"Eigenvalues for simplified Phugoid oscillation (Angle of attack = 0, angular acceleration = 0)(Case A): {eigenvalue_phugoid_oscillation_a_1, eigenvalue_phugoid_oscillation_a_2}")
    
    return eigenvalue_phugoid_oscillation_a_1,eigenvalue_phugoid_oscillation_a_2
    
def phugoid_oscillation_b():
    A = 2*muc*(CZa*Cmq - 2*muc*Cma)
    B = 2*muc*(CXu*Cma - Cmu*CXa) + Cmq*(CZu*CXa - CXu*CZa)
    C = CZ0*(Cmu*CZa - CZu*Cma)
    
    eigenvalue_phugoid_oscillation_b_1 = (-B + np.sqrt(B**2 - A*C))/(2*A*C)
    eigenvalue_phugoid_oscillation_b_2 = (-B - np.sqrt(B**2 - A*C))/(2*A*C)
    
   
    print(f"Eigenvalues for simplified Phugoid oscillation (Angle of attack = constant, angular acceleration = 0)(Case B): {eigenvalue_phugoid_oscillation_b_1, eigenvalue_phugoid_oscillation_b_2}")
    
    return eigenvalue_phugoid_oscillation_b_1,eigenvalue_phugoid_oscillation_b_2
    
# Executing the functions 
short_period_oscillation_a()
short_period_oscillation_b()
phugoid_oscillation_a()
phugoid_oscillation_b()



    
    
    