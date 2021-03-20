import os
from functools import partial
from logging import info, debug
from typing import Tuple, TypeVar
from math import floor, ceil
from decimal import Decimal

from src.file_io import File
from src.netlist import BaseNetlistFile, Netlist
from src.netlist_cost_functions import delay_cost_function
from src.liberate import liberate_simulator
from src.brute_force_search import (
    BruteForceCandidateGenerator,
    BruteForceSearch,
    CostFunction,
    Simulator,
)
from src.circuit_search_common import Range


# pylint: disable=too-many-locals
def brute_force_search(
    reference_netlist_path: str,
    tcl_script: str,
    liberate_dir: str,
    out_dir: str,
    delay_index: Tuple[int, int],
    width: Range[Decimal],
    length: Range[Decimal],
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

    reference_netlist = Netlist.create(BaseNetlistFile.create(File(reference_netlist_path)))

    T = TypeVar("T", Decimal, int)

    def num_steps(_range: Range[T]) -> int:
        return floor((_range.high - _range.low) / _range.step_size) + 1

    num_width = num_steps(width)
    debug(f"Running with {num_width} values for width")
    num_length = num_steps(length)
    debug(f"Running with {num_length} values for length")
    num_fingers = num_steps(fingers)
    debug(f"Running with {num_fingers} values for fingers")
    num_devices = len(reference_netlist.device_widths)
    debug(f"Varying those across {num_devices} devices")
    num_iterations = ceil(
        ((num_width * num_length * num_fingers) ** num_devices) / simulations_per_iteration
    )
    info(f"Running {num_iterations} iterations")
    info(f"with {simulations_per_iteration} simulations per iteration")

    candidate_generator = BruteForceCandidateGenerator.create(
        reference_netlist=reference_netlist,
        width_range=width,
        length_range=length,
        fingers_range=fingers,
        simulations_per_iteration=simulations_per_iteration,
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
    best_netlist = best_netlist.clone(cell_name=reference_netlist.cell_name)
    best_netlist_path = os.path.join(out_dir, best_netlist.cell_name + ".sp")
    best_netlist.persist(File(best_netlist_path))
    info(f"Find optimized netlist at {best_netlist_path}")
