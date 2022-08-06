#!/bin/bash
set -euo pipefail

#declare -a examples=("mnist_wizpl.py" "nn_tutorial_example.py" "nn_example.py" "nn_example2.py" "rnn_example.py")
declare -a examples=("mnist_wizpl.py" "nn_tutorial_example.py" "rnn_example.py")
for i in "${examples[@]}"
do
    cd examples/neural_networks
    python3 $i
    cp miniwizpl_test.cpp miniwizpl_test.cpp.emp_wit ../..
    cd ../..
    g++ -I./miniwizpl/boilerplate \
        -pthread -Wall -funroll-loops -Wno-ignored-attributes -Wno-unused-result -march=native -maes -mrdseed -std=c++11 -O3 \
        miniwizpl_test.cpp -lemp-zk -lemp-tool -lcrypto \
        -o miniwizpl_test
    ./miniwizpl_test 1 12348 & ./miniwizpl_test 2 12348
    rm miniwizpl_test.cpp miniwizpl_test.cpp.emp_wit
done
