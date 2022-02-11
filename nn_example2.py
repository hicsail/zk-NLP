import numpy as np
from mini_wizpl import SecretArray, relu, print_emp

# simple neural network

N_FEATURES = 784
N_EXAMPLES = 1
N_HIDDEN = 128

# initialize inputs randomly
inputs = SecretArray(np.random.randint(-10, high=10, size=(N_EXAMPLES, N_FEATURES)))

# initialize weights randomly
inp_layer = SecretArray(np.random.randint(-10, high=10, size=(N_FEATURES, 512)))

# build hidden layers w/ random weights + relu activation
net = relu(inputs @ inp_layer)

# hidden layer
layer = SecretArray(np.random.randint(-10, high=10, size=(512, 64)))
net = relu(net @ layer)

# hidden layer
layer = SecretArray(np.random.randint(-10, high=10, size=(64, 10)))
net = relu(net @ layer)

# binary output layer
outp_layer = SecretArray(np.random.randint(-10, high=10, size=(10, 2)))
net = net @ outp_layer

# print the result
print(net.val())
print(net)

print_emp(net, 'miniwizpl_test.cpp')
