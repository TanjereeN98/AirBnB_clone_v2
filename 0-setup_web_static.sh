#!/usr/bin/env bash
# Test script
sudo apt-get -y update;
sudo apt-get -y install nginx;
sudo ufw allow 'Nginx HTTP';
sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/;
sudo sh -c 'echo "Hello World" > /data/web_static/releases/test/index.html';
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current;
sudo chown -R ubuntu:ubuntu /data/
sudo sh -c 'cat > /etc/nginx/sites-available/default' <<EOF
server {
    listen 80;
    add_header X_Served_by \$HOSTNAME;
    listen [::]:80 default_server;
    server_name tuttrue.tech;
    location /hbnb_static {
        alias /data/web_static/current/;
    }
}
EOF
sudo service nginx restart;
