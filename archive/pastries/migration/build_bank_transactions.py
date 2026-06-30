import pandas as pd
import glob

BANK_PATH = BANK_PATH = "data/raw/bank/*.csv"  # adjust if needed
OUT_FILE = "migration/output/transactions_raw.csv"

def load_bank_files():
    files = glob.glob(BANK_PATH)

    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df["source_file"] = f
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)

def main():
    df = load_bank_files()

    print("ROWS:", len(df))
    print(df.head(20))

    df.to_csv(OUT_FILE, index=False)
    print("Saved →", OUT_FILE)

if __name__ == "__main__":
    main()
