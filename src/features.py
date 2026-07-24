"""Canonical feature encoding for NSL-KDD. Single source of truth."""
import numpy as np, pandas as pd

CAT_COLS = ["protocol_type", "service", "flag"]
DROP_COLS = ("label", "subtype", "partition", "is_unseen")

def feature_cols(df):
    return [c for c in df.columns if c not in DROP_COLS]

def fit_categories(*frames):
    cats = {}
    for c in CAT_COLS:
        vals = pd.concat([f[c].astype(str) for f in frames])
        cats[c] = pd.Categorical(vals).categories
    return cats

def encode(df, cols, cats):
    X = df[cols].copy()
    for c in CAT_COLS:
        X[c] = pd.Categorical(X[c].astype(str), categories=cats[c]).codes
    return X.astype(np.float32).to_numpy()
