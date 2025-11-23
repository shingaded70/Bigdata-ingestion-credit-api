# Architecture Explained

This document explains the overall design of the **Unified Big Data Ingestion, Storage,
and Credit-Regulated API Delivery System**.

## 1. Ingestion Layer

- Handles batch uploads (CSV / JSON / Parquet files).
- Handles streaming ingestion via **Kafka**.
- Decouples producers from consumers so that processing can scale independently.

## 2. Processing Layer (Spark)

- Uses **Apache Spark** for:
  - Parsing and validating heterogeneous input data.
  - Normalizing into a canonical schema.
  - Writing standardized data to the data lake as partitioned Parquet.
- Supports both **batch** jobs and **Structured Streaming**.

## 3. Data Lake (S3 / MinIO + Parquet)

- Central storage for all normalized data.
- Parquet format is used for:
  - Columnar compression
  - Efficient analytical reads
- Tables are partitioned by date and country to support fast time-range and geo queries.

## 4. Serving Layer (ClickHouse)

- ClickHouse is used as a **low-latency analytical database**.
- Normalized data is loaded from the data lake into ClickHouse.
- APIs query ClickHouse directly for fast response times.

## 5. API Layer (FastAPI)

- Exposes REST endpoints to:
  - Query transactions with filters and pagination.
  - Check remaining credits.
- Implements **credit-based access control**:
  - Each response consumes credits based on the number of records returned.

## 6. Control Plane (PostgreSQL + Redis)

- PostgreSQL stores:
  - Users
  - API keys
  - Credit balances
  - Usage logs
- Redis provides:
  - Caching for frequently repeated queries.
  - Fast access to rate-limiting / session data.

## 7. Scalability and Fault Tolerance

- Kafka partitions can be increased to scale ingestion.
- Spark can run on a cluster (YARN / Kubernetes) with many executors.
- ClickHouse can be deployed as a distributed cluster.
- The API layer can scale horizontally behind a load balancer or API gateway.
