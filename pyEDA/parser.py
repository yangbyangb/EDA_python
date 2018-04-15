import re

from Element import HSrc
import Circuit
import Element


def parse(filename):
    mycircuit = Circuit.Circuit(title="", filename=filename)
    file = open(filename, "r")
    lines = []
    line_number = 0
    elements = []

    if file is not None:
        while True:
            line = file.readline()
            line_number = line_number + 1
            line = line.strip().lower()
            if line_number == 1:
                mycircuit.title = line
            elif len(line) == 0:
                break
            line = plus_line(file, line)

            if line[0] == '.':
                line_elements = line.lower().split()
                if line_elements[0] == ".end":
                    print("End of the netlist file.")
                elif line_elements[0] == ".op":
                    mycircuit.op = True
                elif line_elements[0] == ".dc":
                    mycircuit.dc = True
                    mycircuit.dc_source = line_elements[1]
                    mycircuit.dc_start = line_elements[2]
                    mycircuit.dc_stop = line_elements[3]
                    mycircuit.dc_point_number = line_elements[4]
                    # TODO:mycircuit.dc_type = line_elements[]
                elif line_elements[0] == ".ac":
                    mycircuit.ac = True
                    mycircuit.ac_type = line_elements[1]
                    mycircuit.ac_point_number = line_elements[2]
                    mycircuit.ac_start = line_elements[3]
                    mycircuit.ac_stop = line_elements[4]
                elif line_elements[0] == ".tran":
                    mycircuit.tran = True
                    mycircuit.tran_start = 0
                    mycircuit.tran_step = line_elements[1]
                    mycircuit.tran_stop = line_elements[2]
                else:
                    pass

            lines.append((line, line_number))

    for line, line_number in lines:

        r_pattern = re.match(r'^R.*', line, re.I)
        c_pattern = re.match(r'^C.*', line, re.I)
        l_pattern = re.match(r'^L.*', line, re.I)

        d_pattern = re.match(r'^D.*', line, re.I)
        mos_pattern = re.match(r'^M.*', line, re.I)

        v_pattern = re.match(r'^V.*', line, re.I)
        v_pulse_pattern = re.match(r'(^V.*) (.*) (.*) PULSE (.*) (.*) (.*) (.*) (.*) (.*) (.*)', line, re.I)
        i_pattern = re.match(r'^I.*', line, re.I)

        e_pattern = re.match(r'^E.', line, re.I)
        f_pattern = re.match(r'^F.', line, re.I)
        g_pattern = re.match(r'^G.', line, re.I)
        h_pattern = re.match(r'^H.', line, re.I)

        if r_pattern:
            element = parse_resistor(line, mycircuit)
        elif c_pattern:
            element = parse_capacitor(line, mycircuit)
        elif l_pattern:
            element = parse_inductor(line, mycircuit)
        elif d_pattern:
            element = parse_diode(line, mycircuit)
        elif mos_pattern:
            element = parse_mos(line, mycircuit)
        elif v_pattern:
            element = parse_vsrc(line, mycircuit)
        elif v_pulse_pattern:
            element = parse_v_pulse_src(line, mycircuit)
        elif i_pattern:
            element = parse_isrc(line, mycircuit)
        elif e_pattern:
            element = parse_vcvs(line, mycircuit)
        elif f_pattern:
            element = parse_cccs(line, mycircuit)
        elif g_pattern:
            element = parse_vccs(line, mycircuit)
        elif h_pattern:
            element = parse_ccvs(line, mycircuit)
        else:
            element = None

        if element:
            elements += [element]

    return mycircuit, elements


def parse_resistor(line, mycircuit):

    line_elements = line.split()

    n1 = mycircuit.add_node(line_elements[1])
    n2 = mycircuit.add_node(line_elements[2])

    value = unit_transform(line_elements[3])

    element = Element.Resistor(name=line_elements[0], n1=n1, n2=n2, value=value)

    return [element]


def parse_capacitor(line, mycircuit):

    line_elements = line.split()

    n1 = mycircuit.add_node(line_elements[1])
    n2 = mycircuit.add_node(line_elements[2])

    value = unit_transform(line_elements[3])

    element = Element.Capacitor(name=line_elements[0], n1=n1, n2=n2, value=value)

    return [element]


def parse_inductor(line, mycircuit):

    line_elements = line.split()

    n1 = mycircuit.add_node(line_elements[1])
    n2 = mycircuit.add_node(line_elements[2])

    value = unit_transform(line_elements[3])

    element = Element.Inductor(name=line_elements[0], n1=n1, n2=n2, value=value)

    return [element]


def parse_diode(line, mycircuit, models=None):

    line_elements = line.split()

    n1 = mycircuit.add_node(line_elements[1])
    n2 = mycircuit.add_node(line_elements[2])

    model_label = line_elements[3]

    element = Element.diode(name=line_elements[0], n1=n1, n2=n2, model=models[model_label])

    return [element]


def parse_mos(line, mycircuit, models=None):

    line_elements = line.split()
    nd = mycircuit.add_node(line_elements[1])
    ng = mycircuit.add_node(line_elements[2])
    ns = mycircuit.add_node(line_elements[3])
    nb = mycircuit.add_node(line_elements[4])
    model_label = line_elements[5]

    w = None
    l = None

    pattern = re.match(
        r'(^M.*) (.*) (.*) (.*) (.*) (.*) ([LW])=([0-9.]*[FPNUMKGT]?) ([LW])=([0-9.]*[FPNUMKGT]?)', line, re.I)
    #     1      2    3    4    5    6    7      8                     9      10

    if pattern.group(7).lower() == 'w':
        w = unit_transform(pattern.group(8))
    elif pattern.group(7).lower() == 'l':
        l = unit_transform(pattern.group(8))
    if pattern.group(9).lower() == 'w':
        w = unit_transform(pattern.group(10))
    elif pattern.group(9).lower() == 'l':
        l = unit_transform(pattern.group(10))

    element = Element.mos(line_elements[0], nd, ng, ns, nb, w, l, models[model_label])

    return [element]


def parse_vsrc(line, mycircuit):
    line_elements = line.split()
    dc_value = None
    ac_value = None

    pattern = re.match(
        r'(^V.*) (.*) (.*) ([AD]C)?(=)?( ?)([0-9.]*[FPNUMKGT]?)V?(,?)( ?)([0-9.]*$)?', line, re.I)
    #     1      2 n1 3 n2 4       5   6   7                     8   9   10
    n1 = mycircuit.add_node(line_elements[1])
    n2 = mycircuit.add_node(line_elements[2])

    if pattern.group(4).lower() == 'dc':
        dc_value = pattern.group(7)
    elif pattern.group(4).lower() == 'ac':
        ac_value = pattern.group(7)

    element = Element.VSrc(name=line_elements[0], n1=n1, n2=n2,
                           dc_value=dc_value, ac_value=ac_value)

    return [element]


def parse_v_pulse_src(line, mycircuit):

    pattern = re.match(r'(^V.*) (.*) (.*) PULSE (.*) (.*) (.*)S? (.*)S? (.*)S? (.*)S? (.*)S?', line, re.I)
                    #    1      2    3          4    5    6      7      8      9      10

    name = pattern.group(1)
    n1 = mycircuit.add_node(pattern.group(2))
    n2 = mycircuit.add_node(pattern.group(3))
    voltage_low = unit_transform(pattern.group(4))
    voltage_high = unit_transform(pattern.group(5))
    delay = unit_transform(pattern.group(6))
    rise = unit_transform(pattern.group(7))
    fall = unit_transform(pattern.group(8))
    width = unit_transform(pattern.group(9))
    period = unit_transform(pattern.group(10))

    element = Element.VPulseSrc(name=name, n1=n1, n2=n2,
                                voltage_low=voltage_low, voltage_high=voltage_high,
                                delay=delay, rise=rise, fall=fall, width=width, period=period)

    return [element]


def parse_isrc(line, mycircuit):
    line_elements = line.split()
    dc_value = None
    ac_value = None
    n1 = mycircuit.add_node(line_elements[1])
    n2 = mycircuit.add_node(line_elements[2])

    pattern = re.match(
        r'(^I.) (.*) (.*) ([AD]C)?(=)?( ?)([0-9.]*[FPNUMKGT]?)A?(,?)( ?)([0-9.]*$)?', line, re.I)
    #     1     2 n1 3 n2 4       5   6   7                     8   9   10

    if pattern.group(4):
        if pattern.group(4).lower() == 'dc':
            dc_value = unit_transform(pattern.group(7))
        elif pattern.group(4).lower() == 'ac':
            ac_value = unit_transform(pattern.group(7))
    else:
        dc_value = unit_transform(pattern.group(7))

    element = Element.ISrc(name=line_elements[0], n1=n1, n2=n2, dc_value=dc_value, ac_value=ac_value)

    return [element]


def parse_vcvs(line, mycircuit):
    line_elements = line.split()

    n1 = mycircuit.add_node(line_elements[1])
    n2 = mycircuit.add_node(line_elements[2])
    nc1 = mycircuit.add_node(line_elements[3])
    nc2 = mycircuit.add_node(line_elements[4])

    element = Element.ESrc(name=line_elements[0], n1=n1, n2=n2, nc1=nc1, nc2=nc2,
                           value=unit_transform(line_elements[5]))

    return [element]


def parse_ccvs(line, mycircuit):
    line_elements = line.split()

    n1 = mycircuit.add_node(line_elements[1])
    n2 = mycircuit.add_node(line_elements[2])

    element = Element.HSrc(name=line_elements[0], n1=n1, n2=n2, source_name=line_elements[3],
                           value=unit_transform(line_elements[4]))  # type: HSrc

    return [element]


def parse_vccs(line, mycircuit):
    line_elements = line.split()

    n1 = mycircuit.add_node(line_elements[1])
    n2 = mycircuit.add_node(line_elements[2])
    nc1 = mycircuit.add_node(line_elements[3])
    nc2 = mycircuit.add_node(line_elements[4])

    element = Element.GSrc(name=line_elements[0], n1=n1, n2=n2, nc1=nc1, nc2=nc2,
                           value=unit_transform(line_elements[5]))

    return [element]


def parse_cccs(line, mycircuit):
    line_elements = line.split()

    n1 = mycircuit.add_node(line_elements[1])
    n2 = mycircuit.add_node(line_elements[2])

    element = Element.FSrc(name=line_elements[0], n1=n1, n2=n2, source_name=line_elements[3],
                           value=unit_transform(line_elements[4]))

    return [element]


def unit_transform(str_value):
    unit_dict = {'f': 1e-15, 'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3, 'k': 1e+3, 'meg': 1e+6, 'g': 1e+9, 't': 1e+12}
    str_value = str_value.lower()
    if str_value[-1] in 'fpnumkgt':
        return float(float(str_value[:-1]) * unit_dict[str_value[-1]])
    else:
        return float(str_value)


def plus_line(file, line):

    while True:
        last = file.tell()
        next_line = file.readline()
        next_line = next_line.strip().lower()
        if not next_line:
            break
        elif next_line[0] == '+':
            line += ' ' + next_line[1:]
        else:
            file.seek(last)
            break
    return line
