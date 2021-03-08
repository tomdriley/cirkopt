# pylint: disable=too-many-lines
# This file contains full example LDB files

LIBERTY_EXAMPLE = r"""
library (example_tt_1.0_70) {
  /* Models written by Liberate 18.1.0.293 from Cadence Design Systems, Inc. on Sun Feb 14 11:56:51 EST 2021 */
  comment : "";
  date : "$Date: Sun Feb 14 11:55:04 2021 $";
  revision : "1.0";
  delay_model : table_lookup;
  capacitive_load_unit (1,pf);
  current_unit : "1mA";
  leakage_power_unit : "1nW";
  pulling_resistance_unit : "1kohm";
  time_unit : "1ns";
  voltage_unit : "1V";
  voltage_map (VDD, 1);
  voltage_map (VSS, 0);
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
    index_1 ("0.006, 0.3");
    index_2 ("0.006, 0.3");
  }
  lu_table_template (delay_template) {
    variable_1 : input_net_transition;
    variable_2 : total_output_net_capacitance;
    index_1 ("0.006, 0.3");
    index_2 ("0.0001, 0.07");
  }
  lu_table_template (mpw_const_template) {
    variable_1 : constrained_pin_transition;
    index_1 ("0.006, 0.3");
  }
  power_lut_template (passive_power_template) {
    variable_1 : input_transition_time;
    index_1 ("0.006, 0.3");
  }
  power_lut_template (power_template) {
    variable_1 : input_transition_time;
    variable_2 : total_output_net_capacitance;
    index_1 ("0.006, 0.3");
    index_2 ("0.0001, 0.07");
  }
  lu_table_template (waveform_template_name) {
    variable_1 : input_net_transition;
    variable_2 : normalized_voltage;
    index_1 ("0, 1");
    index_2 ("0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16");
  }
  normalized_driver_waveform (waveform_template_name) {
    driver_waveform_name : "PreDriver20.5:rise";
    index_1 ("0.006, 0.3");
    index_2 ("0, 0.05, 0.0543202, 0.126015, 0.2, 0.28178, 0.362839, 0.442588, 0.515655, 0.587655, 0.658428, 0.727955, 0.8, 0.849933, 0.897637, 0.949849, 1");
    values ( \
      "0, 0.001, 0.00105, 0.0015, 0.002, 0.0026, 0.00325, 0.00395, 0.00465, 0.0054, 0.0062, 0.00705, 0.008, 0.0087, 0.0094, 0.0102, 0.011", \
      "0, 0.05, 0.0525, 0.075, 0.1, 0.13, 0.1625, 0.1975, 0.2325, 0.27, 0.31, 0.3525, 0.4, 0.435, 0.47, 0.51, 0.55" \
    );
  }
  normalized_driver_waveform (waveform_template_name) {
    driver_waveform_name : "PreDriver20.5:fall";
    index_1 ("0.006, 0.3");
    index_2 ("0, 0.05, 0.0543202, 0.126015, 0.2, 0.28178, 0.362839, 0.442588, 0.515655, 0.587655, 0.658428, 0.727955, 0.8, 0.849933, 0.897637, 0.949849, 1");
    values ( \
      "0, 0.001, 0.00105, 0.0015, 0.002, 0.0026, 0.00325, 0.00395, 0.00465, 0.0054, 0.0062, 0.00705, 0.008, 0.0087, 0.0094, 0.0102, 0.011", \
      "0, 0.05, 0.0525, 0.075, 0.1, 0.13, 0.1625, 0.1975, 0.2325, 0.27, 0.31, 0.3525, 0.4, 0.435, 0.47, 0.51, 0.55" \
    );
  }
  normalized_driver_waveform (waveform_template_name) {
    index_1 ("0.006, 0.3");
    index_2 ("0, 0.05, 0.0543202, 0.126015, 0.2, 0.28178, 0.362839, 0.442588, 0.515655, 0.587655, 0.658428, 0.727955, 0.8, 0.849933, 0.897637, 0.949849, 1");
    values ( \
      "0, 0.001, 0.00105, 0.0015, 0.002, 0.0026, 0.00325, 0.00395, 0.00465, 0.0054, 0.0062, 0.00705, 0.008, 0.0087, 0.0094, 0.0102, 0.011", \
      "0, 0.05, 0.0525, 0.075, 0.1, 0.13, 0.1625, 0.1975, 0.2325, 0.27, 0.31, 0.3525, 0.4, 0.435, 0.47, 0.51, 0.55" \
    );
  }
  cell (INVX1_1) {
    area : 0.684;
    cell_footprint : "INV";
    cell_leakage_power : 0.0419087;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0252871;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0585303;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0419087;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00832102, 0.489515", \
            "0.0672285, 0.668921" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00473799, 0.679718", \
            "0.0474931, 0.679714" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00762433, 0.403115", \
            "0.0508851, 0.576593" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00387208, 0.558002", \
            "0.0469762, 0.557815" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.000515676, 0.000532389", \
            "0.000526963, 0.000499179" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "-1.06866e-05, 2.29925e-05", \
            "-7.57353e-06, 1.24871e-05" \
          );
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
      capacitance : 0.000534564;
      rise_capacitance : 0.000534564;
      rise_capacitance_range (0.000419181, 0.000534564);
      fall_capacitance : 0.00053418;
      fall_capacitance_range (0.000405789, 0.00053418);
    }
  }
  cell (INVX1_2) {
    area : 0;
    cell_leakage_power : 0.0308355;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0180438;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0436272;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0308355;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.0102831, 0.887086", \
            "0.0790586, 1.06402" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00712152, 1.2387", \
            "0.0530544, 1.23876" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00748415, 0.512267", \
            "0.0503829, 0.685214" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00419125, 0.711806", \
            "0.049188, 0.711775" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.000332321, 0.000333744", \
            "0.000339105, 0.00031275" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "5.18522e-05, 6.68114e-05", \
            "5.92076e-05, 6.3818e-05" \
          );
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
      capacitance : 0.000325899;
      rise_capacitance : 0.000325899;
      rise_capacitance_range (0.000255041, 0.000325899);
      fall_capacitance : 0.00032576;
      fall_capacitance_range (0.000250233, 0.00032576);
    }
  }
  cell (INVX1_3) {
    area : 0;
    cell_leakage_power : 0.0402848;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0239827;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0565869;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0402848;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00935542, 0.626023", \
            "0.0733304, 0.803784" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00578095, 0.871345", \
            "0.0492911, 0.871325" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00693003, 0.354652", \
            "0.0452878, 0.528981" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00342839, 0.489812", \
            "0.0458249, 0.490142" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.000460079, 0.000477935", \
            "0.000470185, 0.00044778" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "1.78626e-05, 4.35176e-05", \
            "2.60666e-05, 3.69194e-05" \
          );
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
      capacitance : 0.000487621;
      rise_capacitance : 0.000487621;
      rise_capacitance_range (0.000381212, 0.000487621);
      fall_capacitance : 0.000487424;
      fall_capacitance_range (0.000374154, 0.000487424);
    }
  }
  cell (INVX1_4) {
    area : 0;
    cell_leakage_power : 0.0527119;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0302401;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0751838;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0527119;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00880019, 0.478776", \
            "0.0711915, 0.658158" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00499155, 0.66391", \
            "0.0471397, 0.663896" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00656211, 0.267587", \
            "0.0402841, 0.441764" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00301863, 0.368213", \
            "0.0442559, 0.37289" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00058473, 0.000620399", \
            "0.000599821, 0.000573079" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "-1.64312e-05, 2.0742e-05", \
            "-3.91262e-06, 9.39519e-06" \
          );
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
      capacitance : 0.000648431;
      rise_capacitance : 0.000648431;
      rise_capacitance_range (0.000506406, 0.000648431);
      fall_capacitance : 0.000647943;
      fall_capacitance_range (0.000496935, 0.000647943);
    }
  }
  cell (INVX1_5) {
    area : 0;
    cell_leakage_power : 0.0646564;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0365597;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0927531;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0646564;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00846291, 0.388352", \
            "0.0696257, 0.567804" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00451463, 0.536668", \
            "0.0457931, 0.536651" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00634244, 0.215824", \
            "0.0371641, 0.3898" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00279269, 0.295907", \
            "0.0430901, 0.306558" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.000708463, 0.000755716", \
            "0.000729657, 0.000598" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "-5.12417e-05, -2.02331e-06", \
            "-3.49559e-05, -1.9504e-05" \
          );
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
      capacitance : 0.00080969;
      rise_capacitance : 0.00080969;
      rise_capacitance_range (0.000631629, 0.00080969);
      fall_capacitance : 0.000809206;
      fall_capacitance_range (0.000619401, 0.000809206);
    }
  }
  cell (INVX1_6) {
    area : 0;
    cell_leakage_power : 0.0785189;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0437469;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.113291;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0785189;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00817958, 0.32283", \
            "0.0672366, 0.501756" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00416405, 0.444895", \
            "0.0448263, 0.445742" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00618273, 0.181402", \
            "0.0347399, 0.354106" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.0026502, 0.248033", \
            "0.0423827, 0.263408" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.000834291, 0.000895776", \
            "0.000864675, 0.000646118" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "-8.67518e-05, -2.4787e-05", \
            "-6.07971e-05, -5.00498e-05" \
          );
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
      capacitance : 0.000970918;
      rise_capacitance : 0.000970918;
      rise_capacitance_range (0.000756715, 0.000970918);
      fall_capacitance : 0.000970119;
      fall_capacitance_range (0.000741904, 0.000970119);
    }
  }
  cell (INVX1_7) {
    area : 0;
    cell_leakage_power : 0.0920984;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0508982;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.133299;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0920984;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00796714, 0.276713", \
            "0.0654463, 0.456428" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00392245, 0.380251", \
            "0.0439822, 0.383278" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00607126, 0.156818", \
            "0.0330491, 0.330968" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00255807, 0.213582", \
            "0.041763, 0.235242" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.000957249, 0.00103578", \
            "0.000998892, 0.000846239" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "-0.000123022, -4.79343e-05", \
            "-8.6827e-05, -7.95311e-05" \
          );
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
      capacitance : 0.00113144;
      rise_capacitance : 0.00113127;
      rise_capacitance_range (0.000881615, 0.00113127);
      fall_capacitance : 0.00113144;
      fall_capacitance_range (0.000864691, 0.00113144);
    }
  }
  cell (INVX1_8) {
    area : 0;
    cell_leakage_power : 0.105498;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0580264;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.15297;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.105498;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00782771, 0.242445", \
            "0.0640842, 0.421923" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.0037493, 0.332128", \
            "0.0434084, 0.338033" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00599312, 0.138344", \
            "0.0318036, 0.311627" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00248957, 0.187851", \
            "0.0413691, 0.214097" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00108121, 0.00116872", \
            "0.00113333, 0.000908158" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "-0.00015899, -7.11158e-05", \
            "-0.000113291, -0.000111612" \
          );
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
      capacitance : 0.00129324;
      rise_capacitance : 0.00129324;
      rise_capacitance_range (0.00100685, 0.00129324);
      fall_capacitance : 0.00129265;
      fall_capacitance_range (0.000986922, 0.00129265);
    }
  }
  cell (INVX1_9) {
    area : 0;
    cell_leakage_power : 0.118778;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0651389;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.172417;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.118778;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00774737, 0.216002", \
            "0.0632206, 0.396036" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00363749, 0.295011", \
            "0.0429599, 0.303888" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00595691, 0.123996", \
            "0.0309008, 0.296176" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.0024496, 0.167634", \
            "0.0411013, 0.19859" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00121041, 0.0013138", \
            "0.00127051, 0.00111271" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "-0.000194965, -9.4262e-05", \
            "-0.000140333, -0.000143678" \
          );
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
      capacitance : 0.00145424;
      rise_capacitance : 0.00145424;
      rise_capacitance_range (0.00113175, 0.00145424);
      fall_capacitance : 0.00145248;
      fall_capacitance_range (0.00110945, 0.00145248);
    }
  }
  cell (INVX1_10) {
    area : 0;
    cell_leakage_power : 0.132367;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.072241;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.192493;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.132367;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00769541, 0.194961", \
            "0.0625122, 0.375119" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00355132, 0.265436", \
            "0.0427959, 0.277368" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00592777, 0.112425", \
            "0.0301818, 0.283755" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00241873, 0.151419", \
            "0.0408986, 0.18689" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00133992, 0.00145263", \
            "0.00141191, 0.00125156" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "-0.000230975, -0.000117127", \
            "-0.000166864, -0.000175497" \
          );
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
      capacitance : 0.00161487;
      rise_capacitance : 0.00161487;
      rise_capacitance_range (0.0012557, 0.00161487);
      fall_capacitance : 0.00161477;
      fall_capacitance_range (0.00123052, 0.00161477);
    }
  }
}
"""
LIBERTY_F3E7F6B4_EXAMPLE = r"""
library (example_tt_1.0_70) {
  /* Models written by Liberate 18.1.0.293 from Cadence Design Systems, Inc. on Sun Mar  7 14:19:52 EST 2021 */
  comment : "";
  date : "$Date: Sun Mar  7 14:18:11 2021 $";
  revision : "1.0";
  delay_model : table_lookup;
  capacitive_load_unit (1,pf);
  current_unit : "1mA";
  leakage_power_unit : "1nW";
  pulling_resistance_unit : "1kohm";
  time_unit : "1ns";
  voltage_unit : "1V";
  voltage_map (VDD, 1);
  voltage_map (VSS, 0);
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
    index_1 ("0.006, 0.3");
    index_2 ("0.006, 0.3");
  }
  lu_table_template (delay_template) {
    variable_1 : input_net_transition;
    variable_2 : total_output_net_capacitance;
    index_1 ("0.006, 0.3");
    index_2 ("0.0001, 0.07");
  }
  lu_table_template (mpw_const_template) {
    variable_1 : constrained_pin_transition;
    index_1 ("0.006, 0.3");
  }
  power_lut_template (passive_power_template) {
    variable_1 : input_transition_time;
    index_1 ("0.006, 0.3");
  }
  power_lut_template (power_template) {
    variable_1 : input_transition_time;
    variable_2 : total_output_net_capacitance;
    index_1 ("0.006, 0.3");
    index_2 ("0.0001, 0.07");
  }
  cell (INVX1_00) {
    area : 0;
    cell_leakage_power : 0.0308355;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0180438;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0436272;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0308355;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00958782, 0.886114", \
            "0.077001, 1.03111" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00712193, 1.23877", \
            "0.0500621, 1.23877" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00684512, 0.511206", \
            "0.0497121, 0.654289" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00406313, 0.711752", \
            "0.0482117, 0.711534" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.000329189, 0.000325682", \
            "0.000340793, 0.000263972" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "5.0248e-05, 6.79432e-05", \
            "6.34413e-05, 6.29983e-05" \
          );
        }
      }
    }
    pin (A) {
      direction : input;
      related_ground_pin : VSS;
      related_power_pin : VDD;
      max_transition : 0.3;
      capacitance : 0.00032571;
      rise_capacitance : 0.000325689;
      rise_capacitance_range (0.000252438, 0.000325689);
      fall_capacitance : 0.00032571;
      fall_capacitance_range (0.000247423, 0.00032571);
    }
  }
  cell (INVX1_01) {
    area : 0;
    cell_leakage_power : 0.0402848;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0239827;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0565869;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0402848;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00865761, 0.624445", \
            "0.0716466, 0.771535" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00578074, 0.871343", \
            "0.0466966, 0.871339" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00628653, 0.353642", \
            "0.0448028, 0.497867" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00324111, 0.489809", \
            "0.0452681, 0.489792" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.000455712, 0.000448015", \
            "0.000471108, 0.00041226" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "1.56884e-05, 4.51785e-05", \
            "3.27622e-05, 3.53862e-05" \
          );
        }
      }
    }
    pin (A) {
      direction : input;
      related_ground_pin : VSS;
      related_power_pin : VDD;
      max_transition : 0.3;
      capacitance : 0.000487459;
      rise_capacitance : 0.000487459;
      rise_capacitance_range (0.00037731, 0.000487459);
      fall_capacitance : 0.000487294;
      fall_capacitance_range (0.000368444, 0.000487294);
    }
  }
  cell (INVX1_02) {
    area : 0;
    cell_leakage_power : 0.0527119;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0302401;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0751838;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0527119;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00810281, 0.477693", \
            "0.0696473, 0.625731" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00499558, 0.663908", \
            "0.0447997, 0.663895" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00591146, 0.266565", \
            "0.0398355, 0.410741" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00280058, 0.368266", \
            "0.0438666, 0.368282" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.000579469, 0.000599387", \
            "0.000601249, 0.000538514" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "-1.95914e-05, 2.29847e-05", \
            "4.37976e-06, 6.97292e-06" \
          );
        }
      }
    }
    pin (A) {
      direction : input;
      related_ground_pin : VSS;
      related_power_pin : VDD;
      max_transition : 0.3;
      capacitance : 0.000648006;
      rise_capacitance : 0.000648006;
      rise_capacitance_range (0.000500963, 0.000648006);
      fall_capacitance : 0.000647718;
      fall_capacitance_range (0.000490971, 0.000647718);
    }
  }
  cell (INVX1_03) {
    area : 0;
    cell_leakage_power : 0.0646564;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0365597;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0927531;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0646564;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00776497, 0.387615", \
            "0.0682042, 0.536191" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00451478, 0.536667", \
            "0.0435081, 0.536623" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00570371, 0.215043", \
            "0.036798, 0.359447" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00254053, 0.295933", \
            "0.0429162, 0.297569" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.000703449, 0.000751551", \
            "0.000729888, 0.000657384" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "-5.50469e-05, -6.44977e-07", \
            "-2.32345e-05, -2.27052e-05" \
          );
        }
      }
    }
    pin (A) {
      direction : input;
      related_ground_pin : VSS;
      related_power_pin : VDD;
      max_transition : 0.3;
      capacitance : 0.000808181;
      rise_capacitance : 0.000808181;
      rise_capacitance_range (0.00062773, 0.000808181);
      fall_capacitance : 0.000808073;
      fall_capacitance_range (0.000617281, 0.000808073);
    }
  }
  cell (INVX1_04) {
    area : 0;
    cell_leakage_power : 0.0785189;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0437469;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.113291;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0785189;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.0074729, 0.321742", \
            "0.0658639, 0.470784" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.0041364, 0.444854", \
            "0.04261, 0.444853" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00556126, 0.180304", \
            "0.0343606, 0.324624" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00239097, 0.247941", \
            "0.0422835, 0.252228" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.000826256, 0.000862957", \
            "0.000864376, 0.000787864" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "-9.22666e-05, -2.19951e-05", \
            "-4.84349e-05, -5.36991e-05" \
          );
        }
      }
    }
    pin (A) {
      direction : input;
      related_ground_pin : VSS;
      related_power_pin : VDD;
      max_transition : 0.3;
      capacitance : 0.000968733;
      rise_capacitance : 0.000968733;
      rise_capacitance_range (0.000747975, 0.000968733);
      fall_capacitance : 0.000968432;
      fall_capacitance_range (0.00073335, 0.000968432);
    }
  }
  cell (INVX1_05) {
    area : 0;
    cell_leakage_power : 0.0920984;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0508982;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.133299;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.0920984;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00727783, 0.275992", \
            "0.0642094, 0.424754" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00387668, 0.38025", \
            "0.0419109, 0.380201" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00547658, 0.156046", \
            "0.0326779, 0.300249" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00228156, 0.213726", \
            "0.0418803, 0.221302" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.000949883, 0.00103153", \
            "0.000997255, 0.000910978" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "-0.000128191, -4.61153e-05", \
            "-7.26802e-05, -8.56213e-05" \
          );
        }
      }
    }
    pin (A) {
      direction : input;
      related_ground_pin : VSS;
      related_power_pin : VDD;
      max_transition : 0.3;
      capacitance : 0.00112943;
      rise_capacitance : 0.00112943;
      rise_capacitance_range (0.000876646, 0.00112943);
      fall_capacitance : 0.00112915;
      fall_capacitance_range (0.000862154, 0.00112915);
    }
  }
  cell (INVX1_06) {
    area : 0;
    cell_leakage_power : 0.105498;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0580264;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.15297;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.105498;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00714249, 0.241515", \
            "0.0629325, 0.39066" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00368741, 0.332198", \
            "0.041411, 0.332338" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00541058, 0.137426", \
            "0.0313581, 0.281823" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00220695, 0.187812", \
            "0.0413836, 0.19879" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.0010731, 0.00114256", \
            "0.00113166, 0.0010476" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "-0.000166134, -6.78015e-05", \
            "-9.81411e-05, -0.000118376" \
          );
        }
      }
    }
    pin (A) {
      direction : input;
      related_ground_pin : VSS;
      related_power_pin : VDD;
      max_transition : 0.3;
      capacitance : 0.00128949;
      rise_capacitance : 0.00128931;
      rise_capacitance_range (0.000996614, 0.00128931);
      fall_capacitance : 0.00128949;
      fall_capacitance_range (0.000976923, 0.00128949);
    }
  }
  cell (INVX1_07) {
    area : 0;
    cell_leakage_power : 0.118778;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.0651389;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.172417;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.118778;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00705347, 0.215003", \
            "0.0620683, 0.364127" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.0035648, 0.295029", \
            "0.0410675, 0.29597" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00538114, 0.123319", \
            "0.0305286, 0.267457" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00216084, 0.167764", \
            "0.0411597, 0.181739" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00119987, 0.00127206", \
            "0.00126963, 0.00114817" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "-0.000202909, -9.39192e-05", \
            "-0.000123617, -0.000152013" \
          );
        }
      }
    }
    pin (A) {
      direction : input;
      related_ground_pin : VSS;
      related_power_pin : VDD;
      max_transition : 0.3;
      capacitance : 0.00145005;
      rise_capacitance : 0.00145005;
      rise_capacitance_range (0.00112586, 0.00145005);
      fall_capacitance : 0.00144975;
      fall_capacitance_range (0.00109587, 0.00144975);
    }
  }
  cell (INVX1_08) {
    area : 0;
    cell_leakage_power : 0.132367;
    pg_pin (VDD) {
      pg_type : primary_power;
      voltage_name : "VDD";
    }
    pg_pin (VSS) {
      pg_type : primary_ground;
      voltage_name : "VSS";
    }
    leakage_power () {
      value : 0.072241;
      when : "A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.192493;
      when : "!A";
      related_pg_pin : VDD;
    }
    leakage_power () {
      value : 0.132367;
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
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00700079, 0.194214", \
            "0.0613619, 0.343146" \
          );
        }
        rise_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00347326, 0.265482", \
            "0.0408333, 0.267711" \
          );
        }
        cell_fall (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.0053614, 0.111614", \
            "0.0298176, 0.25586" \
          );
        }
        fall_transition (delay_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00212596, 0.151502", \
            "0.0409625, 0.168665" \
          );
        }
      }
      internal_power () {
        related_pin : "A";
        related_pg_pin : VDD;
        rise_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "0.00132857, 0.00145062", \
            "0.00140838, 0.00129012" \
          );
        }
        fall_power (power_template) {
          index_1 ("0.006, 0.3");
          index_2 ("0.0001, 0.07");
          values ( \
            "-0.000239024, -0.000114905", \
            "-0.000148729, -0.000185991" \
          );
        }
      }
    }
    pin (A) {
      direction : input;
      related_ground_pin : VSS;
      related_power_pin : VDD;
      max_transition : 0.3;
      capacitance : 0.00161064;
      rise_capacitance : 0.00161064;
      rise_capacitance_range (0.00124469, 0.00161064);
      fall_capacitance : 0.00160983;
      fall_capacitance_range (0.00122439, 0.00160983);
    }
  }
}
"""