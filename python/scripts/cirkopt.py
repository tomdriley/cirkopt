#!/usr/bin/env python3

# Set up path relative to python root folder so we can find the other packages
import sys
import os.path
import argparse
import logging
from logging import DEBUG, debug, INFO, info, WARNING, error
from random import randint
from typing import Type, TypeVar
from textwrap import dedent
from decimal import Decimal

import numpy as np

PYTHON_SCRIPTS_DIRECTORY: str = os.path.dirname(os.path.abspath(__file__))
PYTHON_DIRECTORY: str = os.path.abspath(os.path.join(PYTHON_SCRIPTS_DIRECTORY, ".."))
LIBERATE_DIRECTORY: str = os.path.abspath(os.path.join(PYTHON_DIRECTORY, "../liberate"))
sys.path.append(PYTHON_DIRECTORY)

# These imports rely on changed sys.path
from scripts.brute_force_search import brute_force_search  # pylint: disable=wrong-import-position
from scripts.genetic_search import genetic_search  # pylint: disable=wrong-import-position
from scripts.single_param_sweep import single_param_sweep  # pylint: disable=wrong-import-position
from src.circuit_search_common import Param, Range  # pylint: disable=wrong-import-position


RangeType = TypeVar("RangeType", int, Decimal)


def _range(param: Param, _type: Type[RangeType], string: str) -> Range[RangeType]:
    params = string.split(":")
    if len(params) != 3:
        raise ValueError("Range should be formatted as low:step_size:high (inclusive")
    low, step_size, high = tuple(map(_type, params))
    return Range(param, low, high, step_size)


def width(string: str) -> Range[Decimal]:
    return _range(Param.WIDTH, Decimal, string)


def length(string: str) -> Range[Decimal]:
    return _range(Param.LENGTH, Decimal, string)


def fingers(string: str) -> Range[int]:
    return _range(Param.FINGERS, int, string)


def _add_common_args(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--outdir",
        help="Directory to place results in, e.g. graphs, netlists, ldb.",
        default=os.path.join(PYTHON_DIRECTORY, "out"),
    )
    parser.add_argument(
        "--netlist",
        help="Path to reference netlist to modify. ",
        default=os.path.join(LIBERATE_DIRECTORY, "netlist/INVX1.sp"),
    )
    parser.add_argument(
        "--tclscript",
        help="Characterization tcl script with liberate settings and templates",
        default=os.path.join(LIBERATE_DIRECTORY, "tcl/char.tcl"),
    )
    parser.add_argument(
        "--debug",
        help="Print lots of debugging statements",
        action="store_const",
        dest="loglevel",
        const=DEBUG,
        default=WARNING,
    )
    parser.add_argument(
        "--verbose",
        help="Be verbose",
        action="store_const",
        dest="loglevel",
        const=INFO,
    )
    parser.add_argument(
        "--outindex",
        help="Index of value from LDB table to show, space separated, e.g.: 0 1",
        nargs=2,
        type=int,
        default=[0, 0],
    )

def _init_logger(loglevel: int, outdir: str) -> None:
    create_outdir = not os.path.isdir(outdir)

    if create_outdir:
        os.mkdir(outdir)

    logging.basicConfig(
        format="%(levelname)s (%(asctime)s): %(message)s",
        datefmt="%I:%M:%S %p",
        level=loglevel,
        handlers=[
            logging.FileHandler(os.path.join(outdir, "cirkopt.log")),
            logging.StreamHandler(sys.stdout),
        ],
    )

    if create_outdir:
        info(f"Created output directory {outdir}")



# Basically a copy of this blog post [1].
# [1] https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html
class Cirkopt:
    def __init__(self):
        usage = """
                cirkopt <command> [<args>]

                The most commonly used commands are:
                explore       Generate plots showing search space
                search        Find an optimal design using genetic algorithm
                brute_force   Find optimal design using exhaustive search"""
        parser = argparse.ArgumentParser(description="SPICE circuit optimizer", usage=dedent(usage))
        parser.add_argument("command", help="Sub command to run")
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            error("Unrecognized command")
            parser.print_help()
            sys.exit()
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    # pylint: disable=no-self-use
    def explore(self):
        parser = argparse.ArgumentParser(
            description="Generate plots showing search space",
        )
        # prefixing the argument with -- means it's optional
        parser.add_argument(
            "--param",
            help="Paramater to sweep, e.g.: width",
            type=lambda input: Param[input.upper()],
            choices=tuple(Param),
            default=Param.WIDTH,
        )
        parser.add_argument(
            "--range",
            help=(
                "Range of numbers to sweep over, start then end, space separated"
                + " e.g.: 200e-9 1e-6"
            ),
            nargs=2,
            type=float,
            default=[200e-9, 1e-6],
        )
        parser.add_argument(
            "--numsteps",
            help="Number of values to simulate within range, e.g. 9",
            type=int,
            default=9,
        )
        parser.add_argument(
            "--outpin",
            help="Name of pin to get data from, e.g.: Y",
            default="Y",
        )

        _add_common_args(parser)

        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (cirkopt) and the subcommand (explore)
        args = parser.parse_args(sys.argv[2:])

        _init_logger(args.loglevel, args.outdir)

        # Print all the arguments given
        for key in args.__dict__:
            debug(f"{key:<10}: {args.__dict__[key]}")

        # Additional parsing
        values = np.linspace(start=args.range[0], stop=args.range[1], num=args.numsteps)
        debug(f"values: {values}")

        info("Exploring search space.")
        single_param_sweep(
            reference_netlist=args.netlist,
            param=args.param,
            values=values,
            graph_pin=args.outpin,
            graph_delay_index=args.outindex,
            tcl_script=args.tclscript,
            liberate_dir=LIBERATE_DIRECTORY,
            out_dir=args.outdir,
        )

    # pylint: disable=no-self-use
    def search(self):
        parser = argparse.ArgumentParser(
            description="Use genetic search to find optimal design",
        )
        parser.add_argument(
            "--iterations",
            help="Number of search iterations to run",
            type=int,
            default=100,
        )
        parser.add_argument(
            "--individuals",
            help="Number of search individuals per population",
            type=int,
            default=10,
        )
        parser.add_argument(
            "--elitism",
            help="If the best candidate should continue to next population",
            type=bool,
            default=True,
        )
        parser.add_argument(
            "--npoints",
            help="Number of crossover points, should be less than number of devices * 3",
            type=int,
            default=2,
        )
        parser.add_argument(
            "--alpha",
            help="Alpha for n point crossover",
            type=float,
            default=0.5,
        )
        parser.add_argument(
            "--pmutation",
            help="Probability of adding gaussian noise mutation to a given device param within a candidate",
            type=float,
            default=0.05,
        )
        parser.add_argument(
            "--mutation-std-dev",
            help="Standard deviation of additive gaussian noise mutation",
            type=float,
            default=5.0,
        )
        parser.add_argument(
            "--width",
            help="Defines the range of widths a device may have, eg.: low:step_size:high (inclusive)",
            type=width,
            default="120e-9:5e-9:1e-6",
        )
        parser.add_argument(
            "--length",
            help="Defines the range of lengths a device may have, eg.: low:step_size:high (inclusive)",
            type=length,
            default="45e-9:1e-9:45e-9",
        )
        parser.add_argument(
            "--fingers",
            help="Defines the range of fingers a device may have, eg.: low:step_size:high (inclusive)",
            type=fingers,
            default="1:1:1",
        )
        parser.add_argument(
            "--seed",
            help="Removes randomization on the initial seed to make the results more reproducable",
            type=int,
            default=randint(0, 2 ** 32),
        )

        _add_common_args(parser)

        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (cirkopt) and the subcommand (explore)
        args = parser.parse_args(sys.argv[2:])

        _init_logger(args.loglevel, args.outdir)

        # Print all the arguments given
        for key in args.__dict__:
            debug(f"{key:<10}: {args.__dict__[key]}")

        genetic_search(
            reference_netlist_path=args.netlist,
            max_iterations=args.iterations,
            num_individuals=args.individuals,
            elitism=args.elitism,
            npoints=args.npoints,
            alpha=args.alpha,
            pmutation=args.pmutation,
            mutation_std_deviation=args.mutation_std_dev,
            width_range=args.width,
            length_range=args.length,
            fingers_range=args.fingers,
            delay_index=tuple(args.outindex),
            seed=args.seed,
            tcl_script=args.tclscript,
            liberate_dir=LIBERATE_DIRECTORY,
            out_dir=args.outdir,
        )

    # pylint: disable=no-self-use
    def brute_force(self):
        parser = argparse.ArgumentParser(
            description="Perform exhaustive search to optimize netlist",
        )
        parser.add_argument(
            "--width",
            help="Defines the range of widths a device may have, eg.: low:step_size:high (inclusive)",
            type=width,
            default="120e-9:5e-9:1e-6",
        )
        parser.add_argument(
            "--length",
            help="Defines the range of lengths a device may have, eg.: low:step_size:high (inclusive)",
            type=length,
            default="45e-9:1e-9:45e-9",
        )
        parser.add_argument(
            "--fingers",
            help="Defines the range of fingers a device may have, eg.: low:step_size:high (inclusive)",
            type=fingers,
            default="1:1:1",
        )
        parser.add_argument(
            "--simulations-per-iteration",
            help="Defines how many netlists to simulate to run per iteration.",
            type=int,
            default=10,
        )

        _add_common_args(parser)

        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (cirkopt) and the subcommand (explore)
        args = parser.parse_args(sys.argv[2:])

        _init_logger(args.loglevel, args.outdir)

        # Print all the arguments given
        for key in args.__dict__:
            debug(f"{key:<10}: {args.__dict__[key]}")

        info("Exploring search space.")
        brute_force_search(
            reference_netlist_path=args.netlist,
            tcl_script=args.tclscript,
            liberate_dir=LIBERATE_DIRECTORY,
            out_dir=args.outdir,
            delay_index=tuple(args.outindex),
            width=args.width,
            length=args.length,
            fingers=args.fingers,
            simulations_per_iteration=args.simulations_per_iteration,
        )


if __name__ == "__main__":
    Cirkopt()
