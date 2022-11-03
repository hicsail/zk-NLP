#!/bin/bash
set -euo pipefail

# cd examples
# python3 gale_shapley_emp.py
# cp miniwizpl_test.cpp miniwizpl_test.cpp.emp_wit ..
# cd ..
# g++ -pthread -Wall -funroll-loops -Wno-ignored-attributes -Wno-unused-result -march=native -maes -mrdseed -std=c++11 -O3 \
#     miniwizpl_test.cpp -lemp-zk -lemp-tool -lcrypto \
#     -o miniwizpl_test
# ./miniwizpl_test 1 12346 & ./miniwizpl_test 2 12346
# rm miniwizpl_test.cpp miniwizpl_test.cpp.emp_wit
echo "testing dfa_example.py"
cd examples
python3 dfa_example.py dfa_test_input.txt
cp miniwizpl_test.cpp miniwizpl_test.cpp.emp_wit ..
cd ..
g++ -I./miniwizpl/boilerplate \
    -pthread -Wall -funroll-loops -Wno-ignored-attributes -Wno-unused-result -march=native -maes -mrdseed -std=c++11 -O3 \
    miniwizpl_test.cpp -lemp-zk -lemp-tool -lcrypto \
    -o miniwizpl_test
./miniwizpl_test 1 12347 & ./miniwizpl_test 2 12347
rm miniwizpl_test.cpp miniwizpl_test.cpp.emp_wit
