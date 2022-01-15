FROM ubuntu:18.04
FROM httpd:2.4

RUN groupadd container_users && useradd -ms /bin/bash -g container_users belmont
RUN echo "Acquire::Check-Valid-Until \"false\";\nAcquire::Check-Date \"false\";" | cat > /etc/apt/apt.conf.d/10no--check-valid-until
RUN apt-get update && apt-get -y install software-properties-common
RUN apt-get -y install build-essential
RUN apt-get -y install python3-pip
RUN python3 -m pip install --upgrade pip
RUN apt-get -y install curl
RUN apt-get -y install jq

USER belmont

ENV DEMETER_DIR /home/belmont/demeter
ENV PATH /home/belmont/.local/bin:$PATH
ENV FLASK_APP="api.py"
ENV FLASK_ENV="production"

RUN mkdir -p $DEMETER_DIR
RUN mkdir -p $DEMETER_DIR/files

ADD . $DEMETER_DIR

USER root
RUN chown -R belmont:container_users $DEMETER_DIR/files/

USER belmont
COPY ./files/  $DEMETER_DIR/files/

WORKDIR $DEMETER_DIR
COPY ./ui/ /usr/local/apache2/htdocs/

RUN python3 -m pip install -r requirements.txt
CMD ["bash", "getNav.sh"]
