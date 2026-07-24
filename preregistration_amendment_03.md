# Preregistration Amendment 3

**Amends:** `preregistration.md` §0.8 and §11.2; Amendments 1 and 2 stand unchanged.
**Written:** after notebook 05, before notebook 06.
**Binding on commit.**

---

## C0. Provenance of these decisions

This amendment is written after coverage results exist, so the basis for each change must be auditable rather than asserted.

**The two substantive changes (C1, C2) follow from degeneracies visible in notebook 03, which computed the shift measures and computed no coverage.** The git history establishes the ordering:

```
9fa0aaa  nb03: shift ladders, S_cov with permutation null, S_lab, S_sup, Arm B weights
0e3e6d4  nb04: models and calibration
3d7818a  nb05: three conformal protocols, coverage and set size
```

`reports/ladder_shift_measures_nslkdd.csv` at commit `9fa0aaa` contains the constant `S_lab` column and the `S_cov` range that motivate C1 and C3. No coverage number existed at that commit.

**C3's resolution deliberately does not alter the preregistered primary term**, precisely because collinearity was assessed after outcomes were visible. The term stays; only its interpretation is qualified.

**C6 records an observation made after outcomes and changes nothing.**

---

## C1. `S_lab` is not estimable within NSL-KDD

Amendment 1 §A3.2 holds broad-class prevalence fixed at natural KDDTest+ proportions across every rung. `S_lab`, the total variation between source and evaluation class priors, is consequently constant:

```
rung 0.0  0.1363
rung 0.2  0.1361
rung 0.4  0.1360
rung 0.6  0.1361
rung 0.8  0.1360
```

Standard deviation below 1e-3. A predictor with no variance cannot be fitted.

**Decision.** `S_lab` and its protocol interaction are **omitted from the within-NSL-KDD model**. They re-enter the pooled model once a dataset with differing class prevalence is added.

**Consequence for Amendment 2 §B2.3.** The `S_lab` placebo check cannot be performed within NSL-KDD. It is deferred to the pooled model and is not treated as satisfied in the interim.

---

## C2. The dataset random effect is not estimable with one dataset

Preregistration §11.2 specifies `(1 + S_cov | dataset)` plus `(1 | architecture:dataset)`. With a single dataset both terms have one level and are unidentified.

**Decision.** The within-NSL-KDD model uses:

```
(1 | architecture)
(1 | seed)
(1 | class)
(1 | ladder_realization)
```

The dataset terms are restored in the pooled model.

---

## C3. `S_cov` and `S_sup` are collinear within NSL-KDD

Across the ladder, `S_sup` spans 0.001 to 0.454 while `S_cov` spans 0.846 to 0.897. Both increase monotonically with rung, and `S_cov` moves largely as a consequence of the `S_sup` manipulation rather than as an independent factor.

**Decision, three parts.**

**C3.1 The preregistered primary term is unchanged.** The primary test remains the `SHC × S_cov` interaction. Substituting `S_sup` after seeing outcomes would be exactly the practice this document exists to prevent.

**C3.2 Collinearity is measured and reported.** Variance inflation factors are computed for all fixed effects and reported with the model. If VIF for either shift term exceeds 10, the two shift interactions are reported as **jointly identified only**, and no individual coefficient is interpreted in isolation.

**C3.3 The gate does not depend on separating them.** Amendment 2 §B4 already defines G2 as a contrast at rung `f = 0.00`, where `S_sup ≈ 0`. A contrast between protocols at a fixed rung is a direct estimate and is unaffected by collinearity between the two shift predictors. G2 is therefore evaluated by that contrast, not by a coefficient.

---

## C4. Within-NSL-KDD model, as fitted in notebook 06

```
K ~ BetaBinomial(N, p, phi)

logit(p) = b0
         + b1 * Protocol                (REC, SHC; TSC reference)
         + b2 * S_cov
         + b3 * S_sup
         + b4 * (SHC x S_cov)           <- preregistered primary
         + b5 * (SHC x S_sup)
         + b6 * (REC x S_cov)
         + (1 | architecture) + (1 | seed) + (1 | class) + (1 | ladder_realization)
```

Fitted at the primary specification only: α = 0.05, randomized APS, Mondrian, Arm A, feasible cells. Other α values, LAC, marginal conformal and deterministic APS are fitted as separate sensitivity models and are not additional tests of the primary hypothesis.

Convergence fallback order is unchanged from §11.2: drop `ladder_realization`, then `seed`, and report any dropped term.

A Gaussian linear mixed model on the coverage deviation, with identical fixed and random structure, is reported as a transparent secondary analysis.

---

## C5. Status of the confirmatory test

The preregistered primary model is cross-dataset. With one dataset it cannot be fitted.

**Notebook 06 reports a within-dataset analysis, not the confirmatory test.** Criterion 4 of Amendment 2 §B3 already requires replication in at least two independent shifted environments. The confirmatory pooled model is fitted when the second environment exists.

Nothing in notebook 06 may be described as confirming H1. It estimates the within-NSL-KDD effect and evaluates gates G1 and G2, both of which are within-dataset conditions.

---

## C6. Post-outcome observation, no specification change

Under the marginal conformal variant, REC does not sit at nominal for the focal class: 0.709 at rung 0.00 against 0.956 under Mondrian. This is marginal conformal behaving as specified, since it guarantees marginal and not class-conditional coverage, and it was visible only after coverage was computed.

**No specification changes.** Marginal conformal remains a comparison arm, as preregistered, and was never part of the primary test. The observation is reported in the paper as a property of marginal conformal rather than as a protocol effect, and it means the marginal arm cannot serve as a clean reference for a class-conditional claim.

---

## C7. Unchanged

Primary contrast remains TSC versus SHC. Primary outcome remains class-conditional coverage at α = 0.05 under randomized APS and Mondrian conformal. Focal class remains R2L. Success criteria and gates are unchanged from Amendment 2 §B3 and §B4.

## Provenance note

The commit that registers this amendment (cb09675, message "preregistration amendment 3:
within-dataset model specification") comes before the notebook 06 commit (375406c) that
fits the specified model. The body of cb09675 was saved as a placeholder by mistake, and
the full specification text was written into this file later, at commit 8c941b5, which
comes after the notebook 06, 07, and 08 commits. This file records the within-dataset
model used in notebook 06. Because the readable text entered the repository after those
notebooks, this file does not by itself timestamp the exact wording ahead of them, and it
is provided here for transparency.
