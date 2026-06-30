from __future__ import annotations
import pandas as pd
from config.settings import ensure_directories
from core.data_store import load_all_tables, load_table, save_table
from core.logging_config import get_logger
logger = get_logger(__name__)
def main() -> None:
    ensure_directories()
    students = load_table("students")
    print("Initial students columns:", students.columns.tolist())
    print("Initial students rows:", len(students))
    sample = pd.DataFrame(
        [
            {
                "student_id": "STU-001",
                "first_name": "Ada",
                "last_name": "Lovelace",
                "status": "Current",
                "notes": "Test record",
            }
        ]
    )
    save_table("students", sample)
    reloaded = load_table("students")
    print("Reloaded students rows:", len(reloaded))
    print("Reloaded first row:", reloaded.iloc[0].to_dict())
    everything = load_all_tables()
    print("Loaded tables:", sorted(everything.keys()))
    logger.info("Backend smoke test completed successfully.")
if __name__ == "__main__":
    main()
