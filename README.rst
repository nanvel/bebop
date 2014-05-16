Cowboy Bebop tv wiki
====================

Technology stack
----------------

    - `Tornado <http://www.tornadoweb.org/en/stable/>`__
    - `AWS DynamoDB <http://aws.amazon.com/documentation/dynamodb/>`__

Development
-----------

.. code-block:: bash

    cd bebop
    virtualenv .env --no-site-packages
    source .env/bin/activate
    pip install -r requirements/development.txt
    # download DynamoDB local http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Tools.DynamoDBLocal.html
    tar -xvf dynamodb_local_x.tar.gz
    make dynamo
    python app.py
