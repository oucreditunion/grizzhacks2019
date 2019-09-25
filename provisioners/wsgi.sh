#!/bin/bash

#install necessary packages to server PHP and Python from apache
sudo apt-get install -y apache2 libapache2-mod-wsgi libapache2-mod-php5 php5-curl

#add the configuration file to tell apache where to find our python code
sudo cp /vagrant/provisioners/wsgi.conf /etc/apache2/conf-enabled/

#restart apache so the new configuration takes effect
sudo /etc/init.d/apache2 restart

