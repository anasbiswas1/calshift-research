# Preregistration Amendment 2

**Amends:** `preregistration.md` sections 10.2, 13.1, and gate G2; Amendment 1 stands unchanged.
**Written:** after notebook 02, before notebook 03.
**Binding on commit.**

## B0. What was known when this amendment was written

Source partitions built, feasibility table computed, focal class recorded as R2L. No shift measure has been computed, no model trained, no coverage number exists. The change below follows from an algebraic property of the estimator, not from any observed result.

---

## B1. The defect

Preregistration §10.2 defines Arm B as inverse-probability reweighting of the evaluation partition to the calibration class prior:

```
w_i = π_cal(y_i) / π_eval(y_i)
```

The weight depends only on the class label. Within any class it is therefore constant, and the weighted class-conditional coverage estimator reduces to the unweighted one:

```
Cov_c^B = Σ_{i∈c} w·1[y_i ∈ C(x_i)] / Σ_{i∈c} w  =  Σ_{i∈c} 1[y_i ∈ C(x_i)] / n_c  =  Cov_c^A
```

Effective sample size per class is likewise unchanged:

```
ESS_c = (n_c·w)² / (n_c·w²) = n_c
```

Verified numerically on the realised partitions: ESS equals n exactly for every class (R2L 299, DoS 774, Probe 251, Normal 1008, U2R 7).

**Consequence.** Class-conditional coverage is invariant to broad-class prior shift by construction. Preregistration §13.1 criterion 2, "sign and significance retained in Arm B", is vacuously satisfied for the primary outcome, and gate G2 is unreachable. Neither can discriminate between hypotheses.

---

## B2. Resolution

### B2.1 Arm B is retained, with its scope corrected

Arm B applies to **marginal** coverage, where class mix genuinely affects the estimate. It is reported as a secondary analysis. It does not appear in the primary class-conditional analysis.

### B2.2 The support-shift control moves to the ladder

The ladder already supplies a stronger control than prior-matching. At rung `f = 0.00` the evaluation partition contains only subtypes present in the source pool, so `S_sup = 0` while covariate shift remains non-zero. At `f > 0` both mechanisms are present.

The ladder therefore decomposes the two mechanisms that can move class-conditional coverage. Prior shift, which cannot, is removed from the confirmatory path.

### B2.3 `S_lab` becomes a placebo predictor

`S_lab` is retained in the class-conditional model as a **placebo term with an expected null coefficient**. A materially non-zero estimate indicates a pipeline defect rather than a finding, and is treated as a diagnostic failure requiring investigation before any result is reported.

This is a deliberate falsification check, not a wasted parameter.

---

## B3. Replacement of §13.1 criterion 2

Criterion 2 is replaced. E0 succeeds only if all four of the following hold:

1. Holm-adjusted 95 per cent interval for the SHC × `S_cov` term excludes zero
2. **The SHC × `S_cov` effect holds at rung `f = 0.00`, where `S_sup = 0`**, establishing that coverage loss is not attributable solely to subtype novelty
3. Focal-class (R2L) coverage under SHC is at least 5 percentage points below TSC
4. Direction replicates in at least two environments differing in traffic source, capture methodology, and shift mechanism

Criteria 1, 3 and 4 are unchanged.

---

## B4. Replacement of gate G2

| Gate | Success condition | If not met |
|---|---|---|
| **G2** | The SHC × `S_cov` effect is present at rung `f = 0.00` | Coverage loss is attributable to support shift alone. Report as a support-shift finding; do not claim a covariate-shift effect |

The previous G2, "sign and significance retained in Arm B", is withdrawn as unreachable.

---

## B5. Deviation: `S_cov` subsample size

Preregistration §9 fixes the `S_cov` domain-classifier subsample at 20,000 per side. Amendment 1 subsequently fixed `D_eval` at 2,340 rows, so 20,000 per side is unattainable on the evaluation side.

**`S_cov` is computed at 2,000 rows per side**, the largest round figure fitting inside `D_eval` with margin, held constant across every dataset and rung so the statistic remains comparable.

Logged in `reports/deviations.md`.

---

## B6. Unchanged

All other sections of the preregistration and Amendment 1 stand. The primary contrast remains TSC versus SHC. The primary outcome remains class-conditional coverage at α = 0.05 with randomized APS under Mondrian conformal. The focal class remains R2L.
