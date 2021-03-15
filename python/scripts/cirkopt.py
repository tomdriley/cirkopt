#!/usr/bin/env python3

# Set up path relative to python root folder so we can find the other packages
import sys
import os.path
import argparse
import logging
from logging import DEBUG, debug, INFO, info, WARNING, error
from random import randint

import numpy as np

PYTHON_SCRIPTS_DIRECTORY: str = os.path.dirname(os.path.abspath(__file__))
PYTHON_DIRECTORY: str = os.path.abspath(os.path.join(PYTHON_SCRIPTS_DIRECTORY, ".."))
LIBERATE_DIRECTORY: str = os.path.abspath(os.path.join(PYTHON_DIRECTORY, "../liberate"))
sys.path.append(PYTHON_DIRECTORY)

# These imports rely on changed sys.path
from scripts.genetic_search import (  # pylint: disable=wrong-import-position
    genetic_search,
)
from scripts.single_param_sweep import (  # pylint: disable=wrong-import-position
    single_param_sweep,
)
from src.single_param_sweep import Param  # pylint: disable=wrong-import-position


def _add_common_args(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--outdir",
        help=("Directory to place results in, e.g. graphs, netlists, ldb."),
        default=os.path.join(PYTHON_DIRECTORY, "out"),
    )
    parser.add_argument(
        "--netlist",
        help=("Path to reference netlist to modify. "),
        default=os.path.join(LIBERATE_DIRECTORY, "netlist/INVX1.sp"),
    )
    parser.add_argument(
        "--tclscript",
        help=("Characterization tcl script with liberate settings and templates"),
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


# Basically a copy of this blog post [1].
# [1] https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html
class Cirkopt:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="SPICE circuit optimizer",
            usage="""
cirkopt <command> [<args>]

The most commonly used commands are:
explore     Generate plots showing search space
search      Find an optimal design""",
        )
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
        logging.basicConfig(
            format="%(levelname)s (%(asctime)s): %(message)s",
            datefmt="%I:%M:%S %p",
            level=args.loglevel,
        )
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
            netlist_dir=os.path.join(args.outdir, "netlist"),
            liberate_log=os.path.join(args.outdir, "liberate.log"),
            out_dir=args.outdir,
            ldb_name="CIRKOPT",
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
            "--min-width",
            help="Minimum width for a device (inclusive)",
            type=float,
            default=120e-9,
        )
        parser.add_argument(
            "--max-width",
            help="Maximum width for a device (inclusive)",
            type=float,
            default=10e-6,
        )
        parser.add_argument(
            "--min-length",
            help="Minimum length for a device (inclusive)",
            type=float,
            default=45e-9,
        )
        parser.add_argument(
            "--max-length",
            help="Maximum length for a device (inclusive)",
            type=float,
            default=45e-9,
        )
        parser.add_argument(
            "--min-fingers",
            help="Minimum fingers for a device (inclusive)",
            type=int,
            default=1,
        )
        parser.add_argument(
            "--max-fingers",
            help="Maximum fingers for a device (inclusive)",
            type=int,
            default=1,
        )
        parser.add_argument(
            "--precision",
            help=(
                "The smallest step size in device width and length to take (i.e 5nm would be '5e-9'). "
                + "Stored as string to avoid floating point madness."
            ),
            type=str,
            default="5e-9",
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
        logging.basicConfig(
            format="%(levelname)s (%(asctime)s): %(message)s",
            datefmt="%I:%M:%S %p",
            level=args.loglevel,
        )

        # Print all the arguments given
        for key in args.__dict__:
            debug(f"{key:<10}: {args.__dict__[key]}")

        genetic_search(
            reference_netlist=args.netlist,
            max_iterations=args.iterations,
            num_individuals=args.individuals,
            elitism=args.elitism,
            npoints=args.npoints,
            alpha=args.alpha,
            pmutation=args.pmutation,
            mutation_std_deviation=args.mutation_std_dev,
            min_width=args.min_width,
            max_width=args.max_width,
            min_length=args.min_length,
            max_length=args.max_length,
            min_fingers=args.min_fingers,
            max_fingers=args.max_fingers,
            precision=args.precision,
            delay_index=tuple(args.outindex),
            seed=args.seed,
            tcl_script=args.tclscript,
            liberate_dir=LIBERATE_DIRECTORY,
            netlist_dir=os.path.join(args.outdir, "netlist"),
            liberate_log=os.path.join(args.outdir, "liberate.log"),
            out_dir=args.outdir,
            ldb_name="CIRKOPT",
        )


if __name__ == "__main__":
    Cirkopt()
