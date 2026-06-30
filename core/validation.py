from __future__ import annotations
from typing import Any
import pandas as pd
from core.dataframe_utils import (
    coerce_to_string_columns,
    ensure_columns,
    normalize_column_names,
    reorder_columns,
)
from core.exceptions import RecordValidationError, SchemaValidationError
from core.integrity import validate_foreign_keys
from core.logging_config import get_logger
from core.rules import TABLE_RULES
from core.schema_registry import SCHEMAS
logger = get_logger(__name__)
def get_schema(table_name: str) -> list[str]:
    if table_name not in SCHEMAS:
        raise SchemaValidationError(f"Unknown schema table: {table_name}")
    return SCHEMAS[table_name]
def get_table_rules(table_name: str) -> dict[str, Any]:
    if table_name not in TABLE_RULES:
        raise SchemaValidationError(f"No rules registered for table: {table_name}")
    return TABLE_RULES[table_name]
def make_empty_table(table_name: str) -> pd.DataFrame:
    return pd.DataFrame(columns=get_schema(table_name))
def validate_required_columns(df: pd.DataFrame, table_name: str) -> None:
    schema = get_schema(table_name)
    missing = [column for column in schema if column not in df.columns]
    if missing:
        raise SchemaValidationError(
            f"Table '{table_name}' is missing required columns: {missing}"
        )
def prepare_table(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    schema = get_schema(table_name)
    clean = normalize_column_names(df)
    clean = ensure_columns(clean, schema)
    clean = coerce_to_string_columns(clean, schema)
    clean = reorder_columns(clean, schema)
    return clean
def validate_no_duplicate_keys(
    df: pd.DataFrame,
    key_columns: list[str],
    table_name: str,
) -> None:
    if df.empty:
        return
    missing_keys = [c for c in key_columns if c not in df.columns]
    if missing_keys:
        raise SchemaValidationError(
            f"Table '{table_name}' is missing key columns: {missing_keys}"
        )
    duplicated = df.duplicated(subset=key_columns, keep=False)
    if duplicated.any():
        duplicate_rows = df.loc[duplicated, key_columns]
        raise SchemaValidationError(
            f"Table '{table_name}' contains duplicate keys in {key_columns}: "
            f"{duplicate_rows.to_dict(orient='records')}"
        )
def validate_required_values(df: pd.DataFrame, table_name: str) -> None:
    if df.empty:
        return
    rules = get_table_rules(table_name)
    required_columns = rules.get("required", [])
    failures: list[str] = []
    for column in required_columns:
        if column not in df.columns:
            failures.append(f"Missing required column: {column}")
            continue
        empty_mask = df[column].fillna("").astype(str).str.strip() == ""
        if empty_mask.any():
            row_indexes = df.index[empty_mask].tolist()
            failures.append(
                f"Column '{column}' has empty values at rows {row_indexes}"
            )
    if failures:
        raise RecordValidationError(
            f"Table '{table_name}' failed required-value validation: {failures}"
        )
def validate_table(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    clean = prepare_table(df, table_name)
    validate_required_columns(clean, table_name)
    validate_required_values(clean, table_name)
    rules = get_table_rules(table_name)
    unique_key = rules.get("unique_key")
    if unique_key:
        validate_no_duplicate_keys(clean, list(unique_key), table_name)
    validate_foreign_keys(table_name, clean)
    return clean
