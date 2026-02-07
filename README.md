# MyFinny - Personal Finance ETL Project

## Project Overview

This project is an ETL (Extract, Transform, Load) pipeline that I built to manage my personal finance data. The goal is to automatically process transaction data from CSV files and load them into a PostgreSQL database with a proper data warehouse structure using dimensional modeling.

The data is sourced by filling Google Forms questions and later the response will be stored inside of a Google Sheets. Within the Google Sheets, I applied Google App Script to make the Sheets automatically create a new tab within the Sheet file for each month. It works by checking the timestamp of the data when the user click "Submit Form". Then, after the sheet is seperated by several months, we download each month file as csv that we will insert into the /data/raw/ folder.

---

## Project Objectives

1. **Automate** the process of importing financial transactions from CSV files
2. **Transform** raw transaction data into a structured format suitable for analysis
3. **Store** data in a proper star schema data warehouse
4. **Archive** processed files to avoid duplicate processing

---

## Project Structure

```
myfinny/
│
├── data/
│   ├── raw/                           # Place new CSV files here
│   └── archived/                      # Processed files moved here
│
├── database/
│   ├── ddl/
│   │   └── schema.sql                # Database DDL script
│   └── README.md                      # Database documentation
│
├── etl/
│   ├── extract.py                    # Reads CSV files
│   ├── transform.py                  # Cleans and transforms data
│   ├── load.py                       # Loads data to PostgreSQL
│   └── file_manager.py               # Handles file operations
│
├── scripts/
│   └── google-apps-script/
│       ├── Code.gs                   # Google Sheets automation
│       └── README.md                 # Apps Script documentation
│
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
├── main.py                           # Main ETL pipeline script
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

---

## Database Schema

I designed this database using the **star schema** approach, which is what we learned in class for data warehousing. It consists of:

### Dimension Tables

**1. dim_category**
- Stores transaction categories (Income or Spending)
- Static data: 2 records

**2. dim_expense**
- Stores different types of expenses
- Includes a "Not Applicable" entry (ID: 0) for income transactions
- Examples: Food, Electricity, Internet, Snacks, etc.

**3. dim_source**
- Stores income sources
- Includes a "Not Applicable" entry (ID: 0) for spending transactions
- Examples: Monthly Income, Activities, Others

**4. dim_date**
- Date dimension for time-based analysis
- Stores: date_id (YYYYMMDD), full_date, year, month_num, month_name

### Fact Table

**fact_transaction**
- Central fact table storing all transactions
- Contains foreign keys to all dimension tables
- Measures: amount, description
- Timestamp: created_at

---

## How the ETL Process Works

### 1. **Extract** (extract.py)
- Reads CSV files from `data/raw/` folder
- Uses pandas to load data into a DataFrame

### 2. **Transform** (transform.py)
- **Date Processing:** Converts timestamp strings to datetime objects
- **Category Mapping:** Maps "Income" and "Spending" to category IDs
- **Amount Handling:** 
  - For Income: uses the "Amount" column
  - For Spending: uses the "Price" column
- **Foreign Key Logic:**
  - If Income (category_id = 1): expense_id = 0, and source_id is mapped
  - If Spending (category_id = 2): source_id = 0, and expense_id is mapped
- **Description:** Combines Spending Description and Source Description
- **Data Cleaning:** Drops rows with null critical values

### 3. **Load** (load.py)
- **dim_date:** Inserts unique dates (with ON CONFLICT DO NOTHING to avoid duplicates)
- **fact_transaction:** Appends all transaction records
- Uses SQLAlchemy for database connections

### 4. **Archive** (file_manager.py)
- After successful processing, moves CSV files to `data/archived/`
- Prevents reprocessing the same file multiple times

---

## Setup Instructions

### Prerequisites
- Python 3.x
- PostgreSQL database
- Basic knowledge of terminal/command line

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

The required packages are:
- `pandas` - for data manipulation
- `sqlalchemy` - for database connections
- `psycopg2-binary` - PostgreSQL adapter
- `python-dotenv` - for environment variables (optional)

### 2. Database Setup

Create a PostgreSQL database and run the DDL script to create all tables:

```sql
-- Create database
CREATE DATABASE finance_project;

-- Then create all dimension and fact tables
-- (See full DDL in the SQL script provided separately)
```

**Important:** Make sure to populate the dimension tables (dim_category, dim_expense, dim_source) with the static reference data!

### 3. Configure Database Connection

Create a `.env` file in the project root by copying the example:

```bash
cp .env.example .env
```

Then edit `.env` and update your database credentials:

```env
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=finance_project

---

## How to Run

1. **Place your CSV file** in the `data/raw/` folder

2. **Run the ETL pipeline:**
   ```bash
   python main.py
   ```

3. **Expected output:**
   ```
   Found 1 file(s) to process
   
   Extracting: MyFinny data - February 2026.csv
   Preview:
   ...
   
   Successfully processed & archived: MyFinny data - February 2026.csv
   ```

4. **Check your database** - the data should now be in the fact_transaction table!

---

## CSV File Format

Your input CSV should have these columns:

| Column | Description | Example |
|--------|-------------|---------|
| Timestamp | Transaction date/time | 06/02/2026 20:14:05 |
| Date | Transaction date | 06/02/2026 |
| Category | Income or Spending | Spending |
| Spending Category | Type of expense | Snacks |
| Spending Description | Details of expense | Coffee |
| Price | Amount for spending | 40000 |
| Amount | Amount for income | 2000000 |
| Source | Income source | Monthly Income |
| Source Description | Income details | Transfer |

---

## Features

- Automated ETL pipeline
- Star schema data warehouse design
- Proper dimension and fact table separation
- Handles both income and spending transactions
- Automatic file archiving
- Duplicate prevention (ON CONFLICT handling)
- Date dimension for time-series analysis
- Clean separation of concerns (extract, transform, load)

---

## Technologies Used

- **Python 3** - Main programming language
- **Pandas** - Data manipulation and analysis
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Relational database
- **psycopg2** - PostgreSQL adapter for Python

---

## Challenges I Faced

1. **Column name mismatches** - The CSV had "Timestamp" but my code initially expected "created_at". Had to map the column names properly.

2. **Foreign key logic** - Figuring out when to use expense_id vs source_id based on transaction category was tricky at first. Had to make sure Income transactions don't get assigned invalid expense IDs.

3. **Database connection strings** - Initially used JDBC format instead of SQLAlchemy format. Had to convert to `postgresql://` format.

4. **os.getenv() confusion** - Accidentally passed the actual URL to os.getenv() instead of an environment variable name. That was a silly mistake that took a while to debug!

---

## Future Improvements

If I have more time, here are things I'd like to add:

- [ ] Add data validation (check for negative amounts, invalid dates, etc.)
- [x] ~~Create a config file for database credentials instead of hardcoding~~ (Done: using .env)
- [ ] Add logging to track ETL runs (success/failure, row counts, etc.)
- [ ] Build a simple dashboard for visualizing the data
- [ ] Add error handling for specific edge cases
- [ ] Support for multiple file formats (Excel, JSON)
- [ ] Implement incremental loads for large datasets
- [ ] Add unit tests for each ETL component

---

## What I Learned

This project really helped me understand:
- How ETL pipelines work in practice
- The importance of dimensional modeling in data warehousing
- Working with pandas for data transformation
- Using SQLAlchemy for database interactions
- The star schema pattern and why it's useful for analytics
- File handling and automation in Python

---

## Contact

For questions or suggestions about this project, feel free to reach out!

---

**Note:** This is a learning project for my Data Engineering course. The code might not be production-ready but it demonstrates the core concepts of ETL and data warehousing!