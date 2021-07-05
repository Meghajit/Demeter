FROM ubuntu:16.04

RUN groupadd container_users && useradd -ms /bin/bash -g container_users belmont
RUN apt-get update && apt-get -y install software-properties-common
RUN apt-get -y install build-essential
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get -y install python3.7
RUN rm /usr/bin/python3
RUN ln -s /usr/bin/python3.7 /usr/bin/python3
RUN apt-get -y install python3-pip
RUN python3 -m pip install --upgrade pip
RUN apt-get -y install curl

USER belmont

ENV DEMETER_DIR /home/belmont/demeter/
ENV PATH /home/belmont/.local/bin:$PATH
ENV FLASK_APP="api.py"
ENV FLASK_ENV="production"

RUN mkdir -p $DEMETER_DIR
ADD . $DEMETER_DIR

WORKDIR $DEMETER_DIR

RUN ls -la

RUN pwd

RUN python3 -m pip install --no-cache-dir -t /home/belmont/.local/bin --force-reinstall -r ./requirements.txt

CMD flask run --port=8080 --host=0.0.0.0