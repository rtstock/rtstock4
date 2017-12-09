
#import pandas as pd

#import config
#import os
#import mytools

    
    
def test():
    try:
        import sys
        #import imp
        #ret = imp.find_module('os')
        #import numpy
        ret = list(sys.modules)
        #if 'numpy' in sys.modules:
        #    ret = 'success connect'
        #else:
        #    ret = 'no numpy'
    except (RuntimeError, TypeError, NameError):
        ret = 'My error was caught: ' + str(NameError)
    return ret

print test()
