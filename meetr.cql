CREATE KEYSPACE IF NOT EXISTS meetr 
WITH replication = {'class' : 'SimpleStrategy', 'replication_factor' : 3};

USE meetr;

CREATE TABLE IF NOT EXISTS metrics (
    metric varchar,
    collected_at timestamp,
    metric_value bigint,    
    PRIMARY KEY (metric, collected_at)
) WITH COMPACT STORAGE;
