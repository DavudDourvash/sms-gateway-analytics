# Day 5 — Idempotent Ingestion & File Hashing

## Focus

The focus of Day 5 was understanding how repeated ingestion can create duplicate data and how to design an ingestion process to be idempotent.

## What I Implemented

* Restarted the Dockerized PostgreSQL environment.
* Verified the PostgreSQL container and project schemas.
* Validated the current Raw Layer.
* Confirmed that the same 100,000-row sample had been loaded three times.
* Verified:

  * Total raw rows: 300,000
  * Distinct logical records: 100,000
* Confirmed that duplicate records had identical values, indicating repeated ingestion rather than distinct source activities.
* Discussed why adding a primary key directly to the Raw Layer is not necessarily the correct solution.
* Created an ingestion tracking table:

```text
raw.ingestion_log
```

The table stores:

* `file_name`

* `file_hash`

* `loaded_at`

* `row_count`

* `status`

* Added a unique constraint on `file_hash`.

* Calculated the SHA-256 hash of `sample_100k.txt`:

```text
CB4057AB9066A94BB3F07816809BE85D5847499DD223EEA1F4A7C4C439350B68
```

* Registered the file and its hash in `raw.ingestion_log`.

## Key Engineering Concept: Idempotent Ingestion

An ingestion process is idempotent when processing the same source data multiple times does not unintentionally change the final state.

For example:

```text
First ingestion:
100,000 logical records

Retry with the same content:
100,000 logical records
```

Not:

```text
100,000 → 200,000
```

## File Name vs. File Content

Using only the file name to detect previously processed files is insufficient.

For example:

```text
2026-09-22.txt
2026-09-23.txt
```

may have different names but identical content.

Therefore, the pipeline uses a content-based identifier:

```text
File
 ↓
SHA-256
 ↓
File Hash
```

If two files have identical content, they produce the same SHA-256 hash.

The `UNIQUE` constraint on `file_hash` can then prevent the same content from being registered as a new ingestion.

## Important Distinction

Two different types of duplicates need to be handled separately:

### 1. Duplicate File / Repeated Ingestion

Detected using:

```text
File Content → SHA-256 Hash
```

### 2. Duplicate Records Inside Data

Handled at the appropriate data-model layer using the defined grain and database constraints.

For the analytical fact table, the grain is:

```text
time_key + square_id + country_code
```

and the fact table already has a primary key on this grain.

## Current State

The ingestion tracking mechanism has been created and the first file has been registered.

The final end-to-end idempotent ingestion test is still pending.

## Key Takeaway

A reliable data pipeline is not only about successfully loading data.

It must also handle:

* repeated execution
* retries
* duplicate ingestion
* data lineage
* validation
* reproducibility

The main lesson from Day 5:

> **Successful ingestion is not enough; ingestion must also be safe to repeat.**
