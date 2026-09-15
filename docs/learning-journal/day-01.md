# Day 1 — Learning Journal

## Purpose of This Journal

This project is being built as a practical learning environment for *Fundamentals of Data Engineering*.

The purpose of this journal is to connect concepts studied from the book to actual engineering decisions made while building the project.

The goal is not to force every book concept into the project.

A concept is marked as:

* **Applied** — meaningfully used in the current project stage.
* **Partially Applied** — relevant, but only part of the concept has been implemented.
* **Not Yet Applied** — understood or identified, but not required at the current stage.

---

# Data Architecture

## What I Learned

Data architecture should be designed around the movement and use of data rather than around individual technologies.

Before selecting databases, cloud services, orchestration tools, or frameworks, the problem, data requirements, and expected data flow should be understood.

## Application in This Project

The project started by defining the analytical problem and the expected data flow.

The initial conceptual architecture is:

```text
Data Source
    ↓
Python Ingestion
    ↓
Raw Data
    ↓
Storage
    ↓
Transformation
    ↓
Analytics
    ↓
AI Analyst
```

This architecture is intentionally conceptual at this stage.

The implementation technologies are not treated as irreversible decisions.

## Evidence

* `docs/project-scope.md`
* `docs/architecture.md`
* `README.md`

## Status

**Applied**

---

# Domains and Services

## What I Learned

A Data Engineering system can be understood as a collection of responsibilities or domains rather than simply as a collection of tools.

Each part of the architecture should have a clear responsibility.

This helps prevent unnecessary coupling and makes the architecture easier to evolve.

## Application in This Project

The project separates responsibilities into conceptual layers:

```text
Source
    ↓
Ingestion
    ↓
Raw Data
    ↓
Storage
    ↓
Transformation
    ↓
Analytics
    ↓
AI Analyst
```

For example:

* Ingestion is responsible for bringing data into the system.
* Raw storage preserves the source representation.
* Transformation prepares data for analytical use.
* Analytics provides meaningful metrics.
* The AI Analyst consumes analytical information rather than directly modifying raw data.

## Evidence

* `docs/architecture.md`

## Status

**Applied**

---

# Data Architecture Principles

## What I Learned

Good architecture should avoid unnecessary complexity and should evolve according to actual requirements.

Important principles applied during the initial design include:

* Understand the data before finalizing the model.
* Keep raw data separate from transformed data.
* Prefer simple architecture initially.
* Keep important decisions reversible.
* Introduce additional infrastructure only when it solves a demonstrated problem.

## Application in This Project

The project deliberately starts with a local implementation.

The expected evolution is:

```text
Local
  ↓
Dockerized
  ↓
Automated
  ↓
Cloud
  ↓
Production-like
```

This prevents the project from becoming a collection of technologies that are not required by the current problem.

## Evidence

* `docs/architecture.md`

## Status

**Applied**

---

# Data Modeling

## What I Learned

A data model should be based on the actual characteristics of the data and the analytical questions that need to be answered.

The initial model should therefore be treated as a hypothesis until the real source data has been examined.

## Application in This Project

An initial analytical model was proposed around:

```text
fact_sms_activity
dim_time
dim_square
dim_country
```

However, this model was explicitly marked as provisional.

The project first performs Data Profiling before finalizing the Fact/Dimension design.

## Evidence

* `docs/architecture.md`

## Status

**Partially Applied**

The model will be reviewed in Day 3 using the actual profiling results.

---

# Designing for Change

## What I Learned

Early architecture decisions should remain reversible when the available information is incomplete.

A decision made before understanding the data may need to change later.

## Application in This Project

PostgreSQL and the initial Star Schema were not treated as irreversible decisions.

The project explicitly follows:

```text
Understand
    ↓
Profile
    ↓
Model
    ↓
Implement
```

rather than:

```text
Choose Technology
    ↓
Force Data Into It
```

## Evidence

* `docs/architecture.md`
* `docs/data-profiling.md`

## Status

**Applied**

---

# Day 1 Reflection

The most important lesson from the first day was that Data Engineering should begin with the problem and data, not with technology.

The project therefore follows:

```text
Business Problem
      ↓
Data Requirements
      ↓
Data Source
      ↓
Architecture
      ↓
Data Model
      ↓
Implementation
```

This became the foundation for the work performed on Day 2.
