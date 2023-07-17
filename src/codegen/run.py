from os.path import expanduser
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, TextIO, Tuple

import re
import subprocess
import sys


IGRAPH_SOURCE_FOLDER = Path.home() / "dev" / "igraph" / "igraph"


def longest_common_prefix_length(items: Sequence[str]) -> int:
    if not items:
        return 0

    best = 0
    min_length = len(min(items, key=len, default=""))
    for i in range(1, min_length):
        prefixes = [item[:i] for item in items]
        if len(set(prefixes)) > 1:
            break

        if prefixes[0][-1] != "_":
            continue

        best = i

    return best


def generate_enums(template: Path, output: Path, headers: Iterable[Path]):
    """Generates the contents of ``enums.py`` in the source tree by parsing
    the given include files from igraph's source tree.

    Parsing is done with crude string operations and not with a real C parser
    so the formatting of the input file matters.
    """

    IGNORED_ENUMS = set(
        (
            "igraph_cached_property_t",
            "igraph_attribute_type_t",
            "igraph_attribute_elemtype_t",
            "igraph_lapack_dsyev_which_t",
        )
    )
    ENUM_NAME_REMAPPING = {
        "Adjacency": "AdjacencyMode",
        "BlissSh": "BLISSSplittingHeuristics",
        "Degseq": "DegreeSequenceMode",
        "EdgeorderType": "EdgeOrder",
        "EitType": "EdgeIteratorType",
        "EsType": "EdgeSequenceType",
        "FasAlgorithm": "FeedbackArcSetAlgorithm",
        "FileformatType": "FileFormat",
        "LayoutDrlDefault": "DRLLayoutPreset",
        "Loops": None,
        "Neimode": "NeighborMode",
        "Optimal": "Optimality",
        "PagerankAlgo": "PagerankAlgorithm",
        "RandomTree": "RandomTreeMethod",
        "SparsematType": "SparseMatrixType",
        "SparsematSolve": "SparseMatrixSolver",
        "SpincommUpdate": "SpinglassUpdateMode",
        "VitType": "VertexIteratorType",
        "VsType": "VertexSequenceType",
    }
    EXTRA_ENUM_MEMBERS: Dict[str, Sequence[Tuple[str, int]]] = {
        "Loops": [("IGNORE", 0)]
    }

    def process_enum(fp: TextIO, spec) -> Optional[str]:
        spec = re.sub(r"\s*/\*[^/]*\*/\s*", " ", spec)
        spec = spec.replace("IGRAPH_DEPRECATED_ENUMVAL", "")
        spec = re.sub(r"\s+", " ", spec)

        spec, sep, name = spec.rpartition("}")
        if not sep:
            raise ValueError("invalid enum, needs braces")
        _, sep, spec = spec.partition("{")
        if not sep:
            raise ValueError("invalid enum, needs braces")

        name = name.replace(";", "").strip().lower()
        orig_name = name
        if orig_name in IGNORED_ENUMS:
            return None
        if not name.startswith("igraph_") or name.startswith("igraph_i_"):
            return None

        name = name[7:]
        if name.endswith("_t"):
            name = name[:-2]
        name = "".join(part.capitalize() for part in name.split("_"))

        entries = [entry.strip() for entry in spec.split(",")]
        entries = [entry for entry in entries if entry]
        plen = longest_common_prefix_length(entries)
        entries = [entry[plen:] for entry in entries]

        remapped_name = ENUM_NAME_REMAPPING.get(name, name)
        if remapped_name is None:
            return name  # it is already written by hand
        else:
            name = remapped_name

        fp.write(f"class {name}(IntEnum):\n")
        fp.write(f'    """Python counterpart of an ``{orig_name}`` enum."""\n\n')

        last_value = -1
        for entry in entries:
            key, sep, value = entry.replace(" ", "").partition("=")
            if key.startswith("UNUSED_"):
                continue

            if sep:
                try:
                    value_int = int(value)
                except ValueError:
                    # this is an alias to another enum member, skip
                    continue
            else:
                value_int = last_value + 1

            try:
                key = int(key)
            except ValueError:
                # this is what we expected
                pass
            else:
                if key == 1:
                    key = "ONE"
                else:
                    raise ValueError(
                        f"enum key is not a valid Python identifier: {key}"
                    )

            fp.write(f"    {key} = {value_int}\n")
            last_value = value_int

        for key, value_int in EXTRA_ENUM_MEMBERS.get(name, ()):
            fp.write(f"    {key} = {value_int}\n")

        fp.write("\n\n")
        return name

    def process_file(outfp: TextIO, infp: TextIO) -> List[str]:
        all_names = []

        current_enum, in_enum = [], False
        for line in infp:
            if "//" in line:
                line = line[: line.index("//")]

            line = line.strip()

            if line.startswith("typedef enum"):
                current_enum = [line]
                in_enum = "}" not in line
            elif in_enum:
                current_enum.append(line)
                in_enum = "}" not in line

            if current_enum and not in_enum:
                name = process_enum(outfp, " ".join(current_enum))
                if name:
                    all_names.append(name)

                current_enum.clear()

        return all_names

    with output.open("w") as outfp:
        with template.open("r") as infp:
            outfp.write(infp.read())

        exports = []
        for path in headers:
            with path.open("r") as infp:
                exports.extend(process_file(outfp, infp))

        outfp.write("__all__ = (\n")
        for item in sorted(exports):
            outfp.write(f"    {item!r},\n")
        outfp.write(")\n")


def main():
    """Executes the code generation steps that are needed to make the source
    code of the Python extension complete.
    """
    common_args = [
        sys.executable,
        "-m",
        "stimulus",
        "-f",
        str(IGRAPH_SOURCE_FOLDER / "interfaces" / "functions.yaml"),
        "-t",
        str(IGRAPH_SOURCE_FOLDER / "interfaces" / "types.yaml"),
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

    generate_enums(
        Path("src/codegen/internal_enums.py.in"),
        Path("src/igraph_ctypes/_internal/enums.py"),
        (IGRAPH_SOURCE_FOLDER / "include").glob("*.h"),
    )


if __name__ == "__main__":
    sys.exit(main())
