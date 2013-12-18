#!/usr/bin/env python

import tornado.web
import logging
from meetr.models import MetricsModel

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
        
        log = logging.getLogger('tornado.access')
        log.debug("%s %s %s" ,self.request.method, self.request.uri, self.request.arguments)

        data = dict()
        for arg in ['metric', 'timestamp', 'value']:
            data[arg] = self.get_argument(arg)

        # TODO: Return appropriate error codes on failure
        MetricsModel.add(data)
        self.set_status(200)

    def get(self):
        """search for metrics"""
        log = logging.getLogger('tornado.access')
        log.debug("%s %s %s" ,self.request.method, self.request.uri, self.request.arguments)

        query = dict()
        for arg in ['metric', 'to', 'from', 'aggregation']:
            query[arg] = self.get_argument(arg)

        # TODO: Return appropriate error codes on failure
        MetricsModel.search(query)
        self.set_status(200)
