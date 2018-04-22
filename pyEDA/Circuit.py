import Element


class Circuit(list):

    def __init__(self, title, filename=None):
        self.title = title
        self.filename = filename
        self.nodes_dict = {}
        self.gnd = '0'
        self.nodes = 0

        self.op = False

        self.dc = False
        self.dc_start = None
        self.dc_stop = None
        self.dc_point_number = None
        self.dc_source = None
        self.dc_type = None

        self.ac = False
        self.ac_type = None
        self.ac_start = None
        self.ac_stop = None
        self.ac_point_number = None

        self.tran = False
        self.tran_start = None
        self.tran_stop = None
        self.tran_step = None

        self.has_nonlinear = False

    def create_node(self, name):
        index = 0 in self.nodes_dict
        if name not in self.nodes_dict:
            if name == '0':
                node = 0
            else:
                node = int(len(self.nodes_dict) / 2) + (not index)
            self.nodes_dict.update({node: name})
            self.nodes_dict.update({name: node})
        return name

    def add_node(self, name):
        if name not in self.nodes_dict:
            if name == '0':
                node = 0
            else:
                index = 0 in self.nodes_dict
                node = int(len(self.nodes_dict) / 2) + (not index)
            self.nodes_dict.update({node: name})
            self.nodes_dict.update({name: node})
        else:
            node = self.nodes_dict[name]
        return node

    def add_resistor(self, name, n1, n2, value):
        n1 = self.add_node(n1)
        n2 = self.add_node(n2)
        element = Element.Resistor(name=name, n1=n1, n2=n2, value=value)
        self.append(element)

    def add_capacitor(self, name, n1, n2, value, ic=None):
        n1 = self.add_node(n1)
        n2 = self.add_node(n2)
        element = Element.Capacitor(name=name, n1=n1, n2=n2, value=value, ic=ic)
        self.append(element)

    def add_inductor(self, name, n1, n2, value, ic=None):
        n1 = self.add_node(n1)
        n2 = self.add_node(n2)
        element = Element.Inductor(name=name, n1=n1, n2=n2, value=value, ic=ic)
        self.append(element)

    def add_diode(self, name, n1, n2, model_label, models=None, area=None, ic=None, off=False):
        n1 = self.add_node(n1)
        n2 = self.add_node(n2)
        if models is None:
            models = self.models
        element = Element.diode(name=name, n1=n1, n2=n2, model=models[
            model_label], area=area, ic=ic, off=off)
        self.append(element)

    def add_mos(self, name, nd, ng, ns, nb, type, w, l):
        nd = self.add_node(nd)
        ng = self.add_node(ng)
        ns = self.add_node(ns)
        nb = self.add_node(nb)
        element = Element.mos(name=name, nd=nd, ng=ng, ns=ns, nb=nb, type=type, w=w, l=l)
        self.append(element)

    def add_vsrc(self, name, n1, n2, dc_value, abs_ac=0, arg_ac=0):
        n1 = self.add_node(n1)
        n2 = self.add_node(n2)
        element = Element.VSrc(name=name, n1=n1, n2=n2, dc_value=dc_value, abs_ac=abs_ac, arg_ac=arg_ac)
        self.append(element)

    def add_v_pulse_src(self, name, n1, n2, voltage_low, voltage_high, delay, rise, fall, width, period):
        n1 = self.add_node(n1)
        n2 = self.add_node(n2)
        element = Element.VPulseSrc(name=name, n1=n1, n2=n2,
                                    voltage_low=voltage_low, voltage_high=voltage_high,
                                    delay=delay, rise=rise, fall=fall, width=width, period=period)
        self.append(element)

    def add_isrc(self, name, n1, n2, dc_value, ac_value=0):
        n1 = self.add_node(n1)
        n2 = self.add_node(n2)
        element = Element.ISrc(name=name, n1=n1, n2=n2, dc_value=dc_value, ac_value=ac_value)
        self.append(element)

    def add_cccs(self, name, n1, n2, source_name, value):
        n1 = self.add_node(n1)
        n2 = self.add_node(n2)
        element = Element.FSrc(name=name, n1=n1, n2=n2, source_name=source_name, value=value)
        self.append(element)

    def add_ccvs(self, name, n1, n2, source_name, value):
        n1 = self.add_node(n1)
        n2 = self.add_node(n2)
        element = Element.HSrc(name=name, n1=n1, n2=n2, source_name=source_name, value=value)
        self.append(element)

    def add_vcvs(self, name, n1, n2, sn1, sn2, value):
        n1 = self.add_node(n1)
        n2 = self.add_node(n2)
        sn1 = self.add_node(sn1)
        sn2 = self.add_node(sn2)
        element = Element.ESrc(name=name, n1=n1, n2=n2, sn1=sn1, sn2=sn2, value=value)
        self.append(element)

    def add_vccs(self, name, n1, n2, sn1, sn2, value):
        n1 = self.add_node(n1)
        n2 = self.add_node(n2)
        sn1 = self.add_node(sn1)
        sn2 = self.add_node(sn2)
        element = Element.GSrc(name=name, n1=n1, n2=n2, sn1=sn1, sn2=sn2, value=value)
        self.append(element)

    def get_nodes_number(self):
        return int(len(self.nodes_dict) / 2)

    def is_nonlinear(self):
        for elem in self:
            if elem.is_nonlinear:
                return True
        return False
