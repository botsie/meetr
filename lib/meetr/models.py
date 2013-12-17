#!/usr/bin/env python

import cql
from datetime import datetime
import pytz


class MetricsModel(object):
	"""Understands how metrics are represented in the db"""
	ISO_8601 = '%Y-%m-%d %H:%M:%S'

	@staticmethod
	def add(data):
		""" Class method to add a new metric """
		cluster = '127.0.0.1'
		keyspace = 'meetr'

		metric = data['metric']
		timestamp = data['timestamp']
		value = data['value']

		utc = pytz.utc
		timestamp = utc.localize(datetime.strptime(timestamp,MetricsModel.ISO_8601)).strftime(MetricsModel.ISO_8601)


		con = cql.connect(cluster, 9160,  keyspace, cql_version='3.0.0')
		cursor = con.cursor()

		cql_template = """INSERT INTO metrics (
		    metric, 
		    collected_at,
		    metric_value
		    ) VALUES ('{0}', '{1}', {2});"""
		cql_str = cql_template.format(metric,timestamp,value)

		cursor.execute(cql_str)