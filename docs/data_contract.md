# Transaction Data Contract

## Purpose
This document defines the canonical transaction data structure used
across the entire system, regardless of the original data source.

---

## Canonical Transaction Schema

| Field | Type | Description |
|------|------|------------|
| user_id | Integer | Unique identifier of the user |
| date | Date (YYYY-MM-DD) | Transaction date |
| amount | Decimal | Transaction amount |
| description | String | Transaction description |
| platform | String | Payment platform (GPay, PhonePe, etc.) |
| source | String | Data source (CSV, SMS, Manual) |
| category | String / Null | Assigned spending category |

---

## Example Canonical Transaction

```json
{
  "user_id": 1,
  "date": "2025-08-12",
  "amount": 450.00,
  "description": "Swiggy food order",
  "platform": "PhonePe",
  "source": "CSV",
  "category": null
}
```

## Design Principles

- Single unified data structure
- Source-independent ingestion
- Validation-friendly format
- AI-ready for categorization
- Privacy-first (no sensitive credentials stored)
