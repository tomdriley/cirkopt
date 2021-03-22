#!/usr/bin/env python3
import subprocess
import os
from shutil import copy
import sys
import shutil
import time
from itertools import cycle
import logging
from logging import info, error
from typing import NamedTuple, List, Sequence
import json

from src.file_io import File
from src.liberty_parser import LibertyParser, LibertyResult
from src.netlist import Netlist
from src.cirkopt_json import ObjectEncoder

LIBERATE_DEFAULT_CMD: str = "liberate"

LiberateCompletedProcess = NamedTuple(
    "LiberateCompletedProcess",
    [("args", List[str]), ("returncode", int), ("stdout", str)],
)


def _waiting_animation(complete_condition, refresh_rate_Hz: int = 10) -> None:
    if logging.getLogger().getEffectiveLevel() > logging.INFO:
        # Don't print anything
        while complete_condition() is None:
            # Wait for completion
            pass
        return
    # Copy of [1]
    # [1] https://stackoverflow.com/questions/22029562/python-how-to-make-simple-animated-loading-while-process-is-running
    for c in cycle(["|", "/", "-", "\\"]):
        if complete_condition() is not None:
            break
        loading_msg = "Running Liberate..." + c
        sys.stdout.write("\r" + loading_msg)
        sys.stdout.flush()
        time.sleep(1 / refresh_rate_Hz)
    # Clear text then print message
    sys.stdout.write("\r" + " " * len(loading_msg) + "\r")
    info("Liberate completed.")


def _run_liberate(
    candidates: Sequence[Netlist],
    tcl_script: str,
    liberate_dir: str,
    netlist_dir: str,
    liberate_log: str,
    out_dir: str,
    ldb_name: str,
    liberate_cmd: str = LIBERATE_DEFAULT_CMD,
) -> LiberateCompletedProcess:
    """Run Cadence Liberate

    characterizes SPICE (.sp) files and generate Liberty library (.lib or .ldb)
    """

    # TODO: Run setup script before

    if not os.path.isfile(tcl_script):
        raise FileNotFoundError(tcl_script)
    if not os.path.isdir(liberate_dir):
        raise NotADirectoryError(liberate_dir)
    if shutil.which(liberate_cmd) is None:
        error(
            f"'{liberate_cmd}' does not appear to be an executable, "
            + "did you forget to source the setup script?"
        )
        sys.exit()

    if not os.path.isdir(out_dir):
        info(f"Creating output directory {out_dir}")
        os.mkdir(out_dir)

    if not os.path.isdir(netlist_dir):
        info(f"Creating netlist working directory {netlist_dir}")
        os.mkdir(netlist_dir)

    for netlist in candidates:
        netlist_file = File(os.path.join(netlist_dir, netlist.cell_name + ".sp"))
        netlist.persist(netlist_file)

    cell_names = ",".join(tuple(netlist.cell_name for netlist in candidates))

    info("Running liberate.")
    with open(
        file=liberate_log,
        mode="w",
    ) as log_file:  # TODO: use MockFile interface
        r: subprocess.Popen = subprocess.Popen(
            args=[liberate_cmd, tcl_script],
            stderr=subprocess.STDOUT,
            stdout=log_file,
            text=True,
            env={
                **os.environ,
                "NETLIST_DIR": netlist_dir,
                "OUT_DIR": out_dir,
                "CELL_NAMES": cell_names,
                "LDB_NAME": ldb_name,
                "LIBERATE_DIR": liberate_dir,
            },
        )
        _waiting_animation(complete_condition=r.poll)
    # Convert to CompletedProcess so we can check the return code
    results: subprocess.CompletedProcess = subprocess.CompletedProcess(
        args=r.args,
        returncode=r.returncode,
        stdout=r.stdout,
        stderr=r.stderr,
    )
    results.check_returncode()

    return LiberateCompletedProcess(
        args=results.args, returncode=results.returncode, stdout=results.stdout
    )


def liberate_simulator(
    candidates: Sequence[Netlist],
    iteration: int,
    tcl_script: str,
    liberate_dir: str,
    out_dir: str,
) -> LibertyResult:
    run_folder = os.path.join(out_dir, "iteration-" + str(iteration))
    if not os.path.isdir(run_folder):
        info(f"Creating output directory {run_folder}")
        os.mkdir(run_folder)

    # Serialize candidates
    json_file: File = File(os.path.join(run_folder, "candidates.json"))
    candidates_json: str = json.dumps(candidates, indent=4, cls=ObjectEncoder)
    json_file.write(candidates_json)

    netlist_dir = os.path.join(run_folder, "netlist")
    # Place current log in same place to allow `tail -f`
    liberate_log_working = os.path.join(out_dir, "liberate.log")
    ldb_name = "CIRKOPT"

    # Run simulations
    _run_liberate(
        candidates=candidates,
        tcl_script=tcl_script,
        liberate_dir=liberate_dir,
        netlist_dir=netlist_dir,
        liberate_log=liberate_log_working,
        out_dir=run_folder,
        ldb_name=ldb_name,
    )

    # Keep copy so to prevent overwritting
    copy(liberate_log_working, run_folder)

    # Parse results
    ldb_path = os.path.join(run_folder, "lib", ldb_name + ".lib")
    ldb_file = File(ldb_path)
    parser = LibertyParser()
    return parser.parse(ldb_file)
