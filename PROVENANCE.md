# Provenance of the preregistration

## Disclosure

`preregistration.md` and Amendments 1 and 2 were authored before the notebooks
that implement them, but through a workflow lapse were not committed to this
repository until after `3d7818a` (notebook 05, the first commit containing
coverage results). Amendment 3 was committed at `cb09675` on the day it was
written. This is disclosed rather than presented as a clean timeline.

## Evidence that the specification preceded the results

The specification is encoded in code committed well before any outcome existed.

- `2458ca9` (notebook 01, first project commit) adds `src/config.py`, which sets
  SEEDS, ALPHA_PRIMARY, SPLIT_FRACTIONS, min_calib_n, SCOV_SUBSAMPLE_PER_SIDE,
  PERMUTATION_NULL_DRAWS, N_MATCHED_DRAWS, N_LADDER_REALIZATIONS,
  MIN_ESS_FOCAL_CLASS and PRACTICAL_COVERAGE_DROP, each annotated with the
  preregistration section it derives from.
- `8b12467` (notebook 02) applies the section 12 focal-class rule and the
  section 7.6 feasibility rule, and records the focal class before any coverage
  existed.
- `9fa0aaa` (notebook 03) cites "Amendment 1 A3.2" and "Amendment 2 B5" by
  section, with the rung fractions and the 2,000-per-side subsample those
  sections specify.
- `0e3e6d4` (notebook 04) records model decisions before fitting.
- `3d7818a` (notebook 05) is the first commit containing any coverage number.

## Deviation log

Recorded in `reports/deviations.md`.
