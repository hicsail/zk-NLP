import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from mini_wizpl import SecretTensor, Prim, print_emp

old_relu = F.relu
def my_relu(x):
    #print('ReLU Override successful')
    return Prim('relu', [x])

F.relu = my_relu

old_linear = F.linear
def my_linear(inp, weight, bias):
    #print('Linear Override successful')
    return Prim('matplus', [Prim('matmul', [inp, SecretTensor(weight.T)]),
                            SecretTensor(bias)])
#return old_addmm(inp, mat1, mat2)
F.linear = my_linear

old_softmax = F.log_softmax
def my_softmax(x, dim=1):
    #print('Softmax Override successful')
    return Prim('softmax', [x, dim])
#return old_addmm(inp, mat1, mat2)
F.log_softmax = my_softmax

old_cat = torch.cat
def my_cat(to_cat, dim):
    print('Concatenate Override successful')
    return Prim('cat', [to_cat[0], to_cat[1], dim])
torch.cat = my_cat
