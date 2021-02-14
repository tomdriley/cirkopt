import textwrap
import unittest

from src.liberate_template_utils import update_liberate_template_cell_names
from tests.mock_file import MockFile

EXAMPLE_TEMPLATE_FILE = """
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
    AND2X1_2
    BUFX8_2
    BUFX8_drv_2
    INVX1_2
    XOR2X1_2
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
    $cells"""


class TestLiberateTemplateUtils(unittest.TestCase):

    def test_update_liberate_template_cell_names(self):
        template_file = MockFile()
        template_file.write(EXAMPLE_TEMPLATE_FILE)

        backup_file = MockFile()

        update_liberate_template_cell_names(
            file=template_file,
            cell_names=[f'INVX1_{i}' for i in range(5)],
            backup_file=backup_file
        )

        # Test backup file is unmodified copy of original
        self.assertEqual(EXAMPLE_TEMPLATE_FILE, backup_file.read())

        old_cells = textwrap.dedent("""
        set cells {
            AND2X1_2
            BUFX8_2
            BUFX8_drv_2
            INVX1_2
            XOR2X1_2
        }
        """)
        new_cells = textwrap.dedent("""
        set cells {
            INVX1_0
            INVX1_1
            INVX1_2
            INVX1_3
            INVX1_4
        }
        """)

        expected_new_template_file_contents = EXAMPLE_TEMPLATE_FILE.replace(old_cells, new_cells)
        self.assertEqual(expected_new_template_file_contents, template_file.read())
