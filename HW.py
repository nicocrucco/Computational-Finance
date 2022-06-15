#!/usr/bin/env python3
import scipy
from math import *
from scipy.stats import norm
import numpy as np
from scipy import optimize as op

# -----------------------------------------------------

class HW:

    def __init__(self, **kwargs):
        self.gamma = kwargs["gamma"] 
        self.sigma = kwargs["sigma"] 
    # --------------------


    def show(self):
        print("@ %-12s: %-8s %8.4f" %("Info", "gamma", self.gamma))
        print("@ %-12s: %-8s %8.4f" %("Info", "sigma", self.sigma))
    # --------------------

    def S2_f(self, t):
        g = self.gamma
        s = self.sigma
        h = exp( -g*t)
        return  ( (s*s)/(g*g ) )* ( t - (2/g)*( 1. - h ) + (1./(2*g)) * (1. - h*h ) ) 
    # ---------------------------

    def S2_X(self, t):
        g = self.gamma
        s = self.sigma
        h = exp( -2*g*t)
        return ( (s*s)/( 2 * g ) )* ( 1. - h )
    # ---------------------------

    def cov(self, t):
        if t < 1./(24*60):
            self.sx  = 0.0
            self.sf  = 0.0
            self.rho = 1.0
            return

        g = self.gamma
        s = self.sigma
        h = exp( -g*t)

        sx  = sqrt( self.S2_X(t) )
        sf  = sqrt( self.S2_f(t) )
        C_xf= ( (s*s)/(2.*g*g) ) * ( 1 - h ) * ( 1 - h )

        self.sx  = sx
        self.sf  = sf
        self.rho = C_xf/(sx*sf)
    # ----------------------------------------

    def BondPrice( self, t, T, dc, x):
        g = self.gamma
        b_tT = (1. - exp(-g*(T-t)))/g
        A_tT = (dc.P_0t(T)/dc.P_0t(t))*exp( .5 * ( self.S2_f(t) + self.S2_f(T-t) - self.S2_f(T) ) )
        return A_tT*np.exp(-b_tT*x)      #P(t,T)
    # -----------------------------------

    def Annuity( self, t, tn, Dt, p, dc, x):
        A=0
        #A = np.full( len(x), 0.0, dtype=np.double ) 
        for n in range(p):
            A  += Dt*self.BondPrice( t, tn+(1+n)*Dt, dc, x)
        return A
    # -----------------------------------

    def SwapRate( self, t, tn, Dt, p, dc, x):
        A = self.Annuity(t, tn, Dt, p, dc, x)
        R = self.BondPrice( t, tn, dc, x) - self.BondPrice( t, t+p*Dt, dc, x)
        return R/A, A
    # -----------------------------------

    def IntPhi( self, dc, Dt, N):
        i_phi  = np.ndarray(shape = N+1, dtype=np.double)

        i_phi[0] = 0
        for n in range(N):
            i_phi[n+1] = i_phi[n] + log( dc.P_0t((n+1)*Dt)/dc.P_0t( n*Dt)) - .5*self.S2_f((n+1)*Dt) + .5 * self.S2_f(n*Dt)

        return i_phi
# ----------------------------------------

    def Sigma( self, t, T):
        '''
        Integrals in the interval [t, tm] of the
        square of the time-dependent volatility of the
        zero coupon bond P(t, T)
        '''
        g = self.gamma
        s = self.sigma
        
        return ( (s*s)/(2*g*g*g) ) * pow((1 - exp(-g*(T-t))), 2) *( 1 - exp(- 2*g*t) )  #( (s*s)/(2*g*g*g) ) * pow( (exp(-g*T)- exp(-g*tm)), 2) *( exp( 2*g*t) - 1 )
# ----------------------------------------

    def OptionPrice( self, t, T, Strike, dc):
        '''
        Bond put; 
        the option maturity is 't', the bond expires in T
        '''
        g = self.gamma
        s = self.sigma
        S2 = self.Sigma(t, T)        
        S = sqrt( S2 )        
        P_ts = dc.P_0t(t)   #si considera option maturity (T)
        P_te = dc.P_0t(T)   #si considera bond mat (S)
        F = P_te/Strike*P_ts     # F = Strike*P_ts/P_te            
        if S < 1.e-08:
            if F >= 1.:
                P_an = 1.0
                P_cn = 1.0
            else:
                P_an = 0.0
                P_cn = 0.0
        else:
            Lm = log( F )/(S) + .5*S   #per la put è col meno!!!
            Lp = log( F )/(S) - .5*S    #per la put è col più!!!
            P_an = norm.cdf(Lm)
            P_cn = norm.cdf(Lp)
           
        return  P_te*P_an - Strike*P_ts * P_cn                            #P_ts*Strike*P_cn - P_te*P_an

    def expr(self,x, *args):  
        tn, p , k, dc= args 
        funz=0
        for i in range(1,p):
            funz+=k*self.BondPrice(tn,tn+i,dc,x)
        funz+=(1+k)*self.BondPrice(tn,tn+p,dc,x)
        return funz-1


    def RStar(self, k, tn, p, dc):
        root=op.newton(self.expr, 0.0001, args=(tn,p, k, dc))
        #print("r* value:   ", root)
        prova=0
        for i in range(1,p):
            prova += k*self.BondPrice(tn,tn+i,dc,root)
        prova+=(1+k)*self.BondPrice(tn,tn+p,dc,root)    
        #if prova==1:
        #    print(True)
        #else: 
        #    print(False)
        return root

    def Swaption(self, tn, p, k, dc):
        Value = 0
        c_i= k * 1
        r_star= self.RStar(k, tn, p, dc)
        for i in range(1,p):
            strike = self.BondPrice(tn, tn + i, dc, r_star)
            Value += c_i * self.OptionPrice(tn, tn+i , strike, dc)
        strikef = self.BondPrice(tn, tn + p, dc, r_star) 
        Valuef = Value + (1+k*1) * self.OptionPrice(tn, tn+p, strikef, dc)

        return Valuef, r_star


# -----------------------------------
# End Class HW 
# -----------------------------------

def hw_evol(rand, hw, Dt, L, N):

    '''
    Evolution of the H+W model in the 'bank-account' numeraire
    '''

    hw.cov(Dt)

    xr = rand.normal( loc = 0.0, scale = 1.0, size=(L, N))
    ir = rand.normal( loc = 0.0, scale = 1.0, size=(L, N))

    X  = np.ndarray(shape = ( L+1, N), dtype=np.double )
    Ix = np.ndarray(shape = ( L+1, N), dtype=np.double )

    sx   = hw.sx
    sf   = hw.sf
    rho  = hw.rho
    gamm = hw.gamma
    g    = 1 - exp(-gamm*Dt)

    ir = sf*( rho*xr + sqrt( 1. - rho*rho)*ir )
    xr = sx*xr

    X[0]  = 0.0
    Ix[0] = 0.0

    for n in range(L):
        mx      = - g*(X[n])
        mf      =  (g/gamm)*(X[n])
        X[n+1]  = X[n]  + mx + xr[n]
        Ix[n+1] = Ix[n] + mf + ir[n]

    return X, Ix
# ----------------------------------------

def hw_evol_P_0T(rand, hw, Dt, L, T, N):

    '''
    Evolution of the H+W model in the 'terminal P_(t,T)' numeraire
    This evolution is legal for t <= L Dt.
    '''

    xr = rand.normal( loc = 0.0, scale = 1.0, size=(L, N))
    X  = np.ndarray(shape = ( L+1, N), dtype=np.double )

    sx   = sqrt(hw.S2_X(Dt))
    gamm = hw.gamma
    sgma = hw.sigma
    g    = exp(-gamm*Dt)
    h    = (1. - exp(-gamm*Dt))/gamm
    h2   = (1. - exp(-2*gamm*Dt))/(2*gamm)
    xr   = sx*xr

    X[0]  = 0.0

    for n in range(L):
        mx      = g*X[n] - ((sgma*sgma)/gamm)*(h - exp(-gamm*(T-(n+1)*Dt))*h2)
        X[n+1]  = mx + xr[n]

    return X
# ----------------------------------------
