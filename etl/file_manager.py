from pathlib import Path
import shutil

RAW_DIR = Path("data/raw")
ARCHIVE_DIR = Path("data/archived")

def get_raw_files():
    return list(RAW_DIR.glob("*.csv"))

def archive_file(file_path: Path):
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.move(str(file_path), ARCHIVE_DIR / file_path.name)
