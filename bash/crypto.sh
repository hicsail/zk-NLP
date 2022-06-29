#!/bin/bash
set -euo pipefail

cp miniwizpl/boilerplate/* .
#declare -a examples=("rsa_bignum.py" "dsa.py" "fv.py")
declare -a examples=("rsa_bignum.py")
for i in "${examples[@]}"
do
    cd examples/crypto
    python3 $i
    cp miniwizpl_test.cpp ../..
    cd ../..
    g++ -pthread -Wall -funroll-loops -Wno-ignored-attributes -Wno-unused-result -march=native -maes -mrdseed -std=c++11 -O3 \
        miniwizpl_test.cpp -lemp-zk -lemp-tool -lcrypto \
        -o miniwizpl_test
    ./miniwizpl_test 1 12345 & ./miniwizpl_test 2 12345
    rm miniwizpl_test.cpp
done
