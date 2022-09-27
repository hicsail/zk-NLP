import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR

from miniwizpl import SecretTensor, Prim, print_emp
from mnist_model import Net
import miniwizpl.torch

model = Net()
model.load_state_dict(torch.load('./examples/neural_networks/mnist.pt'))
model.eval()

print('model architecture:')
print(model)

# Run the model on a secret input
print('output on a test input:')
test_input = torch.randn(1, 784)
output = model(test_input)
print(output)

print('output on a secret input:')
secret_input = SecretTensor(test_input)
secret_output = model(secret_input)
print(secret_output)

# Compile the output to EMP
print_emp(secret_output, 'miniwizpl_test.cpp')
