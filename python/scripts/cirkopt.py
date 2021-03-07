#!/usr/bin/env python3

# Set up path relative to python root folder so we can find the other packages
import sys
import os.path
import argparse
import logging
import numpy as np
from logging import DEBUG, debug, INFO, info, WARNING, error

PYTHON_SCRIPTS_DIRECTORY: str = os.path.dirname(os.path.abspath(__file__))
PYTHON_DIRECTORY: str = os.path.abspath(os.path.join(PYTHON_SCRIPTS_DIRECTORY, ".."))
LIBERATE_DIRECTORY: str = os.path.abspath(os.path.join(PYTHON_DIRECTORY, "../liberate"))
sys.path.append(PYTHON_DIRECTORY)

# These imports rely on changed sys.path
from scripts.single_param_sweep import (  # pylint: disable=wrong-import-position
    main as sweep_param,
)
from src.single_param_sweep import Param  # pylint: disable=wrong-import-position

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
        parser.add_argument(
            "--outindex",
            help="Index of value from LDB table to show, space separated, e.g.: 0 1",
            nargs=2,
            type=int,
            default=[0, 1],
        )
        parser.add_argument(
            "--outdir",
            help=(
                "Directory to place results in, e.g. graphs. "
                + "Does not include generated netlists or LDB library."
            ),
            default=os.path.join(PYTHON_DIRECTORY, "out"),
        )
        parser.add_argument(
            "--workdir",
            help=(
                "Directory to place generated netlists. "
                + "Must match settings in Liberate configeration files. "
            ),
            default=os.path.join(LIBERATE_DIRECTORY, "netlist_wrk"),
        )
        parser.add_argument(
            "--netlist",
            help=(
                "Path to reference netlist to modify. "
                + "Must match settings in Liberate configeration file."
            ),
            default=os.path.join(LIBERATE_DIRECTORY, "netlist_ref/INVX1.sp"),
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
        sweep_param(
            reference_netlist_rel_path=args.netlist,
            netlist_work_dir_rel_path=args.workdir,
            param=args.param,
            values=values,
            graph_pin=args.outpin,
            graph_delay_index=args.outindex,
            out_dir_rel_path=args.outdir,
        )


if __name__ == "__main__":
    Cirkopt()
