"""UGR'16 feature encoding. Single source of truth for UGR16 feature matrices.
NetFlow fields: te,td,sa,da,sp,dp,pr,flg,fwd,stos,pkt,byt,label (+week).
pr (protocol) is DROPPED: string in july, destroyed to NaN in the august parquet
by an earlier numeric coercion, so not comparable across the pair (deviation).
Identifiers (IPs) and the timestamp are excluded. flg is categorical, one-hot
against a fixed vocabulary learned on source; the encoder normalizes numeric-
looking category values so int/float storage cannot mismatch."""
import numpy as np, pandas as pd

DROP    = ['te','sa','da','pr','label','week','partition']
NUMERIC = ['td','sp','dp','fwd','stos','pkt','byt']
CATEG   = ['flg']

def _cat(df, c):
    s = df[c]
    if pd.api.types.is_numeric_dtype(s):
        s = s.astype('Float64').astype('string').str.replace(r'\.0$', '', regex=True)
    else:
        s = s.astype('string').str.strip()
    return s.fillna('na').replace({'<NA>': 'na', 'nan': 'na', 'None': 'na', '': 'na'}).astype(str)

def numeric_frame(df):
    return df[NUMERIC].apply(pd.to_numeric, errors='coerce')

def build_vocab(df, top=20):
    return {c: list(_cat(df, c).value_counts().index[:top]) for c in CATEG}

def encode(df, vocab):
    Xn = numeric_frame(df).to_numpy(dtype=np.float64)
    Xn[~np.isfinite(Xn)] = np.nan
    cols, names = [Xn], list(NUMERIC)
    for c in CATEG:
        s = _cat(df, c)
        for v in vocab[c]:
            cols.append((s == v).to_numpy(dtype=np.float64)[:, None]); names.append(f'{c}={v}')
    return np.hstack(cols), names
