
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
    && apt upgrade -y

COPY . .

RUN pip3 install -r requirements.txt
RUN python3 install.py --deps --tool --ot --zk
RUN ldconfig

CMD [ "sleep", "infinity" ]