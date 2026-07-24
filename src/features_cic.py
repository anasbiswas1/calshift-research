"""CIC-IDS2017 feature encoding. Single source of truth for CIC feature matrices."""
import numpy as np

META = ['label_raw', 'label', 'subtype', 'day', 'source_file',
        'attempted_relabelled_benign', 'partition']
ID_LIKE = ['Flow ID', 'Src IP', 'Source IP', 'Dst IP', 'Destination IP',
           'Src Port', 'Source Port', 'Dst Port', 'Destination Port',
           'Protocol', 'Timestamp']
INTERNAL = ['_capture_ts', '_order', '_block']

def feature_cols(df):
    drop = set(META) | set(ID_LIKE) | set(INTERNAL)
    cols = [c for c in df.columns if c not in drop]
    return df[cols].select_dtypes(include=[np.number]).columns.tolist()

def matrix(df, cols):
    X = df[cols].to_numpy(dtype=np.float64)
    X[~np.isfinite(X)] = np.nan
    return X
