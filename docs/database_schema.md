# Database Schema Design (MySQL)

## Purpose
This document defines the relational database schema used to store
users, transactions, and spending categories for the system.

The schema is designed to:
- Match the canonical transaction data contract
- Enforce data integrity
- Support analytics and AI categorization
- Scale with additional features

---

## Database Overview

Database Type: MySQL  
Design Style: Normalized relational schema  

---

## Table: users

Stores basic user information.

| Column | Type | Constraints |
|------|------|------------|
| user_id | INT | PRIMARY KEY, AUTO_INCREMENT |
| username | VARCHAR(100) | NOT NULL |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP |

---

## Table: categories

Stores spending categories.

| Column | Type | Constraints |
|------|------|------------|
| category_id | INT | PRIMARY KEY, AUTO_INCREMENT |
| name | VARCHAR(100) | UNIQUE, NOT NULL |
| description | TEXT | NULL |

---

## Table: transactions

Stores all financial transactions.

| Column | Type | Constraints |
|------|------|------------|
| transaction_id | INT | PRIMARY KEY, AUTO_INCREMENT |
| user_id | INT | FOREIGN KEY → users(user_id) |
| category_id | INT | FOREIGN KEY → categories(category_id), NULL |
| date | DATE | NOT NULL |
| amount | DECIMAL(10,2) | NOT NULL |
| description | VARCHAR(255) | NOT NULL |
| platform | VARCHAR(50) | NOT NULL |
| source | VARCHAR(20) | NOT NULL |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP |

---

## Relationships

- One user can have many transactions
- One category can classify many transactions
- Each transaction belongs to one user
- Category assignment is optional and may be added later

---

## Mapping to Canonical Data Contract

| Canonical Field | Database Column |
|---------------|----------------|
| user_id | users.user_id |
| date | transactions.date |
| amount | transactions.amount |
| description | transactions.description |
| platform | transactions.platform |
| source | transactions.source |
| category | categories.name (via category_id) |

---

## Design Notes

- Category is nullable to allow delayed AI classification
- No sensitive banking data is stored
- Schema supports future analytics queries
