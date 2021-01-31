** Library name: gsclib045
** Cell name: BUFX8
** View name: schematic
.subckt BUFX8_drv Y A VDD VSS
mn1 VSS n0 y VSS g45n1svt L=45e-9 W=2.065e-6 AD=289.1e-15 AS=289.1e-15 PD=4.41e-6 PS=4.41e-6 NRD=67.7966e-3 NRS=67.7966e-3 M=1
mn0 VSS a n0 VSS g45n1svt L=45e-9 W=520e-9 AD=72.8e-15 AS=72.8e-15 PD=1.32e-6 PS=1.32e-6 NRD=269.231e-3 NRS=269.231e-3 M=1
mp1 y n0 VDD VDD g45p1svt L=45e-9 W=3.115e-6 AD=436.1e-15 AS=436.1e-15 PD=6.51e-6 PS=6.51e-6 NRD=44.9438e-3 NRS=44.9438e-3 M=1
mp0 n0 a VDD VDD g45p1svt L=45e-9 W=780e-9 AD=109.2e-15 AS=109.2e-15 PD=1.84e-6 PS=1.84e-6 NRD=179.487e-3 NRS=179.487e-3 M=1
.ends BUFX8_drv
