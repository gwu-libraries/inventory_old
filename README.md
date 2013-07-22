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

2. Create a directory for your projects (replace &lt;INV_HOME&gt; with your desired directory path and name: for instance /inventory or /home/&lt;username&gt;/inventory)

        $ mkdir /<INV_HOME>
        $ cd /<INV_HOME>

3. Pull down the project from github

        (GW staff only)
        $ git clone git@github.com:gwu-libraries/inventory.git

        (everyone else)
        $ git clone https://github.com/gwu-libraries/inventory.git

4. Create virtual Python environment for the project

        $ cd /<INV_HOME>/inventory
        $ virtualenv --no-site-packages ENV

5. Activate your virtual environment

        $ source ENV/bin/activate

6. install django, tastypie, and other python dependencies

        (ENV)$ pip install -r requirements.txt


PART III - Configure your installation
--------------------------------------

0. Create a logs directory

        $ mkdir logs

1. Copy the local settings template to an active file

        $ cd inv/inv
        $ cp local_settings.py.template local_settings.py

2. Update the values in the local_setting.py file:  for the database,
NAME, USER, and PASSWORD to the database you created above, and set ENGINE
to 'postgresql_psycopg2'; also, set a SECRET_KEY. Enter appropriate values
for requester, minter, url and port under IDSERVICE and TEST_IDSERVICE.

        $ vim local_settings.py

3. Copy the WSGI file template to an active file

        $ cp wsgi.py.template wsgi.py

4. Update the wsgi.py file. (Change the value of ENV to your environment path)

        $ vim wsgi.py

5. Initialize database tables. WARNING: Be sure you are still using your
virtualenv. DO NOT create a superuser when prompted!

        (ENV)$ cd /<INV_HOME>/inv
        (ENV)$ python manage.py syncdb

    If you encounter an authentication error with postgresql edit your local_settings.py file and set HOST = 'localhost'

    If you encounter an error during the above command that ends with:

        TypeError: decode() argument 1 must be string, not None

    Then you need to add location values to your profile. Open your .bashrc file in an editor:

        $ vim ~/.bashrc

    Enter the following values at the end of the file and save.

        export LC_ALL=en_US.UTF-8
        export LANG=en_US.UTF-8

    Now, reload your bashrc changes

        source ~/.bashrc

    Now, rerun the syncdb command

        (ENV)$ python manage.py syncdb

6. Migrate the database to the latest updates

        $ python manage.py migrate

7. Create the database super user

        (ENV)$ python manage.py createsuperuser

    Enter your information when prompted

8. Copy the Apache virtual host file to the Apache2 directory

        $ cd /<INV_HOME>/inventory
        $ sudo cp apache/inventory /etc/apache2/sites-available/inventory

9. Update the values in the Apache virtual host file.

    Edit the host port number
    Edit your server name (base url)
    Edit the many instances of &lt;path to INV_HOME&gt;. Beware: the line for the WSGI Daemon has two references to that path.

        $ sudo vim /etc/apache2/sites-available/inventory

    To change all of the path values at once use the global replace command in vim

        :%s/old_value/new_value/g

10. Enable the new virtualhost. If you are using port 80 also disable the default host

        $ sudo a2ensite inventory
        $ sudo a2dissite default
        $ sudo /etc/init.d/apache2 restart

11. If you want to enable SSL follow these steps,
    
    Copy the Apache virtual host SSL file to the Apache2 directory
        
        $ cd /<INV_HOME>/inventory
        $ sudo cp apache/inventory-ssl /etc/apache2/sites-available/inventory-ssl

    Uncomment the following line in /etc/apache2/sites-available/inventory

        #Redirect permanent / https://inventory.example.com/

    See the [SSL documentation](https://github.com/gwu-libraries/SSL_HowTo) for detailed instructions.

    Enable the new virtualhost file

        $ sudo a2dissite inventory
        $ sudo a2ensite inventory
        $ sudo a2ensite inventory-ssl
        $ sudo /etc/init.d/apache2 restart

12. Test your installation by pasting your base url and port in your web browser

13. Log in to the admin module and change the website information by
entering your base url and port under the Sites section.


Usage Instructions
==================

Inventory makes use of the tastypie library for automatic creation of API urls. See the [documentation](http://django-tastypie.readthedocs.org/en/v0.9.12/interacting.html) for detailed instructions.

GET
---

To fetch data from the system via http, use a GET request with the following url pattern:

http://your.sites.base.url:port/api/version/model/id?format=json&username=username&api_key=api_key

The version by default is v1. The api_key for a user can be found in the admin interface, which can be found by appending /admin to your base url.

Here is an example url with the api key removed:

http://inventory.example.com/api/v1/item/38989/c01wdbsmv/?format=json&username=gomez&api_key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

POST
----

To create a new item, use the POST method with a url pointing to the model type and the item attributes in the body. Don't forget to add the format, username, and api key paramaters.

URL

http://inventory.example.com/api/v1/item/

Body Data

```json
{"collection": "38989/c010g26gs40w/", "id": "38989/c01wwwwww", "local_id": "39020025220180", "notes": "A test item", "original_item_type": "2", "project": "38989/c0102488q518", "title": "Our Test Item!"}
```

PUT
---

To edit the data of an existing item, use the PUT method. Point the url to the specific item and put **ALL** of the items attributes in the body data.

URL

http://inventory.example.com/api/v1/item/38989/c01wwwwww

Body Data

```json
{"collection": "38989/c010g26gs40w/", "id": "38989/c01wwwwww", "local_id": "39020025220180", "notes": "A test item", "original_item_type": "2", "project": "38989/c0102488q518", "title": "Our Test Item!"}
```

PATCH
-----

To edit just a few attributes for an item, use the PATCH method instead of PUT.

URL

http://inventory.example.com/api/v1/item/38989/c01wwwwww

Body Data

```json
{"title": "We Changed the Title"}
```

DELETE
------

To remove an item from the database, use the DELETE method with the url pointed at the specific item
