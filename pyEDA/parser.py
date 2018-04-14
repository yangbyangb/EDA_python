import re

from . import Circuit
from . import Element


def parse(filename):
    mycircuit = Circuit.Circuit(title="", filename=filename)

    file = open(filename, "r")

    lines = []

    commands = []

    line_number = 0

    while file is not None:
        while True:
            line = file.readline()
            if len(line) == 0:
                break
            line_number = line_number + 1
            line = line.strip().lower()
            if line_number == 1:
                mycircuit.title = line
            elif len(line) == 0:
                continue
            line = plus_line(file, line)

            if line[0] == ".":
                line_elements = line.split()
                if line_elements[0] == ".end":
                    print("End of the netlist file.")
                else:
                    commands.append((line, line_number))
                continue

            lines.append((line, line_number))

    for line, line_number in lines:

        R_pattern = re.match(r'^R.*', line, re.I)
        C_pattern = re.match(r'^C.*', line, re.I)
        L_pattern = re.match(r'^L.*', line, re.I)

        D_pattern = re.match(r'^D.*', line, re.I)
        MOS_pattern = re.match(r'^M.*', line, re.I)

        V_pattern = re.match(r'^V.*', line, re.I)
        I_pattern = re.match(r'^I.*', line, re.I)

        E_pattern = re.match(r'^E.', line, re.I)
        F_pattern = re.match(r'^F.', line, re.I)
        G_pattern = re.match(r'^G.', line, re.I)
        H_pattern = re.match(r'^H.', line, re.I)

        if R_pattern:
            element = parse_resistor(line, mycircuit)
        elif C_pattern:
            element = parse_capacitor(line, mycircuit)
        elif L_pattern:
            element = parse_inductor(line, mycircuit)
        elif D_pattern:
            element = parse_diode(line, mycircuit)
        elif MOS_pattern:
            element = parse_mos(line, mycircuit)
        elif V_pattern:
            element = parse_vsrc(line, mycircuit)
        elif I_pattern:
            element = parse_isrc(line, mycircuit)
        elif E_pattern:
            element = parse_vcvs(line, mycircuit)
        elif F_pattern:
            element = parse_cccs(line, mycircuit)
        elif G_pattern:
            element = parse_vccs(line, mycircuit)
        elif H_pattern:
            element = parse_ccvs(line, mycircuit)
        else:
            pass

    mycircuit += element

    return mycircuit


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


def parse_mos(line, mycircuit, models):

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


def parse_isrc(line, mycircuit):
    line_elements = line.split()
    dc_value = None
    ac_value = None
    n1 = mycircuit.add_node(line_elements[1])
    n2 = mycircuit.add_node(line_elements[2])

    pattern = re.match(
        r'(^I.) (.*) (.*) ([AD]C)?(=)?( ?)([0-9.]*[FPNUMKGT]?)A?(,?)( ?)([0-9.]*$)?', line, re.I)
    #     1     2 n1 3 n2 4       5   6   7                     8   9   10

    if pattern.group(4).lower() == 'dc':
        dc_value = pattern.group(7)
    elif pattern.group(4).lower() == 'ac':
        ac_value = pattern.group(7)

    element = Element.ISrc(name=line_elements[0], n1=n1, n2=n2, dc_value=dc_value, ac_value=ac_value)

    return [element]


def parse_vcvs(line, mycircuit):
    line_elements = line.split()

    n1 = mycircuit.add_node(line_elements[1])
    n2 = mycircuit.add_node(line_elements[2])
    sn1 = mycircuit.add_node(line_elements[3])
    sn2 = mycircuit.add_node(line_elements[4])

    element = Element.ESrc(name=line_elements[0], n1=n1, n2=n2, sn1=sn1, sn2=sn2, value=unit_transform(line_elements[5]))

    return [element]


def parse_ccvs(line, mycircuit):
    line_elements = line.split()

    n1 = mycircuit.add_node(line_elements[1])
    n2 = mycircuit.add_node(line_elements[2])

    element = Element.HSrc(name=line_elements[0], n1=n1, n2=n2, source_name=line_elements[3], value=unit_transform(line_elements[4]))

    return [element]


def parse_vccs(line, mycircuit):
    line_elements = line.split()

    n1 = mycircuit.add_node(line_elements[1])
    n2 = mycircuit.add_node(line_elements[2])
    sn1 = mycircuit.add_node(line_elements[3])
    sn2 = mycircuit.add_node(line_elements[4])

    element = Element.GSrc(name=line_elements[0], n1=n1, n2=n2, sn1=sn1, sn2=sn2, value=unit_transform(line_elements[5]))

    return [element]


def parse_cccs(line, mycircuit):
    line_elements = line.split()

    n1 = mycircuit.add_node(line_elements[1])
    n2 = mycircuit.add_node(line_elements[2])

    element = Element.FSrc(name=line_elements[0], n1=n1, n2=n2, source_name=line_elements[3], value=unit_transform(line_elements[4]))

    return [element]


def unit_transform(str_value):
    unit_dict = {'f': 1e-15, 'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3, 'k': 1e+3, 'meg': 1e+6, 'g': 1e+9, 't': 1e+12}
    str_value = str_value.lower()
    if str_value[-1] in 'fpnumkgt':
        return float(float(str_value[:-1]) * unit_dict[str_value[-1]])
    else:
        return float(str_value)


class ParseError(Exception):

    pass


def plus_line(file, line):

    while True:
        last = file.tell()
        next = file.readline()
        next = next.strip().lower()
        if not next:
            break
        elif next[0] == '+':
            line += ' ' + next[1:]
        else:
            file.seek(last)
            break
    return line
