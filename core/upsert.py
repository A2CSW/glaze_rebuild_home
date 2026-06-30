from __future__ import annotations
import pandas as pd
from core.exceptions import ServiceError
from core.table_ops import build_exact_match_mask
def insert_row(df: pd.DataFrame, row: dict[str, str]) -> pd.DataFrame:
    return pd.concat([df, pd.DataFrame([row])], ignore_index=True)
def update_rows(
    df: pd.DataFrame,
    criteria: dict[str, str],
    updates: dict[str, str],
    require_match: bool = True,
) -> pd.DataFrame:
    clean = df.copy()
    if clean.empty:
        if require_match:
            raise ServiceError("Cannot update rows in an empty table.")
        return clean
    mask = build_exact_match_mask(clean, criteria)
    if require_match and not mask.any():
        crit = ", ".join(f"{k}={v}" for k, v in criteria.items())
        raise ServiceError(f"No matching rows found for update: {crit}")
    for key, value in updates.items():
        if key not in clean.columns:
            raise ServiceError(f"Cannot update missing column: {key}")
        clean.loc[mask, key] = str(value).strip()
    return clean
def delete_rows(
    df: pd.DataFrame,
    criteria: dict[str, str],
) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    mask = build_exact_match_mask(df, criteria)
    return df.loc[~mask].copy()
def replace_group(
    df: pd.DataFrame,
    criteria: dict[str, str],
    new_rows: list[dict[str, str]],
) -> pd.DataFrame:
    remaining = delete_rows(df, criteria)
    if not new_rows:
        return remaining.reset_index(drop=True)
    replacement_df = pd.DataFrame(new_rows)
    return pd.concat([remaining, replacement_df], ignore_index=True)
