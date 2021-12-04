FROM ubuntu:18.04
FROM httpd:2.4

RUN groupadd container_users && useradd -ms /bin/bash -g container_users belmont
RUN apt-get update && apt-get -y install software-properties-common
RUN apt-get -y install build-essential
RUN apt-get -y install python3-pip
RUN python3 -m pip install --upgrade pip
RUN apt-get -y install curl

# giving access of apache logs directory to belmont user and the group
RUN chown belmont:container_users /usr/local/apache2/logs

USER belmont

ENV DEMETER_DIR /home/belmont/demeter/
ENV PATH /home/belmont/.local/bin:$PATH
ENV FLASK_APP="api.py"
ENV FLASK_ENV="production"

RUN mkdir -p $DEMETER_DIR
ADD . $DEMETER_DIR

WORKDIR $DEMETER_DIR
COPY ./ui/ /usr/local/apache2/htdocs/

RUN python3 -m pip install -r requirements.txt
CMD bash start.sh