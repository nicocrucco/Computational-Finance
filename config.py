from importlib.machinery import SourceFileLoader as ldr
from math import *
# ---------------------------

def get_input_parms(args):

    '''
    Parsing of the input line options
    ------

    A line option is something of the form
    -o1 V1 -o2 V2 --o3 -o4 V4 --o5
    where ordering is irrelevant. 
    The function 'get_input_parms',
    when confronted with a line like the one above,
    will return the disctionary
    dict = { "o1": "V1", "o2": "V2", "o3": True, "o4": "V4", "o5": True}

    If some error occurs, the dictionay will hold a key 'err' whose
    value is the detected error.  The user, therefore, will check 
        for an error in the input line checking whether the dict reuturned 
    by 'get_input_parms' holds a key called 'err'. 

    If 'err' happens to be an input key, then, all we can say, is that
    the user is looking for troubles.
    '''

    run_args = {}
    n        = 0

    while 1:
        if n == len(args): break
        key = args[n]

        if n == 0:
            run_args["prog"] = key
        elif key[0:2] == "--": 
            run_args[key[2:]] = True
        elif key[0] == "-":
            n += 1
            if n == len(args):
                run_args["err"] = "Missing value for opt '%s'" %key
                break
            run_args[key[1:]] = args[n]
        else:
            run_args["err"] = "Illegal option '%s'" %key
            break
        n += 1

    return run_args
# ---------------------------------------------

def loadConfig(file):
    '''
    Loads the file 'file' and returns it as a python module
    This is quivalent to 
    #import file as PAR
    I do prefer this because once the code is debugged you can
    modify the content of 'PAR' without touching the code
    '''

    print("@ %-12s: Loading params from: '%s'" %("Info", file ))

    #
    # dynamic loading of the input file
    # we invoke the python interpreter
    #
    PAR = ldr("PAR", file).load_module()
    print("@ %-12s: Loading Done!" %("Info"))
    return PAR

