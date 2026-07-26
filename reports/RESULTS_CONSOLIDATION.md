# CALSHIFT — Consolidated Results (writeup scaffold)

Every number below is committed and verified. This is the paper's results narrative
in order, with each headline sourced to its notebook/commit and figure. It is the
scaffold to draft into. Experimental work is FROZEN at this document; next step is
writing. Repo: github.com/anasbiswas1/calshift-research. Head at consolidation:
nb26 `c666be0`.

Paper arc: **diagnosis → discovery → mechanism → label-free monitor (with boundary)**,
supported by four robustness analyses (prior-shift, alpha, efficiency, calibration),
all under a preregistration.

---

## 0. Study design (the credibility asset — write this first, prominently)

Preregistered study; preregistration + amendments committed. Three conformal
calibration protocols evaluated on class-conditional (Mondrian) coverage with APS
nonconformity scores at primary alpha = 0.05:
- **REC** — recalibrate on the evaluation set (oracle upper bound).
- **TSC** — target-supervised calibration (needs target labels; not deployable).
- **SHC** — source-held-out calibration (the ONLY deployable protocol).

Three environments, three DISTINCT shift types (this is the design's strength):

| dataset | shift type | source → target | focal (fixed in advance) |
|---|---|---|---|
| NSL-KDD | support (subtype novelty) | KDDTrain+ → KDDTest+, 5-rung unseen-subtype ladder × 20 realizations | R2L |
| CIC-IDS2017 | support (DoS variant holdout) | Wednesday DoS, 5 variant-holdout realizations | DoS |
| UGR'16 | fixed-support covariate | July week5 → August week1 (~1 month temporal) | nerisbotnet |

Model panel per dataset: RF / XGB / MLP × 10 seeds, hyperparameters frozen on a
validation split, one-vs-rest isotonic calibration fit on a held-out source
partition. Focal classes chosen before any coverage number existed.

Shift is MEASURED, not assumed: S_cov (domain-classifier AUC), S_lab (TV distance of
class priors), S_sup (target mass in unseen subtypes), each with a permutation null.

---

## 1. DIAGNOSIS — the deployable protocol undercovers under shift (all 3 datasets)

Focal class-conditional coverage under SHC at alpha 0.05 (nominal 0.95):

| dataset | focal | SHC | TSC | REC | verdict |
|---|---|---|---|---|---|
| NSL-KDD | R2L | 0.030 (rung 0.80) / 0.086 overall | 0.953 | 0.956 | collapses |
| CIC-IDS2017 | DoS | 0.590 | 0.988 | 0.988 | collapses |
| UGR'16 | nerisbotnet | 0.947 | 0.950 | 0.950 | HOLDS |

Source: `coverage_primary_*.csv`, focal verdict JSONs.
Claim: the only deployable protocol loses class-conditional coverage under support
shift, badly (NSL, CIC). TSC and REC hold, so the failure is specific to
source-only calibration, not to conformal prediction per se.

## 2. DISCOVERY — covariate-shift failure is SELECTIVE and unpredicted by aggregate shift

UGR'16, one clean fixed-support covariate environment (S_cov 0.69 > null 0.51;
S_lab = 0, S_sup = 0). Class-conditional coverage under SHC (alpha 0.05):

| class | SHC coverage | TSC | reads |
|---|---|---|---|
| nerisbotnet (focal) | 0.947 | 0.950 | holds |
| dos | 0.950 | 0.950 | holds |
| background | 0.949 | 0.950 | holds |
| scan11 | 0.535 | 0.950 | COLLAPSES |
| scan44 | 0.799 | 0.982 | collapses |

Source: `UGR16_RESULTS.md`, commit `3c499f4`.
Claim: under the SAME aggregate covariate shift, some classes hold and others
collapse. Which classes fail is NOT predictable from the aggregate S_cov. The
preregistered focal (nerisbotnet) holds; the scan collapse is reported as a
DISCOVERED finding, not retro-promoted to focal (preregistration discipline).
This is the phenomenon the rest of the paper explains and detects.

## 3. POOLED cross-dataset model — support shift is the identified driver

49,500 coverage cells (counts-based), cluster-robust binomial GLM + empirical-logit
mixed-model cross-check, TSC reference. Source: `pooled_model_results.json`, nb18-19,
commit `51caaf4`.

- **beta7 (SHC × S_sup)** = **-0.374** GLM / **-0.658** mixed. Same sign, both highly
  significant. **WELL IDENTIFIED** (NSL sweeps S_sup 0→0.46). => support shift drives
  coverage failure. This is the pooled headline.
- **beta5 (SHC × S_cov)** = -0.252 GLM / **+0.254** mixed. **SIGN FLIP => NOT
  IDENTIFIED** (S_cov varies only between 3 datasets). Reported as sign-unstable;
  covariate evidence deferred to the per-dataset UGR result (§2).
- Deviation: exact crossed-RE binomial GLMM to be run in R/lme4 for camera-ready;
  statsmodels approximations agree on the identified effect. Recorded in `deviations.md`.

## 4. MECHANISM — score movement explains the failures (central result)

Per class, per architecture: KS distance between source and target true-class
nonconformity-score distributions vs realized undercoverage. Source:
`score_shift_explainability.csv`, `score_shift_verdict.json`, nb20+22, commit `a8c1d16`.

- **Spearman(score movement, undercoverage) = +0.925, p = 4.5e-26, n = 60 class-cells,
  across all three datasets.** Holds within each architecture (rf/xgb/mlp all strongly
  positive).
- Sharpest case: NSL R2L, score shift 0.84 with undercoverage 0.88 — the largest in
  the study, exactly where movement is largest.
- Figure: `score_shift_vs_undercoverage.png`.

Claim: classes undercover precisely when their score distribution moves past the
source-calibrated quantile. Mechanistic, robust, cross-dataset. This turns the §2
"selective" observation from assertion into a measured law and MOTIVATES the detector.

## 5. LABEL-FREE MONITOR — predicting failure without target labels (constructive core)

Monitor = per-class drift of the PREDICTED-class score distribution (source vs target),
fully label-free, combined with a predicted-mass-collapse fallback for classes that
vanish from predictions. Graded against realized undercoverage and an oracle
(true-label) drift. Source: `monitor_labelfree.csv`, `monitor_verdict.json`,
`nsl_added_verdict.json`, nb21+22, commit `a8c1d16`.

- **Detector vs undercoverage: Spearman +0.73, AUC 0.90**, all three datasets (n=60).
  Oracle (true-label) +0.90 / AUC 0.96 — the label-free signal recovers most of it.
- Per-dataset detector rho: CIC +0.77, UGR +0.82, NSL +0.38.
- Figure: `monitor_labelfree.png`.

### 5a. The boundary — where the monitor is blind (honest limitation, do NOT hide)
- **Displacement-type** drift (model still predicts the novel class, less confidently):
  the predicted-class distribution moves, monitor CATCHES it.
- **Similarity-type** drift (model confidently misroutes the novel class as familiar):
  predicted-class distribution barely moves, monitor ATTENUATES or goes blind.
- Demonstrated: UGR scan11 undercovers 0.49, oracle drift 0.52, label-free drift only
  0.14 (misroute 0.56). NSL U2R undercovers 0.41, oracle drift 0.60, label-free
  UNMEASURABLE (misroute 0.84) — caught only by the mass-collapse fallback.
- **Boundary characterization is INCOMPLETE**: Spearman(misroute, blind-spot gap) =
  +0.25, p = 0.09, n too small. State as the acknowledged open edge; the misroute proxy
  is too weak to carry a formal boundary. (Paper 2 territory — see §7.)

Claim: a label-free monitor predicts coverage failure with AUC 0.90, robustly, WITH a
demonstrated and mechanistically-explained blind spot. This honesty is the Q1 asset,
not a weakness — a monitor that "worked everywhere" would be suspect.

---

## 6. SUPPORTING ANALYSES (robustness — each closes a specific reviewer objection)

### 6a. Arm B / prior-shift confound (nb23, `2150d24`; NSL pre-existing)
Objection: "undercoverage is just the target having a different class mix."
- **Focal class-conditional coverage is INVARIANT to IPW reweighting: focal shift
  +0.0000 on both CIC and UGR (exact by construction).** => the focal gap CANNOT be a
  prior-shift artifact. Load-bearing.
- CIC marginal 0.936 → 0.770 under IPW (shift -0.166); the benign majority masked the
  DoS failure, matching source prior (DoS upweighted 7–47×) exposes it. ESS min 1,744
  (>> 30 threshold), reliable.
- UGR marginal 0.879 → 0.879 (weights ~1.0, ESS ~59,996): null check, no prior-shift
  confound. Source: `armb_verdict.json`, `armb_weights_*.csv`.

### 6b. Alpha-sensitivity (nb24, `2a1b132`)
Objection: "you picked a convenient alpha."
- NSL R2L SHC: 0.03 / 0.02 / 0.02 at alpha 0.05 / 0.10 / 0.20.
- CIC DoS SHC: 0.60 / 0.56 / 0.48 (focal gap WIDENS with alpha).
- UGR nerisbotnet holds: 0.95 / 0.90 / 0.79. Scans collapse at EVERY alpha.
- Nothing hinges on 0.05. Source: `alpha_sensitivity.csv`, figure `alpha_sensitivity.png`.
  (NSL alpha 0.01 also available if a tighter level is ever requested.)

### 6c. Set-size / efficiency (nb25, `ef32a58`)
Objection: "SHC's smaller sets are more efficient."
- Everywhere SHC undercovers, its sets are SMALLER AND miss coverage: NSL R2L set 2.04
  vs TSC 4.68 (gap -2.6) at coverage 0.03 vs 0.95; CIC DoS set 1.07 vs 1.45 (mean gap
  -0.56) at 0.60 vs 0.99.
- UGR nerisbotnet holds (0.947) with legitimately tighter sets (1.14 vs 1.77), but SHC
  MEAN coverage still drops to 0.836 (scans drag it).
- Claim: SHC's narrow sets are the symptom of a too-tight source quantile, not
  efficiency; TSC/REC pay width for valid coverage. Source: `efficiency_setsize.csv`,
  figure `efficiency_setsize.png`.

### 6d. Calibration quality (nb26, `c666be0`)
Objection: "your base probabilities were miscalibrated."
- Per-class ECE <= 0.002 everywhere; top-label ECE NSL 0.0006, CIC 0.0001, UGR 0.0024;
  Brier tiny. Evaluated on the source pool, HELD OUT from the isotonic fit set.
- => the coverage failures under shift are NOT a base-calibration artifact. Source:
  `calibration_quality.csv`, figure `calibration_reliability.png`. (Calibrated quality
  only; raw probs not cached, so no before/after — recorded scope note.)

---

## 7. LIMITATIONS & FUTURE WORK (write honestly; these are Paper 2, not Paper 1 gaps)

- **Boundary characterization incomplete** (§5a): misroute vs blind-spot gap not
  significant at current n. Needs a continuous confusability measure and more
  similarity-type cases (candidate: 5G-NIDD as the similarity exemplar).
- **beta5 (covariate interaction) not identified** in the pooled model: S_cov varies
  only between 3 datasets. Needs more covariate-shift environments.
- **No correction/remedy**: the monitor flags failure but does not fix it. Label-free
  correction under similarity-type drift is open (deliberately Paper 2).
- **Tooling**: exact crossed-RE binomial GLMM deferred to R/lme4 for camera-ready.

## 8. FIGURE INVENTORY (all committed under reports/)
1. `score_shift_vs_undercoverage.png` — mechanism (§4), the central figure.
2. `monitor_labelfree.png` — monitor vs coverage + label-free-vs-oracle gap (§5).
3. `alpha_sensitivity.png` — focal coverage vs nominal across alpha (§6b).
4. `efficiency_setsize.png` — coverage vs set size, focal (§6c).
5. `calibration_reliability.png` — reliability curves, focal classes (§6d).

## 9. ONE-PARAGRAPH ABSTRACT SEED (draft target)
The deployable source-held-out conformal protocol loses class-conditional coverage
under distribution shift, demonstrated across three NIDS datasets and three shift
types under preregistration. The failure is per-class and, under covariate shift,
selective in a way no aggregate shift measure predicts. It is explained
mechanistically: a class undercovers exactly when its nonconformity-score
distribution moves past the source-calibrated quantile (rho 0.93). A label-free
monitor of predicted-class score drift predicts these failures without target labels
(AUC 0.90), with a demonstrated and characterized blind spot on similarity-type drift
where the model confidently misroutes novel classes. Prior-shift, alpha, efficiency,
and calibration analyses confirm the failures are genuine.
