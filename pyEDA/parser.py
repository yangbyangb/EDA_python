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

            lines += [(line, line_number)]

    for line, line_number in lines:


    mycircuit += element

    return (mycircuit, lines)


def parse_resistor(line, circ):

    line_elements = line.split()
    if len(line_elements) < 4 or (len(line_elements) > 4 and not line_elements[4][0] == "*"):
        raise ParseError("parse_resistor(): malformed line")

    ext_n1 = line_elements[1]
    ext_n2 = line_elements[2]
    n1 = circ.add_node(ext_n1)
    n2 = circ.add_node(ext_n2)

    value = unit_transform(line_elements[3])

    if value == 0:
        raise ParseError("parse_resistor(): ZERO-valued resistors are not allowed.")

    elem = Element.Resistor(part_id=line_elements[0], n1=n1, n2=n2, value=value)

    return [elem]


def parse_capacitor(line, circ):

    line_elements = line.split()
    if len(line_elements) < 4 or \
       (len(line_elements) > 5 and not line_elements[5][0] == "*" and
        not line_elements[4][0] == "*"):
        raise ParseError("parse_capacitor(): malformed line")

    ext_n1 = line_elements[1]
    ext_n2 = line_elements[2]
    n1 = circ.add_node(ext_n1)
    n2 = circ.add_node(ext_n2)

    elem = Element.Capacitor(part_id=line_elements[0], n1=n1, n2=n2,
                             value=unit_transform(line_elements[3]))

    return [elem]


def parse_inductor(line, circ):

    line_elements = line.split()
    if len(line_elements) < 4 or (len(line_elements) > 5 and not line_elements[6][0] == "*"):
        raise ParseError("parse_inductor(): malformed line")

    ext_n1 = line_elements[1]
    ext_n2 = line_elements[2]
    n1 = circ.add_node(ext_n1)
    n2 = circ.add_node(ext_n2)

    elem = Element.Inductor(part_id=line_elements[0], n1=n1, n2=n2,
                            value=unit_transform(line_elements[3]))

    return [elem]




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
