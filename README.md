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

## Walkthrough: Simple Neural Network
This section will explain step-by-step how to use MiniWizPL to prove
in ZK that the execution of a secret neural network model produces
a specific output given a secret input. The code snippets are taken
from the example python file:
`examples/simple_demos/nn_tutorial_example.py`.


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

In order to compile our output we must next install
[EMP-ZK](https://github.com/emp-toolkit/emp-zk) by running the
following commands:

```
wget https://raw.githubusercontent.com/emp-toolkit/emp-readme/master/scripts/install.py
python3 install.py --deps --tool --ot --zk
```

Once we have installed EMP-ZK, we can now compile the generated `cpp`
file, making sure that we add the directory `miniwizpl/boilerplate` to
the include path for the compiler.

```
cp examples/neural_networks/miniwizpl_test.cpp examples/neural_networks/miniwizpl_test.cpp.emp_wit .
g++ -I./miniwizpl/boilerplate \
    -pthread -Wall -funroll-loops -Wno-ignored-attributes -Wno-unused-result -march=native -maes -mrdseed -std=c++11 -O3 \
    miniwizpl_test.cpp -lemp-zk -lemp-tool -lcrypto \
    -o miniwizpl_test
```

Once we have compiled our EMP code, we can run the `miniwizpl_test`
executable in the following way, with the prover running:

```
./miniwizpl_test 1 12349
```

and the verifier running:
```
./miniwizpl_test 2 12349
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

(TODO: perhaps make the example more concrete? Like MNIST?)
