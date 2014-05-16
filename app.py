import sys

import tornado.options
import tornado.web

from bebop.handlers import IndexHandler


application = tornado.web.Application([
    (r'/', IndexHandler),
])


if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
