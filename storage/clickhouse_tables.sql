-- ClickHouse schema for the transactions table

CREATE DATABASE IF NOT EXISTS analytics;

USE analytics;

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id String,
    user_id String,
    timestamp DateTime,
    amount Decimal(18,2),
    currency String,
    category String,
    country String,
    raw_source String,
    ingested_at DateTime
)
ENGINE = MergeTree
PARTITION BY toDate(timestamp)
ORDER BY (user_id, timestamp);
