import sys
from sys import stdout as cout
from scipy.stats import norm
from math import *
import numpy as np
import pandas as pd
from timer import Timer 
#from torch import seed
from stats1 import stats
from config import get_input_parms, loadConfig
from finder import find_pos
from HW import * 
from P_0T import discount_curve as zc
import matplotlib as plt
import ir as PAR

def do_task(**keywords):

    fp = keywords["fp"]
    #Nt = keywords["Nt"]
    #T  = keywords["T"]
    N = keywords["n"]
    p = keywords["p"]
    #Yrs    = keywords["Yrs"]
    seed   = keywords["seed"]
    gamma = keywords["gamma"]
    sigma = keywords["sigma"]
    curve = keywords["curve"]
    tn = keywords["tn"]
    Dt = 1
    Nt=tn+p

    fp.write("@ %-12s: %8.4f\n" %("Gamma", gamma))
    fp.write("@ %-12s: %8.4f\n" %("Sigma", sigma))
    fp.write("@ %-12s: %8.4f\n" %("tn", tn))
    fp.write("@ %-12s: %8.4f\n" %("p", p))
    fp.write("@ %-12s: %8.4f\n" %("Nt", Nt))
    fp.write("@ %-12s: %8d  \n" %("McIter", N))

    Obj = np.random.RandomState()
    Obj.seed(seed)
    # -------------------------------
    #
    # build the discount curve
    # consistent with zero coupon rates given
    # in the input file.
    #
    dc  = zc(curve = curve)
    P_0T  = np.ndarray(shape = ( Nt+1 ), dtype=np.double ) 
    for n in range(Nt+1):
       P_0T[n] = dc.P_0t( n*Dt)
    dscurve= pd.DataFrame(P_0T)
    print("Discount curve: \n",dscurve)  

    #---------------------------------------------   
    # SWAP RATE 
    #---------------------------------------------   

    #t=0
    def a(tn,p):
        a=0
        for i in range(1,p+1):
            a+=dc.P_0t(tn+i)
        return a
    k= (dc.P_0t(tn)-dc.P_0t(tn+p)) / a(tn,p) 
    fp.write("Swap Rate value that makes IRS fair : %8.7f \n" %k)

    ks=[k, k+0.5/100, k-0.5/100, k+1/100, k-1/100, k+5/100, k-5/100]


    #---------------------------------------------
    # ANALYTIC PART                                                    Qua bisogna capire che formula usare per il calcolo analitico
    #---------------------------------------------                
    #the HW model. COSTRUISCO L'OGGETTO DELLA CLASSE HW
    hw = HW(gamma=gamma, sigma=sigma)
    
    # The integral of the Phi function. 
    #i_phi = hw.IntPhi( dc, Dt, Nt)
    fp.write("%6.7s  %14.9s  %10.7s \n"%("k","SW price","r*"))
    for el in ks:
        SW_price, r_star= hw.Swaption(tn, p, el, dc)
        fp.write("%6.7f  %12.7f  %12.7f \n"%(el,SW_price,r_star))



    #---------------------------------------------
    # MONTE CARLO SIMULATION
    #---------------------------------------------
    T0 = Timer();                       #PRIMA PARTE ESERCIZIO 4, BANK ACCOUNT NUMERAIR.

    T0.start()
    X,Ix     = hw_evol( Obj, hw, Dt, p, N)       #matrice L+1 X N 
    i_phi = hw.IntPhi(dc, Dt, Nt)

    t_end   = T0.stop()
    fp.write("\nsimulation time:")
    
    fp.write("@ elapsed %8.4f sec.\n" %(t_end))
    
    Xo   = X[tn]                              #array di N valori per il tempo tn
    f    = Ix[tn]
    df2  = exp(i_phi[tn])*np.exp(-f)

    
    fp.write("\n\n %6.7s  %12.7s +/- %2.7s   %16.7s \n"%("k","BAN","err","N"))

    for el in ks: 
        func=0
        for i in range(1,p):
            P_t= hw.BondPrice( tn, tn+i, dc, Xo)    
            func += el * P_t 
    
        func += (1+el)* hw.BondPrice(tn, tn+p, dc, Xo)
        put   = np.maximum(func - 1.0, 0.0)  # array di valori di payoff
        put   = df2*put 
        #m, S2=stats(put)
        ePut  = np.add.reduce( put * put, 0)/N
        put   = np.add.reduce( put , 0)/N
        ePut  = 3*np.sqrt( np.maximum( ePut - put*put , 0.0)/N )       
        fp.write("%6.7f  %10.7f +/- %8.7f   %8.7s \n"%(el,put,ePut,N))
    
    
   
    #°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°


    To = Timer()                    ## P(t,T) NUMERAIR. SECONDA PARTE ESERCIZIO 4 
    To.start()
    X = hw_evol_P_0T( Obj, hw, Dt, Nt, tn, N)
    t_end = To.stop()
    fp.write("\nsimulation time:")
    fp.write("@ elapsed %8.4f sec.\n" %(t_end))
    #fp.write(" %6s  %8s +/- %8s  %8s\n" %("t_m", "MC", "Err", "PUT") )
    Xo      = X[tn]   
    #P_0t   = dc.P_0t(tn)
    fp.write("\n\n %6.7s  %12.7s +/- %2.7s   %16.7s\n"%("k","P(t,tn)","err","N"))
    T_=[tn, tn+p]
    for el in ks:
        pay=0
        for i in range(1,p):
            P_t= hw.BondPrice( tn, tn+i, dc, Xo)
            pay += el*P_t 
        
        pay += (1+el)*hw.BondPrice(tn, tn+p, dc, Xo) 

        opt1 = dc.P_0t(T_[0])*np.maximum( (pay - 1.0) , 0.0)   ### 
        put1,s1 = stats(opt1)
        err1 = 3*sqrt( s1/N )
        fp.write("%6.7f  %10.7f  +/- %8.7f   %8.7s \n"%(el,put1,err1,N))
    

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°à

    To = Timer()                    ## P(t,T) NUMERAIR. ULTIMA PARTE ESERCIZIO 4 
    To.start()
    X = hw_evol_P_0T( Obj, hw, Dt, Nt, tn+p, N)
    t_end = To.stop()
    fp.write("\nsimulation time:")
    fp.write("@ elapsed %8.4f sec.\n" %(t_end))
    Xo  = X[tn]
    P_tT = hw.BondPrice( tn, tn+p, dc, Xo)
    fp.write("\n\n %6.7s  %12.9s +/- %6.7s   %15.7s\n"%("k","P(t,tn+p)","err","N"))
    for el in ks:
        pay=0
        for i in range(1,p):
            P_t= hw.BondPrice( tn, tn+i, dc, Xo)
            pay += el*P_t 
        
        pay += (1+el)*hw.BondPrice(tn, tn+p, dc, Xo) 
        a=np.maximum( (pay - 1.0) , 0.0)
        opt2 = dc.P_0t(tn+p)* a / P_tT
        put2, sq= stats(opt2)
        err2 = 3*sqrt( sq/N )
        fp.write(" %6.7f  %10.7f +/- %8.7f  %8.7s \n"%(el,put2,err2,N))
    

    #fig, ax = plt.subplots(1,1, figsize=(10, 7.5), linewidth=1)
    #ax.errorbar(t, x, yerr=y, fmt='o', color='r', label="MC put", ms=3)
    #ax.scatter(t, PUT, marker="^", label="put")
    #ax.set_title("$P(0,T) E\\left[\,\\frac{[ P(t_m, T)-k]^+}{P(t_m, T)}\,\\right]$\n $T=%4.1f, \gamma=%4.2f, \sigma=%4.2f, \kappa=%4.2f, N=2^{%d}$" %(T, gamma, sigma, strike, nr))
    #ax.set_ylabel("Option Price")
    #ax.set_xlabel("$t_m$")
    #ax.legend(loc="best")

    #plt.savefig('hw_put.eps', format='eps', dpi=9600)
    #plt.show()

def usage():
    print("Usage: ./main.py [ -- help ] [ -n N] [-tn tn] [-p p] [-gm gamma] [-s sigma] ")
    print("        n        :  N---> number of MC trajectories")
    print("                    If undefined will default to 5000")
    print("        tn       :  Swaption maturity date")
    print("                    defaults to 2")
    print("        p         : final IRS payment")
    print("                    defaults to 20")
    print("        gamma     : the gamma paramter of the HW model")
    print("                    defaults to .5")
    print("        sigma     : the vol paramter of the HW model")
    print("                    defaults to .05")

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
    except KeyError: fp = cout

    try: n = int(parms["n"] )
    except KeyError: n = 5000

    #try: Yrs= float(parms["y"] )
    #except KeyError: Yrs = 10.

    #try: T= float(parms["T"] )
    #except KeyError: T = 20

    try: tn = int(parms["tn"] )
    except KeyError: tn = 2

    try: gamma = float(parms["gm"] )
    except KeyError: gamma = .5

    try: p = float(parms["p"] )
    except KeyError: p = 20

    try: sigma = float(parms["s"] )
    except KeyError: sigma = .05

    #try: strike= float(parms["k"] )
    #except KeyError: strike = .9

    try: seed= float(parms["seed"] )
    except KeyError: seed = 1

    do_task( fp = fp, curve = PAR.curve,  n = n, gamma=gamma, p=p, sigma=sigma, seed = seed, tn=tn)


if __name__ == "__main__":
    run(sys.argv)
    


