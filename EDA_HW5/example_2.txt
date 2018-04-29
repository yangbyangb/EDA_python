*netlist example 2
*VIN 1 0 PULSE 0 5 2NS 2NS 2NS 30NS 60NS
Vin 1 0 AC 1V 180
R1 1 2 1
C1 2 0 1u
*I1 1 0 1
L1 1 2 1m
.ac LIN 100 1 100HZ
*.tran 1ns 1000ns
.end