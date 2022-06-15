#!/usr/bin/env python3

import sys
from sys import stdout as cout
from math import *
import numpy as np
import matplotlib.pyplot as plt
from config import get_input_parms, loadConfig
from timer import Timer
from P_0T import discount_curve as zc
from HW import HW, hw_evol
import ir as PAR
# -----------------------------------------------------

def usage():
    print("Usage: ./main.py -in input_file [ -- help ] [ -nr nr] [-nt intrvls] [-y years] [-T T] [-gm gamma] [-s sigma]")
    print("        input_file: the input file holding interest rates")
    print("        nr        : log base 2 of the number of MC trajectories")
    print("                    the number of MC trajectories will be 2^exp.")
    print("                    If undefined will default to 10")
    print("        year      : bond option exercise date")
    print("                    defaults to 10")
    print("        T         : bond maturity")
    print("                    defaults to 20")
    print("        gamma     : the gamma paramter of the HW model")
    print("                    defaults to .5")
    print("        sigma     : the vol paramter of the HW model")
    print("                    defaults to .05")
    print("        intrvl    : the number of intervals we are going to measure")
    print("                    defaults to 30")
#-------------


def run(argv):

    parms = get_input_parms(argv)

    try:
        Op = parms["help"]
        usage()
        return
    except KeyError:
        pass

    #inpt  = parms["in"]
    #PAR   = loadConfig(inpt)

    try:
        output = parms["out"]
        fp = open(output, "w")
    except KeyError:
        fp = cout

    try: nr = int(parms["nr"] )
    except KeyError: nr = 10
    #N = (1 << nr)
    N=50000
    try: gamma = float(parms["gm"] )
    except KeyError: gamma = .5

    try: sigma = float(parms["s"] )
    except KeyError: sigma = .05

    try: Yrs= float(parms["y"] )
    except KeyError: Yrs = 10.0

    try: bondMaturity= float(parms["T"] )
    except KeyError: bondMaturity = 20

    try: Nt = int(parms["nt"] )
    except KeyError: Nt = 30

    Dt = Yrs/Nt

    Obj = np.random.RandomState()
    Obj.seed(92823)
    # -------------------------------


    T0 = Timer()
    # build the discount curve
    # consistent with zerco coupon rates given
    # in the input file.
    dc = zc(curve = PAR.curve)
    t  = Dt*np.arange(0, Nt+1, 1, dtype = np.double)
    x  = np.ndarray(shape = ( Nt+1 ), dtype=np.double ) 
    y  = np.ndarray(shape = ( Nt+1 ), dtype=np.double ) 

    P_0T  = np.ndarray(shape = ( Nt+1 ), dtype=np.double ) 
    for n in range(Nt+1):
       P_0T[n] = dc.P_0t( n*Dt)        #come sempre questa è la discount  curve di pag.37

    # the HW model
    hw = HW(gamma=gamma, sigma=sigma)

    # The integral of the Phi function
    i_phi = hw.IntPhi( dc, Dt, Nt)
    # ------------------------------------------------------------------------------

    T    = bondMaturity

    T0.start()
    res     = hw_evol( Obj, hw, Dt, Nt, N)     #avvio evoluzione MC
    t_end   = T0.stop()
    fp.write("@ elapsed %8.4f sec.\n" %(t_end))

    print(" %6s  %8s +/- %8s  %8s" %("t_m", "P_tT", "Err", "P_0t(T)" ) )
    for n in range(Nt+1):
        # 'X' and 'Int X ' on the last time step
        tm      = n*Dt
        X       = res[0][n]
        f       = res[1][n]
        df      = exp(i_phi[n])*np.exp(-f)      #discount factor dalla simulazione di MC

        #  compute the value of the bond in tm = Years
        P_tT  = hw.BondPrice( tm, T, dc, X)
        P_tT  = df*P_tT
        P2_tT = np.add.reduce( P_tT * P_tT, 0)/N
        P_tT  = np.add.reduce( P_tT, 0)/N
        Err   = 3*np.sqrt( np.maximum( P2_tT - P_tT*P_tT, 0.0)/N )
        x[n]  = P_tT
        y[n]  = Err

        print(" %6.3f  %8.4f +/- %8.4f  %8.4f" %(n*Dt, P_tT, 2*Err, dc.P_0t(T) ) )


    plt.errorbar(t, x, yerr=y, fmt='o', color='g', label="MC", ms=4)
    
    Cte = dc.P_0t(T)
    vCte = np.full(shape = Nt+1, fill_value=Cte, dtype=np.double)
    plt.plot( t, vCte, color='r', label="P(0,T)")

    plt.ylim(top=Cte*1.01, bottom=Cte*.99)
    plt.title("$E[\, D(0,t_m)\,P(t_m, T)\,]$  T=%5.2f  $\gamma$=%4.2f  $\sigma$=%5.2f  $2^{%d}$" %(T, gamma, sigma, nr))
    plt.xlabel("$t_m$")
    plt.ylabel("P_0t")
    plt.legend(loc="best")
    plt.savefig('hw_martingale.eps', format='eps', dpi=9600)

    plt.show()
    
# -------------------------------


if __name__ == "__main__":
    run(sys.argv)
    
