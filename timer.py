# timer.py

import time

class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""

class Timer:

    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        return elapsed_time
    
def named_timer(name):
    
    scale = 1
    fmt   = "sec."
    Tot   = {}
    count = 0

    def middle_funct(f):
        Tot[name] = 0.0
        def inner_funct(*args, **kwargs):
            nonlocal Tot
            nonlocal count
            count += 1
            T0 = time.perf_counter()
            res = f(*args, **kwargs)
            T1 = time.perf_counter()
            #elapsed = "%12.4e %s" %( (T1-T0)*scale, fmt)
            elapsed = (T1-T0)*scale
            Tot[name] += elapsed
            print("@ %-12s: [%3d] executed %-32s  elapsed %12.4f %-4s, Tot %12.4f %-4s" %("Info", count, name, elapsed, fmt, Tot[name], fmt))
            return res
        return inner_funct

    return middle_funct


class FTimer():

    scale = 1.0
    fmt   = "sec."

    def __init__(self, name):
        self.name = name
        self.To = 0.0
        
    def __enter__(self):
        self.To = time.perf_counter()
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = "%12.4e %s" %( (time.perf_counter()- self.To)*self.scale, self.fmt)
        print("@ %-12s: executed %-20s  elapsed %s" %("Info", self.name, elapsed ))
        return False

