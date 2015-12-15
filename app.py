from os import environ

from tornado import web, options, ioloop

from bebop.common.utils import rel
from bebop.editor.handlers import IndexHandler, EpisodesHandler, EpisodeHandler, SearchHandler
from bebop.editor.models import DDBEpisode


ENV = environ.get('BEBOP_ENV', 'dev')


class BebopApplication(web.Application):

    def __init__(self, **kwargs):
        DDBEpisode().create_table_if_not_exists()
        kwargs['handlers'] = [
            web.url(r'/', IndexHandler, name='index'),
            web.url(r'/episodes', EpisodesHandler, name='episodes'),
            web.url(r'/episode/(?P<number>\d{1,3})', EpisodeHandler, name='episode'),
            web.url(r'/search', SearchHandler, name='search'),
        ]
        kwargs['debug'] = True
        super(BebopApplication, self).__init__(**kwargs)


if __name__ == '__main__':
    options.parse_command_line()
    # see bebop/common/__init__.py
    options.parse_config_file(rel('config/{env}.cfg'.format(env=ENV)))
    application = BebopApplication()
    application.listen(options.options.port)
    ioloop.IOLoop.instance().start()
