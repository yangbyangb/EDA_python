import re

file = open("TEST CIRCUIT.txt", "r")
line_number = 0
Unit_dict = {'F': -15, 'P': -12, 'N': -9, 'U': -6, 'M': -3, 'K': 3, 'Meg': 6, 'G': 9, 'T': 12}
while 1:
    line = file.readline()
    if not line:
        break
    pass
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
            #     1  Name  2 N+ 3 N- 4       5   6   7                       8   9   10
            if RCL_pattern:
                print("\nName:\t", RCL_pattern.group(1),
                      "\nNode1:\t", RCL_pattern.group(2),
                      "\nNode2:\t", RCL_pattern.group(3),
                      "\nValue:\t", RCL_pattern.group(4))
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
                print("\nName:\t", VI_pattern.group(1),
                      "\nNode+:\t", VI_pattern.group(2),
                      "\nNode-:\t", VI_pattern.group(3))
                if VI_pattern.group(4):
                    print(VI_pattern.group(4), "Value:\t", VI_pattern.group(7))
                else:
                    print("DC Value:\t", VI_pattern.group(7))
                if VI_pattern.group(10):
                    print("AC Phase:\t", VI_pattern.group(10))

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
file.close()
