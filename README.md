# Meetr

Cassandra Backed Metrics Storage System.

This is a HTTP interface for sending data to Cassandra. The application uses tornado (asynchronous networking library) for creating the API.

## Prerequisites

Create the Cassandra schema:

    CREATE KEYSPACE stats WITH replication = {
      'class': 'SimpleStrategy',
      'replication_factor': '3'
    };

    USE stats;

    CREATE TABLE metrics (
      metric_id text,
      ts timestamp,
      value float,
      PRIMARY KEY (metric_id, ts)
    ) WITH
      bloom_filter_fp_chance=0.010000 AND
      caching='KEYS_ONLY' AND
      comment='' AND
      dclocal_read_repair_chance=0.000000 AND
      gc_grace_seconds=864000 AND
      index_interval=128 AND
      read_repair_chance=0.100000 AND
      replicate_on_write='true' AND
      populate_io_cache_on_flush='false' AND
      default_time_to_live=0 AND
      speculative_retry='99.0PERCENTILE' AND
      memtable_flush_period_in_ms=0 AND
      compaction={'class': 'SizeTieredCompactionStrategy'} AND
      compression={'sstable_compression': 'LZ4Compressor'};

This script is db/meetr.cql.002

## Deployment

The application is deployed via fabric at the moment. `fabfile.py` in the root directory can be seen for more info.
The app is deployed at location `/srv/meetr`. At the moment, files in `util` directory need to be moved manually.

## Architecture

`application.py` is the actual application which is a web-server using tornado. To scale, multiple instances of `application.py` can be run behind a HAproxy or independantly.

`start_meetr` script can be executed to start multiple instances of `application.py` and this part is simplified by init script `meetr` and it's config file `/etc/sysconfig/meetr`.


## The API Documentation

Tests under `tests/functional_tests.py` can be seen to know more about the API.

Assuming:

        meetr_url = "http://localhost:8888/1.0/metrics"

### Single insert.

        test_data = {
            'metric_id' : 'test-metric',
            'ts' : "2003-12-18 12:18:18+0530",
            'value' : 1
        }

        data = urllib.urlencode(test_data)
        res = urllib2.urlopen(self.meetr_url, data)

### Bulk Insert

        test_data = [
            {
                'metric_id' : 'test-metric',
                'ts' : "2003-12-18 12:18:18+0530",
                'value' : 1
            },
            {
                'metric_id' : 'test-metric',
                'ts' : "2003-12-18 12:18:19+0530",
                'value' : 1
            },
            {
                'metric_id' : 'test-metric',
                'ts' : "2003-12-18 12:18:20+0530",
                'value' : 1
            },
            {
                'metric_id' : 'test-metric',
                'ts' : "2003-12-18 12:18:21+0530",
                'value' : 1
            }
        ]

        metrics = json.dumps(test_data)
        data = urllib.urlencode((('batch','True'),('metrics', metrics)))

        res = urllib2.urlopen(self.meetr_url, data)

### Searching

        data = urllib.urlencode((
            ('metric', 'test-metric'),
            ('from', "2003-12-18 12:18:18+0530"),
            ('to', "2003-12-18 12:18:21+0530"),
            ('aggregation', 'sum')
            ))

        res = urllib2.urlopen(self.meetr_url + '?' + data)
        result = json.load(res)
