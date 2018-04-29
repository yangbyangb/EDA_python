mos test
VDD vdd gnd 1.8
M1 1 in gnd gnd NMOS w=2u l=180n
R1 vdd 1 1k
Vin in gnd PULSE 0.1 1.8V 2ns 3ns 4ns 5ns 20ns
.op
.tran 1ns 1us
.end