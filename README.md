# SMS Gateway Analytics & AI Agent

## Project Overview

This project explores how real-world telecommunications activity data can be transformed into reliable analytics and, eventually, an evidence-based AI analytical assistant.

The primary goal is to learn **Data Engineering fundamentals through a real-world problem**, rather than building an isolated tutorial project.

The project follows an incremental approach:

**Fundamentals → Data Understanding → Modeling → Implementation → Automation/Cloud → AI Analyst**

---

## Objectives

* Build a reliable real-world data ingestion pipeline
* Understand data grain, schema, volume, and data quality
* Apply dimensional modeling and analytical data design
* Build reliable analytics for SMS traffic
* Identify temporal, geographic, and operational patterns
* Introduce automation and cloud infrastructure gradually
* Build an evidence-based AI analyst that can query and explain analytical results

---

## Data Source

The initial version uses the **Telecom Italia real-world telecommunications activity dataset**.

The source contains multiple types of telecommunications activity:

* SMS-in
* SMS-out
* Call-in
* Call-out
* Internet

The current analytical scope is limited to **SMS activity**.

Commercial SMS Gateway entities such as customers, pricing, revenue, delivery status, campaigns, and provider contracts are **outside the current scope**, because equivalent public real-world data is not available.

This distinction is intentional:

> **Source Data Scope ≠ Analytical Scope**

---

## Data Profiling

Day 2 focused on understanding the real structure and quality of the source data before finalizing the analytical model.

Key findings from the profiled daily dataset:

* **4,842,625 rows**
* **10,000 geographic squares**
* **246 country codes**
* **144 time intervals per day**
* **10-minute time intervals**
* No duplicate logical records detected
* No negative activity values detected
* Significant missing values exist in activity measurements
* SMS activity distributions are strongly right-skewed

The observed logical grain is:

**Geographic Square + Time Interval + Country Code**

Detailed profiling results are documented in:

`docs/data-profiling.md`

---

## Data Model

Day 3 transformed the profiling results into an initial analytical data model.

The project currently follows a **star-schema-oriented design**:

```text
                    dim_time
                       |
                       | time_key
                       v
dim_square ---- fact_sms_activity ---- dim_country
                       |
                  +----+----+
                  |         |
               sms_in    sms_out
```

### Fact Table

`fact_sms_activity`

```text
time_key
square_id
country_code
sms_in
sms_out
```

### Dimensions

`dim_time`

```text
time_key
timestamp
date
year
month
hour
minute
day_of_week
day_name
is_weekend
```

`dim_square`

```text
square_id
```

`dim_country`

```text
country_code
```

### Analytical Grain

Each fact record represents:

> **One geographic square + one country code + one 10-minute time interval**

The proposed grain was validated against the profiled source data.

**Duplicate grain records: 0**

Validation script:

`src/profiling/validate_model_grain.py`

### Key Strategy

The current model uses:

* `square_id` as a Natural Key
* `country_code` as a Natural Key
* `time_key` as a Surrogate Key for the time dimension

### NULL Handling

The project currently preserves the distinction between missing and zero values:

> **NULL ≠ 0**

Missing activity values are not automatically converted to zero unless their meaning is established through reliable source documentation or further validation.

Detailed modeling decisions are documented in:

`docs/data-model.md`

---

## Architecture

The current conceptual architecture is:

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

The architecture is intentionally incremental.

The project starts with local processing and will gradually evolve toward:

**Local → Docker → Cloud → Automation/Orchestration → AI Analyst**

New technologies will be introduced only when they solve a demonstrated engineering problem.

Detailed architecture decisions are documented in:

`docs/architecture.md`

---

## Project Status

### Day 1 — Project Foundation

**Completed**

* Business problem defined
* Project scope defined
* Real-world public data source selected
* Initial architecture designed
* Batch and incremental processing strategy defined
* Local-first development strategy defined

### Day 2 — Data Profiling

**Completed**

* Real source file downloaded and inspected
* Source schema identified
* 10-minute time interval structure validated
* Missing values profiled
* Cardinality analyzed
* Duplicate logical records checked
* SMS distributions analyzed
* Full-file profiling completed

Key findings:

* 4,842,625 rows in the profiled daily source file
* 10,000 geographic squares
* 246 country codes
* 144 ten-minute intervals per day
* No duplicate records at the proposed logical grain
* Significant NULL values in activity measures
* SMS-in and SMS-out selected as the current analytical scope

### Day 3 — Data Modeling & Grain Validation

**Completed**

* Analytical grain defined
* Star-schema-oriented model designed
* `fact_sms_activity` defined
* `dim_time` defined
* `dim_square` defined
* `dim_country` defined
* Natural and surrogate key strategy defined
* NULL handling strategy defined
* Grain validation script implemented

Analytical grain:

```text
One geographic square
+
One country code
+
One 10-minute time interval
```

### Day 4 — Docker, PostgreSQL & Raw Ingestion

**Completed / In Progress**

* Docker Desktop configured
* WSL2 environment configured
* PostgreSQL 16 running in Docker
* PostgreSQL database created
* `raw` and `analytics` schemas created
* Analytical tables created
* Raw table created
* `sample_100k.txt` copied into the PostgreSQL container
* First PostgreSQL `COPY` ingestion completed successfully
* Raw ingestion validation started
* Repeated sample loading revealed an idempotency concern

Current database structure:

```text
sms_gateway_analytics
│
├── raw
│   └── telecom_activity_raw
│
└── analytics
    ├── dim_square
    ├── dim_country
    ├── dim_time
    └── fact_sms_activity
```

### Next Step

The next stage is to validate the current Raw Layer before continuing:

```text
Total Rows
    vs.
Distinct Analytical Grain
```

Then:

```text
Raw Data
   ↓
Transformation
   ↓
Dimensions
   ↓
Fact Table
```

The project will first establish a reliable local ingestion and transformation pipeline before introducing additional complexity such as orchestration, cloud infrastructure, or the AI Analyst.

---

## Current Learning Path

```text
Fundamentals of Data Engineering
             ↓
Project Application
             ↓
Data Profiling
             ↓
Data Modeling
             ↓
Docker + PostgreSQL
             ↓
Data Ingestion
             ↓
Transformation
             ↓
Data Quality
             ↓
Incremental Processing
             ↓
Analytics
             ↓
Cloud
             ↓
AI Analyst
```

## Engineering Principles

The project follows these principles:

1. Understand the data before finalizing the model.
2. Keep raw data separate from analytical data.
3. Prefer simple architecture before adding infrastructure.
4. Make ingestion repeatable and observable.
5. Validate data quality at every important stage.
6. Design pipelines to handle retries safely.
7. Keep architectural decisions reversible when possible.
8. Add cloud, orchestration, and AI only when they solve a demonstrated problem.
9. Never fabricate unavailable business data.
10. Build the project incrementally from local development toward production-like architecture.

## Learning Journal

The project documents the connection between the book concepts and their practical implementation.

```text
docs/
├── learning-map.md
└── learning-journal/
    ├── day-01.md
    ├── day-02.md
    ├── day-03.md
    └── day-04.md
```

Each journal entry records:

* What was learned
* How the concept was applied
* Evidence from the project
* Current implementation status
* Open engineering questions

---

## Repository Structure

```text
sms-gateway-analytics/
│
├── data/                         # Local datasets (not tracked by Git)
│
├── docs/
│   ├── project-scope.md
│   ├── data-source.md
│   ├── architecture.md
│   ├── data-profiling.md
│   ├── data-model.md
│   │
│   └── learning-journal/
│       └── day-03.md
│
├── src/
│   └── profiling/
│       ├── profile_sms_data.py
│       ├── profile_sms_data.ipynb
│       ├── validate_model_grain.py
│       └── validate_model_grain.ipynb
│
├── .gitignore
└── README.md
```

---

## Engineering Principles

This project follows several principles:

1. **Understand the data before finalizing the model.**
2. **Preserve raw data before transformation.**
3. **Define and validate data grain before analytical implementation.**
4. **Prefer simple architecture over premature complexity.**
5. **Make data quality observable and testable.**
6. **Keep architectural decisions reversible where possible.**
7. **Introduce new technologies only when they solve a demonstrated problem.**
8. **Never fabricate unavailable business data.**
9. **Separate source-data scope from analytical scope.**
10. **Build incrementally toward production-like architecture.**

---

## Learning Journal

The project is also used as a practical implementation of concepts studied in:

**Fundamentals of Data Engineering**

The learning journal connects data engineering concepts to concrete project decisions, documentation, validation, and code.

```text
docs/
└── learning-journal/
    └── day-03.md
```

The journal will evolve as the project progresses.

---

## Current Learning Path

```text
Business Problem
       ↓
Data Requirements
       ↓
Real Data
       ↓
Data Profiling
       ↓
Data Modeling
       ↓
PostgreSQL Implementation    ← Day 4
       ↓
Data Transformation
       ↓
Analytics
       ↓
Automation / Cloud
       ↓
AI Analyst
```

---

## Project Philosophy

This is not intended to be a collection of disconnected technologies.

The goal is to demonstrate the ability to move from:

**Problem → Data → Understanding → Model → Pipeline → Analytics → AI**

while making engineering decisions based on evidence from the data rather than assumptions.
