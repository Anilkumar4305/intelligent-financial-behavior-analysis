-- =========================================
-- Intelligent Financial Behavior Analysis DB
-- PRODUCTION-READY SCHEMA
-- =========================================

CREATE DATABASE IF NOT EXISTS intelligent_finance_db;
USE intelligent_finance_db;

-- =========================================
-- USERS
-- =========================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- TRANSACTIONS (MATCHES SQLALCHEMY MODEL)
-- =========================================
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,

    date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description VARCHAR(255) NOT NULL,
    platform VARCHAR(50) NOT NULL,

    -- Source of transaction
    source VARCHAR(20) DEFAULT 'manual',

    -- AI Classification fields (CRITICAL)
    category VARCHAR(100) NULL,
    confidence FLOAT NULL,
    classification_method VARCHAR(50) NULL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- BUDGETS (REQUIRED FOR ANALYTICS)
-- =========================================
CREATE TABLE IF NOT EXISTS budgets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    month VARCHAR(7) NOT NULL,  -- format: YYYY-MM
    monthly_budget DECIMAL(10,2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- INDEXES FOR PERFORMANCE
-- =========================================
CREATE INDEX idx_transaction_date ON transactions(date);
CREATE INDEX idx_transaction_category ON transactions(category);
CREATE INDEX idx_budget_month ON budgets(month);
