# Preregistration Amendment 10

**Status:** binding on commit. Made after the CIC-IoT-2023 partitions, feasibility table and
focal-class record were produced (notebook 31) but **before any CIC-IoT-2023 coverage number
is computed**; `reports/` contains no `*_ciciot2023` coverage output at the time of writing.
**Scope:** operationalizes the CIC-IoT-2023 environment named in preregistration sections 3,
10.1 and 11.1. Changes nothing about NSL-KDD, CIC-IDS2017 or UGR'16, whose results are
already recorded.
**Motivation:** CIC-IoT-2023 is the "modern heterogeneous, family holdout" environment. It was
committed to in the base preregistration and not executed until now. Its analysis decisions
are timestamped ahead of its results, on the same principle as the section 12 focal-class rule
and Amendment 5 for CIC-IDS2017.

---

## A10.1 Version of record

The release used is the full CIC-IoT-2023 CSV distribution obtained through the Kaggle mirror
`madhavmalhotra/unb-cic-iot-dataset`: **169 CSV files, 46,686,579 rows, 34 labels**, which
matches the published release. The prepared working frame is pinned by SHA-256 in
`reports/ciciot2023_prepared_fingerprint.json`.

A first acquisition attempt in an earlier session terminated early and yielded 162 files and
44,025,666 rows. That partial download was **not** used for any analysis; it is recorded here
only so the discrepancy between the two acquisition manifests in the repository is explained.

## A10.2 Class taxonomy

Following the Amendment 5 A5.2 convention: the broad attack family is the **class** on which
Mondrian calibration and the focal-class rule operate; the specific attack is the **subtype**
that drives `S_sup` under variant holdout. Benign is the negative class.

```
Benign        1 label
DDoS         12 subtypes      DoS           4 subtypes
Recon         5 subtypes      Mirai         3 subtypes
Web           6 subtypes      Spoofing      2 subtypes
BruteForce    1 subtype
```

Mapping is derived from the label string, and any label not matching an explicit rule and not
on the known web-attack list halts the notebook rather than being absorbed silently into the
residual family. Rows whose label is null are dropped and counted.

## A10.3 Subsampling and the resulting prior

The release is 46.7 million rows, beyond the compute budget, and section 5 caps training by
stratified subsampling. **Decision:** subsample by a per-label cap of 60,000 rows, applied as
a keep-fraction while streaming each file, which retains every rare label in full. The working
frame is 1,510,142 rows, 3.23 per cent of the release.

This is a departure from proportional stratified subsampling and it moves the class prior. Both
priors are recorded in the focal-class record. The material shifts:

| Family | Raw share | Working-frame share | Enrichment |
|---|---|---|---|
| DDoS | 72.79% | 43.19% | 0.59x |
| DoS | 17.33% | 15.90% | 0.92x |
| Recon | 0.76% | 14.54% | 19.2x |
| Spoofing | 1.04% | 7.93% | 7.6x |
| Web (focal) | 0.053% | 1.644% | 30.9x |
| BruteForce | 0.028% | 0.865% | 30.9x |

**Rationale.** Proportional subsampling to a tractable size would leave the rare families with
too few points to calibrate class-conditionally, which would make the study unable to measure
the quantity it exists to measure. The cap also moderates a 73 per cent DDoS share that is an
artefact of how the testbed was driven rather than an operational prior.

**Direction of the resulting bias, stated for the paper.** The focal class is enriched roughly
thirty-fold relative to the raw capture, so it is better represented in training than it would
be in deployment and the classifier should find it easier. Any focal coverage failure measured
in this environment is therefore conservative rather than exaggerated. Marginal coverage and
`S_lab` are affected by the reweighting and are interpreted against the recorded working-frame
prior, never against the raw capture prior.

## A10.4 Focal class

Section 12's rule, with one added constraint carried from the CIC-IDS2017 experience
(Amendment 9): the focal class is the **rarest attack family that satisfies section 7.6 in the
source calibration pool and holds at least two subtypes**. The second condition is necessary
because a family held out of the source entirely returns an infinite quantile under SHC and is
excluded by section 7.6, so it cannot serve as the focal class of a shift experiment.

Applying the rule: **the focal class is Web**, with 3,720 source calibration points against a
floor of 19, and six subtypes (Backdoor_Malware, BrowserHijacking, CommandInjection,
SqlInjection, Uploading_Attack, XSS). BruteForce is rarer at 1,959 source points but holds a
single subtype and is therefore not shiftable; this is recorded so the choice does not read as
an oversight. No family failed feasibility.

## A10.5 Ladder

Section 10.1 specifies family-holdout combinations with `S_cov` and `S_sup` as the analysis
variables rather than the combination index, R = 5. That is retained for the **support-shift
arm**, in which whole families are withheld from the source.

The **focal-class ladder** is a variant holdout within the focal family, mirroring the NSL-KDD
unseen-subtype ladder and the CIC-IDS2017 within-day DoS variant holdout: a monotonically
increasing fraction of the focal class's evaluation mass is drawn from subtypes withheld from
calibration, with the family itself present in both source and target so it remains feasible
under SHC. R = 5 realizations, randomized subtype selection, never ordered by frequency.

## A10.6 What is unchanged

Partitions (section 4, 60/10/15/15 stratified by specific label, seed 20260726), base models
and seeds (5), probability calibration (6), conformal specification and feasibility (7),
matching (8.1), shift measurement (9), arms (10.2), the analysis unit and model (11), the
focal-class rule (12) as extended in A10.4, and all success criteria (13) apply without
modification.

## A10.7 Feature handling

Forty-six numeric columns are retained after excluding identifier-like columns; two constant
columns (`Telnet`, `SMTP`) are dropped, leaving **44 features**. No identifier, address or
timestamp column enters the feature set.
