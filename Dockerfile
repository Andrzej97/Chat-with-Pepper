FROM ubuntu:latest

# install python
RUN apt-get update && apt-get install -y \
	sudo \
	python2.7 \
	python-pip \
	python3.6 \
	python3-pip \
	wget \
	software-properties-common # to enable 'apt-get-repository'

# copy file requirements.txt from your host, this file contains required python packages
COPY ./docker/requirements.txt ./requirements.txt

COPY ./docker/morfeusz2_1.9.13-18.04_amd64.deb ./morfeusz2_1.9.13-18.04_amd64.deb	

COPY ./docker/python3-morfeusz2_0.4.0-18.04_amd64.deb ./python3-morfeusz2_0.4.0-18.04_amd64.deb

WORKDIR /

RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

USER docker

RUN pip3 install -r requirements.txt

# morfeus2 installation
RUN echo docker | sudo -S wget -O - http://download.sgjp.pl/apt/sgjp.gpg.key | sudo apt-key add -
RUN echo docker | sudo -S apt-add-repository http://download.sgjp.pl/apt/ubuntu
RUN echo docker | sudo apt update
RUN echo docker | sudo apt install python3-morfeusz2
RUN echo docker | sudo apt install -y morfeusz2

# mongo installation
#RUN echo docker | sudo -S apt-get update && sudo apt-get install -y mongodb

COPY . ./Chat-with-Pepper
RUN echo docker |sudo -S find /Chat-with-Pepper -type d -exec chmod 777 {} \;

