mos test
VDD vdd gnd 1.8
M1 vdd in gnd gnd NMOS w=200n l=200n
Vin in gnd PULSE 0 1V 2ns 3ns 4ns 5ns 20ns
.op
.tran 1ns 1us
.end