import pandas as pd
from pathlib import Path

def extract_csv(file_path: Path) -> pd.DataFrame:
    print(f"\nExtracting: {file_path.name}")

    df = pd.read_csv(file_path)
    return df
