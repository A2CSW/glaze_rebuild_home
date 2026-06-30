from __future__ import annotations
from pathlib import Path
import pandas as pd
from config.settings import DATA_FILES
from core.atomic_io import atomic_write_csv, safe_read_csv
from core.backup import backup_file
from core.logging_config import get_logger
from core.validation import make_empty_table, prepare_table, validate_table
logger = get_logger(__name__)
TABLE_PATHS: dict[str, Path] = {
    "students": DATA_FILES.students,
    "guardians": DATA_FILES.guardians,
    "classes": DATA_FILES.classes,
    "programmes": DATA_FILES.programmes,
    "products": DATA_FILES.products,
    "programme_products": DATA_FILES.programme_products,
    "programme_classes": DATA_FILES.programme_classes,
    "enrolments": DATA_FILES.enrolments,
    "attendance": DATA_FILES.attendance,
    "bank_transactions": DATA_FILES.bank_transactions,
    "payment_aliases": DATA_FILES.payment_aliases,
    "payment_allocations": DATA_FILES.payment_allocations,
    "bank_audit": DATA_FILES.bank_audit,
}
def get_table_path(table_name: str) -> Path:
    if table_name not in TABLE_PATHS:
        raise KeyError(f"Unknown table name: {table_name}")
    return TABLE_PATHS[table_name]
def load_table(table_name: str) -> pd.DataFrame:
    path = get_table_path(table_name)
    if not path.exists():
        logger.info("Table %s does not exist yet; returning empty schema table", table_name)
        return make_empty_table(table_name)
    df = safe_read_csv(path)
    return prepare_table(df, table_name)
def save_table(table_name: str, df: pd.DataFrame) -> None:
    path = get_table_path(table_name)
    clean = validate_table(df, table_name)
    backup_file(path)
    atomic_write_csv(clean, path)
def load_all_tables() -> dict[str, pd.DataFrame]:
    return {table_name: load_table(table_name) for table_name in TABLE_PATHS}
