#!/usr/bin/env python

import cql
from datetime import datetime
import pytz


# Why am I using all class methods here? Because I want to communicate that this
# object maintains no state

class MetricsModel(object):
    """Understands how metrics are represented in the db"""
    ISO_8601 = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def execute_cql(cls, cql_str):
        cluster = '127.0.0.1'
        keyspace = 'meetr'

        connection = cql.connect(cluster, 9160,  keyspace, cql_version='3.0.0')
        cursor = connection.cursor()
        cursor.execute(cql_str)
        return cursor


    @classmethod
    def add(cls, data):
        """ Class method to add a new metric """
        metric = data['metric']
        timestamp = data['timestamp']
        value = data['value']

        utc = pytz.utc
        timestamp = utc.localize(datetime.strptime(timestamp,MetricsModel.ISO_8601)).strftime(MetricsModel.ISO_8601)

        cql_template = """INSERT INTO metrics (
            metric, 
            collected_at,
            metric_value
            ) VALUES ('{0}', '{1}', {2});"""
        cql_str = cql_template.format(metric,timestamp,value)
        cls.execute_cql(cql_str)


    @classmethod
    def search(cls, query):
        """Class method to search for data"""

        metric = query['metric']
        to_time = query['to']
        from_time = query['from']
        aggregation = query['aggregation']

        # TODO: Validate inputs

        cql_template = """
            SELECT *
            FROM metrics
            WHERE metric = '{0}'
              AND collected_at >= '{1}'
              AND collected_at <= '{2}'
        """
        cql_str = cql_template.format(metric, from_time, to_time)
        cursor = cls.execute_cql(cql_str)

        rows = cursor.fetchall()

        return getattr(cls,aggregation)(rows)

    @classmethod
    def sum(rows):
        return reduce(lambda x,y : x + y['value'], rows)












