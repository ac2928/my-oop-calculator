"""Read a CSV input source; choosing and performing math belong elsewhere."""

from pathlib import Path

import pandas as pd


def read_csv_values(path):
    frame = pd.read_csv(Path(path))           # DataFrame: a table
    if "value" not in frame.columns:
        raise ValueError("CSV must contain a column named value.")
    return frame["value"].tolist()            # Series -> plain list; validation happens later