import os.path

from file_io import File
from netlist import BaseNetlistFile, Netlist


def main() -> None:
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../../liberate/netlist_wrk/INVX1_2.sp")

    netlist_file = File(path)

    base_netlist_file = BaseNetlistFile(netlist_file)

    netlist = Netlist(base_netlist_file)

    new_netlist = netlist.mutate(
        cell_name="INVX1_4",
        device_widths=(260e-9, 310e-9),
        device_lengths=(50e-9, 60e-9),
        device_fingers=(2, 3)
    )
    path = os.path.join(my_path, "../../liberate/netlist_test/INVX1_4.sp")
    new_netlist.persist(File(path))


if __name__ == '__main__':
    main()
