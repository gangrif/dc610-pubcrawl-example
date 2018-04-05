FROM debian
#FROM resin/rpi-raspbian:wheezy

RUN apt-get -y update 
RUN apt-get -y update --fix-missing 
RUN apt-get -y install apache2 qrencode
RUN a2enmod cgi

EXPOSE 80
EXPOSE 443 

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
