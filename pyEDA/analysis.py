import numpy as np


import stamp


def op(mna, rhs):
    result = np.linalg.solve(mna, rhs)
    return result


def dc_sweep(mycircuit, start, stop, point_number, source, sweep_type='LIN'):
    result = None
    # TODO
    return result


def ac(mycircuit, start, stop, point_number, sweep_type=None):
    omega = None
    result = []
    if sweep_type.upper() == 'LOG':
        omega = 2 * np.pi * log_sweep(start=start, stop=stop, point_number=point_number)  # type: float
    elif sweep_type.upper() == 'LIN':
        omega = 2 * np.pi * lin_sweep(start=start, stop=stop, point_number=point_number)
    else:
        pass

    if omega:
        for omg in omega:
            s = 1j * omg
            mna, rhs = stamp.stamp(mycircuit, s, ac=True)
            result += [op(mna=mna, rhs=rhs)]

    return result


def tran(mycircuit, start, stop, step, IC):
    result = None
    # TODO
    return result


def log_sweep(start, stop, point_number):
    x = 10 ** (np.linspace(np.log10(stop), np.log10(start), point_number))
    return x


def lin_sweep(start, stop, point_number):
    x = np.linspace(start, stop, point_number, endpoint=True)
    return x
