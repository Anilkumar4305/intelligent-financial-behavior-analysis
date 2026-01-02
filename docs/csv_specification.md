# CSV Data Ingestion Specification

## Purpose
This document defines the supported CSV format for ingesting
transaction data into the system.

The CSV format is designed to be:
- Simple
- Human-readable
- Compatible with exports from payment platforms

---

## Supported CSV Structure

### Required Header

The CSV file must contain the following header row:

date,amount,description,platform


---

## Field Definitions

| Column | Type | Description |
|------|------|------------|
| date | Date (YYYY-MM-DD) | Transaction date |
| amount | Decimal | Amount spent |
| description | String | Transaction description |
| platform | String | Payment platform name |

---

## Example CSV File

```csv
date,amount,description,platform
2025-08-10,1200,Amazon purchase,GPay
2025-08-11,450,Swiggy order,PhonePe
2025-08-12,300,Mobile recharge,Paytm
```

## Validation Rules

- Header row is mandatory
- Date must follow `YYYY-MM-DD` format
- Amount must be a positive number
- Platform field cannot be empty
- Rows with invalid or incomplete data are rejected

---

## Mapping to Canonical Data Contract

| CSV Column | Canonical Field |
|-----------|----------------|
| date | date |
| amount | amount |
| description | description |
| platform | platform |
| (implicit) | source = "CSV" |
