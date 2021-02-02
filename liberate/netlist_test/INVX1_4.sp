** Library name: gsclib045
** Cell name: INVX1_4
** View name: schematic
.subckt INVX1_4 A Y VDD VSS
*.PININFO  VSS:I VDD:I A:I Y:O
** Above line required by Conformal LEC - DO NOT DELETE

mp0 Y A VDD VDD g45p1svt L=5e-08 W=2.6e-07 AD=54.6e-15 AS=54.6e-15 PD=1.06e-6 PS=1.06e-6 NRD=358.974e-3 NRS=358.974e-3 M=2
mn0 Y A VSS VSS g45n1svt L=6e-08 W=3.1e-07 AD=36.4e-15 AS=36.4e-15 PD=800e-9 PS=800e-9 NRD=538.462e-3 NRS=538.462e-3 M=3
.ends INVX1_4
