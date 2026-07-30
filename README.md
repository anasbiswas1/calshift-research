# Source-Calibrated Conformal Intrusion Detection under Distribution Shift

Code, preregistration and derived results for a preregistered study of whether conformal
prediction retains its **class-conditional** coverage guarantee when a network intrusion
detector is calibrated on past traffic and deployed on shifted traffic.

The short answer is that it does not, on the classes that matter most, and the failure is
selective in a way no environment-level shift statistic can express.

---

## What the study asks

Conformal prediction promises that a prediction set contains the true label with probability at
least `1 - alpha`. That guarantee assumes calibration and test data are exchangeable.
Deployment breaks the assumption twice over: a detector is calibrated on historical traffic and
applied to future traffic, and the target labels needed to recalibrate are exactly what an
operator does not have.

Three calibration protocols are compared, holding the classifier and probability calibrator
fixed so that only the calibration data changes:

| Protocol | Calibrated on | Deployable |
|---|---|---|
| `REC` | the evaluation set itself | no, same-sample reuse; an upper bound by construction |
| `TSC` | a labelled target sample | no, requires target labels |
| `SHC` | the source calibration pool | yes, requires neither target labels nor adaptation |

`SHC` is the object of study. The primary contrast is `TSC` versus `SHC`.

## Environments

Four datasets, each isolating a different form of shift. All are third-party and publicly
available from their original providers; **none is redistributed here**. `notebooks/01`, `09`,
`14` and `31` contain the acquisition steps.

| Dataset | Shift constructed | Focal class |
|---|---|---|
| NSL-KDD | five-rung unseen-subtype ladder, KDDTrain+ to KDDTest+ | R2L |
| CIC-IDS2017 | within-day DoS variant holdout, five realisations | DoS |
| UGR'16 | July week 5 to August week 1, temporal feature drift | nerisbotnet |
| CIC-IoT-2023 | five-rung novel-subtype ladder, two web-attack subtypes withheld | Web |

## Repository layout

```
preregistration.md                  the plan, fixed before analysis
preregistration_amendment_01..11.md dated amendments, in order
PROVENANCE.md                       when each was committed, including a disclosed lapse
reports/deviations.md               everything that departed from the plan
notebooks/                          55 numbered notebooks, independently runnable
src/                                shared modules: config, conformal, per-dataset features
reports/                            170 result files: coverage tables, shift measures, verdicts
figures/springer/                   figures at publication resolution
FULL_MANUSCRIPT.md                  manuscript source
```

Datasets and model binaries are gitignored. Everything needed to check a number in the paper is
committed.

### Notebook ordering

| Range | Contents |
|---|---|
| 01–08 | NSL-KDD: acquisition, partitions, ladders, models, protocols, mechanism |
| 09–13 | CIC-IDS2017 |
| 14–19 | UGR'16, plus the pooled cross-dataset model |
| 20–23 | mechanism and the label-free monitor |
| 24–31 | robustness, efficiency, calibration, abstention |
| 32–35 | CIC-IoT-2023 |
| 36 | results ledger and manuscript number checker |
| 37–52 | additions made in response to review |

Each notebook mounts Google Drive, restores git credentials, and writes its outputs to
`reports/`. They are designed to run in Colab and are not expected to execute elsewhere without
adjusting the paths in the first cell.

## Verifying the numbers

Every numerical value in the manuscript is machine-checked against the committed result files.

`notebooks/36_results_ledger.ipynb` rebuilds `reports/final_results.json` from the files in
`reports/`, then extracts every decimal in the manuscript and matches it against that ledger.
The result is written to `reports/manuscript_number_check.txt`, in the form:

```
ledger entries 133, distinct values 1133
manuscript numbers 289: exact 279, rounded 10, unmatched 0
```

Counts shift as the manuscript is revised; what matters is the last field. Rounded matches are
values quoted to fewer decimals than the source file carries, within 0.006.

An unmatched value would mean a number in the paper does not derive from any committed result.
There are none. This is the one check worth re-running if you want to test the paper's
reproducibility claim rather than take it on trust.

`reports/figure_compliance_springer.csv` records the resolution and physical size of every
figure.

## On the preregistration

The study is preregistered, and the record is deliberately unflattering where the truth is
unflattering.

`PROVENANCE.md` discloses that `preregistration.md` and Amendments 1 and 2 were authored before
the notebooks implementing them but, through a workflow lapse, were not committed until after
the first commit containing coverage results. It then sets out the evidence that the
specification nonetheless preceded the outcomes: the parameters are encoded in `src/config.py`
in the first project commit, each annotated with the preregistration section it derives from,
and notebooks 02 and 03 apply and cite specific amendment sections before any coverage existed.

Section 4.12 of the manuscript classifies every analysis as pilot-informed, prespecified,
prospectively amended, or exploratory. Four analyses are exploratory and labelled as such
throughout: the placebo ladder, which is additionally outcome-informed, the class-conditional
shift measure, the threshold-level decomposition, and the label-free monitor.

`reports/deviations.md` logs the rest, including a preregistered pooled model that proved
unidentifiable at this design and a coverage attribution that was withdrawn.

## What the study found

- The deployable protocol undercovers severely on all four feasible NSL-KDD classes, on
  CIC-IDS2017 denial of service and on two UGR'16 scan classes, by up to 0.86, while other
  classes and an entire fourth environment hold nominal coverage.
- That contrast survives matching both protocols to identical per-class calibration sizes, so it
  reflects calibration-data provenance rather than sample size.
- Neither the category nor the magnitude of shift predicts which classes fail. Rearranging
  evaluation mass among subtypes the source has already seen moves coverage further than
  introducing unseen subtypes does.
- What the failing classes share is movement of their nonconformity scores past the calibrated
  threshold, which orders undercoverage across twenty-eight class cells at rank correlation
  0.84.
- A label-free monitor anticipates failure with a demonstrated blind spot, and margin-ordered
  abstention proves anti-correlated with need.

## Reuse

The notebooks and modules are released for inspection and reuse. The datasets belong to their
original providers and are subject to their terms.
