# SIEVE


SIEVE system consists of two conponents, miniWizPL and emp-zk tool kit.

miniWizPL is a Python library and compiler for writing zero-knowledge statements and generates cpp file to generate an intermediate representation file for emp-zk tool kit to prove and verify. 

----

## Setting up

<strong> miniWizPL </strong><br>

Clone this repo:

```
git clone https://github.com/multiparty/SIEVE.git
```

Then, inside the local repo root directory run:

```
source venv/bin/activate
pip install .
```

<strong> emp-zk tool kit </strong><br>

In the local repo root directory run: 
  ```
  python install.py --deps --tool --ot --zk
  ```
  <br>
    <li> By default it will build for Release. `-DCMAKE_BUILD_TYPE=[Release|Debug]` option is also available.</li>
    <li> No sudo? Change [`CMAKE_INSTALL_PREFIX`](https://cmake.org/cmake/help/v2.8.8/cmake.html#variable%3aCMAKE_INSTALL_PREFIX).</li>

## Examples

We will demonstrate end-to-end execution with simple.py in the examples/simple_demos directory.

<strong> miniWizPL </strong><br>

The `examples` directory contains several examples of miniWizPL
programs that demonstrate the compiler's features. For example, after
installing miniWizPL, you can run:

```
python examples/simple_demos/simple.py
```

You may also explore other systems to prove in the examples directory by just changing the path below.

This will produce a new file in the current directory called
`miniwizpl_test.cpp` containing EMP code encoding the statement that
the prover knows two numbers `x` and `y` such that `x + y = 5`.

`miniwizpl_test.cpp` will be compiled in the following step to run a ZK proof experiment.

<strong> emp-zk tool kit </strong><br>

Run the following command in the directory of `miniwizpl_test.cpp` (If you followed the instruction here exacly, it should be the root directory of this project)

```
g++ -I./miniwizpl/boilerplate -lssl -lcrypto -o\
    -pthread -Wall -funroll-loops -Wno-ignored-attributes -Wno-unused-result -march=native -maes -mrdseed -std=c++11 -O3 \
    miniwizpl_test.cpp -lemp-zk -lemp-tool -lcrypto \
    -o miniwizpl_test
```

Should you encounter an error related to openssl or crypto package, try adding -I and -L as follows:

```
g++ -I./miniwizpl/boilerplate -I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib -lssl -lcrypto -o\
    -pthread -Wall -funroll-loops -Wno-ignored-attributes -Wno-unused-result -march=native -maes -mrdseed -std=c++11 -O3 \
    miniwizpl_test.cpp -lemp-zk -lemp-tool -lcrypto \
    -o miniwizpl_test
```

Once you have compiled our EMP code, we can run the `miniwizpl_test`
executable in your terminal in the following way, with the prover running:

```
./miniwizpl_test 1 12349
```

and in a separate terminal, the verifier running:

```
./miniwizpl_test 2 12349
```

The first command line argument indicates whether or not to run the executable as the prover or verifier, respectively denoted by a `1` or `2`. 

The second command line argument represents the communication port. 
For a successful proof, the above command should run and return 
a non-zero exit code. For a failed proof, the above should report a failed assertion.

## Generating Documentation Re: miniwizpl

Documentation can be generated with `pdoc3`:

```
pip install pdoc3
pdoc --http localhost:8080 miniwizpl
```
