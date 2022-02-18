import numpy as np
from mini_wizpl import SecretArray, relu, print_emp

# simple neural network

N_FEATURES = 7
N_EXAMPLES = 1
N_HIDDEN = 12

# initialize inputs randomly
inputs = SecretArray(np.random.randint(-10, high=10, size=(N_EXAMPLES, N_FEATURES)))

# initialize weights randomly
inp_layer = SecretArray(np.random.randint(-10, high=10, size=(N_FEATURES, N_HIDDEN)))

# build hidden layers w/ random weights + relu activation
net = relu(inputs @ inp_layer)
for _ in range(3):
    layer = SecretArray(np.random.randint(-10, high=10, size=(N_HIDDEN, N_HIDDEN)))
    net = relu(net @ layer)

# binary output layer
outp_layer = SecretArray(np.random.randint(-10, high=10, size=(N_HIDDEN, 2)))
net = net @ outp_layer

# print the result
print(net.val())

print_emp(net, 'miniwizpl_test.cpp')
