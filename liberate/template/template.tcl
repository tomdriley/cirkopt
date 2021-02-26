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
set_var process_match_pins_to_ports 0  ;# disable check for exact match of subckt ports and define_cell command

set_var min_transition 6e-12
set_var max_transition 3e-10
set_var min_output_cap 1e-16

# reference cells
set cells {
    AND2X1
    BUFX8
    BUFX8_drv
    INVX1
    XOR2X1
}
# Overrides with working cells. Must update if new cells are added
set cells {
    INVX1_00
    INVX1_01
    INVX1_02
    INVX1_03
    INVX1_04
    INVX1_05
    INVX1_06
    INVX1_07
}


### Define templates - slew (0-100%) min,max=10ps,500ps
define_template -type delay \
    -index_1 {0.006 0.3 } \
    -index_2 {0.0001 0.07 } \
    delay_template
define_template -type power \
    -index_1 {0.006 0.3 } \
    -index_2 {0.0001 0.07 } \
    power_template
define_template -type constraint \
    -index_1 {0.006 0.3 } \
    -index_2 {0.006 0.3 } \
    const_template

# Define generic list of  input and output names
set inputs   { A B } 
set outputs  { Y }

### Define related supply for all cells and pins
set_pin_vdd -supply_name VDD $cells {*}
set_pin_gnd -supply_name VSS $cells {*}

# Generic define_cell - all cell specific definitions are require to be above this generic definition
define_cell \
    -input  $inputs  \
    -output $outputs \
    -delay      delay_template \
    -power      power_template \
    -constraint const_template \
    $cells