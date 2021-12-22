FROM nginx

COPY . /project

RUN adduser app
RUN cp -r /project/example_nginx/* /etc/nginx
