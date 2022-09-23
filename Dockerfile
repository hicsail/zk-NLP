FROM alpine:latest
WORKDIR /usr/src/app

RUN apk update && apk add\
    build-base \
    python3 \
    py3-pip\
    python3-dev\
    py3-numpy\
    git \
    cmake\
    make\
    openssl-dev\
    bash\
    musl-dev\
    && apk upgrade

COPY . .

RUN . venv/bin/activate
RUN pip3 install .
RUN python3 install.py --deps --tool --ot --zk

RUN python3 examples/simple_demos/simple.py

RUN g++ -I./miniwizpl/boilerplate -I/usr/lib/openssl/include -I./emp-zk/emp-zk -I ./emp-tool/emp-tool -I./emp-ot/emp-ot -I./emp-zk -I./emp-tool -I./emp-ot\ 
    -L./emp-zk/emp-zk-lemp-zk\
    -L./emp-tool/emp-tool-lemp-tool\
    -L/usr/lib/openssl/lib -lssl -lcrypto \
    -pthread -Wall -funroll-loops -Wno-ignored-attributes -Wno-unused-result -march=native -maes -mrdseed -std=c++11 -O3 \
    miniwizpl_test.cpp -o miniwizpl_test

ENTRYPOINT ["./miniwizpl_test" ]


