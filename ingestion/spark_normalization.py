"""
Spark normalization job for big data ingestion.

This script reads raw CSV data from an object storage path, normalizes it
into a canonical transaction schema, and writes it as partitioned Parquet.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, lit, current_timestamp

def main():
    spark = (SparkSession.builder
             .appName("NormalizeIngestedData")
             .getOrCreate())

    raw_path = "s3a://data/raw/transactions_*.csv"
    curated_path = "s3a://data/curated/transactions/"

    df_raw = (spark.read
              .option("header", "true")
              .csv(raw_path))

    df_norm = (df_raw
        .withColumn("transaction_id", col("txn_id"))
        .withColumn("user_id", col("user"))
        .withColumn("timestamp", to_timestamp(col("txn_time")))
        .withColumn("amount", col("amt").cast("decimal(18,2)"))
        .withColumn("currency", col("curr"))
        .withColumn("category", col("cat"))
        .withColumn("country", col("country"))
        .withColumn("raw_source", lit("batch_csv"))
        .withColumn("ingested_at", current_timestamp())
        .select(
            "transaction_id", "user_id", "timestamp", "amount",
            "currency", "category", "country", "raw_source", "ingested_at"
        )
    )

    (df_norm
        .write
        .mode("append")
        .partitionBy("country")
        .parquet(curated_path)
    )

    spark.stop()

if __name__ == "__main__":
    main()
