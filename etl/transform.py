import pandas as pd

CATEGORY_MAP = {
    "Income": 1,
    "Spending": 2
}

EXPENSE_MAP = {
    "Not Applicable": 0,
    "Food": 1,
    "Electricity": 2,
    "Internet": 3,
    "Fuel": 4,
    "Hygiene": 5,
    "Shopping": 6,
    "Laundry": 7,
    "Snacks": 8
}

SOURCE_MAP = {
    "Not Applicable": 0,
    "Monthly Income": 1,
    "Activities": 2,
    "Others": 3
}

def transform_transactions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # -------------------------
    # Date handling
    # -------------------------
    df["created_at"] = pd.to_datetime(df["Timestamp"], dayfirst=True)
    df["full_date"] = df["created_at"].dt.date

    df["date_id"] = df["created_at"].dt.strftime("%Y%m%d").astype(int)
    df["year"] = df["created_at"].dt.year
    df["month_num"] = df["created_at"].dt.month
    df["month_name"] = df["created_at"].dt.month_name()

    # -------------------------
    # Category → ID
    # -------------------------
    df["category_id"] = df["Category"].map(CATEGORY_MAP)

    # -------------------------
    # Amount handling (Income uses Amount, Spending uses Price)
    # -------------------------
    df["amount"] = df["Amount"].fillna(df["Price"])

    # -------------------------
    # Description handling
    # -------------------------
    df["description"] = df["Spending Description"].fillna(df["Source Description"])

    # -------------------------
    # FK handling (conditional based on category)
    # -------------------------
    # If Income (category_id=1): expense_id=0, map source_id
    # If Spending (category_id=2): source_id=0, map expense_id
    
    df["expense_id"] = df.apply(
        lambda row: 0 if row["category_id"] == 1 
        else EXPENSE_MAP.get(row["Spending Category"], 0),
        axis=1
    )
    
    df["source_id"] = df.apply(
        lambda row: 0 if row["category_id"] == 2 
        else SOURCE_MAP.get(row["Source"], 0),
        axis=1
    )

    # -------------------------
    # Null handling
    # -------------------------
    df = df.dropna(subset=[
        "amount",
        "category_id",
        "date_id"
    ])

    return df
