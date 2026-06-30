import pandas as pd
from engine.state.ingestion_contract import LedgerEntry


class IngestionEngine:
    """
    SINGLE AUTHORITY INGESTION LAYER

    Rules:
    - Tanya Tracker is primary truth
    - Bank confirms tracker
    - No reverse inference allowed
    """

    def __init__(self, bank_df: pd.DataFrame, tracker_df: pd.DataFrame):
        self.bank = bank_df.copy()
        self.tracker = tracker_df.copy()

    def reconcile_tracker_to_bank(self):
        results = []

        for _, t in self.tracker.iterrows():

            t_ref = str(t.get("reference", "")).lower()
            t_student = t.get("student_id", None)
            t_amount = float(t.get("amount", 0))
            t_date = t.get("date", "")

            match = self._find_bank_match(t_ref, t_amount)

            if match is None:
                results.append({
                    "source": "tracker",
                    "student_id": t_student,
                    "amount": t_amount,
                    "date": t_date,
                    "description": t_ref,
                    "match_status": "tracker_missing_bank_match",
                    "confidence": 0.0
                })
                continue

            results.append({
                "source": "tracker",
                "student_id": t_student,
                "amount": t_amount,
                "date": t_date,
                "description": t_ref,
                "match_status": "reconciled",
                "bank_reference": match["description"],
                "confidence": 1.0
            })

        return results

    def reconcile_bank_to_tracker(self):
        results = []

        for _, b in self.bank.iterrows():

            b_desc = str(b.get("transaction description", "")).lower()
            b_amount = float(b.get("amount_signed", 0))
            b_date = b.get("transaction date", "")

            match = self._find_tracker_match(b_desc, b_amount)

            if match is None:
                results.append({
                    "source": "bank",
                    "student_id": None,
                    "amount": b_amount,
                    "date": b_date,
                    "description": b_desc,
                    "match_status": "bank_unmatched",
                    "confidence": 0.0
                })
                continue

            results.append({
                "source": "bank",
                "student_id": match.get("student_id"),
                "amount": b_amount,
                "date": b_date,
                "description": b_desc,
                "match_status": "reconciled",
                "tracker_reference": match.get("reference"),
                "confidence": 1.0
            })

        return results

    def _find_bank_match(self, tracker_ref, amount):
        for _, b in self.bank.iterrows():
            desc = str(b.get("transaction description", "")).lower()
            amt = float(b.get("amount_signed", 0))

            if abs(amt - amount) < 0.01 and tracker_ref in desc:
                return {"description": desc}

        return None

    def _find_tracker_match(self, bank_desc, amount):
        for _, t in self.tracker.iterrows():
            ref = str(t.get("reference", "")).lower()
            amt = float(t.get("amount", 0))

            if abs(amt - amount) < 0.01 and ref in bank_desc:
                return {
                    "student_id": t.get("student_id"),
                    "reference": ref
                }

        return None
