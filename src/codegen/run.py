from os.path import expanduser

import subprocess
import sys


def main():
    """Executes the code generation steps that are needed to make the source
    code of the Python extension complete.
    """
    args = [
        expanduser(x)
        for x in [
            "~/dev/igraph/stimulus/.venv/bin/python",
            "~/dev/igraph/stimulus/.venv/bin/stimulus",
            "-f",
            "~/dev/igraph/igraph/interfaces/functions.yaml",
            "-t",
            "~/dev/igraph/igraph/interfaces/types.yaml",
            "-f",
            "src/codegen/functions.yaml",
            "-t",
            "src/codegen/types.yaml",
            "-l",
            "python:ctypes",
            "-i",
            "src/codegen/internal_lib.py.in",
            "-o",
            "src/igraph_ctypes/_internal/lib.py",
        ]
    ]
    proc = subprocess.run(args, check=True)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
