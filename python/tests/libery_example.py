LIBERTY_EXAMPLE = """
library (example_tt_1.0_70) {
  /* Models written by Liberate 18.1.0.293 from Cadence Design Systems, Inc. on Mon Feb  1 21:39:01 EST 2021 */
  comment : "";
  date : "$Date: Mon Feb  1 21:38:31 2021 $";
  revision : "1.0";
  delay_model : table_lookup;
//  capacitive_load_unit (1,pf);
  current_unit : "1mA";
  leakage_power_unit : "1nW";
  pulling_resistance_unit : "1kohm";
  time_unit : "1ns";
  voltage_unit : "1V";
//  voltage_map (VDD, 1);
//  voltage_map (VSS, 0);
  default_cell_leakage_power : 0;
  default_fanout_load : 1;
  default_max_transition : 0.3;
  default_output_pin_cap : 0;
  in_place_swap_mode : match_footprint;
  input_threshold_pct_fall : 50;
  input_threshold_pct_rise : 50;
  nom_process : 1;
  nom_temperature : 70;
  nom_voltage : 1;
  output_threshold_pct_fall : 50;
  output_threshold_pct_rise : 50;
  slew_derate_from_library : 1;
  slew_lower_threshold_pct_fall : 20;
  slew_lower_threshold_pct_rise : 20;
  slew_upper_threshold_pct_fall : 80;
  slew_upper_threshold_pct_rise : 80;
  operating_conditions (tt_1.0_70) {
    process : 1;
    temperature : 70;
    voltage : 1;
  }
  default_operating_conditions : tt_1.0_70;
  lu_table_template (const_template) {
    variable_1 : constrained_pin_transition;
    variable_2 : related_pin_transition;
//    index_1 ("0.006, 0.3");
//    index_2 ("0.006, 0.3");
  }
  lu_table_template (delay_template) {
    variable_1 : input_net_transition;
    variable_2 : total_output_net_capacitance;
//    index_1 ("0.006, 0.3");
//    index_2 ("0.0001, 0.07");
  }
  lu_table_template (mpw_const_template) {
    variable_1 : constrained_pin_transition;
//    index_1 ("0.006, 0.3");
  }
  power_lut_template (passive_power_template) {
    variable_1 : input_transition_time;
//    index_1 ("0.006, 0.3");
  }
  power_lut_template (power_template) {
    variable_1 : input_transition_time;
    variable_2 : total_output_net_capacitance;
//    index_1 ("0.006, 0.3");
//    index_2 ("0.0001, 0.07");
  }
  lu_table_template (waveform_template_name) {
    variable_1 : input_net_transition;
    variable_2 : normalized_voltage;
//    index_1 ("0, 1");
//    index_2 ("0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16");
  }
  normalized_driver_waveform (waveform_template_name) {
    driver_waveform_name : "PreDriver20.5:rise";
//    index_1 ("0.006, 0.3");
//    index_2 ("0, 0.05, 0.0543202, 0.126015, 0.2, 0.28178, 0.362839, 0.442588, 0.515655, 0.587655, 0.658428, 0.727955, 0.8, 0.849933, 0.897637, 0.949849, 1");
//    values ( \
//      "0, 0.001, 0.00105, 0.0015, 0.002, 0.0026, 0.00325, 0.00395, 0.00465, 0.0054, 0.0062, 0.00705, 0.008, 0.0087, 0.0094, 0.0102, 0.011", \
//      "0, 0.05, 0.0525, 0.075, 0.1, 0.13, 0.1625, 0.1975, 0.2325, 0.27, 0.31, 0.3525, 0.4, 0.435, 0.47, 0.51, 0.55" \
//    );
  }
  normalized_driver_waveform (waveform_template_name) {
    driver_waveform_name : "PreDriver20.5:fall";
//    index_1 ("0.006, 0.3");
//    index_2 ("0, 0.05, 0.0543202, 0.126015, 0.2, 0.28178, 0.362839, 0.442588, 0.515655, 0.587655, 0.658428, 0.727955, 0.8, 0.849933, 0.897637, 0.949849, 1");
//    values ( \
//      "0, 0.001, 0.00105, 0.0015, 0.002, 0.0026, 0.00325, 0.00395, 0.00465, 0.0054, 0.0062, 0.00705, 0.008, 0.0087, 0.0094, 0.0102, 0.011", \
//      "0, 0.05, 0.0525, 0.075, 0.1, 0.13, 0.1625, 0.1975, 0.2325, 0.27, 0.31, 0.3525, 0.4, 0.435, 0.47, 0.51, 0.55" \
//    );
  }
  normalized_driver_waveform (waveform_template_name) {
//    index_1 ("0.006, 0.3");
//    index_2 ("0, 0.05, 0.0543202, 0.126015, 0.2, 0.28178, 0.362839, 0.442588, 0.515655, 0.587655, 0.658428, 0.727955, 0.8, 0.849933, 0.897637, 0.949849, 1");
//    values ( \
//      "0, 0.001, 0.00105, 0.0015, 0.002, 0.0026, 0.00325, 0.00395, 0.00465, 0.0054, 0.0062, 0.00705, 0.008, 0.0087, 0.0094, 0.0102, 0.011", \
//      "0, 0.05, 0.0525, 0.075, 0.1, 0.13, 0.1625, 0.1975, 0.2325, 0.27, 0.31, 0.3525, 0.4, 0.435, 0.47, 0.51, 0.55" \
//    );
  }
  cell (INVX1_4) {
    area : 0;
    cell_leakage_power : 0.0921361;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0656144;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.118658;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0921361;
      related_pg_pin : VDD;
    }
    pin (Y) {
      direction : output;
      function : "!A";
      min_capacitance : 0.0001;
      power_down_function : "(!VDD) + (VSS)";
      related_ground_pin : VSS;
      related_power_pin : VDD;
      max_capacitance : 0.07;
      timing () {
        related_pin : "A";
        timing_sense : negative_unate;
        timing_type : combinational;
        cell_rise (delay_template) {
//          index_1 ("0.006, 0.3");
//          index_2 ("0.0001, 0.07");
//          values ( \
//            "0.011013, 0.366337", \
//            "0.080447, 0.540745" \
//          );
        }
        rise_transition (delay_template) {
//          index_1 ("0.006, 0.3");
//          index_2 ("0.0001, 0.07");
//          values ( \
//            "0.00686264, 0.5037", \
//            "0.0482119, 0.50379" \
//          );
        }
        cell_fall (delay_template) {
//          index_1 ("0.006, 0.3");
//          index_2 ("0.0001, 0.07");
//          values ( \
//            "0.00586106, 0.124964", \
//            "0.0285109, 0.293113" \
//          );
        }
        fall_transition (delay_template) {
//          index_1 ("0.006, 0.3");
//          index_2 ("0.0001, 0.07");
//          values ( \
//            "0.00280904, 0.16772", \
//            "0.0402187, 0.199308" \
//          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
//          index_1 ("0.006, 0.3");
//          index_2 ("0.0001, 0.07");
//          values ( \
//            "0.00111478, 0.00122939", \
//            "0.00113318, 0.00107976" \
//          );
        }
        fall_power (power_template) {
//          index_1 ("0.006, 0.3");
//          index_2 ("0.0001, 0.07");
//          values ( \
//            "4.34746e-05, 9.40774e-05", \
//            "8.66932e-05, 7.52027e-05" \
//          );
        }
      }
    }
    pin (A) {
      driver_waveform_fall : "PreDriver20.5:fall";
      driver_waveform_rise : "PreDriver20.5:rise";
      direction : input;
      related_ground_pin : VSS;
      related_power_pin : VDD;
      max_transition : 0.3;
      capacitance : 0.00129776;
      rise_capacitance : 0.00129776;
//      rise_capacitance_range (0.0010274, 0.00129776);
      fall_capacitance : 0.00129726;
//      fall_capacitance_range (0.00103831, 0.00129726);
    }
  }
}
"""
