# python-igraph-ctypes

This repository contains an **experimental** Python API to the [igraph C
library](https://igraph.org), with the following goals:

- It should contain as little hand-written C code as possible.

- It should rely on code generation to create most of the glue code between
  Python and igraph's core C API to make it easier to adapt to changes in the
  underlying C library without having to re-write too much of the Python code.

- It should provide full type annotations.

## Status

This repo is **highly experimental** and currently it is only in
a proof-of-concept stage. The vast majority of igraph's API is not exposed, and
things may break randomly, or they may not even work.

## Usage

1. Clone the repo.

2. Install [`uv`](https://astral.sh/uv) if you don't have it yet.

3. Run `uv sync` to prepare a virtualenv with all the required
   dependencies.

4. Run `uv run pytest` to run the unit tests, or `uv run python` to run
   a Python interpreter where you can `import igraph_ctypes`

## Development

During development, you need to have the shared library of igraph's C core
(`libigraph.4.so` on Linux, `libigraph.4.dylib` on macOS) available in your
`LD_LIBRARY_PATH` (Linux) or `DYLD_LIBRARY_PATH` (macOS).

Large chunks of the code in the library are generated from the interface specification
file in igraph (`functions.yaml`). Stimulus is the name of the component responsible for
the code generation and it is in a separate project, referred from this project as a
dev dependency. To regenerate the code, run `uv run python3 -m codegen.run`, which uses
Stimulus to parse the interface specification file from igraph and generate the Python
code.

## Benchmarking

Benchmarks will be placed in `benchmarks` and they will compare the "old",
official Python interface of igraph with this new implementation. To run the
benchmarks, type `uv run richbench benchmarks`.

## Caveats

- Apparently you'll need to ensure that the igraph shared library is built
  without sanitizers, otherwise the `dlopen()` call fails, at least on macOS.
