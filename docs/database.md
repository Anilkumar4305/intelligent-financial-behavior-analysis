# Database Schema & Data Model

## 1. Database Selection

The project uses **MySQL**, an open-source relational database, due to its reliability, scalability, and strong support for structured data. It integrates smoothly with Python-based backend frameworks such as FastAPI and Flask.

---

## 2. Design Objectives

- Store transaction data in a structured and normalized format
- Support multiple data ingestion sources (CSV, Manual, SMS-style input)
- Enable efficient querying for analysis and visualization
- Ensure privacy-first and minimal data storage principles
- Maintain scalability for future feature extensions

---

## 3. Database Tables Overview

The system consists of the following core tables:

| Table Name | Purpose |
|-----------|---------|
| users | Stores basic user information |
| transactions | Stores all financial transactions |
| categories | Stores predefined expense categories |

---

## 4. Table Structure: users

| Column Name | Data Type | Description |
|------------|----------|-------------|
| user_id | INT (Primary Key, Auto Increment) | Unique user identifier |
| username | VARCHAR(50) | Display name of the user |
| email | VARCHAR(100) | User email address |
| created_at | DATETIME | Account creation timestamp |

**Notes:**
- No sensitive financial or banking credentials are stored.
- Designed to support privacy and GDPR compliance.

---

## 5. Table Structure: categories

| Column Name | Data Type | Description |
|------------|----------|-------------|
| category_id | INT (Primary Key, Auto Increment) | Unique category identifier |
| name | VARCHAR(50) | Category name (e.g., Food, Transport) |
| description | VARCHAR(255) | Optional category description |

**Notes:**
- Categories are predefined and shared across all users.
- Easily extendable for future use cases.

---

## 6. Table Structure: transactions

| Column Name | Data Type | Description |
|------------|----------|-------------|
| transaction_id | INT (Primary Key, Auto Increment) | Unique transaction identifier |
| user_id | INT (Foreign Key) | References users.user_id |
| date | DATE | Transaction date |
| amount | DECIMAL(10,2) | Transaction amount |
| description | VARCHAR(255) | Merchant or transaction details |
| platform | VARCHAR(50) | Payment platform (PhonePe, GPay, etc.) |
| source | VARCHAR(20) | Input source (CSV, Manual, SMS) |
| category_id | INT (Foreign Key) | References categories.category_id |
| created_at | DATETIME | Record creation timestamp |

---

## 7. Entity Relationship Diagram (ERD)

users
└── user_id
│
│
transactions
└── category_id
│
categories

```mermaid
erDiagram
    USERS ||--o{ TRANSACTIONS : has
    CATEGORIES ||--o{ TRANSACTIONS : classifies

    USERS {
        int user_id
        string username
        string email
    }

    TRANSACTIONS {
        int transaction_id
        date date
        float amount
        string description
        string platform
        string source
    }

    CATEGORIES {
        int category_id
        string name
    }

- One user can have multiple transactions.
- Each transaction belongs to a single category.
- Categories are global and reused across users.

---

## 8. Data Flow Explanation

- User-provided data (CSV, Manual, SMS-style input) is normalized before storage.
- All transaction records are stored in the `transactions` table.
- AI-based categorization updates the `category_id` field.
- The structured data enables efficient analysis and visualization.

---

## 9. Ethical & Privacy Considerations

- Only essential user and transaction data is stored.
- No banking credentials or sensitive personal data is collected.
- User data can be deleted upon request.
- The system follows privacy-first and consent-based data processing principles.

---

## 10. Summary

This database design ensures a clean, scalable, and ethical foundation for financial behavior analysis, enabling seamless integration with backend APIs, AI categorization modules, and visualization dashboards.

