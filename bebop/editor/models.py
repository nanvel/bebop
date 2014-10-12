import logging

from tornado import gen

from ..common.dynamo import DDBBase


logger = logging.getLogger(__name__)


class DDBEpisode(DDBBase):

    TABLE_NAME = 'bebop'

    # The data type for the attribute. You can specify S for string data,
    # N for numeric data, or B for binary data.
    ATTRIBUTE_DEFINITIONS = [{
        'AttributeName': 'number',
        'AttributeType': 'N'
    }, {
        'AttributeName': 'title',
        'AttributeType': 'S'
    }]

    # http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DataModel.html#DataModelPrimaryKey
    KEY_SCHEMA = [{
        'AttributeName': 'number',
        'KeyType': 'HASH'
    }]

    # http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html

    LOCAL_SECONDARY_INDEXES = []

    GLOBAL_SECONDARY_INDEXES = [{
        'IndexName': 'by_title',
        'KeySchema': [
            {
                'AttributeName': 'title',
                'KeyType': 'HASH'
            }
        ],
        # http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html#LSI.Projections
        'Projection': {
            'ProjectionType': 'ALL',
        },
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 2,
            'WriteCapacityUnits': 2,
        }
    }]

    # http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughputIntro.html
    PROVISIONED_THROUGHPUT = {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 2
    }

    ATTRIBUTES = {
        'number': 'N',
        'title': 'S',
        'airdate': 'N', # timestamp
        'content': 'S',
    }

    @gen.coroutine
    def get(self, number):
        # http://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html
        ddb_get_item = self.dynamodb(operation='GetItem')
        res = yield gen.Task(ddb_get_item.call,
            table_name=self.TABLE_NAME,
            key=self.with_types({'number': number}))
        raise gen.Return(res)

    @gen.coroutine
    def create(self, **kwargs):
        item = {}
        ddb_put_item = self.dynamodb(operation='PutItem')
        res = yield gen.Task(ddb_put_item.call,
            table_name=self.TABLE_NAME,
            item=self.with_types(kwargs))
        raise gen.Return(res)

    @gen.coroutine
    def delete(self, number):
        ddb_delete_item = self.dynamodb(operation='DeleteItem')
        res = yield gen.Task(ddb_delete_item.call,
            table_name=self.TABLE_NAME,
            key=self.with_types({'number': number}))
        raise gen.Return(res)

    @gen.coroutine
    def items(self, limit=10, last=None):
        ddb_scan = self.dynamodb(operation='Scan')
        kwargs = {
            'table_name': self.TABLE_NAME,
            'limit': int(limit),
        }
        if last:
            kwargs['exclusive_start_key'] = self.with_types({'number': last})
        res = yield gen.Task(ddb_scan.call, **kwargs)
        raise gen.Return(res)

    @gen.coroutine
    def search(self, q, limit=10, last=None):
        ddb_query = self.dynamodb(operation='Query')
        kwargs = {
            'table_name': self.TABLE_NAME,
            'limit': int(limit),
            'index_name': 'by_title',
            'key_conditions': {
                'title': {
                    'AttributeValueList': [{'S': q}],
                    'ComparisonOperator': 'EQ'
                }
            }
        }
        if last:
            kwargs['exclusive_start_key'] = self.with_types({'number': last})
        res = yield gen.Task(ddb_query.call, **kwargs)
        raise gen.Return(res)
