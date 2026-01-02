# Database Setup Guide

This document explains how to initialize and populate the MySQL database
for the Intelligent Financial Behavior Analysis System.

---

## Prerequisites

- MySQL 8.x installed
- Access to MySQL command line or GUI (MySQL Workbench)

---

## Step 1: Create Database Schema

Run the following command in MySQL:

```sql
SOURCE schema.sql;
```
This will:

- Create the database intelligent_finance_db

- Create all required tables

- Apply foreign key constraints

## Step 2: Insert Seed Data

Run the following command:

```sql
SOURCE seed.sql;
```
This will insert:

- Sample user data

- Predefined spending categories

- Example transactions (including uncategorized data)

## Notes

- All data is synthetic and safe for testing

- No real financial or personal data is used

- Categories can be reassigned later by AI models

## Troubleshooting

- Ensure schema.sql is executed before seed.sql

- Verify database selection using USE intelligent_finance_db;

- Check for foreign key errors if execution fails