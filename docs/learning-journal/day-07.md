# Day 7 — Python COPY Load & Ingestion Pipeline

## Session Focus

Implement the actual file loading step of the Python ingestion pipeline and connect the idempotency check to a real PostgreSQL `COPY` operation.

## Review

Previous sessions established:

* Raw telecom data is preserved separately from analytical tables.
* PostgreSQL runs inside Docker.
* `raw.telecom_activity_raw` stores the original telecom activity structure.
* `raw.ingestion_log` is used to track previously processed files.
* SHA-256 is used as the file identity.
* The ingestion pipeline must be idempotent.
* A previously processed file should produce `SKIP` rather than being loaded again.

## What We Implemented

### 1. Case-insensitive Hash Check

The ingestion log originally stored the existing hash in uppercase while Python's `hashlib.hexdigest()` returns lowercase.

The original comparison:

```sql
WHERE file_hash = %s
```

was therefore case-sensitive.

It was changed to:

```sql
WHERE LOWER(file_hash) = LOWER(%s)
```

This allows the pipeline to correctly recognize the same file regardless of hash letter case.

Result:

```text
Ingestion action: SKIP
```

for the previously registered `sample_100k.txt` file.

---

### 2. Created a Small Ingestion Test File

A one-row test file was created locally:

```text
data/raw/sample_ingestion_test.txt
```

The record contains the expected eight raw columns:

```text
square_id
time_interval
country_code
sms_in
sms_out
call_in
call_out
internet
```

The file was intentionally kept outside Git because raw data files are ignored by the repository.

---

### 3. Implemented `load_file_to_raw()`

A new Python function was added to perform the actual PostgreSQL load:

```python
def load_file_to_raw(conn, file_path: Path) -> int:
    """Load a TSV file into the raw telecom activity table."""
```

The function uses PostgreSQL:

```sql
COPY raw.telecom_activity_raw
FROM STDIN
WITH (
    FORMAT text,
    DELIMITER E'\t',
    NULL ''
)
```

Python reads the local file and streams its contents to PostgreSQL through the database connection.

Conceptually:

```text
Local File
    ↓
Python
    ↓
COPY FROM STDIN
    ↓
PostgreSQL
    ↓
raw.telecom_activity_raw
```

---

### 4. Preserved NULL Semantics

The `COPY` operation uses:

```sql
NULL ''
```

This means empty fields in the source file are loaded as SQL `NULL`.

This preserves the project's existing data-quality principle:

> Missing activity is not automatically interpreted as zero.

---

### 5. Connected LOAD Decision to Actual Loading

Previously, the pipeline could only determine:

```text
SKIP
```

or:

```text
LOAD
```

but `LOAD` did not perform an actual database operation.

The pipeline was extended so that:

```text
Hash Check
    ↓
File not found in ingestion_log
    ↓
LOAD
    ↓
load_file_to_raw()
    ↓
COPY
```

The successful test produced:

```text
Ingestion action: LOAD
Rows loaded: 1
```

This confirms that Python successfully transferred data into PostgreSQL using `COPY FROM STDIN`.

---

## Current Pipeline

The current implementation is:

```text
Input File
    ↓
Calculate SHA-256
    ↓
Check raw.ingestion_log
    ↓
 ┌───────────────┐
 │ Hash exists?  │
 └───────┬───────┘
         │
    ┌────┴────┐
   Yes       No
    ↓         ↓
  SKIP       LOAD
              ↓
        COPY FROM STDIN
              ↓
      raw.telecom_activity_raw
```

## Important Limitation

The ingestion pipeline is **not yet fully transactional or idempotent after the actual load**.

At the end of Day 7:

* File detection works.
* `SKIP` detection works.
* Actual `COPY` loading works.
* Row counting works.

But after a successful `COPY`, the file is not yet registered in `raw.ingestion_log`.

Therefore the complete workflow:

```text
COPY
  ↓
Register ingestion
  ↓
COMMIT
```

has not yet been implemented.

This will be the next step.

## Key Learning

### `COPY FROM STDIN`

`COPY FROM STDIN` allows the application to stream file contents to PostgreSQL through the database connection.

This is preferable to making PostgreSQL directly access a local Windows path when PostgreSQL is running inside Docker.

### Idempotency

Idempotency requires more than detecting a previously processed file.

The complete operation should eventually behave like:

```text
New file
   ↓
LOAD
   ↓
Register file
   ↓
COMMIT

Same file again
   ↓
SKIP
```

The registration and database load must eventually become one reliable transaction.

## Day 7 Outcome

Successfully implemented and tested:

* Case-insensitive file-hash detection
* Python → PostgreSQL connection
* PostgreSQL `COPY FROM STDIN`
* Streaming local file contents to PostgreSQL
* Raw table loading
* Row counting
* LOAD decision execution

Next session:

> Complete transactional ingestion by registering the file in `raw.ingestion_log` and ensuring `LOAD + registration` behave atomically.
