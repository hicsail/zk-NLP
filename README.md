# miniWizPL

A Python library and compiler for writing zero-knowledge statements

[[_TOC_]]

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

## Generating Documentation

Documentation can be generated with `pdoc3`:

```
pip install pdoc3
pdoc --http localhost:8080 miniwizpl
```

## Walkthrough: Simple Neural Network
This section will explain step-by-step how to use MiniWizPL to prove
in ZK that the execution of a secret neural network model produces
a specific output given a secret input. The code snippets are taken
from the example python file: [nn_tutorial_example.py](examples/neural_networks/nn_tutorial_example.py).


By default the Python file produces a ZK statement that can be
fed into EMP toolkit ZK backend. This section assumes
that the reader possesses working knowledge of PyTorch.


The first step is to make the necessary imports from PyTorch to create
the neural network model:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR
```

Additionally, we must import the relevant MiniWizPL libraries:

```python
from miniwizpl import SecretTensor, PublicTensor, print_emp, compare_tensors
import miniwizpl.torch
```

`SecretTensor` is a class that defines what pieces of data are secret
by wrapping PyTorch tensors. `print_emp` is a function that produces
the final ZK statement for the ZK backend. `compare_tensors`
is a function that appends a special comparison function to the ZK
statement given two `SecretTensors`, or one `SecretTensor` and
`PublicTensor` (a `PublicTensor` behaves almost exactly like a
`SecretTensor` in miniWizPL, with the difference being that miniWizPL
will generate public values instead of secret values in EMP to
represent the contents of the tensor).
And finally, `miniwizpl.torch` contains overloads for
various PyTorch functions that allows the program to simultaneously
perform the neural network operations and progressively build up the
final ZK statement.


The next step is to define our neural network model. Below is a
class that implements a fully-connected neural net with in PyTorch.
The neural net has two layers called `fc1` and `fc2`.
The final line instantiates the class.

```python
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(784, 32)
        self.fc2 = nn.Linear(32, 10)

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output

model = Net()
```
In addition to defining our model, we initialize the input to
our model. The first line initializes a PyTorch tensor representing
an input vector. The second line turns that PyTorch tensor into
a secret PyTorch tensor.

```python
test_input = torch.randn(1, 784)
test_input = SecretTensor(test_input)
```

Once we have defined our input and model, we can pass the input into
our model the same way we would normally do in PyTorch:

```python
output = model(test_input)
```

Under the hood, this is using the overloaded functions from
`miniwizpl.torch` that take `SecretTensor`s as inputs. The functions
behave the same way as the PyTorch functions, but with additional
information contained in the output. The result that normally would be
produced by invoking the model in PyTorch is stored inside
`output.val`. The remainder of the information stored in `output` is a
syntax tree used to produce the final output ZK statement.

We wish to prove that our secret input fed into our secret model
produces a specific output, so we additionally must call the
`compare_tensors` function.

```python
expected_output = PublicTensor(output.val)
output = compare_tensors(output, expected_output)
```

Finally, we pass `output` into the `print_emp` function, which
generates a ZK statement from the syntax tree inside `output` and
stores it inside the file `miniwizpl_test.cpp`. This also generates
a file called `miniwizpl_test.cpp.emp_wit`.

```python
print_emp(output, "miniwizpl_test.cpp")
```

(TODO: perhaps make the example more concrete? Like MNIST?)


## Walkthrough: DSA

This section will explain step-by-step how to use MiniWizPL to verify
in ZK a cryptographic signature computed via
[DSA](https://en.wikipedia.org/wiki/Digital_Signature_Algorithm). The
code snippets are taken from the example python file:
[dsa.py](examples/crypto/dsa.py).

We will make use of the third party library
[Galois](https://github.com/mhostetter/galois) to handle finite field operations

```python
import random
import galois
```

Additionally, we must import the relevant MiniWizPL libraries:

```python
from miniwizpl import SecretInt, assertTrueEMP, pow, print_emp, set_bitwidth
```

The class `SecretInt` is a wrapper for adding Python integers to the
Witness. The function `assertTrueEMP` adds an assertion will get
inserted as a statement in the resulting ZK statement that will be
checked the verifier when running the EMP executable. The function
`print_emp` produces the C++ file to be compiled against EMP-ZK.  The
function `pow` is a MiniWizPL overload of the Python math exponent
function. Finally the function `set_bitwidth` is used to set a
configuration variable in EMP.

Our next steps are just vanilla DSA: implement functions for
generating the key pair, signing and verifying the message:

```python


# Generate the parameters for DSA

def gen_params():
    N = 8
    L = 12  # we get this many bits of security

    q = galois.random_prime(N)
    p = galois.random_prime(L)
    while (p-1)%q != 0:
        p = galois.next_prime(p)

    h = 2
    g = pow(h, (p-1)//q, p)
    return p, q, g

p, q, g = gen_params()

# Generate keys
def gen_key():
    x = random.randint(1, q-1)
    y = pow(g, x, p)
    return x, y

# Sign the message
def sign(m):
    k = random.randint(1, q-1)
    r = pow(g, k, p) % q
    s = (pow(k, q-2, q) * (m + sk*r)) % q
    return r, s

# Verify the message
def verify(r, s, m):
    w = pow(s, q-2, q)
    u1 = (m*w) % q
    u2 = (r*w) % q
    v = ((pow(g, u1, p) * pow(pk, u2, p)) % p) % q
    return v == r



message = 5

# generate keys and sign the message
sk, pk = gen_key()
r, s = sign(message)

```

Finally, we generate our statement to be verified, by
passing in `SecretInt(message)`, along with the signature
parameters. We pass the output into `assertTrueEMP` so that it checked
by the Verifier, and we finally call `print_emp` to generate the cpp
file to be compiled against EMP-ZK.

```python
output = verify(r, s, SecretInt(message))
assertTrueEMP(output)
print_emp(True, 'miniwizpl_test.cpp')

```

## Executing your example in EMP-ZK

In order to compile the output we next install
[EMP-ZK](https://github.com/emp-toolkit/emp-zk) by running the
following commands:

```sh
git clone https://github.com/emp-toolkit/emp-tool.git --branch 0.2.4
cd emp-tool
cmake -DCMAKE_BUILD_TYPE=Release .
make -j4
make install
cd ..
git clone https://github.com/emp-toolkit/emp-ot.git --branch 0.2.3
cd emp-ot
cmake -DCMAKE_BUILD_TYPE=Release .
make -j4
make install
cd ..
git clone https://github.com/emp-toolkit/emp-zk.git --branch 0.2.0
cd emp-zk
cmake -DCMAKE_BUILD_TYPE=Release .
make -j4
make install
cd ..
```

Once we have installed EMP-ZK, we can now compile the generated C++
file, making sure that we add the directory `miniwizpl/boilerplate` to
the include path for the compiler.

```sh
cp examples/neural_networks/miniwizpl_test.cpp examples/neural_networks/miniwizpl_test.cpp.emp_wit .
g++ -I./miniwizpl/boilerplate \
    -pthread -Wall -funroll-loops -Wno-ignored-attributes -Wno-unused-result -march=native -maes -mrdseed -std=c++11 -O3 \
    miniwizpl_test.cpp -lemp-zk -lemp-tool -lcrypto \
    -o miniwizpl_test
```

Once we have compiled our EMP code, the prover runs:
```sh
./miniwizpl_test 1 $PORT_NUMBER
```

and the verifier runs:

```sh
./miniwizpl_test 2 $PORT_NUMBER
```

The first command line argument indicates whether or not to run the
executable as the prover or verifier, respectively denoted by a `1`
or `2`. The second command line argument represents the communication
port. For a successful proof, the above command should run and return
a non-zero exit code. For a failed proof, the above should report a
failed assertion.

(TODO: clarify how we would in actuality have two separate .cpp files,
one for the prover and one for the verifier along with a witness file
only accessible to the prover. Clarify how to compile these two files
separately into two executables. Also, clarify how we would handle
communication between separate machines as "localhost" is currently
hardcoded into miniWizPL)
