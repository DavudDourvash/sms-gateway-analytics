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

### Day 1 — Project Definition & Architecture ✅

* Business problem defined
* Project scope defined
* Real-world dataset selected
* Initial architecture defined
* Processing strategy defined
* Development strategy defined
* Initial data model proposed
* Architecture principles documented

### Day 2 — Data Profiling ✅

* Real dataset downloaded and inspected
* Source schema identified
* Data grain investigated
* Data volume measured
* Time structure validated
* Missing values analyzed
* Duplicate records checked
* Cardinality analyzed
* Data quality checks performed
* SMS activity distribution analyzed
* Profiling results documented

### Day 3 — Data Modeling & Grain Validation ✅

* Analytical grain defined
* Proposed grain validated against real data
* Fact table designed
* Dimension tables designed
* Star-schema-oriented model defined
* Time dimension designed
* Natural and surrogate key strategy defined
* NULL handling strategy documented
* Data model documentation completed
* Learning journal updated

Key evidence:

```text
docs/data-model.md
docs/learning-journal/day-03.md
src/profiling/validate_model_grain.py
src/profiling/validate_model_grain.ipynb
```

### Day 4 — PostgreSQL Implementation 🔜

The next stage will transform the conceptual model into a working analytical database.

Planned activities:

* Set up PostgreSQL
* Create the analytical schema
* Define physical table structures
* Define data types and constraints
* Load initial data
* Validate loaded data against the source
* Test analytical queries
* Document implementation decisions

**Day 4 has not started yet.**

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
