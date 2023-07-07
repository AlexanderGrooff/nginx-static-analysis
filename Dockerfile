FROM nginx:1.25.1

COPY . /project
WORKDIR /project

RUN adduser app

RUN apt-get update
RUN apt-get install python3 python3-pip python3-venv -y

# Pip errors when breaking system env if we don't use venv
ENV VIRTUAL_ENV=/venv
RUN /usr/bin/python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python -m pip install -r /project/requirements/development.txt
