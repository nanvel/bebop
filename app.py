import sys
import logging

import tornado.options
import tornado.web

from boto.dynamodb2.layer1 import DynamoDBConnection

from bebop.utils import rel
from bebop.handlers import IndexHandler


logger = logging.getLogger(__name__)


SETTINGS = {
    'handlers': [(r'/', IndexHandler),],
    'template_path': rel('templates'),
    'static_path': rel('static'),
    'debug': True,
}


def init_db():
    """
    1. Create connection
    2. Create table (if not exists) and load inital data
    """
    from boto.dynamodb2.table import Table
    conn = DynamoDBConnection(
        host='localhost', port=8010,
        aws_secret_access_key='anything',
        is_secure=False)

    TABLE_NAME = 'bebop-tv'

    if TABLE_NAME not in conn.list_tables()['TableNames']:
        logger.info('Creating bebop-tv table ...')
        from boto.dynamodb2.fields import HashKey, KeysOnlyIndex
        from boto.dynamodb2.table import Table
        from boto.dynamodb2.types import NUMBER
        from initial_data import TVS
        table = Table.create(TABLE_NAME, schema=[
            HashKey('number', data_type=NUMBER),
        ], throughput={
            'read': 5,
            'write': 15,
        }, connection=conn)
        for episode in TVS:
            table.put_item(data=episode)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    init_db()
    application = tornado.web.Application(**SETTINGS)
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
