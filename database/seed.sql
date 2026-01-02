-- =========================================
-- Seed Data for Intelligent Financial
-- Behavior Analysis System
-- =========================================

USE intelligent_finance_db;

-- =========================================
-- Insert sample users
-- =========================================
INSERT INTO users (username, email) VALUES
('anil_kumar', 'anil@example.com');

-- =========================================
-- Insert sample categories
-- =========================================
INSERT INTO categories (name, description) VALUES
('Food', 'Food and dining expenses'),
('Shopping', 'Online and offline purchases'),
('Utilities', 'Electricity, water, recharge, etc.'),
('Transport', 'Travel and fuel expenses');

-- =========================================
-- Insert sample transactions
-- =========================================
INSERT INTO transactions
(user_id, category_id, date, amount, description, platform, source)
VALUES
(1, 1, '2025-08-10', 1200.00, 'Amazon purchase', 'GPay', 'CSV'),
(1, 1, '2025-08-11', 450.00, 'Swiggy food order', 'PhonePe', 'CSV'),
(1, 3, '2025-08-12', 300.00, 'Mobile recharge', 'Paytm', 'SMS'),
(1, NULL, '2025-08-13', 1500.00, 'Electricity bill', 'GPay', 'CSV');
