from enum import IntFlag
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
import importlib.util
import re
import subprocess
import sys
import yaml


IGRAPH_C_CORE_SOURCE_FOLDER = Path.home() / "dev" / "igraph" / "igraph"
SOURCE_FOLDER = Path(sys.modules[__name__].__file__ or "").parent.parent.absolute()

BOOLEAN_ENUM_MEMBERS: dict[str, tuple[str, str]] = {
    "AddWeights": ("YES", "NO"),
}
"""Enums that also accept ``True`` and ``False``, mapped to the names of the
enum members that they correspond to.
"""


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
    """Generates a Python module that re-exports all top-level functions,
    classes and annotated type aliases matching the given glob or globs from
    another module.

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
    top_level_names = [
        n.target.id
        if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)
        else getattr(n, "name", None)
        for n in node.body
        if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AnnAssign))
    ]
    matched_symbols = [n for n in top_level_names if n and matcher(n)]
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

    HANDWRITTEN_FLAGS = ("AllowedEdgeTypes", "WriteGMLOptions")
    IGNORED_ENUMS = {
        "igraph_cached_property_t",
        "igraph_lapack_dsyev_which_t",
    }
    ENUM_NAME_REMAPPING = {
        "Adjacency": "AdjacencyMode",
        "AttributeElemtype": "AttributeElementType",
        "BlissSh": "BLISSSplittingHeuristics",
        "ColoringGreedy": "GreedyColoringHeuristics",
        "Degseq": "DegreeSequenceMode",
        "EdgeorderType": "EdgeOrder",
        "EitType": "EdgeIteratorType",
        "ErdosRenyi": "ErdosRenyiType",
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
    EXTRA_ENUM_MEMBERS: dict[str, Sequence[tuple[str, Union[int, str]]]] = {
        "GreedyColoringHeuristics": [("NEIGHBORS", "COLORED_NEIGHBORS")],
        "LayoutGrid": [("NO_GRID", "NOGRID"), ("AUTO_GRID", "AUTOGRID")],
        "Loops": [("IGNORE", 0)],
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
        if len(entries) == 1:
            # No common prefix to infer from a single entry; strip the longest
            # prefix derived from the name of the enum type instead
            words = orig_name.upper().split("_")[:-1]
            prefixes = ("_".join(words[:i]) + "_" for i in range(len(words), 1, -1))
            plen = next((len(p) for p in prefixes if entries[0].startswith(p)), 0)
        else:
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
        all_values: dict[str, int] = {}
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
            all_values[key.lower()] = value_int
            last_value = value_int

        for key, value_int_or_str in EXTRA_ENUM_MEMBERS.get(name, ()):
            if isinstance(value_int_or_str, str):
                value_str = all_members[value_int_or_str.lower()]
                aliased_to = value_int_or_str
            else:
                value_str = str(value_int_or_str)
                aliased_to = key
            fp.write(f"    {key} = {value_str}\n")
            all_members[key.lower()] = aliased_to

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
        if name in BOOLEAN_ENUM_MEMBERS:
            true_member, false_member = BOOLEAN_ENUM_MEMBERS[name]
            fp.write("        elif value is True:\n")
            fp.write(f"            return cls.{true_member}\n")
            fp.write("        elif value is False:\n")
            fp.write(f"            return cls.{false_member}\n")
        fp.write("        elif isinstance(value, int):\n")
        fp.write("            return cls(value)\n")
        fp.write("        else:\n")
        fp.write("            try:\n")
        fp.write(f"                return _{name}_string_map[value]\n")
        fp.write("            except KeyError:\n")
        fp.write(
            f'                raise ValueError(f"{{value!r}} cannot be '
            f'converted to {name}") from None\n'
        )
        fp.write("\n\n")
        fp.write(f"_{name}_string_map: dict[str, {name}] = {{\n")
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

        exports = list(HANDWRITTEN_FLAGS)
        for path in headers:
            with path.open("r") as infp:
                exports.extend(process_file(outfp, infp))

        outfp.write("__all__ = (\n")
        for item in sorted(exports):
            outfp.write(f"    {item!r},\n")
        outfp.write(")\n")


def _load_module_from_path(path: Path, name: str):
    """Loads a standalone Python module from the given path without importing
    the package that contains it.
    """
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _enum_strings(module, enum_class) -> list[str]:
    """Returns the strings accepted by the ``from_()`` class method of the given
    enum class, i.e. the keys of its string map, in the order of definition of
    the corresponding enum members.
    """
    string_map = getattr(module, f"_{enum_class.__name__}_string_map")
    order = {name.lower(): index for index, name in enumerate(enum_class.__members__)}
    return sorted(string_map, key=lambda key: order.get(key, len(order)))


def generate_enum_literals(module, template: Path, output: Path) -> None:
    """Generates the string literal type aliases corresponding to the enums in
    the given (generated) enum module.

    Args:
        module: the loaded enum module
        template: template of the module containing the string literal types
        output: path to the module containing the string literal types
    """
    with output.open("w") as outfp:
        with template.open("r") as infp:
            outfp.write(infp.read())

        for name in module.__all__:
            enum_class = getattr(module, name)
            strings = ", ".join(f'"{s}"' for s in _enum_strings(module, enum_class))
            literal = f"Literal[{strings}]"
            if issubclass(enum_class, IntFlag):
                kind = "a combination of flags of"
                literal = f"{literal} | Iterable[{literal}]"
            else:
                kind = "a value of"
            extra = ""
            if name in BOOLEAN_ENUM_MEMBERS:
                literal = f"{literal} | bool"
                true_member, false_member = BOOLEAN_ENUM_MEMBERS[name]
                extra = (
                    f" ``True`` and ``False`` are equivalent to "
                    f'``"{true_member.lower()}"`` and ``"{false_member.lower()}"``.'
                )
            outfp.write(f"{name}: TypeAlias = {literal}\n")
            outfp.write(
                f'"""String literals accepted where {kind} the ``{name}`` '
                f'enum is expected.{extra}"""\n\n'
            )

        outfp.write("\n__all__ = (\n")
        for name in module.__all__:
            outfp.write(f"    {name!r},\n")
        outfp.write(")\n")


def generate_enum_types(module, output: Path, abstract_types: Path) -> None:
    """Generates the abstract type definitions for Stimulus that convert the
    string literals of the enums in the given (generated) enum module to the
    C enums.

    Args:
        module: the loaded enum module
        output: path to the type definition file that the abstract type
            definitions should be written into
        abstract_types: path to the type definition file of the C core where
            the abstract enum types are declared
    """
    enum_classes = {}
    for name in module.__all__:
        enum_class = getattr(module, name)
        match = re.search(r"``(igraph_\w+_t)``", enum_class.__doc__ or "")
        if match:
            enum_classes[match.group(1)] = enum_class

    with abstract_types.open() as fp:
        abstract_type_specs = yaml.safe_load(fp)

    type_specs = {}
    for abstract_type, spec in sorted(abstract_type_specs.items()):
        flags = str(spec.get("FLAGS", "")).upper()
        enum_class = enum_classes.get(spec.get("CTYPE"))
        if ("ENUM" not in flags and "BITS" not in flags) or enum_class is None:
            continue

        name = enum_class.__name__
        type_spec = {
            "PY_TYPE": name,
            "INCONV": {
                "IN": f"%C% = c_int(_enums.{name}.from_(%I%))",
                "OUT": "%C% = c_int()",
            },
            "DEFAULT": {},
        }
        if "ENUM" in flags:
            type_spec["OUTCONV"] = {
                "OUT": f"%I% = cast({name}, _enums.{name}(%C%.value).name.lower())"
            }

        # Abstract default values in functions.yaml are the names of the enum
        # members, or sometimes their string representations in quotes
        for string in _enum_strings(module, enum_class):
            type_spec["DEFAULT"][string.upper()] = f'"{string}"'
            type_spec["DEFAULT"][f'"{string}"'] = f'"{string}"'

        type_specs[abstract_type] = type_spec

    with output.open("w") as fp:
        fp.write(
            "# Abstract types for the enums of the C core of igraph.\n"
            "#\n"
            "# This file is generated by codegen/run.py; do not edit by hand.\n"
            "# Override the entries in types.yaml instead.\n\n"
        )
        yaml.safe_dump(type_specs, fp, sort_keys=False, width=1000)


def check_enum_defaults(functions: Path, enum_names: Iterable[str]) -> None:
    """Checks that the generated typed wrapper functions do not refer to enum
    defaults that Stimulus could not map to a string literal.

    Raises:
        RuntimeError: if an unmapped enum default was found
    """
    # Enum names qualified with a module name are references to the enum
    # classes in conversions and not default values
    pattern = re.compile(rf"(?<![\w.])(?:{'|'.join(enum_names)})\.[A-Za-z_]\w*")
    unmapped = sorted(set(pattern.findall(functions.read_text())))
    if unmapped:
        raise RuntimeError(
            "Unmapped enum default values in generated code: " + ", ".join(unmapped)
        )


def main():
    """Executes the code generation steps that are needed to make the source
    code of the Python extension complete.
    """
    generate_enums(
        SOURCE_FOLDER / "codegen" / "internal_enums.py.in",
        SOURCE_FOLDER / "igraph_ctypes" / "_internal" / "enums.py",
        (IGRAPH_C_CORE_SOURCE_FOLDER / "include").glob("*.h"),
    )

    # Stimulus needs the abstract types of the enums so the enum module is
    # generated and loaded first
    enum_module = _load_module_from_path(
        SOURCE_FOLDER / "igraph_ctypes" / "_internal" / "enums.py",
        "_igraph_ctypes_codegen_enums",
    )
    generate_enum_literals(
        enum_module,
        SOURCE_FOLDER / "codegen" / "internal_literals.py.in",
        SOURCE_FOLDER / "igraph_ctypes" / "_internal" / "literals.py",
    )
    generate_enum_types(
        enum_module,
        SOURCE_FOLDER / "codegen" / "types_enums.yaml",
        IGRAPH_C_CORE_SOURCE_FOLDER / "interfaces" / "types.yaml",
    )

    common_args = [
        sys.executable,
        "-m",
        "stimulus",
        "-f",
        str(IGRAPH_C_CORE_SOURCE_FOLDER / "interfaces" / "functions.yaml"),
        "-t",
        str(IGRAPH_C_CORE_SOURCE_FOLDER / "interfaces" / "types.yaml"),
        "-t",
        str(SOURCE_FOLDER / "codegen" / "types_enums.yaml"),
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

    check_enum_defaults(
        SOURCE_FOLDER / "igraph_ctypes" / "_internal" / "functions.py",
        enum_module.__all__,
    )

    reexport(
        SOURCE_FOLDER / "igraph_ctypes" / "_internal" / "literals.py",
        SOURCE_FOLDER / "igraph_ctypes" / "enums.py",
        "._internal.literals",
    )

    reexport(
        SOURCE_FOLDER / "igraph_ctypes" / "_internal" / "types.py",
        SOURCE_FOLDER / "igraph_ctypes" / "types.py",
        "._internal.types",
        match=(
            "AttributeCombinationSpecification",
            "AttributeCombinationSpecificationEntry",
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
