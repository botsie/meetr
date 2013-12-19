#!/usr/bin/env python

import cql
from datetime import datetime
import pytz
import tornado.options
from tornado.options import options

tornado.options.define("cassandra_host", group='Cassandra', default='localhost')
tornado.options.define("cassandra_keyspace", group='Cassandra', default='meetr')
tornado.options.define("cassandra_port", group='Cassandra', default=9160)


# Why am I using all class methods here? Because I want to communicate that this
# object maintains no state

class MetricsModel(object):
    """Understands how metrics are represented in the db"""
    ISO_8601 = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def execute_cql(cls, cql_str):
        cluster = options.cassandra_host
        keyspace = options.cassandra_keyspace
        port = options.cassandra_port

        connection = cql.connect(cluster, port,  keyspace, cql_version='3.0.0')
        cursor = connection.cursor()
        cursor.execute(cql_str)
        
        rows = cursor.fetchall()
        cols = cursor.description

        result = list()
        for row in rows:
            result_row = dict()
            for i in range(len(cols)):
                result_row[cols[i][0]] = row[i]
            result.append(result_row)

        return result

    @classmethod
    def insert_statement(cls, data):
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
        return cql_template.format(metric,timestamp,value)



    @classmethod
    def add(cls, data):
        """ Class method to add a new metric """
        cls.execute_cql(cls.insert_statement(data))

    @classmethod
    def batch_add(cls, data):
        """Class method to add a batch of metrics"""
        statements = list()
        for row in data:
            statements.append(cls.insert_statement(row))

        cql_template = """
        BEGIN BATCH
            {0}
        APPLY BATCH;
        """
        cls.execute_cql(cql_template.format("\n".join(statements)))


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
        rows = cls.execute_cql(cql_str)

        print rows

        return { 
            'metric': rows[0]['metric'], 
            'from' : from_time,
            'to' : to_time,
            'aggregation' : aggregation,
            'value': getattr(cls,aggregation)(rows)['metric_value']
        }

    @classmethod
    def sum(cls, rows):
        f = lambda x,y : { 'metric' : x['metric'], 'metric_value': x['metric_value'] + y['metric_value']}
        return reduce(f , rows)












