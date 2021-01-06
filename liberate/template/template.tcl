#$Id$

set_vdd -type primary VDD $VDD_VALUE
set_gnd -type primary VSS 0
set_gnd -no_model     GND 0

set_var slew_lower_rise 0.2
set_var slew_lower_fall 0.2
set_var slew_upper_rise 0.8
set_var slew_upper_fall 0.8

set_var measure_slew_lower_rise 0.2
set_var measure_slew_lower_fall 0.2
set_var measure_slew_upper_rise 0.8
set_var measure_slew_upper_fall 0.8

set_var delay_inp_rise 0.5
set_var delay_inp_fall 0.5
set_var delay_out_rise 0.5
set_var delay_out_fall 0.5

set_var def_arc_msg_level 0
set_var process_match_pins_to_ports 1
set_var max_transition 2.1e-10
set_var min_transition 6.50794e-12
set_var min_output_cap 2.52711e-16

set cells { 
    AND2X1 
    DFFQX1 
    DFFSRHQX1 
    INVX1 
    SDFFQX1 
    SDFFSRHQX1 
    TLATQX1 
    TLATX1 
    TLATSRX1 
    XOR2X1 
}

define_template -type delay      -index_1 {0.006 0.21 } -index_2 {0.0002 0.03 } delay_template
define_template -type power      -index_1 {0.006 0.21 } -index_2 {0.0002 0.03 } power_template
define_template -type constraint -index_1 {0.006 0.21 } -index_2 {0.006 0.21 }  const_template

set cell AND2X1
if {[ALAPI_active_cell $cell]} {
    define_cell \
       -input { A B } \
       -output { Y } \
       -pinlist { A B Y } \
       -delay delay_template \
       -power power_template \
       $cell
}

set cell BUFX8
if {[ALAPI_active_cell $cell]} {
define_cell \
       -input { A } \
       -output { Y } \
       -pinlist { A Y } \
       -delay delay_template \
       -power power_template \
       $cell
    define_index -index_2 {0.01 0.45 } -type {delay power} $cell
}

if {[ALAPI_active_cell "BUFX8_drv"]} {
define_cell \
       -input { A } \
       -output { Y } \
       -pinlist { A Y } \
       BUFX8_drv
}

set cell DFFQX1
if {[ALAPI_active_cell $cell]} {
    define_cell \
       -clock { CK } \
       -input { D } \
       -output { Q } \
       -pinlist { CK D Q } \
       -delay delay_template \
       -power power_template \
       -constraint const_template \
       $cell
}

set cell DFFSRHQX1
if {[ALAPI_active_cell $cell]} {
    define_cell \
       -clock { CK } \
       -async { RN SN } \
       -input { D } \
       -output { Q } \
       -pinlist { CK D RN SN Q } \
       -delay delay_template \
       -power power_template \
       -constraint const_template \
       $cell
}

set cell INVX1
if {[ALAPI_active_cell $cell]} {
    define_cell \
       -input { A } \
       -output { Y } \
       -pinlist { A Y } \
       -delay delay_template \
       -power power_template \
       $cell
}

set cell SDFFQX1
if {[ALAPI_active_cell $cell]} {
    define_cell \
       -clock { CK } \
       -input { D SE SI } \
       -output { Q } \
       -pinlist { CK D SE SI Q } \
       -delay delay_template \
       -power power_template \
       -constraint const_template \
       $cell
}

set cell SDFFSRHQX1
if {[ALAPI_active_cell $cell]} {
define_cell \
       -clock { CK } \
       -async { RN SN } \
       -input { D SE SI } \
       -output { Q } \
       -pinlist { CK D RN SE SI SN Q } \
       -delay delay_template \
       -power power_template \
       -constraint const_template \
       $cell
}

set cell TLATQX1
if {[ALAPI_active_cell $cell]} {
    define_cell \
       -clock { G } \
       -input { D } \
       -output { Q } \
       -pinlist { D G Q } \
       -delay delay_template \
       -power power_template \
       -constraint const_template \
       $cell
}

set cell TLATX1
if {[ALAPI_active_cell $cell]} {
    define_cell \
       -clock { G } \
       -input { D } \
       -output { Q QN } \
       -pinlist { D G Q QN } \
       -delay delay_template \
       -power power_template \
       -constraint const_template \
       $cell
}

set cell TLATSRX1
if {[ALAPI_active_cell $cell]} {
    define_cell \
       -clock { G } \
       -async { RN SN } \
       -input { D } \
       -output { Q QN } \
       -pinlist { D G RN SN Q QN } \
       -delay delay_template \
       -power power_template \
       -constraint const_template \
       $cell
}

set cell XOR2X1
if {[ALAPI_active_cell $cell]} {
    define_cell \
       -input { A B } \
       -output { Y } \
       -pinlist { A B Y } \
       -delay delay_template \
       -power power_template \
       $cell
}
