inventory
=========

A system for tracking location of digital items and progress in reformatting projects

Installation Instructions
=========================

PART I - Basic server requirements
----------------------------------

1. Install Apache and other dependencies

    sudo apt-get install apache2 libapache2-mod-wsgi libaio-dev python-dev python-profiler

2. Install Postgresql

    sudo apt-get install postgresql postgresql-contrib libpq-dev

3. Set up Postgresql

    sudo -u postgres psql postgres

Follow instructions to create password for postgres superuser

Create a user for django

    sudo -u postgres createuser --createdb --no-superuser --no-createrole --pwprompt django

#TODO: change this to Apache user???

Create a database for the inventory application

    sudo -u postgres createdb -O django inventory

4. Install Git

    sudo apt-get install git-core

PART II - Set up project environment
------------------------------------

1. Install virtualenv

    sudo apt-get install python-setuptools
    sudo easy_install virtualenv

2. Create directory for your projects (replace LPHOME with your root dir)

    mkdir /LPHOME
    cd /LPHOME

3. Pull down the project from github

    git clone git@github.com:gwu-libraries/launchpad.git

4. Create virtual Python environment for the project

    cd /LPHOME/launchpad
    virtualenv --no-site-packages ENV

5. Activate your virtual environment

    source ENV/bin/activate

6. install django, cx_Oracle, and other python dependencies

    pip install -r requirements.txt

PART III - Configure your installation
--------------------------------------

#TODO
