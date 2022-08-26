# Deltalake with Amazon EMR

This guide helps you quickly explore the main features of Delta Lake.
It provides code snippets that show how to read from and write to Delta tables with Amazon EMR.
<br/>For more details, check [this video](https://youtu.be/l1lDAh2bKsU?t=245)

## Quickstart

1. Create s3 bucket for delta lake (e.g. `learn-deltalake-2022`)
2. Create EMR Cluster using AWS CDK. (Check details in [instructions](./cdk/INSTRUCTIONS.md))
3. Open the Amazon EMR console at [https://console.aws.amazon.com/elasticmapreduce/](https://console.aws.amazon.com/elasticmapreduce/)
4. Create Jupyter Notebook
5. Upload `deltalake-with-emr-demo.ipynb` into Jupyter Notebook
6. Set kernel to PySpark, and Run each cells
7. For run Amazn Athena queries on Delta Lake, Check [this](./amazon_athena_queries_on_deltalake.md)

## Key Configurations

- Amazon EMR Applications
  - Hadoop
  - Hive
  - JupyterHub
  - JupyterEnterpriseGateway
  - Livy
  - Apache Spark (>= 3.0)

- Apache Spark (PySpark)

  <pre>
  {
    "conf": {
      "spark.jars.packages": "io.delta:delta-core_2.12:<i>{version}</i>",
      "spark.sql.extensions": "io.delta.sql.DeltasparkSessionExtension",
      "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    }
  }
  </pre>

  * :warning: **YOU MUST REPLACE** <i>{version}</i> with the appropriate one
  * For more details, check [this](https://docs.delta.io/latest/quick-start.html#set-up-apache-spark-with-delta-lake)

## Compatibility with Apache Spark

| Delta lake version | Apache Spark version |
|--------------------|----------------------|
| 1.1.x | 3.2.x |
| 1.0.x | 3.1.x |
| 0.7.x and 0.8.x | 3.0.x |
| Below 0.7.x | 2.4.2 - 2.4.<i>\<latest\></i> |

## References

 * [(video) Incremental Data Processing using Delta Lake with EMR](https://youtu.be/l1lDAh2bKsU)
 * [(video) DBT + Spark/EMR + Delta Lake/S3](https://youtu.be/B1zEKtoD8QY)
 * [Compatibility with Apache Spark](https://docs.delta.io/latest/releases.html#compatibility-with-apache-spark)
 * [Application versions in Amazon EMR 6.x releases](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-release-app-versions-6.x.html)
 * [Application versions in Amazon EMR 5.x releases](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-release-app-versions-5.x.html)
 * [Delta Lake releases](https://docs.delta.io/latest/releases.html)
 * [Delta Core Maven Repository](https://mvnrepository.com/artifact/io.delta/delta-core)
 * [Set up Apache Spark with Delta Lake](https://docs.delta.io/latest/quick-start.html#set-up-apache-spark-with-delta-lake)
 * [Presto and Athena to Delta Lake integration](https://docs.delta.io/1.0.0/presto-integration.html)
 * [Redshift Spectrum to Delta Lake integration](https://docs.delta.io/1.0.0/redshift-spectrum-integration.html)
 * [Support for automatic and incremental Presto/Athena manifest generation (#453)](https://github.com/delta-io/delta/releases/tag/v0.7.0)

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

