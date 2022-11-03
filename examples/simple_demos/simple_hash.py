import numpy as np
from miniwizpl import *

n = 100
input_vec = [1,2,3,4]
input_vec = [SecretInt(v) for v in input_vec]
p = 97
np.random.seed(1)

rvec = np.random.randint(0, p, (len(input_vec), len(input_vec)))

state = input_vec
for _ in range(n):
    state = np.dot(rvec, state)
    #state = np.mod(state, p)

# size of the AST is exponential in n
# because there is no sharing for subexpressions
# for s in state:
#     print(s)
#     print()
output = state[0]

assert0(output)
print_ir0("miniwizpl_test_ir0")
