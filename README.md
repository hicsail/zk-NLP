# zk-NLP

zk-NLP provides an E2E pipeline to implement natural language processing (NLP) analysis under the Zero-Knowledge Proof.

----

## 📖 Setting up

<strong> Option A Use published docker image </strong>

Run this in command line:
```
docker run --platform linux/amd64 -it hicsail/zk-nlp:main      
```

<strong> Option B Clone Repo </strong>

Clone this repo:

```
git clone https://github.com/hicsail/zk-NLP.git
```

Move into the root directory of the project

```
cd zk-NLP
```

Inside the root directory, run build image:

```
docker-compose up -d --build
```

Now you have a brand new container running on your machine


## 🖥️ Getting started

<strong> 1) Enter Docker Shell</strong> 

Since you have a running container, you can subsequently run the following command in your terminal to start Docker Shell:

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

<strong> 2) Install wiztoolkit</strong> 

Inside the container, clone wiztoolkit repo and move into wiztoolkit:

(*) You might need to set up ssh key - Follow <a href="https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=linux"> the instruction </a>

```
git clone git@github.mit.edu:sieve-all/wiztoolkit.git
cd wiztoolkit
```

And run the following commands to install wiztoolkit (Backend for IR0):

```
make
make install
```

After the installation, copy the wtk-fire-alarm binary to bin directory:

```
cp /usr/src/app/wiztoolkit/target/wtk-firealarm /usr/bin/wtk-firealarm
```

Then, move back to the root directory.

```
cd ..
```


## 🏋️‍♀️ Run your python script inside the container

You can run your Python script in the docker shell and compile it into zk statements by 'miniwizpl'.
All of the main scripts to run are stored in the <a href="https://github.com/hicsail/zk-NLP/tree/main/examples/substring_search/IR0"> example/substring_search/IR0 directory </a>.

You may run any of them in the docker shell either way described hereunder:


<strong> Option 1) Shell Script </strong> 

The following command will run the Python script and make the firearm app check an output if already installed (Otherwise, it will notify you to do so).

The grammar of the shell script includes the following four tags:

```
/bin/bash ./run_emp.sh -f <Name of your Python script to run> 
                       -o <Optional: test or debug> 
                       -s <Optional: Scale of Testing Complexity> 
                       -t <Optional: Target Directory>
```

For example, copy and paste the command into your terminal, which will run <a href="https://github.com/hicsail/SIEVE/blob/main/examples/substring_search/IR0/between.py">    between.py</a> in debug mode.<br>

```
   /bin/bash ./shell/run_IR0.sh -f between -o debug
```

Here are the meanings of the four tags:

<strong> -f (Required) </strong>: Name of your Python script to run (such as "between" and "after")

<strong> -o (Optional) </strong>: Choose a mode to run your python script: 
  <ul>
    <li> "test" produces a synthetic test case, including an input text and target substrings. 
    <li> "debug" uses your own text corpus input in <a href="https://github.com/hicsail/SIEVE/blob/main/examples/dfa_test_input.txt"> dfa_test_input.txt</a>
    <li> If the second argument is empty, it will assume a "debug" operation
  </ul>

<strong> -s (Optional) </strong>: Choose a scale of test complexity (e.g., 0 and 1, default = 0)
<ul>

  This value will be used as a parameter by <a href="https://github.com/hicsail/zk-NLP/blob/425e0a1e8a163241fc509bffcac28c1e3e6f8962/examples/substring_search/common/util.py#L74-L83"> the generate_text function </a>

</ul>


<strong> -t (Optional) </strong>: Choose a directory to save interim outputs (.rel, .ins, .wit files)


<strong> 2) Python </strong> 

You can also run each script without the shell script. Here is an example:

```
python3 examples/substring_search/IR0/after_all_multi.py 'irs' 230584300921369395 'p2' 3 test
```

This will run the after_all_multi algorithm in the field size of '230584300921369395' in test mode and the input scale of 3 ('p2' is not as important a parameter as the rest of the arguments).


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



## <strong> Manual Execution for EMP-ZK tool (Deprecated) </strong>

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
