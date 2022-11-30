# SIEVE

SIEVE project aims to provide an E2E pipeline to implement Zero-Knowledge Proof.

It consists of two components, miniWizPL and emp-zk tool kit.

miniWizPL is a Python library that compiles zero-knowledge statements in Python Script into C++ code with EMP took kit.
This E2E module runs the compiled C++ code and asserts whether or not prover's claim is valid.

----

## 📖 Setting up

Clone this repo:

```
git clone https://github.com/hicsail/SIEVE.git
```

Then, inside the local repo root directory run to build an image and a container:

```
docker-compose up -d --build
```

Please move into the root directory

```
cd SIEVE
```
## 🖥️ Getting started

You have to do above operations only once, and from next time you can run the following command in your terminal to start Docker Shell:

```
docker exec -it <containerID> bash
```

You can get a containerID from the docker desktop app by clicking the small button highlighted in the red circle
<ul>
    <img width="1161" alt="image" src="https://user-images.githubusercontent.com/62607343/203409123-1a95786f-8b2a-4e71-a920-3a51cf50cf0f.png">
</ul>

If you see something like the following in your command line, you are successfully inside docker shell
<ul>
<img width="300" alt="image" src="https://user-images.githubusercontent.com/62607343/203413803-19021cb9-07ba-4376-ade0-dbdc6c8506c5.png">
</ul>


## 🏋️‍♀️ Experiment your code

There are two avenues to chose from for you to experiment your python scripts inside the container:

<strong> 1) Easy Way </strong>
<ul>

You can run your python script and compile by miniwizpl in the following command:

```
/bin/bash ./run_emp.sh -f <sub_folder> -c <Python script name> -o <Optional: test or debug>
```

<strong> -f (Optional) </strong> : Set one of subfolders if you're experimenting with one of python scripts in the subfolder.
  <ul>
    <li> crypto
    <li> neural_networks
    <li> poseidon_hash
    <li> simple_demos
    <li> substring_search
  </ul>

** You can omit this if you are running a python script just below the examples directory.


<strong> -c (Required) </strong> : Choose a python script in the subfolder

<strong> -o (Optional) </strong> : Choose a mode to run your python script: 
  <ul>
    <li> "debug" prints the intermediate results of DFA transitions (It does not compile with miniwizpl).
    <li> "test" produces a synthetic test case, including an input text and target substrings. 
    <li> If the thrid argument is empty, it will use the user defined target text in "dfa_test_input.txt" and you have to set target: 
  </ul>
  
  https://github.com/hicsail/SIEVE/blob/200b8dc6076e8024352815e4753204b658544a43/examples/substring_search/stringlist_search_after_all.py#L13
<br>
For example, you can run:

```
/bin/bash ./run_emp.sh -f substring_search -c stringlist_search_between.py -o debug
```

This means that you are running <strong> stringlist_search_between.py </strong> in the <strong> substring_search </strong> in <strong> debug mode </strong>.<br>

If you want to run a script just beneath examples directory, then run without -f flag like:

```
/bin/bash ./run_emp.sh -c dfa_example.py 
```

# Todo: Add IR0 implementation

</ul>

<strong> 2) Manual Execution </strong>
<ul>
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
</ul>


## 🎲 Tuning Testing Scale

You may choose a scale of test cases (i.e., difficulty of tests) in generate_text() function (default to 0 = original length of text)

https://github.com/hicsail/SIEVE/blob/a3c52beb324c2908f695b1422f1fca22fea92a2d/examples/substring_search/stringlist_search_after_all.py#L8


----

## Generating Documentation Re: miniwizpl

Documentation can be generated with `pdoc3`:

```
pip install pdoc3
pdoc --http localhost:8080 miniwizpl
```

## Changes from original code stacks
<ul>
<li> Changed #include statement in mini_wizpl_top.cpp in miniwizpl/boilerplate, from "ram-zk/zk-mem.h" to "emp-zk/emp-zk/extensions/ram-zk/zk-mem.h" 
, so that test file can find the path properly</li>
<li> Added "-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" into g++ command instruction </li>

<li> Sudo prefix is removed from install.py to fit Dockerfile's style </li>
<li> Added "prefix to mnist.pt directory in examples/neural_networks/mnist_wizpl.py, so that the system can find the file inside container </li>

<li> OR operation added to class AST in miniwizpl/expr.py, in order to implement stringlist_search_between </li>
</ul>
