#!/bin/bash
set -euo pipefail

cp miniwizpl/boilerplate/* .
declare -a examples=("gale_shapley_emp.py")
for i in "${examples[@]}"
do
    cd examples
    python3 $i
    cp miniwizpl_test.cpp ..
    cd ..
    g++ -pthread -Wall -funroll-loops -Wno-ignored-attributes -Wno-unused-result -march=native -maes -mrdseed -std=c++11 -O3 \
        miniwizpl_test.cpp -lemp-zk -lemp-tool -lcrypto \
        -o miniwizpl_test
    ./miniwizpl_test 1 12345 & ./miniwizpl_test 2 12345
    rm miniwizpl_test.cpp
done

cd examples
python3 dfa_example.py dfa_test_input.txt
cp miniwizpl_test.cpp ..
cd ..
g++ -pthread -Wall -funroll-loops -Wno-ignored-attributes -Wno-unused-result -march=native -maes -mrdseed -std=c++11 -O3 \
    miniwizpl_test.cpp -lemp-zk -lemp-tool -lcrypto \
    -o miniwizpl_test
./miniwizpl_test 1 12345 & ./miniwizpl_test 2 12345
rm miniwizpl_test.cpp
