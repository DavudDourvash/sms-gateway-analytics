# Day 3 — Data Modeling and Analytical Grain

## Purpose

Day 3 focused on turning the results of data profiling into an initial analytical data model.

The main goal was to define the grain, fact table, dimensions, keys, and time-related attributes before implementing the model in PostgreSQL.

---

## Data Grain

### What I learned

The grain defines exactly what one record in a fact table represents.

A correct grain is essential because analytical aggregations depend on it.

### Application in this project

The raw source data was analyzed using:

```text
square_id + time_interval + country_code
```

No duplicate records were found at this logical grain.

Therefore, the analytical grain was defined as:

> One geographic square + one country code + one 10-minute time interval

### Evidence

Validation script:

```text
src/profiling/validate_model_grain.py
```

Validation result:

```text
Duplicate grain records: 0
```

### Status

Completed.

---

## Dimensional Modeling

### What I learned

A dimensional model separates measurable activity from descriptive context.

The central fact table contains measurements, while dimensions provide the context needed to analyze those measurements.

### Application in this project

The initial analytical model was designed as:

```text
                    dim_time
                       |
                       |
dim_square ---- fact_sms_activity ---- dim_country
                       |
                  sms_in / sms_out
```

### Status

Completed.

---

## Fact Table

### What I learned

A fact table represents measurable activity at a defined grain.

### Application in this project

The fact table is:

```text
fact_sms_activity
```

Conceptual attributes:

```text
time_key
square_id
country_code
sms_in
sms_out
```

The two primary measures are:

* `sms_in`
* `sms_out`

The fact table does not duplicate descriptive time attributes because those attributes belong to `dim_time`.

### Status

Completed.

---

## Time Dimension

### What I learned

A time dimension provides reusable descriptive attributes for temporal analysis.

Instead of storing only a raw timestamp, the timestamp can be transformed into analytical attributes such as date, hour, day of week, and weekend status.

### Application in this project

The proposed time dimension is:

```text
dim_time

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

The source contains 10-minute intervals.

For a 62-day period:

```text
62 × 144 = 8,928 timestamps
```

The time dimension is shared across the project rather than rebuilt independently for each source file.

### Status

Completed.

---

## Natural Keys and Surrogate Keys

### What I learned

A Natural Key is an identifier that already exists in the source or business domain.

A Surrogate Key is an artificial identifier introduced by the data model.

Surrogate keys should not be introduced automatically when a stable natural identifier is already suitable.

### Application in this project

The current design uses:

```text
dim_square
    square_id → Natural Key

dim_country
    country_code → Natural Key

dim_time
    time_key → Surrogate Key
```

This keeps the model simple while allowing the time dimension to have its own internal identifier.

### Status

Completed.

---

## NULL Handling

### What I learned

A NULL value and a zero value do not necessarily mean the same thing.

Converting NULL values to zero without understanding their meaning can introduce incorrect analytical conclusions.

### Application in this project

The profiling stage showed many NULL values in `sms_in` and `sms_out`.

Therefore, the current model does not automatically convert NULL to zero.

The current principle is:

```text
NULL ≠ 0
```

The interpretation may be revised later if reliable source documentation confirms the meaning of missing activity values.

### Status

Initial decision completed.

---

## Data Profiling Before Data Modeling

### What I learned

The data model should be based on observed characteristics of the source data rather than assumptions made before inspecting the data.

Important observations from profiling included:

* 10-minute time intervals
* 10,000 geographic squares
* 246 country codes
* No duplicate records at the proposed grain
* Large numbers of NULL activity values
* SMS activity as the current analytical scope

### Application in this project

The data model was defined after profiling the real source file.

This allowed the initial model to be based on actual source characteristics.

### Status

Completed.

---

## Day 3 Reflection

The main lesson from Day 3 was that data modeling should follow data understanding.

The process used was:

```text
Raw Data
    ↓
Profiling
    ↓
Grain Validation
    ↓
Data Model
    ↓
Implementation
```

The analytical model is intentionally simple and remains open to revision as more source files are ingested and additional requirements are discovered.

---

## Day 3 Status

**Conceptual Data Model: Completed**

**Grain Validation: Completed**

**Implementation: Not Started**

**PostgreSQL Schema: Next Stage**
