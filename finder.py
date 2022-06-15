
def __recursive_finder( x, ll, s, e):
    '''
    upon entry this routine, the following constraints must hold:
    ll[s] <= x < ll[e]
    '''
    if (e == s) or ( e == s+1): return s 

    m = int( (e+s)/2 )

    if x <  ll[m]: 
        return __recursive_finder(x, ll, s, m)
    if x == ll[m]: 
        return m
    if x >  ll[m]: 
        return __recursive_finder(x, ll, m, e)
# ------------------------

def find_pos( x, ll):
    if x < ll[0]: return -1
    if x >= ll[-1]: return  len(ll)-1

    return __recursive_finder(x, ll, 0, len(ll) - 1)
