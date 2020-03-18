"""
Title: verification script for asymmetrical maneuvers. It will cover:
       - aperiodic roll
       - dutch roll (simplified)
       - dutch roll (oversimlified)
       - spiral motion
Author: Casper Kanaar
"""
# Importing relevant modules 
from parameters_citation import * 
import numpy as np



# Coefficients of the characteristic equation 
A = 16*mub**3*(KX2*KZ2-KXZ**2)
B = -4*mub**2*(2*CYb*(KX2*KZ2 - KXZ**2)+Cnr*KX2+Clp*KZ2+(Clr+Cnp)*KXZ)
C = 2*mub*((CYb*Cnr - CYr*Cnb)*KX2+(CYb*Clp - Clb*CYp)*KZ2+((CYb*Cnp - Cnb*CYp)+(CYb*Clr-Clb*CYr))*KXZ+4*mub*Cnb*KX2+4*mub*Clb*KXZ+0.5*(Clp*Cnr-Cnp*Clr))
D = -4*mub*CL*(Clb*KZ2+Cnb*KXZ)+2*mub*(Clb*Cnp - Cnb*Clp)+0.5*CYb*(Clr*Cnp - Cnr*Clp)+0.5*CYp*(Clb*Cnr-Cnb*Clr)+0.5*CYr*(Clp*Cnb - Cnp*Clb)
E = CL*(Clb*Cnr - Cnb*Clr)

    
coefficients = [A,B,C,D,E]

eiegenvalues_asymmetric_full = np.roots(coefficients)

print(f"Eigenvalues for the full asymmetrical equations of motion: {eiegenvalues_asymmetric_full}")

