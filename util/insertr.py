#!/usr/bin/env python

import cql
import random
from datetime import datetime
import pytz
from tornado.options import define, options, parse_command_line
import time
import sys

define("count", default=10, help="Number of metrics to insert")
parse_command_line()

cluster = '127.0.0.1'
port = 9160
keyspace = 'meetr'

con = cql.connect(cluster, port,  keyspace, cql_version='3.0.0')
cursor = con.cursor()


cql_template = """INSERT INTO metrics (
    metric, 
    collected_at,
    metric_value
    ) VALUES (:metric_, :collected_at_, :metric_value_);"""

instance_id = "hostname"
metric = "hostname.bytes_out"

utc = pytz.utc
for c in range(options.count):
    value = random.randint(128,512)
    time_stamp = utc.localize(datetime.utcnow()).strftime('%Y-%m-%d %H:%M:%S %z')
    cursor.execute(cql_template, dict(metric_=metric, collected_at_=time_stamp, metric_value_=value))
    sys.stdout.write('.')
    sys.stdout.flush()
    time.sleep(1)

print ""