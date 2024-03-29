# Deltalake with Amazon EMR

This guide helps you quickly explore the main features of Delta Lake.
It provides code snippets that show how to read from and write to Delta tables with Amazon EMR.
<br/>For more details, check [this video, "Incremental Data Processing using Delta Lake with EMR"](https://youtu.be/l1lDAh2bKsU?t=245)

## Quickstart

1. Create s3 bucket for delta lake (e.g. `learn-deltalake-2022`)
2. Create an **EMR Cluster** using AWS CDK (Check details in [instructions](./cdk-stacks/emr-cluster/INSTRUCTIONS.md))
3. Create an **EMR Studio** using AWS CDK (Check details in [instructions](./cdk-stacks/emr-studio/INSTRUCTIONS.md))
4. Open the Amazon EMR console at [https://console.aws.amazon.com/elasticmapreduce/](https://console.aws.amazon.com/elasticmapreduce/)
5. Open the EMR Studio and create an **EMR Studio Workspace**
6. Launch the EMR Studio Workspace
7. Attach the EMR Cluster to a Jupyter Notebook
8. Upload `deltalake-with-emr-demo.ipynb` into the Jupyter Notebook
9. Set kernel to PySpark, and Run each cells
10. For running Amazon Athena queries on Delta Lake, Check [this](./amazon_athena_queries_on_deltalake.md)

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

:information_source: **<i>The following table lists are lastly updated on 26 Aug 2022</i>**

| Delta lake version | Apache Spark version |
|--------------------|----------------------|
| 2.0.x | 3.2.x |
| 1.2.x | 3.2.x |
| 1.1.x | 3.2.x |
| 1.0.x | 3.1.x |
| 0.7.x and 0.8.x | 3.0.x |
| Below 0.7.x | 2.4.2 - 2.4.<i>\<latest\></i> |

 * More infomration at: [Delta Lake releases](https://docs.delta.io/latest/releases.html)

## References

 * [(video) Incremental Data Processing using Delta Lake with EMR](https://youtu.be/l1lDAh2bKsU)
 * [(video) DBT + Spark/EMR + Delta Lake/S3](https://youtu.be/B1zEKtoD8QY)
 * [An Introduction to Modern Data Lake Storage Layers (2022-02-22)](https://dacort.dev/posts/modern-data-lake-storage-layers/)
   * [(github) Modern Data Lake Storage Layers](https://github.com/dacort/modern-data-lake-storage-layers)
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

