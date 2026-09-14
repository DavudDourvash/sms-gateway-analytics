# Data Architecture

## Version 1

The initial architecture follows a simple batch-oriented data pipeline.

```text
Public Telecom Data
        ↓
Python Ingestion
        ↓
Raw Data
        ↓
PostgreSQL
        ↓
Transformation
        ↓
Analytics Data Mart
        ↓
AI Analyst
```

## Architecture Layers

### 1. Source Layer

Public real-world telecommunications activity data from the Telecom Italia Big Data Challenge dataset.

The initial analytical scope focuses on SMS activity.

### 2. Ingestion Layer

Python will be used to retrieve, inspect, and process the source data.

The ingestion process will initially support batch processing and will evolve toward incremental processing as the project grows.

### 3. Raw Data Layer

The original source data will be preserved before analytical transformations.

The raw layer provides a reproducible starting point for downstream processing and makes it possible to reprocess data when transformation logic changes.

### 4. Storage Layer

PostgreSQL is planned as the initial structured analytical storage layer.

This decision is provisional and will be validated after profiling the real dataset.

Storage design will consider:

* Data volume
* Data types
* Query patterns
* Partitioning
* Indexing
* Incremental loading

### 5. Transformation Layer

SQL and Python will transform raw data into structures suitable for analysis.

Transformations may include:

* Data type normalization
* Data quality checks
* Time transformations
* Aggregations
* Dimension preparation
* Fact table preparation

### 6. Analytics Layer

The analytics layer will provide metrics and analytical datasets for understanding SMS activity.

Initial analytical areas include:

* SMS traffic over time
* SMS-in vs. SMS-out activity
* Geographic patterns
* Traffic peaks and drops
* Anomaly detection

### 7. AI Analyst Layer

The final stage of the project will introduce an AI-powered analytical assistant.

The AI Analyst should not directly guess answers.

Instead, it should use analytical data and SQL-based evidence to answer questions such as:

> Why did SMS activity decrease?

The goal is to build an evidence-based analytical workflow:

```text
User Question
      ↓
AI Analyst
      ↓
Query / Analysis
      ↓
Analytical Data
      ↓
Evidence
      ↓
Explanation
```

## Processing Strategy

The initial pipeline will use batch processing.

Because the source dataset is large, data will be processed incrementally rather than loading the complete dataset into memory at once.

The processing strategy may evolve toward:

```text
Batch Processing
      ↓
Incremental Processing
      ↓
Automated Pipeline
      ↓
Scheduled / Orchestrated Pipeline
```

The final processing architecture will be determined based on the actual characteristics of the data.

## Development Strategy

Development will initially run locally.

The project will evolve progressively:

```text
Local Development
      ↓
Dockerized Environment
      ↓
Cloud Infrastructure
      ↓
Production-like Pipeline
```

Cloud technologies will be introduced after the local architecture and data pipeline are understood and validated.

## Initial Data Model

The analytical model is expected to evolve toward a star schema containing:

* `fact_sms_activity`
* `dim_time`
* `dim_cell`
* `dim_country`

This is an initial hypothesis rather than a final schema.

The final data model will be determined after profiling the source data and understanding:

* Grain
* Keys
* Relationships
* Cardinality
* Data types
* Data volume
* Query patterns

## Architectural Principles

The project will follow these principles:

1. **Understand the data before designing the final model.**
2. **Keep raw data separate from transformed data.**
3. **Prefer simple architecture before adding complexity.**
4. **Use incremental processing when data volume requires it.**
5. **Make data quality observable and testable.**
6. **Keep architecture decisions reversible when possible.**
7. **Introduce cloud, orchestration, and AI only when they solve a demonstrated problem.**
8. **Never fabricate unavailable business data.**

## Current Status

**Version:** 1.0

**Status:** Initial architecture defined.

**Next step:** Profile the real source data before finalizing the storage and analytical data model.
