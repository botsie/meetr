#!/usr/bin/env python

import tornado.web

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


class MetricsController(tornado.web.RequestHandler):
	"""Controller for '/1.0/metrics'"""

	def post(self):
		"""create a new metric"""
		self.write("Post!")

	def get(self):
		"""search for metrics"""
		self.write("Get!")