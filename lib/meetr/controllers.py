#!/usr/bin/env python

import tornado.web
import logging
import json

from meetr.models import MetricsModel

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class DebugController(tornado.web.RequestHandler):
    def get(self):
        self.debug_request()

    def post(self):
        self.debug_request()

    def debug_request(self):
        
        str = "{0} {1} {2}".format(self.request.method, self.request.uri, self.request.arguments)

        log = logging.getLogger('tornado.access')
        log.debug(str)
        self.write(str)
        d = self.get_argument('boo', 'error')
        log.debug(d)


"""
REST API:

Create

POST /1.0/metrics

{metric=<metric name>&timestamp=<timestamp>&value=<value>}

Search

GET /1.0/metrics?metric=<metric>&from=<date>&to=<date>&aggregation=sum

Bulk Create

POST /1.0/metrics

{batch=true&metrics=<json>}

"""


class MetricsController(tornado.web.RequestHandler):
    """Controller for '/1.0/metrics'"""

    def post(self):
        """create a new metric"""
        
        log = logging.getLogger('tornado.access')
        log.debug("%s %s %s" ,self.request.method, self.request.uri, self.request.arguments)

        if 'batch' in self.request.arguments:
            metrics = json.loads(self.get_argument('metrics'))
            MetricsModel.batch_add(metrics)
        else:
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
        self.write(MetricsModel.search(query))
        self.set_status(200)
