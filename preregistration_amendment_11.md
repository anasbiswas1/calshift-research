# Preregistration Amendment 11

**Status:** binding on commit. Corrects a construction error in the CIC-IoT-2023 ladder
introduced by notebook 32 (commit `92110ef`) and reclassifies the coverage run it produced
(notebook 34, commit `44f20b0`).
**Scope:** CIC-IoT-2023 only. Nothing about NSL-KDD, CIC-IDS2017 or UGR'16 changes.

---

## A11.1 The error

Amendment 10 A10.5 specifies a ladder in which "a monotonically increasing fraction of the
focal class's evaluation mass is drawn from subtypes withheld from calibration". The
implementation in notebook 32 did not withhold anything.

The source/target split was stratified by specific label, which guarantees that every
subtype appears on both sides. The realised split confirms it: all six Web subtypes have
rows in both source and target, for example `Uploading_Attack` 876 source and 376 target,
`Backdoor_Malware` 2253 source and 965 target. The ladder then varied which subtypes
dominated the evaluation set, but every subtype remained in the training partition, the
probability-calibration partition and the source calibration pool.

Consequently the quantity recorded as `S_sup` is the fraction of focal evaluation mass in
subtypes *nominally designated* held-out, not the fraction in subtypes absent from the
source. There was no support shift. The environment as built carries `S_cov` = 0.50 at the
permutation null, `S_lab` = 0.008, and no support shift: it is a no-shift condition.

## A11.2 Disposition of the affected run

The notebook 34 coverage run is **retained and reclassified as a no-shift control**, not
discarded. Its result, focal coverage 0.9528 under SHC against a nominal 0.95 with every
class inside its band and no infeasible cells, is what conformal theory predicts for
exchangeable data. It is therefore a valid negative control on a modern dataset, which the
study otherwise possesses only on NSL-KDD (notebook 29, source-versus-source split).

Its artefacts are renamed to carry `nosplit_control` in place of the misleading names:
`coverage_nosplit_control_ciciot2023.csv`, and the `S_sup` column in
`ladder_shift_measures_ciciot2023.csv` is renamed `eval_composition_frac` to stop it being
read as support shift.

## A11.3 Corrected construction

A fixed set of focal subtypes is designated **novel** and every row of those subtypes is
assigned to the target side, so they are absent from the training partition, the
probability-calibration partition and the source calibration pool. This reproduces what
NSL-KDD obtains for free, where KDDTest+ contains R2L subtypes absent from KDDTrain+.

**Novel subtypes:** `Uploading_Attack` (1,252 rows) and `Backdoor_Malware` (3,218 rows),
the two smallest Web subtypes. Removing them leaves the focal class with roughly 2,100
source calibration points, far above the section 7.6 floor of 19, while providing 4,470
genuinely unseen target rows from which to build the ladder.

**Fixed, not per-realization.** The novel set is the same across all realizations, so there
is one source side and one model panel. Realizations vary only the evaluation draw, which is
the correct unit of variation and avoids refitting the panel five times.

**Ladder.** At rung f, a fraction f of the focal class's evaluation mass is drawn from the
novel subtypes and 1 minus f from subtypes present in the source. `S_sup` is then the
measured fraction of focal evaluation mass in subtypes genuinely absent from the source, and
the notebook asserts that those subtypes have zero rows in every source partition.

**Evaluation prior.** D_eval is drawn at the *source-side* family prevalence rather than the
whole-frame prevalence, so that `S_lab` stays near zero and the manipulation is support shift
in isolation.

**Scope of the shift.** Because the novel subtypes are absent from training as well as from
calibration, this tests support shift and novel-behaviour detection together. That is the
realistic deployment case and it matches NSL-KDD, so the two environments remain comparable.

## A11.4 What is unchanged

The dataset, taxonomy, per-label cap and recorded priors (Amendment 10 A10.1 to A10.3), the
focal class Web and the rule that selected it (A10.4), the feature handling (A10.7), the
partition proportions, the model panel and calibration, the conformal specification, and all
success criteria.
