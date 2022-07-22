import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR
from miniwizpl import SecretTensor, PublicTensor, print_emp, compare_tensors
import miniwizpl.torch

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

test_input = torch.randn(1, 784)
test_input = SecretTensor(test_input)

output = model(test_input)
expected_output = PublicTensor(output.val)
output = compare_tensors(output, expected_output)

# Compile the output to EMP
print_emp(output, "miniwizpl_nn.cpp")
