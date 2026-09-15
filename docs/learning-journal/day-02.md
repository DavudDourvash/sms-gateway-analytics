# Day 2 — Learning Journal

## Purpose

Day 2 focused on **Data Profiling**.

The objective was to understand the actual structure, grain, volume, and quality of the real dataset before finalizing the analytical data model.

This day was particularly important because several assumptions from Day 1 could now be tested against real data.

---

# Data Modeling

## What I Learned

Data modeling should begin with understanding the **grain** of the data.

Before deciding what a Fact Table or Dimension Table should look like, we need to know:

> What does one row represent?

The grain determines what can be stored, measured, aggregated, and related in the analytical model.

## Application in This Project

The raw dataset was profiled to determine its logical grain.

The observed grain is:

```text
Geographic Square
        +
Time Interval
        +
Country Code
        ↓
Activity Measurements
```

The dataset contains several telecommunications activity measures, including SMS, calls, and Internet activity.

The current analytical scope is limited to SMS activity.

## Evidence

* `docs/data-profiling.md`
* `src/profiling/profile_sms_data.py`
* `src/profiling/profile_sms_data.ipynb`

## Status

**Applied**

The grain has been identified, but its final implementation in the analytical model will be completed during Day 3.

---

# Data Quality

## What I Learned

Data quality should be measured and observed rather than assumed.

Important checks include:

* Completeness
* Uniqueness
* Validity
* Consistency
* Range validation
* Cardinality
* Temporal consistency

## Application in This Project

The full daily dataset was profiled.

Key results:

```text
Rows:                 4,842,625
Geographic Squares:   10,000
Country Codes:        246
Time Intervals:       144
Duplicate Records:    0
Negative Values:      0
```

Missing values were also measured for every field.

## Evidence

* `docs/data-profiling.md`
* `src/profiling/profile_sms_data.py`

## Status

**Applied**

---

# Data Grain

## What I Learned

Grain is one of the most important concepts in analytical data modeling.

A clear grain prevents ambiguity about what each record represents and helps determine the correct Fact Table design.

## Application in This Project

The profiling process showed that the logical record is associated with:

```text
square_id
+
time_interval
+
country_code
```

The project therefore currently treats:

> Geographic Square + Time Interval + Country Code

as the observed logical grain.

No duplicate combinations were detected in the profiled file.

## Evidence

* `docs/data-profiling.md`

## Status

**Applied**

---

# Data Volume

## What I Learned

Data volume is an important engineering consideration.

A pipeline that works for a small sample may behave differently when processing millions of rows.

The physical characteristics of the data should therefore influence ingestion and processing strategies.

## Application in This Project

The daily source file contains:

```text
4,842,625 rows
```

and is approximately:

```text
327 MB
```

The profiling process therefore used chunk-based processing instead of assuming the entire file should be loaded into memory at once.

## Evidence

* `src/profiling/profile_sms_data.py`
* `docs/data-profiling.md`

## Status

**Applied**

---

# Batch Processing

## What I Learned

Batch processing is appropriate when data arrives or is handled in groups rather than requiring continuous event-by-event processing.

The processing strategy should match the characteristics and requirements of the data source.

## Application in This Project

The source dataset is organized into daily files.

The initial project therefore uses a batch-oriented approach:

```text
Daily File
    ↓
Python Processing
    ↓
Profiling / Transformation
```

The project will later evaluate incremental processing as the pipeline evolves.

## Evidence

* `docs/architecture.md`
* `src/profiling/profile_sms_data.py`

## Status

**Partially Applied**

The current implementation demonstrates batch processing, while production-style incremental ingestion will be addressed later.

---

# NULL and Missing Data

## What I Learned

A missing value should not automatically be interpreted as zero.

The semantic meaning of missing data must be understood before deciding how it should be represented in an analytical model.

## Application in This Project

The profiling identified substantial missing values in activity measurements.

For example, the raw dataset contains NULL values in:

* `sms_in`
* `sms_out`
* `call_in`
* `call_out`
* `internet`

The project therefore follows:

```text
NULL ≠ 0
```

No automatic conversion is performed at this stage.

The semantic interpretation of these missing values will be considered during the modeling stage.

## Evidence

* `docs/data-profiling.md`

## Status

**Applied**

The profiling decision is complete; the final analytical representation will be decided during modeling.

---

# Data Validation

## What I Learned

Data validation should be part of the pipeline rather than something performed only after a problem occurs.

## Application in This Project

The profiling process included validation of:

* Row counts
* Time range
* Expected number of intervals
* Duplicate logical records
* Negative activity values
* Cardinality
* Missing values

The time structure was also validated.

The dataset contains:

```text
144 intervals per day
10-minute intervals
```

## Evidence

* `docs/data-profiling.md`
* `src/profiling/profile_sms_data.py`

## Status

**Applied**

---

# Data Profiling Before Data Modeling

## What I Learned

Data profiling should precede final data modeling when the source structure and quality are not fully understood.

Profiling can reveal characteristics that invalidate assumptions made during the initial architecture design.

## Application in This Project

The initial Day 1 model suggested:

```text
fact_sms_activity
dim_time
dim_square
dim_country
```

After profiling, we discovered:

* 10,000 geographic squares
* 246 country codes
* 144 time intervals
* Significant missing values
* Multiple activity types in the source
* SMS is only one part of the raw dataset
* No duplicate logical records

Therefore the initial Star Schema remains a hypothesis rather than a finalized design.

## Evidence

* `docs/data-profiling.md`
* `docs/architecture.md`

## Status

**Applied**

The profiling results will directly inform Day 3 Data Modeling.

---

# Day 2 Reflection

The most important lesson from Day 2 was:

> **Do not finalize a Data Model based on assumptions about the data. Profile the real data first.**

The project moved from:

```text
Initial Assumption
       ↓
Real Dataset
       ↓
Data Profiling
       ↓
Observed Characteristics
       ↓
Data Model Review
```

This created a direct connection between the concepts studied in *Fundamentals of Data Engineering* and actual engineering decisions in the project.

---

# Connection to Day 3

The results of Day 2 create the next engineering question:

> How should the observed data grain, dimensions, measures, and quality characteristics influence the final analytical model and architecture?

Day 3 will therefore focus on:

* Data Modeling
* Fact and Dimension design
* Star Schema
* Raw → Staging → Analytics
* NULL handling
* Storage decisions
* Architecture revision
