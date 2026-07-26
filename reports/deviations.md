
## notebook 03
- S_cov subsample reduced from the preregistered 20000 per side to 2000, because Amendment 1 fixed D_eval at 2340 rows and 20000 per side is unattainable on the evaluation side. Recorded in Amendment 2 B5.

## notebook 06
- Amendment 3 C4 specifies a beta-binomial GLMM in glmmTMB. Substituted a binomial GLM with cluster-robust standard errors clustered on ladder realization, because no pure-Python package supports the specified structure on the count interface. Architecture and class enter as fixed effects. The Gaussian secondary model retains random intercepts.

## nb10 note: amendments 7-8 committed within 5b5cfc5 (nb09 message); provenance intact, before any coverage.

## nb11 - permutation null S_cov uses single-split AUC at 8k/side for tractability (measured S_cov is 5-fold at 20k/side per section 9). Logged before any coverage.

## nb12 - CIC used architecture-appropriate FIXED hyperparameters (RF/XGB/MLP) chosen for dataset scale, not a per-dataset macro-F1 grid (section 5), to bound compute. Before any coverage.

## nb15 (UGR16) - source july_week5 is the uniqblacklistremoved variant, target august_week1 is the raw full file; blacklist dropped (not comparable). pr (protocol) dropped from features: string in july but destroyed to NaN in the august parquet by an earlier numeric coercion, so not comparable; S_cov computed on 9 flow features. Focal = nerisbotnet by true rarity, not the 50k caps. All before any coverage.
