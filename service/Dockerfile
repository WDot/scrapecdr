FROM library/ubuntu:latest

RUN apt-get update
RUN apt -y install ssh
RUN apt -y install cmake
RUN apt -y install python3
RUN apt -y install python3-pip
RUN apt -y install nginx
RUN apt -y install default-jre
RUN pip3 install sklearn
RUN pip3 install pandas
RUN pip3 install numpy
RUN pip3 install scipy
RUN pip3 install flask
RUN pip3 install waitress
RUN pip3 install requests
RUN pip3 install editdistance
RUN pip3 install Scrapy
RUN pip3 install bleach[css]

WORKDIR /app

COPY . /app

ENTRYPOINT bash start.sh
