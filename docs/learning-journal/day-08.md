# Day 8 — Building the First Analytics Layer

## Session Goal

Build the first working analytical dataset by transforming raw telecommunications activity data into a dimensional model in PostgreSQL, then run an initial SQL analysis.

## 1. Review of the Existing Architecture

The project follows this pipeline:

```text
Public Telecom Dataset
        ↓
Python Ingestion
        ↓
PostgreSQL Raw Layer
        ↓
SQL Transformation
        ↓
Analytics Layer
        ↓
SQL Analytics
        ↓
AI Analyst
```

The raw data is stored separately from analytical tables.

Existing PostgreSQL schemas:

- `raw`
- `analytics`

Existing analytical tables:

- `analytics.dim_time`
- `analytics.dim_square`
- `analytics.dim_country`
- `analytics.fact_sms_activity`

## 2. Raw Data Inspection

The raw table was inspected before starting the transformation.

```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT (square_id, time_interval, country_code))
        AS unique_records,
    COUNT(sms_in) AS sms_in_non_null,
    COUNT(sms_out) AS sms_out_non_null
FROM raw.telecom_activity_raw;
```

Results:

| Metric | Result |
|---|---:|
| Total raw rows | 300,000 |
| Unique logical records | 100,000 |
| Non-null `sms_in` | 198,870 |
| Non-null `sms_out` | 113,979 |

The raw table contained three copies of the 100,000-row sample previously loaded during testing.

This duplication was acknowledged but not fully corrected during this session.

## 3. Populating Dimension Tables

### Geographic dimension

```sql
INSERT INTO analytics.dim_square (square_id)
SELECT DISTINCT square_id
FROM raw.telecom_activity_raw
ON CONFLICT (square_id) DO NOTHING;
```

Result: 255 geographic squares.

### Country dimension

```sql
INSERT INTO analytics.dim_country (country_code)
SELECT DISTINCT country_code
FROM raw.telecom_activity_raw
ON CONFLICT (country_code) DO NOTHING;
```

Result: 111 country codes.

### Time dimension

Unique timestamps were extracted from the raw Unix timestamps, which are stored in milliseconds.

The conversion used:

```sql
TO_TIMESTAMP(time_interval / 1000.0)
    AT TIME ZONE 'UTC'
```

The transformation populated the time attributes:

- Timestamp
- Date
- Year and month
- Hour and minute
- Day of week
- Day name
- Weekend indicator

Result: 144 unique time intervals, corresponding to one day of 10-minute intervals.

## 4. Populating the Fact Table

The first analytical load inserted 100,000 rows into `analytics.fact_sms_activity`.

The transformation:

1. Selected distinct combinations of the source dimensions and SMS measures.
2. Joined the source data to `dim_time`, `dim_square`, and `dim_country`.
3. Retrieved the corresponding `time_key`.
4. Inserted the resulting records into the fact table.

The following SQL patterns were used:

- `SELECT DISTINCT` to remove identical source rows in this sample.
- `JOIN` to connect facts to dimensions.
- `ON CONFLICT DO NOTHING` to avoid primary-key conflicts.

PostgreSQL confirmed:

```text
INSERT 0 100000
```

The fact table was initially empty, so this was the first analytical load.

## 5. First SQL Analysis: Activity by Hour

The first analytical query aggregated SMS activity by hour.

```sql
SELECT
    dt.hour,
    SUM(f.sms_in) AS total_sms_in,
    SUM(f.sms_out) AS total_sms_out,
    COUNT(*) AS record_count
FROM analytics.fact_sms_activity AS f
JOIN analytics.dim_time AS dt
    ON dt.time_key = f.time_key
GROUP BY dt.hour
ORDER BY dt.hour;
```

### Initial observations

- The highest observed `sms_in` total occurred at hour 9, at approximately 2,662.48.
- The highest observed `sms_out` total occurred at hour 10, at approximately 1,272.38.
- The lowest observed `sms_in` total occurred at hour 4, at approximately 99.78.
- Activity increased substantially during the morning hours in this sample.

These are descriptive observations about the sampled public telecommunications activity data. They do not establish SMS delivery quality or the operational performance of a commercial SMS gateway.

The source values are aggregated activity measurements and should not automatically be interpreted as actual commercial message counts.

## 6. Final Validation

The following query was used to validate the analytical dataset:

```sql
SELECT
    COUNT(*) AS fact_rows,
    COUNT(DISTINCT time_key) AS time_intervals,
    COUNT(DISTINCT square_id) AS squares,
    COUNT(DISTINCT country_code) AS countries,
    COUNT(*) FILTER (WHERE sms_in IS NULL) AS missing_sms_in,
    COUNT(*) FILTER (WHERE sms_out IS NULL) AS missing_sms_out
FROM analytics.fact_sms_activity;
```

Results:

| Metric | Result |
|---|---:|
| Fact rows | 100,000 |
| Time intervals | 144 |
| Geographic squares | 255 |
| Country codes | 111 |
| Missing `sms_in` | 33,710 |
| Missing `sms_out` | 62,007 |

The missing-value counts match the earlier profile of the 100,000-row sample.

Missing values were preserved as SQL `NULL` rather than converted to zero.

## 7. Key Concepts Learned

### Dimensional modeling

Dimension tables provide descriptive context, while fact tables store measurable activity at a defined grain.

### SQL joins

Foreign-key relationships and joins connect the fact table to the appropriate dimension records.

### Aggregation

`SUM`, `COUNT`, and `GROUP BY` transform detailed records into analytical results.

### Data quality

Row counts, dimension coverage, and missing-value checks help validate the output of a transformation pipeline.

### Source scope versus analytical scope

The source contains SMS, calls, and Internet activity, but the current analytical scope remains focused on SMS activity.

The dataset does not provide commercial customer records, delivery statuses, pricing, revenue, or provider contracts.

## 8. Technical Debt and Limitations

The following items are intentionally deferred to prioritize end-to-end progress:

- The raw table still contains duplicate copies of the sample.
- `DISTINCT` is a temporary approach for this sample, not a complete conflict-resolution policy.
- Transactional ingestion and ingestion-log registration are not yet atomic.
- The pipeline has not yet been tested against the complete 62-day dataset.
- The time-zone interpretation must remain consistent across future transformations.
- Additional analytical views and automated data-quality checks have not yet been implemented.

These limitations should be addressed when they become necessary for the next project milestones.

## 9. Day 8 Outcome

Completed:

- Inspected the existing raw dataset.
- Populated geographic, country, and time dimensions.
- Loaded 100,000 records into the fact table.
- Ran the first hourly SMS activity analysis.
- Validated the fact table and missing-value counts.

The project now has a working initial path from raw data to SQL analytics.

## Next Session — Day 9

Focus on practical SQL analytics:

1. Analyze SMS activity trends over time.
2. Compare inbound and outbound activity.
3. Identify high-activity geographic squares.
4. Prepare reusable analytical queries for the future AI Analyst.

**Day 9 objective:** Produce useful analytical outputs rather than spend additional time on low-priority infrastructure details.
