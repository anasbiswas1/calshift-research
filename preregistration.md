# Preregistration: Calibration Source and Distribution Shift in Conformal Trust Layers for Network Intrusion Detection

**Status:** binding on commit. Timestamped in the project repository before any E0 result is computed.
**Supersedes:** research plan v5, sections 0.6, 0.8, 2 and E0.
**Deviations policy:** §16.

---

## 1. Scope

This document fixes every analysis decision for the primary experiment (E0) and states the binding rules for the dependent experiments (E1 to E8). Decisions not written here are exploratory by definition and will be labelled as such in any resulting paper.

The paper's central claim concerns the verifiability of other researchers' analysis decisions. That claim is untenable from a study whose own decisions were made after seeing outcomes. This document exists to make the claim tenable.

---

## 2. Research questions

**RQ1.** Does the empirical coverage of a conformal trust layer depend on whether the conformal quantile was calibrated on target-distribution data or on source-distribution data, holding the base model, the probability calibrator, the nonconformity score, the calibration sample size, and the evaluation sample fixed?

**RQ2.** If it does, is the dependence attributable to prior shift, covariate shift, or support shift, and does it concentrate in minority attack classes?

**RQ3.** Which published remedies close the gap, and what information does each require at deployment time?

**RQ4.** Do per-alert trust scores retain discriminative value in the affected class cells, measured at fixed analyst workload?

**RQ5.** Can affected predictions be identified without target labels, and under what boundary condition?

RQ1 and RQ2 are confirmatory. RQ3 to RQ5 are structured but not confirmatory; their hypotheses are stated in §13 with success criteria.

---

## 3. Datasets

Four core, one optional. The claim text will say **four datasets** plus one optional replication, correcting the "five datasets" phrasing in plan v5.

| Dataset | Version | Role |
|---|---|---|
| NSL-KDD | KDDTrain+ / KDDTest+ | Deliberate benchmark mismatch |
| CIC-IDS2017 | WTMC-2021 corrected (Engelen et al. 2021), fixed CICFlowMeter | Session and day aware |
| UGR'16 | v2 convention, calibration March to May only | Long-duration temporal |
| CIC-IoT-2023 | CSV release | Modern heterogeneous, family holdout |
| NF-CSE-CIC-IDS2018-v3 | optional | Second controlled temporal environment |

UNSW-NB15 is dropped from the core portfolio. Its role in earlier plans was a no-shift control under random splitting, which §8's permutation null now supplies within every dataset. Retaining it would add a dataset without adding a shift mechanism.

UGR'16 is subsampled to 5 million flows per weekly window at two independent sampling rates. Both are analysed; disagreement between them is reported.

---

## 4. Partitions

Five disjoint partitions, drawn from the source distribution unless stated:

```
D_train      base model fitting
D_val        model selection and hyperparameters
D_probcal    probability calibrator
D_confcal    conformal quantile
D_eval       evaluation
```

`D_train`, `D_val` and `D_probcal` are always source-drawn and are identical across all protocols and arms. Only `D_confcal` varies between protocols. `D_eval` is fixed within a ladder level and identical across protocols.

Split proportions from the source partition: 60 / 10 / 15 / 15 for train, val, probcal, and the source calibration pool from which `S_cal` is drawn. Stratified by class.

---

## 5. Base models

Three architectures: Random Forest, XGBoost, and a feed-forward DNN. Hyperparameters selected once per (dataset, architecture) on `D_val` by macro-F1, then frozen. The selection grid is recorded in the repository before E0.

Ten seeds: 42, 1337, 2024, 7, 91, 512, 6021, 88, 3407, 12345. The same ten integers for every dataset.

Training partitions capped at 2 million rows by stratified subsampling.

---

## 6. Probability calibration

One-vs-rest isotonic regression fitted on `D_probcal`, source data only, held fixed across all protocols and arms.

Outputs are renormalized to sum to one:

```
p̂_k(x) = g_k(x) / Σ_j g_j(x)
```

where `g_k` is the one-vs-rest calibrated score. Renormalization is required because APS operates on a distribution.

Sensitivity analysis uses Dirichlet calibration, which is multiclass-native and needs no renormalization.

**Secondary factor, reported separately:** a target-fitted probability calibrator paired with a source-fitted conformal quantile, to test whether probability recalibration alone closes the gap. This is never mixed into the primary contrast.

---

## 7. Conformal specification

### 7.1 Scores

**Primary, randomized APS:**

```
s_APS(x, y) = Σ_{j : p̂_j(x) > p̂_y(x)} p̂_j(x)  +  U · p̂_y(x),     U ~ Uniform(0,1)
```

Strict inequality in the sum. Labels tied at `p̂_y(x)` contribute nothing to the first term; ties are resolved by the randomization term, not by jitter or by an ordering convention. Each label draws an independent `U`.

`U` is drawn from a counter-based RNG (Philox) keyed by the tuple `(dataset, seed, sample_id, label_index)`. This guarantees that REC, TSC and SHC observe identical realized scores on identical evaluation points. Without it the protocol contrast absorbs randomization noise.

Randomized rather than deterministic APS, because deterministic APS over-covers and this study measures departures from nominal. Deterministic APS is a sensitivity check.

**Secondary, LAC:** `s_LAC(x, y) = 1 − p̂_y(x)`. No randomization. Included because it is the likely choice of the audited papers.

### 7.2 Quantile

Calibration scores `s_1, ..., s_n`, order statistics `s_(1) ≤ ... ≤ s_(n)`:

```
k  = ⌈(n + 1)(1 − α)⌉
q̂  = s_(k)     if k ≤ n
q̂  = +∞        if k > n
```

### 7.3 Prediction set

```
C(x) = { y : s(x, y) ≤ q̂ }
```

Empty sets are permitted and their rate is reported. Top-1 forcing is prohibited: it inflates coverage, which is the measured quantity. Full-set rate is reported.

### 7.4 Variant

**Mondrian (class-conditional) split conformal is primary**, applied per class with `n` the calibration count in that class. Membership of label `y` uses `q̂_y`.

**Marginal split conformal is the comparison arm**, included because it is what the field predominantly uses and it links the experiment to the audit.

### 7.5 Levels

Primary α = 0.05. Sensitivity at 0.10 and 0.20. α = 0.01 only where §7.6 is satisfied.

### 7.6 Feasibility and exclusion

Class-conditional conformal at level α requires

```
n_c ≥ ⌈1/α⌉ − 1
```

calibration points in class `c`. Nineteen at α = 0.05, ninety-nine at α = 0.01.

A feasibility table over (dataset, class, α) is produced and committed **before** any coverage result is examined. Infeasible cells return `q̂ = +∞` and trivial coverage of one; they are **excluded from analysis**, never recorded as covered.

The set of feasible cells is itself a reported result.

---

## 8. Protocols and matching

| Protocol | `D_confcal` drawn from |
|---|---|
| **REC** reused-evaluation calibration | `D_eval` itself |
| **TSC** target-supervised calibration | `T_cal`, target distribution, disjoint from `D_eval` |
| **SHC** source-held-out calibration | `S_cal`, source distribution |

The term "transductive" is not used anywhere in this project unless full conformal is implemented.

```
E_reuse            = Δ_REC − Δ_TSC
E_cal-distribution = Δ_TSC − Δ_SHC        PRIMARY
```

### 8.1 Matching procedure

Per ladder level and matched draw:

1. Fix `D_eval`.
2. Draw `T_cal` and `S_cal` with equal total size.
3. Match broad-class counts between them wherever source support permits.
4. Identical score, α, base model and probability calibrator.
5. **R = 10 matched draws** per level. Reduced from 50; see §11 for why.
6. Paired analysis on identical `D_eval` observations.

`|T_cal| = |D_eval|` so REC and TSC use calibration sets of equal size and differ only in reuse.

### 8.2 Support deficit

Where a class is absent or under-supported in the source pool, matching fails. Record

```
d_c = max(0, n_c^target − n_c^source-available)
```

Levels with non-zero deficit are flagged as exhibiting support shift and are analysed through `S_sup` in §9, not treated as covariate shift.

---

## 9. Shift measurement

| Symbol | Mechanism | Definition |
|---|---|---|
| `S_lab` | Prior shift | Total variation distance between calibration and evaluation class priors |
| `S_cov` | Covariate shift | AUC of a domain classifier separating calibration from evaluation covariates |
| `S_sup` | Support shift | Fraction of evaluation mass in classes or subtypes with zero or near-zero source support |

`S_cov` is computed at a **fixed subsample of 20,000 per side**, so the statistic is comparable across datasets and is not driven by n. The domain classifier is a gradient-boosted tree with fixed hyperparameters, five-fold cross-fitted, AUC averaged across folds.

**No-shift is defined against a permutation null.** Split the calibration partition at random 200 times, compute `S_cov` each time, and treat a partition as no-shift if its `S_cov` falls below the 95th percentile of that null.

**Binding constraint for E1.** The domain classifier used to compute `S_cov` and any density-ratio estimator used by weighted conformal in E1 must be fitted on **disjoint samples**. Using one fitted object both to define the shift axis and to supply a remedy's weights would contaminate the remedy evaluation. Two independent subsamples of the calibration pool are reserved for this purpose.

---

## 10. Ladders and arms

**Governing principle.** Shift is a measured covariate. Ladder level is a device for generating variation and never appears as a predictor. All analysis regresses on measured `S_cov`, `S_lab`, `S_sup`.

### 10.1 Construction

**NSL-KDD.** Randomized realizations with fixed total `n`, fixed broad-class prevalence, monotonically increasing fraction of unseen subtypes, matched subtype counts within level, and **R = 20** independent draws of which subtypes enter at each level. Subtypes are never ordered by frequency, because frequency correlates with difficulty.

**CIC-IDS2017.** Four conditions, each with measured shift: same-day session-separated control; earlier-attack-day to later-attack-day transfer; leave-one-attack-day-out; attack-family holdout. Monday is excluded as a calibration source because it is effectively benign-only and cannot support Mondrian calibration of attack classes. **R = 5** realizations.

**UGR'16.** Calibrate March to May, evaluate successive weekly windows from July. **R = 5** realizations per window.

**CIC-IoT-2023.** Multiple family-holdout combinations per k, k = 0 to 5, with `S_cov` and `S_sup` as the analysis variables rather than k. **R = 5** combinations per k.

**NF-CSE-CIC-IDS2018-v3.** Optional, treated as CIC-IDS2017.

### 10.2 Arms

**Arm A, natural.** Class prior floats.

**Arm B, prior-matched by reweighting.** Plan v5 specified stratified resampling of the evaluation set to the calibration prior. That is replaced. Resampling discards most minority-class evaluation points, which is fatal for a study whose claim concerns minority classes, and it makes a null in Arm B indistinguishable from lost power.

Arm B instead uses **inverse-probability reweighting**, which preserves every evaluation observation:

```
w_i       = π_cal(y_i) / π_eval(y_i)
Cov_B     = Σ_i w_i · 1[y_i ∈ C(x_i)] / Σ_i w_i
ESS_c     = (Σ_{i ∈ c} w_i)² / Σ_{i ∈ c} w_i²
```

Weighted coverage is modelled through the effective sample size. **A focal class with `ESS_c < 30` in Arm B is reported as inconclusive, not as a null.** This distinction is binding.

**Interpretation.** Arm B removes broad-class prior shift only. It does not remove subtype novelty, conditional feature shift, or absence of source support. Results are reported as *not explained by broad-class prior shift*, never as *covariate-driven*.

---

## 11. Analysis unit and primary model

### 11.1 Analysis unit

Plan v5 left this undefined, and the implied design exceeded forty million rows for NSL-KDD alone, which no crossed-random-effects GLMM will fit.

**The primary model runs at primary α (0.05), primary score (randomized APS), and primary variant (Mondrian) only.** Other α values, LAC, deterministic APS, marginal conformal and Dirichlet calibration are fitted as **separate sensitivity models**, never as additional rows in the primary model.

Matched draws are reduced to R = 10 and are **averaged before modelling**, with draw-level dispersion absorbed by a beta-binomial rather than entered as independent rows, since draws share evaluation points and would otherwise be pseudo-replication.

**One row =** `(dataset, ladder realization, seed, architecture, protocol, class)` with a coverage count `K` and denominator `N`.

Approximate row counts: NSL-KDD 54,000; CIC-IDS2017 9,000; UGR'16 18,000; CIC-IoT-2023 13,500. Total near 95,000, which is tractable.

### 11.2 Model

```
K ~ BetaBinomial(N, p, φ)

logit(p) = β0
         + β1 · Protocol                 (REC, SHC; TSC reference)
         + β2 · S_cov + β3 · S_lab + β4 · S_sup
         + β5 · (SHC × S_cov)            ← PRIMARY
         + β6 · (SHC × S_lab)
         + β7 · (SHC × S_sup)
         + β8 · (REC × S_cov)
         + (1 + S_cov | dataset)
         + (1 | architecture:dataset)
         + (1 | seed)
         + (1 | class:dataset)
         + (1 | ladder_realization)
```

Beta-binomial rather than binomial to absorb overdispersion from draw averaging. Fitted in glmmTMB by maximum likelihood. If the full random-effects structure fails to converge, terms are dropped in this preregistered order: `ladder_realization`, then `seed`, then the `S_cov` slope in the dataset term. Any dropped term is reported.

**Secondary Gaussian model.** A linear mixed model on Δ with the identical fixed-effects and random-effects structure, reported for interpretability. Agreement between the two is reassurance; disagreement is reported.

---

## 12. Focal classes

Plan v5's "worst-class undercoverage" compared minima taken separately per protocol. The minimum is a biased estimator and the argmin class can differ across protocols, so part of any observed gap would be selection artifact.

**Rule, preregistered.** For each dataset the focal class is the **rarest attack class that satisfies §7.6 at α = 0.05 in the source calibration pool**. The resulting class is recorded in the repository **before any coverage outcome is examined**, and does not change thereafter.

Per-class profiles across all feasible classes are reported alongside, descriptively.

---

## 13. Hypotheses and success criteria

### 13.1 Primary, confirmatory

**H1.** `β5 < 0`. Coverage under SHC degrades with covariate shift relative to TSC.

E0 succeeds only if **all four** hold:

1. Holm-adjusted 95 per cent interval for `β5` excludes zero, Arm A
2. Sign and significance retained in Arm B, with focal-class `ESS ≥ 30`
3. **Focal-class coverage under SHC is at least 5 percentage points below TSC**
4. Direction replicates in at least two environments differing in traffic source, capture methodology, and shift mechanism

**Justification for the 5 point threshold, fixed in advance.** At α = 0.05 an operator expects 95 per cent coverage. A fall to 90 per cent doubles the per-alert miss rate, which is the smallest change that alters an escalation or staffing decision at realistic alert volumes. The threshold derives from that reasoning and not from any observed effect size.

### 13.2 Secondary

**H2.** `β7 > |β5|` in magnitude on levels with non-zero support deficit, indicating support shift dominates covariate shift where both are present.

**H3.** `E_reuse` is smaller in magnitude than `E_cal-distribution` on matched partitions. Tested as a paired difference with a Wilcoxon signed-rank test and a paired bootstrap.

### 13.3 Structured but non-confirmatory

**E1.** For each remedy in {weighted conformal, ECP/EACP, recency-weighted conformal, adaptive conformal, target-supervised rolling oracle}, report coverage, focal-class coverage, mean set size, empty-set rate, and the information requirement. **Success is defined as identifying at least one shift mechanism under which no label-free remedy restores focal-class coverage within 2 percentage points of nominal at a mean set size below half the label space.** This criterion is preregistered so that E1 cannot be retrofitted to whatever the results show.

**E4.** Affectedness is defined **from shift measures, not from coverage outcomes**. A class cell is affected at a ladder level if `S_sup` for that class exceeds zero or `S_cov` for the level exceeds the permutation-null threshold. Defining affectedness from coverage and then testing trust scores on the selected cells would condition on the outcome.

**E6 and E7** remain hypotheses. Their success criteria are in plan v5 §3 and are unchanged.

---

## 14. Multiplicity

**One primary test:** `β5`, Arm A, primary α, primary score, primary variant.

Holm correction is applied across the protocol contrasts within the primary model.

Everything else is either **preregistered secondary** (H2, H3, E1's criterion) and reported with unadjusted intervals labelled as such, or **descriptive and exploratory**, labelled explicitly in every table and figure caption. Sensitivity models are not additional tests of H1 and will not be reported as though they were.

---

## 15. Reported quantities

For every analysed cell: coverage, focal-class coverage, mean and median prediction-set size, empty-set rate, full-set rate, effective sample size in Arm B, `S_cov`, `S_lab`, `S_sup`, support-deficit vector, and the feasibility flag.

Coverage is never reported without set size.

---

## 16. Deviations

Any departure from this document is recorded in `reports/deviations.md` with the date, the reason, and whether it was made before or after the affected outcome was observed. The deviation log is released with the artifact.

Analyses not specified here are exploratory and will be labelled exploratory in the paper.

---

## 17. Ethics and open science

No human subjects. All datasets are public research releases used within their stated licences. UGR'16 contains real ISP traffic that is already anonymised by its publishers; no de-anonymisation is attempted and no attempt is made to identify hosts or users.

Artifact release, targeting the Open Science requirements of the intended venue: this preregistration, the feasibility tables, the focal-class record, the RNG stream definition and seeds, the matched-subsampling procedure, the deviation log, the audit coding form and completed sheets, the reproduction records, and a reference implementation of the five-partition protocol.

---

## 18. Commit

This document is committed to `github.com/anasbiswas1/<repo>/preregistration.md` and tagged before notebook `05_conformal_three_protocols` produces its first coverage output. The commit hash is cited in the paper.
