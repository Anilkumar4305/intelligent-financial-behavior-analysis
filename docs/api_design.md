
> ⚠️ **Status: Work in Progress (Deferred)**
>
> This API design is intentionally kept as a draft.
> Final endpoint definitions and data contracts will be completed
> after validating data ingestion formats, categorization logic,
> and overall system workflows.
>
> This approach avoids premature architectural decisions
> and aligns with real-world iterative software development practices.

# Backend API Design

## 1. Overview

This document describes the design of the backend REST APIs for the *Intelligent Financial Behavior Analysis & Decision Support System*.  
The backend is responsible for secure data ingestion, validation, normalization, categorization, analysis, and delivery of insights to the frontend interface.

The APIs follow RESTful principles with a strong emphasis on scalability, modularity, and ethical data handling.

---

## 2. API Responsibilities

The backend APIs are responsible for:

- Accepting user-authorized transaction data
- Validating and normalizing incoming data
- Persisting structured data into the database
- Triggering categorization and analytical workflows
- Providing aggregated insights for visualization
- Ensuring privacy-first and stateless communication

---

## 3. Endpoint List

### 3.1 Authentication APIs

| Method | Endpoint | Description |
|------|---------|------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Authenticate an existing user |

---

### 3.2 Data Ingestion APIs

| Method | Endpoint | Description |
|------|---------|------------|
| POST | `/api/transactions/upload-csv` | Upload transaction data via CSV |
| POST | `/api/transactions/manual` | Add a transaction manually |
| POST | `/api/transactions/sms` | Submit SMS-style transaction text |

---

### 3.3 Transaction Management APIs

| Method | Endpoint | Description |
|------|---------|------------|
| GET | `/api/transactions` | Retrieve all user transactions |
| GET | `/api/transactions/{id}` | Retrieve a specific transaction |
| DELETE | `/api/transactions/{id}` | Delete a transaction |

---

### 3.4 Categorization API

| Method | Endpoint | Description |
|------|---------|------------|
| POST | `/api/categorize` | Categorize uncategorized transactions |

---

### 3.5 Analytics APIs

| Method | Endpoint | Description |
|------|---------|------------|
| GET | `/api/analytics/summary` | Overall spending summary |
| GET | `/api/analytics/category-wise` | Category-wise expense analysis |
| GET | `/api/analytics/monthly` | Monthly spending trends |

---

## 4. Sample Request & Response

### 4.1 Manual Transaction Entry

**Request**
```json
{
  "date": "2025-08-12",
  "amount": 450,
  "description": "Swiggy food order",
  "platform": "PhonePe"
}
```
Response
```json
{
  "status": "success",
  "transaction_id": 102,
  "message": "Transaction stored successfully"
}
```

---

# 🔹 SMS Example (Same Pattern)

```markdown
### 4.2 SMS-style Input

**Request**
```json
{
  "message": "Rs.1200 spent on Amazon via GPay on 10-08-2025"
}
```
Response

```json
{
  "status": "success",
  "parsed_data": {
    "amount": 1200,
    "platform": "GPay",
    "description": "Amazon purchase",
    "date": "2025-08-10"
  }
}
```

## 5. Validation Rules

The backend enforces strict validation rules before processing any request:

Mandatory fields must be present

Transaction amount must be greater than zero

Date must follow a valid and supported format

Platform values must belong to an allowed list

Invalid or malformed requests are rejected

Duplicate or inconsistent entries are flagged

Error Handling Strategy
Status Code	Meaning
400	Invalid request or validation error
401	Unauthorized access
404	Resource not found
500	Internal server error
Security & Privacy Considerations

No banking credentials are collected or stored

APIs operate only on user-consented data

Sensitive data is never logged

Stateless authentication mechanisms are used

Data access is restricted strictly per user

## 8. Summary

This API design ensures clean separation of concerns, scalability, and ethical data handling.
It provides a robust foundation for integrating data ingestion, AI-based categorization, analytics, and visualization in a real-world financial behavior analysis system.