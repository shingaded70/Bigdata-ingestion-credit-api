# Data Lake Structure (S3 / MinIO)

The data lake is organized into **layers** and **partitions** to support high-performance
analytics at scale.

## Buckets / Prefixes

- `s3://data/raw/`  
  - Stores raw, unprocessed files exactly as received.
  - Example:
    - `s3://data/raw/transactions_2025-11-01_sourceA.csv`
    - `s3://data/raw/transactions_2025-11-01_sourceB.json`

- `s3://data/curated/`  
  - Stores cleaned, normalized data in **Parquet** format.
  - Optimized for reading via Spark, ClickHouse, and query engines.

## Partitioning Strategy

For the canonical `transactions` dataset:

- Primary partitions:
  - `dt = date(timestamp)`
  - `country`

Example Parquet layout:

```text
s3://data/curated/transactions/
    dt=2025-11-01/country=IN/part-0000.parquet
    dt=2025-11-01/country=US/part-0001.parquet
    dt=2025-11-02/country=IN/part-0002.parquet
```

This layout allows query engines to **prune partitions** efficiently when users filter by
date and/or country, reducing I/O and improving performance.
