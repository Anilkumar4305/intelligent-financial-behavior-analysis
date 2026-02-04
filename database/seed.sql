USE intelligent_finance_db;

-- =========================================
-- SAMPLE TRANSACTIONS
-- =========================================
INSERT INTO transactions
(date, amount, description, platform, source, category, confidence, classification_method)
VALUES
('2025-08-10', 1200.00, 'Amazon purchase', 'GPay', 'csv', 'SHOPPING', 0.85, 'rule-based'),
('2025-08-11', 450.00, 'Swiggy food order', 'PhonePe', 'csv', 'FOOD', 0.90, 'rule-based'),
('2025-08-12', 300.00, 'Mobile recharge', 'Paytm', 'sms', 'BILLS', 0.75, 'rule-based'),
('2025-08-13', 1500.00, 'Electricity bill', 'GPay', 'csv', 'BILLS', 0.80, 'rule-based');

-- =========================================
-- SAMPLE BUDGETS
-- =========================================
INSERT INTO budgets (category, month, monthly_budget) VALUES
('FOOD', '2025-08', 5000),
('SHOPPING', '2025-08', 7000),
('BILLS', '2025-08', 4000);
