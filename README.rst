Cowboy Bebop tv wiki
====================

The application allows to add/edit/remove Cowboy Bebop tv serios information. It uses Amazon DynamoDB storage and works with it asynchronously.

**UPD 2015-06-25**

ATTN: The example contains bad practices. See my `DynamoDB in examples <http://nanvel.name/label/dynamodb>`__ tutorial instead.

Usage
-----

.. code-block:: bash

    git clone https://github.com/nanvel/bebop
    cd bebop/bin
    # http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Tools.DynamoDBLocal.html
    wget http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest
    tar -xvf dynamodb_local_latest
    rm dynamodb_local_latest
    cd ..
    make dynamo
    python app.py
    python example.py


Resources used
--------------

    - `animenewsnetwork.com <http://www.animenewsnetwork.com/encyclopedia/anime.php?id=13>`__
