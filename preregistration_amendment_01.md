# Preregistration Amendment 1

**Amends:** `preregistration.md` sections 1, 3, 10.1, 12.
**Written:** after notebook 01, before notebook 02.
**Binding on commit.**

## A0. What was known when this amendment was written

Everything observed to date is **dataset structure**, not experimental outcome:

- NSL-KDD row counts, class counts, subtype inventory, and the test-only subtype table
- Projected calibration-set sizes derived from the preregistered split fractions
- The resulting feasibility and focal-class projection

No model has been trained. No probability calibrator has been fitted. No conformal quantile has been computed. No coverage number exists. The decisions below are therefore made before any outcome that could bias them, which is the condition the preregistration exists to satisfy.

---

## A1. Addition to §1: pilot-data declaration

The following is appended to §1 of the preregistration.

> Prior exploratory work by the authors on NSL-KDD, UNSW-NB15 and CIC-IDS2017 motivated the hypothesis in §13.1. That work used uncorrected datasets, a single random seed, a two-protocol design, and no matched calibration sets, and it is not part of the confirmatory test reported here. The confirmatory analysis is specified in full in this document and is run on corrected data, redesigned shift ladders, matched calibration sets, three protocols, and ten seeds. This is therefore a pilot-informed preregistration rather than a blind one, and is declared as such.

Rationale: the earlier results are public in a prior preprint. A reviewer who finds them and no declaration here would reasonably read the omission as concealment. Declaring the pilot converts a liability into evidence of discipline.

---

## A2. Addition to §3: CIC-IDS2017 attempted-attack policy

The WTMC-2021 corrected release (Engelen et al. 2021) separates completed attacks from attempted attacks that did not succeed. The preregistration did not state how these rows are treated. That gap is closed here.

**Primary analysis: attempted-attack rows are excluded.**
**Sensitivity analysis: attempted rows merged into the parent attack family.**

Rationale. Engelen et al. separated the two deliberately, and a failed attempt can be behaviourally closer to benign traffic than to the attack family it belongs to. Merging them blurs the class definitions on which the class-conditional coverage claim rests. Excluding them keeps the primary class definitions clean; the merge sensitivity shows whether the choice drives any result.

The row counts under each policy are reported so the effect of the choice is visible.

In notebook 01, `ATTEMPTED_POLICY` is set to `'exclude'`.

---

## A3. Replacement of §10.1, NSL-KDD ladder

The preregistration specified fixed total `n`, fixed broad-class prevalence, monotonically increasing unseen-subtype fraction, matched subtype counts, and R = 20 realizations, but fixed no numeric values. The values are fixed here from the observed subtype structure.

### A3.1 Observed structure

Target pool is KDDTest+, 22,544 rows. Seventeen subtypes appear in test and not in train, carrying 16.63 per cent of test mass.

| Class | Seen | Unseen | Unseen subtypes |
|---|---|---|---|
| Normal | 9,711 | 0 | 0 |
| DoS | 5,741 | 1,719 | 5 |
| Probe | 1,106 | 1,315 | 2 |
| R2L | 2,199 | 686 | 7 |
| U2R | 37 | 30 | 3 |

### A3.2 Fixed parameters

- **Rungs:** unseen-subtype fraction ∈ {0.00, 0.20, 0.40, 0.60, 0.80}
- **Broad-class prevalence:** held at natural KDDTest+ prevalence across all rungs
- **Per-rung `D_eval` size:** 2,340 rows, giving R2L ≈ 300 per rung
- **`|T_cal| = |D_eval|`**, drawn disjointly from the same target pool
- **Realizations:** R = 20 independent draws of which unseen subtypes enter at each rung

R2L binds the design. Its ceiling is 428 rows per rung at the 0.80 rung once the disjoint `T_cal` requirement is accounted for, so 300 leaves margin. DoS and Probe have greater headroom at these settings.

### A3.3 U2R exclusion

U2R supports a maximum of 18 to 30 rows per rung, and its projected source calibration pool holds 8 records against a requirement of 19 at α = 0.05. It therefore supports neither the ladder nor class-conditional conformal under source-held-out calibration.

**U2R is retained in the data at natural prevalence and excluded from the ladder prevalence constraint and from all class-conditional analysis.** This exclusion is reported as a result, not as a limitation of the analysis: on this benchmark the rarest attack class cannot be given a class-conditional conformal guarantee at operationally meaningful α under the only calibration protocol available in deployment.

### A3.4 Declared limitation: incomplete randomization at high rungs

R2L's unseen subtypes are severely unequal. snmpguess (331), snmpgetattack (178) and httptunnel (133) carry 93.6 per cent of R2L unseen mass; the remaining four carry 44 rows in total.

Consequently, above an unseen fraction of approximately 0.59 the required unseen count cannot be reached without snmpguess. **At the 0.60 and 0.80 rungs, snmpguess appears in every realization.** Subtype identity is fully randomized only at the lower rungs.

R = 20 distinct realizations remains achievable (43 feasible subtype subsets exist at the hardest rung), but the realizations are correlated through one subtype at the top of the ladder. This is stated in the paper rather than left for a reader to infer.

Probe carries only two unseen subtypes, so randomization over subtype identity is degenerate for Probe. Probe supplies a shift gradient but not a randomized one, and is analysed accordingly.

---

## A4. Addition to §12: focal class record

The preregistered rule is the rarest attack class supporting the paired TSC-versus-SHC contrast in the source calibration pool at α = 0.05.

**Projected focal class for NSL-KDD: R2L.**

U2R fails the rule because its projected source calibration pool holds 8 records against a requirement of 19. R2L holds 149 and is the next rarest.

This projection is computed from the preregistered split fractions applied to raw class counts. It is **confirmed against the realised partitions in notebook 02 and recorded there before any coverage number is computed.** If the realised partition changes the answer, the change and its cause are recorded in the deviation log.

R2L is also where NSL-KDD's shift concentrates: 0.79 per cent of train against 12.80 per cent of test. The rule selecting it was fixed in advance and was not chosen for that property.

---

## A5. Unchanged

All other sections of the preregistration stand. Ladder parameters for CIC-IDS2017, UGR'16 and CIC-IoT-2023 are not fixed here; they are fixed in a later amendment once each dataset's structure has been inspected, under the same condition that no outcome has been observed.
