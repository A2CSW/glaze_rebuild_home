import pandas as pd
import glob

OUT_FILE = "migration/output/tanya_tracker_clean.csv"


def load():
    files = glob.glob("data/raw/payments_tracker/*")

    if not files:
        raise FileNotFoundError("No tracker file found in data/raw/payments_tracker")

    path = files[0]
    print("USING FILE:", path)

    if path.endswith(".csv"):
        return pd.read_csv(path)
    else:
        return pd.read_excel(path)


def clean_columns(df):
    df = df.copy()

    df.columns = [
        c.lower().strip().replace(" ", "_")
        for c in df.columns
    ]

    print("COLUMNS:", df.columns.tolist())
    return df


def basic_hygiene(df):
    df = df.copy()

    # drop fully empty rows
    df = df.dropna(how="all")

    # strip all string fields safely
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].astype(str).str.strip()

    return df


def main():
    df = load()
    df = clean_columns(df)
    df = basic_hygiene(df)

    print("ROWS:", len(df))
    print(df.head(20))

    df.to_csv(OUT_FILE, index=False)
    print("Saved →", OUT_FILE)


if __name__ == "__main__":
    main()
