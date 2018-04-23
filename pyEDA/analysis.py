import numpy as np
import math

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
        if mycircuit.has_nonlinear:
            result += [diode_iter(mycircuit=mycircuit, elements=elements,
                                  dc_sweep_source=source, dc_sweep_v_value=dc_sweep_v_value)]
        else:
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

    if omega.all():
        for omg in omega:
            s = 1j * omg
            mna, rhs = stamp.stamp(mycircuit=mycircuit, elements=elements, s=s, ac=True)
            result += [op(mna=mna, rhs=rhs)]

    return result


def tran(mycircuit, elements, start, stop, step):
    result = []
    previous_result = []
    t = 0
    show_t = []

    while True:
        show_t += [t]

        vpulse_cur_value = None
        for element in elements:
            element = element[0]
            if element.is_v_pulse:
                vpulse_cur_value = v_pulse_tran(t, element)

        if t == 0:
            mna, rhs = stamp.stamp(mycircuit=mycircuit, elements=elements, t=t, vpulse_cur_value=vpulse_cur_value)
            previous_result = op(mna, rhs)
            if t >= start:
                result += [previous_result]
            else:
                pass
        elif t <= stop:
            mna, rhs = stamp.stamp(mycircuit=mycircuit, elements=elements, vpulse_cur_value=vpulse_cur_value,
                                   t=t, v_t_minus_h=previous_result, i_t_minus_h=previous_result)
            previous_result = op(mna, rhs)
            if t >= start:
                result += [previous_result]
            else:
                pass
        else:
            break

        t += step

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


def diode_iter(mycircuit, elements,
               dc_sweep_source=None, dc_sweep_v_value=None,
               ac=False, s=None,
               tran=False, vpulse_cur_value=None, t=0, v_t_minus_h=None, i_t_minus_h=None):
    node_num = mycircuit.get_nodes_number()
    result = np.zeros(node_num)
    for element in elements:
        element = element[0]
        name = element.name.lower()
        if name:
            if name[0] == 'd':
                result[element.n1] = 1
    pre_result = 1
    cur_result = 0
    delta = 1e-12
    VD = 0
    ID = 0

    while True:
        if abs(pre_result - cur_result) < delta:
            break

        pre_result = cur_result

        for element in elements:
            element = element[0]
            name = element.name.lower()
            if name:
                if name[0] == 'd':
                    VD = result[element.n1] - result[element.n2]
                    ID = math.exp(40 * np.real(VD)) - 1

        mna, rhs = stamp.stamp(mycircuit=mycircuit, elements=elements,
                               ID=ID, VD=VD,
                               dc_sweep_source=dc_sweep_source, dc_sweep_v_value=dc_sweep_v_value,
                               ac=ac, s=s,
                               tran=tran, vpulse_cur_value=vpulse_cur_value,
                               t=t, v_t_minus_h=v_t_minus_h, i_t_minus_h=i_t_minus_h)
        result = op(mna, rhs)

        cur_result = ID

    return result


def log_sweep(start, stop, point_number):
    x = 10 ** (np.linspace(np.log10(start), np.log10(stop), point_number))
    return x


def lin_sweep(start, stop, point_number):
    x = np.linspace(start, stop, point_number, endpoint=True)
    return x
