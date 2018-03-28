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
RCL_index = 0
EG_index = 0
VI_index = 0
while line:
    if not (line_number == 0):  # 忽略第一行
        if not line[0] == '.':
            # comment
            comment_pattern = re.match(r'\*', line, re.M | re.I)  # 匹配注释

            if comment_pattern:
                comment = comment_pattern.group()
                print("\ncomment line:\t", line_number, "    ", line[:-1])  # 输出注释行

            # instance
            RCL_pattern = re.match(r'(^[RCL].*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)[FH]?', line, re.I)  # 匹配RCL器件
            # D
            D_pattern = re.match(r'(^D.*) (.*) (.*) (.*)', line, re.I)
            # Q
            Q_pattern = re.match(r'(^Q.*) (.*) (.*) (.*) (.*)', line, re.I)
            # MOS
            MOS_pattern = re.match(
                r'(^M.*) (.*) (.*) (.*) (.*) (.*) ([LW])=([0-9.]*[FPNUMKGT]?) ([LW])=([0-9.]*[FPNUMKGT]?)', line, re.I)
            #     1      2    3    4    5    6    7      8                     9      10
            VI_pattern = re.match(
                r'(^[VI].) (.*) (.*) ([AD]C)?(=)?( ?)([0-9.]*[FPNUMKGT]?)[VA]?(,?)( ?)([0-9.]*$)?', line, re.I)
            #     1  Name  2 N+ 3 N- 4       5   6   7                        8   9   10
            EG_pattern = re.match(r'(^[EG].) (.*) (.*) (.*) (.*) ([0-9.]*[FPNUMKGT]?)(mho)?', line, re.I)
            FH_pattern = re.match(r'(^[FH].) (.*) (.*) (V.*) ([0-9.]*[FPNUMKGT]?)(ohm)?', line, re.I)

            if RCL_pattern:
                RCL_N1 = int(RCL_pattern.group(2))  # N1
                RCL_N2 = int(RCL_pattern.group(3))  # N2
                i = max(i, RCL_N1, RCL_N2)
                RCL_Value = unit_transform(RCL_pattern.group(4))  # Value
                tmp_array = ([RCL_N1, RCL_N2, RCL_Value])
                if RCL_index == 1:
                    RCL_array = np.row_stack((RCL_array, tmp_array))
                else:
                    RCL_array = tmp_array
                    RCL_index = 1
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
            elif VI_pattern:
                VI_N1 = int(VI_pattern.group(2))
                VI_N2 = int(VI_pattern.group(3))
                if VI_pattern.group(4):
                    print(VI_pattern.group(4), "Value:\t", VI_pattern.group(7))
                # else:
                #    print("DC Value:\t", VI_pattern.group(7))
                VI_value = unit_transform(VI_pattern.group(7))
                if VI_pattern.group(10):
                    print("AC Phase:\t", VI_pattern.group(10))
                    VI_value = unit_transform(VI_pattern.group(10))
                tmp_array = [VI_N1, VI_N2, VI_value]
                if VI_index == 1:
                    VI_array = np.column_stack((VI_array, tmp_array))
                else:
                    VI_array = tmp_array
                    VI_index = 1
            elif EG_pattern:
                EG_N1 = int(EG_pattern.group(2))
                EG_N2 = int(EG_pattern.group(3))
                EG_NC1 = int(EG_pattern.group(4))
                EG_NC2 = int(EG_pattern.group(5))
                i = max(i, EG_N1, EG_N2, EG_NC1, EG_NC2)
                EG_Value = unit_transform(EG_pattern.group(6))
                tmp_array = [EG_N1, EG_N2, EG_NC1, EG_NC2, EG_Value]
                if EG_index == 1:
                    EG_array = np.column_stack((EG_array, tmp_array))
                else:
                    EG_array = tmp_array
                    EG_index = 1
            elif FH_pattern:
                print("\nName:\t", FH_pattern.group(1),
                      "\nN+:\t", FH_pattern.group(2),
                      "\nN-:\t", FH_pattern.group(3),
                      "\nVname:\t", FH_pattern.group(4),
                      "\nValue:\t", FH_pattern.group(5))

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

print(RCL_array)
print(EG_array)
print(VI_array)

# 运算
i += 1

R_row_num = RCL_array.shape[0]  # 矩阵的行数
R_col_num = RCL_array.shape[1]  # 矩阵的列数

a = np.zeros([i, i])  # i*i矩阵
b = np.zeros([i, 1])
c = np.zeros([i, 1])

for index in range(R_row_num):
    N1 = RCL_array[index, 0]
    N2 = RCL_array[index, 1]
    G_Value = 1 / RCL_array[index, 2]
    if RCL_index:
        a[N1, N1] += G_Value
        a[N2, N2] += G_Value
        a[N1, N2] -= G_Value
        a[N2, N1] -= G_Value

print(a)

file.close()
