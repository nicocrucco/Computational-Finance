#!/usr/bin/env python3

from   math import *
import numpy as np 
import matplotlib.pyplot as plt
from   Lib.stats import stats

def normal_rv(Obj, N, sgma=[1.]):

    c = 0
    array = None
    for s in sgma:
        if c == 0:
            array = Obj.normal( loc=0.0, scale=s, size=N)
            c += 1
        else: array += Obj.normal( loc=0.0, scale=s, size=N)

    return array
# -----------------------------------------------------

def normal_pdf( x, sgma = [1.]):
    S2 = 0;
    for s in sgma: S2 += s*s

    return (1./sqrt(2*np.pi*S2))*np.exp( - x*x/(2*S2) )
#-------------------

    

def run( sgma=(1.,), Ns = [6]):

    M  = 0
    S2 = 0.0
    for s in sgma: S2 += s*s
    print()
    print("Normal Distribution")
    print("@ sgma: %s" %str(sgma))
    print("@ E[ X ] = %8.4f,  E[( X - M)^2] = %8.4f" %(M, S2))

    print("%9s    %8s %10s -- %8s   %8s -- %s " %("N", "E[X]", "E[(X-m)^2]", "|M-E[X]|", "MC-err", "Op"))
    #
    # (1/l) exp(-x/l) < eps
    # x < -(1/l)log( l*eps )
    #
    Eps = 1.e-04
    Xm  = 5*sqrt(S2)

    Dx = 2.*Xm/( 2.e+02 )
    x  = np.arange(-Xm, Xm, Dx)
    y  = normal_pdf(x, sgma=sgma)

    for n in Ns:
        N = ( 1 << n )
        array = normal_rv( Obj, N, sgma=sgma)
        m, s2 = stats( array )
        err  = s2/sqrt(N)
        Op  = ( abs(m-M) < 2.*err )
        print("%9d    %8.4f %10.4f -- %8.4f   %8.4f -- %s " %( N, m, s2, abs(m-M), err, Op))

        if n >= 16:

            plt.hist(array, density=True, facecolor='g', bins=x)
            plt.plot(x, y, color='r')
            plt.show()

if __name__ == "__main__":
    '''
    Checks the convolution laws for normal distributions
    '''

    Obj = np.random.RandomState()
    Obj.seed(92823)

    Ns = [6, 8, 10, 12, 14, 16, 18, 20, 22]
    sgma = [ (5.,), (3.0, 4.0), (sqrt(5.), ), (1., 1., 1., 1., 1.) ]

    for s in sgma:
        run(sgma=s, Ns = Ns)

