# MyFinny Database Schema

This folder contains the database schema for the MyFinny financial tracking system.

## Database Type

PostgreSQL

## Schema Overview

The database uses a **star schema** design optimized for financial transaction analysis, consisting of:
- **1 Fact Table**: `fact_transaction` (stores transaction records)
- **4 Dimension Tables**: `dim_category`, `dim_expense`, `dim_source`, `dim_date`

## Tables

### Dimension Tables

#### 1. `dim_category`
Transaction category classification.

| Column | Type | Description |
|--------|------|-------------|
| category_id | INT (PK) | Unique category identifier |
| category_name | VARCHAR(50) | Category name |

**Static Data:**
- `1` - Income
- `2` - Spending

#### 2. `dim_expense`
Expense classification for spending transactions.

| Column | Type | Description |
|--------|------|-------------|
| expense_id | INT (PK) | Unique expense identifier |
| expense_name | VARCHAR(100) | Expense type name |

**Static Data:**
- `0` - Not Applicable (dummy for income)
- `1` - Food
- `2` - Electricity
- `3` - Internet
- `4` - Fuel
- `5` - Hygiene
- `6` - Shopping
- `7` - Laundry
- `8` - Snacks

#### 3. `dim_source`
Income source classification for income transactions.

| Column | Type | Description |
|--------|------|-------------|
| source_id | INT (PK) | Unique source identifier |
| source_name | VARCHAR(100) | Source name |

**Static Data:**
- `0` - Not Applicable (dummy for spending)
- `1` - Monthly
- `2` - Activities
- `3` - Others

#### 4. `dim_date`
Date dimension for time-based analysis.

| Column | Type | Description |
|--------|------|-------------|
| date_id | INT (PK) | Date identifier (YYYYMMDD format) |
| full_date | DATE | Full date value |
| year | INT | Year |
| month_num | INT | Month number (1-12) |
| month_name | VARCHAR(20) | Month name |

### Fact Table

#### 5. `fact_transaction`
Main transaction fact table.

| Column | Type | Description |
|--------|------|-------------|
| transaction_id | SERIAL (PK) | Auto-incrementing transaction ID |
| date_id | INT (FK) | Reference to dim_date |
| category_id | INT (FK) | Reference to dim_category |
| expense_id | INT (FK) | Reference to dim_expense |
| source_id | INT (FK) | Reference to dim_source |
| amount | NUMERIC(15,2) | Transaction amount |
| description | TEXT | Optional transaction description |
| created_at | TIMESTAMP | Record creation timestamp |

## Relationships

```
fact_transaction
  ├── dim_date (date_id)
  ├── dim_category (category_id)
  ├── dim_expense (expense_id)
  └── dim_source (source_id)
```

## Business Rules

1. **Income Transactions**: Use `category_id = 1`, `expense_id = 0` (Not Applicable)
2. **Spending Transactions**: Use `category_id = 2`, `source_id = 0` (Not Applicable)
3. **Date ID Format**: Stored as integer in YYYYMMDD format (e.g., 20260207 for Feb 7, 2026)

## Deployment

### Prerequisites
- PostgreSQL 12 or higher
- Database user with CREATE TABLE and INSERT privileges

### Setup Instructions

1. **Create Database**
   ```sql
   CREATE DATABASE myfinny;
   ```

2. **Connect to Database**
   ```bash
   psql -U your_username -d myfinny
   ```

3. **Run DDL Script**
   ```bash
   psql -U your_username -d myfinny -f database/ddl/schema.sql
   ```

   Or within psql:
   ```sql
   \i database/ddl/schema.sql
   ```

### Verification

Check that all tables were created:
```sql
\dt
```

Verify dimension data:
```sql
SELECT * FROM dim_category;
SELECT * FROM dim_expense;
SELECT * FROM dim_source;
```

## Example Queries

### Insert Income Transaction
```sql
INSERT INTO fact_transaction (date_id, category_id, expense_id, source_id, amount, description)
VALUES (20260207, 1, 0, 1, 5000000.00, 'Monthly salary');
```

### Insert Spending Transaction
```sql
INSERT INTO fact_transaction (date_id, category_id, expense_id, source_id, amount, description)
VALUES (20260207, 2, 1, 0, 50000.00, 'Lunch at restaurant');
```

### Monthly Summary
```sql
SELECT 
    d.month_name,
    d.year,
    c.category_name,
    SUM(f.amount) as total_amount,
    COUNT(*) as transaction_count
FROM fact_transaction f
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_category c ON f.category_id = c.category_id
GROUP BY d.year, d.month_num, d.month_name, c.category_name
ORDER BY d.year, d.month_num, c.category_name;
```

### Expense Breakdown
```sql
SELECT 
    e.expense_name,
    COUNT(*) as transaction_count,
    SUM(f.amount) as total_spent
FROM fact_transaction f
JOIN dim_expense e ON f.expense_id = e.expense_id
WHERE f.category_id = 2  -- Spending only
GROUP BY e.expense_name
ORDER BY total_spent DESC;
```

## Notes

- The dimension tables are pre-populated with static reference data
- `dim_date` needs to be populated separately via the ETL process
- Transaction amounts are stored with 2 decimal places
- All foreign keys are enforced with referential integrity constraints
