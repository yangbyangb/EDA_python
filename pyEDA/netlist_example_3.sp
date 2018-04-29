*netlist example 3
V1 1 gnd PULSE 0 1 0.5us 1ps 1ps 1s 2s
R1 1 2 1
C1 2 gnd 1u
R2 2 3 2
C2 3 gnd 2u
R2 3 4 3
C2 4 gnd 3u
R2 4 5 4
C2 5 gnd 4u
.tran 1ns 1us
.end