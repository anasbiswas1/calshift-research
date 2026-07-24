# Preregistration Amendment 9

**Status:** binding on commit. Made before any CIC-IDS2017 coverage number is computed; `reports/` contains no `*_cicids2017` coverage file at the time of writing.
**Scope:** revises the CIC-IDS2017 ladder roles from Amendment 7 in light of the Wednesday structure revealed by notebook 10. Makes the DoS variant holdout the primary CIC ladder (support shift), demotes the within-attack covariate split to a secondary check, and routes the covariate-shift interaction to UGR'16 and cross-dataset variation. Changes no focal class, no feasibility result, and no NSL-KDD result.

---

## A9.1 What notebook 10 revealed

On Wednesday the four DoS variants were run in sequence, each in a short window, so ordering by capture time segregates variants rather than inducing covariate drift at fixed support. In the reference session split, GoldenEye is almost entirely in the target (7361 vs 32 in the source pool), Slowloris entirely in the source (589 vs 0), and Hulk mostly in the source. A within-day time split of all DoS is therefore a variant holdout plus prior shift, not the fixed-support covariate shift that Amendment 7's W-cov intended. On CIC, time and attack variant are the same axis.

This is a structural property of real intrusion captures: an attack class appears in a burst under near-constant conditions, so deployment covariate shift on a fixed attack class is rare within a capture. This is recorded as a finding, not worked around.

---

## A9.2 CIC primary ladder: DoS variant holdout (support shift)

The primary CIC ladder is the DoS novel-variant holdout on Wednesday, the direct analogue of the NSL-KDD unseen-subtype ladder inside R2L.

- **Partition structure.** Source = flows of the kept DoS variants plus a benign portion; target = flows of the held-out DoS variants plus a benign portion. Benign is split between source and target independently of variant to avoid a benign-only confound. The five-partition protocol (section 4) is applied within the source: train, val, probcal, and the source calibration pool. `D_eval` and `T_cal` are drawn from the target.
- **Realizations.** R = 5, each holding out a different subset of the four DoS variants, chosen to span a range of held-out mass. The held-out variant set of each realization is recorded before any coverage. Held-out variant mass is measured and entered as `S_sup`; the realization is never entered as an index.
- **Expected mechanism.** The Mondrian DoS quantile is calibrated on kept variants and evaluated on a target containing held-out variants, so `S_sup` rises with held-out mass and the coverage loss concentrates in the DoS focal class. This is where CIC produces its focal-class gap under SHC.

The data supports this cleanly because the variants are already segregated in time.

---

## A9.3 Secondary covariate check, reported honestly

The within-attack covariate split is retained as a secondary check, not a primary contrast: DoS Hulk alone (the dominant variant, ~158k flows), split earlier vs later by capture order at fixed variant support, so any residual shift is covariate. If its measured `S_cov` sits below the permutation null (section 9), CIC reports weak within-attack covariate drift rather than a covariate effect. Covariate drift within a single short attack is expected to be small; the measured value decides, and a low value is the correct outcome if that is what the data shows.

---

## A9.4 Covariate interaction routed to UGR'16 and cross-dataset variation

The SHC x `S_cov` interaction (beta5), which came out inconclusive on NSL-KDD (criterion 1, disclosed), is carried by the datasets whose structure genuinely contains fixed-support covariate shift:

- **UGR'16** (section 10.1): calibrate March to May, evaluate successive weekly windows from July. The same classes persist across windows, so this is genuine temporal covariate drift at retained support, which CIC cannot supply.
- **Cross-dataset spread of `S_cov`** in the pooled primary model (section 11.2).

Criterion 4 (section 13.1, replication in a second environment) is satisfied by NSL-KDD and CIC both replicating the subtype/variant-driven focal-class gap. The covariate mechanism is tested where it exists rather than forced onto a dataset that lacks it.

---

## A9.5 Arm B and prior shift

The variant holdout carries broad-class prior shift, because DoS prevalence differs between source and target. Arm B's inverse-probability reweighting (section 10.2) absorbs it, so the CIC result is reported as not explained by broad-class prior shift. A focal-class effective sample size below 30 in Arm B is reported as inconclusive, not null (section 10.2).

---

## A9.6 Unchanged

Focal class (DoS on Wednesday, notebook 10), feasibility (notebook 10), the cross-day family-holdout support arm (Amendment 7 A7.3), partitions (section 4), conformal specification (section 7), shift measurement (section 9), the primary model (section 11.2), success criteria (section 13), and Amendments 5, 6 and 8 all stand. Amendment 7's within-day design is refined: the variant holdout (formerly W-sup) is promoted to the primary CIC ladder, and the within-attack covariate split (formerly W-cov) is demoted to a secondary check.
