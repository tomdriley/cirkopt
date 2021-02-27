import os
from typing import Union, Sequence, Tuple
from logging import info

from src.file_io import File
from src.liberty_parser import LibertyParser
from src.liberate_grapher import graph_cell_delay
from src.netlist import BaseNetlistFile, Netlist
from src.single_param_sweep import (
    NoopCostFunction,
    Param,
    ParamSweepCandidateGenerator,
    SingleParamSweep,
)


# pylint: disable=too-many-locals
def main(
    sim_result_rel_path: str,
    reference_netlist_rel_path: str,
    netlist_work_dir_rel_path: str,
    param: Param,
    values: Sequence[Union[float, int]],
    graph_pin: str,
    graph_delay_index: Tuple[int, int],
    out_dir_rel_path: str,
):
    curr_path = os.path.abspath(os.path.dirname(__file__))
    sim_result_path = os.path.join(curr_path, sim_result_rel_path)
    reference_netlist_path = os.path.join(curr_path, reference_netlist_rel_path)
    netlist_work_dir_path = os.path.join(curr_path, netlist_work_dir_rel_path)
    out_dir_path = os.path.join(curr_path, out_dir_rel_path)

    if not os.path.isfile(reference_netlist_path):
        raise FileNotFoundError(reference_netlist_path)

    if not os.path.isdir(netlist_work_dir_path):
        raise NotADirectoryError(netlist_work_dir_path)

    if not os.path.isdir(out_dir_path):
        info(f"Creating output directory {out_dir_path}")
        os.mkdir(out_dir_path)

    def persist_netlist_in_run_dir(netlist: Netlist):
        netlist_file = File(f"{netlist_work_dir_path}/{netlist.cell_name}.sp")
        netlist.persist(netlist_file)

    sim_file = File(sim_result_path)
    candidate_generator = ParamSweepCandidateGenerator(
        reference_netlist=Netlist(BaseNetlistFile(File(reference_netlist_path))),
        netlist_persister=persist_netlist_in_run_dir,
        param=param,
        values=values,
    )
    single_param_sweep = SingleParamSweep(
        NoopCostFunction(), candidate_generator, LibertyParser(), sim_file
    )

    # Do the sweep
    info("Starting single parameter linear sweep.")
    single_param_sweep.search()

    # Graph the results of simulation
    param_str = str(param)
    info("Generating graph of results.")
    graph_cell_delay(
        sim_file=sim_file,
        pin=graph_pin,
        delay_index=graph_delay_index,
        x_axis=values,
        x_axis_title=param_str,
        out_path=f"{out_dir_path}/sweep-{param_str.lower()}.png",
    )


if __name__ == "__main__":
    # TODO: use command line args instead of hard coding
    main(
        sim_result_rel_path="../../liberate/lib/example_tt_1.0_70_nldm.lib",
        reference_netlist_rel_path="../../liberate/netlist_ref/INVX1.sp",
        netlist_work_dir_rel_path="../../liberate/netlist_wrk",
        param=Param.WIDTH,
        values=[i * 100e-9 for i in range(2, 11)],
        graph_pin="Y",
        graph_delay_index=(0, 1),
        out_dir_rel_path="../out",
    )
