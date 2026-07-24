# Preregistration Amendment 4

**Amends:** Amendment 2 §B3 criterion 1. Amendments 1 and 3 stand unchanged.
**Written:** after notebook 05, after notebook 06 was written but **before it was fitted to the real data**.
**Binding on commit.**

---

## D0. Provenance

Three facts, each checkable.

**The collinearity was documented before any model existed.** Amendment 3 §C3.2 was committed at `cb09675`, and it states the rule in advance: if VIF exceeds 10, the shift interactions are reported as jointly identified only. That amendment was written from `reports/ladder_shift_measures_nslkdd.csv` at commit `9fa0aaa`, which contains no coverage.

**The collinearity is a deterministic property of the design, not a result.** `corr(S_cov, S_sup) = 0.958` follows from the ladder construction alone. Anyone holding notebook 03's output could predict that an individual `S_cov` coefficient would be unidentified without fitting anything.

**Disclosure.** Notebook 06 was dry-run against a synthetic stand-in constructed to resemble the observed coverage. In that run the `SHC × S_cov` coefficient was noise, interval [−1.43, +1.26], while `SHC × S_sup` was −3.06 with interval [−3.20, −2.92]. **The real model has not been fitted.** This amendment is informed by a synthetic demonstration of a known design property, and that is disclosed rather than concealed.

---

## D1. The conflict

Two committed instructions cannot both be followed.

**Amendment 2 §B3 criterion 1.** The Holm-adjusted 95 per cent interval for the `SHC × S_cov` term must exclude zero.

**Amendment 3 §C3.2.** If VIF for either shift term exceeds 10, the two shift interactions are reported as jointly identified only, and no individual coefficient is interpreted in isolation.

VIF exceeds 10. Criterion 1 requires interpreting exactly the coefficient C3.2 forbids interpreting.

Left unresolved, the study would report a failed criterion on an effect of roughly 80 percentage points, not because the effect is absent but because two predictors move together by construction.

---

## D2. Why the single coefficient is not the right test

Under near-collinearity, individual coefficients are unidentified while **linear combinations along the direction the data actually vary are identified**. The ladder moves `S_cov` and `S_sup` together. The scientific question, whether SHC coverage degrades as shift increases, is a question about that joint direction, not about either coordinate separately.

Criterion 1 as worded asks a question the design cannot answer. Its intent, that SHC degrade with shift, remains answerable.

---

## D3. Replacement of criterion 1

Criterion 1 is replaced by a two-part requirement. **Both parts must hold.**

### D3.1 Joint significance

A Wald test of

```
H0:  beta(SHC x S_cov) = 0  and  beta(SHC x S_sup) = 0
```

must reject at the 5 per cent level, Holm-adjusted across the two protocol contrasts.

This establishes that SHC coverage depends on shift. On its own it is directionless, which is why D3.2 is required.

### D3.2 Directional contrast along the observed shift range

Let `s_min` and `s_max` be the minimum and maximum observed `(S_cov, S_sup)` pairs across the ladder. The change in the SHC-versus-TSC gap between them is

```
Delta_gap = beta(SHC x S_cov) * (S_cov_max - S_cov_min)
          + beta(SHC x S_sup) * (S_sup_max - S_sup_min)
```

This is a linear combination with weights fixed by the observed design. Its standard error follows from the fitted covariance matrix, and it is **estimable even when its components are not**, because the weights follow the direction in which the data vary.

Requirement: `Delta_gap` significantly negative, 95 per cent interval excluding zero.

### D3.3 If VIF is at or below 10

If the realised VIF does not exceed 10, C3.2 does not bind, and **criterion 1 reverts to its original wording** in Amendment 2 §B3. The replacement applies only under the condition that created the conflict.

---

## D4. What is reported regardless

The individual `SHC × S_cov` coefficient and interval are reported in full, labelled not individually identified, with the realised VIF and correlation alongside. Nothing is suppressed because it is inconvenient.

The Gaussian secondary model is reported with the same contrast.

---

## D5. Why this is not moving the goalposts

Three checks, stated so a reviewer can apply them.

**The replacement is not easier to satisfy in the relevant direction.** D3.2 requires a signed, directional result. A coefficient interval excluding zero could be satisfied by a positive coefficient; D3.2 cannot.

**The rule predates the conflict.** C3.2 prescribed joint reporting under VIF > 10 before any model was fitted. This amendment implements that prescription rather than inventing a new one.

**The load-bearing evidence is model-free and already fixed.** Gate G2, the protocol contrast at rung 0.00, and criterion 3, the focal-class gap against a 5-point bar, are contrasts at fixed rungs. Neither involves a shift coefficient, and neither is affected by this amendment. If the model were removed entirely, those two would still stand.

---

## D6. Unchanged

Criterion 2, the effect holding at rung 0.00, is unchanged. Criterion 3, focal coverage at least 5 percentage points below TSC, is unchanged. Criterion 4, replication in at least two independent environments, is unchanged and remains outstanding.

Gates G1 and G3 are unchanged. G2 is unchanged from Amendment 2 §B4.

Notebook 06 remains a within-dataset analysis and does not confirm H1, per Amendment 3 §C5.
