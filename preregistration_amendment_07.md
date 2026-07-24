# Preregistration Amendment 7

**Status:** binding on commit. Made before any CIC-IDS2017 coverage number is computed; `reports/` contains no `*_cicids2017` coverage output at the time of writing.
**Scope:** refines the CIC-IDS2017 ladder in Amendment 5 (A5.3) so that focal-class coverage under shift is measurable, which the pure day-based design cannot deliver. Adds a within-day shift environment as the primary CIC ladder and re-roles the cross-day conditions as a support-shift arm. Changes no other CIC decision.

---

## A7.1 Why the pure day-based ladder cannot measure focal-class coverage

In CIC-IDS2017 each attack family is captured on a single day (Tuesday Brute Force; Wednesday DoS and Heartbleed; Thursday Infiltration and Web Attack; Friday Bot, PortScan, DDoS). The deployable protocol SHC calibrates its class-conditional quantile on source data. Under any cross-day split, an attack family present in the target is absent from the source, so SHC has no calibration points for it, the class is infeasible by section 7.6, and it is excluded. Only benign traffic spans days.

Therefore the cross-day conditions in A5.3 (C2 earlier-to-later, C3 leave-one-day-out) predominantly express support shift, whole novel families appearing in the target, under which those families are unmeasurable rather than miscovered. They cannot deliver a focal attack class whose coverage is measured under shift, which the focal-class rule (section 12) and success criterion 3 (section 13.1) require.

---

## A7.2 Within-day shift as the primary CIC ladder (new)

To measure focal-class coverage under shift, the shifted attack class must appear in both the source calibration pool and the evaluation target. On CIC-IDS2017 this is only possible within a single day. Wednesday is selected: DoS on Wednesday holds roughly 171,000 flows across four variants (Hulk, GoldenEye, Slowloris, Slowhttptest), enough internal structure to shift.

Two within-day shift axes on Wednesday, each a measured ladder over R = 5 realizations:

- **W-cov (covariate shift).** Wednesday is split into disjoint session blocks by capture time. Calibrate on an earlier block, evaluate on a later block, both containing DoS and benign. Covariate-shift manipulation at fixed class support: `S_cov` is measured per section 9 and `S_sup` is near zero by construction.
- **W-sup (novel-variant shift).** DoS variants are held out between calibration and evaluation: calibrate on a subset of variants, evaluate on a target whose DoS mass includes held-out variants. This is the CIC analogue of the NSL-KDD unseen-subtype ladder inside R2L. `S_sup` rises with held-out variant mass; the held-out fraction varies across realizations and is never entered as an index.

Benign traffic is drawn from Wednesday in both source and target to avoid a benign-only confound. The five-partition protocol (section 4) applies within Wednesday: train, val, probcal and the source calibration pool from the source block; `D_eval` and `T_cal` from the target block. Implementation note: the session split uses the flow capture timestamp; notebook 10 verifies a usable time field exists before building the split and records the split boundary.

---

## A7.3 Cross-day conditions re-roled as the support-shift arm

The A5.3 conditions are retained but re-roled. C2, C3 and C4 (attack-family holdout across days) become the CIC support-shift arm, reported through `S_sup`, and are the vehicle for the finding that novel attack families are structurally unmeasurable under SHC because the class drops out by section 7.6. C1 (same-day session-separated control) is subsumed by W-cov. These conditions are descriptive of support shift and do not contribute a measured focal-class coverage under covariate shift.

---

## A7.4 Focal class

The focal-class rule (section 12) is unchanged and is computed in notebook 10 from the Wednesday source calibration pool, not asserted here. DoS on Wednesday is the only attack family with both sufficient calibration support at alpha = 0.05 and internal variant structure to shift, so DoS is the expected focal class. Bot (736 rows, single variant, single day) is retained as a small secondary covariate-shift check under a Friday session split if it satisfies section 7.6, but it is not the focal class. Web Attack, Infiltration and Heartbleed remain below the feasibility floor and are excluded and reported.

---

## A7.5 What this buys the study

W-cov is a clean covariate-shift manipulation on a well-supported class. Covariate shift is the effect that came out inconclusive on NSL-KDD, where the SHC by `S_cov` interval crossed zero (criterion 1 failed and was disclosed). CIC W-cov gives the primary test a second, better-powered environment for the SHC by `S_cov` interaction, while the cross-day arm supplies the support-shift contrast. This is the mechanism by which the second dataset speaks to the question the first could not settle.

---

## A7.6 Unchanged

Partitions (4), models and seeds (5), probability calibration (6), conformal and feasibility (7), matching (8.1), shift measurement (9), arms (10.2), primary model (11.2), focal-class rule (12), success criteria (13), and Amendments 5 (A5.1 Attempted, A5.2 taxonomy) and 6 (version of record) all apply without modification. Only the CIC ladder construction (A5.3) is refined.
