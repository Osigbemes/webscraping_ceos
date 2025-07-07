import pandas as pd
import unicodedata
import os

def clean_unicode(text):
    if isinstance(text, str):
        return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return text

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        df[col] = df[col].map(clean_unicode)
    return df

def export_to_csv(records: list, path: str = "output/output.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df = pd.DataFrame(records)
    df = clean_dataframe(df)
    df.to_csv(path, index=False, encoding="utf-8")

def export_to_stata(records: list, path: str = "output/output.dta"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df = pd.DataFrame(records)
    df = clean_dataframe(df)
    df.to_stata(path, write_index=False, version=117)
