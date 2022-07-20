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
```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR
```

```python
from miniwizpl import utils, SecretTensor, print_emp, compare_secret_tensors
import miniwizpl.torch
```

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

```python
test_input = torch.randn(1, 784)
test_input = SecretTensor(test_input)
```

```python
output = model(test_input)
```

```python
expected_output = SecretTensor(output.val)
output = compare_secret_tensors(output, expected_output)
```

```python
print_emp(output, "miniwizpl_nn.cpp")
```
