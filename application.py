#!/usr/bin/env python

import os
import sys
import tornado.ioloop
import tornado.web
import tornado.options

sys.path.append(os.path.join(sys.path[0], "lib")) 

from meetr.controllers import MetricsController, MainHandler, DebugController

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/dbg", DebugController),
    (r"/1.0/metrics", MetricsController)
], debug=True)


def main():
    tornado.options.parse_command_line()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()