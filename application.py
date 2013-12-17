#!/usr/bin/env python

import os
import sys
import tornado.ioloop
import tornado.web

sys.path.append(os.path.join(sys.path[0], "lib")) 

class Routes:
	"""
	Understands how to map URLS to Controllers and to Docs
	"""
	def initialize(self, routes):
		pass

	def add(self):
		pass

	def get(self):
		pass


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

"""
REST API:

Create

POST /1.0/metrics

{metric=<metric name>&timestamp=<timestamp>&value=<value>}

Search

GET /1.0/metrics?metric=<metric>&from=<date>&to=<date>&aggregation=sum
"""

application = tornado.web.Application([
    (r"/", MainHandler),
])


def main():
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()