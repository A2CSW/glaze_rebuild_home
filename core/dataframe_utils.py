from __future__ import annotations
import pandas as pd
def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a copy of the DataFrame with whitespace-stripped column names.
    """
    clean = df.copy()
    clean.columns = clean.columns.astype(str).str.strip()
    return clean
def ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Return a copy of the DataFrame with all required columns present.
    Missing columns are added with empty string values.
    Extra columns are preserved.
    """
    clean = df.copy()
    for column in columns:
        if column not in clean.columns:
            clean[column] = ""
    return clean
def reorder_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Return a DataFrame with schema columns first, followed by any extras.
    """
    clean = df.copy()
    leading = [c for c in columns if c in clean.columns]
    extras = [c for c in clean.columns if c not in leading]
    return clean[leading + extras]
def coerce_to_string_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Convert selected columns to strings while preserving empty values.
    """
    clean = df.copy()
    for column in columns:
        if column in clean.columns:
            clean[column] = clean[column].fillna("").astype(str)
    return clean
