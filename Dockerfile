
# FROM ubuntu:latest

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
# RUN pip3 install numpy==1.18
RUN python3 install.py --deps --tool --ot --zk

# RUN git clone https://github.com/emp-toolkit/emp-tool.git --branch master
# WORKDIR /usr/src/app/emp-tool
# RUN cmake .
# RUN make -j4
# RUN make install
# WORKDIR /usr/src/app

# RUN git clone https://github.com/emp-toolkit/emp-ot.git --branch master
# WORKDIR /usr/src/app/emp-ot
# RUN cmake .
# RUN make -j4
# RUN make install
# WORKDIR /usr/src/app

# RUN git clone https://github.com/emp-toolkit/emp-zk.git --branch master
# WORKDIR /usr/src/app/emp-zk
# RUN cmake .
# RUN make -j4
# RUN make install
# WORKDIR /usr/src/app

RUN python3 examples/simple_demos/simple.py

RUN g++ -I./miniwizpl/boilerplate -I/usr/lib/openssl/include -I./emp-zk/emp-zk -I ./emp-tool/emp-tool -I./emp-ot/emp-ot -I./emp-zk -I./emp-tool -I./emp-ot\ 
    -L./emp-zk/emp-zk-lemp-zk\
    -L./emp-tool/emp-tool-lemp-tool\
    -L/usr/lib/openssl/lib -lssl -lcrypto \
    -pthread -Wall -funroll-loops -Wno-ignored-attributes -Wno-unused-result -march=native -maes -mrdseed -std=c++11 -O3 \
    miniwizpl_test.cpp -o miniwizpl_test

ENTRYPOINT ["./miniwizpl_test" ]


