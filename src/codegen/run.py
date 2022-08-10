from os.path import expanduser

import subprocess
import sys


def main():
    """Executes the code generation steps that are needed to make the source
    code of the Python extension complete.
    """
    common_args = [
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
    ]

    args = [
        expanduser(x)
        for x in common_args
        + [
            "-l",
            "python:ctypes",
            "-i",
            "src/codegen/internal_lib.py.in",
            "-o",
            "src/igraph_ctypes/_internal/lib.py",
        ]
    ]
    subprocess.run(args, check=True)

    args = [
        expanduser(x)
        for x in common_args
        + [
            "-l",
            "python:ctypes-typed-wrapper",
            "-i",
            "src/codegen/internal_functions.py.in",
            "-o",
            "src/igraph_ctypes/_internal/functions.py",
        ]
    ]
    subprocess.run(args, check=True)


if __name__ == "__main__":
    sys.exit(main())
