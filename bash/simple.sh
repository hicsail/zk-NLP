#!/bin/bash
set -euo pipefail

declare -a examples=("secret_indexing.py"	"simple.py" "simple_loop.py" "stack_example.py")
for i in "${examples[@]}"
do
    echo "testing ${i}"
    cd examples/simple_demos
    python3 $i
    cp miniwizpl_test.cpp miniwizpl_test.cpp.emp_wit ../..
    cd ../..
    g++ -I./miniwizpl/boilerplate \
        -pthread -Wall -funroll-loops -Wno-ignored-attributes -Wno-unused-result -march=native -maes -mrdseed -std=c++11 -O3 \
        miniwizpl_test.cpp -lemp-zk -lemp-tool -lcrypto \
        -o miniwizpl_test
    ./miniwizpl_test 1 12349 & ./miniwizpl_test 2 12349
    rm miniwizpl_test.cpp miniwizpl_test.cpp.emp_wit
done
