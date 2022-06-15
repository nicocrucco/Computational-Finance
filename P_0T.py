#!/usr/bin/env python3

import sys
from sys import stdout as cout
from scipy.stats import norm
from math import *
import numpy as np
import pandas as pd
from time import time
from stats1 import stats
from config import get_input_parms, loadConfig
from finder import find_pos
# -----------------------------------------------------

class discount_curve:

    def __init__( self, **keywrds):
        curve   = pd.DataFrame( keywrds["curve"] )
        self.tl = curve[0]
        self.rc = curve[1]
        self.pt = np.exp(-self.tl*self.rc)
    # ------------------------------------------

    def f_0t( self, tN ):

        '''
            f_0t := \int_0^t r(s) ds
        '''

        t  = self.tl
        r  = self.rc
        pt = self.pt

        n = find_pos( tN, list(t) )

        if n < 0: return tN*r[0]

        fs = t[n]* r[n]
        if n + 1 == t.size : 
            ft  = (tN-t[n])*r[n]
        else:
            fe = t[n+1]*r[n+1]
            ft =  ( tN - t[n])*(fe-fs)/(t[n+1] - t[n])

        return fs + ft
    #------------------------------------------------

    def rz( self, t): return self.f_0t(t)/t
    def ry( self, t): return exp(self.f_0t(t)/t) - 1.
    def P_0t( self, t): return exp( -self.f_0t(t) )
    # -----------------------------------------------------------------

    def show( self ):

        tl = self.tl
        n  = 0
        print("%3s  %9s  %8s  %8s  %8s" %( "pos", "t", "P_0t", "rc", "ry"))
        for t in tl:
            p  = self.P_0t(t)
            xc = self.rz(t)
            xy = self.ry(t)
            print("%3d  %9.6f  %8.6f  %8.6f  %8.6f" %( n, t, p, xc, xy))
            n += 1
        


# -----------------------------------------------------

def usage():
    print("Usage: $> python3 euro_opt.py [options]")
    print("Options:")
    print("    %-24s: this output" %("--help"))
    print("    %-24s: output file" %("-out"))
    print("    %-24s: input file" %("-in"))
# -----------------------------------------------------


def run(argv):

    output = None
    parms  = get_input_parms(argv)
    print("@ %-12s: %s" %("argv", str(argv)));
    print("@ %-12s: %s" %("parms", str(parms)));

    try:
        Op = parms["help"]
        usage()
        return
    except KeyError:
        pass

    try:
        output = parms["out"]
        fp = open(output, "w")
    except KeyError:
        fp = cout

    inpt = parms["in"]      ## bisogna isnserire un file per forza
    PAR    = loadConfig(inpt)

    dc = discount_curve(curve = PAR.curve)
   ## dc.show()

    D = 1./365.
    W = 1./52.
    M = 1./12.
    Y = 1.
    times = [ 1*D, 2.*D, 3*D, 4.*D, 5.*D, 6*D, 1.*W, 2.*W, 1.*M, 2.*M, 3.*M, 6.*M, 1.*Y, 2.*Y, 5.*Y, 10.*Y, 15.*Y, 20.*Y, 30.*Y]

    n = 0
    fp.write("\n")
    fp.write("%3s  %9s  %8s  %8s  %8s\n" %("n", "t", "P_0t", "r", "ry") )
    for t in times:
        fp.write("%3d  %9.6f  %8.6f  %8.6f  %8.6f\n" %(n, t, dc.P_0t(t), dc.rz(t), dc.ry(t)) )
        n += 1

    print("#-\n")
    dc.show()

   
    if output != None:
        print("@ %-12s: output written to '%s'\n" %("Info", output))
        fp.close()
# --------------------------

if __name__ == "__main__":

    run(sys.argv)
