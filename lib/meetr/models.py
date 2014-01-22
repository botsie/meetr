#!/usr/bin/env python

import cql
from datetime import datetime
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
        metric_id = data['metric_id']
        ts = data['ts']
        value = data['value']

        cql_template = """INSERT INTO metrics (
            metric_id, 
            ts,
            value
            ) VALUES ('{0}', '{1}', {2});"""
        return cql_template.format(metric_id,ts,value)



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
            WHERE metric_id = '{0}'
              AND ts >= '{1}'
              AND ts <= '{2}';
        """
        cql_str = cql_template.format(metric, from_time, to_time)
        rows = cls.execute_cql(cql_str)

        return { 
            'metric_id': rows[0]['metric_id'], 
            'from' : from_time,
            'to' : to_time,
            'aggregation' : aggregation,
            'value': getattr(cls,aggregation)(rows)['value']
        }

    @classmethod
    def sum(cls, rows):
        f = lambda x,y : { 'metric_id' : x['metric_id'], 'value': x['value'] + y['value']}
        return reduce(f , rows)












