#!/usr/bin/env python3

import sys
from   sys import stdout as cout
from   scipy.stats import norm
from   math   import *
from   Lib.config import get_input_parms

#-------------------
def usage():
    cout.write("Let X a normal RV with mean 'm' and variance s^2\n")
    cout.write("this functions returns P( |X - m| > qs )\n")
    cout.write("and P( |X - m| < qs )\n")
    cout.write("#-\n")
    cout.write("usage:\n")
    cout.write("$> ./norm_cdf.py [-q list] [--help]\n")
    cout.write(" help: this output\n")
    cout.write(" list: list of s values\n")
# --------------------------------------------

def do_task(lx = [1,2,3]):
    xIn = "P( |X - m| > (q s) )"
    xOut= "P( |X - m| < (q s) )"
    cout.write("%8s|%30s, %30s\n" %("q", xIn, xOut))
    for x in lx: 
        val = 2*norm.cdf(-x)
        cout.write("%8.4f|%24.6f%6s, %24.6f%6s\n" %(x, val, "", 1-val, ""))
# ----------------------------------

def run(argv):
    parms = get_input_parms(argv)
    cout.write("argv : %s\n" %(argv))
    cout.write("parms: %s\n" %(parms))

    try:
        if parms["help"]:
            usage()
            return
    except KeyError:
        pass

    try:
        l = parms["q"]
        lx = eval(l)
    except KeyError:
        lx = [1, 1.96, 2, 3]

    cout.write("#--\n")
    do_task(lx=lx)
# ----------------------------------

if __name__ == "__main__":
    run(sys.argv)
