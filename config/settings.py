from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
BACKUP_DIR = DATA_DIR / "backups"
LOG_DIR = BASE_DIR / "logs"
APP_NAME = "GLAZE"
APP_VERSION = "0.1.0"
DEFAULT_ENCODING = "utf-8"
BACKUP_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"
@dataclass(frozen=True)
class DataFiles:
    students: Path = PROCESSED_DATA_DIR / "students.csv"
    guardians: Path = PROCESSED_DATA_DIR / "guardians.csv"
    classes: Path = PROCESSED_DATA_DIR / "classes.csv"
    programmes: Path = PROCESSED_DATA_DIR / "programmes.csv"
    products: Path = PROCESSED_DATA_DIR / "products.csv"
    programme_products: Path = PROCESSED_DATA_DIR / "programme_products.csv"
    programme_classes: Path = PROCESSED_DATA_DIR / "programme_classes.csv"
    enrolments: Path = PROCESSED_DATA_DIR / "enrolments.csv"
    attendance: Path = PROCESSED_DATA_DIR / "attendance.csv"
    bank_transactions: Path = PROCESSED_DATA_DIR / "bank_transactions.csv"
    payment_aliases: Path = PROCESSED_DATA_DIR / "payment_aliases.csv"
    payment_allocations: Path = PROCESSED_DATA_DIR / "payment_allocations.csv"
    bank_audit: Path = PROCESSED_DATA_DIR / "bank_audit.csv"
DATA_FILES = DataFiles()
def ensure_directories() -> None:
    for path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, BACKUP_DIR, LOG_DIR]:
        path.mkdir(parents=True, exist_ok=True)
