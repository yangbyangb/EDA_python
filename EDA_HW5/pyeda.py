# -*- coding: UTF-8 -*-

import re
import numpy as np
import math
import matplotlib.pyplot as plt
import pylab
from ahkab import ahkab, circuit, time_functions

file = open("example_3.txt", "r")
mycircuit = circuit.Circuit(title="Example circuit", filename=None)
gnd = mycircuit.get_ground_node()
line_number = 0
Unit_dict = {'f': 1e-15, 'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3, 'k': 1e+3, 'meg': 1e+6, 'g': 1e+9, 't': 1e+12}


def unit_transform(value):
    value = value.lower()
    if value[-1] in 'fpnumkgt':
        return float(float(value[:-1]) * Unit_dict[value[-1]])
    else:
        return float(value)


def get_complex_magnitude(complex):
    magnitude = (np.real(complex) ** 2) + (np.imag(complex) ** 2)
    return magnitude


def dc_simulation(MNA, RHS):
    i = MNA.shape[0]
    if R_index >= 1:
        for index in range(R_index):
            if R_index > 1:
                R_array_row = R_array[index]  # 取R矩阵的一行
            else:
                R_array_row = R_array
            R_Np = int(R_array_row[0])
            R_Nn = int(R_array_row[1])
            R_Value_G = 1 / complex(R_array_row[2])
            if R_Np > 0:
                MNA[R_Np - 1, R_Np - 1] += R_Value_G
            if (R_Np > 0) & (R_Nn > 0):
                MNA[R_Nn - 1, R_Np - 1] -= R_Value_G
                MNA[R_Np - 1, R_Nn - 1] -= R_Value_G
            if R_Nn > 0:
                MNA[R_Nn - 1, R_Nn - 1] += R_Value_G
    if G_index >= 1:
        for index in range(G_index):
            if G_index > 1:
                G_array_row = G_array[index]
            else:
                G_array_row = G_array
            G_Np = G_array_row[0]
            G_Nn = G_array_row[1]
            G_NCp = G_array_row[2]
            G_NCn = G_array_row[3]
            G_Value = G_array_row[4]
            if (G_Np > 0) & (G_NCp > 0):
                MNA[G_Np - 1, G_NCp - 1] += G_Value
            if (G_Nn > 0) & (G_NCn > 0):
                MNA[G_Nn - 1, G_NCn - 1] += G_Value
            if (G_Np > 0) & (G_NCn > 0):
                MNA[G_Np - 1, G_NCn - 1] -= G_Value
            if (G_Nn > 0) & (G_NCp > 0):
                MNA[G_Nn - 1, G_NCp - 1] -= G_Value
    if I_index >= 1:
        for index in range(I_index):
            if I_index > 1:
                I_array_row = I_array[index]
            else:
                I_array_row = I_array
            I_Np = I_array_row[0]
            I_Nn = I_array_row[1]
            I_Value = I_array_row[2]
            if I_Np > 0:
                RHS[I_Np - 1] = -I_Value
            if I_Nn > 0:
                RHS[I_Nn - 1] = I_Value
    if V_index >= 1:
        for index in range(V_index):
            if V_index > 1:
                V_array_row = V_array[index]
            else:
                V_array_row = V_array
            V_Np = V_array_row[0]
            V_Nn = V_array_row[1]
            V_value = V_array_row[2]
            V_Name = V_array_row[3]
            MNA = np.vstack((MNA, np.zeros(i)))  # 添加分支行
            RHS = np.vstack((RHS, [V_value]))
            MNA = np.hstack((MNA, np.zeros(i + 1).T))  # 添加分支列
            if V_Np > 0:
                MNA[i, V_Np - 1] = 1
                MNA[V_Np - 1, i] = 1
            if V_Nn > 0:
                MNA[i, V_Nn - 1] = 1
                MNA[V_Nn - 1, i] = 1
            i += 1
    if E_index >= 1:
        for index in range(E_index):
            if E_index > 1:
                E_array_row = E_array[index]
            else:
                E_array_row = E_array
            E_Np = E_array_row[0]
            E_Nn = E_array_row[1]
            E_NCp = E_array_row[2]
            E_NCn = E_array_row[3]
            E_Value = E_array_row[4]
            MNA = np.vstack((MNA, np.zeros(i)))  # 添加分支行
            RHS = np.vstack((RHS, [E_Value]))
            V = np.vstack((V, np.zeros(1)))
            MNA = np.hstack((MNA, np.zeros(i + 1).T))  # 添加分支列
            if E_Np > 0:
                MNA[i, E_Np - 1] = 1
                MNA[E_Np - 1, i] = 1
                MNA[i, E_Np - 1] = -E_Value
            if E_Nn > 0:
                MNA[i, E_Nn - 1] = 1
                MNA[E_Nn - 1, i] = 1
                MNA[i, E_Nn - 1] = E_Value
            i += 1
    if F_index >= 1:
        for index in range(F_array):
            if F_index > 1:
                F_array_row = F_array[index]
            else:
                F_array_row = F_array
            F_Np = F_array_row[0]
            F_Nn = F_array_row[1]
            F_Value = F_array_row[2]
            MNA = np.vstack((MNA, np.zeros(i)))  # 添加分支行
            RHS = np.vstack((RHS, [F_Value]))
            V = np.vstack((V, np.zeros(1)))
            MNA = np.hstack((MNA, np.zeros(i + 1).T))  # 添加分支列
            for V_Name in V_array[3]:  # 对于第四行元素
                if F_V_Name == V_Name:
                    MNA[i, V_array[0] - 1] = 1
                    MNA[i, V_array[1] - 1] = -1
                    MNA[V_array[0] - 1, i] = F_Value
                    MNA[V_array[1] - 1, i] = -F_Value
                    MNA[V_array[0] - 1, i] = 1
                    MNA[V_array[1] - 1, i] = -1
            i += 1
    # TODO: Add stamp of H(CCVS)

    # return np.linalg.solve(MNA, RHS)


def ac_stamp(MNA, RHS, s):
    row = MNA.shape[0]
    if C_index >= 1:
        for index in range(C_index):
            if C_index > 1:
                C_array_row = C_array[index]  # 取C矩阵的一行
            else:
                C_array_row = C_array
            C_Np = C_array_row[0]
            C_Nn = C_array_row[1]
            C_Value = C_array_row[2]
            if C_Np > 0:
                MNA[C_Np - 1, C_Np - 1] += s * C_Value
            if C_Nn > 0:
                MNA[C_Nn - 1, C_Nn - 1] += s * C_Value
            if (C_Np > 0) & (C_Nn > 0):
                MNA[C_Np - 1, C_Nn - 1] -= s * C_Value
                MNA[C_Nn - 1, C_Np - 1] -= s * C_Value
    if L_index >= 1:
        for index in range(L_index):
            if L_index > 1:
                L_array_row = L_array[index]  # 取L矩阵的一行
            else:
                L_array_row = L_array
            L_Np = L_array_row[0]
            L_Nn = L_array_row[1]
            L_Value = L_array_row[2]
            MNA = np.vstack((MNA, np.zeros(row)))  # 添加分支行
            RHS = np.vstack((RHS, [0]))
            MNA = np.hstack((MNA, np.zeros(row + 1).T))  # 添加分支列
            if L_Np > 0:
                MNA[L_Np - 1, row] = 1
                MNA[row, L_Np - 1] = 1
            if L_Nn > 0:
                MNA[L_Nn - 1, row] = -1
                MNA[row, L_Nn - 1] = -1
            if (L_Np > 0) & (L_Nn > 0):
                MNA[row, row] -= s * L_Value
            row += 1
    # print("MNA_AC:\n", MNA, "\nRHS_AC:\n", RHS)


def ac_simulation(freq, MNA, V, RHS):
    # print("frequency:\t", freq)
    omega = 2 * math.pi * freq
    ss = 1j * omega
    MNA_local = np.zeros((4, 4))
    RHS_local = np.zeros((4, 1))
    # V_AC_Source.v(omega, ss)
    V_result = np.zeros((MNA.shape[0], len(f)))
    for index in range(len(freq)):
        s = ss[index]
        # print("s:\t", s)
        MNA_local = MNA
        RHS_local = RHS
        ac_stamp(MNA_local, RHS_local, s)
        # print("MNA_local:\n", MNA_local)
        # print("RHS_local:\n", RHS_local)
        # V_result[:, [index]] = np.linalg.solve(MNA_local, RHS_local)
        # print(np.linalg.solve(MNA_local, RHS_local))
    # print(V_result)
    # print("V1 magnitude:\n", get_complex_magnitude(V_result[0]), "\nV2 magnitude:\n", get_complex_magnitude(V_result[1]))
    # plt.figure(1)
    # plt.plot(f, get_complex_magnitude(V_result[0]), color="blue", linewidth=1.0, linestyle="-")
    # plt.figure(2)
    # plt.plot(f, get_complex_magnitude(V_result[1]), color="red", linewidth=1.0, linestyle="-")
    # plt.show()


class Resistor:

    def __init__(self, l):
        self.pattern = re.match(r'(^R.*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)(ohm)?', l, re.I)
        self.name = self.pattern.group(1)
#        self.Np = int(self.pattern.group(2))
#        self.Nn = int(self.pattern.group(3))
        self.value = unit_transform(self.pattern.group(4))
        self.value_g = 1 / self.value

    def fill_stamps(self, MNA):
        if self.Np > 0:
            MNA[self.Np - 1, self.Np - 1] += self.value_g
        if (self.Np > 0) & (self.Nn > 0):
            MNA[self.Nn - 1, self.Np - 1] -= self.value_g
            MNA[self.Np - 1, self.Nn - 1] -= self.value_g
        if self.Nn > 0:
            MNA[self.Nn - 1, self.Nn - 1] += self.value_g


class Capacitor:

    def __init__(self, l, C0):
        self.pattern = re.match(r'(^C.*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)(F)?', l, re.I)
        self.name = self.pattern.group(1)
        self.Np = int(self.pattern.group(2))
        self.Nn = int(self.pattern.group(3))
        self.value = unit_transform(self.pattern.group(4)) + C0

    def fill_stamps(self, MNA, s):
        if self.Np > 0:
            MNA[self.Np - 1, self.Np - 1] += s * self.value
        if self.Nn > 0:
            MNA[self.Nn - 1, self.Nn - 1] += s * self.value
        if (self.Np > 0) & (self.Nn > 0):
            MNA[self.Np - 1, self.Nn - 1] -= s * self.value
            MNA[self.Nn - 1, self.Np - 1] -= s * self.value


class Inductor:

    def __init__(self, l, L0):
        self.pattern = re.match(r'(^L.*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)(H)?', l, re.I)
        self.name = self.pattern.group(1)
        self.Np = int(self.pattern.group(2))
        self.Nn = int(self.pattern.group(3))
        self.value = unit_transform(self.pattern.group(4)) + L0

    def fill_stamps(self, MNA, RHS, s):
        row_num = MNA.shape[0]
        MNA = np.vstack((MNA, np.zeros(row_num)))  # 添加分支行
        RHS = np.vstack((RHS, [0]))
        MNA = np.hstack((MNA, np.zeros(row_num + 1).T))  # 添加分支列
        if self.Np > 0:
            MNA[self.Np - 1, row_num] = 1
            MNA[row_num, self.Np - 1] = 1
        if self.Nn > 0:
            MNA[self.Nn - 1, row_num] = -1
            MNA[row_num, self.Nn - 1] = -1
        if (self.Np > 0) & (self.Nn > 0):
            MNA[row_num, row_num] -= s * self.value


class VoltageSource:

    def __init__(self, l):
        self.pattern = re.match(
                r'(^V.*) ([0-9]*) ([0-9]*) ([AD]C)?(=)?( ?)([0-9.]*[FPNUMKGT]?)V?(,?)( ?)([0-9.]*$)?', l, re.I)
            #     1      2 N+     3 N-     4       5   6   7                     8   9   10
        self.name = self.pattern.group(1)
        self.Np = int(self.pattern.group(2))
        self.Nn = int(self.pattern.group(3))
        self.value = unit_transform(self.pattern.group(7))
        if self.pattern.group(4).lower() == 'dc':
            self.type = 0  # dc source
        else:
            self.type = 1  # ac source
        if self.pattern.group(10):
            self.phase = self.pattern.group(10)

    def fill_stamps(self, MNA, RHS, s):
        row_num = MNA.shape[0]
        MNA = np.vstack((MNA, np.zeros(row_num)))  # 添加分支行
        RHS = np.vstack((RHS, [self.value]))
        MNA = np.hstack((MNA, np.zeros(row_num + 1).T))  # 添加分支列
        if self.Np > 0:
            MNA[row_num, self.Np - 1] = 1
            MNA[self.Np - 1, row_num] = 1
        if self.Nn > 0:
            MNA[row_num, self.Nn - 1] = 1
            MNA[self.Nn - 1, row_num] = 1


class ACVoltageSource:

    def __init__(self, magnitude, phase):
        self.magnitude = magnitude
        self.phase = float(phase) / 180.0 * math.pi  # rad

    def v(self, omega0, s):  # s domain
        return self.magnitude * (omega0 * math.cos(self.phase) + s * math.sin(self.phase)) / (s ** 2 + omega0 ** 2)


class ACSimulation:
    index = 1

    def __init__(self, l):
        self.line = l
        self.pattern = re.match(r'.AC (.*) (.*) ([0-9.]*[FPNUMKGT]?)(Hz)? ([0-9.]*[FPNUMKGT]?)(Hz)?', line, re.I)
        self.step = unit_transform(self.pattern.group(2))
        self.start = unit_transform(self.pattern.group(3))
        self.stop = unit_transform(self.pattern.group(5))


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

    def v(self, t):
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


class TranSimulation:
    index = 1

    def __init__(self, l):
        self.line = l
        self.pattern = re.match(r'.tran ([0-9.]*[FPNUMKGT]?)S? ([0-9.]*[FPNUMKGT]?)S?', line, re.I)
        self.step = unit_transform(self.pattern.group(1))
        self.stop = unit_transform(self.pattern.group(2))


line = file.readline()

while line:
    if not (line_number == 0):  # 忽略第一行
        if not line[0] == '.':
            # comment
            comment_pattern = re.match(r'\*', line, re.M | re.I)  # 匹配注释

            if comment_pattern:
                comment = comment_pattern.group()
                print("\ncomment line:\t", line_number, "    ", line[:-1])  # 输出注释行

            # instance
            R_pattern = re.match(r'(^R.*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)(ohm)?', line, re.I)
            C_pattern = re.match(r'(^C.*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)F?', line, re.I)
            L_pattern = re.match(r'(^L.*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)H?', line, re.I)
            # D
            D_pattern = re.match(r'(^D.*) (.*) (.*) (.*)', line, re.I)
            # Q
            Q_pattern = re.match(r'(^Q.*) (.*) (.*) (.*) (.*)', line, re.I)
            # MOS
            MOS_pattern = re.match(
                r'(^M.*) (.*) (.*) (.*) (.*) (.*) ([LW])=([0-9.]*[FPNUMKGT]?) ([LW])=([0-9.]*[FPNUMKGT]?)', line, re.I)
            #     1      2    3    4    5    6    7      8                     9      10
            V_DC_pattern = re.match(
                r'(^V.*) ([0-9]*) ([0-9]*) (DC)?(=?)( ?)([0-9.]*[FPNUMKGT]?)V?(,?)( ?)([0-9.]*$)?', line, re.I)
            #     1      2 N+     3 N-     4    5   6   7                     8   9   10
            V_AC_pattern = re.match(
                r'(^V.*) ([0-9]*) ([0-9]*) (AC)?(=?)( ?)([0-9.]*[FPNUMKGT]?)V?(,?)( ?)([0-9.]*$)?', line, re.I)
            #     1      2 N+     3 N-     4    5   6   7                     8   9   10
            V_PULSE_pattern = re.match(
                r'(^V.*) (.*) (.*) PULSE ([0-9.]*[FPNUMKGT]?) ([0-9.]*[FPNUMKGT]?) ([0-9.]*[FPNUMKGT]?)S? ([0-9.]*[FPNUMKGT]?)S? ([0-9.]*[FPNUMKGT]?)S? ([0-9.]*[FPNUMKGT]?)S? ([0-9.]*[FPNUMKGT]?)S?',
                line, re.I)
            I_AC_pattern = re.match(
                r'(^I.) (.*) (.*) (AC)?(=)?( ?)([0-9.]*[FPNUMKGT]?)A?(,?)( ?)([0-9.]*$)?', line, re.I)
            I_DC_pattern = re.match(
                r'(^I.) (.*) (.*) (DC)?(=)?( ?)([0-9.]*[FPNUMKGT]?)A?(,?)( ?)([0-9.]*$)?', line, re.I)
            G_pattern = re.match(r'(^G.) (.*) (.*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)(mho)?', line, re.I)
            E_pattern = re.match(r'(^E.) (.*) (.*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)', line, re.I)
            F_pattern = re.match(r'(^F.) (.*) (.*) (V.*) ([0-9.]*[FPNUMKGT]?)?', line, re.I)
            H_pattern = re.match(r'(^H.) (.*) (.*) (V.*) ([0-9.]*[FPNUMKGT]?)(ohm)?', line, re.I)

            if R_pattern:
                R_name = R_pattern.group(1)
                R_Np = R_pattern.group(2)  # Np
                R_Nn = R_pattern.group(3)  # Nn
                R_Value = unit_transform(R_pattern.group(4))  # Value
                mycircuit.add_resistor(R_name, n1=R_Np, n2=R_Nn, value=R_Value)
            elif C_pattern:
                C_name = C_pattern.group(1)
                C_Np = C_pattern.group(2)  # Np
                C_Nn = C_pattern.group(3)  # Nn
                C_Value = unit_transform(C_pattern.group(4))  # Value
                mycircuit.add_capacitor(C_name, n1=C_Np, n2=C_Nn, value=C_Value)
            elif L_pattern:
                L_name = L_pattern.group(1)
                L_Np = L_pattern.group(2)  # Np
                L_Nn = L_pattern.group(3)  # Nn
                L_Value = unit_transform(L_pattern.group(4))  # Value
                mycircuit.add_inductor(L_name, n1=L_Np, n2=L_Nn, value=L_Value)
            elif D_pattern:
                print("\nName:\t", D_pattern.group(1),
                      "\nNode1:\t", D_pattern.group(2),
                      "\nNode2:\t", D_pattern.group(3),
                      "\nModel:\t", D_pattern.group(4))
            elif Q_pattern:
                print("\nName:\t", Q_pattern.group(1),
                      "\nCollector:\t", Q_pattern.group(2),
                      "\nBase:\t", Q_pattern.group(3),
                      "\nEmitter:\t", Q_pattern.group(4),
                      "\nModel:\t", Q_pattern.group(5))
            elif MOS_pattern:
                print("\nName:\t", MOS_pattern.group(1),
                      "\nDrain:\t", MOS_pattern.group(2),
                      "\nGate:\t", MOS_pattern.group(3),
                      "\nSource:\t", MOS_pattern.group(4),
                      "\nBulk:\t", MOS_pattern.group(5),
                      "\nModel:\t", MOS_pattern.group(6),
                      "\n", MOS_pattern.group(7), ":\t", MOS_pattern.group(8),
                      "\n", MOS_pattern.group(9), ":\t", MOS_pattern.group(10))
            elif V_DC_pattern:
                V_Name = V_DC_pattern.group(1)
                V_Np = V_DC_pattern.group(2)
                V_Nn = V_DC_pattern.group(3)
                V_value = unit_transform(V_DC_pattern.group(7))
                mycircuit.add_vsource(V_Name, n1=V_Np, n2=V_Nn, dc_value=V_value)
            elif V_AC_pattern:
                V_Name = V_AC_pattern.group(1)
                V_Np = V_AC_pattern.group(2)
                V_Nn = V_AC_pattern.group(3)
                V_value = unit_transform(V_AC_pattern.group(7))
                V_AC_phase = V_AC_pattern.group(10)
                mycircuit.add_vsource(V_Name, n1=V_Np, n2=V_Nn, ac_value=V_value)
            elif V_PULSE_pattern:
                V_PULSE = PulseVoltageSource(line)
                v_pulse = time_functions.pulse(v1=V_PULSE.voltage_low, v2=V_PULSE.voltage_high, td=V_PULSE.delay,
                                               per=V_PULSE.period, tr=V_PULSE.rise, tf=V_PULSE.fall, pw=V_PULSE.width)
                mycircuit.add_vsource(V_PULSE.name, n1=V_PULSE.Np, n2=V_PULSE.Nn, function=v_pulse)
            elif I_DC_pattern:
                I_Name = I_DC_pattern.group(1)
                I_Np = I_DC_pattern.group(2)
                I_Nn = I_DC_pattern.group(3)
                I_value = unit_transform(I_DC_pattern.group(7))
                mycircuit.add_isource(I_Name, n1=I_Np, n2=I_Nn, dc_value=I_value)
            elif I_AC_pattern:
                I_Name = I_AC_pattern.group(1)
                I_Np = I_AC_pattern.group(2)
                I_Nn = I_AC_pattern.group(3)
                I_value = unit_transform(I_AC_pattern.group(7))
                mycircuit.add_isource(I_Name, n1=I_Np, n2=I_Nn, ac_value=I_value)
            elif E_pattern:
                E_name = E_pattern.group(1)
                E_Np = E_pattern.group(2)
                E_Nn = E_pattern.group(3)
                E_NC1 = E_pattern.group(4)
                E_NC2 = E_pattern.group(5)
                E_Value = unit_transform(E_pattern.group(6))
                mycircuit.add_vcvs(E_name, n1=E_Np, n2=E_Nn, sn1=E_NC1, sn2=E_NC2, value=E_Value)
            elif G_pattern:
                G_name = G_pattern.group(1)
                G_Np = G_pattern.group(2)
                G_Nn = G_pattern.group(3)
                G_NC1 = G_pattern.group(4)
                G_NC2 = G_pattern.group(5)
                G_Value = unit_transform(G_pattern.group(6))
                mycircuit.add_vccs(G_name, n1=G_Np, n2=G_Nn, sn1=G_NC1, sn2=G_NC2, value=G_Value)
            elif F_pattern:
                F_name = F_pattern.group(1)
                F_Np = F_pattern.group(2)
                F_Nn = F_pattern.group(3)
                Src_Name = F_pattern.group(4)
                F_Value = unit_transform(F_pattern.group(5))
                mycircuit.add_cccs(F_name, n1=F_Np, n2=F_Nn, source_id=Src_Name, value=F_name)
            elif H_pattern:
                H_name = H_pattern.group(1)
                H_Np = H_pattern.group(2)
                H_Nn = H_pattern.group(3)
                Src_Name = H_pattern.group(4)
                H_Value = unit_transform(H_pattern.group(5))
                mycircuit.add_ccvs(H_name, n1=H_Np, n2=H_Nn, source_id=Src_Name, value=H_Value)
        else:
            # command
            simulation_pattern = re.match(r'^(.[dat](\w*)) (.)*', line, re.I)  # 匹配仿真模式
            PARAM_pattern = re.match(r'.PARAM (.*)=(.*)', line, re.I)
            DC_pattern = re.match(r'.DC (.*) (.*)[VA]? (.*)[VA]? (.*)', line, re.I)
            AC_pattern = re.match(r'.AC (.*) ([0-9.]*) ([0-9.]*[FPNUMKGT]?)(Hz)? ([0-9.]*[FPNUMKGT]?)(Hz)?', line, re.I)
            TRAN_pattern = re.match(r'.tran .*', line, re.I)
            OP_pattern = re.match(r'.op(eration?)', line, re.I)
            # TODO: ADD the following commands:
            # OPTIONS_pattern = re.match(r'', line, re.I)
            # MODEL_pattern = re.match(r'', line, re.I)
            # PRINT_pattern = re.match(r'', line, re.I)
            END_pattern = re.match(r'.END', line, re.I)

            if simulation_pattern:
                print("\nMode:", simulation_pattern.group(1).replace(".", ""))
            if PARAM_pattern:
                print("\nPARAM",
                      "\nName:\t", PARAM_pattern.group(1),
                      "\nValue:\t", PARAM_pattern.group(2))
            if DC_pattern:
                print("Var:\t", DC_pattern.group(1),
                      "\nStart:\t", DC_pattern.group(2),
                      "\nStop:\t", DC_pattern.group(3),
                      "\nStep:\t", DC_pattern.group(4), )
            if AC_pattern:
                ac = ACSimulation(line)
                ac_analysis =
            if OP_pattern:
                print("DC operationg point")
            if TRAN_pattern:
                tran = TranSimulation(line)

            if END_pattern:
                print("\nEnd of the Netlist File.")

    line_number = line_number + 1
    line = file.readline()

op_analysis = ahkab.new_op()

# Stamp
# dc
MNA_DC = np.zeros([i, i], dtype=complex)  # 初始化i*i矩阵
V_DC = np.zeros([i, 1], dtype=complex)
RHS_DC = np.zeros([i, 1], dtype=complex)

# dc_result = dc_simulation(MNA_DC, V_DC, RHS_DC)
# dc_simulation(MNA_DC, V_DC, RHS_DC)
# print("MNA_DC:\n", MNA_DC, "\nRHS_DC\n", RHS_DC, "\nV_DC\n", V_DC)

# ac
MNA_AC = MNA_DC
RHS_AC = RHS_DC
V_AC = V_DC
if ac.index:
    ac_analysis = ahkab.new_ac(start=ac.start, stop=ac.stop, points=ac.step)
    f = np.linspace(ac.start, ac.stop, ac.step, endpoint=True)
    # ac_simulation(f, MNA_AC, V_AC, RHS_AC)

# tran
# TODO:随时间t变化，定义L的i
t = 0
h = 1e-12  # accuracy index
if tran:
    tran_analysis = ahkab.new_tran(tstart=0, tstop=tran.stop, tstep=tran.step)
    q = int(tran.stop / tran.step) + 1
    for index in range(q):
        MNA_TRAN = MNA_DC
        RHS_TRAN = RHS_DC
        V_TRAN = V_DC
        # dc_result = dc_simulation(MNA_TRAN, V_TRAN, RHS_TRAN)
        # dc_simulation(MNA_TRAN, V_TRAN, RHS_TRAN)
        i = MNA_TRAN.shape[0]
        t = tran.step * index
        if C_index >= 1:
#            v = V_PULSE.v(t)
            for index in range(C_index):
                MNA_TRAN = np.vstack((MNA_TRAN, np.zeros(i)))  # 添加分支行
#                RHS = np.vstack((RHS, 0))  # [C_Value / h * V_PULSE.v(t - h)]
#                MNA_TRAN = np.hstack((MNA_TRAN, np.zeros(i + 1).T))  # 添加分支列
                if C_index > 1:
                    C_array_row = C_array[index]
                else:
                    C_array_row = C_array
#                C_Np = int(C_array_row[0])
#                C_Nn = int(C_array_row[1])
                C_Value = C_array_row[2]

#                if C_Np > 0:
#                    MNA_TRAN[i, C_Np - 1] = C_Value / h
#                    MNA_TRAN[C_Np - 1, i] = 1
#                if C_Nn > 0:
#                    MNA_TRAN[i, C_Nn - 1] = -C_Value / h
#                    MNA_TRAN[C_Nn - 1, i] = -1
#                MNA_TRAN[i, i] = -1
#                i += 1
        if L_index >= 1:
            for index in range(L_index):
                if L_index > 1:
                    L_array_row = L_array[index]
                else:
                    L_array_row = L_array
                L_Np = L_array_row[0]
                L_Nn = L_array_row[1]
                L_Value = L_array_row[2]
                MNA_TRAN = np.vstack((MNA_TRAN, np.zeros(i)))  # 添加分支行
#                RHS = np.vstack((RHS, [0]))
#                V = np.vstack((V, np.zeros(1)))
#                MNA_TRAN = np.hstack((MNA_TRAN, np.zeros(i + 1).T))  # 添加分支列
#                if L_Np > 0:
#                    MNA_TRAN[i, L_Np - 1] = 1
#                    MNA_TRAN[L_Np - 1, i] = 1
#                if C_Nn > 0:
#                   MNA_TRAN[i, L_Nn - 1] = -1
#                   MNA_TRAN[L_Nn - 1, i] = -1
#                MNA_TRAN[i, i] = -L_Value / h
#                i += 1

    # print(V_TRAN)
r = ahkab.run(mycircuit, an_list=[op_analysis, ac_analysis, tran_analysis])
# print("\nMNA_DC =\n", MNA_DC)
# print("\nRHS =\n", RHS_DC, '\n')
# for index in range(i):
    # print("V", index + 1, "=", "%.4f" % float(dc_result[index]), "V")  # 保留两位小数
# print("\nMNA_AC =\n", MNA_AC)

fig = pylab.figure()
pylab.subplot(211)
pylab.semilogx(r['ac']['f'], np.abs(r['ac']['Vn4']), 'o-')
pylab.ylabel('abs(V(n4)) [V]')
pylab.title(mycircuit.title + " - AC Simulation")
pylab.subplot(212)
pylab.grid(True)
pylab.semilogx(r['ac']['f'], np.angle(r['ac']['Vn4']), 'o-')
pylab.xlabel('Frequency [Hz]')
pylab.ylabel('arg(V(n4)) [rad]')
fig.savefig('ac_plot.png')

fig = pylab.figure()
pylab.title(mycircuit.title + " - TRAN Simulation")
pylab.plot(r['tran']['T'], r['tran']['VN1'], label="Input voltage")
# pylab.hold(True)
pylab.plot(r['tran']['T'], r['tran']['VN4'], label="output voltage")
pylab.legend()
# pylab.hold(False)
pylab.grid(True)
pylab.ylim([0, 1.2])
pylab.ylabel('Step response')
pylab.xlabel('Time [s]')
fig.savefig('tran_plot.png')
pylab.show()

file.close()
