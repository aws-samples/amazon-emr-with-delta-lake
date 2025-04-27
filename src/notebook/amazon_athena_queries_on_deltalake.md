# Use Hive to query Delta Lake tables

We can query data of Delta Lake by using a Hive external table.

### 1. Create database

```
CREATE DATABASE IF NOT EXISTS my_hive_delta_db;
```

### 2. Create table

<pre>
DROP TABLE IF EXISTS my_hive_delta_db.delta_trip_table;

CREATE EXTERNAL TABLE my_hive_delta_db.delta_trip_table (
  destination string,
  trip_id bigint,
  tstamp string,
  origin string
)
PARTITIONED BY (route_id string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.SymlinkTextInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION 's3://<i>your-s3-location-for-delta-hive-table</i>/_symlink_format_manifest/';
</pre>

### 3. Repair partitions

```
MSCK REPAIR TABLE my_hive_delta_db.delta_trip_table;
```

### 4. Run Queries

```
SELECT count(*) FROM my_hive_delta_db.delta_trip_table;

SELECT max(trip_id) FROM my_hive_delta_db.delta_trip_table;

SELECT DISTINCT destination FROM my_hive_delta_db.delta_trip_table ORDER BY destination;

SELECT destination, route_id, trip_id, tstamp FROM my_hive_delta_db.delta_trip_table LIMIT 10;

SELECT DISTINCT route_id FROM my_hive_delta_db.delta_trip_table ORDER BY route_id;

SELECT * FROM my_hive_delta_db.delta_trip_table WHERE trip_id > 1999996 ORDER BY trip_id;

SELECT count(*) AS Count_Syracuse FROM my_hive_delta_db.delta_trip_table WHERE destination = 'Syracuse';

SELECT count(*) AS Count_Philadelphia FROM my_hive_delta_db.delta_trip_table WHERE destination = 'Philadelphia';

SELECT count(*) as Count_total FROM my_hive_delta_db.delta_trip_table;

SELECT count(*) as Count_NJ FROM my_hive_delta_db.delta_trip_table WHERE destination = 'New Jersey';
```



# Querying Delta Lake tables

We can use Amazon Athena to read Delta Lake tables stored in Amazon S3 directly without having to generate manifest files or run the `MSCK REPAIR` statement.

### 1. Create database

```
CREATE DATABASE IF NOT EXISTS my_spark_delta_db;
```

### 2. Create table

<pre>
DROP TABLE IF EXISTS my_spark_delta_db.delta_spark_table;

CREATE EXTERNAL TABLE my_spark_delta_db.delta_spark_table
LOCATION 's3://<i>your-s3-location-for-delta-spark-table</i>/<i>your-folder</i>/'
TBLPROPERTIES ('table_type' = 'DELTA');
</pre>

### 3. Run Queries

```
SELECT count(*) FROM my_spark_delta_db.delta_spark_table;

SELECT max(trip_id) FROM my_spark_delta_db.delta_spark_table;

SELECT DISTINCT destination FROM my_spark_delta_db.delta_spark_table ORDER BY destination;

SELECT destination, route_id, trip_id, tstamp FROM my_spark_delta_db.delta_spark_table LIMIT 10;

SELECT DISTINCT route_id FROM my_spark_delta_db.delta_spark_table ORDER BY route_id;

SELECT * FROM my_spark_delta_db.delta_spark_table WHERE trip_id > 1999996 ORDER BY trip_id;

SELECT count(*) AS Count_Syracuse FROM my_spark_delta_db.delta_spark_table WHERE destination = 'Syracuse';

SELECT count(*) AS Count_Philadelphia FROM my_spark_delta_db.delta_spark_table WHERE destination = 'Philadelphia';

SELECT count(*) as Count_total FROM my_spark_delta_db.delta_spark_table;

SELECT count(*) as Count_NJ FROM my_spark_delta_db.delta_spark_table WHERE destination = 'New Jersey';
```



# References

 * [Apache Hive to Delta Lake integration](https://docs.delta.io/latest/hive-integration.html)
 * [Querying Linux Foundation Delta Lake tables](https://docs.aws.amazon.com/athena/latest/ug/delta-lake-tables.html)
