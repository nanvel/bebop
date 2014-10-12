import json

from tornado.web import RequestHandler
from tornado import gen

from .models import DDBEpisode


class IndexHandler(RequestHandler):

    def get(self):
        self.write('It works.')


class EpisodesHandler(RequestHandler):

    @gen.coroutine
    def get(self):
        limit = self.get_argument('limit', 10)
        last = self.get_argument('last', None)
        episode = DDBEpisode()
        e = yield episode.items(limit=limit, last=last)
        self.write(json.dumps(e))


class EpisodeHandler(RequestHandler):

    @gen.coroutine
    def get(self, number):
        episode = DDBEpisode()
        e = yield episode.get(number=number)
        self.write(json.dumps(e))

    @gen.coroutine
    def put(self, number):
        # returns 201 if created or 200 if modified
        data = json.loads(self.request.body)
        data['number'] = number
        episode = DDBEpisode()
        e = yield episode.create(**data)
        self.write(json.dumps(e))

    @gen.coroutine
    def delete(self, number):
        episode = DDBEpisode()
        e = yield episode.delete(number=number)
        self.write(json.dumps(e))


class SearchHandler(RequestHandler):

    @gen.coroutine
    def get(self):
        limit = self.get_argument('limit', 10)
        last = self.get_argument('last', None)
        q = self.get_argument('q')
        episode = DDBEpisode()
        e = yield episode.search(limit=limit, last=last, q=q)
        self.write(json.dumps(e))
