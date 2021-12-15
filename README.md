python-igraph-ctypes
====================

This repository contains an **experimental** Python API to the [igraph C
library](https://igraph.org), with the following goals:

* It should contain as little C code as possible.

* It should rely on code generation to create most of the glue code between
  Python and igraph's core C API to make it easier to adapt to changes in the
  underlying C library without having to re-write too much of the Python code.

* It should provide full type annotations.

Status
------

This repo is **highly experimental** and currently it is only in
a proof-of-concept stage. The vast majority of igraph's API is not exposed, and
things may break randomly, or they may not even work.

Usage
-----

1. Clone the repo.

2. Install [`poetry`](https://python-poetry.org) if you don't have it yet.

3. Run `poetry install` to prepare a virtualenv with all the required
   dependencies.

4. Run `poetry run pytest` to run the unit tests, or `poetry run python` to run
   a Python interpreter where you can `import igraph_ctypes`

