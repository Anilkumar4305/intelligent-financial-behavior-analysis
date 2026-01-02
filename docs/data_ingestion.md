# Data Ingestion Module

## 1. Supported Input Types

The system supports multiple user-authorized input methods to ensure flexibility and privacy:

1. **CSV File Upload**
   - Users can upload exported transaction history from banks, UPI apps, or wallets.
   - This allows bulk data processing and quick analysis.

2. **Manual Entry**
   - Users can manually input transactions that may not be captured in CSV files.
   - This ensures completeness and correction of missing or erroneous data.

3. **SMS-style Text Input (Simulated)**
   - Users can paste transaction messages received via SMS or mobile notifications.
   - Example: `"Rs.450 spent on Swiggy via PhonePe on 12-08-2025"`
   - The system parses these messages to extract relevant transaction information.

---

## 2. CSV Format

The system expects CSV files with the following columns:

| Column Name | Description |
|------------|-------------|
| date | Transaction date in format YYYY-MM-DD |
| amount | Transaction amount (numeric) |
| description | Transaction details or narration |
| platform | Payment platform (PhonePe, GPay, Paytm, etc.) |

**Notes:**
- The system can handle variations in CSV column order.
- Additional columns are ignored.
- Data is validated before processing.

---

## 3. SMS Simulation Explanation

- Direct automatic access to SMS or UPI platforms is **not implemented** to maintain privacy and legality.
- Users provide transaction messages manually in text form, simulating automatic ingestion.
- The parsing engine extracts:
  - Date
  - Amount
  - Merchant / description
  - Platform
- All data is normalized into a **unified internal format** for consistent processing across CSV, manual, and SMS inputs.

---

## 4. Ethical & Privacy Considerations

- No banking credentials or personal authentication data are collected.
- No unauthorized access or scraping of private platforms occurs.
- All data processing is **user-authorized** and **transparent**.
- Data is used solely for categorization, analysis, and insight generation.
- The system complies with **privacy-first design principles** and ensures ethical handling of user financial information.

