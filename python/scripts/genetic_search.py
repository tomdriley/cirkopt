import os
from functools import partial
import logging
from logging import info, debug
from typing import Tuple, Optional

import matplotlib.pyplot as plt  # type: ignore

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
    reference_netlist: str,
    max_iterations: int,
    num_individuals: int,
    elitism: bool,
    npoints: int,
    alpha: float,
    pmutation: float,
    mutation_std_deviation: float,
    min_width: float,
    max_width: float,
    min_length: float,
    max_length: float,
    min_fingers: int,
    max_fingers: int,
    precision: str,
    delay_index: Tuple[int, int],
    seed: Optional[int],
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
        netlist_dir=netlist_dir,
        liberate_log=liberate_log,
        out_dir=out_dir,
        ldb_name=ldb_name,
    )

    # Validates npoints
    candidate_generator = GeneticCandidateGenerator.create(
        num_individuals,
        elitism,
        npoints,
        alpha,
        pmutation,
        mutation_std_deviation,
        min_width,
        max_width,
        min_length,
        max_length,
        min_fingers,
        max_fingers,
        precision,
        Netlist.create(BaseNetlistFile(File(reference_netlist))),
        seed=seed,
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
    info(f"Find netlist is named {best_netlist.cell_name} in {netlist_dir}")

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
