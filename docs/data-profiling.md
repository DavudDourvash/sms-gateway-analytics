# Data Profiling

## 1. Profiling Objective

The purpose of this profiling stage is to understand the real structure, grain, volume, time characteristics, cardinality, missingness, and basic data quality of the Telecom Italia telecommunications activity dataset before finalizing the storage model and analytical data model.

The profiling was performed on the full daily dataset for 2013-11-01.

The analysis intentionally precedes final data modeling to avoid designing the analytical schema based on assumptions rather than observed data.

---

## 2. Dataset Overview

The source file contains aggregated telecommunications activity across geographic grid squares and time intervals.

The raw source contains the following activity types:

- SMS-in
- SMS-out
- Call-in
- Call-out
- Internet traffic

The current project analytical scope is limited to SMS activity.

Therefore:

> Source Data Scope ≠ Analytical Scope

The raw dataset is broader than the current analytical model.

---

## 3. Logical Schema

The source contains eight logical fields:

| Column | Description | Observed Type |
|---|---|---|
| square_id | Geographic grid square identifier | Integer |
| time_interval | Unix timestamp in milliseconds | Integer |
| country_code | Country/source code associated with the activity | Integer |
| sms_in | Incoming SMS activity | Float |
| sms_out | Outgoing SMS activity | Float |
| call_in | Incoming call activity | Float |
| call_out | Outgoing call activity | Float |
| internet | Internet traffic activity | Float |

The raw file does not contain a header row.

Missing activity fields are represented as empty values in the source file.

---

## 4. Data Grain

The observed logical grain is:

> One row represents telecommunications activity associated with one geographic square, one 10-minute time interval, and one country code.

Conceptually:

```text
Geographic Square
        +
Time Interval
        +
Country Code
        ↓
Activity Measurements