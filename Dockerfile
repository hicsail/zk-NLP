FROM hicsail/zk-oracles:main
WORKDIR /usr/src/app

COPY . .

RUN pip3 install --upgrade pip && \
    pip3 install .

RUN pypy3 -m pip install -r requirements.txt

RUN pip3 install git+https://github.com/gxavier38/pysnark.git@8a2a571bef430783adf8fe28cb8bb0b0bf8a7c94

CMD [ "sleep", "infinity" ]