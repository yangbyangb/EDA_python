import numpy as np


import stamp


def op(mna, rhs):
    result = np.linalg.solve(mna, rhs)
    return result


def dc_sweep(mycircuit, elements, start, stop, point_number, source, sweep_type='LIN'):
    sweep_v = None
    result = []
    if sweep_type:
        if sweep_type.upper() == 'LOG':
            sweep_v = log_sweep(start=start, stop=stop, point_number=point_number)
        elif sweep_type.upper() == 'LIN':
            sweep_v = lin_sweep(start=start, stop=stop, point_number=point_number)
    else:
        sweep_v = lin_sweep(start=start, stop=stop, point_number=point_number)

    for dc_sweep_v_value in sweep_v:
        mna, rhs = stamp.stamp(mycircuit=mycircuit, elements=elements,
                               dc_sweep_source=source, dc_sweep_v_value=dc_sweep_v_value)
        result += [op(mna=mna, rhs=rhs)]

    return result


def ac(mycircuit, elements, start, stop, point_number, sweep_type=None):
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
            mna, rhs = stamp.stamp(mycircuit=mycircuit, elements=elements, s=s, ac=True)
            result += [op(mna=mna, rhs=rhs)]

    return result


def tran(mycircuit, elements, start, stop, step, rhs):
    result = []
    previous_result = []
    t = 0
    point_number = int(stop - start / step + 1)

    for element in elements:
        element = element[0]
        if element.is_v_pulse:
            v_pulse_tran(t, element)

    while True:
        if t == 0:  # ???
            mna, rhs = stamp.stamp(mycircuit=mycircuit, elements=elements)
            previous_result = op(mna, rhs)
            if t >= start:
                result += previous_result
            else:
                pass
        elif t <= stop:
            mna, rhs = stamp.stamp(mycircuit=mycircuit, elements=elements,
                                   v_t_minus_h=previous_result, i_t_minus_h=previous_result)
            previous_result = op(mna, rhs)
            if t >= start:
                result += previous_result
            else:
                pass
        else:
            break

        t += step

    show_t = lin_sweep(start=start, stop=stop, point_number=point_number)
    return show_t, result


def v_pulse_tran(t, element):
    delay = element.delay
    rise = element.rise
    width = element.width
    fall = element.fall
    period = element.period
    low = element.voltage_low
    high = element.voltage_high

    t = t % period

    if t <= delay:
        return low
    elif t <= (delay + rise):
        return (high - low) / rise * (t - delay) + low
    elif t <= (delay + rise + width):
        return high
    elif t <= (delay + rise + width + fall):
        return high - (high - low) / fall * (t - delay - rise - width)
    else:
        return low


def log_sweep(start, stop, point_number):
    x = 10 ** (np.linspace(np.log10(stop), np.log10(start), point_number))
    return x


def lin_sweep(start, stop, point_number):
    x = np.linspace(start, stop, point_number, endpoint=True)
    return x
