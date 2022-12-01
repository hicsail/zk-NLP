
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

RUN pip3 install -r requirements.txt
RUN python3 install.py --deps --tool --ot --zk
RUN ldconfig

RUN git clone https://github.com/stealthsoftwareinc/wiztoolkit.git

CMD [ "sleep", "infinity" ]