# Data Source

## Primary Source

Telecom Italia Big Data Challenge — Telecommunications Activity Dataset.

The dataset contains real-world aggregated telecommunications activity from the Telecom Italia cellular network.

## Source

Harvard Dataverse

Dataset:
Telecommunications - SMS, Call, Internet - MI

DOI:
10.7910/DVN/EGZHFV

Source Data vs. Analytical Scope

The raw source dataset contains multiple types of telecommunications activity:

SMS-in activity
SMS-out activity
Call-in activity
Call-out activity
Internet activity

The analytical scope of this project is currently limited to SMS activity.

Therefore:

The raw dataset is treated as a broader Telecommunications Activity source.
SMS-in and SMS-out are the primary metrics for the current analytical layer.
Call and Internet activity are retained in the raw source but are outside the current analytical scope.
No commercial SMS Gateway entities such as customers, pricing, revenue, delivery status, or provider contracts are inferred from this dataset.

This distinction is intentional:

Source Data Scope ≠ Analytical Scope

The project may expand to other activity types in future versions if they provide a meaningful analytical or engineering use case.
## Data Dimensions

The SMS activity data provides information across:

- Geographic grid cells
- Time intervals
- Country codes
- SMS-in activity
- SMS-out activity

The activity is aggregated into spatial and temporal units rather than exposing individual users.

## Why This Dataset?

The dataset provides real-world telecom activity and allows the project to explore:

- Large-scale data processing
- Time-series analytics
- Spatial analytics
- Data modeling
- Data quality
- Data engineering
- Operational analytics

## Data Grain

Each logical record represents telecommunications activity associated with:

* A geographic grid square
* A time interval
* A country code

The time dimension is based on 10-minute intervals.

Conceptually:

```text
Geographic Square
        +
Time Interval
        +
Country Code
        ↓
Activity Measurements
```

The raw record may contain activity measurements for SMS, calls, and Internet. Missing activity values may result in fewer populated fields in the raw representation.

The current analytical layer will extract and model the SMS-related measurements from these records.


## Limitations

The dataset does not provide commercial SMS Gateway information such as:

- Customer accounts
- Pricing
- Revenue
- Provider contracts
- Delivery status
- Campaign information

These entities will not be fabricated and may be introduced only in later stages using clearly documented sources or simulated operational data.

## Current Status

Data source selected.

Initial analytical scope:
SMS activity.
