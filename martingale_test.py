#!/usr/bin/env python3

import sys
from sys import stdout as cout
from math import *
from stats1 import stats
from timer import Timer
from config import get_input_parms
import numpy as np
import matplotlib.pyplot as plt

def mcX(Obj, N, So, T, J, sigma):

    DT = T/N
    S = np.ndarray(shape = ( N+1, J), dtype=np.double)

    X = Obj.normal( -.5*sigma*sigma*DT, sigma*sqrt(DT), (N,J))
    S[0] = So
    for n in range(N):
        S[n+1] = S[n] * np.exp( X[n] )

    cout.write("Iter %d\n" %(S[0].size))
    res = {"t" : np.ndarray(shape = (N+1,), dtype=np.double)
          ,"m" : np.ndarray(shape = (N+1,), dtype=np.double)
          ,"S2": np.ndarray(shape = (N+1,), dtype=np.double)
          }

    for n in range(N+1):
        Sn    = S[n]
        m,s2 = stats(Sn)
        res["t"][n]  = n*DT
        res['m'][n]  = m
        res["S2"][n] = s2*s2

    return res
# -----------------------------------------------------

def martingale_check(**keywrds):

    Obj = np.random.RandomState()
    T0  = Timer();

    fp     = cout
    J      = keywrds["J"]
    N      = keywrds["N"]
    So     = keywrds["So"]
    T      = keywrds["T"]
    sigma  = keywrds["Sigma"]
    Seed   = keywrds["Seed"]

    Obj.seed(Seed)
    St     = np.full(shape = (N+1,), fill_value=So, dtype=np.double)


    ex     = "2^%d" %J
    fp.write("\n")
    fp.write("@ %-12s %8s\n"   %("J", ex))
    fp.write("@ %-12s %8.4f\n" %("So", So))
    fp.write("@ %-12s %8.4f\n" %("T", T))
    fp.write("@ %-12s %8.4f\n" %("sigma", sigma))

    j   = ( 1 << J )
    T0.start()
    res = mcX(Obj, N, So, T, j, sigma)
    t1 = T0.stop()

    fp.write("\n")
    fp.write("%8s  %8s   %8s -- %8s\n" %( "t", "E[S(t)]", "McErr", "ThErr" ))
    for n in range( res["t"].size):
        t = res["t"][n]

        # the theoretica error in 't'.
        ThErr = So*sqrt( (exp( sigma*sigma*t) -1)/j )
        fp.write("%8.4f  %8.4f   %8.4f -- %8.4f\n" %( t, res["m"][n], sqrt(res["S2"][n]/j), ThErr ))

    fp.write("@ Elapsed %.4f sec.\n" %t1);

    err = 3.*np.sqrt( res["S2"]/j)
    lbl = "Mc: E[ S(t) ]"
    
    # the lower value of the y-axis
    Ym  = So*(1. - .3)

    # the highest value of the y-axis
    YM  = So*(1. + .3)

    # spacing between lines
    Dy  =  (YM-Ym)/20.

    Xl  = Dy
    Yl  = YM-Dy

    fig, ax = plt.subplots(1,1, figsize=(8, 6), linewidth=1)
    ax.set_title(r"Martingale test      $\sigma=%.3f, T = %.3f,\;N=2^{%d}$" %(sigma, T, J) )
    ax.set_ylim(Ym, YM)
    ax.errorbar(res["t"], res["m"], yerr=err, fmt='x', color='g', label=lbl)

    ax.plot(res["t"], St, color='r', label="So")
    ax.legend(loc="best")

    plt.show()
# --------------------------

def usage():
    cout.write("Martingale test for BS model\n")
    cout.write("\nusage: ./ln_mc.py [options list]\n\n")
    cout.write("Options\n")
    cout.write(" %-12s: this output\n" %("help"))
    cout.write(" %-12s: log_2 number of trajectories\n" %("-j nr"))
    cout.write(" %-12s  defaults to 10\n" %(""))
    cout.write(" %-12s: number of steps in the trajectory\n" %("-n ns"))
    cout.write(" %-12s  defaults to 12\n" %(""))
    cout.write(" %-12s: length (in years) of the trajectory\n" %("-t T"))
    cout.write(" %-12s  defaults to 1.\n" %(""))
    cout.write(" %-12s: So\n" %("-s So"))
    cout.write(" %-12s  defaults to 1.2\n" %(""))
    cout.write(" %-12s: sigma\n" %("-vol sigma"))
    cout.write(" %-12s  defaults to .2\n" %(""))
    cout.write(" %-12s: seed for random generator\n" %("-seed Seed"))
    cout.write(" %-12s  defaults to 1\n" %(""))
# -------------------------------------------------------------

def run(argv):
    parms = get_input_parms(argv)
    print(f"argv: {argv}")
    print(f"parms: {parms}")

    try:
        if parms["help"]:
            usage()
            return
    except KeyError:
        pass

    Sigma = eval(parms.get("vol", ".20"))

    try: T = eval(parms["t"])
    except KeyError: T = 1.0

    try: So = eval(parms["s"])
    except KeyError: So = 1.2

    try: N = eval(parms["n"])
    except KeyError: N = 12

    try: J = eval(parms["j"])
    except KeyError: J = 12

    try: Seed = eval(parms["seed"])
    except KeyError: Seed = 1

    martingale_check(J=J, N = N, So = So, Seed = Seed, T = T, Sigma = Sigma )
#-------------------------------------------------------

if __name__ == "__main__":
    '''
    Test of the martingale property of the log-normal model
    '''
    run(sys.argv)
