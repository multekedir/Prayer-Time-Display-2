#!/bin/bash

sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-virtualenv nginx gunicorn

sudo mkdir /home/www && cd /home/www

git clone https://github.com/multekedir/Prayer-Time-Display-2.git && cd Prayer-Time-Display-2
python3 -m pip install pipenv
python3 -m pipenv shell
pipenv install


sudo /etc/init.d/nginx start
sudo rm /etc/nginx/sites-enabled/default
sudo touch /etc/nginx/sites-available/Prayer-Time-Display-2
sudo ln -s /etc/nginx/sites-available/flask_project /etc/nginx/sites-enabled/Prayer-Time-Display-2

sudo echo "server {
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /static {
        alias  /home/www/Prayer-Time-Display-2/static/;
    }
}"  > /etc/nginx/sites-enabled/Prayer-Time-Display-2

sudo /etc/init.d/nginx restar

cd /home/www/Prayer-Time-Display-2/
gunicorn app:app -b localhost:5000

