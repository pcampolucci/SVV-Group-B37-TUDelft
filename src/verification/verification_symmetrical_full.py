"""
Title: verification script for asymmetrical maneuvers of the full equations of motion. It will cover:
       - Short period motion 
       - Phugoid motion

Author: Casper Kanaar
"""
# Importing relevant modules 
from parameters_citation import * 
import numpy as np



# Coefficients of the characteristic equation 
A = 4*muc**2*KY2*(CZadot - 2*muc)
B = Cmadot*2*muc*(CZq+2*muc) - Cmq*2*muc*(CZadot - 2*muc) - 2*muc*KY2*(CXu*(CZadot - 2*muc)-2*muc*CZa)
C = Cma * 2 * muc*(CZq+2*muc) - Cmadot * (2*muc*CX0 + CXu*(CZq + 2*muc)) + Cmq*(CXu*(CZadot-2*muc)-2*muc*CZa) + 2*muc*KY2*(CXa*CZu - CZa*CXu)
D = Cmu*(CXa*(CZq + 2*muc) - CZ0*(CZadot - 2*muc)) - Cma*(2*muc*CX0 + CXu*(CZq+2*muc)) + Cmadot*(CX0*CXu-CZ0*CZu) + Cmq*(CXu*CZa - CZu * CXa)
E = -Cmu*(CX0*CXa + CZ0 * CZa) + Cma*(CX0*CXu+CZ0*CZu)
    
coefficients = [A,B,C,D,E]

eiegenvalues_symmetric_full = np.roots(coefficients)

print(f"Eigenvalues for the full symmetrical equations of motion: {eiegenvalues_symmetric_full}")





    

