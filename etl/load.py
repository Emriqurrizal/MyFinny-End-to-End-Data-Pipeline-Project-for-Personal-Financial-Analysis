from sqlalchemy import create_engine, text
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build database URL from environment variables
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'finance_project')

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

def load_dim_date(df: pd.DataFrame):
    dim_date_df = df[[
        "date_id",
        "full_date",
        "year",
        "month_num",
        "month_name"
    ]].drop_duplicates()

    with engine.begin() as conn:
        for _, row in dim_date_df.iterrows():
            conn.execute(
                text("""
                    INSERT INTO dim_date (
                        date_id,
                        full_date,
                        year,
                        month_num,
                        month_name
                    )
                    VALUES (
                        :date_id,
                        :full_date,
                        :year,
                        :month_num,
                        :month_name
                    )
                    ON CONFLICT (date_id) DO NOTHING
                """),
                row.to_dict()
            )

def load_fact_transaction(df: pd.DataFrame):
    fact_df = df[[
        "date_id",
        "category_id",
        "expense_id",
        "source_id",
        "amount",
        "description",
        "created_at"
    ]]

    fact_df.to_sql(
        "fact_transaction",
        engine,
        if_exists="append",
        index=False
    )
