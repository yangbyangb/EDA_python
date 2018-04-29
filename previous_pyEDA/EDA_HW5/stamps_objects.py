#########################################################################
#       Author: Yang Bo                                                 #
#       Date:   2018.3.31                                               #
#       Descripthon:    This file is aim to achieve EDA homework        #
#                       by Objected-oriented programming                #
#########################################################################

# -*- coding: UTF-8 -*-

import re
import numpy as np
import math

file = open("example_1.txt", "r")
line_number = 0
Unit_dict = {'f': 1e-15, 'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3, 'k': 1e+3, 'meg': 1e+6, 'g': 1e+9, 't': 1e+12}


def unit_transform(value):
    value = value.lower()
    if value[-1] in 'fpnumkgt':
        return float(float(value[:-1]) * Unit_dict[value[-1]])
    else:
        return float(value)


# elements objects


class Resistor:
    index = 1

    def __init__(self, l):
        self.line = l
        self.pattern = re.match(r'(^R.*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)(ohm)?', line, re.I)
        self.name = self.pattern.group(1)
        self.Np = int(self.pattern.group(2))
        self.Nn = int(self.pattern.group(3))
        self.value = unit_transform(self.pattern.group(4))
        self.g = 1 / self.value


class Capacitor:
    index = 1

    def __init__(self, l):
        self.line = l
        self.pattern = re.match(r'(^C.*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)F?', line, re.I)
        self.name = self.pattern.group(1)
        self.Np = int(self.pattern.group(2))
        self.Nn = int(self.pattern.group(3))
        self.value = unit_transform(self.pattern.group(4))


class Inductor:
    index = 1

    def __init__(self, l):
        self.line = l
        self.pattern = re.match(r'(^L.*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)H?', line, re.I)
        self.name = self.pattern.group(1)
        self.Np = int(self.pattern.group(2))
        self.Nn = int(self.pattern.group(3))
        self.value = unit_transform(self.pattern.group(4))


class Diode:
    index = 1

    def __init__(self, l):
        self.line = l
        self.pattern = re.match(r'(^D.*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)', line, re.I)
        self.name = self.pattern.group(1)
        self.Np = int(self.pattern.group(2))
        self.Nn = int(self.pattern.group(3))
        self.value = unit_transform(self.pattern.group(4))


class BJT:
    index = 1

    def __init__(self, l):
        self.line = l
        self.pattern = re.match(r'(^Q.*) (.*) (.*) (.*) (.*)', line, re.I)
        self.name = self.pattern.group(1)
        self.collector = self.pattern.group(2)
        self.base = self.pattern.group(3)
        self.emitter = self.pattern.group(4)
        self.model = self.pattern.group(5)


class MOSFET:
    index = 1

    def __init__(self, l):
        self.line = l
        self.pattern = re.match(
            r'(^M.*) (.*) (.*) (.*) (.*) (.*) ([LW])=([0-9.]*[FPNUMKGT]?) ([LW])=([0-9.]*[FPNUMKGT]?)', line, re.I)
        #     1      2    3    4    5    6    7      8                    9      10
        self.name = self.pattern.group(1)
        self.drain = self.pattern.group(2)
        self.gate = self.pattern.group(3)
        self.source = self.pattern.group(4)
        self.bulk = self.pattern.group(5)
        self.model = self.pattern.group(6)
        # TODO:self.W = ??
        # TODO:self.L = ??


class VoltageSource:
    index = 1

    def __init__(self, l):
        self.line = l
        self.pattern = re.match(r'(^V.) (.*) (.*) ([AD]C)?(=)?( ?)([0-9.]*[FPNUMKGT]?)V?(,?)( ?)([0-9.]*$)?', line, re.I)
                            #     1     2 N+ 3 N- 4       5   6   7                     8   9   10


class PulseVoltageSource:
    index = 1

    def __init__(self, l):
        self.line = l
        self.pattern = re.match(
            r'(^V.*) (.*) (.*) PULSE ([0-9.]*[FPNUMKGT]?) ([0-9.]*[FPNUMKGT]?) ([0-9.]*[FPNUMKGT]?)S? ([0-9.]*[FPNUMKGT]?)S? ([0-9.]*[FPNUMKGT]?)S? ([0-9.]*[FPNUMKGT]?)S? ([0-9.]*[FPNUMKGT]?)S?',
            line, re.I)

        self.name = self.pattern.group(1)
        self.Np = unit_transform(self.pattern.group(2))
        self.Nn = unit_transform(self.pattern.group(3))
        self.voltage_low = unit_transform(self.pattern.group(4))
        self.voltage_high = unit_transform(self.pattern.group(5))
        self.delay = unit_transform(self.pattern.group(6))
        self.rise = unit_transform(self.pattern.group(7))
        self.fall = unit_transform(self.pattern.group(8))
        self.width = unit_transform(self.pattern.group(9))
        self.period = unit_transform(self.pattern.group(10))

    def v(self, t):  # Pulse voltage formula by time(t)
        t %= self.period
        if t <= self.delay:
            return self.voltage_low
        else:
            t -= self.delay
            if t <= self.rise:
                return self.voltage_low + (self.voltage_high - self.voltage_low) / self.rise * t
            else:
                t -= self.rise
                if t <= self.width:
                    return self.voltage_high
                else:
                    t -= self.width
                    if t <= self.fall:
                        return self.voltage_high - (self.voltage_low - self.voltage_high) / self.fall * t
                    else:
                        return self.voltage_low


class CurrentSource:
    index = 1

    def __init__(self, l):
        self.line = l
        self.pattern = re.match(r'(^I.) (.*) (.*) ([AD]C)?(=)?( ?)([0-9.]*[FPNUMKGT]?)A?(,?)( ?)([0-9.]*$)?', line, re.I)


class VCVS:
    index = 1
    def __init__(self, l):
        self.line = l
        self.pattern = re.match(r'(^E.) (.*) (.*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)', line, re.I)


class CCCS:
    index = 1
    def __init__(self, l):
        self.line = l
        self.pattern = re.match(r'(^F.) (.*) (.*) (V.*) ([0-9.]*[FPNUMKGT]?)?', line, re.I)


class VCCS:
    index = 1
    def __init__(self, l):
        self.line = l
        self.pattern = re.match(r'(^G.) (.*) (.*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)(mho)?', line, re.I)


class CCVS:
    index = 1
    def __init__(self, l):
        self.line = l
        self.pattern = re.match(r'(^H.) (.*) (.*) (V.*) ([0-9.]*[FPNUMKGT]?)(ohm)?', line, re.I)


line = file.readline()

while line:
    if not (line_number == 0):  # dismiss the first line, which is always the title line
        if not line[0] == '.':
            # comment
            # TODO:$注释
            comment_pattern = re.match(r'^\*', line, re.M | re.I)  # match comments start with *

            if comment_pattern:
                comment = comment_pattern.group()
                print("\ncomment:\t", line_number, "\t", line[:-1])  # print the content of comment

            first_letter = re.match(r'(^[RCLDQVIEFGH]).*', line, re.I).group()
            if first_letter == 'R':

