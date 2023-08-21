from fnmatch import fnmatch
from os.path import expanduser
from pathlib import Path
from typing import (
    Callable,
    Iterable,
    Optional,
    Sequence,
    TextIO,
    Union,
)

import ast
import re
import subprocess
import sys


IGRAPH_C_CORE_SOURCE_FOLDER = Path.home() / "dev" / "igraph" / "igraph"
SOURCE_FOLDER = Path(sys.modules[__name__].__file__ or "").parent.parent.absolute()


def create_glob_matcher(globs: Union[str, Iterable[str]]) -> Callable[[str], bool]:
    if isinstance(globs, str):
        return create_glob_matcher((globs,))

    glob_list = list(globs)

    def result(value: str) -> bool:
        return any(fnmatch(value, g) for g in glob_list)

    return result


def longest_common_prefix_length(items: Sequence[str]) -> int:
    """Finds the length of the longest common prefix of the given list of
    strings.
    """
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


def reexport(
    input: Path,
    output: Path,
    module_name: str,
    match: Union[str, Sequence[str]] = "*",
    *,
    template: Path = SOURCE_FOLDER / "codegen" / "reexport.py.in",
) -> None:
    """Generates a Python module that re-exports all top-level functions and
    classes matching the given glob or globs from another module.

    Args:
        input: the module whose content is to be re-exported
        output: path to the source of the newly generated module
        match: glob or globs that the re-exported function or class names
            must match
        template: name of the template file to use for the output
    """
    with input.open() as fp:
        node = ast.parse(fp.read(), str(input))

    matcher = create_glob_matcher(g for g in match if "*" in g or "?" in g)
    matched_symbols = [
        n.name
        for n in node.body
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and matcher(n.name)
    ]
    matched_symbols.extend(g for g in match if "*" not in g and "?" not in g)
    matched_symbols.sort()

    with output.open("w") as outfp:
        with template.open("r") as infp:
            outfp.write(infp.read().format(**locals()))

        outfp.write(f"from {module_name} import (\n")
        for symbol in matched_symbols:
            outfp.write(f"    {symbol},\n")
        outfp.write(")\n\n")

        outfp.write("__all__ = (\n")
        for symbol in matched_symbols:
            outfp.write("    " + repr(symbol).replace("'", '"') + ",\n")
        outfp.write(")\n")


def generate_enums(  # noqa: C901
    template: Path, output: Path, headers: Iterable[Path]
) -> None:
    """Generates the contents of ``enums.py`` in the source tree by parsing
    the given include files from igraph's source tree.

    Parsing is done with crude string operations and not with a real C parser
    so the formatting of the input file matters.
    """

    IGNORED_ENUMS = {
        "igraph_cached_property_t",
        "igraph_lapack_dsyev_which_t",
    }
    ENUM_NAME_REMAPPING = {
        "Adjacency": "AdjacencyMode",
        "AttributeElemtype": "AttributeElementType",
        "BlissSh": "BLISSSplittingHeuristics",
        "Degseq": "DegreeSequenceMode",
        "EdgeorderType": "EdgeOrder",
        "EitType": "EdgeIteratorType",
        "ErrorType": "ErrorCode",
        "EsType": "EdgeSequenceType",
        "FasAlgorithm": "FeedbackArcSetAlgorithm",
        "FileformatType": "FileFormat",
        "LayoutDrlDefault": "DRLLayoutPreset",
        "LazyAdlistSimplify": "LazyAdjacencyListSimplify",
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
    EXTRA_ENUM_MEMBERS: dict[str, Sequence[tuple[str, int]]] = {
        "Loops": [("IGNORE", 0)]
    }

    def process_enum(fp: TextIO, spec) -> Optional[str]:  # noqa: C901
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
        all_members: dict[str, str] = {}
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
            all_members[key.lower()] = key
            last_value = value_int

        for key, value_int in EXTRA_ENUM_MEMBERS.get(name, ()):
            fp.write(f"    {key} = {value_int}\n")
            all_members[key.lower()] = key

        fp.write("\n")
        fp.write(f"    _string_map: ClassVar[dict[str, {name}]]\n")
        fp.write("\n")
        fp.write("    @classmethod\n")
        fp.write("    def from_(cls, value: Any):\n")
        fp.write('        """Converts an arbitrary Python object into this enum.\n')
        fp.write("\n")
        fp.write("        Raises:\n")
        fp.write("            ValueError: if the object cannot be converted\n")
        fp.write('        """\n')
        fp.write(f"        if isinstance(value, {name}):\n")
        fp.write("            return value\n")
        fp.write("        elif isinstance(value, int):\n")
        fp.write("            return cls(value)\n")
        fp.write("        else:\n")
        fp.write("            try:\n")
        fp.write("                return cls._string_map[value]\n")
        fp.write("            except KeyError:\n")
        fp.write(
            f'                raise ValueError(f"{{value!r}} cannot be '
            f'converted to {name}") from None\n'
        )
        fp.write("\n\n")
        fp.write(f"{name}._string_map = {{\n")
        for key in sorted(all_members.keys()):
            fp.write(f"    {key!r}: {name}.{all_members[key]},\n")
        fp.write("}\n")
        fp.write("\n\n")

        return name

    def process_file(outfp: TextIO, infp: TextIO) -> list[str]:
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
        str(IGRAPH_C_CORE_SOURCE_FOLDER / "interfaces" / "functions.yaml"),
        "-t",
        str(IGRAPH_C_CORE_SOURCE_FOLDER / "interfaces" / "types.yaml"),
        "-f",
        str(SOURCE_FOLDER / "codegen" / "functions.yaml"),
        "-t",
        str(SOURCE_FOLDER / "codegen" / "types.yaml"),
        "-D",
        str(SOURCE_FOLDER.parent / "docs" / "fragments"),
    ]

    args = [
        expanduser(x)
        for x in common_args
        + [
            "-l",
            "python:ctypes",
            "-i",
            str(SOURCE_FOLDER / "codegen" / "internal_lib.py.in"),
            "-o",
            str(SOURCE_FOLDER / "igraph_ctypes" / "_internal" / "lib.py"),
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
            str(SOURCE_FOLDER / "codegen" / "internal_functions.py.in"),
            "-o",
            str(SOURCE_FOLDER / "igraph_ctypes" / "_internal" / "functions.py"),
        ]
    ]
    subprocess.run(args, check=True)

    generate_enums(
        SOURCE_FOLDER / "codegen" / "internal_enums.py.in",
        SOURCE_FOLDER / "igraph_ctypes" / "_internal" / "enums.py",
        (IGRAPH_C_CORE_SOURCE_FOLDER / "include").glob("*.h"),
    )

    reexport(
        SOURCE_FOLDER / "igraph_ctypes" / "_internal" / "enums.py",
        SOURCE_FOLDER / "igraph_ctypes" / "enums.py",
        "._internal.enums",
    )

    reexport(
        SOURCE_FOLDER / "igraph_ctypes" / "_internal" / "types.py",
        SOURCE_FOLDER / "igraph_ctypes" / "types.py",
        "._internal.types",
        match=(
            "BoolArray",
            "EdgeLike",
            "EdgeSelector",
            "FileLike",
            "IntArray",
            "RealArray",
            "VertexLike",
            "VertexPair",
            "VertexSelector",
        ),
    )


if __name__ == "__main__":
    sys.exit(main())
