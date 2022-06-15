from math import *
import numpy as np

def BS_trj(Obj, nt, So, T, J, sigma):

    '''
    Generates J trajectories according to the Black+Scholes model
    Each trajectory is made up of nT equally spaced steps.
    The output matrix will have the geometry S[nt+1][J],
    For each trajectory S[0] will hold the initial value.
    '''
    
    DT = T/nt
    S  = np.ndarray(shape = ( nt+1, J), dtype=np.double)

    X    = Obj.normal( -.5*sigma*sigma*DT, sigma*sqrt(DT), (nt,J))
    S[0] = So

    for n in range(nt):
        S[n+1] = S[n] * np.exp( X[n] )

    return S




