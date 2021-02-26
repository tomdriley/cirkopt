#!/usr/bin/env python3
import subprocess
import os.path
import shutil
from logging import info
from typing import NamedTuple, List, Sequence, Optional
from src.file_io import File
from src.liberate_template_utils import update_liberate_template_cell_names

# Liberate project folder is defined relative to the location of this script
PYTHON_SRC_DIRECTORY: str = os.path.dirname(os.path.abspath(__file__))
LIBERATE_DEFAULT_PROJECT_DIRECTORY: str = os.path.abspath(
    os.path.join(PYTHON_SRC_DIRECTORY, "../../liberate")
)
CHAR_TCL_DEFAULT_PATH: str = os.path.join(
    LIBERATE_DEFAULT_PROJECT_DIRECTORY, "tcl/char.tcl"
)
TEMPLATE_TCL_DEFAULT_PATH: str = os.path.join(
    LIBERATE_DEFAULT_PROJECT_DIRECTORY, "template/template.tcl"
)
LIBERATE_DEFAULT_CMD: str = "liberate"

LiberateResult = NamedTuple(
    "LiberateResult", [("args", List[str]), ("returncode", int), ("stdout", str)]
)


def run_liberate(
    cell_names: Optional[Sequence[str]] = None,
    liberate_cmd: str = LIBERATE_DEFAULT_CMD,
    char_tcl_path: str = CHAR_TCL_DEFAULT_PATH,
    run_dir: str = LIBERATE_DEFAULT_PROJECT_DIRECTORY,
) -> LiberateResult:
    """Run Cadence Liberate

    characterizes SPICE (.sp) files and generate Liberty library (.lib or .ldb)
    """

    if not os.path.isfile(char_tcl_path):
        raise TypeError(f"No file found at path {char_tcl_path}")
    if shutil.which(liberate_cmd) is None:
        raise TypeError(f"'{liberate_cmd}' does not appear to be an executable")

    # Update cells to simulate
    if cell_names is not None:
        template_tcl_file = File(TEMPLATE_TCL_DEFAULT_PATH)
        update_liberate_template_cell_names(template_tcl_file, cell_names)

    # TODO: Run setup script before

    info("Running liberate.")
    results = subprocess.run(
        args=[liberate_cmd, char_tcl_path],
        cwd=run_dir,
        check=True,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
        text=True,
    )

    return LiberateResult(
        args=results.args, returncode=results.returncode, stdout=results.stdout
    )
