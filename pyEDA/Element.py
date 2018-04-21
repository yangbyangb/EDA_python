import numpy as np


class Element(object):

    def __init__(self, name=None, n1=None, n2=None,
                 is_nonlinear=False, is_symbolic=True,
                 value=None, branch_number4tran=None, is_v_pulse=False):
        self.name = name
        self.n1 = n1
        self.n2 = n2
        self.value = value

        self.branch_number4tran = branch_number4tran
        self.is_v_pulse = is_v_pulse

        self.is_nonlinear = is_nonlinear
        self.is_symbolic = is_symbolic


class Resistor(Element):

    def __init__(self, name, n1, n2, value):
        self.name = name
        self.n1 = n1
        self.n2 = n2
        self.value = value
        self.g = 1.0 / value

        self.is_nonlinear = False
        self.is_symbolic = True


class Capacitor(Element):

    def __init__(self, name, n1, n2, value, ic=None):
        self.name = name
        self.n1 = n1
        self.n2 = n2
        self.value = value
        self.ic = ic

        self.is_nonlinear = False
        self.is_symbolic = True


class Inductor(Element):

    def __init__(self, name, n1, n2, value, ic=None):
        self.name = name
        self.n1 = n1
        self.n2 = n2
        self.value = value
        self.ic = ic

        self.is_nonlinear = False
        self.is_symbolic = True


class diode(Element):

    def __init__(self, name, n1, n2, model, area=None, ic=None, off=False):
        self.name = name
        self.n1 = n1
        self.n2 = n2
        self.model = model
        self.area = area
        self.ic = ic

        self.is_nonlinear = True
        self.is_symbolic = True


class mos(Element):
    def __init__(self, name, nd, ng, ns, nb, type, w, l):
        self.name = name
        self.nd = nd
        self.ng = ng
        self.ns = ns
        self.nb = nb
        self.type = type  # n/p
        self.w = w
        self.l = l

        self.is_nonlinear = True
        self.is_symbolic = True


class VSrc(Element):

    def __init__(self, name, n1, n2, dc_value, ac_value=0):
        self.name = name
        self.dc_value = dc_value
        self.n1 = n1
        self.n2 = n2
        self.abs_ac = np.abs(ac_value) if ac_value else None
        self.arg_ac = np.angle(ac_value) if ac_value else None
        self.is_nonlinear = False
        self.is_symbolic = True
        self.is_v_pulse = True


class VPulseSrc(Element):

    def __init__(self, name, n1, n2, voltage_low, voltage_high, delay, rise, fall, width, period):
        self.name = name
        self.n1 = n1
        self.n2 = n2
        self.voltage_low = voltage_low
        self.voltage_high = voltage_high
        self.delay = delay
        self.rise = rise
        self.fall = fall
        self.width = width
        self.period = period


class ISrc(Element):

    def __init__(self, name, n1, n2, dc_value=None, ac_value=0):
        self.name = name
        self.dc_value = dc_value
        self.abs_ac = np.abs(ac_value) if ac_value else None
        self.arg_ac = np.angle(ac_value) if ac_value else None
        self.n1 = n1
        self.n2 = n2
        self.is_nonlinear = False
        self.is_symbolic = True


class ESrc(Element):

    def __init__(self, name, n1, n2, value, nc1, nc2):
        self.name = name
        self.n1 = n1
        self.n2 = n2
        self.value = value
        self.nc1 = nc1
        self.nc2 = nc2
        self.is_nonlinear = False
        self.is_symbolic = True


class FSrc(Element):

    def __init__(self, name, n1, n2, value, source_name):
        self.name = name
        self.n1 = n1
        self.n2 = n2
        self.source_name = source_name
        self.alpha = value
        self.is_nonlinear = False
        self.is_symbolic = True


class GSrc(Element):

    def __init__(self, name, n1, n2, value, nc1, nc2):
        self.name = name
        self.n1 = n1
        self.n2 = n2
        self.value = value
        self.nc1 = nc1
        self.nc2 = nc2
        self.is_nonlinear = False
        self.is_symbolic = True


class HSrc(Element):

    def __init__(self, name, n1, n2, value, source_name):
        self.name = name
        self.n1 = n1
        self.n2 = n2
        self.alpha = value
        self.source_name = source_name
        self.is_nonlinear = False
        self.is_symbolic = True
