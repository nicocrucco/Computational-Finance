from math import *
import numpy as np 

def stats(x):

    '''
    Given the constant array 'x', stats will return the tuple
    ( E[x], StDev(x) := sqrt( E[ (x - E[x])^2 ] ))
    where E, represents the sample average.
    '''
    N = x.size
   
    #
    # We make a copy so to preserve the
    # incoming vector
    #
    y = np.array(x, copy=True)

    #
    # m = 0.0
    # for n in range(y.size): m += y[n]/N
    #
    m = np.sum( y )/N

    #for n in range( y.size ): y [n] -= m
    y -= m

    #
    # var = 0.0
    # for n in range(y.size): var += y[n]*y[n]/N
    #
    var = np.dot( y , y )/N

    return m, sqrt(var)
# ------------------------------------------------

