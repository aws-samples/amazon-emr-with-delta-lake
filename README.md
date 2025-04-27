# Delta Lake OSS with Amazon EMR

This guide helps you quickly explore the main features of Delta Lake.
It provides code snippets that show how to read from and write to Delta tables with Amazon EMR.
<br/>For more details, check [this video, "Incremental Data Processing using Delta Lake with EMR"](https://youtu.be/l1lDAh2bKsU?t=245)

## Quickstart

1. Create an **EMR Studio integrated with EMR on EC2** using AWS CDK (Check details in [instructions](./emr_studio_with_emr_on_ec2/README.md)
2. Open the Amazon EMR console at [https://console.aws.amazon.com/elasticmapreduce/](https://console.aws.amazon.com/elasticmapreduce/)
3. Open the EMR Studio and create an **EMR Studio Workspace**
4. Launch the EMR Studio Workspace
5. Attach the EMR Cluster to a Jupyter Notebook by following quick guide:

   On the EMR Studio Workspace Web Console.
   - Step 1. Create a new workspace without attaching the EMR cluster.
   - Step 2. Stop the workspace.
   - Step 3. Select the stopped workspace and restart it using **Launch Workspace > Launch with options**.

    :information_source: More information can be found [here](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-studio-create-use-clusters.html).
6. Upload `deltalake-with-emr-demo.ipynb` into the Jupyter Notebook
7. Set kernel to PySpark, and Run each cells
8.  For running Amazon Athena queries on Delta Lake, Check [this](./amazon_athena_queries_on_deltalake.md)

## Key Configurations

- Amazon EMR Applications
  - Hadoop
  - Hive
  - JupyterHub
  - JupyterEnterpriseGateway
  - Livy
  - Apache Spark (>= 3.0)

- Apache Spark (PySpark)
  - For `emr-6.7.0` version
    <pre>
    {
      "conf": {
        "spark.jars.packages": "<i>io.delta:delta-core_2.12:1.2.1</i>",
        "spark.sql.extensions": "io.delta.sql.DeltasparkSessionExtension",
        "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog"
      }
    }
    </pre>
  - For `>= emr-6.9.0` and `< emr-7.0.0` version
    <pre>
    {
      "conf": {
        "spark.jars.packages": "<i>io.delta:delta-core_2.13:2.1.0</i>",
        "spark.sql.extensions": "io.delta.sql.DeltasparkSessionExtension",
        "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        "spark.sql.catalog.spark_catalog.lf.managed": "true"
      }
    }
    </pre>
  - For `emr-7.x.x` version
    <pre>
    {
      "conf": {
        "spark.jars.packages": "<i>io.delta:delta-spark_2.13:3.3.1</i>",
        "spark.sql.extensions": "io.delta.sql.DeltasparkSessionExtension",
        "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog"
        "spark.sql.catalog.spark_catalog.lf.managed": "true"
      }
    }
    </pre>

  > :warning: **YOU NEED** to configure `spark.jar.packages` according to the Delta version that matches your Spark version.

  > :information_source: For more details on `spark.jar.packages`, see [Apache Spark Configuration - Runtime Environment](https://spark.apache.org/docs/latest/configuration.html#runtime-environment)

  > See also [[1] Set up Apache Spark with Delta Lake](https://docs.delta.io/latest/quick-start.html#set-up-apache-spark-with-delta-lake), [[2] Use a Delta Lake cluster with Spark](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/Deltausing-cluster-spark.html).

## Compatibility with Apache Spark

:information_source: **<i>The following table lists are lastly updated on 3 Aug 2024</i>**

| Delta lake version | Apache Spark version |
|--------------------|----------------------|
| 3.3.x | 3.5.x |
| 3.2.x | 3.5.x |
| 3.1.x | 3.5.x |
| 3.0.x | 3.5.x |
| 2.4.x | 3.4.x |
| 2.3.x | 3.3.x |
| 2.2.x | 3.3.x |
| 2.1.x | 3.3.x |
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
 * [Amazon EMR Releases](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-release-components.html)
   * [Application versions in Amazon EMR 7.x releases](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-release-app-versions-7.x.html)
   * [Application versions in Amazon EMR 6.x releases](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-release-app-versions-6.x.html)
   * [Application versions in Amazon EMR 5.x releases](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-release-app-versions-5.x.html)
 * [Delta Lake releases](https://docs.delta.io/latest/releases.html)
 * [`io.delta` Maven Repository](https://mvnrepository.com/artifact/io.delta)
   * [delta-core](https://mvnrepository.com/artifact/io.delta/delta-core)
   * [delta-spark](https://mvnrepository.com/artifact/io.delta/delta-spark)
 * [Apache Spark Configuration - Runtime Environment](https://spark.apache.org/docs/latest/configuration.html#runtime-environment)
 * [Set up Apache Spark with Delta Lake](https://docs.delta.io/latest/quick-start.html#set-up-apache-spark-with-delta-lake)
 * [Presto and Athena to Delta Lake integration](https://docs.delta.io/1.0.0/presto-integration.html)
 * [Redshift Spectrum to Delta Lake integration](https://docs.delta.io/1.0.0/redshift-spectrum-integration.html)
 * [Support for automatic and incremental Presto/Athena manifest generation (#453)](https://github.com/delta-io/delta/releases/tag/v0.7.0)
 * [Amazon EMR - Attach a compute to an EMR Studio Workspace](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-studio-create-use-clusters.html)

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

