"""Project configuration. Values fixed by preregistration.md; do not tune."""
from pathlib import Path
import math

DRIVE_ROOT   = Path("/content/drive/MyDrive")
PARENT_DIR   = DRIVE_ROOT / "CALSHIFT_Research"
PROJECT_ROOT = PARENT_DIR / "calshift-research"
DATASETS_DIR = DRIVE_ROOT / "NIDS_Datasets"

DATA_DIR    = PROJECT_ROOT / "data"
INTERIM_DIR = DATA_DIR / "interim"
PROC_DIR    = DATA_DIR / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = PROJECT_ROOT / "figures"

# preregistration section 5
SEEDS = [42, 1337, 2024, 7, 91, 512, 6021, 88, 3407, 12345]

# preregistration section 7.5
ALPHA_PRIMARY     = 0.05
ALPHA_SENSITIVITY = [0.10, 0.20]
ALPHA_CONDITIONAL = [0.01]

# preregistration section 4, stratified split of the SOURCE partition
SPLIT_FRACTIONS = {"train": 0.60, "val": 0.10, "probcal": 0.15, "source_cal_pool": 0.15}

# preregistration section 7.6
def min_calib_n(alpha):
    return math.ceil(1.0 / alpha) - 1

# preregistration section 9
SCOV_SUBSAMPLE_PER_SIDE = 20000
PERMUTATION_NULL_DRAWS  = 200
PERMUTATION_NULL_Q      = 0.95

# preregistration sections 8.1 and 10.1
N_MATCHED_DRAWS       = 10
N_LADDER_REALIZATIONS = {"nslkdd": 20, "cicids2017": 5, "ugr16": 5, "ciciot2023": 5}

# preregistration section 10.2
MIN_ESS_FOCAL_CLASS = 30

# preregistration section 13.1
PRACTICAL_COVERAGE_DROP = 0.05

TRAIN_ROW_CAP = 2000000

CANONICAL_CLASSES = ["Normal", "DoS", "Probe", "R2L", "U2R"]
