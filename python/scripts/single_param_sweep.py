import os
from typing import Union, Sequence, Tuple
from logging import info

from src.file_io import File
from src.liberate_grapher import graph_cell_delay
from src.netlist import BaseNetlistFile, Netlist
from src.single_param_sweep import (
    ParamSweepCandidateGenerator,
    SingleParamSweep,
)
from src.circuit_search_common import Param


# pylint: disable=too-many-locals
def main(
    reference_netlist_rel_path: str,
    netlist_work_dir_rel_path: str,
    param: Param,
    values: Sequence[Union[float, int]],
    graph_pin: str,
    graph_delay_index: Tuple[int, int],
    out_dir_rel_path: str,
):
    curr_path = os.path.abspath(os.path.dirname(__file__))
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

    candidate_generator = ParamSweepCandidateGenerator(
        reference_netlist=Netlist.create(BaseNetlistFile(File(reference_netlist_path))),
        netlist_persister=persist_netlist_in_run_dir,
        param=param,
        values=values,
    )
    single_param_sweep = SingleParamSweep(candidate_generator)

    # Do the sweep
    info("Starting single parameter linear sweep.")
    single_param_sweep.search()

    # Graph the results of simulation
    param_str = str(param)
    graph_cell_delay(
        ldb=single_param_sweep.get_ldb(),
        pin=graph_pin,
        delay_index=graph_delay_index,
        x_axis=values,
        x_axis_title=param_str,
        out_path=f"{out_dir_path}/sweep-{param_str.lower()}.png",
    )
