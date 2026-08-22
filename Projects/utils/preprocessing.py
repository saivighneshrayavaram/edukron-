import pandas as pd
import numpy as np


def clean_data(df):

    df = df.copy()

    # Replace special employment value
    if "DAYS_EMPLOYED" in df.columns:
        df["DAYS_EMPLOYED"] = df["DAYS_EMPLOYED"].replace(
            365243, np.nan
        )

    return df