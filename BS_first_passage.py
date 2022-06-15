
from math import *
from scipy.stats import norm

def first_passage( So, t, r, sigma, Bl):

    '''
    Return the probability that S(t) has gone below Bl, at least
    once before t. Let tau this first passage time, we do actually 
    compute Pr( tau < t )
    '''

    if t < 1.e-03: return 0.0
    mu = r - .5*sigma*sigma
    Xl = log(Bl/So)
    res =  1. - ( norm.cdf( (mu*t-Xl)/sqrt(sigma*sigma*t) ) - exp( 2*Xl*mu/(sigma*sigma) )*norm.cdf((mu*t+Xl)/sqrt(sigma*sigma*t)) )
    return res

