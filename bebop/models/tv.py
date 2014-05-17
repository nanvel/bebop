"""
DB interaction abstraction
"""
from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER


class EpisodeModel(object):

    FIELDS = ['number', 'title', 'content', 'airdate']
    ID_KEY = 'number'
    TABLE = 'bebop-tv'

    def __init__(self, *args, **kwargs):
        for field in self.FIELDS:
            setattr(self, field, kwargs.get(field))

    def get_table(self):
        if not getattr(self, 'table', None):
            conn = DynamoDBConnection(
                host='localhost', port=8010,
                aws_secret_access_key='anything',
                is_secure=False)
            self.table = Table(
                self.TABLE,
                schema=[HashKey('number', data_type=NUMBER)],
                connection=conn)
        return self.table

    def save(self):
        table = self.get_table()
        item = table.get_item(
            **{self.ID_KEY: getattr(self, self.ID_KEY)})
        for field in self.FIELDS:
            val = getattr(self, field, None)
            if val:
                item[field] = val
        item.save()
        return self

    def get(self, number):
        table = self.get_table()
        item = table.scan(number__eq=number).next()
        if not item:
            return None
        result = {}
        for field in self.FIELDS:
            result[field] = item.get(field, None)
        return result

    def all(self):
        table = self.get_table()
        results = []
        for item in table.scan():
            result = {}
            for field in self.FIELDS:
                result[field] = item.get(field, None)
            results.append(result)
        return results
