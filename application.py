#!/usr/bin/env python

import os
import sys
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import options

sys.path.append(os.path.join(sys.path[0], "lib")) 

from meetr.controllers import MetricsController, MainHandler, DebugController

tornado.options.define("environment", group='Application', default='development')
tornado.options.define("port", group='Application', default=8888)
tornado.options.define("debug", group='Application', default=False)


class MeetrApplication(object):
    """docstring for MeetrApplication"""

    CONFIG_PATH=os.path.join(sys.path[0], "config",)

    def __init__(self):
        self.load_config()

    def load_config(self):
        tornado.options.parse_command_line()

        config_file_name = os.path.join(self.CONFIG_PATH, 
            options.environment + ".conf")

        if os.path.exists(config_file_name) and os.access(config_file_name, os.R_OK):
            tornado.options.parse_config_file(config_file_name)

        # reparse command line to allow options configured in the
        # config file to be overridden at the command line.
        tornado.options.parse_command_line()


    def run(self):
        application = tornado.web.Application([
            (r"/", MainHandler),
            (r"/dbg", DebugController),
            (r"/1.0/metrics", MetricsController)
        ], debug=options.debug)

        application.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    app = MeetrApplication() 
    app.run()