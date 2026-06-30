from __future__ import annotations
import pandas as pd
from core.exceptions import ServiceError
def build_exact_match_mask(
    df: pd.DataFrame,
    criteria: dict[str, str],
) -> pd.Series:
    if df.empty:
        return pd.Series(dtype=bool)
    mask = pd.Series(True, index=df.index)
    for column, expected in criteria.items():
        if column not in df.columns:
            raise ServiceError(f"Missing column for match operation: {column}")
        mask = mask & (df[column].astype(str).str.strip() == str(expected).strip())
    return mask
def ensure_record_exists(
    df: pd.DataFrame,
    criteria: dict[str, str],
    entity_name: str,
) -> None:
    mask = build_exact_match_mask(df, criteria)
    if df.empty or not mask.any():
        crit = ", ".join(f"{k}={v}" for k, v in criteria.items())
        raise ServiceError(f"{entity_name} not found: {crit}")
def ensure_record_not_exists(
    df: pd.DataFrame,
    criteria: dict[str, str],
    entity_name: str,
) -> None:
    if df.empty:
        return
    mask = build_exact_match_mask(df, criteria)
    if mask.any():
        crit = ", ".join(f"{k}={v}" for k, v in criteria.items())
        raise ServiceError(f"{entity_name} already exists: {crit}")
