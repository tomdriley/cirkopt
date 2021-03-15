import os
from functools import partial
import logging
from logging import info, debug
from typing import Tuple

import matplotlib.pyplot as plt  # type: ignore

from src.file_io import File
from src.netlist import BaseNetlistFile, Netlist
from src.netlist_cost_functions import delay_cost_function
from src.genetic_search import (
    CostFunction,
    GeneticCandidateGenerator,
    GeneticSearch,
)


# pylint: disable=too-many-locals
def main(
    reference_netlist_rel_path: str,
    netlist_work_dir_rel_path: str,
    out_dir_rel_path: str,
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

    if num_individuals < 2:
        raise ValueError("Number of individuals must be at least 2")

    if not 0 < alpha < 1:
        raise ValueError("alpha should be strictly between 0 and 1")

    if not 0 < pmutation < 1:
        raise ValueError("pmutation should be strictly between 0 and 1")

    if mutation_std_deviation <= 0:
        raise ValueError("mutation_std_deviation should be greater than 0")

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
        Netlist.create(BaseNetlistFile(File(reference_netlist_path))),
        persist_netlist_in_run_dir,
        seed=1234,  # Make it reproducible
    )

    cost_function: CostFunction = partial(delay_cost_function, delay_idx=delay_index)
    genetic_search = GeneticSearch(
        candidate_generator,
        cost_function,  # TODO: parameterize when there are more cost functions
        max_iterations,
    )

    # Do the sweep
    info("Starting genetic search.")
    best_netlist = genetic_search.search()
    info("Search complete")
    info(f"Find netlist is named {best_netlist.cell_name} in {netlist_work_dir_path}")

    mpl_logger = logging.getLogger("matplotlib")
    if logging.getLogger().getEffectiveLevel() < logging.WARNING:
        debug("Suppressing matplotlib logs below warning.")
        mpl_logger.setLevel(logging.WARNING)

    # Graph the results of search
    plt.figure()
    plt.title("Minimum cost per iteration")
    plt.plot(genetic_search.min_cost_per_iteration, "b")
    plt.ylabel("Cost")
    plt.ylim(bottom=0)
    plt.xlabel("Iteration number")
    plt.tight_layout()
    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.minorticks_on()
    ax.grid(which="major", linestyle="-", linewidth="0.5", color="red")
    ax.grid(which="minor", linestyle=":", linewidth="0.5", color="black")
    plt.savefig(f"{out_dir_path}/genetic-cost-per-iteration.png")
