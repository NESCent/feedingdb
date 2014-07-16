#!/bin/bash

# post-puppet.sh: Add your shell commands here.

yum groupinstall "Development Tools"
yum install -y python-pip make gcc python-devel postgresql-devel postgresql-server
service postgresql initdb
service postgresql start

easy_install virtualenv
sudo -u vagrant virtualenv ~vagrant/venv
source ~vagrant/venv/bin/activate
pip install -r /server/src/feedb/dependencies.pip
