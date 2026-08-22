import pandas as pd
import numpy as np
import streamlit as st

# ============================================================
# DATASET PATH
# ============================================================
DATA_PATH = r"C:\Users\Hp\Downloads\home credit\data\application_train.csv"
# ============================================================
# LOAD DATA
# ============================================================
def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    return df