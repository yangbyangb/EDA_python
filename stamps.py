import re
import numpy as np

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

i = 0
R_index = 0
C_index = 0
L_index = 0
G_index = 0
I_index = 0
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
                if R_index == 1:
                    R_array = np.row_stack((R_array, tmp_array))
                else:
                    R_array = tmp_array
                    R_index = 1
            elif C_pattern:
                C_Np = int(C_pattern.group(2))  # Np
                C_Nn = int(C_pattern.group(3))  # Nn
                i = max(i, C_Np, C_Nn)
                C_Value = unit_transform(C_pattern.group(4))  # Value
                tmp_array = ([C_Np, C_Nn, C_Value])
                if C_index == 1:
                    C_array = np.row_stack((C_array, tmp_array))
                else:
                    C_array = tmp_array
                    C_index = 1
            elif L_pattern:
                L_Np = int(L_pattern.group(2))  # Np
                L_Nn = int(L_pattern.group(3))  # Nn
                i = max(i, L_Np, L_Nn)
                L_Value = unit_transform(L_pattern.group(4))  # Value
                tmp_array = ([L_Np, L_Nn, L_Value])
                if L_index == 1:
                    L_array = np.row_stack((L_array, tmp_array))
                else:
                    L_array = tmp_array
                    L_index = 1
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
                V_Np = int(V_pattern.group(2))
                V_Nn = int(V_pattern.group(3))
                if V_pattern.group(4):
                    print(V_pattern.group(4), "Value:\t", V_pattern.group(7))
                V_value = unit_transform(V_pattern.group(7))
                if V_pattern.group(10):
                    print("AC Phase:\t", V_pattern.group(10))
                    V_value = unit_transform(V_pattern.group(10))
                tmp_array = [V_Np, V_Nn, V_value]
                if V_index == 1:
                    V_array = np.column_stack((V_array, tmp_array))
                else:
                    V_array = tmp_array
                    V_index = 1
            elif I_pattern:
                I_Np = int(I_pattern.group(2))
                I_Nn = int(I_pattern.group(3))
                if I_pattern.group(4):
                    print(I_pattern.group(4), "Value:\t", I_pattern.group(7))
                I_value = unit_transform(I_pattern.group(7))
                if I_pattern.group(10):
                    print("AC Phase:\t", I_pattern.group(10))
                    I_value = unit_transform(I_pattern.group(10))
                tmp_array = [I_Np, I_Nn, I_value]
                if I_index == 1:
                    I_array = np.column_stack((I_array, tmp_array))
                else:
                    I_array = tmp_array
                    I_index = 1
            elif G_pattern:
                G_Np = int(G_pattern.group(2))
                G_Nn = int(G_pattern.group(3))
                G_NC1 = int(G_pattern.group(4))
                G_NC2 = int(G_pattern.group(5))
                i = max(i, G_Np, G_Nn, G_NC1, G_NC2)
                G_Value = unit_transform(G_pattern.group(6))
                tmp_array = [G_Np, G_Nn, G_NC1, G_NC2, G_Value]
                if G_index == 1:
                    G_array = np.column_stack((G_array, tmp_array))
                else:
                    G_array = tmp_array
                    G_index = 1
            elif F_pattern:
                print("\nName:\t", F_pattern.group(1),
                      "\nN+:\t", F_pattern.group(2),
                      "\nN-:\t", F_pattern.group(3),
                      "\nVname:\t", F_pattern.group(4),
                      "\nValue:\t", F_pattern.group(5))

        else:
            # command
            simulation_pattern = re.match(r'^(.[dat](\w*)) (.)*', line, re.I)  # 匹配仿真模式
            PARAM_pattern = re.match(r'.PARAM (.*)=(.*)', line, re.I)
            DC_pattern = re.match(r'.DC (.*) (.*)[VA]? (.*)[VA]? (.*)', line, re.I)
            AC_pattern = re.match(r'.AC (.*) (.*) ([0-9.]*[FPNUMKGT]?)(Hz)? ([0-9.]*[FPNUMKGT]?)(Hz)?', line, re.I)
            TRAN_pattern = re.match(r'.tran ([0-9.]*[FPNUMKGT]?)S? ([0-9.]*[FPNUMKGT]?)S?', line, re.I)
            OP_pattern = re.match(r'.op(eration?)', line, re.I)
            # TO-DO
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
            if OP_pattern:
                print("DC operationg point")
            if TRAN_pattern:
                print("Step:\t", TRAN_pattern.group(1),
                      "\nStop:\t", TRAN_pattern.group(2))
            if END_pattern:
                print("\nEnd of the Netlist File.")

    line_number = line_number + 1
    line = file.readline()

# print(R_array)
# print(G_array)
# print(I_array)

# 运算
i += 1

R_row_num = R_array.shape[0]  # 矩阵的行数
R_col_num = R_array.shape[1]  # 矩阵的列数

a = np.zeros([i, i])  # i*i矩阵
V = np.zeros([i, 1])
RHS = np.zeros([i, 1])

for index in range(R_row_num):
    R_Np = R_array[index, 0]
    R_Nn = R_array[index, 1]
    R_Value_G = 1 / R_array[index, 2]
    if R_index:
        a[R_Np, R_Np] += R_Value_G
        a[R_Nn, R_Nn] += R_Value_G
        a[R_Np, R_Nn] -= R_Value_G
        a[R_Nn, R_Np] -= R_Value_G

# G_row_num = G_array.shape[0]
# G_col_num = G_array.shape[1]
G_row_num = len(G_array)
# for index in range(G_row_num):
#    Np = G_array[index, 0]
#    Nn = G_array[index, 1]
#    NCp = G_array[index, 2]
#    NCn = G_array[index, 3]
#    Value = G_array[index, 4]
G_Np = G_array[0]
G_Nn = G_array[1]
G_NCp = G_array[2]
G_NCn = G_array[3]
G_Value = G_array[4]
if G_index:
    a[G_Np, G_NCp] += G_Value
    a[G_Nn, G_NCn] += G_Value
    a[G_Np, G_NCn] -= G_Value
    a[G_Nn, G_NCp] -= G_Value

if I_index:
    I_Np = I_array[0]
    I_Nn = I_array[1]
    I_Value = I_array[2]
    RHS[I_Np] = I_Value
    RHS[I_Nn] = -I_Value

V = np.linalg.solve(a, RHS)
V[1] = V[0] - V[1]

print("\nmatrix = ", a)
print("\nRHS = ", RHS)
print("\nV1 = ", V[1],
      "\nV2 = ", V[0])

file.close()
