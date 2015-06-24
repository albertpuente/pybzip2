'''
Timer decorator.
'''

import time

def timeit(method):
    """Wraps a function and prints how many seconds it took to finish
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print(method.__name__, "took", te - ts, "s")
        return result

    return timed