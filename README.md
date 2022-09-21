# miniWizPL
## A Python library and compiler for writing zero-knowledge statements

----

## Installing

You can install miniWizPL with `pip`. Clone this repo and then run:

```
pip install .
```

## Running the Compiler

miniWizPL programs are Python programs; when you run the program, its
output is a ZK statement in the format of a supported backend.
Currently supported backends are:

- EMP toolkit
- SIEVE IR0/1 (wip)

## Examples

The `examples` directory contains several examples of miniWizPL
programs that demonstrate the compiler's features. For example, after
installing miniWizPL, you can run:

```
python examples/simple_demos/simple.py
```

This will produce a new file in the current directory called
`miniwizpl_test.cpp` containing EMP code encoding the statement that
the prover knows two numbers `x` and `y` such that `x + y = 5`.

## Generating Documentation

Documentation can be generated with `pdoc3`:

```
pip install pdoc3
pdoc --http localhost:8080 miniwizpl
```
# SIEVE
