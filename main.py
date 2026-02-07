from etl.extract import extract_csv
from etl.transform import transform_transactions
from etl.load import load_dim_date, load_fact_transaction
from etl.file_manager import get_raw_files, archive_file

def main():
    raw_files = get_raw_files()

    if not raw_files:
        print("No files found in data/raw/")
        return

    print(f"Found {len(raw_files)} file(s) to process")

    for file_path in raw_files:
        try:
            # Extract
            df_raw = extract_csv(file_path)

            # Transform
            df_transformed = transform_transactions(df_raw)

            # Load
            load_dim_date(df_transformed)
            load_fact_transaction(df_transformed)

            # Archive
            archive_file(file_path)

            print(f"Successfully processed & archived: {file_path.name}")

        except Exception as e:
            print(f"Failed processing: {file_path.name}")
            print(e)

if __name__ == "__main__":
    main()
