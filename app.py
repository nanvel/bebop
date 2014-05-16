import sys

import tornado.options
import tornado.web

from bebop.utils import rel
from bebop.handlers import IndexHandler


SETTINGS = {
    'handlers': [(r'/', IndexHandler),],
    'template_path': rel('templates'),
    'static_path': rel('static'),
    'debug': True,
}


if __name__ == '__main__':
    tornado.options.parse_command_line()
    application = tornado.web.Application(**SETTINGS)
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
