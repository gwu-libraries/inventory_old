inventory
=========

A system for tracking location of digital items and progress in reformatting projects

Installation Instructions
=========================

PART I - Basic server requirements
----------------------------------

1. Install Apache and other dependencies

        $ sudo apt-get install apache2 libapache2-mod-wsgi libaio-dev python-dev python-profiler

2. Install Postgresql

        $ sudo apt-get install postgresql postgresql-contrib libpq-dev

3. Set up Postgresql

        $ sudo -u postgres psql postgres

    Follow instructions to create password for postgres superuser

    Create a user for django

        $ sudo -u postgres createuser --createdb --no-superuser --no-createrole --pwprompt django

    Create a database for the inventory application

        $ sudo -u postgres createdb -O django inventory

4. Install Git

        $ sudo apt-get install git-core

PART II - Set up project environment
------------------------------------

1. Install virtualenv

        $ sudo apt-get install python-setuptools
        $ sudo easy_install virtualenv

2. Create a directory for your projects (replace &lt;INV_HOME$gt; with your desired directory path and name: for instance /inventory or /home/&lt;username&gt;/inventory)

        $ mkdir /<INV_HOME>
        $ cd /<INV_HOME>

3. Pull down the project from github

        $ git clone git@github.com:gwu-libraries/launchpad.git

4. Create virtual Python environment for the project

        $ cd /<INV_HOME>/inventory
        $ virtualenv --no-site-packages ENV

5. Activate your virtual environment

        $ source ENV/bin/activate

6. install django, tastypie, and other python dependencies

        (ENV)$ pip install -r requirements.txt

PART III - Configure your installation
--------------------------------------

1. Copy local settings template to active file

        $ cd /inv/inv
        $ cp local_settings.py.template local_settings.py

2. Update the values in the local_setting.py file. (Add name, user, and password to the default database, and change the engine to 'postgresql_psycopg2'.

        $ vim local_settings.py

3. Initialize database tables. (Be sure you are still using your virtualenv)

        (ENV)$ cd /<INV_HOME>/inv
        (ENV)$ python manage.py syncdb

4. Copy the Apache virtual host file to the Apache2 directory

        $ cd /<INV_HOME>/inventory
        $ sudo cp apache/inventory /etc/apache2/sites-available/inventory

5. Update the values in the Apache virtual host file.

    Edit the host port number
    Edit your server name (base url)
    Edit the many instances of &lt;path to INV_HOME&gt;. Beware: the line for the WSGI Daemon has to references to that path.

        $ sudo vim /etc/apache2/sites-available/inv

    To change all of the path values at once use the global replace command in vim

        :%s/old_value/new_value/g

6. Enable the new virtualhost

        $ sudo a2ensite inventory
        $ sudo /etc/init.d/apache2 restart

7. Test your installation by pasting your base url and port in your web browser
