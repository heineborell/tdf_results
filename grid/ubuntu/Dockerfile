FROM ubuntu:latest

RUN apt-get update && \ 
	apt-get install -y curl build-essential && \
	apt install wget && \
	apt-get install -y git &&  \
	apt-get install -y python3 python3-pip &&\
	apt-get install -y neovim &&\
	apt-get clean


#RUN apt-get install -y chromium  chromium-driver &&\
#	apt-get install -y chromium-browser 
## Set the environment variables for Chromium
#ENV CHROME_BIN=/usr/bin/chromium
#ENV CHROME_DRIVER=/usr/bin/chromium-driver

WORKDIR /project

COPY requirements.txt /project/

RUN apt-get install -y virtualenv && \
	mkdir envs && \
	cd envs && virtualenv -p python3 tdf

RUN git clone https://github.com/heineborell/tdf_results


