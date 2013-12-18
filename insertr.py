#!/usr/bin/env python

import cql
import random
from datetime import datetime
import pytz
import tornado.options 

cluster = '127.0.0.1'
keyspace = 'meetr'

con = cql.connect(cluster, 9160,  keyspace, cql_version='3.0.0')
print ("Connected!")
cursor = con.cursor()

instance_id = "hostname"
metric = "bytes_out"
value = random.randint(128,512)

utc = pytz.utc
time_stamp = utc.localize(datetime.utcnow()).strftime('%Y-%m-%d %H:%M:%S %z')

cql_template = """INSERT INTO metrics (
    instance_id, 
    metric, 
    collected_at,
    metric_value
    ) VALUES ('{0}', '{1}', '{2}', {3});"""
cql = cql_template.format(instance_id,metric,time_stamp,value)

print(cql)


cursor.execute(cql)