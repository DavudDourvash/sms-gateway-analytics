# Day 6 — Idempotent Ingestion Pipeline

## Date

2026-09-27

## Focus

Implement the first executable part of an **idempotent ingestion pipeline** using:

* Python
* SHA-256 file hashing
* PostgreSQL
* `psycopg`
* `raw.ingestion_log`

---

## Goal

The goal of Day 6 was to move the idempotency concept from a database-level experiment into the Python ingestion pipeline.

Target flow:

```text
Source File
    ↓
Calculate SHA-256
    ↓
Check ingestion_log
    ↓
Already Loaded?
   ↙       ↘
 YES       NO
  ↓         ↓
SKIP      LOAD
```

The actual `LOAD` step is intentionally left for the next session.

---

## What Was Implemented

### 1. PostgreSQL Driver

Installed the PostgreSQL driver for Python:

```text
psycopg 3.3.6
psycopg-binary 3.3.6
```

The driver allows the Python ingestion script to communicate directly with PostgreSQL.

---

### 2. File Hash Calculation

Implemented SHA-256 hashing using Python's `hashlib`.

The ingestion script reads the file in chunks instead of loading the entire file into memory.

```python
for chunk in iter(lambda: file.read(1024 * 1024), b""):
    sha256.update(chunk)
```

This approach is more appropriate for large source files.

---

### 3. Stable Project File Path

The project root is determined from the script location:

```python
PROJECT_ROOT = Path(__file__).resolve().parents[2]
```

The input file is then defined relative to the project root:

```python
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "sample_100k.txt"
```

This avoids depending on the current working directory when the script is executed.

---

### 4. Python → PostgreSQL Connection

Implemented a reusable database connection function using `psycopg`:

```python
def get_db_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="sms_gateway_analytics",
        user="analytics_user",
        password="analytics_password",
    )
```

The connection was successfully tested.

---

### 5. Ingestion Log Check

Implemented a function to check whether the calculated file hash already exists in:

```text
raw.ingestion_log
```

The query uses:

```sql
SELECT EXISTS (
    SELECT 1
    FROM raw.ingestion_log
    WHERE file_hash = %s
);
```

The result is converted into a Python boolean:

```text
True  → File already registered
False → File is new
```

---

## Test Result

The ingestion script successfully:

1. Located the source file.
2. Calculated its SHA-256 hash.
3. Connected to PostgreSQL.
4. Queried `raw.ingestion_log`.
5. Produced an ingestion decision.

Example output:

```text
File: ...\data\raw\sample_100k.txt
SHA-256: cb4057ab9066a94bb3f07816809be85d5847499dd223eea1f4a7c4c439350b68
Ingestion action: LOAD
```

At this stage, `LOAD` represents the **decision only**.

No actual database loading was performed by the Python script.

---

## Important Engineering Observation

The current pipeline has reached the decision point:

```text
File
 ↓
Hash
 ↓
ingestion_log
 ↓
LOAD / SKIP decision
```

The next engineering step is to implement the actual loading process safely.

The intended next flow is:

```text
Calculate Hash
      ↓
Check ingestion_log
      ↓
Already Loaded?
   ↙          ↘
 YES           NO
  ↓             ↓
SKIP          COPY
                ↓
          Register ingestion
```

The `COPY` operation and ingestion registration should eventually be handled within a transaction so that a failed ingestion does not leave an inconsistent state.

---

## Concepts Learned

### Idempotency

An ingestion process is idempotent when repeating the same operation does not unintentionally create additional copies of the same data.

Example:

```text
Run 1 → LOAD 100,000 rows
Run 2 → SKIP
Run 3 → SKIP
```

Instead of:

```text
Run 1 → 100,000 rows
Run 2 → 200,000 rows
Run 3 → 300,000 rows
```

---

### Content Hash vs. File Name

A file name is not a reliable identifier for file content.

For example:

```text
sample_100k.txt
sample_backup.txt
sample_copy.txt
```

could contain exactly the same data.

SHA-256 identifies the **content**, rather than relying only on the file name.

---

### Decision vs. Execution

A useful distinction in ingestion design:

```text
Decision
LOAD / SKIP
```

is different from:

```text
Execution
Actually loading the data
```

Day 6 currently implements the first part.

---

## Current Architecture

```text
                    ┌─────────────────┐
                    │   Source File   │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Python Ingestion│
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │    SHA-256      │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │  PostgreSQL     │
                    │ ingestion_log   │
                    └────────┬────────┘
                             ↓
                      LOAD / SKIP
```

---

## Next Step

Day 7 / next ingestion session:

* Implement actual PostgreSQL `COPY`
* Stream the source file from Python
* Use a database transaction
* Register successful ingestion in `raw.ingestion_log`
* Test first load
* Run the same file again
* Verify that the second run produces `SKIP`
* Validate row counts and ingestion log

---

## Key Takeaway

Day 6 moved idempotency from a theoretical concept into executable ingestion logic.

The pipeline can now identify a source file using its content hash and make an explicit `LOAD` or `SKIP` decision.

The next step is to make the `LOAD` operation itself reliable and transactional.
