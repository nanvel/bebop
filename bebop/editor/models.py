import logging

from tornado import gen
from tornado_botocore import Botocore


logger = logging.getLogger(__name__)


class Episode(object):

    TABLE_NAME = 'bebop1'
    REGION = 'us-east-1'

    # The data type for the attribute. You can specify S for string data,
    # N for numeric data, or B for binary data.
    ATTRIBUTE_DEFINITIONS = [{
        'AttributeName': 'number',
        'AttributeType': 'N'
    }, {
        'AttributeName': 'title',
        'AttributeType': 'S'
    }, {
        'AttributeName': 'airdate',
        'AttributeType': 'N'
    }]

    # http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DataModel.html#DataModelPrimaryKey
    KEY_SCHEMA = [{
        'AttributeName': 'number',
        'KeyType': 'HASH'
    }, {
        'AttributeName': 'airdate',
        'KeyType': 'RANGE'
    }]

    # http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html

    LOCAL_SECONDARY_INDEXES = [{
        'IndexName': 'by_title',
        'KeySchema': [
            {
                'AttributeName': 'number',
                'KeyType': 'HASH'
            }, {
                'AttributeName': 'title',
                'KeyType': 'RANGE'
            }
        ],
        # http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html#LSI.Projections
        'Projection': {
            'NonKeyAttributes': [
                'description'
            ],
            'ProjectionType': 'INCLUDE'
        }
    }]

    # http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughputIntro.html
    PROVISIONED_THROUGHPUT = {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 2
    }

    def __init__(self):
        pass

    def dynamodb(self, operation):
        session = getattr(self, '_session', None)
        ddb = Botocore(
            service='dynamodb', operation=operation,
            region_name=self.REGION, session=session)
        self._session = ddb.session
        return ddb

    @property
    def table_kwargs(self):
        kwargs = {
            'table_name': self.TABLE_NAME,
            'attribute_definitions': self.ATTRIBUTE_DEFINITIONS,
            'key_schema': self.KEY_SCHEMA,
            'provisioned_throughput': self.PROVISIONED_THROUGHPUT,
        }
        if hasattr(self, 'LOCAL_SECONDARY_INDEXES'):
            kwargs['local_secondary_indexes'] = self.LOCAL_SECONDARY_INDEXES
        if hasattr(self, 'GLOBAL_SECONDARY_INDEXES'):
            kwargs['global_secondary_indexes'] = self.GLOBAL_SECONDARY_INDEXES
        return kwargs

    def create_table_if_not_exists(self):
        import botocore.session
        session = botocore.session.get_session()
        ddb = session.get_service('dynamodb')
        operation = ddb.get_operation('DescribeTable')
        endpoint = ddb.get_endpoint(self.REGION)
        res = operation.call(endpoint, table_name=self.TABLE_NAME)
        if res[1].get('Errors', [{}])[0].get('Code', '') == 'ResourceNotFoundException':
            logger.info('Creting {table_name} table ...'.format(table_name=self.TABLE_NAME))
            operation = ddb.get_operation('CreateTable')
            res = operation.call(endpoint, **self.table_kwargs)
            if res[0].status_code != 200:
                msg = '{table_name} table creation failed.'.format(table_name=self.TABLE_NAME)
                logger.error(msg)
                raise Exception(msg)

    def count(self):
        """Returns series count.
        """
        pass

    @gen.coroutine
    def get(self, number):
        ddb_get_item = self.dynamodb(operation='GetItem')
        # TODO: use global secondary index
        res = yield gen.Task(ddb_get_item.call,
            table_name=self.TABLE_NAME,
            key={'number': {'N': str(number)}, 'airadate': {'N': '123'}})
        raise gen.Return(res)

    def by_number(self, offset=0, limit=10):
        """Returns series sorted by number.
        """
        pass

    def by_title(self, offset=0, limit=10):
        """Returns series sorted by title.
        """
        pass

    def update(self, number, **kwargs):
        pass

    def create(self, number, **kwargs):
        pass
