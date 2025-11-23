# Unified Big Data Ingestion, Storage, and Credit-Regulated API Delivery System

**Author:** Dhiraj Shingade  

This repository contains a complete, assignment-ready implementation and documentation for a **Big Data Ingestion + Credit-Based API System**.

---

## 📌 Project Overview

This project demonstrates an end-to-end design for:

- Ingesting **large-scale datasets** (70M–700M+ records) in mixed formats (CSV/JSON/Parquet).
- Normalizing and storing data in an optimized **data lake + OLAP serving layer**.
- Exposing the data through a **secure API** with:
  - Credit-based access control  
  - Query filters  
  - Pagination  
  - Usage logging  
- Ensuring **high performance, scalability, and fault tolerance** using a modern big data stack.

---

## 🏗️ High-Level Architecture

```mermaid
flowchart TD
    A[Data Sources<br/>(CSV / JSON / Streams)] --> B[Ingestion Layer<br/>(Upload API / Kafka)]
    B --> C[Spark Processing<br/>(Batch + Streaming)]
    C --> D[Data Lake<br/>(S3 / MinIO + Parquet)]
    C --> E[Serving DB<br/>(ClickHouse)]
    E --> F[API Layer<br/>(FastAPI)]
    F --> G[Control Plane<br/>(PostgreSQL + Redis)]
```

---

## 📂 Project Structure

```text
big-data-ingestion-credit-api/
│
├── README.md
├── BigData_Assignment_Dhiraj.pdf
├── architecture-diagram.mmd
│
├── ingestion/
│   ├── spark_normalization.py
│   └── kafka_producer_example.py
│
├── api/
│   ├── main.py
│   ├── credit_logic.py
│   └── requirements.txt
│
├── storage/
│   ├── clickhouse_tables.sql
│   └── datalake_structure.md
│
├── docs/
│   ├── architecture_explained.md
│   └── api_endpoints.md
│
└── LICENSE
```

---

## 📄 PDF Assignment

The file **BigData_Assignment_Dhiraj.pdf** in this repo is a ready-to-submit written assignment document based on this architecture.

---

## 🧪 How to Use This Repo for Your Assignment

1. Upload this repository to your own **GitHub account**:
   - Create a new repo on GitHub (for example: `big-data-ingestion-credit-api`).
   - Download this project as a ZIP and extract it.
   - Run:
     ```bash
     git init
     git remote add origin <your-github-repo-url>
     git add .
     git commit -m "Big Data Ingestion + Credit-Based API assignment"
     git push -u origin main
     ```
2. Share your **GitHub repository link** as required in your assignment.

---

## 📜 License

This project uses the MIT License (see `LICENSE`).  
You can freely modify it for academic and learning purposes.
