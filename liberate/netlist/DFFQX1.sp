** Library name: gsclib045
** Cell name: DFFQX1
** View name: schematic
.subckt DFFQX1 CK D Q VDD VSS
*.PININFO  CK:I D:I VDD:I VSS:I Q:O
** Above line required by Conformal LEC - DO NOT DELETE

mn26 n20 CKb n21 VSS g45n1svt L=45e-9 W=145e-9 AD=20.3e-15 AS=20.3e-15 PD=570e-9 PS=570e-9 NRD=965.517e-3 NRS=965.517e-3 M=1
mn25 n21 D VSS VSS g45n1svt L=45e-9 W=145e-9 AD=20.3e-15 AS=20.3e-15 PD=570e-9 PS=570e-9 NRD=965.517e-3 NRS=965.517e-3 M=1
mn55 Q qbint VSS VSS g45n1svt L=45e-9 W=260e-9 AD=36.4e-15 AS=36.4e-15 PD=800e-9 PS=800e-9 NRD=538.462e-3 NRS=538.462e-3 M=1
mn50 n35 qbint VSS VSS g45n1svt L=45e-9 W=145e-9 AD=20.3e-15 AS=20.3e-15 PD=570e-9 PS=570e-9 NRD=965.517e-3 NRS=965.517e-3 M=1
mn51 n30 CKb n35 VSS g45n1svt L=45e-9 W=145e-9 AD=20.3e-15 AS=20.3e-15 PD=570e-9 PS=570e-9 NRD=965.517e-3 NRS=965.517e-3 M=1
mn35 n25 mout VSS VSS g45n1svt L=45e-9 W=145e-9 AD=20.3e-15 AS=20.3e-15 PD=570e-9 PS=570e-9 NRD=965.517e-3 NRS=965.517e-3 M=1
mn30 mout n20 VSS VSS g45n1svt L=45e-9 W=145e-9 AD=20.3e-15 AS=20.3e-15 PD=570e-9 PS=570e-9 NRD=965.517e-3 NRS=965.517e-3 M=1
mn40 n30 CKbb mout VSS g45n1svt L=45e-9 W=145e-9 AD=20.3e-15 AS=20.3e-15 PD=570e-9 PS=570e-9 NRD=965.517e-3 NRS=965.517e-3 M=1
mn45 qbint n30 VSS VSS g45n1svt L=45e-9 W=145e-9 AD=20.3e-15 AS=20.3e-15 PD=570e-9 PS=570e-9 NRD=965.517e-3 NRS=965.517e-3 M=1
mn21 CKbb CKb VSS VSS g45n1svt L=45e-9 W=145e-9 AD=20.3e-15 AS=20.3e-15 PD=570e-9 PS=570e-9 NRD=965.517e-3 NRS=965.517e-3 M=1
mn36 n20 CKbb n25 VSS g45n1svt L=45e-9 W=145e-9 AD=20.3e-15 AS=20.3e-15 PD=570e-9 PS=570e-9 NRD=965.517e-3 NRS=965.517e-3 M=1
mn20 CKb CK VSS VSS g45n1svt L=45e-9 W=145e-9 AD=20.3e-15 AS=20.3e-15 PD=570e-9 PS=570e-9 NRD=965.517e-3 NRS=965.517e-3 M=1
mp26 n20 CKbb n22 VDD g45p1svt L=45e-9 W=215e-9 AD=30.1e-15 AS=30.1e-15 PD=710e-9 PS=710e-9 NRD=651.163e-3 NRS=651.163e-3 M=1
mp25 n22 D VDD VDD g45p1svt L=45e-9 W=215e-9 AD=30.1e-15 AS=30.1e-15 PD=710e-9 PS=710e-9 NRD=651.163e-3 NRS=651.163e-3 M=1
mp51 n30 CKbb n36 VDD g45p1svt L=45e-9 W=215e-9 AD=30.1e-15 AS=30.1e-15 PD=710e-9 PS=710e-9 NRD=651.163e-3 NRS=651.163e-3 M=1
mp50 n36 qbint VDD VDD g45p1svt L=45e-9 W=215e-9 AD=30.1e-15 AS=30.1e-15 PD=710e-9 PS=710e-9 NRD=651.163e-3 NRS=651.163e-3 M=1
mp55 Q qbint VDD VDD g45p1svt L=45e-9 W=390e-9 AD=54.6e-15 AS=54.6e-15 PD=1.06e-6 PS=1.06e-6 NRD=358.974e-3 NRS=358.974e-3 M=1
mp35 n26 mout VDD VDD g45p1svt L=45e-9 W=215e-9 AD=30.1e-15 AS=30.1e-15 PD=710e-9 PS=710e-9 NRD=651.163e-3 NRS=651.163e-3 M=1
mp36 n20 CKb n26 VDD g45p1svt L=45e-9 W=215e-9 AD=30.1e-15 AS=30.1e-15 PD=710e-9 PS=710e-9 NRD=651.163e-3 NRS=651.163e-3 M=1
mp21 CKbb CKb VDD VDD g45p1svt L=45e-9 W=215e-9 AD=30.1e-15 AS=30.1e-15 PD=710e-9 PS=710e-9 NRD=651.163e-3 NRS=651.163e-3 M=1
mp20 CKb CK VDD VDD g45p1svt L=45e-9 W=215e-9 AD=30.1e-15 AS=30.1e-15 PD=710e-9 PS=710e-9 NRD=651.163e-3 NRS=651.163e-3 M=1
mp45 qbint n30 VDD VDD g45p1svt L=45e-9 W=215e-9 AD=30.1e-15 AS=30.1e-15 PD=710e-9 PS=710e-9 NRD=651.163e-3 NRS=651.163e-3 M=1
mp40 n30 CKb mout VDD g45p1svt L=45e-9 W=215e-9 AD=30.1e-15 AS=30.1e-15 PD=710e-9 PS=710e-9 NRD=651.163e-3 NRS=651.163e-3 M=1
mp30 mout n20 VDD VDD g45p1svt L=45e-9 W=215e-9 AD=30.1e-15 AS=30.1e-15 PD=710e-9 PS=710e-9 NRD=651.163e-3 NRS=651.163e-3 M=1
.ends DFFQX1
