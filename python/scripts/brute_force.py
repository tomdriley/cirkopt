import os
from typing import Tuple
from logging import info

from src.file_io import File
from src.netlist import BaseNetlistFile, Netlist
from src.brute_force_search import (
    Range,
    BruteForceCandidateGenerator,
    BruteForceSearch,
)


# pylint: disable=too-many-locals
def main(
    reference_netlist_rel_path: str,
    netlist_work_dir_rel_path: str,
    width: Range[float],
    length: Range[float],
    fingers: Range[int],
    simulations_per_iterations: int,
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

    reference_netlist_file = BaseNetlistFile(File(reference_netlist_path))
    candidate_generator = BruteForceCandidateGenerator.create(
        reference_netlist=Netlist.create(reference_netlist_file),
        netlist_persister=persist_netlist_in_run_dir,
        width_range=width,
        length_range=length,
        fingers_range=fingers,
        simulations_per_iterations=simulations_per_iterations
    )
    single_param_sweep = BruteForceSearch(candidate_generator)

    # Do the sweep
    info("Starting brute force search.")
    single_param_sweep.search()

    # Graph the results of simulation
    # Todo graph
