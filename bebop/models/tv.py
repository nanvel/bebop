"""
DB interaction abstraction
"""
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER


class EpisodeModel(ConnectorMixin):

    FIELDS = ['number', 'title', 'content', 'airdate']
    ID_KEY = 'number'
    TABLE = 'bebop-tv'

    def __init__(self, *args, **kwargs):
        self.table = Table(
            self.TABLE,
            schema=[HashKey('number', data_type=NUMBER)])
        for field in self.FIELDS:
            setattr(self, field, kwargs.get(field))

    def save(self):
        item = self.table.get_item(
            **{self.ID_KEY: getattr(self, self.ID_KEY)})
        for field in self.FIELDS:
            val = getattr(self, field, None)
            if val:
                item[field] = val
        item.save()
        return self

    def get(self, number):
        pass

    def all():
        pass