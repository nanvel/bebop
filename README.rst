Cowboy Bebop tv wiki
====================

Technology stack
----------------

    - `Tornado <http://www.tornadoweb.org/en/stable/>`__
    - `AWS DynamoDB <http://aws.amazon.com/documentation/dynamodb/>`__
    - `AngularJS <https://angularjs.org/>`__
    - `HTML5 WebSocket <http://en.wikipedia.org/wiki/WebSocket>`__

Development
-----------

.. code-block:: bash

    cd bebop
    virtualenv .env --no-site-packages
    source .env/bin/activate
    pip install -r requirements/development.txt
    # download DynamoDB local http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Tools.DynamoDBLocal.html
    tar -xvf dynamodb_local_x.tar.gz
    vim ~/.boto
    # add:
    # [Credentials]
    # aws_access_key_id = keyid
    # aws_secret_access_key = accesskey
    make dynamo
    python app.py

Resources used
--------------

    - `animenewsnetwork.com <http://www.animenewsnetwork.com/encyclopedia/anime.php?id=13>`__
    - `List of Cowboy Bebop episodes <http://en.wikipedia.org/wiki/List_of_Cowboy_Bebop_episodes>`__
    - `An Introduction to boto’s DynamoDB v2 interface <http://boto.readthedocs.org/en/latest/dynamodb2_tut.html>`__
    - `
Marrying Boto to Tornado: Greenlets bring them together <http://blog.joshhaas.com/2011/06/marrying-boto-to-tornado-greenlets-bring-them-together/>`__
    - `Greenlet-Tornado <https://github.com/mopub/greenlet-tornado>`__