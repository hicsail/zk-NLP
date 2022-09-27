FROM alpine:latest
WORKDIR /usr/src/app

RUN apk update && apk add\
    build-base \
    python3 \
    py3-pip\
    python3-dev\
    # py3-numpy\
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
RUN pip3 install numpy
RUN python3 install.py --deps --tool --ot --zk

RUN python3 examples/simple_demos/simple.py

RUN g++  miniwizpl_test.cpp -o miniwizpl_test\
    -pthread -Wall -funroll-loops -Wno-ignored-attributes -Wno-unused-result -march=native -maes -mrdseed -std=c++11 -O3 \
    -L/usr/lib/openssl/lib -lssl -lcrypto \
    -L./emp-zk/emp-zk -lemp-zk\
    -L./emp-tool/emp-tool -lemp-tool\
    -I./miniwizpl/boilerplate -I/usr/lib/openssl/include

# ENTRYPOINT ["./miniwizpl_test", "1", "12349","&", "&&", "./miniwizpl_test", "2", "12349"]
RUN chmod +x ./shell.sh

ENTRYPOINT [ "/bin/bash", "/usr/src/app/shell.sh","&", "&&", "sleep", "infinity"]

