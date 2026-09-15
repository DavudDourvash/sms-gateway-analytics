# Data Model

## Modeling Objective

The goal of the analytical data model is to transform the raw telecommunications activity data into a structured model suitable for analytical queries, BI dashboards, and future AI-assisted analysis.

The current analytical scope is limited to SMS activity.

---

## Source Data vs. Analytical Scope

The raw source dataset contains multiple types of telecommunications activity:

* SMS-in activity
* SMS-out activity
* Call-in activity
* Call-out activity
* Internet activity

The **analytical scope of this project is currently limited to SMS activity**.

Therefore:

* The raw dataset is treated as a broader Telecommunications Activity source.
* SMS-in and SMS-out are the primary measures in the current analytical layer.
* Call and Internet activity are retained in the raw source but are outside the current analytical scope.
* No commercial SMS Gateway entities such as customers, pricing, revenue, delivery status, or provider contracts are inferred from this dataset.

This distinction is intentional:

> **Source Data Scope ≠ Analytical Scope**

---

## Observed Data Grain

Based on profiling of the real source data, each logical record represents telecommunications activity associated with:

* A geographic grid square
* A country code
* A 10-minute time interval

Therefore, the proposed analytical grain is:

> **One geographic square + one country code + one 10-minute time interval**

Conceptually:

```text
Geographic Square
        +
Country Code
        +
10-Minute Time Interval
        ↓
One Fact Record
        ↓
SMS Measurements
```

---

## Grain Validation

The proposed analytical grain was validated against the raw source data using the combination:

```text
square_id + time_interval + country_code
```

A dedicated validation script was used to check whether duplicate records existed at this logical grain.

Validation result:

```text
Duplicate grain records: 0
```

Therefore, for the profiled source file, no duplicate records were found at the proposed analytical grain.

This provides evidence that:

> One geographic square + one country code + one 10-minute time interval

can currently be treated as the logical grain of `fact_sms_activity`.

The validation script is located at:

```text
src/profiling/validate_model_grain.py
```

This validation is based on the currently profiled source data and should be repeated when additional source files are ingested.

---

## Initial Star Schema

The analytical model follows a simple star-schema-oriented design:

```text
                    dim_time
                       |
                       | time_key
                       |
                       v
dim_square ---- fact_sms_activity ---- dim_country
                       |
                  +----+----+
                  |         |
               sms_in    sms_out
```

The model consists of:

* One central fact table
* Three dimensions
* Two primary SMS measures

---

## Fact Table

### fact_sms_activity

The fact table stores SMS activity measurements at the defined analytical grain.

Conceptual structure:

```text
fact_sms_activity
------------------
time_key
square_id
country_code
sms_in
sms_out
```

### Grain

Each row represents:

> One geographic square + one country code + one 10-minute time interval

### Measures

The current measures are:

* `sms_in`
* `sms_out`

These measures represent the SMS activity recorded by the source for the corresponding grain.

---

## Dimension Tables

### dim_time

The time dimension provides descriptive and analytical attributes for each actual timestamp.

Conceptual structure:

```text
dim_time
--------
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

The time dimension contains one record per actual 10-minute timestamp rather than one record per time-of-day.

For the 62-day source period:

```text
62 days × 144 intervals per day = 8,928 timestamps
```

Time attributes are derived from the source `time_interval` value during transformation.

New source files should reuse existing timestamps and add only timestamps that do not already exist in `dim_time`.

---

### dim_square

The square dimension represents the geographic grid identifiers present in the source data.

Conceptual structure:

```text
dim_square
----------
square_id
```

`square_id` is currently treated as a **Natural Key** because it is a meaningful identifier provided directly by the source.

The same square should not be duplicated when it appears in multiple source files.

---

### dim_country

The country dimension represents the country codes present in the source data.

Conceptual structure:

```text
dim_country
-----------
country_code
```

`country_code` is currently treated as a **Natural Key** because it is a meaningful identifier provided directly by the source.

The same country code should be represented by one unique dimension record across the project.

---

## Keys

The current key strategy is:

| Table         | Key            | Type          |
| ------------- | -------------- | ------------- |
| `dim_time`    | `time_key`     | Surrogate Key |
| `dim_square`  | `square_id`    | Natural Key   |
| `dim_country` | `country_code` | Natural Key   |

The logical grain of the fact table is represented by:

```text
time_key + square_id + country_code
```

Surrogate keys are not introduced where the source already provides a suitable stable natural identifier.

---

## NULL Handling

The profiling stage showed a significant number of NULL values in activity measurements.

For example, the source contains NULL values for both `sms_in` and `sms_out`.

A NULL value is **not automatically interpreted as zero**.

Therefore:

> **NULL ≠ 0**

The current model preserves this distinction.

NULL handling may be revised later if reliable source documentation or additional validation establishes that a missing activity value explicitly represents zero activity.

---

## Modeling Decisions

The following decisions have been made based on the current profiling and modeling analysis:

1. The analytical scope is limited to SMS activity.
2. The fact table is `fact_sms_activity`.
3. The dimensions are `dim_time`, `dim_square`, and `dim_country`.
4. The fact grain is one square + one country + one 10-minute interval.
5. `sms_in` and `sms_out` are the current measures.
6. `square_id` is used as a Natural Key.
7. `country_code` is used as a Natural Key.
8. `time_key` is used as a Surrogate Key for the time dimension.
9. Time attributes are maintained in `dim_time` rather than duplicated in the fact table.
10. Dimension records are reusable across source files.
11. NULL values are not automatically converted to zero.
12. Grain validation must be repeated when additional source files are ingested.

---

## Open Questions

The following implementation decisions remain open and will be addressed during later stages:

* Physical PostgreSQL data types
* Exact PostgreSQL table definitions
* Indexing strategy
* Partitioning strategy, if required
* Incremental ingestion implementation
* Handling of new dimension values during ingestion
* Production data-quality checks
* Whether additional source activity types should be modeled in future versions

These decisions are intentionally deferred until the implementation and ingestion stages.

---

## Current Model Status

The conceptual analytical model has been defined and validated against the currently profiled source data.

The next stage is implementation:

```text
Raw Source
    ↓
Transformation
    ↓
PostgreSQL
    ↓
fact_sms_activity
    +
dim_time
    +
dim_square
    +
dim_country
```

The model remains intentionally simple and can evolve as additional data and requirements are introduced.
