"""
DB interaction abstraction
"""
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import STRING


class EpisodeModel(ConnectorMixin):

    FIELDS = ['title', 'content', 'last_editor']
    ID_KEY = 'title'
    TABLE = 'bebop-tv'

    def __init__(self, *args, **kwargs):
        for field in self.FIELDS:
            setattr(self, field, kwargs['field'])

    def save(self):
        table = Table(
            self.TABLE,
            schema=[HashKey('title', data_type=STRING)])
        item = table.get_item(
            **{self.ID_KEY: getattr(self, self.ID_KEY)})
        for field in self.FIELDS:
            val = getattr(self, field, None)
            if val:
                item[field] = val
        item.save()
