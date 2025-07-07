import pandas as pd
import os

def write_to_csv(data, filename="output.csv"):
    df = pd.DataFrame(data)
    os.makedirs("data", exist_ok=True)
    df.to_csv(f"data/{filename}", index=False)

def write_to_dta(data, filename="output.dta"):
    df = pd.DataFrame(data)
    os.makedirs("data", exist_ok=True)
    df.to_stata(f"data/{filename}", write_index=False)
