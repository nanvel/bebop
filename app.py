from bebop.common.utils import rel
from bebop.editor.handlers import IndexHandler, EpisodesHandler, EpisodeHandler
from bebop.editor.models import Episode
from os import environ
from tornado import web, options, ioloop


ENV = environ.get('BEBOP_ENV', 'dev')


class BebopApplication(web.Application):

    def __init__(self, **kwargs):
        Episode().create_table_if_not_exists()
        kwargs['handlers'] = [
            web.url(r'/', IndexHandler, name='index'),
            web.url(r'/episodes', EpisodesHandler, name='episodes'),
            web.url(r'/episode/(?P<number>\d{1,3})', EpisodeHandler, name='episode'),
        ]
        kwargs['debug'] = True
        kwargs['template_path'] = rel('templates')
        kwargs['static_path'] = rel('static')
        super(BebopApplication, self).__init__(**kwargs)


if __name__ == '__main__':
    options.parse_command_line()
    # see bebop/common/__init__.py
    options.parse_config_file(rel('config/{env}.cfg'.format(env=ENV)))
    application = BebopApplication()
    application.listen(options.options.port)
    ioloop.IOLoop.instance().start()
