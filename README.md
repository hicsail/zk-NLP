# SIEVE


SIEVE system consists of two conponents, miniWizPL and emp-zk tool kit.

miniWizPL is a Python library and compiler for writing zero-knowledge statements and generates cpp file to generate an intermediate representation file for emp-zk tool kit to prove and verify. 

----

## Setting up

<strong> miniWizPL </strong><br>

Clone this repo:

```
git clone https://github.com/hicsail/SIEVE.git
```

Then, inside the local repo root directory run:

```
docker-compose up -d --build
```

This will build an image and compose a container

Once the container is made, it will automatically run simple.py and corresponding proof and verification as an example


## If you want to chose a demo file and run it inside the docker:

Run the following command in your terminal:

```
docker exec -it <containerID> bash
```

Now you are inside docker shell

<br>
<strong> 1) Easy Way </strong>
<br>
<br>

Then run:

```
/bin/bash ./run.sh -f <sub_folder> -c <Python script name> -o <Optional: test or debug>
```

For example, you can run:

```
/bin/bash ./run.sh -f substring_search -c stringlist_search_between.py -o debug
```

The argument at the end is optional. 
    <li> "debug" prints the intermediate results of DFA transitions (It does not compile with miniwizpl).
    <li> "test" produces a synthetic test case, including an input text and target substrings. 
    <li> If the thrid argument is empty, it will use the user defined target text in "dfa_test_input.txt" and users have to set their target in places like: https://github.com/hicsail/SIEVE/blob/200b8dc6076e8024352815e4753204b658544a43/examples/substring_search/stringlist_search_after_all.py#L13

If you want to run a script just beneath examples directory, then run without -f flag like:

```
/bin/bash ./run.sh -c dfa_example.py 
```

<br>
<strong> 2) Manual Execution </strong>
<br>
<br>

In case you want to experiment manually, run inside docker shell:

```
python[3] examples/simple_demos/simple.py
```

And run the following command:

```
g++  miniwizpl_test.cpp -o miniwizpl_test\
    -pthread -Wall -funroll-loops -Wno-ignored-attributes -Wno-unused-result -march=native -maes -mrdseed -std=c++11 -O3 \
    -I/usr/src/app/miniwizpl/boilerplate\
    -I/usr/lib/openssl/include\
    -L/usr/lib/openssl/lib -lssl -lcrypto \
    -L/usr/src/app/emp-zk/emp-zk -lemp-zk\
    -L/usr/src/app/emp-tool/emp-tool -lemp-tool\
    -L/usr/local/lib -Wl,-R/usr/local/lib    
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

----

## Generating Documentation Re: miniwizpl

Documentation can be generated with `pdoc3`:

```
pip install pdoc3
pdoc --http localhost:8080 miniwizpl
```

## Changes from original code stacks

<li> Changed #include statement in mini_wizpl_top.cpp in miniwizpl/boilerplate, from "ram-zk/zk-mem.h" to "emp-zk/emp-zk/extensions/ram-zk/zk-mem.h" 
, so that test file can find the path properly</li>
<li> Added "-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" into g++ command instruction </li>

<li> Sudo prefix is removed from install.py to fit Dockerfile's style </li>
<li> Added "prefix to mnist.pt directory in examples/neural_networks/mnist_wizpl.py, so that the system can find the file inside container </li>

<li> OR operation added to class AST in miniwizpl/expr.py, in order to implement stringlist_search_between </li>
