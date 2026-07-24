# Preregistration Amendment 5

**Status:** binding on commit. Made before any CIC-IDS2017 coverage number is computed; `reports/` contains no `*_cicids2017` output at the time of writing.
**Scope:** operationalizes the CIC-IDS2017 second environment named in sections 3, 10.1 and 11.1. Fixes three items the base preregistration left open or implicit. Changes nothing about NSL-KDD, whose results are already recorded.
**Motivation:** criterion 4 (section 13.1) requires replication in a second environment differing in traffic source, capture methodology, and shift mechanism. CIC-IDS2017 is that environment. Its analysis decisions are timestamped ahead of its results, on the same principle as the section 12 focal-class rule.

---

## A5.1 Treatment of "Attempted" attacks

The WTMC-2021 corrected release separates completed attacks from attempted attacks, a distinction absent from the uncorrected UNB CSVs and unaddressed in the base preregistration (flagged in notebook 01 cell 11).

**Decision.** Attempted rows are excluded from the primary analysis. A sensitivity analysis merges each Attempted variant into its parent family and is reported alongside, labelled sensitivity.

**Rationale.** Engelen et al. separated Attempted deliberately on behavioural grounds; an attempted attack frequently lacks the completed attack's discriminative flow signature. The paper's claim concerns class-conditional coverage, so mixing a behaviourally distinct sub-population into a family class would blur the exact quantity under test. Exclusion keeps the primary classes clean; the merge sensitivity demonstrates the finding does not depend on the exclusion.

**Not adopted:** treating Attempted as its own class. It would create classes too small to satisfy section 7.6 and would not correspond to any class an operator reasons about.

---

## A5.2 CIC-IDS2017 class taxonomy

Section 7.4 (Mondrian) and section 12 (focal class) operate over classes. CIC-IDS2017 does not use the NSL five-class taxonomy, so its class set is fixed here.

**Decision.** The broad attack family is the class; the specific attack variant is the subtype, mirroring the NSL-KDD class/subtype split in `src/features.py`. Benign is the negative class, the CIC analogue of NSL "Normal". The `label_family` column produced in notebook 01 cell 10 is the class; the variant string is the subtype and drives `S_sup` under the family-holdout and novel-variant conditions, the CIC analogue of NSL unseen subtypes.

Classes (families), subject to what the corrected label inventory in notebook 01 actually contains:

```
Benign
DoS            subtypes: Hulk, GoldenEye, Slowloris, Slowhttptest
DDoS
PortScan
Brute Force    subtypes: FTP-Patator, SSH-Patator
Web Attack     subtypes: Brute Force, XSS, SQL Injection
Bot
Infiltration
Heartbleed
```

**Focal class.** Unchanged rule from section 12: the rarest attack family satisfying section 7.6 at alpha = 0.05 in the CIC source calibration pool, recorded to `reports/focal_class_record.json` before any CIC coverage is examined, and not revised thereafter. Families failing section 7.6 are excluded under section 7.6, never forced. Heartbleed and Infiltration are expected to fail feasibility and be excluded; that exclusion is itself a reported result, consistent with the NSL rare-class finding.

---

## A5.3 Source and target distributions per ladder condition

Section 10.1 names four CIC conditions but does not state which partition is the source and which is the target. The five-partition protocol (section 4) draws train, val, probcal and the source calibration pool from the source, and draws `D_eval` and `T_cal` from the target. That mapping is fixed here per condition, using the known CIC-IDS2017 capture schedule (Monday benign; Tuesday Brute Force; Wednesday DoS and Heartbleed; Thursday Web Attack and Infiltration; Friday Bot, PortScan and DDoS).

| Condition | Source distribution | Target distribution |
|---|---|---|
| C1 same-day session-separated control | an earlier time block of an attack day | a disjoint later time block of the same day |
| C2 earlier-to-later attack-day transfer | earlier attack day(s) in the week | a later attack day |
| C3 leave-one-attack-day-out | all attack days except one | the held-out attack day |
| C4 attack-family holdout | all data with one family removed | data including the held-out family |

Monday is excluded as a source in every condition (section 10.1) because it is effectively benign-only and cannot support Mondrian calibration of attack classes. Benign traffic for the target is drawn from the same day or days as the target attacks, to prevent a benign-only shift confound. R = 5 realizations per condition (config `N_LADDER_REALIZATIONS["cicids2017"] = 5`). Shift is measured, not assumed: each realization reports `S_cov`, `S_lab`, `S_sup` per section 9 and enters the model on those measures, never on a condition index.

---

## A5.4 What is unchanged

Partitions (4), base models and seeds (5), probability calibration (6), conformal specification and feasibility (7), matching (8.1), shift measurement (9), arms (10.2), the primary model (11.2), the focal-class rule (12), and all success criteria (13) apply to CIC-IDS2017 without modification.
