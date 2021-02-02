** Library name: gsclib045
** Cell name: XOR2X1
** View name: schematic
.subckt XOR2X1 A B Y VDD VSS
*.PININFO  A:I VSS:I B:I VDD:I Y:O
** Above line required by Conformal LEC - DO NOT DELETE

mn1 n2 B VSS VSS g45n1svt L=45e-9 W=145e-9 AD=20.3e-15 AS=20.3e-15 PD=570e-9 PS=570e-9 NRD=965.517e-3 NRS=965.517e-3 M=1
mn0 n1 A VSS VSS g45n1svt L=45e-9 W=145e-9 AD=20.3e-15 AS=20.3e-15 PD=570e-9 PS=570e-9 NRD=965.517e-3 NRS=965.517e-3 M=1
mn5 Y n0 VSS VSS g45n1svt L=45e-9 W=260e-9 AD=36.4e-15 AS=36.4e-15 PD=800e-9 PS=800e-9 NRD=538.462e-3 NRS=538.462e-3 M=1
mn3 n0 B net131 VSS g45n1svt L=45e-9 W=145e-9 AD=20.3e-15 AS=20.3e-15 PD=570e-9 PS=570e-9 NRD=965.517e-3 NRS=965.517e-3 M=1
mn4 n0 n2 n1 VSS g45n1svt L=45e-9 W=145e-9 AD=20.3e-15 AS=20.3e-15 PD=570e-9 PS=570e-9 NRD=965.517e-3 NRS=965.517e-3 M=1
mn2 net131 n1 VSS VSS g45n1svt L=45e-9 W=145e-9 AD=20.3e-15 AS=20.3e-15 PD=570e-9 PS=570e-9 NRD=965.517e-3 NRS=965.517e-3 M=1
mp3 n0 n2 net130 VDD g45p1svt L=45e-9 W=215e-9 AD=30.1e-15 AS=30.1e-15 PD=710e-9 PS=710e-9 NRD=651.163e-3 NRS=651.163e-3 M=1
mp1 n2 B VDD VDD g45p1svt L=45e-9 W=215e-9 AD=30.1e-15 AS=30.1e-15 PD=710e-9 PS=710e-9 NRD=651.163e-3 NRS=651.163e-3 M=1
mp4 n1 B n0 VDD g45p1svt L=45e-9 W=215e-9 AD=30.1e-15 AS=30.1e-15 PD=710e-9 PS=710e-9 NRD=651.163e-3 NRS=651.163e-3 M=1
mp0 n1 A VDD VDD g45p1svt L=45e-9 W=215e-9 AD=30.1e-15 AS=30.1e-15 PD=710e-9 PS=710e-9 NRD=651.163e-3 NRS=651.163e-3 M=1
mp5 Y n0 VDD VDD g45p1svt L=45e-9 W=390e-9 AD=54.6e-15 AS=54.6e-15 PD=1.06e-6 PS=1.06e-6 NRD=358.974e-3 NRS=358.974e-3 M=1
mp2 net130 n1 VDD VDD g45p1svt L=45e-9 W=215e-9 AD=30.1e-15 AS=30.1e-15 PD=710e-9 PS=710e-9 NRD=651.163e-3 NRS=651.163e-3 M=1
.ends XOR2X1