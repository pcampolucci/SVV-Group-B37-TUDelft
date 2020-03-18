"""
Title: Eigenvalue verirication. It will cover the verification of the eigenvalues of the numerical model compared to the approximated models.
       - Short period motion 
       - Phugoid motion
       - Dutch roll
       - Spiral roll 
       - Aperiodic roll

Author: Casper Kanaar
"""

# =============================================================================
# Importing relevant modules
from src.input.parameters_citation import *


# =============================================================================
# Eigenvalue parameters
def dimensionalise_eigenvalue(eigenvalue,chord_or_span,V):
    dimensional_eigenvalue = eigenvalue*(V/chord_or_span)
    return dimensional_eigenvalue


def undamped_natural_frequency(eigenvalue,V,chord_or_span):
    w0 = np.sqrt(np.real(eigenvalue)**2 + np.imag(eigenvalue)**2)*(V/chord_or_span)
    return w0


def damping_ratio(eigenvalue):
    zeta = -np.real(eigenvalue)/np.sqrt(np.real(eigenvalue)**2 + np.imag(eigenvalue)**2)
    return zeta 


def period(w0,zeta):
    P = np.pi*2/(w0*np.sqrt(1-zeta**2))
    return P 


def T05(real_eigenvalue,chord_or_span,V):
    T_05 = np.log(0.5)/real_eigenvalue * (chord_or_span/V)
    return T_05


def eigenvalue_parameters(coefs,chord_or_span):
    eigenvals = np.roots(coefs)
    dimensional_eigenvals = dimensionalise_eigenvalue(eigenvals,chord_or_span,V0)
    
    w0 = undamped_natural_frequency(eigenvals[0],V0,chord_or_span)
    zeta = damping_ratio(eigenvals[0])
    P = period(w0,zeta)
    T_05 = T05(np.real(eigenvals[0]),chord_or_span,V0)
    
    return dimensional_eigenvals, w0, zeta, P, T_05


def undamped_natural_frequency_2(eigenvalue):
    w0 = np.sqrt(np.real(eigenvalue)**2 + np.imag(eigenvalue)**2)
    return w0


def T05_2(real_eigenvalue):
    T_05 = np.log(0.5)/real_eigenvalue 
    return T_05


def eigenvalue_parameters_2(eigenvalue):
    eigenvals = eigenvalue
    
    w0 = undamped_natural_frequency_2(eigenvals)
    zeta = damping_ratio(eigenvals)
    P = period(w0,zeta)
    T_05 = T05_2(np.real(eigenvals))
    
    return eigenvals, w0, zeta, P, T_05


def eigenvalue_parameters_3(eigenvalue):
    eigenvals = eigenvalue 
    
    w0 = undamped_natural_frequency_2(eigenvals)
    zeta = damping_ratio(eigenvals)
    T_05 = T05_2(eigenvals)
    
    return eigenvals, w0, zeta, T_05


# =============================================================================
# Symmetrical reduced EOM
# =============================================================================
def short_period_oscillation_a():
    A = 4*(muc**2)*KY2
    B = -2*muc*(KY2*CZa + Cmadot + Cmq)
    C = CZa*Cmq - 2*muc*Cma
    
    coefs = [A,B,C]
    
    parameters = eigenvalue_parameters(coefs,c)
    
    return parameters


def short_period_oscillation_b():
    A = -2*muc*KY2
    B = Cmadot + Cmq
    C = Cma
    
    coefs = [A,B,C]
    
    parameters = eigenvalue_parameters(coefs,c)
    
    return parameters
    

def phugoid_oscillation_a():
    A = -4*muc**2
    B = 2*muc*CXu
    C = -CZu*CZ0
    
    coefs = [A,B,C]
    
    parameters = eigenvalue_parameters(coefs,c)
    
    return parameters
    
    
def phugoid_oscillation_b():
    A = 2*muc*(CZa*Cmq - 2*muc*Cma)
    B = 2*muc*(CXu*Cma - Cmu*CXa) + Cmq*(CZu*CXa - CXu*CZa)
    C = CZ0*(Cmu*CZa - CZu*Cma)
    
    coefs = [A,B,C]
    
    parameters = eigenvalue_parameters(coefs,c)
    
    return parameters
    

# =============================================================================
# Asymmetrical reduced EOM
def aperiodic_roll():
    eigenvalue_ap_roll = Clp / (4 * mub * KX2)
    
    dimensional_eigenvals = dimensionalise_eigenvalue(eigenvalue_ap_roll,b,V0)
    
    w0 = undamped_natural_frequency(eigenvalue_ap_roll,V0,b)
    zeta = damping_ratio(eigenvalue_ap_roll)
    T_05 = T05(eigenvalue_ap_roll,b,V0)
    
    return dimensional_eigenvals, w0, zeta, T_05
    

def dutch_roll_a():
    A = 8 * mub**2 * KZ2
    B = -2 * mub * (Cnr + 2 * KZ2 * CYb)
    C = 4 * mub * Cnb + CYb * Cnr
    
    coefs = [A,B,C]
    
    eigenvals = np.roots(coefs)
    
    parameters = eigenvalue_parameters(coefs,b)
    
    return parameters
    
   
def dutch_roll_b():
    A = -2 * mub * KZ2
    B = 0.5 * Cnr
    C = - Cnb
    
    coefs = [A,B,C]
    
    eigenvals = np.roots(coefs)
    
    parameters = eigenvalue_parameters(coefs,b)
    
    return parameters


def spiral_motion():
    eigenvalue_spiral_motion = (2 * CL * (Clb*Cnr - Cnb*Clr))/(Clp * (CYb*Cnr + 4*mub*Cnb) - Cnp * (CYb*Clr + 4*mub*Clb))
    
    dimensional_eigenvals = dimensionalise_eigenvalue(eigenvalue_spiral_motion,b,V0)
    
    w0 = undamped_natural_frequency(eigenvalue_spiral_motion,V0,b)
    zeta = damping_ratio(eigenvalue_spiral_motion)
    T_05 = T05(eigenvalue_spiral_motion,b,V0)
    
    return dimensional_eigenvals, w0, zeta, T_05


# =============================================================================
# Error function
def error(analytical,numerical):
    e = (np.abs(numerical-analytical))/((np.abs(analytical+numerical))/2)*100
    return e 
    
# =============================================================================
# Analytical parameters

eigenvalues_short_period_a,w0_short_period_a,damping_ratio_short_period_a, P_short_period_a, T_05_short_period_a = short_period_oscillation_a()

eigenvalues_short_period_b,w0_short_period_b,damping_ratio_short_period_b, P_short_period_b, T_05_short_period_b = short_period_oscillation_b()

eigenvalues_phugoid_a,w0_phugoid_a,damping_ratio_phugoid_a, P_phugoid_a, T_05_phugoid_a = phugoid_oscillation_a()

eigenvalues_phugoid_b,w0_phugoid_b,damping_ratio_phugoid_b, P_phugoid_b, T_05_phugoid_b = phugoid_oscillation_b()

eigenvalues_aperiodic_roll_a,w0_aperiodic_roll_a,damping_aperiodic_roll_a, T_05_aperiodic_roll_a = aperiodic_roll()

eigenvalues_dutchroll_a,w0_dutchroll_a,damping_ratio_dutchroll_a, P_dutchroll_a, T_05_dutchroll_a = dutch_roll_a()

eigenvalues_dutchroll_b,w0_dutchroll_b,damping_ratio_dutchroll_b, P_dutchroll_b, T_05_dutchroll_b = dutch_roll_b()

eigenvalues_spiral_roll_a,w0_spiral_roll_a,damping_spiral_roll, T_05_spiral_roll_a = spiral_motion()

# =============================================================================
# Symmetrical full state equation 
C1_sym = np.array([[-2*muc*c/(V0**2),0,0,0],[0,(CZadot - 2*muc)*(c/V0),0,0],[0,0,-c/V0,0],[0,Cmadot*c/V0,0,-2*muc*KY2*(c**2/V0**2)]])
C2_sym = np.array([[CXu/V0,CXa,CZ0,CXq*c/V0],[CZu/V0,CZa,-CX0,(CZq+2*muc)*(c/V0)],[0,0,0,c/V0],[Cmu/V0,Cma,0,Cmq*c/V0]])

C1_sym_inv = np.linalg.inv(C1_sym)
A_sym = -np.matmul(C1_sym_inv,C2_sym)

eigenvalues_symmetric = np.linalg.eig(A_sym)[0]

eigenvalues_short_period,w0_short_period,damping_ratio_short_period, P_short_period, T_05_short_period = eigenvalue_parameters_2(eigenvalues_symmetric[0])

eigenvalues_phugoid,w0_phugoid,damping_phugoid, P_phugoid, T_05_phugoid = eigenvalue_parameters_2(eigenvalues_symmetric[2])

# =============================================================================
# Asymmetrical full state equation
C1_asym = np.array([[(CYbdot - 2*mub)*(b/V0), 0, 0, 0],[0,-b/(2*V0),0,0],[0,0,-2*mub*KX2*(b**2/V0**2),2*mub*KXZ*(b**2/V0**2)],[Cnbdot*(b/V0),0,2*mub*KXZ*(b**2/V0**2),-2*mub*KZ2*(b**2/V0**2)]])
C2_asym = np.array([[CYb, CL, CYp*b/(2*V0),(CYr - 4*mub)*(b/(2*V0))],[0,0,b/(2*V0),0],[Clb,0,Clp*(b/(2*V0)),Clr*(b/(2*V0))],[Cnb,0,Cnp*(b/(2*V0)),Cnr*(b/(2*V0))]])

C1_asym_inv = np.linalg.inv(C1_asym)
A_asym = -np.matmul(C1_asym_inv,C2_asym)

eigenvalues_asymmetric = np.linalg.eig(A_asym)[0]

eigenvalues_aperiodic_roll, w0_aperiodic_roll, damping_ratio_aperiodic_roll, T_05_aperiodic_roll = eigenvalue_parameters_3(eigenvalues_asymmetric[0])

eigenvalues_dutch_roll,w0_dutch_roll,damping_dutch_roll, P_dutchroll, T_05_dutch_roll= eigenvalue_parameters_2(eigenvalues_asymmetric[1])

eigenvalues_aperiodic_spiral, w0_aperiodic_spiral, damping_ratio_aperiodic_spiral, T_05_aperiodic_spiral = eigenvalue_parameters_3(eigenvalues_asymmetric[3])

# =============================================================================
# Verification, computing the errors.

# Eigenvalues
error_shortperiod_realeigenvalue_a = error(np.real(eigenvalues_short_period_a[0]),np.real(eigenvalues_short_period))
error_shortperiod_imageigenvalue_a = error(np.imag(eigenvalues_short_period_a[0]),np.imag(eigenvalues_short_period))

error_shortperiod_realeigenvalue_b = error(np.real(eigenvalues_short_period_b[0]),np.real(eigenvalues_short_period))
error_shortperiod_imageigenvalue_b = error(np.imag(eigenvalues_short_period_b[0]),np.imag(eigenvalues_short_period))

error_phugoid_realeigenvalue_a = error(np.real(eigenvalues_phugoid_a[0]),np.real(eigenvalues_phugoid))
error_phugoid_imageigenvalue_a = error(np.imag(eigenvalues_phugoid_a[0]),np.imag(eigenvalues_phugoid))

error_phugoid_realeigenvalue_b = error(np.real(eigenvalues_phugoid_b[0]),np.real(eigenvalues_phugoid))
error_phugoid_imageigenvalue_b = error(np.imag(eigenvalues_phugoid_b[0]),np.imag(eigenvalues_phugoid))

error_aperiodic_roll_realeigenvalue = error(eigenvalues_aperiodic_roll_a,eigenvalues_aperiodic_roll)

error_dutchroll_realeigenvalue_a = error(np.real(eigenvalues_dutchroll_a[0]),np.real(eigenvalues_dutch_roll))
error_dutchroll_imageigenvalue_a = error(np.imag(eigenvalues_dutchroll_a[0]),np.imag(eigenvalues_dutch_roll))

error_dutchroll_realeigenvalue_b = error(np.real(eigenvalues_dutchroll_b[0]),np.real(eigenvalues_dutch_roll))
error_dutchroll_imageigenvalue_b = error(np.imag(eigenvalues_dutchroll_b[0]),np.imag(eigenvalues_dutch_roll))
    
error_aperiodic_spiral_realeigenvalue = error(eigenvalues_spiral_roll_a,eigenvalues_aperiodic_spiral)

# Damping ratio 
error_shortperiod_dampingratio_a = error(damping_ratio_short_period_a,damping_ratio_short_period)
error_shortperiod_dampingratio_b = error(damping_ratio_short_period_b,damping_ratio_short_period)

error_phugoid_dampingratio_a= error(damping_ratio_phugoid_a,damping_phugoid)
error_phugoid_dampingratio_b= error(damping_ratio_phugoid_b,damping_phugoid)

error_aperiodic_roll_dampingratio = error(damping_aperiodic_roll_a,damping_ratio_aperiodic_roll)

error_dutchroll_dampingratio_a = error(damping_ratio_dutchroll_a,damping_dutch_roll)
error_dutchroll_dampingratio_b = error(damping_ratio_dutchroll_b,damping_dutch_roll)

error_aperiodic_spiral_damping = error(damping_spiral_roll,damping_ratio_aperiodic_spiral)

# Undamped natural frequency 
error_shortperiod_w0_a = error(w0_short_period_a,w0_short_period)
error_shortperiod_w0_b = error(w0_short_period_b,w0_short_period)

error_phugoid_w0_a = error(w0_phugoid_a,w0_phugoid)
error_phugoid_w0_b = error(w0_phugoid_b,w0_phugoid)

error_aperiodic_roll_w0 = error(w0_aperiodic_roll_a,w0_aperiodic_roll)

error_dutchroll_w0_a = error(w0_dutchroll_a,w0_dutch_roll)
error_dutchroll_w0_b = error(w0_dutchroll_b,w0_dutch_roll)

error_spiral_w0 = error(w0_spiral_roll_a,w0_aperiodic_spiral)

# Period
error_shortperiod_P_a = error(P_short_period_a,P_short_period)
error_shortperiod_P_b = error(P_short_period_b,P_short_period)

error_phugoid_P_a = error(P_phugoid_a,P_phugoid)
error_phugoid_P_b = error(P_phugoid_b,P_phugoid)

error_dutchroll_P_a = error(P_dutchroll_a,P_dutchroll)
error_dutchroll_P_b = error(P_dutchroll_b,P_dutchroll)

# Time to damp out half of the amplitude
error_shortperiod_T_a = error(T_05_short_period_a,T_05_short_period)
error_shortperiod_T_b = error(T_05_short_period_b,T_05_short_period)

error_phugoid_T_a = error(T_05_phugoid_a,T_05_phugoid)
error_phugoid_T_b = error(T_05_phugoid_b,T_05_phugoid)

error_aperiodic_roll_T = error(T_05_aperiodic_roll_a,T_05_aperiodic_roll)

error_dutchroll_T_a = error(T_05_dutchroll_a,T_05_dutch_roll)
error_dutchroll_T_b = error(T_05_dutchroll_b,T_05_dutch_roll)

error_aperiodic_spiral_T = error(T_05_spiral_roll_a,T_05_aperiodic_spiral)













