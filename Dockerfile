FROM nginx

COPY . /project
WORKDIR /project

RUN adduser app
RUN cp -r /project/example_nginx/* /etc/nginx

RUN apt-get update
RUN apt-get install python3 python3-pip -y
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

RUN python -m pip install -r /project/requirements/development.txt
