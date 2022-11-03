import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from . import SecretTensor, Prim, val_of, AST

old_relu = F.relu
def my_relu(x):
    #print('ReLU Override successful')
    if isinstance(x, AST):
        return Prim('relu', [x], old_relu(val_of(x)))
    else:
        return old_relu(x)

F.relu = my_relu

old_linear = F.linear
def my_linear(inp, weight, bias):
    #print('Linear Override successful')
    if isinstance(inp, AST) or isinstance(weight, AST) or isinstance(bias, AST):
        # TODO: might we need intermediate values here? (i.e. fix "None")
        return Prim('matplus', [Prim('matmul', [inp, SecretTensor(weight.T)], None),
                                SecretTensor(bias)],
                    old_linear(val_of(inp), val_of(weight), val_of(bias)))
    else:
        return old_linear(inp, weight, bias)
F.linear = my_linear

old_softmax = F.log_softmax
def my_log_softmax(x, dim=1):
    #print('Softmax Override successful')
    if isinstance(x, AST) or isinstance(dim, AST):
        # TODO: support additional dimensions
        return Prim('log_softmax', [x], old_softmax(val_of(x)))
    else:
        return old_softmax(x, dim)

F.log_softmax = my_log_softmax

old_cat = torch.cat
def my_cat(to_cat, dim):
    # print('Concatenate Override successful')
    assert isinstance(to_cat, tuple)
    assert len(to_cat) == 2

    if isinstance(to_cat[0], AST) or isinstance(to_cat[1], AST) or isinstance(dim, AST):
        return Prim('cat', [to_cat[0], to_cat[1], dim],
                    old_cat((val_of(to_cat[0]), val_of(to_cat[1])),
                            val_of(dim)))
    else:
        return old_cat(to_cat, dim)
torch.cat = my_cat
