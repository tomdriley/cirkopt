TEST_NETLIST = r"""
** Library name: gsclib045
** Cell name: INVX1_3
** View name: schematic
.subckt INVX1_3 A Y VDD VSS
*.PININFO  VSS:I VDD:I A:I Y:O
** Above line required by Conformal LEC - DO NOT DELETE

mp0 Y A VDD VDD g45p1svt L=45e-9 W=250e-9 AD=54.6e-15 AS=54.6e-15 PD=1.06e-6 PS=1.06e-6 NRD=358.974e-3 NRS=358.974e-3 M=1
mn0 Y A VSS VSS g45n1svt L=50e-9 W=300e-9 AD=36.4e-15 AS=36.4e-15 PD=800e-9 PS=800e-9 NRD=538.462e-3 NRS=538.462e-3 M=2
.ends INVX1_3
"""
NETLIST_F3E7F6B4_EXAMPLES = {
    "INVX1_00": r"""** Library name: gsclib045
** Cell name: INVX1_00
** View name: schematic
.subckt INVX1_00 A Y VDD VSS
*.PININFO  VSS:I VDD:I A:I Y:O
** Above line required by Conformal LEC - DO NOT DELETE

mp0 Y A VDD VDD g45p1svt L=4.5e-08 W=2e-07 AD=54.6e-15 AS=54.6e-15 PD=1.06e-6 PS=1.06e-6 NRD=358.974e-3 NRS=358.974e-3 M=1
mn0 Y A VSS VSS g45n1svt L=4.5e-08 W=2e-07 AD=36.4e-15 AS=36.4e-15 PD=800e-9 PS=800e-9 NRD=538.462e-3 NRS=538.462e-3 M=1
.ends INVX1_00
""",
    "INVX1_01": r"""** Library name: gsclib045
** Cell name: INVX1_01
** View name: schematic
.subckt INVX1_01 A Y VDD VSS
*.PININFO  VSS:I VDD:I A:I Y:O
** Above line required by Conformal LEC - DO NOT DELETE

mp0 Y A VDD VDD g45p1svt L=4.5e-08 W=3e-07 AD=54.6e-15 AS=54.6e-15 PD=1.06e-6 PS=1.06e-6 NRD=358.974e-3 NRS=358.974e-3 M=1
mn0 Y A VSS VSS g45n1svt L=4.5e-08 W=3e-07 AD=36.4e-15 AS=36.4e-15 PD=800e-9 PS=800e-9 NRD=538.462e-3 NRS=538.462e-3 M=1
.ends INVX1_01
""",
    "INVX1_02": r"""** Library name: gsclib045
** Cell name: INVX1_02
** View name: schematic
.subckt INVX1_02 A Y VDD VSS
*.PININFO  VSS:I VDD:I A:I Y:O
** Above line required by Conformal LEC - DO NOT DELETE

mp0 Y A VDD VDD g45p1svt L=4.5e-08 W=1.11e-06 AD=54.6e-15 AS=54.6e-15 PD=1.06e-6 PS=1.06e-6 NRD=358.974e-3 NRS=358.974e-3 M=1
mn0 Y A VSS VSS g45n1svt L=4.5e-08 W=1.35e-07 AD=36.4e-15 AS=36.4e-15 PD=800e-9 PS=800e-9 NRD=538.462e-3 NRS=538.462e-3 M=1
.ends INVX1_02
""",
    "INVX1_03": r"""** Library name: gsclib045
** Cell name: INVX1_03
** View name: schematic
.subckt INVX1_03 A Y VDD VSS
*.PININFO  VSS:I VDD:I A:I Y:O
** Above line required by Conformal LEC - DO NOT DELETE

mp0 Y A VDD VDD g45p1svt L=4.5e-08 W=5e-07 AD=54.6e-15 AS=54.6e-15 PD=1.06e-6 PS=1.06e-6 NRD=358.974e-3 NRS=358.974e-3 M=1
mn0 Y A VSS VSS g45n1svt L=4.5e-08 W=5e-07 AD=36.4e-15 AS=36.4e-15 PD=800e-9 PS=800e-9 NRD=538.462e-3 NRS=538.462e-3 M=1
.ends INVX1_03
""",
    "INVX1_04": r"""** Library name: gsclib045
** Cell name: INVX1_04
** View name: schematic
.subckt INVX1_04 A Y VDD VSS
*.PININFO  VSS:I VDD:I A:I Y:O
** Above line required by Conformal LEC - DO NOT DELETE

mp0 Y A VDD VDD g45p1svt L=4.5e-08 W=6e-07 AD=54.6e-15 AS=54.6e-15 PD=1.06e-6 PS=1.06e-6 NRD=358.974e-3 NRS=358.974e-3 M=1
mn0 Y A VSS VSS g45n1svt L=4.5e-08 W=6e-07 AD=36.4e-15 AS=36.4e-15 PD=800e-9 PS=800e-9 NRD=538.462e-3 NRS=538.462e-3 M=1
.ends INVX1_04
""",
    "INVX1_05": r"""** Library name: gsclib045
** Cell name: INVX1_05
** View name: schematic
.subckt INVX1_05 A Y VDD VSS
*.PININFO  VSS:I VDD:I A:I Y:O
** Above line required by Conformal LEC - DO NOT DELETE

mp0 Y A VDD VDD g45p1svt L=4.5e-08 W=7e-07 AD=54.6e-15 AS=54.6e-15 PD=1.06e-6 PS=1.06e-6 NRD=358.974e-3 NRS=358.974e-3 M=1
mn0 Y A VSS VSS g45n1svt L=4.5e-08 W=7e-07 AD=36.4e-15 AS=36.4e-15 PD=800e-9 PS=800e-9 NRD=538.462e-3 NRS=538.462e-3 M=1
.ends INVX1_05
""",
    "INVX1_06": r"""** Library name: gsclib045
** Cell name: INVX1_06
** View name: schematic
.subckt INVX1_06 A Y VDD VSS
*.PININFO  VSS:I VDD:I A:I Y:O
** Above line required by Conformal LEC - DO NOT DELETE

mp0 Y A VDD VDD g45p1svt L=4.5e-08 W=8e-07 AD=54.6e-15 AS=54.6e-15 PD=1.06e-6 PS=1.06e-6 NRD=358.974e-3 NRS=358.974e-3 M=1
mn0 Y A VSS VSS g45n1svt L=4.5e-08 W=8e-07 AD=36.4e-15 AS=36.4e-15 PD=800e-9 PS=800e-9 NRD=538.462e-3 NRS=538.462e-3 M=1
.ends INVX1_06
""",
    "INVX1_07": r"""** Library name: gsclib045
** Cell name: INVX1_07
** View name: schematic
.subckt INVX1_07 A Y VDD VSS
*.PININFO  VSS:I VDD:I A:I Y:O
** Above line required by Conformal LEC - DO NOT DELETE

mp0 Y A VDD VDD g45p1svt L=4.5e-08 W=9e-07 AD=54.6e-15 AS=54.6e-15 PD=1.06e-6 PS=1.06e-6 NRD=358.974e-3 NRS=358.974e-3 M=1
mn0 Y A VSS VSS g45n1svt L=4.5e-08 W=9e-07 AD=36.4e-15 AS=36.4e-15 PD=800e-9 PS=800e-9 NRD=538.462e-3 NRS=538.462e-3 M=1
.ends INVX1_07
""",
    "INVX1_08": r"""** Library name: gsclib045
** Cell name: INVX1_08
** View name: schematic
.subckt INVX1_08 A Y VDD VSS
*.PININFO  VSS:I VDD:I A:I Y:O
** Above line required by Conformal LEC - DO NOT DELETE

mp0 Y A VDD VDD g45p1svt L=4.5e-08 W=1e-06 AD=54.6e-15 AS=54.6e-15 PD=1.06e-6 PS=1.06e-6 NRD=358.974e-3 NRS=358.974e-3 M=1
mn0 Y A VSS VSS g45n1svt L=4.5e-08 W=1e-06 AD=36.4e-15 AS=36.4e-15 PD=800e-9 PS=800e-9 NRD=538.462e-3 NRS=538.462e-3 M=1
.ends INVX1_08
""",
}
