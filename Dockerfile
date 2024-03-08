FROM ubuntu:latest
WORKDIR /usr/src/app

RUN apt update && apt install -y\
    build-essential\
    python3 \
    python3-pip\
    python3-dev\
    python3-numpy\
    git \
    cmake\
    make\
    libssl-dev\
    bash\
    musl-dev\
    nano\
    wget\
    unzip\
    uuid-dev\
    default-jdk\
    && apt upgrade -y

COPY . .

RUN pip3 install --upgrade pip && \
    pip3 install .

RUN pip3 install -r requirements.txt

RUN pip3 install git+https://github.com/gxavier38/pysnark.git@8a2a571bef430783adf8fe28cb8bb0b0bf8a7c94

CMD [ "sleep", "infinity" ]