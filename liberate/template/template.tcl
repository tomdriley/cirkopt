#$Id$

set_vdd -type primary VDD $VDD
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
set_var min_transition 6e-12
set_var max_transition 3e-10
set_var min_output_cap 1e-16

### Define templates - slew (0-100%) min,max=10ps,500ps
define_template -type delay      -index_1 {0.006 0.3 } -index_2 {0.0001 0.07 } delay_template
define_template -type power      -index_1 {0.006 0.3 } -index_2 {0.0001 0.07 } power_template
define_template -type constraint -index_1 {0.006 0.3 } -index_2 {0.006 0.3 } const_template


set cells { 
    AND2X1 
    BUFX8
    BUFX8_drv
    INVX1  
    XOR2X1 
}

### Define related supply for all cells and pins
set_pin_vdd -supply_name VDD $cells {*}
set_pin_gnd -supply_name VSS $cells {*}
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

set cell INVX1_2
if {[ALAPI_active_cell $cell]} {
    define_cell \
       -input { A } \
       -output { Y } \
       -pinlist { A Y } \
       -delay delay_template \
       -power power_template \
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
