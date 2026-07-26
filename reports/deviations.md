
## notebook 03
- S_cov subsample reduced from the preregistered 20000 per side to 2000, because Amendment 1 fixed D_eval at 2340 rows and 20000 per side is unattainable on the evaluation side. Recorded in Amendment 2 B5.

## notebook 06
- Amendment 3 C4 specifies a beta-binomial GLMM in glmmTMB. Substituted a binomial GLM with cluster-robust standard errors clustered on ladder realization, because no pure-Python package supports the specified structure on the count interface. Architecture and class enter as fixed effects. The Gaussian secondary model retains random intercepts.

## nb10 note: amendments 7-8 committed within 5b5cfc5 (nb09 message); provenance intact, before any coverage.

## nb11 - permutation null S_cov uses single-split AUC at 8k/side for tractability (measured S_cov is 5-fold at 20k/side per section 9). Logged before any coverage.

## nb12 - CIC used architecture-appropriate FIXED hyperparameters (RF/XGB/MLP) chosen for dataset scale, not a per-dataset macro-F1 grid (section 5), to bound compute. Before any coverage.

## nb15 (UGR16) - source july_week5 is the uniqblacklistremoved variant, target august_week1 is the raw full file; blacklist dropped (not comparable). pr (protocol) dropped from features: string in july but destroyed to NaN in the august parquet by an earlier numeric coercion, so not comparable; S_cov computed on 9 flow features. Focal = nerisbotnet by true rarity, not the 50k caps. All before any coverage.

## nb16 (UGR16) - fixed architecture-appropriate hyperparameters (RF/XGB/MLP), not a per-dataset macro-F1 grid (section 5), to bound compute; before any coverage.

## nb19 - pooled model: the preregistered crossed-random-effects binomial GLMM was approximated by a cluster-robust binomial GLM on counts plus an empirical-logit mixed model, because that GLMM is not reliably fittable in Python; exact lme4/glmer fit deferred to R for the camera-ready. S_cov is between-dataset only (3 clusters) so the SHC x S_cov interaction (beta5) is weakly identified and reported as suggestive; the SHC x S_sup interaction (beta7) is well identified within NSL.

## nb31 (CIC-IoT-2023) - subsampling
Per-label cap of 60,000 rows applied as a streaming keep-fraction, rather than proportional
stratified subsampling to a row budget (section 5). Retains every rare label in full; the
working frame is 1,510,142 rows, 3.23 per cent of the release. This moves the class prior:
the focal class Web goes from 0.053 per cent of the raw capture to 1.644 per cent of the
working frame, an enrichment of about 31x. Both priors are recorded in the focal-class record.
The enrichment makes the focal class easier for the classifier than it would be in deployment,
so any focal coverage failure measured here is conservative. Recorded before any coverage.

## nb31 (CIC-IoT-2023) - focal-class rule extension
Section 12 selects the rarest attack family satisfying section 7.6. Extended to require at
least two subtypes, because a single-subtype family cannot be shifted by variant holdout while
remaining feasible under SHC (the CIC-IDS2017 lesson, Amendment 9). BruteForce is rarer
(1,959 source calibration points) but single-subtype, so the focal class is Web (3,720 points,
six subtypes). Recorded before any coverage. See Amendment 10 A10.4.

## Primary analysis reassignment (manuscript-level, applies to all environments)
The preregistered primary test is beta5, the SHC x S_cov interaction in the pooled
cross-dataset model (section 11.2, section 13.1). That interaction is not identified at this
design: S_cov varies almost entirely between dataset clusters and the coefficient is
sign-unstable across estimators. The manuscript therefore reports the pooled model as
secondary and descriptive, and rests its causal claim on the within-dataset dose-response.
This is a departure from section 11 and is disclosed as such in the paper.

## nb33 (CIC-IoT-2023) - hyperparameters
Fixed architecture-appropriate hyperparameters (RF/XGB/MLP) chosen for dataset scale rather than a per-dataset macro-F1 selection grid (section 5), to bound compute on a 634,309-row training partition. Same deviation already logged for CIC-IDS2017 (nb12) and UGR16 (nb16). Recorded before any coverage.
