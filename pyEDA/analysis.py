import numpy as np


from . import (Element, Circuit, parser, stamp)


def dc(mna, rhs):
    v = np.linalg.solve(mna, rhs)
    return v


def ac(mna, rhs, mycircuit, sweep_type=None):
    if sweep_type.upper() == 'LOG':

    elif sweep_type.upper() == 'LIN':

    else:
        pass

    mna, rhs = stamp.stamp(mycircuit, ac=True)



def tran():



def log_sweep(start, stop, point_number):
    x = 10 ** (np.linspace(np.log10(stop), np.log10(start), point_number))
    return x

def lin_sweep(start, stop, point_number):
    x = np.linspace(start, stop, point_number, endpoint=True)
    return x
