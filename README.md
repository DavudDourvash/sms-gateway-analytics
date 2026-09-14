# SMS Gateway Analytics & AI Agent

## Project Overview

This project explores how real-world SMS and telecom traffic data can be transformed into reliable analytics and, eventually, an AI-powered analytical assistant.

The primary goal is to learn **Data Engineering fundamentals through a real-world problem**, rather than building an isolated tutorial project.

The project follows an incremental approach:

**Fundamentals → Data Understanding → Modeling → Implementation → Automation/Cloud → AI Analyst**

---

## Objectives

* Build a real data ingestion pipeline
* Understand data grain, schema, and data quality
* Learn data modeling and analytical data design
* Build reliable analytics for SMS traffic
* Explore operational and business insights
* Introduce automation and cloud infrastructure gradually
* Build an evidence-based AI analyst

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

Commercial SMS Gateway entities such as customers, pricing, revenue, delivery status, and provider contracts are **outside the current scope**, because equivalent public real-world data is not available.

---

## Data Profiling

Day 2 focused on understanding the real structure and quality of the source data before finalizing the data model.

Key findings:

* **4,842,625 rows** in the profiled daily dataset
* **10,000 geographic squares**
* **246 country codes**
* **144 time intervals per day**
* **10-minute time grain**
* No duplicate logical records detected
* No negative activity values detected
* Significant missing values exist in activity measurements
* SMS activity distributions are strongly right-skewed

The observed logical grain is:

**Geographic Square + Time Interval + Country Code**

Detailed profiling results are documented in:

`docs/data-profiling.md`

---

## Architecture

The current conceptual architecture is:

**Data Source
→ Python Ingestion
→ Raw Data
→ Storage
→ Transformation
→ Analytics
→ AI Analyst**

The storage technology and final analytical data model are still being evaluated based on the results of data profiling.

The architecture will evolve incrementally from a local implementation toward automation, cloud infrastructure, and eventually an AI-powered analytical layer.

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
* Schema identified
* Data grain identified
* Data volume measured
* Time structure validated
* Missing values analyzed
* Duplicate records checked
* Cardinality analyzed
* Data quality checks performed
* SMS activity distribution analyzed
* Profiling results documented

### Day 3 — Architecture & Data Model Review 🔜

The next step is to use the profiling results to validate and refine:

* Data grain
* Fact table design
* Dimension tables
* Star schema
* Raw → Staging → Analytics layers
* NULL handling
* Storage technology
* Overall architecture

---

## Repository Structure

```text
sms-gateway-analytics/
│
├── data/                  # Local datasets (not tracked by Git)
│
├── docs/
│   ├── project-scope.md
│   ├── data-source.md
│   ├── architecture.md
│   └── data-profiling.md
│
├── src/
│   └── profiling/
│       ├── profile_sms_data.py
│       └── profile_sms_data.ipynb
│
├── .gitignore
└── README.md
```

---

## Engineering Principles

This project follows several principles:

1. Understand the data before finalizing the model.
2. Preserve raw data before transformation.
3. Prefer simple architecture over premature complexity.
4. Make data quality observable and testable.
5. Keep architectural decisions reversible where possible.
6. Introduce new technologies only when they solve a demonstrated problem.
7. Never fabricate unavailable business data.
8. Build the project incrementally toward production-like architecture.

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
Implementation
       ↓
Automation / Cloud
       ↓
AI Analyst
```
