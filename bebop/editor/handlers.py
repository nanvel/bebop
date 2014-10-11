import json

from tornado.web import RequestHandler
from tornado import gen

from .models import Episode


class IndexHandler(RequestHandler):

    def get(self):
        self.write('It works.')


class EpisodesHandler(RequestHandler):

    def get(self):
        self.write(json.dumps({'series': 1}))


class EpisodeHandler(RequestHandler):

    @gen.coroutine
    def get(self, number):
        episode = Episode()
        e = yield episode.get(number=number)
        self.write(str(e))

    def put(self, number):
        # returns 201 if created or 200 if modified
        self.write('create episode')

    def delete(self, number):
        self.write('delete episode')
