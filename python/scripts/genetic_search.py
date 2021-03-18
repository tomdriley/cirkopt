import os
from functools import partial
import logging
from logging import info, debug
from typing import Tuple, Optional
from decimal import Decimal

import matplotlib.pyplot as plt  # type: ignore

from src.circuit_search_common import Range
from src.file_io import File
from src.netlist import BaseNetlistFile, Netlist
from src.netlist_cost_functions import delay_cost_function
from src.liberate import liberate_simulator
from src.genetic_search import (
    CostFunction,
    GeneticCandidateGenerator,
    GeneticSearch,
    Simulator,
)


# pylint: disable=too-many-locals
def genetic_search(
    reference_netlist_path: str,
    max_iterations: int,
    num_individuals: int,
    elitism: bool,
    npoints: int,
    alpha: float,
    pmutation: float,
    mutation_std_deviation: float,
    width_range: Range[Decimal],
    length_range: Range[Decimal],
    fingers_range: Range[int],
    delay_index: Tuple[int, int],
    seed: Optional[int],
    tcl_script: str,
    liberate_dir: str,
    out_dir: str,
    initial_candidates: Optional[str],
):
    if not os.path.isfile(reference_netlist_path):
        raise FileNotFoundError(reference_netlist_path)

    if not os.path.isdir(out_dir):
        info(f"Creating output directory {out_dir}")
        os.mkdir(out_dir)

    if num_individuals < 2:
        raise ValueError("Number of individuals must be at least 2")

    if not 0 < alpha < 1:
        raise ValueError("alpha should be strictly between 0 and 1")

    if not 0 < pmutation < 1:
        raise ValueError("pmutation should be strictly between 0 and 1")

    if mutation_std_deviation <= 0:
        raise ValueError("mutation_std_deviation should be greater than 0")

    simulator: Simulator = partial(
        liberate_simulator,
        tcl_script=tcl_script,
        liberate_dir=liberate_dir,
        out_dir=out_dir,
    )

    reference_netlist: Netlist = Netlist.create(BaseNetlistFile(File(reference_netlist_path)))
    debug(f"Reference netlist name: {reference_netlist.cell_name}")

    # Validates npoints
    candidate_generator = GeneticCandidateGenerator.create(
        num_individuals,
        elitism,
        npoints,
        alpha,
        pmutation,
        mutation_std_deviation,
        width_range,
        length_range,
        fingers_range,
        reference_netlist,
        seed=seed,
        initial_candidates=initial_candidates,
    )

    cost_function: CostFunction = partial(
        delay_cost_function,
        delay_idx=delay_index,
    )

    search_algorithm = GeneticSearch(
        simulator=simulator,
        candidate_generator=candidate_generator,
        cost_function=cost_function,  # TODO: parameterize when there are more cost functions
        max_iterations=max_iterations,
    )

    # Do the sweep
    info("Starting genetic search.")
    best_netlist = search_algorithm.search()
    info("Search complete")
    debug(f"Reference netlist name: {reference_netlist.cell_name}")
    best_netlist = best_netlist.clone(cell_name=reference_netlist.cell_name)
    best_netlist_path = os.path.join(out_dir, best_netlist.cell_name + ".sp")
    best_netlist.persist(File(best_netlist_path))
    info(f"Find netlist is named {best_netlist.cell_name} in {best_netlist_path}")

    mpl_logger = logging.getLogger("matplotlib")
    if logging.getLogger().getEffectiveLevel() < logging.WARNING:
        debug("Suppressing matplotlib logs below warning.")
        mpl_logger.setLevel(logging.WARNING)

    # Graph the results of search
    plt.figure()
    plt.title("Minimum cost per iteration")
    plt.plot(search_algorithm.min_cost_per_iteration, "b")
    plt.ylabel("Cost")
    plt.ylim(bottom=0)
    plt.xlabel("Iteration number")
    plt.tight_layout()
    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.minorticks_on()
    ax.grid(which="major", linestyle="-", linewidth="0.5", color="red")
    ax.grid(which="minor", linestyle=":", linewidth="0.5", color="black")
    plt.savefig(f"{out_dir}/genetic-cost-per-iteration.png")
