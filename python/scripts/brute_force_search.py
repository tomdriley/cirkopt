import os
from functools import partial
from logging import info
from typing import Tuple


from src.file_io import File
from src.netlist import BaseNetlistFile, Netlist
from src.netlist_cost_functions import delay_cost_function
from src.liberate import liberate_simulator
from src.brute_force_search import (
    BruteForceCandidateGenerator,
    BruteForceSearch,
    CostFunction,
    Simulator
)
from src.circuit_search_common import Range


# pylint: disable=too-many-locals
def brute_force_search(
    reference_netlist_path: str,
    tcl_script: str,
    liberate_dir: str,
    out_dir: str,
    delay_index: Tuple[int, int],
    width: Range[float],
    length: Range[float],
    fingers: Range[int],
    simulations_per_iteration: int,
):
    if not os.path.isfile(reference_netlist_path):
        raise FileNotFoundError(reference_netlist_path)

    if not os.path.isdir(out_dir):
        info(f"Creating output directory {out_dir}")
        os.mkdir(out_dir)

    simulator: Simulator = partial(
        liberate_simulator,
        tcl_script=tcl_script,
        liberate_dir=liberate_dir,
        out_dir=out_dir,
    )

    reference_netlist = Netlist.create(BaseNetlistFile(File(reference_netlist_path)))
    candidate_generator = BruteForceCandidateGenerator.create(
        reference_netlist=reference_netlist,
        width_range=width,
        length_range=length,
        fingers_range=fingers,
        simulations_per_iteration=simulations_per_iteration
    )
    cost_function: CostFunction = partial(
        delay_cost_function,
        delay_idx=delay_index,
    )
    brute_force = BruteForceSearch(
        simulator=simulator,
        candidate_generator=candidate_generator,
        cost_function=cost_function,  # TODO: parameterize when there are more cost functions
    )

    # Do the sweep
    info("Starting brute force search...")
    best_netlist = brute_force.search()
    info("Search complete")
    best_netlist.mutate(
        cell_name=reference_netlist.cell_name,
        device_widths=best_netlist.device_widths,
        device_lengths=best_netlist.device_lengths,
        device_fingers=best_netlist.device_fingers,
    )
    best_netlist_path = os.path.join(out_dir, best_netlist.cell_name + ".sp")
    best_netlist.persist(File(best_netlist_path))
    info(f"Find optimized netlist at {reference_netlist}")
