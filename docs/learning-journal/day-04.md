# Day 4 — PostgreSQL, Docker and Raw Data Ingestion

## Purpose

Day 4 focused on implementing the conceptual data model in PostgreSQL and creating the first local data ingestion pipeline using Docker.

The main goal was to move from:

Conceptual Data Model

to:

Physical Database Model

and then load real source data into the Raw Layer.

---

## Dockerized PostgreSQL

### What I learned

PostgreSQL can be run inside a Docker container instead of being installed directly on the host operating system.

Docker provides an isolated and reproducible environment for database development.

### Application in this project

The project uses:

* Docker Desktop
* PostgreSQL 16
* Docker Compose
* Persistent PostgreSQL volume

The PostgreSQL container is:

`sms_gateway_postgres`

The database is:

`sms_gateway_analytics`

The PostgreSQL server was successfully accessed using `psql`.

### Status

Completed.

---

## Database Schemas

Two schemas were created:

* `raw`
* `analytics`

### Purpose

The `raw` schema is responsible for preserving source data.

The `analytics` schema contains the structured analytical model.

Conceptually:

```text
Source Data
    ↓
raw
    ↓
Transformation
    ↓
analytics
```

This separation prevents raw source data from being mixed with analytical structures.

### Status

Completed.

---

## Physical Data Model

The conceptual model from Day 3 was implemented in PostgreSQL.

The analytical tables are:

* `analytics.dim_square`
* `analytics.dim_country`
* `analytics.dim_time`
* `analytics.fact_sms_activity`

The fact table uses:

```text
time_key + square_id + country_code
```

as its composite primary key.

This enforces the analytical grain defined on Day 3:

> One geographic square + one country code + one 10-minute time interval

### Status

Completed.

---

## Raw Layer

A Raw table was created:

```text
raw.telecom_activity_raw
```

The table preserves the source structure:

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

The Raw table intentionally does not use the analytical fact-table primary key.

The purpose of this layer is to preserve source data before transformation.

### Status

Completed.

---

## First Data Ingestion

A 100,000-row sample was copied into the Docker container:

```text
sample_100k.txt
```

The file was then loaded into PostgreSQL using PostgreSQL `COPY`.

The ingestion command successfully reported:

```text
COPY 100000
```

This demonstrated that PostgreSQL can directly load the tab-separated source file into the Raw Layer.

### Status

Completed.

---

## NULL Handling During Ingestion

The source contains empty activity fields.

The `COPY` command was configured with:

```sql
NULL ''
```

This allows empty source fields to remain SQL `NULL` values.

This preserves the distinction established during profiling:

> NULL ≠ 0

No artificial zero values were introduced during ingestion.

### Status

Completed.

---

## First Ingestion Validation

After loading the sample, the Raw table contained:

```text
300,000 rows
```

The most recent `COPY` operation added:

```text
100,000 rows
```

Therefore, the table already contained data from previous load attempts.

This revealed an important ingestion concern:

> Re-running a load operation can create duplicate data if the pipeline is not idempotent.

The duplicate-grain validation was intentionally not completed during Day 4 because the work session ended.

---

## Idempotent Ingestion

### What I learned

A data ingestion process should ideally be safe to retry.

If the same source file is processed multiple times, the pipeline should not unintentionally create duplicate records.

This property is commonly described as:

> Idempotent ingestion

### Application in this project

The current Raw table contains 300,000 rows after multiple sample loads.

The next step is to compare:

```text
total rows
```

with:

```text
distinct (square_id, time_interval, country_code)
```

to determine whether repeated ingestion created duplicate logical records.

This will be investigated before continuing with the transformation layer.

### Status

Investigation started — validation pending.

---

## Data Engineering Concepts Applied

Day 4 connected several engineering concepts:

* Dockerized development
* Database schemas
* Physical data modeling
* Raw data preservation
* PostgreSQL `COPY`
* NULL preservation
* Data ingestion
* Retry safety
* Idempotency
* Data validation

The overall pipeline is now evolving toward:

```text
Public Telecom Data
        ↓
Python / Source File
        ↓
Raw Layer
        ↓
PostgreSQL
        ↓
Transformation
        ↓
Analytics Layer
        ↓
AI Analyst
```

---

## Day 4 Reflection

The main lesson from Day 4 was that implementing a pipeline is different from designing one.

The conceptual model looked correct on paper, but the first real ingestion immediately exposed an operational concern:

> What happens when the same data is loaded more than once?

This is an example of why data engineering requires both:

* Data modeling
* Operational thinking

A pipeline is not complete simply because it can load data once.

It should also be observable, repeatable, and safe to retry.

---

## Day 4 Status

**Docker Environment: Completed**

**PostgreSQL Setup: Completed**

**Database Schemas: Completed**

**Physical Data Model: Completed**

**Raw Table: Completed**

**Sample Ingestion: Completed**

**Ingestion Validation: In Progress**

**Idempotent Ingestion: Next Step**

**Transformation: Not Started**
