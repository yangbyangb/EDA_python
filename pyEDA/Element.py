import numpy as np


class Element(object):

    def __init__(self, part_id=None, n1=None, n2=None, is_nonlinear=False, is_symbolic=True, value=None):
        self.part_id = part_id
        self.n1 = n1
        self.n2 = n2
        self.value = value
        self.is_nonlinear = is_nonlinear
        self.is_symbolic = is_symbolic

    def __str__(self):
        return str(self.value)


class Resistor(Element):

    def __init__(self, part_id, n1, n2, value):
        self.part_id = part_id
        self.n1 = n1
        self.n2 = n2
        self.value = value
        self.g = 1. / value
        self.is_nonlinear = False
        self.is_symbolic = True


class Capacitor(Element):

    def __init__(self, part_id, n1, n2, value):
        self.part_id = part_id
        self.value = value
        self.n1 = n1
        self.n2 = n2
        self.is_nonlinear = False
        self.is_symbolic = True


class Inductor(Element):

    def  __init__(self, part_id, n1, n2, value):
        self.value = value
        self.n1 = n1
        self.n2 = n2
        self.part_id = part_id
        self.is_nonlinear = False
        self.is_symbolic = True


class VSrc(Element):

    def __init__(self, part_id, n1, n2, dc_value, ac_value=0):
        self.part_id = part_id
        self.dc_value = dc_value
        self.n1 = n1
        self.n2 = n2
        self.abs_ac = np.abs(ac_value) if ac_value else None
        self.arg_ac = np.angle(ac_value) if ac_value else None
        self.is_nonlinear = False
        self.is_symbolic = True


class ISrc(Element):

    def __init__(self, part_id, n1, n2, dc_value=None, ac_value=0):
        self.part_id = part_id
        self.dc_value = dc_value
        self.abs_ac = np.abs(ac_value) if ac_value else None
        self.arg_ac = np.angle(ac_value) if ac_value else None
        self.n1 = n1
        self.n2 = n2
        self.is_nonlinear = False
        self.is_symbolic = True


class ESrc(Element):

    def __init__(self, part_id, n1, n2, value, sn1, sn2):
        self.part_id = part_id
        self.n1 = n1
        self.n2 = n2
        self.alpha = value
        self.sn1 = sn1
        self.sn2 = sn2
        self.is_nonlinear = False
        self.is_symbolic = True


class FSrc(Element):

    def __init__(self, part_id, n1, n2, value, source_id):
        self.part_id = part_id
        self.n1 = n1
        self.n2 = n2
        self.source_id = source_id
        self.alpha = value
        self.is_nonlinear = False
        self.is_symbolic = True


class GSrc(Element):

    def __init__(self, part_id, n1, n2, value, sn1, sn2):
        self.part_id = part_id
        self.n1 = n1
        self.n2 = n2
        self.alpha = value
        self.sn1 = sn1
        self.sn2 = sn2
        self.is_nonlinear = False
        self.is_symbolic = True


class HSrc(Element):

    def __init__(self, part_id, n1, n2, value, source_id):
        self.part_id = part_id
        self.n1 = n1
        self.n2 = n2
        self.alpha = value
        self.source_id = source_id
        self.is_nonlinear = False
        self.is_symbolic = True
