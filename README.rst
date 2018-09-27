=====
CLEO
=====
The codebase of CLEO

Prerequisites
=============

- Postgres, postgis.
- Python >=2.7, >=3.5
- Redis
- Elasticsearch 5.x


Installation
============

Additional Python 3.6 dependencies
----------------------------------
tkinter
~~~~~~~
On Python 3.6 you will need to install the ``python3.6-tk`` package for
``tkinter`` support.

.. code-block:: sh

    sudo apt-get install python3.6-tk

NodeJS
------

Install NodeJS:

.. code-block:: sh

    https://nodejs.org/en/download/

Then run:

.. code-block:: sh

    yarn install

Postgis
-------

.. code-block:: sh

    sudo apt-get install libgdal-dev

    sudo su -l postgres

    createdb -T template0 -E utf-8 -l en_US.UTF-8 -O postgres muses

    psql  -c 'create extension postgis;' -d muses

    ./manage.py migrate

Database engine shall be `django.contrib.gis.db.backends.postgis`.

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'muses',
            'USER': 'whoever',
            'PASSWORD': 'whatever',
        }
    }

Redis
-----
**Install**

.. code-block:: sh

    sudo apt install redis-server

**Allow connections**

- Edit the redis conf file ``sudo nano  /etc/redis/redis.conf`` file.
- Find line ``bind 127.0.0.1`` and change it to ``bind 0.0.0.0``
- Save the redis.conf file.

**Restart**

.. code-block:: sh

    sudo systemctl restart redis

or

.. code-block:: sh

    /etc/init.d/redis-server restart

**Test**

.. code-block:: sh

    redis-cli ping

The expected output is ``PONG``.

Elasticsearch
-------------
Either install it or run with Docker.

.. code-block:: sh

    docker pull docker.elastic.co/elasticsearch/elasticsearch:5.5.3
    docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:5.5.3

Data Sources
============

Importing data from known sources
---------------------------------

At the moment, data is imported from the following data sources:

- www.rmo.nl
- brooklynmuseum.org
- thewalters.org
- metmuseum.org

CSRF tokens
===========
To obtain a CSRF token make use of `/csrftoken/` endpoint.

**Sample request:**

.. code-block:: text

    POST http://localhost:8000/csrftoken/

**Or with cURL:**

.. code-block:: text

    curl -X POST -i http://localhost:8000/csrftoken/

**Sample response:**

.. code-block:: javascript

    {"token": "bsHtEMn9K8rqWSm1ql5hz5BcBNR3DuFJRgyc6VVE4c0Gh7PzjaEJap9FErsgxkBz"}

AI
==
The description of the Artificial Intelligence (AI) or algorithm that was
created for Cleo can be found at https://cleo.aincient.org/pages/en/open-source/

Elasticsearch indexes
=====================
Synonyms
--------
There are two lists of synonyms for Elasticsearch:

- English: `implementation/synonyms/raw/en.txt`
- Dutch: `implementation/synonyms/raw/nl.txt`

Both of them are not in format accepted by Elasticsearch. We need to do some
tiny transformation in order to make it acceptable.

Example of the English synonyms:

.. code-block:: text

    word_id;preferred_EN;variant1;variant2;variant3;variant4;variant5;variant6;variant7
    1;Anatolia;anatolia;anatolie;anatolien;;;;
    2;Assyria;assyria;assyrie;assyrien;;;;
    3;Babylonia;babylonia;babylonie;babylonien;;;;
    4;Byblos;;;;;;;
    5;Crocodilopolis;;;;;;;
    6;Greek-Roman;graeco-roman;greco-roman;;;;;
    7;Herodote;herodotos;;;;;;
    8;Horapollo;horapollon;;;;;;
    9;Isis-aphrodite;;;;;;;
    10;Manetho;manethon;manethos;;;;;
    11;Maya;;;;;;;
    12;Nefertiti;nefertete;nofretete;;;;;
    13;Oxyrhynchus;oxyrhynchos;behnasa;el-Bahnasa;bahnasa;;;
    14;pharaoh;pharao;;;;;;
    15;Plutarchus;plutarchos;;;;;;
    16;Punt;;;;;;;
    17;Rosetta;Rosette;el rashid;el-rashid;al-rashid;;;
    18;Saqqara;saqqarah;saqqareh;sakkarah;;;;
    19;Serapeum;serapaeum;serapeion;;;;;
    20;Sinuhe;sinouhe;;;;;;
    21;Taffeh;taffah;taffa;tafa;taphis;;;
    22;Thebes;;;;;;;
    23;Teye;tiy;tiye;;;;;
    24;Wenamun;wen-amon;wenamoen;;;;;

What is made of it:

.. code-block:: text

    anatolia, anatolia, anatolie, anatolien
    assyria, assyria, assyrie, assyrien
    babylonia, babylonia, babylonie, babylonien
    greek-roman, graeco-roman, greco-roman
    herodote, herodotos
    horapollo, horapollon
    manetho, manethon, manethos
    nefertiti, nefertete, nofretete
    oxyrhynchus, oxyrhynchos, behnasa, el-bahnasa, bahnasa
    pharaoh, pharao
    plutarchus, plutarchos
    rosetta, rosette, el rashid, el-rashid, al-rashid
    saqqara, saqqarah, saqqareh, sakkarah
    serapeum, serapaeum, serapeion
    sinuhe, sinouhe
    taffeh, taffah, taffa, tafa, taphis
    teye, tiy, tiye
    wenamun, wen-amon, wenamoen

In detail:

- All one-word lines are being removed
- All words are lower-cased.
- All empty elements are removed.
- First row is removed.
- First element of each row (number) is removed.

.. note::

    Do not commit synonyms files if anyhow the format has been changed (see
    the example of the synonyms file if anything (format, delimiter, etc)
    has been changed.

Geo-coordinates
---------------
If no geo-location could be discovered, the values for latitude and longitude
are set respectively to "-90.0" and "-180.0".

Authentication and registration
===============================
Logging in
----------
In order to log in, you should make a POST request with the following
information to the `/rest-auth/login/` endpoint.

**Sample request:**

.. code-block:: text

    POST http://localhost:8000/rest-auth/login/

.. code-block:: javascript

    {
        "usernname": "admin",
        "password": "test"
    }

**Or if we use cURL:**

.. code-block:: text

    curl -X POST -H 'Content-Type: application/json' -i http://localhost:8000/rest-auth/login/ --data '{
        "username": "admin",
        "email": "",
        "password": "test"
    }'

**Sample response:**

.. code-block:: text

    HTTP 200 OK
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept

.. code-block:: javascript

    {
        "key": "144bae5d5e3f00bef13c92a5d33a327d7bc37f0a"
    }

Logging out
-----------
It's as simple as sending a GET request to the `/rest-auth/logout/` endpoint.

**Sample request:**

.. code-block:: text

    GET http://localhost:8000/rest-auth/logout/

**Sample response:**

.. code-block:: javascript

    {"detail": "Successfully logged out."}

Authenticated user details
--------------------------
It's as simple as sending a GET request to the `/rest-auth/user/` endpoint.

**Sample request:**

.. code-block:: text

    GET http://localhost:8000/rest-auth/user/

**Sample response:**

.. code-block:: javascript

    {
        "pk": 3,
        "username": "admin",
        "email": "admin@localhost",
        "first_name": "Admin",
        "last_name": "Localhost",
        "account_settings": {
            "language": "nl"
        }
    }

Editing the profile
-------------------
It's a POST request to the `/rest-auth/user/` endpoint.

**Sample request:**

.. code-block:: text

    POST http://localhost:8000/rest-auth/user/

.. code-block:: javascript


    {
        "pk": 3,
        "username": "admin",
        "email": "admin2@localhost",
        "first_name": "Admin",
        "last_name": "Localhost",
        "account_settings": {
            "language": "en"
        }
    }

**Sample response:**

.. code-block:: text

    HTTP 200 OK
    Allow: GET, PUT, PATCH, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

.. code-block:: javascript

    {
        "pk": 3,
        "username": "admin",
        "email": "admin2@localhost",
        "first_name": "Admin",
        "last_name": "Localhost",
        "account_settings": {
            "language": "en"
        }
    }

Registration
------------
Post request to `/rest-auth/registration/`.

**Sample request:**

.. code-block:: text

    POST http://localhost:8000/rest-auth/registration/

.. code-block:: javascript

    {
        "username": "test4",
        "email": "test4@localhost",
        "password1": "test1234",
        "password2": "test1234"
    }

**Sample response:**

.. code-block:: text

    HTTP 201 Created
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept

.. code-block:: javascript

    {
        "key": "eb7698d526bfa06bbba59cf747ed1c23f78866cd"
    }



Password reset
--------------
For non-authenticated users who forgot their password.

Step 1: Request password reset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Post request to `/rest-auth/password/reset/`. If there's an account
registered with the given e-mail address, a password reset e-mail would be sent
to the latter for the confirmation.

**Sample request:**

.. code-block:: text

    POST http://localhost:8000/rest-auth/password/reset/

.. code-block:: javascript

    {
        "email": "test4@localhost"
    }

**Sample response:**

.. code-block:: text

    HTTP 200 OK
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept

.. code-block:: javascript

    {
        "detail": "Password reset e-mail has been sent."
    }

Step 2: Confirm password reset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sample e-mail contents:

.. code-block:: text

    http://localhost:8000/rest-auth/password/reset/confirm/?uidb64=xxx&token=4xr-xxx
    uidb64: xxx
    token: 4xr-xxx

Make a POST request to the endpoint specified
`/rest-auth/password/reset/confirm/` providing the following fields:

- `new_password1`: Your new password
- `new_password2`: Repeat your new password
- `uid`: The value of `uid64` you got in a confirmation e-mail.
- `token`: The value of `token` your got in a confirmation e-mail.

**Sample request**

.. code-block:: text

    POST http://localhost:8000/rest-auth/password/reset/confirm/?uidb64=xxx&token=4xr-xxxx

.. code-block:: javascript

    {
        "new_password1": "newpass",
        "new_password2": "newpass",
        "uid": "xxx",
        "token": "4xr-xxxxxx"
    }

**Sample response:**

.. code-block:: text

    HTTP 200 OK
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept

.. code-block:: javascript

    {
        "detail": "Password has been reset with the new password."
    }

Change current password
-----------------------
For authenticated users who desire to change their current password.

Make a POST request to the `/rest-auth/password/change/` endpoint.


**Sample request**

.. code-block:: text

    POST http://localhost:8000/rest-auth/password/change/

.. code-block:: javascript

    {
        "new_password1": "newpass2",
        "new_password2": "newpass2"
    }

**Sample response:**

.. code-block:: text

    HTTP 200 OK
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept

.. code-block:: javascript

    {
        "detail": "New password has been saved."
    }

Favourites
==========
Manage
------
Add
~~~
**Sample request**

.. code-block:: text

    POST http://localhost:8000/account/usercollectionitemfavourites/

.. code-block:: javascript

    {
        "collection_item": 36522
    }

**Sample response**

.. code-block:: text

    HTTP 201 Created
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Location: http://localhost:8000/account/usercollectionitemfavourites/10/
    Vary: Accept

.. code-block:: javascript

    {
        "url": "http://localhost:8000/account/usercollectionitemfavourites/10/",
        "id": 10,
        "user": 3,
        "collection_item": 36522
    }

**Exceptions**

If you try to add the same item to favourites more than once, you will
get the following response:

.. code-block:: text

    HTTP 400 Bad Request
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

.. code-block:: javascript

    {
        "detail": "You have already added that item as a favourite."
    }

Remove
------
To remove item from favourite, send a DELETE request to the item detail
endpoint `/account/usercollectionitemfavourites/{item-id}/`:

**Sample request**

.. code-block:: text

    DELETE http://localhost:8000/account/usercollectionitemfavourites/1/

**Sample response**

.. code-block:: text

    HTTP 204 No Content
    Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

List
----
Get `/account/usercollectionitemfavourites/show_indexes/`.

**Sample request**

.. code-block:: text

    GET http://localhost:8000/account/usercollectionitemfavourites/show_indexes/

Export
------
CSV
~~~
To export all favourites into CSV format, the
`/account/usercollectionitemfavourites/show_indexes/` endpoint is used.

**Sample request**

.. code-block:: text

    GET http://localhost:8000/account/usercollectionitemfavourites/export_all/

Excel
~~~~~
To export all favourites into excel format, the
`/account/usercollectionitemfavourites/show_indexes/` endpoint is used.

**Sample request**

.. code-block:: text

    GET http://localhost:8000/account/usercollectionitemfavourites/export_all/?docformat=xlsx

Download single item
--------------------
CSV
~~~
Endpoint: `/api/collectionitem/{object-id}/download/`

**Sample request**

    http://localhost:3000/api/collectionitem/36534/download/

Excel
~~~~~
Endpoint: `/api/collectionitem/{object-id}/download/`

**Sample request**

    http://localhost:3000/api/collectionitem/36534/download/?docformat=xlsx

Find similar items
------------------
By image upload
~~~~~~~~~~~~~~~
Step 1. Uploading an image
^^^^^^^^^^^^^^^^^^^^^^^^^^
We have a endpoint for user uploaded user images, which are used to find
similar items.

**Sample request**

.. code-block:: text

    POST http://localhost:8000/account/usersearchimages/

.. code-block:: javascript

    {
        "image": "base64:sdhfdsfjdskljfds"
    }

**Sample response**

.. code-block:: text

    HTTP 201 Created
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Location: http://localhost:8000/account/usersearchimages/2/
    Vary: Accept

.. code-block:: javascript

    {
        "url": "http://localhost:8000/account/usersearchimages/2/",
        "id": 2,
        "user": 3,
        "image": "http://localhost:8000/media/image1.jpg",
        "created": "2018-06-20",
        "updated": "2018-06-20"
    }

Frontend
========

DEV
---

To run the frontend use the following code

.. code-block:: sh

    yarn start

Go to http://localhost:3000/search/

Production
-------------

To build the production version run the following command

.. code-block:: sh

    yarn build

Testing
=======

Project is covered with tests.

.. code-block:: sh

    ./runtests.py

It's assumed that you have all the requirements installed. If not, first
install the test requirements:

.. code-block:: sh

    pip install -r implementation/requirements/test.txt

Writing documentation
=====================

Keep the following hierarchy.

.. code-block:: text

    =====
    title
    =====

    header
    ======

    sub-header
    ----------

    sub-sub-header
    ~~~~~~~~~~~~~~

    sub-sub-sub-header
    ^^^^^^^^^^^^^^^^^^

    sub-sub-sub-sub-header
    ++++++++++++++++++++++

    sub-sub-sub-sub-sub-header
    **************************

License
=======
Apache 2.0.

Authors
=======
In alphabetical order (first name, last name, email).

- Artur Barseghyan <artur.barseghyan@gmail.com>
- Erick Martijn Bouma <bouma@gw20e.com>
- Haike Zegwaard <zegwaard@gw20e.com>
- Jasper Krebbers <krebbers@gw20e.com>
- Lukas Chripko <chripko@gw20e.com>
- Thomas Derksen <derksen@gw20e.com>
- Hans van den Berg <wepouaout64@gmail.com>
