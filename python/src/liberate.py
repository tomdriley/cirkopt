#!/usr/bin/env python3
import subprocess
import os.path
import shutil

# Liberate project folder is defined relative to the location of this script
PYTHON_SRC_DIRECTORY: str = os.path.dirname(os.path.abspath(__file__))
LIBERATE_DEFAULT_PROJECT_DIRECTORY: str = os.path.abspath(
    os.path.join(PYTHON_SRC_DIRECTORY, "../../liberate")
)
CHAR_TCL_DEFAULT_PATH: str = os.path.join(
    LIBERATE_DEFAULT_PROJECT_DIRECTORY, "tcl/char.tcl"
)
# Liberate executable location assumes you are running on University servers by default
LIBERATE_DEFAULT_PATH: str = "/CMC/tools/cadence/LIBERATE18.10.293_lnx86/bin/liberate"


def run_liberate(
    liberate_path: str = LIBERATE_DEFAULT_PATH,
    char_tcl_path: str = CHAR_TCL_DEFAULT_PATH,
    run_dir: str = LIBERATE_DEFAULT_PROJECT_DIRECTORY,
) -> subprocess.CompletedProcess:
    """Run Cadence Liberate

    characterizes SPICE (.sp) files and generate Liberty library (.lib or .ldb)
    """

    if not os.path.isfile(char_tcl_path):
        raise TypeError(f"No file found at path {char_tcl_path}")
    if shutil.which(liberate_path) is None:
        raise TypeError(f"'{liberate_path}' does not appear to be an executable")

    # TODO: Support capturing output in log
    # TODO: Run setup script before

    return subprocess.run(
        args=[liberate_path, char_tcl_path],
        cwd=run_dir,
        check=True,
        capture_output=True,
    )


if __name__ == "__main__":
    run_liberate()
