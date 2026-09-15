# Data Model

## Modeling Objective

The purpose of the data model is to transform the raw telecommunications activity data into a structured analytical model focused on SMS activity.

The model is designed to support questions such as:

* How does SMS traffic change over time?
* Which geographic areas have higher SMS activity?
* How does SMS activity vary by country?
* When do unusual traffic patterns occur?
* How can analytical results later be exposed to an AI analyst?

The model is intentionally simple in its first version and may evolve as the project develops.

---

## Source Data vs. Analytical Scope

The source dataset contains several types of telecommunications activity:

* SMS-in
* SMS-out
* Call-in
* Call-out
* Internet

The current analytical scope is limited to:

* `sms_in`
* `sms_out`

Call and Internet activity remain in the raw source layer but are outside the current analytical model.

This distinction is intentional:

> **Source Data Scope ≠ Analytical Scope**

---

## Observed Data Grain

Based on the profiling performed during Day 2, each logical record represents activity associated with:

* One geographic square
* One country code
* One 10-minute time interval

Therefore, the analytical grain is:

> **One geographic square + one country code + one 10-minute time interval**

Conceptually:

```text
Geographic Square
        +
Country Code
        +
10-Minute Time Interval
        ↓
One SMS Activity Record
```

This grain is the foundation of the `fact_sms_activity` table.

---

## Initial Star Schema

The initial analytical model follows a Star Schema:

```text
                         dim_time
                            |
                            |
                            |
dim_square -------- fact_sms_activity -------- dim_country
                         /       \
                        /         \
                   sms_in       sms_out
```

The central fact table contains measurable SMS activity, while dimension tables provide the context required for analysis.

---

## Fact Table

### fact_sms_activity

The fact table stores SMS activity measurements at the defined analytical grain.

Conceptual structure:

| Column      | Role        | Description                       |
| ----------- | ----------- | --------------------------------- |
| activity_id | Key         | Surrogate identifier, if required |
| time_key    | Foreign Key | Reference to `dim_time`           |
| square_key  | Foreign Key | Reference to `dim_square`         |
| country_key | Foreign Key | Reference to `dim_country`        |
| sms_in      | Measure     | Incoming SMS activity             |
| sms_out     | Measure     | Outgoing SMS activity             |

The final physical implementation of keys will be determined during PostgreSQL implementation.

---

## Dimension Tables

### dim_time

The time dimension provides attributes for temporal analysis.

Initial conceptual structure:

| Column      | Description         |
| ----------- | ------------------- |
| time_key    | Dimension key       |
| timestamp   | Original time value |
| date        | Calendar date       |
| hour        | Hour of day         |
| minute      | Minute              |
| day_of_week | Day of week         |
| day_name    | Day name            |

This dimension will allow analysis such as:

* SMS activity by hour
* SMS activity by day
* Peak traffic periods
* Weekday vs. weekend patterns
* Temporal anomaly detection

---

### dim_square

The square dimension represents the geographic grid square from the source dataset.

Initial conceptual structure:

| Column     | Description                |
| ---------- | -------------------------- |
| square_key | Dimension key              |
| square_id  | Original source identifier |

At this stage, no additional geographic attributes are invented.

If a reliable mapping between `square_id` and geographic information becomes available, the dimension may be extended in a future version.

---

### dim_country

The country dimension represents the country code associated with the activity.

Initial conceptual structure:

| Column       | Description                  |
| ------------ | ---------------------------- |
| country_key  | Dimension key                |
| country_code | Original source country code |

A country-name mapping may be added later if a reliable source is identified.

The project will not infer or fabricate country names from the raw data.

---

## Keys

The profiling results from Day 2 showed no duplicate logical records for the combination:

```text
square_id
+
time_interval
+
country_code
```

Therefore, this combination is currently treated as the logical/natural key of the source activity record.

```text
(square_id, time_interval, country_code)
```

The physical database implementation may use surrogate keys for dimensions and/or the fact table.

The final key strategy will be decided during PostgreSQL implementation.

---

## Grain Validation

The proposed analytical grain was validated against the raw source data using the combination:

```text
square_id
+
time_interval
+
country_code
```

A dedicated validation script was used to check whether multiple records exist for the same logical grain.

Validation result:

```text
Duplicate grain records: 0
```

Therefore, for the profiled source file, no duplicate records were found at the proposed analytical grain.

This provides evidence that:

> **One geographic square + one country code + one 10-minute time interval**

can currently be treated as the logical grain of `fact_sms_activity`.

The validation script is located at:

```text
src/profiling/validate_model_grain.py
```

This validation is based on the currently profiled source data. It should be repeated when additional source files are ingested.



## Measures

The current analytical model contains two primary measures:

### sms_in

Represents incoming SMS activity.

### sms_out

Represents outgoing SMS activity.

These measures are retained from the source data without inventing additional business metrics.

Future derived metrics may include:

* Total SMS activity
* Incoming/outgoing ratio
* Traffic growth rate
* Moving averages
* Anomaly scores

Derived metrics will be created in the analytical layer rather than altering the meaning of the raw source fields.

---

## NULL Handling

The profiling stage identified a significant number of NULL values in the activity columns.

NULL values will **not** automatically be converted to zero.

This distinction is important:

```text
NULL ≠ 0
```

For example:

```text
sms_out = 0
```

means the value is explicitly zero.

Whereas:

```text
sms_out = NULL
```

means that no value is available in the source representation.

Any conversion from NULL to zero must be based on an explicit data rule and validated against the meaning of the source data.

Until such a rule is established, the distinction will be preserved.

---

## Modeling Decisions

The following decisions were made based on the Day 2 profiling results:

### 1. Use a Star Schema

A Star Schema is selected as the initial analytical model because the current use cases are primarily analytical and involve measurable activity across time, geography, and country.

### 2. Keep the Fact Table at the Observed Grain

The fact table will not aggregate the data beyond the observed source grain during initial modeling.

```text
One square
+
One country
+
One 10-minute interval
```

### 3. Focus the Analytical Model on SMS

Although the source contains calls and Internet activity, the current project focuses on SMS analytics.

### 4. Preserve Raw Data Separately

The raw source will remain separate from the analytical model.

The transformation flow is:

```text
Raw Data
    ↓
Staging / Cleaning
    ↓
Analytical Model
    ↓
fact_sms_activity
    +
Dimensions
```

### 5. Do Not Invent Business Entities

The source does not provide commercial gateway information such as:

* Customer accounts
* Message delivery status
* Pricing
* Revenue
* Provider contracts
* Campaign information

These entities will not be fabricated in the analytical model.

If such capabilities are added in the future, their data source and assumptions will be explicitly documented.

---

## Open Questions

The following decisions remain open and will be resolved as the project evolves:

* Should the fact table use a surrogate `activity_id`?
* Should the natural key also be enforced as a database constraint?
* Should `dim_time` contain every 10-minute interval or only intervals present in the source?
* How should `country_code = 0` be represented?
* Is there a reliable mapping from `square_id` to geographic coordinates or regions?
* Should NULL activity values remain NULL throughout the analytical layer?
* What indexes will be required for analytical queries?
* How should the model evolve when multiple daily source files are ingested?

These questions are intentionally left open rather than being decided prematurely.

---

## Current Model Status

**Status: Initial analytical model defined**

The first version of the data model is based on:

* Real source data profiling
* Observed data grain
* Current analytical requirements
* SMS-focused project scope

The model will be validated and refined during the PostgreSQL and transformation stages.

> **Model first, implementation second — but keep the model reversible.**
