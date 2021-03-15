import os
from logging import info

from src.file_io import File
from src.netlist import BaseNetlistFile, Netlist
from src.brute_force_search import (
    BruteForceCandidateGenerator,
    BruteForceSearch,
)
from src.circuit_search_common import Range


# pylint: disable=too-many-locals
def main(
    reference_netlist_rel_path: str,
    netlist_work_dir_rel_path: str,
    width: Range[float],
    length: Range[float],
    fingers: Range[int],
    simulations_per_iteration: int,
):
    curr_path = os.path.abspath(os.path.dirname(__file__))
    reference_netlist_path = os.path.join(curr_path, reference_netlist_rel_path)
    netlist_work_dir_path = os.path.join(curr_path, netlist_work_dir_rel_path)

    if not os.path.isfile(reference_netlist_path):
        raise FileNotFoundError(reference_netlist_path)

    if not os.path.isdir(netlist_work_dir_path):
        raise NotADirectoryError(netlist_work_dir_path)

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
        simulations_per_iteration=simulations_per_iteration
    )
    brute_force = BruteForceSearch(candidate_generator)

    # Do the sweep
    info("Starting brute force search.")
    best_netlist = brute_force.search()
    info("Search complete")
    info(f"Best Netlist: {best_netlist.cell_name} in {netlist_work_dir_path}")
