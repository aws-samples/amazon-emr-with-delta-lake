### 1. Create database

```
CREATE DATABASE my_delta_db;
```

### 2. Create table

<pre>
DROP TABLE IF EXISTS my_delta_db.delta_trip_table;

CREATE EXTERNAL TABLE my_delta_db.delta_trip_table (
  destination string,
  trip_id bigint,
  tstamp string,
  origin string
)
PARTITIONED BY (route_id string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.SymlinkTextInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION 's3://<i>your-s3-location</i>/_symlink_format_manifest/';
</pre>

### 3. Repair partitions

```
MSCK REPAIR TABLE my_delta_db.delta_trip_table;
```

### 4. Others

```
SELECT count(*) FROM my_delta_db.delta_trip_table;

SELECT max(trip_id) FROM my_delta_db.delta_trip_table;

SELECT DISTINCT destination from my_delta_db.delta_trip_table ORDER BY destination;

SELECT destination, route_id, trip_id, tstamp FROM my_delta_db.delta_trip_table LIMIT 10;

SELECT DISTINCT route_id from my_delta_db.delta_trip_table ORDER BY route_id;

SELECT * FROM my_delta_db.delta_trip_table WHERE trip_id > 1999996 ORDER BY trip_id;

SELECT count(*) AS Count_Syracuse FROM my_delta_db.delta_trip_table WHERE destination = 'Syracuse';

SELECT count(*) AS Count_Philadelphia FROM my_delta_db.delta_trip_table WHERE destination = 'Philadelphia';

SELECT count(*) as Count_total FROM my_delta_db.delta_trip_table;

SELECT count(*) as Count_NJ FROM my_delta_db.delta_trip_table WHERE destination = 'New Jersey';
```
