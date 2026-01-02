# SMS Text Ingestion Specification

## Purpose
This document defines how SMS-style transaction messages are ingested,
parsed, and normalized into the system.

To ensure ethical compliance and zero-cost implementation, the system
uses SMS text simulation rather than direct access to a user's inbox.

---

## Supported Input Type

- Plain text strings simulating transaction SMS messages
- User-provided input (manual paste or uploaded text file)

---

## Example SMS Messages

- Rs.1200 spent on Amazon via GPay on 10-08-2025
- INR 450 paid to Swiggy using PhonePe on 11-08-2025


---

## Data Extraction Goals

From each SMS message, the system attempts to extract:

| Field | Description |
|------|------------|
| amount | Transaction amount |
| platform | Payment platform used |
| description | Merchant or purpose |
| date | Transaction date |

---

## Validation Rules

- Message must contain a numeric amount
- Platform name must be detectable
- Date must be present or inferred
- Messages failing extraction are flagged
- No message content is stored permanently

---

## Mapping to Canonical Data Contract

| Extracted Field | Canonical Field |
|---------------|----------------|
| amount | amount |
| platform | platform |
| description | description |
| date | date |
| (implicit) | source = "SMS" |

---

## Ethical & Privacy Justification

- No automatic SMS reading
- No device permissions required
- No banking credentials collected
- User has full control over data input
- Fully compliant with privacy-first principles

---

## Notes

This ingestion method is designed as a proof-of-concept and can later
be extended to real device-based ingestion with explicit user consent.
