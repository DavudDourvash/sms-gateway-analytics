# Data Architecture

## Version 1

The initial architecture follows a simple batch-oriented data pipeline.

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
