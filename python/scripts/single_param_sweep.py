import os
from typing import Union, Sequence, Tuple
from logging import info
from functools import partial

from src.file_io import File
from src.liberate_grapher import graph_cell_delay
from src.netlist import BaseNetlistFile, Netlist
from src.liberate import liberate_simulator
from src.single_param_sweep import (
    Param,
    ParamSweepCandidateGenerator,
    SingleParamSweep,
    Simulator,
)


# pylint: disable=too-many-locals
def single_param_sweep(
    reference_netlist: str,
    param: Param,
    values: Sequence[Union[float, int]],
    graph_pin: str,
    graph_delay_index: Tuple[int, int],
    tcl_script: str,
    liberate_dir: str,
    netlist_dir: str,
    liberate_log: str,
    out_dir: str,
    ldb_name: str,
):
    if not os.path.isfile(reference_netlist):
        raise FileNotFoundError(reference_netlist)

    if not os.path.isdir(out_dir):
        info(f"Creating output directory {out_dir}")
        os.mkdir(out_dir)

    if not os.path.isdir(netlist_dir):
        info(f"Creating netlist working directory {netlist_dir}")
        os.mkdir(netlist_dir)

    def persist_netlist_in_run_dir(netlist: Netlist):
        netlist_file = File(os.path.join(netlist_dir, netlist.cell_name + ".sp"))
        netlist.persist(netlist_file)

    simulator: Simulator = partial(
        liberate_simulator,
        tcl_script=tcl_script,
        liberate_dir=liberate_dir,
        netlist_dir=netlist_dir,
        liberate_log=liberate_log,
        out_dir=out_dir,
        ldb_name=ldb_name,
    )

    candidate_generator = ParamSweepCandidateGenerator(
        reference_netlist=Netlist.create(BaseNetlistFile(File(reference_netlist))),
        netlist_persister=persist_netlist_in_run_dir,
        param=param,
        values=values,
    )
    search_algorithm = SingleParamSweep(
        simulator=simulator,
        candidate_generator=candidate_generator,
    )

    # Do the sweep
    info("Starting single parameter linear sweep.")
    search_algorithm.search()

    # Graph the results of simulation
    param_str = str(param)
    graph_cell_delay(
        ldb=search_algorithm.get_ldb(),
        pin=graph_pin,
        delay_index=graph_delay_index,
        x_axis=values,
        x_axis_title=param_str,
        out_path=f"{out_dir}/sweep-{param_str.lower()}.png",
    )
