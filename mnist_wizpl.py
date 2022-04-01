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
model.load_state_dict(torch.load('mnist.pt'))
model.eval()

print('model architecture:')
print(model)

# Run the model on a secret input
print('output on a test input:')
test_input = SecretTensor(torch.randn(1, 784))
output = model(test_input)
print(output)

# Compile the output to EMP
print_emp(output, 'miniwizpl_test.cpp')
