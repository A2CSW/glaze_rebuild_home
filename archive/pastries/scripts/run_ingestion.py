import pandas as pd
from engine.ingestion.ingestion_engine import IngestionEngine


BANK_FILE = "migration/output/transactions_clean.csv"
TRACKER_FILE = "migration/output/tanya_tracker_clean.csv"
OUT_FILE = "migration/output/ingestion_output.csv"


def main():
    bank = pd.read_csv(BANK_FILE)
    tracker = pd.read_csv(TRACKER_FILE)

    engine = IngestionEngine(bank, tracker)

    tracker_results = engine.reconcile_tracker_to_bank()
    bank_results = engine.reconcile_bank_to_tracker()

    all_results = tracker_results + bank_results

    df = pd.DataFrame(all_results)

    print("TRACKER RESULTS:", len(tracker_results))
    print("BANK RESULTS:", len(bank_results))
    print("TOTAL:", len(df))

    print(df["match_status"].value_counts())

    df.to_csv(OUT_FILE, index=False)
    print("Saved →", OUT_FILE)


if __name__ == "__main__":
    main()
