#$Id: settings.tcl,v 1.16 2016/08/24 20:55:41 ctai Exp ctai $#
#####----------------------------------------
##### Set liberate variables
#####----------------------------------------
### External Simulator (Spectre) settings ###
set_var extsim_cmd_option      "+aps +spice -mt +liberate +rcopt=2"
set_var extsim_deck_header     "simulator lang=spectre\nOpt1 options reltol=1e-4 \nsimulator lang=spice"
set_var extsim_option          "redefinedparams=ignore hier_ambiguity=lower limit=delta "
set_var extsim_leakage_option  "redefinedparams=ignore hier_ambiguity=lower limit=delta "


### SKI ###
set_var ski_enable               1
set_var ski_clean_mode           1  ;# run $ALTOSHOME/bin/clean_sm.sh to clean up inactive semaphores
set_var ski_compatibility_mode   1


### Misc ###
set_var parse_auto_define_leafcell   0 ;# disable auto leaf cell determination
set_var tmpdir /dev/shm          ;# /dev/shm - use local RAM disk for tmp dir, /tmp - use local disk
set_var extsim_deck_dir [file normalize "decks"]   ;# specify directory for SPICE decks and output files


### Input waveform ###
set_var predriver_waveform       2 ;# use pre-driver waveform


### Arc Generation
set_var force_condition              4


### Capacitance ###
set_var min_capacitance_for_outputs            1        ;# write min_capacitance attribute for output pins
# set_var measure_cap_lower_rise                 0
# set_var measure_cap_upper_rise                 0.5
# set_var measure_cap_upper_fall                 1
# set_var measure_cap_lower_fall                 0.5


### Timing ###


### Constraint ###
#set_var constraint_info                  2
#set_var constraint_search_time_abstol    1e-12	;# 1ps resolution for bisection search
set_var nochange_mode                    1        ;# enable nochange_* constraint characterization


### min_pulse_width ###
set_var conditional_mpw            0       ;# 0=disable conditional mpw


### Leakage ###
set_var max_leakage_vector                 [expr 2**10]
set_var leakage_float_internal_supply      0            ;# get worst case leakage for power switch cells when off
set_var reset_negative_leakage_power       1            ;# convert negative leakage current to 0


### Power ###
set_var voltage_map                         1	;# create pg_pin groups, related_power_pin / related_ground_pin
set_var pin_based_power                     0	;# Monitor power based on Vdd pin only
set_var power_multi_output_binning_mode	    1
set_var power_subtract_leakage              4	;# use 4 for cells with exhaustive leakage states.
set_var subtract_hidden_power               2   ;# subtract hidden power for all cells
set_var subtract_hidden_power_use_default   2   ;# subtract hidden power for overlapping when, then default group

### Hidden Power ###
set_var max_hidden_vector                   [expr 2**10]


## CCS ###


### CCSN ###
set_var ccsn_include_passgate_attr 1  ;# include pin level attribute is_unbuffered and has_pass_gate, and
                                       # ccsn_*_stage group level attribute is_pass_gate


### CCSP ###


## ECSM ##


## ECSMN ##


## ECSMP ##


## EM ##
if { [info exists CHAR_EM_TECH_FILE] && ($CHAR_EM_TECH_FILE ne "") } { set_var em_tech_file [file normalize $CHAR_EM_TECH_FILE] }
set_var em_char_arcs_mode   1                 ;# test only high (RF) output pulse; default=test both high (RF) and low (FR) pulse


#####----------------------------------------
##### Writing Output Files
#####----------------------------------------
set_var write_library_is_unbuffered            1
set_var cell_use_both_ff_latch_groups          2 ;# allow use of multiple ff,latch,state_table groups in userdata file
set_var user_data_override { power_down_function pg_pin }
set_var sdf_cond_style                         1
set_var parenthesize_not                       0 ;# use !A instead of !(A)
set_var driver_type_model_pad_check            1 ;# enable fix to disable output of driver_type pin attribute for tie cells CCR1407896

#####----------------------------------------
##### liberate_lv
#####----------------------------------------
if { $::LIBERATE_program == "LIBERATE_LV" } {
    set validate_cells_per_bundle 10000
}

#####----------------------------------------
##### variety
#####----------------------------------------
if { $::LIBERATE_program == "VARIETY" } {
    set_var variation_mean_nominal_mode       4 ;# save mean, stddev, and skewness values (in addition to normal variation data) to ldb
    #set_var variation_static_partition_mode  2 ;# Enable logic-cone analysis (0=disable; 1=faster/less accurate; 3=slower/more accurate)
    #set_var non_linear_random_variation      3 ;# (1=characterize positive and negative variation; 3=trade off minor early accuracy for faster run time)
                                                # use default of 0 for AOCV(fastest)
    #####  Constraint  #####
    #set_var constraint_random_variation_search_time_abstol [expr [get_var constraint_search_time_abstol] * 0.1] ;# typically set to 10% of constraint_search_time_abstol
    set_var lvf_constraint_early_late_mode   1 ;# output early and late sigma type for constraint
                                                #   more accruate for non-gaussian distribution
    set_var mpw_variation                    1 ;# enable mpw variation characterization

    #####  Monte Carlo  #####
    set_var extsim_monte_option  "sampling=lds" ;# set Spectre Monte Carlo sampling method [standard lhs lds orthogonal]
                                                 # lhs=Latin-Hypercube, lds=Low-Discrepancy Sequence
    #set_var extsim_cmd_option "[get_var extsim_cmd_option] +mp=5" ;#distribute Monte Carlo jobs (5 .alter per job)
}

