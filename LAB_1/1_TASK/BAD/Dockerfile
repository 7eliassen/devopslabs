FROM ubuntu:latest 

RUN apt-get update 
RUN apt-get install nginx vim curl wget net-tools telnet openssh-server -y

ENV ADMIN_PASSWORD=12345

COPY . /var/www/html/

EXPOSE 80 22

CMD ["nginx", "-g", "daemon off;"]