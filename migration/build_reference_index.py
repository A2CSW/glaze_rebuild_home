import pandas as pd
from difflib import SequenceMatcher

BANK_FILE = "migration/output/transactions_clean.csv"
TRACKER_FILE = "migration/output/tanya_tracker_clean.csv"
OUT_FILE = "migration/output/reference_index.csv"


def similarity(a, b):
    if pd.isna(a) or pd.isna(b):
        return 0.0
    return SequenceMatcher(None, str(a).lower(), str(b).lower()).ratio()


def load_data():
    bank = pd.read_csv(BANK_FILE)
    tracker = pd.read_csv(TRACKER_FILE)
    return bank, tracker


def extract_bank_refs(bank):
    if "transaction description" in bank.columns:
        col = "transaction description"
    elif "description" in bank.columns:
        col = "description"
    else:
        raise ValueError(f"No usable reference column found: {bank.columns.tolist()}")

    return (
        bank[[col]]
        .dropna()
        .drop_duplicates()
        .rename(columns={col: "transaction_description"})
    )


def extract_tracker_refs(tracker):
    cols = [c for c in tracker.columns if "note" in c or "method" in c]

    if not cols:
        return pd.DataFrame(columns=["reference"])

    refs = tracker[cols].fillna("").astype(str)
    refs["reference"] = refs.apply(lambda r: " ".join(r.values), axis=1)

    return refs[["reference"]].drop_duplicates()


def build_index(bank_refs, tracker_refs):
    rows = []

    for _, b in bank_refs.iterrows():
        b_ref = b["transaction_description"]

        best_score = 0.0
        best_match = ""

        for _, t in tracker_refs.iterrows():
            score = similarity(b_ref, t["reference"])

            if score > best_score:
                best_score = score
                best_match = t["reference"]

        rows.append({
            "bank_reference": b_ref,
            "tracker_reference": best_match,
            "similarity_score": best_score
        })

    df = pd.DataFrame(rows)

    high_cut = df["similarity_score"].quantile(0.95)
    medium_cut = df["similarity_score"].quantile(0.80)

    def classify(x):
        if x >= high_cut:
            return "high"
        if x >= medium_cut:
            return "medium"
        return "low"

    df["confidence"] = df["similarity_score"].apply(classify)

    return df


def main():
    bank, tracker = load_data()

    bank_refs = extract_bank_refs(bank)
    tracker_refs = extract_tracker_refs(tracker)

    index = build_index(bank_refs, tracker_refs)

    print(index["confidence"].value_counts())

    index.to_csv(OUT_FILE, index=False)
    print("Saved →", OUT_FILE)


if __name__ == "__main__":
    main()
