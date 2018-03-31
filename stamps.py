import re
import numpy as np
import math

file = open("example_1.txt", "r")
line_number = 0
Unit_dict = {'f': 1e-15, 'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3, 'k': 1e+3, 'meg': 1e+6, 'g': 1e+9, 't': 1e+12}


def unit_transform(value):
    value = value.lower()
    if value[-1] in 'fpnumkgt':
        return int(value[:-1] * Unit_dict[value[-1]])
    else:
        return int(value)


line = file.readline()

i = 0  # 记录节点个数
R_index = 0  # 记录器件个数
C_index = 0
L_index = 0
E_index = 0
G_index = 0
F_index = 0
H_index = 0
V_index = 0
I_index = 0
AC_index = 0
TRAN_index = 0
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
            V_pattern = re.match(
                r'(^V.) (.*) (.*) ([AD]C)?(=)?( ?)([0-9.]*[FPNUMKGT]?)V?(,?)( ?)([0-9.]*$)?', line, re.I)
            #     1     2 N+ 3 N- 4       5   6   7                     8   9   10
            I_pattern = re.match(
                r'(^I.) (.*) (.*) ([AD]C)?(=)?( ?)([0-9.]*[FPNUMKGT]?)A?(,?)( ?)([0-9.]*$)?', line, re.I)
            G_pattern = re.match(r'(^G.) (.*) (.*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)(mho)?', line, re.I)
            E_pattern = re.match(r'(^E.) (.*) (.*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)', line, re.I)
            F_pattern = re.match(r'(^F.) (.*) (.*) (V.*) ([0-9.]*[FPNUMKGT]?)?', line, re.I)
            H_pattern = re.match(r'(^H.) (.*) (.*) (V.*) ([0-9.]*[FPNUMKGT]?)(ohm)?', line, re.I)

            if R_pattern:
                R_Np = int(R_pattern.group(2))  # Np
                R_Nn = int(R_pattern.group(3))  # Nn
                i = max(i, R_Np, R_Nn)
                R_Value = unit_transform(R_pattern.group(4))  # Value
                tmp_array = ([R_Np, R_Nn, R_Value])
                if R_index >= 1:
                    R_array = np.row_stack((R_array, tmp_array))
                else:
                    R_array = tmp_array
                R_index += 1
            elif C_pattern:
                C_Np = int(C_pattern.group(2))  # Np
                C_Nn = int(C_pattern.group(3))  # Nn
                i = max(i, C_Np, C_Nn)
                C_Value = unit_transform(C_pattern.group(4))  # Value
                tmp_array = ([C_Np, C_Nn, C_Value])
                if C_index >= 1:
                    C_array = np.row_stack((C_array, tmp_array))
                else:
                    C_array = tmp_array
                C_index += 1
            elif L_pattern:
                L_Np = int(L_pattern.group(2))  # Np
                L_Nn = int(L_pattern.group(3))  # Nn
                i = max(i, L_Np, L_Nn)
                L_Value = unit_transform(L_pattern.group(4))  # Value
                tmp_array = ([L_Np, L_Nn, L_Value])
                if L_index >= 1:
                    L_array = np.row_stack((L_array, tmp_array))
                else:
                    L_array = tmp_array
                L_index += 1
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
            elif V_pattern:
                V_Name = V_pattern.group(1)
                V_Np = int(V_pattern.group(2))
                V_Nn = int(V_pattern.group(3))
                if V_pattern.group(4):
                    print(V_pattern.group(4), "Value:\t", V_pattern.group(7))
                V_value = unit_transform(V_pattern.group(7))
                if V_pattern.group(10):
                    print("AC Phase:\t", V_pattern.group(10))
                    V_value = unit_transform(V_pattern.group(10))
                tmp_array = [V_Np, V_Nn, V_value, V_Name]
                if V_index >= 1:
                    V_array = np.row_stack((V_array, tmp_array))
                else:
                    V_array = tmp_array
                V_index += 1
            elif I_pattern:
                I_Name = I_pattern.group(1)
                I_Np = int(I_pattern.group(2))
                I_Nn = int(I_pattern.group(3))
                if I_pattern.group(4):
                    print(I_pattern.group(4), "Value:\t", I_pattern.group(7))
                I_value = unit_transform(I_pattern.group(7))
                if I_pattern.group(10):
                    print("AC Phase:\t", I_pattern.group(10))
                    I_value = unit_transform(I_pattern.group(10))
                tmp_array = [I_Np, I_Nn, I_value]
                if I_index >= 1:
                    I_array = np.row_stack((I_array, tmp_array))
                else:
                    I_array = tmp_array
                I_index += 1
            elif E_pattern:
                E_Np = int(E_pattern.group(2))
                E_Nn = int(E_pattern.group(3))
                E_NC1 = int(E_pattern.group(4))
                E_NC2 = int(E_pattern.group(5))
                i = max(i, E_Np, E_Nn, E_NC1, E_NC2)
                E_Value = unit_transform(E_pattern.group(6))
                tmp_array = [E_Np, E_Nn, E_NC1, E_NC2, E_Value]
                if E_index >= 1:
                    E_array = np.row_stack((E_array, tmp_array))
                else:
                    E_array = tmp_array
                E_index += 1
            elif G_pattern:
                G_Np = int(G_pattern.group(2))
                G_Nn = int(G_pattern.group(3))
                G_NC1 = int(G_pattern.group(4))
                G_NC2 = int(G_pattern.group(5))
                i = max(i, G_Np, G_Nn, G_NC1, G_NC2)
                G_Value = unit_transform(G_pattern.group(6))
                tmp_array = [G_Np, G_Nn, G_NC1, G_NC2, G_Value]
                if G_index >= 1:
                    G_array = np.row_stack((G_array, tmp_array))
                else:
                    G_array = tmp_array
                G_index += 1
            elif F_pattern:
                F_Np = int(F_pattern.group(2))
                F_Nn = int(F_pattern.group(3))
                F_V_Name = F_pattern.group(4)
                F_Value = unit_transform(F_pattern.group(5))
                i = max(i, F_Np, F_Nn)
                tmp_array = [F_Np, F_Nn, F_Value, F_V_Name]
                if F_index >= 1:
                    F_array = np.row_stack((F_array, tmp_array))
                else:
                    F_array = tmp_array
                F_index += 1
            elif H_pattern:
                H_Np = int(H_pattern.group(2))
                H_Nn = int(H_pattern.group(3))
                H_V_Name = H_pattern.group(4)
                H_Value = unit_transform(H_pattern.group(5))
                i = max(i, H_Np, H_Nn)
                tmp_array = [H_Np, H_Nn, H_Value, H_V_Name]
                if H_index >= 1:
                    H_array = np.row_stack((H_array, tmp_array))
                else:
                    H_array = tmp_array
                H_index += 1
        else:
            # command
            simulation_pattern = re.match(r'^(.[dat](\w*)) (.)*', line, re.I)  # 匹配仿真模式
            PARAM_pattern = re.match(r'.PARAM (.*)=(.*)', line, re.I)
            DC_pattern = re.match(r'.DC (.*) (.*)[VA]? (.*)[VA]? (.*)', line, re.I)
            AC_pattern = re.match(r'.AC (.*) (.*) ([0-9.]*[FPNUMKGT]?)(Hz)? ([0-9.]*[FPNUMKGT]?)(Hz)?', line, re.I)
            TRAN_pattern = re.match(r'.tran ([0-9.]*[FPNUMKGT]?)S? ([0-9.]*[FPNUMKGT]?)S?', line, re.I)
            OP_pattern = re.match(r'.op(eration?)', line, re.I)
            # TODO:
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
                print("Type:\t", AC_pattern.group(1),
                      "\nStep:\t", AC_pattern.group(2),
                      "\nStart:\t", AC_pattern.group(3),
                      "\nStop:\t", AC_pattern.group(5), )
                AC_index = 1
            if OP_pattern:
                print("DC operationg point")
            if TRAN_pattern:
                print("Step:\t", TRAN_pattern.group(1),
                      "\nStop:\t", TRAN_pattern.group(2))
            if END_pattern:
                print("\nEnd of the Netlist File.")

    line_number = line_number + 1
    line = file.readline()

# Stamp
# dc
MNA_DC = np.zeros([i, i])  # 初始化i*i矩阵
V = np.zeros([i, 1])
RHS = np.zeros([i, 1])

if R_index >= 1:
    for index in range(R_index):
        if R_index > 1:
            R_array_row = R_array[index]  # 取R矩阵的一行
        else:
            R_array_row = R_array
        R_Np = R_array_row[0]
        R_Nn = R_array_row[1]
        R_Value_G = 1 / R_array_row[2]
        if R_Np > 0:
            MNA_DC[R_Np-1, R_Np-1] += R_Value_G
        if (R_Np > 0) & (R_Nn > 0):
            MNA_DC[R_Nn-1, R_Np-1] -= R_Value_G
            MNA_DC[R_Np-1, R_Nn-1] -= R_Value_G
        if R_Nn > 0:
            MNA_DC[R_Nn-1, R_Nn-1] += R_Value_G
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
            MNA_DC[G_Np-1, G_NCp-1] += G_Value
        if (G_Nn > 0) & (G_NCn > 0):
            MNA_DC[G_Nn-1, G_NCn-1] += G_Value
        if (G_Np > 0) & (G_NCn > 0):
            MNA_DC[G_Np-1, G_NCn-1] -= G_Value
        if (G_Nn > 0) & (G_NCp > 0):
            MNA_DC[G_Nn-1, G_NCp-1] -= G_Value
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
            RHS[I_Np-1] = -I_Value
        if I_Nn > 0:
            RHS[I_Nn-1] = I_Value
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
        MNA_DC = np.row_stack(MNA_DC, np.zeros(i))  # 添加分支行
        RHS = np.row_stack(RHS, [V_value])
        V = np.row_stack(V, np.zeros(1))
        MNA_DC = np.column_stack(MNA_DC, np.zeros(i + 1).T)  # 添加分支列
        if V_Np > 0:
            MNA_DC[i, V_Np] = 1
            MNA_DC[V_Np, i] = 1
        if V_Nn > 0:
            MNA_DC[i, V_Nn] = 1
            MNA_DC[V_Nn, i] = 1
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
        MNA_DC = np.row_stack(MNA_DC, np.zeros(i))  # 添加分支行
        RHS = np.row_stack(RHS, [E_Value])
        V = np.row_stack(V, np.zeros(1))
        MNA_DC = np.column_stack(MNA_DC, np.zeros(i + 1).T)  # 添加分支列
        if E_Np > 0:
            MNA_DC[i, E_Np] = 1
            MNA_DC[E_Np, i] = 1
            MNA_DC[i, E_Np] = -E_Value
        if E_Nn > 0:
            MNA_DC[i, E_Nn] = 1
            MNA_DC[E_Nn, i] = 1
            MNA_DC[i, E_Nn] = E_Value
        i += 1
if F_index >= 1:
    for index in range(F_array):
        if F_index > 1:
            F_array_row = F_array[index]
        else:
            F_array_row = F_array
        F_Np = F_array[0]
        F_Nn = F_array[1]
        F_Value = F_array[2]
        MNA_DC = np.row_stack(MNA_DC, np.zeros(i))  # 添加分支行
        RHS = np.row_stack(RHS, [F_Value])
        V = np.row_stack(V, np.zeros(1))
        MNA_DC = np.column_stack(MNA_DC, np.zeros(i + 1).T)  # 添加分支列
        for V_Name in V_array[3]:  # 对于第四行元素
            if F_V_Name == V_Name:
                MNA_DC[i, V_array[0]] = 1
                MNA_DC[i, V_array[1]] = -1
                MNA_DC[V_array[0], i] = F_Value
                MNA_DC[V_array[1], i] = -F_Value
                MNA_DC[V_array[0], i] = 1
                MNA_DC[V_array[1], i] = -1
        i += 1
# TODO: Add stamp of H(CCVS)
# if H_index:
#    H_Np = H_array[0]
#    H_Nn = H_array[1]
#    H_Value = H_array[2]
#    MNA_DC = np.row_stack(MNA_DC, np.zeros(i))  # 添加分支行
#    RHS = np.row_stack(RHS, [H_Value])
#    V = np.row_stack(V, np.zeros(1))
#    MNA_DC = np.column_stack(MNA_DC, np.zeros(i + 1).T)  # 添加分支列
#    for V_Name in V_array[3]:  # 对于第四行元素
#        if H_V_Name == V_Name:


# ac
# TODO:随时间t变化
MNA_AC = MNA_DC
if AC_index:
    f = 1  # frequency
    omega = 2 * math.pi * f
    s = 1j * omega
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
                MNA_AC[C_Np, C_Np] += s * C_Value
            if C_Nn > 0:
                MNA_AC[C_Nn, C_Nn] += s * C_Value
            if (C_Np > 0) & (C_Nn > 0):
                MNA_AC[C_Np, C_Nn] -= s * C_Value
                MNA_AC[C_Nn, C_Np] -= s * C_Value
    if L_index >= 1:
        for index in range(L_index):
            if L_index > 1:
                L_array_row = L_array[index]  # 取L矩阵的一行
            else:
                L_array_row = L_array
            L_Np = L_array_row[0]
            L_Nn = L_array_row[1]
            L_Value = L_array_row[2]
            MNA_AC = np.row_stack(MNA_AC, np.zeros(i))  # 添加分支行
            RHS = np.row_stack(RHS, [0])
            V = np.row_stack(V, np.zeros(1))
            MNA_AC = np.column_stack(MNA_AC, np.zeros(i + 1).T)  # 添加分支列
            if L_Np > 0:
                MNA_AC[L_Np, i] = 1
                MNA_AC[i, L_Np] = 1
            if L_Nn > 0:
                MNA_AC[L_Nn, i] = -1
                MNA_AC[i, L_Nn] = -1
            if (L_Np > 0) & (L_Nn > 0):
                MNA_AC[i, i] = -s * L_Value
# tran
# TODO:随时间t变化，定义C的v和L的i
MNA_TRAN = MNA_DC
h = 0.001  # accuracy index
if TRAN_index:
    if C_index >= 1:
        v =
        for index in range(C_index):
            if C_index > 1:
                C_array_row = C_array[index]
            else:
                C_array_row = C_array
            C_Np = C_array_row[0]
            C_Nn = C_array_row[1]
            C_Value = C_array_row[2]
            MNA_TRAN = np.row_stack(MNA_TRAN, np.zeros(i))  # 添加分支行
            RHS = np.row_stack(RHS, [C_Value / h * v])
            V = np.row_stack(V, np.zeros(1))
            MNA_TRAN = np.column_stack(MNA_TRAN, np.zeros(i + 1).T)  # 添加分支列
            if C_Np > 0:
                MNA_TRAN[i, C_Np] = C_Value / h
                MNA_TRAN[C_Np, i] = 1
            if C_Nn > 0:
                MNA_TRAN[i, C_Nn] = -C_Value / h
                MNA_TRAN[C_Nn, i] = -1
            MNA_TRAN[i, i] = -1

V = np.linalg.solve(MNA_DC, RHS)

print("\nMNA_DC =\n", MNA_DC)
print("\nRHS =\n", RHS, '\n')
for index in range(i):
    print("V", index+1, "=", "%.2f" % float(V[index]), "V")  # 保留两位小数
print("\nMNA_AC =\n", MNA_AC)

file.close()
