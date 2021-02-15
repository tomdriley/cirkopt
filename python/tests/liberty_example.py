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
