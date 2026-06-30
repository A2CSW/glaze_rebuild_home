from dataclasses import dataclass
from typing import Optional


@dataclass
class LedgerEntry:
    source: str
    student_id: Optional[str]
    amount: float
    date: str
    description: str
    match_status: str
    confidence: float = 0.0
