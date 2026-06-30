from __future__ import annotations
import shutil
from datetime import datetime
from pathlib import Path
from config.settings import BACKUP_DIR, ensure_directories
from core.logging_config import get_logger
logger = get_logger(__name__)
def backup_file(path: Path) -> Path | None:
    """
    Create a timestamped backup copy of a file if it exists.
    Returns the backup path, or None if the source file does not exist.
    """
    path = Path(path)
    if not path.exists():
        return None
    ensure_directories()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup_name = f"{path.stem}__{timestamp}{path.suffix}"
    backup_path = BACKUP_DIR / backup_name
    shutil.copy2(path, backup_path)
    logger.info("Created backup for %s at %s", path, backup_path)
    return backup_path
