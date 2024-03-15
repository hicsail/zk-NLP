# zk-NLP

zk-NLP repository provides an E2E pipeline, supported by picozk, to test differential privacy under Zero-Knowledge Proof.

----

## Quick Navigation

- [Use Docker](#-use-docker)
- [Run Locally](#-run-locally)

## 🐳 [Use Docker](#-use-docker)


#### 🚧 Build Docker Image and Run Container

##### <ins><i> Option A Use published docker image </i> </ins>

Run this line of code in the command line:
```
docker run --platform linux/amd64 -it hicsail/zk-nlp:main
```

##### <ins><i> Option B Clone Repo </i> </ins>

Run the following in the command line to get the container up and running:
```
git clone https://github.com/hicsail/zk-NLP.git     # Clone the repository
cd zk-NLP                                           # Move into the root directory of the project
docker-compose up -d --build                        # Inside the root directory, run the build image:
```


#### 🖥️ Getting started

##### <ins><i> Step1: Enter Docker Shell</i> </ins>

Since you have a running container, you can subsequently run the following command in your terminal to start Docker Shell:

```
docker exec -it <containerID> bash
```

You can get a container-ID from the docker desktop app by clicking the small button highlighted in the red circle
<ul>
    <img width="1161" alt="image" src="https://user-images.githubusercontent.com/62607343/203409123-1a95786f-8b2a-4e71-a920-3a51cf50cf0f.png">
</ul>

If you see something like the following in your command line, you are successfully inside the docker shell
<ul>
<img width="300" alt="image" src="https://user-images.githubusercontent.com/62607343/203413803-19021cb9-07ba-4376-ade0-dbdc6c8506c5.png">
</ul>


##### <ins><i> Step2: Install wiztoolkit</i> </ins>

We are using Fire Alarm, one of wiztoolkit packages.
After entering the container, clone wiztoolkit repo and run the following commands to install wiztoolkit:

(* You might need to set up ssh key - Follow <a href="https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=linux"> the instruction </a>)

```
git clone git@github.mit.edu:sieve-all/wiztoolkit.git
cd wiztoolkit
make
make install
```

#### 🏋️‍♀️ Run shell script

All of the main scripts to run are stored in the <a href="https://github.com/hicsail/zk-NLP/tree/main/examples/substring_search/IR0"> example/substring_search/IR0 directory </a>.

You can run your Python script in the docker shell, which outputs zk statements, using 'miniwizpl', and check its format by Fire Alarm you have just installed.

You may run any of them in the docker shell either way described hereunder:

For example, copy and paste the command into your terminal, which will run <a href="https://github.com/hicsail/SIEVE/blob/main/examples/substring_search/IR0/between.py">    between.py</a> in debug mode.<br>

```
   /bin/bash ./shell/run_IR0.sh -f between -o debug
```

The grammar of the shell script includes the following four tags:

```
/bin/bash ./run_emp.sh -f <Name of your Python script to run> 
                       -o <Optional: test or debug> 
                       -s <Optional: Scale of Testing Complexity> 
                       -t <Optional: Target Directory>
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


You can also run each script without the shell script without a Fire Alarm check. Here is an example:

```
python3 examples/substring_search/IR0/after_all_multi.py 'irs' 230584300921369395 'p2' 3 test
```

This will run the after_all_multi algorithm in the field size of '230584300921369395' in test mode and the input scale of 3 ('p2' is not as important a parameter as the rest of the arguments).


## 👨‍💻 [Run Locally](#-run-locally)

This option doesn't require Docker, while it focuses on running the Python scripts, skipping setting Fire Alarm.

Run this in the command line:
```
git clone git@github.com:hicsail/zk-NLP.git 
```        

Move into the root directory of the project and install dependencies

```
cd zk-NLP
python3 -m venv venv           # or pypy3 -m venv myenv
source venv/bin/activate       # or source myenv/bin/activate
pip3 install --upgrade pip     # or pypy3 -m pip install --upgrade pip
pip3 install -r requirements.txt  # or pypy3 -m pip install -r requirements.txt
pip3 install .                 # or pypy3 -m pip install .
pip3 install git+https://github.com/gxavier38/pysnark.git@8a2a571bef430783adf8fe28cb8bb0b0bf8a7c94
```

The following will run the main file:
```
python3 zk-NLP.py  # or pypy3 zk-NLP.py
```

## <strong> EMP-ZK tool (Deprecated) </strong>

In case you want to experiment manually, run inside the docker shell:

```
python[3] examples/simple_demos/simple.py
```

Run the following command:

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
