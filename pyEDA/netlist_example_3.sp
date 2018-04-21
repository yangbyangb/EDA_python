*netlist example 3
V1 n1 gnd 5
V1 n1 gnd AC 1V 180
V1 n1 gnd PULSE 0 1 0.5us 1ps 1ps 1s 2s

R1 n1 n2 0.6k
L1 n2 n3 0.01524
C1 n3 gnd 0.11937u
L2 n3 n4 0.06186
C2 n4 gnd 0.15512u
R2 n4 gnd 1.2k

.ac LIN 100 1000 100kHZ
.tran 1us 1ms
.end