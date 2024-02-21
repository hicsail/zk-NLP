
FROM ubuntu:latest
WORKDIR /usr/src/app

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "sleep", "infinity" ]