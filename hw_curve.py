#!/usr/bin/env python3

import sys
from sys import stdout as cout
from math import *
import numpy as np
import matplotlib.pyplot as plt

from timer import Timer
from config import get_input_parms, loadConfig
from P_0T import discount_curve as zc
from HW import HW, hw_evol
# -----------------------------------------------------

def usage():
    print("Usage: ./main.py -in input_file [ -- help ] [ -nr exp] [-y year] [-nt intrvls] [-gm gamma] [-s sigma]")
    print("        input_file: the input file holding interest rates")
    print("        exp       : log base 2 of the number of MC trajectories")
    print("                    the number of MC trajectories will be 2^exp.")
    print("                    If undefined will default to 10")
    print("        gamma     : the gamma paramter of the HW model")
    print("                    defaults to .5")
    print("        sigma     : the vol paramter of the HW model")
    print("                    defaults to .05")
    print("        year      : the number of years of teh simulation")
    print("                    defaults to 10")
    print("        intrvl    : the number of intervals we are going to measure")
    print("                    defaults to 30")
#-------------


def do_task(**keywords):

    # initial values

    curve = keywords["curve"]
    nr    = keywords["nr"]
    fp    = keywords["fp"]
    Yrs    = keywords["Yrs"]
    Nt    = keywords["Nt"]
    gamma = keywords["gamma"]
    sigma = keywords["sigma"]
    T0    = Timer()

    N = (1 << nr)
    Dt = Yrs/Nt

    Obj = np.random.RandomState()
    Obj.seed(92823)
    # -------------------------------


    # build the discount curve
    # consistent with zero coupon rates given
    # in the input file.
    dc = zc(curve = curve)

    P_0T  = np.ndarray(shape = ( Nt+1 ), dtype=np.double ) 
    for n in range(Nt+1):
       P_0T[n] = dc.P_0t( n*Dt)

    # the HW model
    hw = HW(gamma=gamma, sigma=sigma)   #costruisco l'oggetto della classe HW

    # The integral of the Phi function
    i_phi = hw.IntPhi( dc, Dt, Nt)
    # ------------------------------------------------------------------------------

    T0.start()
    res     = hw_evol( Obj, hw, Dt, Nt, N)
    P_tT    = np.add.reduce( np.exp( -res[1] ), 1)/N
    P2_tT   = np.add.reduce( np.exp( -2*res[1] ), 1)/N
    t_end   = T0.stop()
    fp.write("@ elapsed %8.4f sec.\n" %(t_end))

    Err = np.maximum( P2_tT-P_tT*P_tT, 0.0)
    Err = 3.*np.sqrt(Err/N)
    P_tT *= np.exp(i_phi)   #calcolo il discount factor totale

    t = Dt*np.arange(0, Nt+1, 1, dtype = np.double)

    print("%8s  %8s +/- %8s" %("t", "P_0t", "Err"))
    for x,y,z,p in zip(t,P_tT, Err, P_0T):
        print("%8.4f  %8.4f +/- %8.2e   %8.6f" %(x, y, z, p))
    print()

    # plot MC vs discount curve ....
    plt.errorbar(t, P_tT, yerr=Err, fmt='o', color='g', label="MC P(0,T)", ms=4)
    plt.title("HW:P(0, T) $\gamma$=%4.2f   $\sigma$=%5.2f  Mc = $2^{%d}$ " %(gamma, sigma, nr))
    plt.ylim(top=1.2, bottom=.2)
    plt.xlabel("T")
    plt.ylabel("P(0,T)")
    plt.plot( t, P_0T, color='r', label="Input curve")
    plt.legend(loc="best")
    plt.savefig('hw_curve.eps', format='eps', dpi=9600)

    plt.show()
# -------------------------------

def run(argv):

    parms = get_input_parms(argv)

    try:
        Op = parms["help"]
        usage()
        return
    except KeyError:
        pass

    try: nr = int(parms["nr"] )
    except KeyError: nr = 10

    try:
        output = parms["out"]
        fp = open(output, "w")
    except KeyError: fp = cout

    try: Yrs = float(parms["y"] )
    except KeyError: Yrs = 10.

    try: Nt = int(parms["nt"] )
    except KeyError: Nt = 30

    try: gamma = float(parms["gm"] )
    except KeyError: gamma =  .5

    try: sigma = float(parms["s"] )
    except KeyError: sigma = .05

    inpt  = parms["in"]
    PAR   = loadConfig(inpt)

    do_task( fp=fp, nr = nr, Yrs = Yrs, Nt = Nt, curve=PAR.curve, gamma = gamma, sigma = sigma)
# -------------------------------

if __name__ == "__main__":
    run(sys.argv)
