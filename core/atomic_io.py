from __future__ import annotations
import os
import tempfile
from pathlib import Path
from typing import Any
import pandas as pd
from config.settings import DEFAULT_ENCODING
from core.exceptions import DataLoadError, DataSaveError
from core.logging_config import get_logger
logger = get_logger(__name__)
def atomic_write_csv(
    df: pd.DataFrame,
    path: Path,
    **csv_kwargs: Any,
) -> None:
    """
    Write a DataFrame to CSV using a temp-file-then-replace pattern.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    csv_kwargs.setdefault("index", False)
    csv_kwargs.setdefault("encoding", DEFAULT_ENCODING)
    temp_path: Path | None = None
    try:
        fd, raw_temp_path = tempfile.mkstemp(
            suffix=".tmp",
            prefix=f"{path.stem}_",
            dir=path.parent,
        )
        os.close(fd)
        temp_path = Path(raw_temp_path)
        df.to_csv(temp_path, **csv_kwargs)
        os.replace(temp_path, path)
        logger.info("Saved CSV atomically to %s (%s rows)", path, len(df))
    except Exception as exc:
        if temp_path and temp_path.exists():
            temp_path.unlink(missing_ok=True)
        logger.exception("Failed atomic write for %s", path)
        raise DataSaveError(f"Failed to save data to {path}") from exc
def safe_read_csv(
    path: Path,
    default_columns: list[str] | None = None,
    **csv_kwargs: Any,
) -> pd.DataFrame:
    """
    Read a CSV safely.
    Behavior:
    - If file does not exist: return an empty DataFrame with default columns.
    - If file exists but cannot be parsed: raise DataLoadError.
    """
    path = Path(path)
    csv_kwargs.setdefault("encoding", DEFAULT_ENCODING)
    if not path.exists():
        logger.warning("CSV file not found: %s", path)
        return pd.DataFrame(columns=default_columns or [])
    try:
        df = pd.read_csv(path, **csv_kwargs)
        logger.info("Loaded CSV from %s (%s rows)", path, len(df))
        return df
    except Exception as exc:
        logger.exception("Failed to read CSV from %s", path)
        raise DataLoadError(f"Failed to load data from {path}") from exc
