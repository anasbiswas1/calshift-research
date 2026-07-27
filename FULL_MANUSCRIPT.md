# Deployable Conformal Intrusion Detection Undercovers under Distribution Shift: A Preregistered Diagnosis and a Label-Free Failure Monitor

## Abstract

Conformal prediction offers distribution-free, finite-sample coverage guarantees and is
increasingly proposed as a trust layer for machine-learning network intrusion detection.
Its guarantee assumes exchangeability between calibration and test data, which deployment
violates twice over: a detector is calibrated on past traffic and applied to future,
drifted traffic, and the target labels needed to recalibrate are precisely what an
operator lacks. The only deployable protocol is therefore source-held-out. We ask, under
preregistration, whether it retains class-conditional coverage under shift and, if not,
whether its failures can be detected without labels. Across four datasets spanning covariate and support shift, and against negative controls that confirm the pipeline is valid on exchangeable data, the deployable protocol loses class-conditional coverage on every feasible class of three of the four environments, by up to 0.86 relative to the exchangeability-based target, while target-supervised calibration holds. A placebo experiment shows that novelty is not the operative variable: rearranging evaluation mass among subtypes the source has already seen moves coverage 2.6 times more than introducing unseen subtypes does, at zero support shift. A fourth environment isolates support shift on modern IoT traffic and finds no failure at all, confirming that neither aggregate shift measure predicts the outcome. What does predict it is movement of the nonconformity-score distribution: a class undercovers exactly when its scores move past the source-calibrated quantile (Spearman 0.84 across 28 class-level cells spanning four datasets). Building on that mechanism, we propose a label-free monitor of predicted-class
score drift that anticipates coverage failure at a pooled AUROC of 0.93, consistently across all three environments, with an explicitly characterised boundary, since it attenuates where a detector confidently
misroutes a novel class into a familiar one. Robustness analyses exclude prior shift,
level choice, set size, base miscalibration and analytical choice as explanations. All
data, code and the preregistration are released.

**Keywords:** conformal prediction; network intrusion detection; distribution shift;
uncertainty calibration; coverage guarantees; drift detection.

# 1. Introduction

Machine-learning classifiers are now routine components of network intrusion detection,
yet most emit point predictions with no calibrated statement of how far they can be
trusted. An operator faced with an alert needs more than a label; they need to know
whether the model's output is reliable for this particular flow, so that scarce analyst
attention can be routed to the alerts that warrant it and withheld from those that do
not. Conformal prediction is an attractive answer to this need. It wraps any classifier
in a procedure that returns prediction sets with a distribution-free, finite-sample
guarantee: at miscoverage level alpha, the set contains the true label with probability
at least 1 minus alpha (Vovk et al., 2005; Shafer and Vovk, 2008; Angelopoulos and Bates, 2023). Applied per class in the
Mondrian manner, it promises a controllable, class-conditional guarantee that is
especially appealing for intrusion detection, where the rare classes are the dangerous
ones and a marginal guarantee can hide their failure.

That guarantee, however, rests on exchangeability between the calibration data and the
test data, and deployment breaks exchangeability in a way that is structural rather than
incidental. Network traffic drifts: the benign baseline shifts with usage, and attacks
evolve, so a detector calibrated on one period is applied to a later period whose
distribution differs. Worse, the natural fix, recalibrating on the target, is
unavailable in operation, because obtaining target labels requires exactly the analyst
effort the system is meant to conserve, and novel attacks are unlabelled by definition.
The only calibration protocol an operator can actually run is source-held-out
calibration: fix the conformal quantile on labelled source data and apply it to the
unlabelled, drifted target. Whether the coverage guarantee survives this move is the
question on which the practical value of conformal intrusion detection turns, and it is
the question we address.

A body of work restores conformal validity under covariate shift when the shift is
benign in a specific sense, for example when the source-to-target density ratio is known
or estimable, as in weighted conformal prediction (Tibshirani et al., 2019), or when calibration is
adapted online against a stream of labelled feedback, as in adaptive conformal inference
(Gibbs and Candès, 2021). Intrusion detection sits outside the comfort of these assumptions. Its
shift includes the arrival of novel attack subtypes, a change in the support of the
distribution rather than a reweighting of a fixed support, and its operators have no
stream of target labels against which to adapt. In this regime the relevant questions
for a practitioner are not only whether validity can be restored but, more basically,
when and why the deployable protocol fails, whether that failure is visible in aggregate
drift statistics, and whether it can be flagged per class without labels.

We take a deliberately diagnostic and preregistered stance. Rather than propose a method
and report that it wins, we fix in advance the datasets, the shift constructions, the
focal classes, the protocols, the shift measures and the primary test, and then ask what
the deployable protocol does. Preregistration is the instrument that makes a negative or
boundary result credible: because the focal classes and analysis plan were committed
before any coverage number existed, the failures we report cannot be an artefact of
choosing the conditions that produce them, and the one class that survives covariate
shift is the class we named in advance, not one selected after the fact. This methodology
follows the spirit of temporally and spatially honest evaluation in security machine
learning (Pendlebury et al., 2019).

We find that the deployable protocol does not merely fall short of its nominal level but falls below the band the exchangeability guarantee would imply, on every feasible class of the environments in which it fails, and that the outcome is governed by the movement of each class's score distribution rather than by the taxonomic category of the shift. The contributions of this paper are: (i) a preregistered, four-dataset, per-class diagnosis establishing that deployable conformal intrusion detection violates its finite-sample coverage guarantee under distribution shift, validated against negative controls and reported as the magnitude of that violation rather than as a shortfall against a target; (ii) a placebo experiment that separates subtype novelty from score position by construction, showing that composition among already-seen subtypes moves coverage 2.6 times more than novelty does at zero support shift; (iii) the discovery, tested rather than observed, that covariate-shift failure is selective, and the complementary finding that support shift on modern IoT traffic produces no failure at all, so that neither aggregate shift measure predicts the outcome; (iv) a mechanistic
explanation of the failures through nonconformity-score-distribution movement; (v) a label-free coverage-failure monitor, deployable in the sense that it ranks only classes the operator observes, with consistent per-environment performance and an explicitly demonstrated boundary; and (vi) an open release of all data pipelines, calibrated
models, coverage tables, figures and the
preregistration, with deterministic seeds and partition fingerprints for independent
verification.

Section 2 positions the contribution, Section 3 describes the datasets, Section 4 the
methodology, and Section 5 the results, with the discussion, limitations, future work and
conclusion following. Figure 1 gives an overview of the study design.

![**Figure 1.** Overview of the study. The labelled source is partitioned to train the classifier f, tune it, fit the isotonic calibrator g, and form the source calibration pool. The three conformal calibration protocols differ only in the data that forms the class-conditional quantile: REC on the evaluation set (a transductive oracle), TSC on a labelled target sample (not deployable), and SHC on the source pool (the only deployable protocol). Under distribution shift between source and target, SHC undercovers on the focal class while TSC and REC hold. The label-free monitor compares the predicted-class score distribution on target versus source, requiring no target labels, and flags the classes whose coverage will fail; it catches displacement-type drift but is blind to similarity-type drift, where a novel class is confidently misrouted.](figure1_overview.png)

# 2. Related work

**Conformal prediction.** Conformal prediction produces set-valued predictions with
distribution-free, finite-sample coverage under exchangeability (Vovk et al., 2005; Shafer and Vovk, 2008), and
recent expositions have made it broadly accessible (Angelopoulos and Bates, 2023). For
classification, the adaptive prediction set (APS) score yields sets whose size adapts to
instance difficulty and improves conditional coverage (Romano et al., 2020), and class-conditional
or Mondrian conditioning provides per-class guarantees (Sadinle et al., 2019; Vovk et al., 2005), which matter in
intrusion detection because a marginal guarantee can be satisfied while a rare attack
class is badly undercovered. Our study takes APS with Mondrian conditioning as its
instrument and asks what happens to the per-class guarantee when exchangeability fails.

**Conformal prediction under distribution shift.** The exchangeability assumption has
been relaxed along several lines. Weighted conformal prediction restores validity under
covariate shift when the source-to-target likelihood ratio is known or can be estimated
(Tibshirani et al., 2019). Adaptive conformal inference maintains coverage online by adjusting the
level against labelled feedback (Gibbs and Candès, 2021), and more recent analysis characterises
conformal behaviour beyond exchangeability in general (Barber et al., 2023). These methods are
powerful where their assumptions hold, but they assume either an estimable density ratio
over a fixed support or a stream of target labels to adapt against. Network intrusion
detection violates both: novel attack subtypes change the support of the distribution,
and operational deployment provides no target labels. Our contribution is orthogonal and
prior to method design: we diagnose, under these realistic conditions, when and why the
deployable protocol fails, and we show that whether a restoration method such as weighted
conformal prediction could help is itself governed by the support-versus-covariate
distinction we draw.

**Drift and unreliability detection.** A separate literature detects distribution or risk
shift after deployment. Online exchangeability testing via test martingales flags when
the exchangeability assumption is violated (Vovk et al., 2003); risk-tracking methods detect
harmful shifts in a deployed model's error (Podkopaev and Ramdas, 2022); and recent work develops
signals for when individual predictions become unreliable under shift. These approaches
typically operate at the level of the overall distribution or risk, and several rely on
labels or on aggregate signals. We differ in three respects that we state plainly so as
not to overclaim. Our monitor is tied specifically to conformal coverage failure rather
than to distribution change in general; it is per class and fully label-free, using only
the classifier's own outputs on incoming traffic; and, most importantly, we do not claim
a universally reliable signal but instead establish and demonstrate its boundary,
identifying the similarity-type regime in which no predicted-class signal can see the
failure. The general observation that model reliability can be tracked under shift is
therefore partly anticipated by this literature; our specific and, we argue, more useful
contribution is the per-class score-movement mechanism, the label-free predicted-class-
drift monitor derived from it, and the honest characterisation of where that monitor is
blind.

**Calibration and uncertainty.** Probability calibration underlies any score-based trust
layer. Modern classifiers are often miscalibrated (Guo et al., 2017), and isotonic regression provides
a nonparametric remedy (Zadrozny and Elkan, 2002). Calibration is assessed by the Brier score
(Brier, 1950) and the expected calibration error (Naeini et al., 2015), the latter sensitive to binning,
for which equal-mass schemes reduce bias (Roelofs et al., 2022). We calibrate by one-vs-rest isotonic
regression and verify, on held-out in-distribution source data, that the probabilities
feeding the conformal layer are well calibrated, so that the coverage failures we report
cannot be attributed to base miscalibration.

**Machine learning for intrusion detection and its evaluation.** Learned intrusion
detectors are commonly benchmarked on NSL-KDD (Tavallaee et al., 2009), CIC-IDS2017 (Sharafaldin et al., 2018) and
UGR'16 (Maciá-Fernández et al., 2018), and the community has documented how evaluation can be misled, both by
labelling and construction errors in the datasets themselves (Engelen et al., 2021; Liu et al., 2022) and by
temporal and spatial bias in experimental design (Pendlebury et al., 2019). Our work inherits this
critical posture: we adopt corrected labels where available, audit feature separability
to rule out trivial leakage, construct shift explicitly and measure it, and preregister
the analysis. To our knowledge, no prior study offers a preregistered, cross-dataset,
per-class account of whether deployable conformal intrusion detection retains coverage
under distribution shift, together with a label-free monitor for its failures and an
explicit characterisation of that monitor's boundary. That is the gap this paper fills.

# 3. Datasets and preparation

We evaluate the trust layer of conformal intrusion detection on four network intrusion
detection datasets, each chosen to isolate a distinct form of distribution shift between the
data on which a detector is calibrated and the data on which it is deployed. NSL-KDD (Tavallaee et al., 2009) and CIC-IDS2017 (Sharafaldin et al., 2018) exercise *support shift*, in
which the target contains attack behaviour whose fine-grained subtypes were unseen
during calibration; UGR'16 (Maciá-Fernández et al., 2018) exercises *temporal feature drift at fixed broad-class
support*: the same attack families are present in source and target at equal sampled counts
and their feature distributions differ across a one-month gap. The data do not establish that
the conditional law P(Y | X) is invariant across the two weeks, and the provenance caveats in
Section 3.3 make that assumption unattractive, so no claim of covariate shift in the strict
sense is made. Table T1 summarises the four environments. All raw
sources, cleaned artefacts, partition indices and derived tables are version
controlled, and every partition is fingerprinted with a SHA-256 hash so that it can be
verified without access to the underlying data.

**Table T1. Study environments.** Source and target, shift type, measured shift covariates at
the primary configuration, and the preregistered focal class. S_cov is an aggregate
domain-classifier statistic over all classes; S_sup,c is class-conditional on the focal class.
Section 5.9 shows why an aggregate covariate statistic cannot predict class-conditional
outcomes, and the same caution applies to comparing S_cov across rows.

| Dataset | Source → target | Shift type | S_cov | S_lab | S_sup,c (focal) | Focal |
|---|---|---|---|---|---|---|
| NSL-KDD | KDDTrain+ → KDDTest+, 5-rung unseen-subtype ladder | covariate + support | 0.84–0.90 | ~0.14 | 0.00–0.46 | R2L |
| CIC-IDS2017 | Wednesday DoS, 5 variant-holdout realisations | support (+prior) | 0.76–0.77 | 0.44–0.52 | 0.01–0.07 | DoS |
| UGR'16 | July week 5 → August week 1 | temporal feature drift, fixed support | 0.69 | 0.00 | 0.00 | nerisbotnet |
| CIC-IoT-2023 | 5-rung novel-subtype ladder, 2 web-attack subtypes withheld | support only | 0.50 (null) | ~0.01 | 0.00–0.80 | Web |

## 3.1 NSL-KDD

NSL-KDD is used with its canonical split: KDDTrain+ (125,973 flows) as the source and
KDDTest+ (22,544 flows) as the target, with flows grouped into the five standard
classes Normal, DoS, Probe, R2L and U2R. The finer attack subtype label is retained
only to construct and characterise the shift, never as a model input. KDDTest+ is well
suited to a support-shift study because it deliberately contains attack subtypes absent
from KDDTrain+.

Support shift is introduced through a five-rung novelty ladder. At each rung a fixed
fraction f in {0.00, 0.20, 0.40, 0.60, 0.80} of each class's evaluation quota is drawn
from subtypes unseen in the source, the remainder from seen subtypes; the evaluation
set at every rung holds 2,340 flows at the natural KDDTest+ prevalence. Twenty
realisations are drawn per rung, with the unseen subtypes selected in randomised order
so that realisation-to-realisation variation reflects which novel subtypes enter the
evaluation set. Normal is exempt from the unseen-fraction constraint (it has no attack
subtypes) and U2R is exempt (it is too rare to satisfy the constraint at higher rungs);
both exemptions are recorded. Within each realisation the evaluation set and the
target-calibration set are drawn to have identical subtype composition, so that the
target-supervised protocol is not itself exposed to an uncontrolled shift. The focal
class is R2L, fixed before any coverage number was computed as the rarest attack class
supporting the paired target-supervised versus source-held-out contrast in the source
calibration pool at the primary miscoverage level (Table T2).

**Table T2. NSL-KDD class composition** (source KDDTrain+, target KDDTest+).

| Class | Source | Target |
|---|---|---|
| Normal | 67,343 | 9,711 |
| DoS | 45,927 | 7,460 |
| Probe | 11,656 | 2,421 |
| R2L (focal) | 995 | 2,885 |
| U2R | 52 | 67 |

The extreme rarity of R2L and U2R in the source (995 and 52 flows) motivates the focal
choice and drives the feasibility floor on class-conditional calibration.

## 3.2 CIC-IDS2017

For CIC-IDS2017 we adopt the corrected labelling (Engelen et al., 2021) and a cleaned release as the
version of record, using the denial-of-service traffic captured on the Wednesday of the
collection week together with benign traffic; the task is binary, Benign versus DoS.
Support shift is constructed within the single day by holding out DoS variants: the
Hulk variant is always retained in calibration, and five realisations withhold
different combinations of the remaining variants (Slowhttptest; Slowloris; GoldenEye;
Slowloris with Slowhttptest; GoldenEye with Slowloris) from calibration while requiring
them at evaluation (Table T3). Because a detector that trivially separates the classes
would make
the coverage question vacuous, we audited feature separability: the most discriminative
single feature attains an area under the ROC curve of 0.984 and no feature acts as an
identifier, so the near-perfect classifier accuracy on this task is genuine rather than
a consequence of label leakage. The focal class is DoS.

**Table T3. CIC-IDS2017 Wednesday DoS-variant composition** (flows per variant in the source calibration pool versus the target block).

| DoS variant | Source pool | Target block |
|---|---|---|
| Hulk | 22,808 | 6,211 |
| GoldenEye | 32 | 7,361 |
| Slowloris | 589 | 0 |
| Slowhttptest | 297 | 8 |

Hulk is always retained in calibration; each realisation withholds one or more of the
remaining variants (Table T1), so the target requires attack behaviour whose variant was
unseen at calibration, producing a controlled support shift.

## 3.3 UGR'16

UGR'16 provides the covariate-shift environment. We use one week of July traffic as the
source and one week of the following August as the target, separated by approximately
one month of real internet-service-provider traffic. Because the full capture is on the
order of hundreds of gigabytes, each week was streamed in chunks and subsampled to a
common composition of 200,000 background flows and 50,000 flows for each of the four
synthetic attack families (dos, scan11, scan44, nerisbotnet), then written to a
columnar store.

Two provenance decisions are recorded as deviations. First, the July and August
captures are drawn from different released variants of UGR'16, so the blacklist label
is not comparable across the pair and is dropped; only the background class and the four
comparable synthetic attack families are retained. Second, the protocol field is a
categorical string in July but was rendered uninformative in August during an earlier
numeric coercion, so it is not comparable across the pair and is dropped from the
feature set on both weeks; the covariate representation comprises nine flow features,
expanded to twenty-seven dimensions after one-hot encoding of the TCP flag field. The
categorical encoder is hardened to normalise numeric-looking category values so that a
storage-type mismatch cannot silently reappear. By construction UGR'16 carries covariate
shift at fixed support: all four attack families are present in both weeks at equal
sampled counts, so S_lab and S_sup are both zero, while S_cov is 0.69 against a
permutation-null threshold of 0.51 (Section 4.4). This is the only environment in the
study in which the shift is purely covariate. The focal class is nerisbotnet, chosen on
operational rarity rather than the capped counts.

## 3.4 CIC-IoT-2023

CIC-IoT-2023 (Neto et al., 2023) supplies a contemporary environment and isolates support
shift. We use the full CSV release, 169 files and 46,686,579 flows collected from 105 IoT devices, comprising 33 attack types plus benign traffic, giving 34 fine-grained labels. Labels are grouped into seven attack families plus benign
traffic, with the family serving as the class on which class-conditional calibration
operates and the specific attack as the subtype that drives support shift, the same
convention applied to CIC-IDS2017.

The release exceeds the compute budget, so it is subsampled by a per-label cap of 60,000
rows applied as a keep-fraction while streaming, which retains every rare label in full and
yields a working frame of 1,510,142 rows. This departs from proportional subsampling and
moves the class prior: the focal class rises from 0.053 per cent of the raw capture to 1.64
per cent of the working frame. The direction of that bias is stated because it matters for
interpretation. The focal class is better represented in training than it would be in
deployment, so the classifier should find it easier, and any coverage failure measured here
is conservative rather than exaggerated.

Support shift is constructed by designating two of the six web-attack subtypes,
`Uploading_Attack` and `Backdoor_Malware`, as novel and assigning every row of those
subtypes to the target. They are therefore absent from the training partition, the
probability-calibration partition and the source calibration pool, which reproduces what
NSL-KDD obtains for free from KDDTest+ containing R2L subtypes absent from KDDTrain+. The
absence is verified rather than assumed. The remaining rows are split 70/30 into source and
target, and a five-rung ladder raises the fraction of focal evaluation mass drawn from the
novel subtypes from 0.00 to 0.80 across five realisations.

The focal class is Web, selected by the preregistered focal-class rule as the rarest attack family
that satisfies the feasibility floor in the source calibration pool and holds at least two
subtypes. It retains 2,135 source calibration points against a floor of 19. BruteForce is
rarer at 1,371 points but holds a single subtype and therefore cannot be shifted by
withholding while remaining feasible, which is recorded so the choice does not read as an
oversight.

The resulting environment is support shift in isolation. Measured across the ladder, the
covariate shift stays at the permutation null, 0.495 to 0.506, the label-prior shift is
negligible at 0.004 to 0.014, and only the support shift moves, from 0.000 to 0.800. No
other environment in the study achieves this separation, and Section 5.6 shows why it
matters.

## 3.5 Common preprocessing and partitioning

Each source is partitioned once, before any modelling, into four disjoint strata by a
class-stratified split with fixed fractions: training (0.60), validation (0.10),
probability calibration (0.15) and a source calibration pool (0.15). The split is
deterministic under a dataset-specific partition seed, and the resulting partitions are
checked for exhaustiveness and pairwise disjointness and are fingerprinted. The training
partition fits the classifier, the validation partition selects or fixes
hyperparameters, the probability-calibration partition fits the probability calibrator,
and the source calibration pool provides the source-held-out conformal calibration set.
The target pool supplies both the evaluation set and, for the target-supervised
protocol, the target calibration set. Identifiers such as addresses and timestamps are
excluded from all feature representations.

# 4. Methodology

## 4.1 Conformal prediction protocols

The object of study is the calibration set used to form conformal prediction sets
(Vovk et al., 2005; Shafer and Vovk, 2008), not the classifier. We compare three protocols, holding the
classifier and probability calibrator fixed. The recalibrated protocol (REC) calibrates
the conformal quantile on the evaluation set itself; it is not deployable and serves as
a transductive upper bound whose coverage must sit at the nominal level by construction.
The target-supervised protocol (TSC) calibrates on a labelled target sample; it requires
target labels and is not deployable in practice, but it isolates the effect of
calibrating on in-distribution target data. The source-held-out protocol (SHC)
calibrates on the source calibration pool and is the only deployable protocol, requiring
no target labels. The primary contrast is TSC versus SHC. The two protocols differ in calibration-data
provenance and, under natural class prevalence, in class-specific calibration support: they
draw calibration sets of a common overall size, but the per-class counts entering a
class-conditional quantile follow the class composition of the pool they are drawn from. We
do not describe them as differing only in the calibration set. The two protocols draw calibration
sets of a common overall size, but the per-class counts that enter a class-conditional
quantile follow the class composition of the pool they are drawn from, so for a class
that is rare at source and common at target the deployable protocol calibrates on fewer
points. Section 5.11 quantifies this asymmetry and shows that it biases the reported
effect towards conservatism rather than exaggeration.

## 4.2 Nonconformity score and prediction sets

Nonconformity is measured with the adaptive prediction set (APS) score (Romano et al., 2020). For
a calibrated probability vector p(x) and candidate label y, the score accumulates the
probability mass ranked above y and adds a randomised fraction of the mass at y,
s(x, y) = Σ_{j: p_j(x) > p_y(x)} p_j(x) + U·p_y(x), with U uniform on [0, 1]. The
randomising draws are produced by a counter-based generator keyed by model seed, sample
and label, so that the three protocols observe identical realised scores on identical
points and differ only in their calibration set. Prediction sets are formed per class in
the Mondrian manner (Vovk et al., 2005): for miscoverage level α the conformal quantile of a
class is its k-th smallest calibration score with k = ⌈(n+1)(1−α)⌉, or ∞ when k > n. A
class whose calibration count falls below ⌈1/α⌉ − 1 returns an infinite quantile and a
trivially full set; such cells are reported as infeasible and excluded from analysis
rather than counted as covered. The primary miscoverage level is 0.05, with 0.10 and
0.20 reported as sensitivity levels.

## 4.3 Model panel and probability calibration

To ensure the coverage findings are not an artefact of a single classifier, each dataset
is fitted with three architectures, a random forest, a gradient-boosted tree ensemble
(Chen and Guestrin, 2016) and a multilayer perceptron, across ten seeds, giving thirty calibrated
models per dataset (Table T4). Hyperparameters are selected once per architecture on the
validation
partition by macro-averaged F1 and then frozen, or fixed a priori where noted as a
deviation. Probabilities are calibrated by one-vs-rest isotonic regression
(Zadrozny and Elkan, 2002) fitted on the probability-calibration partition of the source and
renormalised to sum to one; the calibrator is fitted on the source only and held fixed
across all protocols and analyses. Model seeds vary the classifier only; the source
partition is drawn once and held fixed across seeds, because the matched draws of
Section 4.5 already supply calibration-set variability and re-drawing the partition per
seed would confound the partition draw with model initialisation.

**Table T4. Base classifier performance** (mean macro-F1 over ten seeds, per architecture).

| Dataset | Random forest | Gradient-boosted trees | MLP |
|---|---|---|---|
| NSL-KDD | 0.535 | 0.551 | 0.560 |
| CIC-IDS2017 | 1.000 | 1.000 | 1.000 |
| UGR'16 | 0.995 | 0.971 | 0.830 |
| CIC-IoT-2023 | 0.878 | 0.891 | 0.741 |

The NSL-KDD macro-F1 is depressed by the extreme rarity of U2R and R2L (Table T2), not
by a weak model; this study concerns coverage given a classifier, not classifier
accuracy. The CIC-IDS2017 classifier is near-perfect on the chosen day, with feature
separability audited to exclude label leakage (Section 3.2).

## 4.4 Shift construction and measurement

Shift between source calibration data and target evaluation data is measured, not
assumed, along three axes. The covariate shift S_cov is the cross-fitted area under the ROC curve of a domain classifier trained to distinguish source from target covariates at a fixed per-side subsample, a classifier two-sample test (Ben-David et al., 2010; Lopez-Paz and Oquab, 2017); a value near one half indicates indistinguishable
distributions. Its no-shift reference is a permutation null obtained by splitting the
source pool at random and computing the same statistic, with the 95th percentile taken as
the threshold below which covariate shift is indistinguishable from none. The label-prior
shift S_lab is the total-variation distance between source and target class-prior vectors.
Support shift is reported in two forms because they are not interchangeable. The global
measure S_sup is the fraction of all target evaluation mass in subtypes absent from the
source; the class-conditional measure S_sup,c is the fraction of class c's target evaluation
mass in subtypes absent from the source. The class-conditional form is the one that can
predict class-conditional coverage, and it is the form used whenever a class-specific outcome
is being explained. The two diverge sharply when the focal class is a small share of traffic:
on CIC-IoT-2023 the focal class is 1.4 per cent of the evaluation set, so a class-conditional
value of 0.80 corresponds to a global value near 0.011. Table T1 reports S_sup,c for the focal
class of each environment, and the earlier global values are retained in the repository. The three axes are exercised differently across datasets (Table T1): the
NSL-KDD ladder sweeps S_sup from 0.00 to 0.46 while its S_cov stays in 0.84–0.90,
CIC-IDS2017 carries support and label shift together, and UGR'16 carries covariate shift
alone with S_lab and S_sup fixed at zero.

## 4.5 Matched-draw coverage estimation

Coverage is estimated over matched draws to separate calibration-set variability from
model and partition effects. For each of the thirty models, ten matched draws are formed;
within a draw the evaluation set and the target calibration set are sampled disjointly
from the target pool and the source calibration set from the source pool, all at a common
size, using deterministic hash-derived seeds so that estimates are exactly reproducible.
Class-conditional coverage is the fraction of evaluation points of a class whose
prediction set contains the true class, and the mean prediction-set size is recorded
alongside it so that coverage is never reported without its efficiency cost.

## 4.6 Primary analysis and the secondary pooled model

The primary analysis is a within-dataset dose-response. The NSL-KDD ladder raises the
fraction of target mass drawn from unseen subtypes across five rungs while holding the
dataset, model panel, partition and evaluation size fixed, so it manipulates support
shift while covariate shift stays nearly constant. Coverage is modelled on the empirical
logit with rung as the fixed effect of interest and a random intercept per realisation,
and the rung effect is the primary test. Because the lowest rung carries essentially no
support shift while covariate shift is already substantial, the same design also
separates the contribution of the two shift types inside one dataset. The other two
environments serve as independent replications.

A pooled cross-dataset model was preregistered, in which all coverage cells are combined
into a table of covered-count out of evaluation-count annotated with the measured shift
covariates and the protocol, and fitted as a binomial generalised linear mixed model
(Breslow and Clayton, 1993) with the protocol-by-shift interactions as the terms of interest and
the target-supervised protocol as reference. We report it as a secondary and descriptive
analysis rather than as inference, for reasons set out in Section 5.13; the
crossed-random-effects fit is additionally not reliably estimable in the available tooling
and is deferred to a specialised estimator (Bates et al., 2015), recorded as a deviation. No causal claim
rests on it.

## 4.7 Mechanism analysis

To explain why coverage fails, we relate, per class and per architecture, the movement of
the class's nonconformity-score distribution between source and target to the realised
undercoverage. Movement is quantified by the Kolmogorov-Smirnov distance between the source and target
distributions of the true-class score, computed with a deterministic mid-point randomisation
so that the distributions are reproducible; the randomised score of Section 4.2 remains the
coverage of record. The Kolmogorov-Smirnov statistic is a two-sided summary of the largest
difference anywhere between the two distribution functions, and is used here as a broad proxy
for distributional movement. It is not the exact quantity that determines coverage. Realised
class-conditional coverage is F_t,c(q_s,c), the target score distribution evaluated at the
source-calibrated threshold, so the exact deficit is (1 - alpha) - F_t,c(q_s,c): a signed,
one-sided quantity at a single point. Reporting that threshold-specific displacement alongside
the proxy is a required refinement and is identified as such in Section 8. If undercoverage arises precisely when a
class's scores move past the source-calibrated quantile, the score-movement statistic
should track undercoverage across classes and architectures.

## 4.8 Label-free failure monitor

The mechanism analysis uses the true class and is therefore an oracle; at deployment the
analyst does not know the label of an incoming flow. The proposed monitor is label-free.
For each class it compares the source and target distributions of that class's score
restricted to the flows the classifier *predicts* to be of that class, a quantity
requiring no target labels, and measures their Kolmogorov-Smirnov distance. A class that
a shifted detector confidently misroutes into a different class can vanish from the
predictions, leaving the predicted-class distribution with too few points to compare;
this collapse is itself a label-free signal, so the monitor combines the predicted-class
drift, where measurable, with the drop in the class's predicted share, where it is not.
Classes are ranked by this signal within the deployment environment, so the score for one
class depends only on the other classes an operator observes on their own network and never
on data from another dataset; the statistic is therefore deployable rather than
transductive. The monitor is graded against realised undercoverage and against the oracle
score movement, and its blind spot is characterised by the misroute rate, the fraction of a
class's true target flows the detector predicts as some other class. We distinguish
displacement-type drift, where the novel behaviour is still predicted as its class, from
similarity-type drift, where it is confidently misrouted; the monitor is expected to
detect the former and to attenuate on the latter.

## 4.9 Robustness analyses

Several analyses guard against alternative explanations. To exclude label-prior shift, an
inverse-probability-weighting analysis (Horvitz and Thompson, 1952) reweights the target evaluation
set to the source class prior and asks whether the source-held-out undercoverage
persists; the effective sample size guards reliability, with an estimate treated as
inconclusive rather than null below a minimum. Class-conditional coverage is invariant to
this reweighting by construction, which is itself the argument that the focal failure
cannot be a label-prior artefact. To exclude a dependence on the miscoverage level, the
focal results are reported at 0.05, 0.10 and 0.20, and across the four levels of the
specification curve of Section 4.14. To exclude a dependence on the classifier, the
focal result is reported per architecture. To exclude the reading that smaller
source-held-out sets are more efficient, each protocol's coverage is reported jointly with
its prediction-set size. To exclude base miscalibration, the per-class Brier score
(Brier, 1950) and expected calibration error (Naeini et al., 2015) of the calibrated probabilities are
reported on the source calibration pool, held out from the calibrator's fitting partition,
using equal-mass binning (Roelofs et al., 2022).

## 4.10 Preregistration and reproducibility

The study is preregistered. Focal classes, protocols, shift measures, the primary test
and the analysis plan were fixed before any coverage number was computed, and all
subsequent departures are logged as dated amendments and deviations. Data partitions,
calibrated probabilities, coverage tables and every derived result are committed with
deterministic seeds, and partition fingerprints permit independent verification.

## 4.11 Evaluation against the finite-sample guarantee

Coverage is assessed against the guarantee itself rather than against the nominal
level alone. For a class calibrated on n points with the quantile at the k-th
smallest score, k = ⌈(n+1)(1−α)⌉, split conformal satisfies, under exchangeability
and continuous scores,

1 − α ≤ P(Y ∈ C(X)) ≤ 1 − α + 1/(n + 1).

We report this band per class. A class whose coverage falls below the lower edge has
not merely underperformed a target; it has violated a distribution-free finite-sample
guarantee, and the size of the shortfall is the magnitude of that violation. All
conformal quantiles in this study are computed by a single implementation returning
the k-th order statistic exactly (`src/conformal.py`).

## 4.12 Negative controls

Because a coverage failure can in principle arise from an implementation error rather than
from shift, we include a negative control in which the source calibration pool is split at
random into two halves, the quantile is calibrated on one half and evaluated on the other. Source and target are exchangeable by construction, so every feasible
class must land inside its guarantee band. The control is run over the full model
panel with five random splits each. Its residual deviation also bounds the pipeline's baseline conservatism, which matters
because the isotonic calibrator produces tied probabilities and therefore mild atoms in the
score distribution.

A second, independent control arises on CIC-IoT-2023. An earlier construction of that
environment varied the evaluation composition without withholding any subtype from the
source, so it carried no shift of any kind: covariate shift at the permutation null,
negligible prior shift and no support shift. It is retained and reported as a no-shift
control on modern traffic rather than discarded, and its result, focal coverage 0.953 under
the deployable protocol with every class inside its band, is what the theory requires. The
error and the reclassification are recorded in the deviation log.

## 4.13 Statistical inference

Coverage indicators within a class share a calibration set and are not independent
Bernoulli draws, so we avoid tests that assume independence. Uncertainty is quantified
by a cluster bootstrap over model seeds with B = 2000 resamples, and a claim of
violation requires the upper end of the bootstrap interval to fall below the lower edge
of the guarantee band. For classes that retain coverage we make a positive claim rather
than accept a null, using two one-sided tests against a practical equivalence margin of
one percentage point. The family of class-by-dataset claims is corrected by the Holm
and Benjamini-Hochberg procedures. Whether classes exposed to a common shift share a
common coverage is tested by Cochran's Q with the I² statistic, rather than inferred
from inspection of a table.

## 4.14 Specification curve

The study computes two nonconformity scores, adaptive prediction sets and least
ambiguous set-valued classification, two conditioning variants, class-conditional and
marginal, and four miscoverage levels, giving sixteen specifications. Rather than
report the preregistered specification alone, we report the focal result across all
sixteen, so that the headline cannot be an artefact of the analytical choices and the
alternative score serves as a robustness check.

# 5. Results

## 5.1 The conformal implementation is validated before it is used

The negative control of Section 4.12 leaves every feasible class statistically consistent with nominal coverage. The band is a population bound under exchangeability, not a requirement that every finite empirical estimate fall inside it, so consistency rather than containment is the criterion.
For the four feasible NSL-KDD classes the observed coverages are 0.9503, 0.9503, 0.9517 and
0.9583 against bands whose lower edge is 0.95, and every seed-clustered bootstrap
interval overlaps its band (Table T5). Two point estimates sit marginally above the
upper edge, by 0.0001 for the majority class and 0.0006 for Probe, which is the expected
consequence of an isotonic calibrator producing tied probabilities and hence mild atoms
in the score distribution. That residual is the baseline conservatism of the pipeline. At 0.0006 it is comparable in size to the smallest deviations reported below, such as the 0.001 shortfall on one UGR'16 class, and two to three orders of magnitude smaller than the substantive failures. Coverage failures reported in this paper are therefore attributable to
distribution shift and not to the implementation.

**Table T5. Negative control: no shift by construction.** Source pool split at random,
calibrate on one half and evaluate on the other, over the full model panel.

| Class | n_cal | Coverage | 95% CI | Guarantee band | Inside |
|---|---|---|---|---|---|
| DoS | 3440 | 0.9503 | [0.9497, 0.9509] | [0.9500, 0.9503] | yes |
| Normal | 5053 | 0.9503 | [0.9495, 0.9509] | [0.9500, 0.9502] | yes |
| Probe | 876 | 0.9517 | [0.9500, 0.9531] | [0.9500, 0.9511] | yes |
| R2L | 75 | 0.9583 | [0.9533, 0.9633] | [0.9500, 0.9632] | yes |

## 5.2 Where the deployable protocol fails, it fails on every feasible class

Under distribution shift the deployable protocol does not merely fall short of the nominal
level; it falls below the lower edge of the band that the exchangeability guarantee would
imply, and in the three environments where it fails at all it does so on every feasible class
rather than only on the preregistered focal one (Table T6). The fourth environment,
CIC-IoT-2023, shows no failure on any class and is treated in Section 5.7.

A point of terminology, since it recurs. The conformal guarantee is conditional on
exchangeability, and the constructions here deliberately break that assumption. Nothing
reported below shows a theorem failing under its own hypotheses. What is shown is
undercoverage relative to the level the guarantee would deliver were exchangeability to hold,
which is the level a practitioner would in fact rely on. We use the band as a reference for
that target throughout and say "falls below the band" rather than "violates the guarantee". On
NSL-KDD the shortfalls below the guarantee's lower edge are 0.864 for the focal class
R2L, 0.278 for DoS, 0.145 for Probe and 0.023 even for Normal, the majority class. On
CIC-IDS2017 the denial-of-service class falls 0.346 below the guarantee. On UGR'16 two
classes fall 0.415 and 0.151 below it. The two non-deployable protocols, which differ
only in the data forming the quantile, sit inside their bands throughout.

**Table T6. Undercoverage relative to the exchangeability-based band under the deployable protocol, α = 0.05.** Shortfall is the distance below the band's lower edge. CIC-IoT-2023 shows no shortfall on any class and is reported in Table T8.

| Dataset | Class | n_cal | Observed | Guarantee lower edge | Shortfall |
|---|---|---|---|---|---|
| NSL-KDD | R2L (focal) | 149 | 0.086 | 0.950 | 0.864 |
| NSL-KDD | DoS | 6889 | 0.672 | 0.950 | 0.278 |
| NSL-KDD | Probe | 1748 | 0.805 | 0.950 | 0.145 |
| NSL-KDD | Normal | 10101 | 0.928 | 0.950 | 0.023 |
| CIC-IDS2017 | DoS (focal) | 24845 | 0.604 | 0.950 | 0.346 |
| UGR'16 | scan11 | 7500 | 0.535 | 0.950 | 0.415 |
| UGR'16 | scan44 | 7500 | 0.799 | 0.950 | 0.151 |
| UGR'16 | nerisbotnet (focal) | 7500 | 0.947 | 0.950 | 0.003 |
| UGR'16 | background | 30000 | 0.949 | 0.950 | 0.001 |

Two entries deserve separate treatment. The UGR'16 focal class and background class fall
below the guarantee by 0.003 and 0.001, which the bootstrap resolves as statistically
detectable, yet two one-sided tests place both inside a one-percentage-point equivalence
margin. They are therefore reported as practically equivalent to nominal while formally
violating the bound, a distinction that matters when the same word, failure, would
otherwise cover both a shortfall of 0.001 and one of 0.864.

## 5.3 Primary analysis: a dose-response along the novelty ladder

The primary within-dataset test is the NSL-KDD ladder, which raises the fraction of focal
evaluation mass drawn from attack subtypes absent from the source while holding dataset,
model panel, partition and evaluation size fixed. Focal coverage falls monotonically from
0.143 at rung 0.00 to 0.030 at rung 0.80, with seed-clustered bootstrap intervals disjoint
between adjacent rungs at every step (Table T7). A mixed model on the empirical logit with a
random intercept per realisation gives a slope of -2.071 per unit of unseen fraction, standard
error 0.024.

**Table T7. Primary dose-response: NSL-KDD focal coverage under the deployable protocol,
α = 0.05.** Seed-clustered bootstrap intervals, B = 2000.

| Rung (unseen fraction) | S_cov | S_sup | Coverage | 95% CI |
|---|---|---|---|---|
| 0.00 | 0.849 | 0.001 | 0.1431 | [0.1284, 0.1617] |
| 0.20 | 0.857 | 0.114 | 0.1139 | [0.1026, 0.1286] |
| 0.40 | 0.864 | 0.228 | 0.0848 | [0.0763, 0.0959] |
| 0.60 | 0.875 | 0.341 | 0.0582 | [0.0522, 0.0662] |
| 0.80 | 0.893 | 0.454 | 0.0298 | [0.0267, 0.0339] |

Three analyses establish what that slope is and is not.

*The effect is not created by the upper rungs.* Restricting to rungs 0.00 to 0.40, below the
level at which one dominant subtype must appear in every realisation because no alternative
carries sufficient mass, gives a slope of -1.475, standard error 0.061, which is 71 per cent
of the full-ladder value. The trend is present and strongly significant in the unconstrained
region; the upper rungs steepen it.

*The class-level effect is a mixture of fixed per-subtype coverages.* Each subtype's own
coverage is essentially invariant across rungs. The largest within-subtype range is 0.042,
against a class-level swing of 0.113, and the dominant subtype `warezmaster` moves by 0.005
with p = 0.79. So the ladder does not change how any subtype behaves; it changes which
subtypes are present, and the class coverage follows as the mixture-weighted average.

*The effect therefore concentrates in one component.* Leave-one-subtype-out confirms this:
removing `warezmaster` collapses the trend to 8 per cent of its value, removing `snmpguess`
leaves 69 per cent, and removing any other subtype changes it by under 3 per cent. This is not
fragility but arithmetic. `warezmaster` is the only R2L subtype the source-calibrated quantile
still covers, at 0.243 against 0.000 to 0.037 for every other subtype, while holding 32.7 per
cent of target mass. A mixture whose components are fixed must move in proportion to the
component that differs.

The sign is stable under every leave-one-out. The magnitude is not, and we report the
lower-rung slope as the conservative estimate rather than the full-ladder slope alone.

## 5.4 Novelty is not the operative variable: a placebo ladder

If the ladder works by changing which subtypes are present rather than by introducing
novelty, then a ladder built entirely from subtypes the source has already seen should move
coverage just as much, with no support shift at all. It does, and by a wide margin.

Among the subtypes present in the source calibration pool, realised coverage ranges from
0.007 for `guess_passwd`, which has 11 calibration points, to 0.243 for `warezmaster`, which
has 3. We therefore construct a placebo ladder in which the focal evaluation mass is drawn
only from these two subtypes, varying their ratio across five rungs. The support shift is zero
at every rung by construction and is verified rather than assumed. The non-focal portion of
each evaluation set uses identical row indices across rungs within a realisation, so nothing
but focal composition can move the result.

**Table T8. Placebo ladder: focal coverage with no support shift, α = 0.05.** Evaluation mass
drawn only from subtypes present in the source. Novelty ladder shown for comparison.

| Fraction `guess_passwd` | 0.00 | 0.25 | 0.50 | 0.75 | 1.00 | swing |
|---|---|---|---|---|---|---|
| Focal coverage | 0.3076 | 0.2331 | 0.1614 | 0.0814 | 0.0097 | **0.298** |
| S_sup | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | |
| Score movement (KS) | 0.801 | 0.836 | 0.873 | 0.914 | 0.972 | |
| *Novelty ladder coverage* | *0.143* | *0.114* | *0.085* | *0.058* | *0.030* | *0.113* |

The placebo ladder moves coverage by 0.298 against the novelty ladder's 0.113, a ratio of
2.63, while the support shift stays at exactly zero. Novelty is therefore not the operative
variable. What moves coverage is where a subtype's scores sit relative to the source-calibrated
quantile, and introducing unseen subtypes is one way, but not the only way and not the most
effective way, of moving them.

Score movement tracks the placebo ladder monotonically, from 0.801 to 0.972, in a setting
where support shift is pinned at zero and cannot be the explanation. This is the one place in
the study where movement and novelty are separated experimentally rather than statistically,
and movement is what carries the effect.

![**Figure 8.** The placebo ladder. (a) Focal coverage against ladder position for the
novelty ladder, which introduces subtypes absent from the source, and for the placebo ladder,
which rearranges mass among subtypes the source has already seen and holds the support shift at
exactly zero. The placebo moves coverage 2.6 times further. (b) Within-subtype coverage range
across the novelty rungs for each subtype, against the class-level swing: every component is
close to invariant, so the class-level dose-response is a mixture average of fixed per-subtype
coverages.](figs/fig8_placebo.png)

The consequence for the wider argument is that `S_sup` should be read as a construction device
rather than a cause. It is the quantity the ladder manipulates, and it correlates with coverage
because manipulating it happens to move scores; it is not the reason coverage falls.

## 5.5 What the ladder's zero point does and does not establish

The measured shift covariates permit a decomposition the cross-dataset design could not
support, and the earlier version of this paper drew a stronger conclusion from it than the
data sustain. We state the corrected version.

At rung 0.00 the support shift is 0.001 and the covariate shift is 0.849; across the ladder
the covariate shift moves only from 0.849 to 0.893 while support shift sweeps to 0.454. Of the
total focal gap of 0.920 below nominal, 0.807 is already present at rung 0.00 and the ladder
adds 0.113.

What that 0.807 is *not* is a covariate-shift effect. Rung 0.00 has no unseen subtypes, but it
is not a no-shift condition in any other sense. The R2L source calibration pool is 86.6 per
cent `warezclient`, a subtype with zero target instances, while the target is 42.7 per cent
`guess_passwd` and 32.7 per cent `warezmaster`, which have 11 and 3 source instances
respectively. The quantile is fitted on one subtype and evaluated on different ones even
before the ladder begins. Section 5.4 shows that composition of exactly this kind is
sufficient to move coverage by 0.298 with no support shift at all, which is larger than the
entire ladder effect.

The 0.807 should therefore be read as the share of the gap not attributable to *labelled
subtype novelty*, and it is substantially composed of subtype substitution among nominally
seen subtypes. A domain-classifier AUROC of 0.849 establishes that source and target features
are distinguishable; it does not establish covariate shift with an invariant conditional law,
and it does not exclude the composition effect that Section 5.4 demonstrates directly. We
withdraw the earlier attribution of 87.7 per cent of the gap to covariate shift.

This also exposes a limitation of `S_sup` as defined. A subtype with 11 calibration points
against 1,231 target instances is, for the purpose of forming a conformal quantile, effectively
unsupported, yet the binary in-source test counts it as seen. A measure of support adequacy
rather than support presence would capture what the current definition misses, and is
identified as necessary in Section 8.

## 5.6 Replication in two further environments

The failure replicates in two independent environments with different shift constructions and different focal classes. A fourth environment, treated separately in Section 5.7, does not replicate it, and that is informative rather than contradictory. On CIC-IDS2017, where support shift is induced by withholding
denial-of-service variants from calibration, focal coverage under the deployable protocol
is 0.604 with an interval of [0.597, 0.611] against 0.988 for target-supervised
calibration. On UGR'16, where the shift is purely covariate at fixed support, the
preregistered focal class holds at 0.947 while two other classes collapse. In every
environment the non-deployable protocols retain coverage, so the failure is a property of
source-only calibration under shift and not of conformal prediction itself.

## 5.7 Subtype novelty is not sufficient to produce undercoverage

The three environments above all carry covariate shift, and the decomposition of Section 5.4
attributes most of the NSL-KDD failure to it. CIC-IoT-2023 supplies the complement: support
shift in isolation, with the covariate shift held at the permutation null and the label-prior
shift negligible (Table T1). If novelty at the subtype level were sufficient to break class-conditional coverage, this is
where it would show. We state the claim in those terms deliberately. The withheld subtypes are
absent from the source by label, but their feature distributions evidently remain inside the
region the model has already learned for the family, so this construction establishes the
insufficiency of semantic subtype novelty rather than of feature-space support loss. A
construction in which source support is genuinely absent in the model-relevant feature space
might behave differently, and we do not claim otherwise.

It does not. Focal coverage under the deployable protocol is 0.949, 0.952, 0.951, 0.952 and
0.952 as the novel fraction rises from 0.00 to 0.80, against a nominal 0.95 (Table T9). At the
top rung the seed-clustered interval is [0.950, 0.954]. Every one of the eight classes sits
inside its guarantee band under all three protocols, no class is infeasible, and the mean
prediction-set size differs by 0.014 between protocols. At a class-conditional novel fraction of 0.80, nearly twice the largest value reached on NSL-KDD, nothing fails.

**Table T9. CIC-IoT-2023: focal coverage under the deployable protocol across the
support-shift ladder, α = 0.05.** Nominal 0.95. S_cov is at the permutation null throughout.

| Novel fraction (S_sup) | 0.00 | 0.20 | 0.40 | 0.60 | 0.80 |
|---|---|---|---|---|---|
| SHC | 0.9491 | 0.9517 | 0.9509 | 0.9520 | 0.9519 |
| TSC | 0.9512 | 0.9532 | 0.9497 | 0.9497 | 0.9482 |
| REC | 0.9519 | 0.9519 | 0.9519 | 0.9519 | 0.9519 |

This is the mechanism's negative prediction, and testing it is the point. Section 5.10 holds
that a class undercovers when its nonconformity-score distribution moves past the
source-calibrated quantile; it therefore requires that score movement be small here. It is.
At the top rung the focal score movement is 0.089, and 0.108 when restricted to the withheld
subtypes alone, against 0.922 for the NSL-KDD focal class. A tenfold difference in movement,
and coverage follows it rather than following the nominal shift measure.

The reason is measurable rather than merely interpretable, and Section 5.10 supplies the
instrument. The withheld subtypes did move the score distribution: focal movement is 0.089,
essentially the same as UGR'16 nerisbotnet at 0.089. What differs is *where* that movement
occurs. Only 12 per cent of it is realised at the source-calibrated threshold, against 99 per
cent for the NSL-KDD focal class and 96 per cent for UGR'16 scan11. The novelty is visible in
the scores and irrelevant to coverage, because coverage depends on the target distribution
evaluated at one point and the movement happens elsewhere. Support shift as counted by S_sup is therefore not the same thing as support shift that moves scores, and only the latter breaks the guarantee. This also explains why the NSL-KDD ladder of Section 5.3 yields a clean dose-response while the same manipulation here yields none: there the unseen subtypes move the scores, here they do not.

One feature of this environment deserves separate comment because it shows what the trust
layer contributes. The classifier misroutes 53 per cent of true focal flows to another class
at every rung, yet class-conditional coverage holds at 0.95. That is possible only because the
prediction sets are set-valued: at a mean size of 1.79 the true class survives in the set even
when the top-ranked prediction is wrong. A point classifier evaluated on the same traffic
would be wrong more often than not on this class, while the conformal set retains its
guarantee.

## 5.8 A satisfied marginal guarantee conceals per-class failure

Under the two valid protocols on NSL-KDD the marginal guarantee is satisfied almost
exactly, at 0.9507 aggregate coverage against a nominal 0.95, yet under that single shared
quantile the rare focal class receives only 0.859, while class-conditional conditioning
delivers 0.956 to the same class on the same data (Table T10). A practitioner monitoring
the marginal guarantee alone would observe a system performing to specification while the
class that matters most was undercovered by nine percentage points. Under the deployable
protocol both collapse, to 0.720 aggregate and 0.071 focal. This result motivates the
class-conditional framing of the study and shows that aggregate coverage reporting is not
sufficient to certify a conformal detector.

**Table T10. Marginal versus class-conditional conditioning, NSL-KDD, α = 0.05.**

| Protocol | Marginal, aggregate | Marginal, focal R2L | Class-conditional, focal R2L |
|---|---|---|---|
| REC | 0.9507 | 0.8591 | 0.9562 |
| TSC | 0.9507 | 0.8595 | 0.9536 |
| SHC | 0.7200 | 0.0714 | 0.0860 |

## 5.9 Covariate-shift failure is selective, and the selectivity is tested

UGR'16 exposes every class to one and the same aggregate feature drift, yet the classes do not
share a common coverage. Three classes sit at or near nominal, background at 0.949, dos at
0.950 and the focal nerisbotnet at 0.947, while scan11 collapses to 0.535 and scan44 to
0.799. Cochran's Q on the five per-class coverages, weighted by inverse variance, is 10,110 on four
degrees of freedom with I² of 100 per cent. That statistic assumes independent effect
estimates, which these are not: the classes share trained models, probability calibrators,
target weeks and matched draws, so the nominal p-value is not formally valid and the statistic
is reported as a descriptive measure of heterogeneity magnitude rather than as a test. The
heterogeneity is large by any reading, but a class-by-protocol interaction model or a paired
cluster bootstrap is required before it is called decisive and
essentially all of the between-class variation is genuine heterogeneity rather than
sampling noise. Which classes fail cannot be read from the aggregate shift magnitude. The
preregistered focal class holds and is reported as such; the scan collapse is a discovered
finding, is not retrospectively promoted to focal, and rests on a single covariate
environment, so it is offered as a phenomenon requiring replication.

## 5.10 Score movement explains the failures

Because the three architectures fitted to a given dataset and class share the same data and
the same shift, they are not independent observations, so the relationship between score
movement and undercoverage is estimated at the class level, one ladder rung per laddered
dataset so that no environment dominates the sample. Across the twenty-eight class-level
cells of the four datasets, the Kolmogorov-Smirnov distance between source and target
true-class score distributions is rank-correlated with realised undercoverage at a Spearman
coefficient of 0.844 (p = 1.7 × 10⁻⁸), with a bootstrap interval of [0.610, 0.939]
(Figure 2). The relationship spans movement from 0.000 to 0.922 and undercoverage from
−0.050 to +0.876.

This coefficient is lower than the 0.926 obtained over the first three datasets, and the
reason is that the fourth environment is a harder test rather than a weaker one: it occupies
the low-movement, no-failure corner and forces the relationship to hold across a range the
earlier datasets never reached. Two checks establish that the pooled figure is not carried by
any single environment. Removing each dataset in turn gives 0.926 without CIC-IoT-2023, 0.873
without UGR'16, 0.785 without NSL-KDD and 0.538 without CIC-IDS2017, so the statistic is
never dependent on one source and leans least on the environment added last.

Within-dataset correlations are 0.900 on NSL-KDD, 0.841 on CIC-IDS2017 and 1.000 on UGR'16.
On CIC-IoT-2023 it is −0.667, and that value should be read as an artefact of range
restriction rather than as counter-evidence. Every class in that environment lies within
0.006 of nominal coverage, so there is no failure for score movement to predict, and a rank
correlation computed over a variable that never leaves a 0.006 band is ordering measurement
noise. A permutation test confirms it: the observed value is not distinguishable from chance
at p = 0.079. The environment tests the mechanism's negative prediction, that low movement
implies no failure, and that prediction holds for all eight of its classes. A class undercovers when target score mass crosses above the source-calibrated threshold. The
two-sided movement statistic tracks that closely enough across these environments to order the
outcomes, but it is a proxy and its relationship to coverage is not constant.

Coverage is the target distribution function evaluated at the source threshold, so the deficit
decomposes exactly as the signed displacement at that threshold plus a finite-sample
calibration slack bounded by 1/(n + 1). We verified this identity numerically to 1.1e-16. The
diagnostic quantity is then the fraction of the two-sided movement realised at the threshold,
which ranges from 0.05 to 0.99 across the class cells of this study. Where a class fails, that
fraction is near one: 0.99 for the NSL-KDD focal class, 0.96 and 0.87 for the UGR'16 scan
classes. Where a class holds, the movement occurs away from the threshold: 0.05 for UGR'16
nerisbotnet and 0.12 to 0.28 for the CIC-IoT-2023 classes. Two distributions can share a
movement statistic while one shifts mass below the threshold and the other above; the signed
displacement separates them and the two-sided statistic cannot.

One consequence must be stated because it constrains what the proxy may be used for. In
environments where nearly all movement is realised at the threshold, the movement statistic and
the coverage deficit become close to the same quantity: on the NSL-KDD focal subtypes the
correlation between the measured statistic and (1 - alpha) minus coverage is 0.997. A
within-environment correlation between movement and undercoverage there is therefore largely
definitional and is not reported as evidence. The cross-dataset correlation retains its meaning
precisely because the realised fraction varies so widely between environments. This unifies the preceding sections: it is the movement of the score distribution, whatever its cause, that breaks the guarantee, which is why covariate shift of sufficient magnitude suffices, why failure under a common shift is class-selective, and why support shift that leaves scores in place, as in Section 5.7, breaks nothing at all.

![**Figure 2.** True-class nonconformity-score movement (KS distance, source vs target) versus realised undercoverage. Because architectures fitted to the same dataset and class are not independent, the reported statistic is estimated at the class level, one ladder rung per laddered dataset, where Spearman is 0.844 (n = 28 across four datasets, 95% CI [0.610, 0.939]). The NSL-KDD focal class R2L, with the largest movement, shows the largest undercoverage; CIC-IoT-2023 occupies the low-movement, no-failure corner.](figs/fig2_mechanism.png)

## 5.11 Robustness

*Prior shift.* Class-conditional coverage is invariant to reweighting the target to the
source class prior by construction, and this is verified numerically on CIC-IDS2017 and
UGR'16, where the focal coverage changes by 0.0000. On CIC-IDS2017, whose aggregate coverage
of 0.936 conceals the focal failure behind a benign majority, reweighting lowers the
aggregate to 0.770 and exposes it.

*Analytical choices.* The focal failure appears in all sixteen specifications of Section 4.14,
formed by two nonconformity scores, two conditioning variants and four miscoverage levels
(0.01, 0.05, 0.10, 0.20), with shortfalls ranging from 0.370 to 0.987, so it is not an artefact
of the score, the conditioning or the level. The full specification table is released with the
code; it is summarised here rather than plotted.

*Miscoverage level.* The outcomes do not depend on the choice of alpha (Figure 4). Focal
coverage under the deployable protocol is 0.030, 0.023 and 0.017 on NSL-KDD at alpha = 0.05,
0.10 and 0.20; 0.604, 0.556 and 0.479 on CIC-IDS2017, with the shortfall widening as the level
loosens; 0.947, 0.895 and 0.790 on UGR'16 and 0.952, 0.908 and 0.817 on CIC-IoT-2023, both
tracking nominal throughout; and the UGR'16 scan classes fall short at every level. Failures
and nulls alike are stable across the grid.

*Architecture.* All three architectures fail, with pooled focal coverage of 0.111 for the
multilayer perceptron, 0.082 for the gradient-boosted ensemble and 0.064 for the random
forest, against a nominal 0.95. The intervals for the perceptron and the random forest do
not overlap, so the severity of the failure depends on the classifier by a factor of about
1.7, while the ladder slope is unchanged. The qualitative conclusion is architecture
independent; its magnitude is not, and a practitioner cannot assume that changing the
underlying model repairs the trust layer.

*Efficiency and calibration.* The deployable protocol's narrower prediction sets are a
symptom of failure rather than a mark of efficiency, since wherever it undercovers its sets
are both smaller and miss coverage, for example 2.04 against 4.68 on NSL-KDD at coverage
0.030 against 0.953 (Figure 5). The calibrated probabilities are well calibrated in distribution, with class-averaged expected calibration error at or below 0.002 on all four datasets, including 0.0006 mean and 0.0015 maximum on CIC-IoT-2023 (Figure 6), so the failures are not a base-miscalibration artefact.

*Calibration-set size.* The per-class calibration sets differ in size across protocols for a
structural reason: on NSL-KDD the deployable protocol calibrates the focal class on 149 source
points against 297 for the target-supervised protocol, because R2L is rare at source and common
at target. Under exchangeability a smaller calibration set biases towards over-coverage, since the band
is bounded above by 1/(n + 1), and the negative control confirms this. That argument does not
survive the loss of exchangeability: once the target score distribution has moved, threshold
estimation noise from a smaller calibration set can move realised coverage in either
direction. We therefore report the asymmetry as an acknowledged confound of the natural-budget
design rather than as a bias of known sign. A class-budget-matched contrast, in which TSC and
SHC are subsampled to identical per-class calibration counts, is required to separate
provenance from support and is not performed here.

*Implementation.* An earlier quantile form used in several intermediate analyses returned one
order statistic above the definition of Section 4.11, which inflates coverage by approximately
1/n and is therefore conservative with respect to every undercoverage finding. Recomputation
puts the difference on the reported focal coverages at 0.00005 and 0.00015, below the
precision at which results are reported.

![**Figure 4.** Alpha-sensitivity across all four environments. Focal SHC coverage versus the nominal level (1 - alpha) at alpha in {0.05, 0.10, 0.20}. NSL-KDD R2L and CIC-IDS2017 DoS undercover at every level; UGR'16 nerisbotnet and CIC-IoT-2023 Web track nominal at every level; the UGR'16 scan classes collapse at every level. Neither the failures nor the nulls depend on the choice of alpha.](figs/fig4_alpha.png)

![**Figure 5.** Efficiency across all four environments. Focal coverage versus focal prediction-set size for each protocol and dataset. Wherever SHC undercovers, its sets are smaller and miss coverage; TSC and REC pay a larger set width. On CIC-IoT-2023, where coverage holds, the three protocols sit together.](figs/fig5_efficiency.png)

![**Figure 6.** Calibration quality of the isotonic-calibrated probabilities on the held-out source calibration pool, for all four environments. (a) Per-class expected calibration error and (b) per-class Brier score, by dataset. On CIC-IoT-2023, where coverage holds, this also forecloses the converse objection that the null is an artefact of unusually good or poor calibration. All per-class ECE values fall at or below 0.002 (dashed line), confirming that the probabilities feeding the conformal layer are well calibrated in distribution.](figs/fig6_calibration.png)

## 5.12 Label-free monitoring, its per-dataset behaviour, and its boundary

Pooled across the fifty-seven feasible class cells it is rank-correlated with realised
undercoverage at 0.738 and separates undercovering classes with an area under the ROC curve
of 0.930, with a bootstrap interval of [0.851, 0.990], against an oracle using true labels
at 0.925 and 0.96; its performance is stable to the threshold defining an undercovering
class (Figure 3).

The monitor is evaluated on the three environments in which coverage actually fails; on CIC-IoT-2023 there is no failure to predict, so it does not apply there. Across those three, performance is consistent rather than carried by any one of them (Table T11): 0.926 on NSL-KDD, 0.955 on CIC-IDS2017 and 0.981 on UGR'16, with every
interval excluding chance. The intervals are nonetheless wide, since each environment
contributes between twelve and thirty class cells, so the per-environment estimates should
be read as consistent in direction rather than precisely resolved.

**Table T11. Label-free monitor by dataset.**

| Dataset | Cells | Undercovering | Monitor ρ | AUROC | 95% CI | Oracle ρ |
|---|---|---|---|---|---|---|
| NSL-KDD | 12 | 9 | 0.776 | 0.926 | [0.667, 1.000] | 0.886 |
| CIC-IDS2017 | 30 | 14 | 0.768 | 0.955 | [0.840, 1.000] | 0.896 |
| UGR'16 | 15 | 6 | 0.824 | 0.981 | [0.893, 1.000] | 0.979 |
| Pooled | 57 | 29 | 0.738 | 0.930 | [0.851, 0.990] | 0.925 |

The monitor's limitation is structural. It detects displacement-type drift, in which novel
behaviour is still predicted as its own class so that the predicted-class distribution
moves,
but it attenuates on similarity-type drift, in which the detector confidently misroutes
novel
behaviour into a familiar class so that the predicted-class distribution barely moves. The
clearest instance is UGR'16 scan11, which undercovers by 0.415 and whose movement the oracle
sees at 0.52, while the label-free signal registers only 0.14 at a misroute rate of 0.56. A
formal characterisation of the boundary is not established: the rank correlation between the
misroute rate and the size of the blind spot is 0.25 and not significant at the available
sample size. We report the boundary as a demonstrated regime rather than a predictive rule.

![**Figure 3.** The label-free coverage-failure monitor. (a) The monitor signal (predicted-class score drift, requiring no target labels) versus realised undercoverage across the 57 feasible class cells (Spearman 0.738, AUROC 0.930). (b) Label-free drift versus oracle (true-label) drift: points far below the diagonal are the similarity-type blind spot, where a novel class is confidently misrouted so the predicted-class distribution barely moves.](figs/fig3_monitor.png)

## 5.13 Abstention does not repair the failure, and the reason is instructive

The monitor identifies which classes will undercover, which raises the operational question
of what to do next. The natural answer is triage: abstain on the least trustworthy alerts,
escalate them to an analyst, and retain the conformal guarantee on the remainder. We
evaluate this with a policy that is deployable, in that it never consults a label. For each alert we compute the margin

m(x) = max over classes c of ( q_c - s(x, c) ),

where q_c is the source-calibrated threshold for class c and s(x, c) the nonconformity score,
and escalate in ascending margin so the most atypical alerts reach the analyst first. A
negative margin means an empty prediction set and therefore a certain miss. Classes whose
threshold is infinite under the feasibility rule are excluded from the maximisation rather
than contributing an infinite margin; scores are on a common scale across classes and are not
renormalised; ties are broken by a fixed ordering of the class index; and the retained-coverage
denominator is the count of retained alerts whose true class is the focal class.

The policy substantially improves the marginal guarantee: escalating a tenth of alerts raises
aggregate coverage from 0.936 to 0.985 on CIC-IDS2017 and from 0.879 to 0.916 on UGR'16. It
does almost nothing for the class-conditional guarantee where that guarantee has failed
(Figure 7), and on the classes that fail worst it does something more troubling than nothing.

Evaluated on the UGR'16 classes that actually fail rather than on focal classes that largely
held, scan11 moves from 0.535 to 0.598 and scan44 from 0.799 to 0.853 when half of all alerts
are escalated, neither reaching nominal within that budget. Meanwhile the classes that were
already sound are pushed into over-coverage, dos to 1.000 and background to 0.996. The
disparity between the worst and best served class barely moves, from 0.415 to 0.402, while half
the analyst budget is consumed.

The reason is that the policy is anti-correlated with need. Uniform escalation would retain
exactly one minus the escalated fraction of every class. Instead the failing classes are
retained *above* uniform at every budget, scan11 by 0.028 to 0.053 and scan44 by 0.021 to
0.044, while the sound classes are retained below it, dos by -0.020 to -0.033. The mean
deviation is +0.039 for the failing classes against -0.009 for the holding ones. A queue
ordered by typicality reaches the confident misroutes last, because a confident misroute is by
construction atypical of nothing. On NSL-KDD, escalating half of all alerts moves focal coverage from 0.029
to 0.030. On CIC-IDS2017 the same budget moves it from 0.604 to 0.667, still far below
nominal, and by then almost half the focal-class alerts have been escalated. Only UGR'16
reaches nominal, at an escalation of 0.025, and its focal class was already at 0.947 before
any abstention.

The reason is the mechanism of Section 5.10, and it explains a limit rather than a
shortcoming of the policy. On NSL-KDD the empty-set fraction is exactly zero: every flow
receives a non-empty prediction set that simply does not contain its true class. The alerts
that break class-conditional coverage are not atypical flows sitting near the edge of every
quantile, but flows the shifted detector confidently assigns to the wrong class, which
therefore carry a large margin and are escalated last. This is the same identifiability
limit that produces the monitor's similarity-type blind spot in Section 5.10: a flow whose
true class is R2L but which the model confidently predicts as Normal is, to any label-free
statistic, indistinguishable from a confident correct prediction.

The practical consequence is that the failure is not repairable by alert-level triage. An
operator can buy back the marginal guarantee cheaply, and can use the monitor to know which
classes are affected, but restoring the per-class guarantee requires information the target
does not supply. That returns the argument to the lever identified in Section 6: obtaining
even a small labelled sample of target traffic, which is expensive but not impossible,
whereas triage alone is neither sufficient nor, on the evidence here, of any material help.

![**Figure 7.** Label-free selective prediction on UGR'16, showing the classes that actually fail rather than focal classes that largely held. (a) Coverage among retained alerts against the fraction escalated to an analyst; the policy orders by margin and never consults a label. (b) The fraction of each class still retained. The failing classes scan11 and scan44 are retained above the uniform rate at every budget while the sound classes are retained below it, so the policy escalates the alerts that least need review.](figs/fig7_selective.png)

## 5.14 Secondary analysis: pooled cross-dataset model

For completeness we fit the preregistered pooled model over all 49,500 coverage cells, with
the caveat that it cannot support inference at this design. The interaction between the
deployable protocol and support shift is negative under every specification, at −0.374, and
the interaction with covariate shift is sign-unstable across estimators. The pooled
sample is
dominated by one dataset, with 36,000 of 49,500 cells from NSL-KDD, the shift covariates
vary
almost entirely between three clusters, and clustering at the dataset level widens the
standard errors by a factor of 4.3 while three-cluster inference is itself unreliable
(Cameron and Miller, 2015). We
therefore treat the pooled coefficients as descriptive and rest the causal claim on the
within-dataset dose-response of Section 5.3 and the decomposition of Section 5.5.

# 6. Discussion

**The deployable protocol does not deliver its promise where it matters most.** The
central practical message is that adopting conformal prediction as a trust layer for
intrusion detection, calibrated in the only way an operator can calibrate it, does not
deliver the advertised class-conditional coverage under realistic shift, and the failure
concentrates precisely on the classes an operator most needs to trust: rare attack
classes and novel attack variants. On the two support-shift datasets the focal attack
class is covered at 0.030 and 0.604 against a nominal 0.95, a shortfall large enough that
a set-valued detector deployed under this protocol would silently omit the true class
from a large fraction of its predictions on exactly the traffic that motivates the
system. Because the target-supervised and recalibrated protocols, which differ only in
the calibration set, retain nominal coverage, the failure is not a defect of conformal
prediction; it is a defect of source-only calibration under shift. Because a negative control on exchangeable data places every class inside its guarantee band, these failures are attributable to shift and not to the implementation. Nor are they repairable by triage: a label-free abstention policy that escalates the least trustworthy alerts recovers the marginal guarantee cheaply but leaves the per-class guarantee essentially untouched (Section 5.14), because the alerts that break it are confident misroutes rather than atypical flows. And because all three
architectures fail, though by margins differing by a factor of about 1.7, changing the
underlying classifier does not repair the trust layer. This reframes the practitioner's
question from "should I use conformal prediction" to "can I obtain even a small labelled
sample of target traffic," since where such a sample is available the
target-supervised protocol restores coverage, making periodic active labelling of a
target sample a concrete and effective lever.

**Neither the category nor the nominal magnitude of shift predicts the failure, and aggregate drift monitoring is insufficient.** A placebo ladder built only from subtypes the source has already seen moves focal coverage by 0.298 with the support shift held at zero, against 0.113 for the novelty ladder itself. A fourth environment closes the argument from
the other side: on modern IoT traffic with covariate shift pinned at the permutation null,
support shift swept to 0.80 produces no coverage failure at all. Covariate shift of
sufficient magnitude is therefore by itself enough to break the guarantee, and support
shift compounds a failure it did not cause. This also reconciles the environments, since
UGR'16 retains its focal coverage at a covariate shift of 0.69 where NSL-KDD loses it at
0.85. What the classes that fail have in common is neither a taxonomic category of shift nor a
larger nominal shift value, since the fourth environment reaches a class-conditional novel
fraction of 0.80 without failing while NSL-KDD fails at 0.45. What they share is the movement
of their score distributions. Neither aggregate measure predicts the outcome: the
same nominal support shift destroys coverage on one dataset and leaves it untouched on
another, and the same is true of covariate shift across classes within a single dataset. Covariate shift additionally produces a
failure that is selective and invisible to aggregate shift statistics. Under one
covariate shift of fixed magnitude, some classes
held coverage and others collapsed, and no dataset-level shift measure distinguished
them. The operational implication is direct: a monitoring dashboard that reports an
aggregate drift score is not sufficient to certify a conformal detector's trustworthiness,
because the same aggregate shift can leave one class safe and break another. Trust must
therefore be assessed per class rather than in aggregate.

**Why the failures happen, and what a label-free monitor can and cannot see.** The
mechanism analysis reduces the phenomenon to a single, measurable cause: a class
undercovers exactly when its nonconformity-score distribution moves past the source-
calibrated quantile. This is intuitive in hindsight, the source quantile is fixed and the
target scores drift out from under it, but it is not trivial, because it holds tightly
and uniformly across classes, architectures and shift types, and it explains the selective
covariate-shift result that no aggregate measure could. It is also constructive, because a
signal that detects such movement without labels would predict failure, which is what our monitor does at a pooled area under the ROC curve of 0.93, consistently across the three environments in which coverage fails. The monitor's
boundary is equally
important and is a genuine identifiability limit rather than an engineering shortfall. When
a shifted detector confidently misroutes a novel class into a familiar one, the novel
traffic never enters the predicted-class distribution being watched, so no predicted-class
signal moves, and the failure is invisible to any label-free monitor of that form; our
predicted-share-collapse fallback recovers such cases only partially. Distinguishing
displacement-type drift, where the monitor succeeds, from similarity-type drift, where it
is blind, is therefore not a tuning detail but the fundamental question a label-free trust
signal for intrusion detection must confront.

**Relation to validity-restoring methods.** The support-versus-covariate distinction also
clarifies when restoration methods would help. Weighted conformal prediction can, in
principle, restore coverage under covariate shift, but it requires estimating a source-to-
target likelihood ratio, an estimation that is itself undermined by support shift and by
the confident misrouting of novel classes, exactly the regime in which our monitor is
blind. Our diagnosis thus delineates the conditions under which such methods are and are
not applicable, and suggests that the hardest cases for coverage restoration coincide with
the hardest cases for label-free failure detection.

# 7. Limitations

Several limitations bound the claims of this paper and are stated plainly. First, the
boundary between the regime in which the monitor succeeds and the regime in which it is blind
is demonstrated but not formally characterised (Section 5.12), so the misroute rate should be
read as a first, insufficient proxy rather than an established predictor. Second, the preregistered pooled cross-dataset
model cannot support inference at this design, for the reasons given in Section 5.14, and no
better-specified fit would repair it; the causal claim rests instead on the within-dataset
dose-response and its replications. Third, the monitor is evaluated only on the three environments in which coverage fails, since CIC-IoT-2023 provides nothing to predict, and although its performance is consistent across those three, each contributes only twelve to thirty class cells, so the per-environment intervals are wide and
the estimates are resolved in direction rather than magnitude. Fourth, the
monitor is diagnostic; it flags coverage failure but does not correct it. Fifth, the
mechanism and monitor analyses use a deterministic mid-point randomisation of the
nonconformity score to obtain reproducible score distributions, which is consistent with,
but not identical to, the randomised score that defines the coverage of record. Sixth,
the per-class calibration sets are not equal in size across protocols, for the structural
reason given in Section 5.9; the asymmetry biases the reported effect towards
conservatism but prevents a strictly size-matched comparison. Seventh, the source
partition is drawn once and shared by all models, so the reported intervals capture model
and draw variability but not partition variability and are correspondingly optimistic.
Eighth, the severity of the failure depends on the classifier, with pooled focal coverage
differing by a factor of about 1.7 across the three architectures, so the magnitudes
reported here should not be read as architecture-free constants. Ninth, the calibration
evidence reports the quality of the calibrated probabilities only; the raw
pre-calibration probabilities were not cached, so a before-and-after comparison would
require retraining and is out of scope. Finally, three of the four datasets are established benchmarks rather than contemporary
captures. CIC-IoT-2023, collected from 105 devices and released in 2023, addresses that
directly, and the mechanism transfers to it unchanged. For the older three the objection
still deserves a direct answer rather than a concession. What is under test here is a
property of a calibration protocol, not the detection performance of a particular model on
current traffic: the question is whether a quantile fitted on labelled source data remains
valid on shifted, unlabelled target data. What an environment must supply to answer it is a
fitted classifier's score distribution, a shift that can be constructed and measured, and
enough per-class data to calibrate, none of which depends on the year the traffic was
captured. The mechanism we identify is stated in terms of scores rather than packets, and it
holds across three architectures and three unrelated shift constructions. For a diagnostic
study, well-characterised benchmarks are in this respect an advantage rather than a
compromise, since their labelling errors are documented and corrected and the shift
constructions can be verified independently by any reader.

What does not transfer automatically is magnitude. Encrypted traffic, different class
balance and different attack families may produce different gap sizes and a different pattern
of which classes fail, so the values reported here should be read as evidence that the
failure occurs and why, not as calibrated expectations for a modern deployment. Within that
scope the individual datasets impose their own caveats: NSL-KDD is dated, CIC-IDS2017's
attacks are synthetically generated and its base classifier is near-perfect on the chosen
day, and UGR'16 required subsampling and the dropping of a non-comparable protocol field, so
its covariate environment represents temporal drift in one provider's traffic rather than
intrusion traffic in general.

# 8. Future work

Several analyses identified above are required before the claims reach their strongest form,
and are listed here rather than left implicit. Class-conditional covariate shift, S_cov,c,
computed by a domain classifier restricted to each class in turn, would replace the aggregate
statistic that Section 5.9 shows cannot predict class-conditional outcomes. The
threshold-specific displacement of Section 4.7, the signed change in the target distribution
function at the source quantile, should be reported alongside the two-sided proxy. A
class-budget-matched contrast, subsampling TSC and SHC to identical per-class calibration
counts, would separate calibration provenance from calibration support. Composition-adjusted
and leave-one-subtype-out analyses of the NSL-KDD ladder would separate the novelty fraction
from subtype identity. Leave-one-environment-out validation of the monitor, with CIC-IoT-2023
included as an all-negative environment measuring specificity and false-alarm burden rather
than excluded for lacking positives, would establish that the monitor is not fitted to the
environments that motivated it. Selective-prediction curves for the UGR'16 scan classes, the
classes that actually fail, would extend the abstention result beyond focal classes that
largely hold. Calibration quality on CIC-IoT-2023 remains to be computed.

The most immediate extension is to complete the characterisation of the monitor's
boundary. This calls for a continuous, model-internal measure of class confusability to
replace the misroute proxy, and for additional environments rich in similarity-type drift,
for which a modern dataset containing confusable attack classes would serve as the
exemplar needed to bring the boundary result to statistical significance. A second
direction is constructive: to convert the monitor from a diagnostic into a remedy by using
its label-free signal to widen prediction sets on the classes it flags, and to test whether
this restores coverage on displacement-type drift while conceding, honestly, that it cannot
on the similarity-type drift where the signal is absent. The negative result of Section 5.14 sharpens this: because alert-level triage cannot reach confident misroutes, a remedy must act on the calibration itself rather than on the alert stream. A second and more immediate direction is replication on contemporary traffic. Because the
mechanism is expressed in terms of score movement rather than packet content, it should
transfer, and a modern IoT or 5G intrusion corpus with a family-holdout construction would
test that prediction directly while supplying the confusable attack classes the boundary
analysis needs. A third direction is inferential, and it is a matter of design rather than of
estimator: no refitting of the
pooled model can identify a covariate interaction that varies only between three dataset
clusters, so what is required is a substantially larger panel of covariate-shift
environments, or repeated shift configurations within datasets of the kind the ladder
provides for support shift. Beyond
these, the framework extends naturally to streaming and online conformal calibration, in
which the monitor could trigger recalibration events, and to adjacent security tasks such
as malware classification, where the same tension between a source-calibrated trust layer
and an unlabelled, drifting target arises.

# 9. Conclusion

We asked, under preregistration, whether the only deployable conformal calibration
protocol for network intrusion detection retains its class-conditional coverage guarantee
under distribution shift, and if not, whether its failures can be detected without target
labels. The answer to the first question is that it does not. Against a negative control
that places every class inside its guarantee band on exchangeable data, source-held-out calibration under shift falls below that band on every feasible class of three environments, by as much as 0.86, while calibration on target data holds; a fourth environment shows no failure at all. A placebo ladder with no support shift moves coverage more than twice as far as the novelty ladder does, and a fourth environment isolating support shift on modern IoT traffic produces no failure at all.
Under pure covariate shift the failure is selective, invisible to aggregate shift
measures, and confirmed heterogeneous by test rather than by inspection. We reduced the phenomenon to a single measurable cause, the movement of a class's
nonconformity-score distribution past the source-calibrated quantile, which orders
undercoverage across twenty-eight class-level cells spanning four datasets at a rank
correlation of 0.84. Building on that cause,
we answered the second question in the affirmative but with an explicit boundary: the label-free monitor predicts coverage failure without target labels, consistently across the three environments in which coverage fails, yet it necessarily attenuates on similarity-type drift, a limit we demonstrate rather than hide. For practitioners, the message is
that a source-calibrated conformal trust layer cannot be assumed to hold under realistic
network drift, that trust must be assessed per class rather than in aggregate, and that a
label-free monitor can flag much but not all of the failure. All data, code and the
preregistration are released to support scrutiny and extension.

# References

Angelopoulos, A.N., Bates, S., 2023. Conformal prediction: a gentle introduction.
Foundations and Trends in Machine Learning 16 (4), 494-591.
https://doi.org/10.1561/2200000101

Barber, R.F., Candès, E.J., Ramdas, A., Tibshirani, R.J., 2023. Conformal prediction
beyond exchangeability. The Annals of Statistics 51 (2), 816-845.
https://doi.org/10.1214/23-AOS2276

Bates, D., Mächler, M., Bolker, B., Walker, S., 2015. Fitting linear mixed-effects models
using lme4. Journal of Statistical Software 67 (1), 1-48.
https://doi.org/10.18637/jss.v067.i01

Ben-David, S., Blitzer, J., Crammer, K., Kulesza, A., Pereira, F., Vaughan, J.W., 2010. A
theory of learning from different domains. Machine Learning 79 (1-2), 151-175.
https://doi.org/10.1007/s10994-009-5152-4

Breslow, N.E., Clayton, D.G., 1993. Approximate inference in generalized linear mixed
models. Journal of the American Statistical Association 88 (421), 9-25.
https://doi.org/10.1080/01621459.1993.10594284

Brier, G.W., 1950. Verification of forecasts expressed in terms of probability. Monthly
Weather Review 78 (1), 1-3.
https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2

Cameron, A.C., Miller, D.L., 2015. A practitioner's guide to cluster-robust inference.
Journal of Human Resources 50 (2), 317-372. https://doi.org/10.3368/jhr.50.2.317

Chen, T., Guestrin, C., 2016. XGBoost: a scalable tree boosting system. In: Proceedings of
the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining.
ACM, pp. 785-794. https://doi.org/10.1145/2939672.2939785

Engelen, G., Rimmer, V., Joosen, W., 2021. Troubleshooting an intrusion detection dataset:
the CICIDS2017 case study. In: 2021 IEEE Security and Privacy Workshops (SPW). IEEE,
pp. 7-12. https://doi.org/10.1109/SPW53761.2021.00009

Gibbs, I., Candès, E.J., 2021. Adaptive conformal inference under distribution shift. In:
Advances in Neural Information Processing Systems, vol. 34. Curran Associates,
pp. 1660-1672.

Guo, C., Pleiss, G., Sun, Y., Weinberger, K.Q., 2017. On calibration of modern neural
networks. In: Proceedings of the 34th International Conference on Machine Learning.
Proceedings of Machine Learning Research, vol. 70. PMLR, pp. 1321-1330.

Horvitz, D.G., Thompson, D.J., 1952. A generalization of sampling without replacement from
a finite universe. Journal of the American Statistical Association 47 (260), 663-685.
https://doi.org/10.1080/01621459.1952.10483446

Liu, L., Engelen, G., Lynar, T., Essam, D., Joosen, W., 2022. Error prevalence in NIDS
datasets: a case study on CIC-IDS-2017 and CSE-CIC-IDS-2018. In: 2022 IEEE Conference on
Communications and Network Security (CNS). IEEE, pp. 254-262.
https://doi.org/10.1109/CNS56114.2022.9947235

Lopez-Paz, D., Oquab, M., 2017. Revisiting classifier two-sample tests. In: International
Conference on Learning Representations (ICLR).

Maciá-Fernández, G., Camacho, J., Magán-Carrión, R., García-Teodoro, P., Therón, R., 2018.
UGR'16: a new dataset for the evaluation of cyclostationarity-based network IDSs.
Computers & Security 73, 411-424. https://doi.org/10.1016/j.cose.2017.11.004

Neto, E.C.P., Dadkhah, S., Ferreira, R., Zohourian, A., Lu, R., Ghorbani, A.A., 2023.
CICIoT2023: a real-time dataset and benchmark for large-scale attacks in IoT environment.
Sensors 23 (13), 5941. https://doi.org/10.3390/s23135941

Naeini, M.P., Cooper, G.F., Hauskrecht, M., 2015. Obtaining well calibrated probabilities
using Bayesian binning. In: Proceedings of the Twenty-Ninth AAAI Conference on Artificial
Intelligence. AAAI Press, pp. 2901-2907.

Pendlebury, F., Pierazzi, F., Jordaney, R., Kinder, J., Cavallaro, L., 2019. TESSERACT:
eliminating experimental bias in malware classification across space and time. In:
Proceedings of the 28th USENIX Security Symposium. USENIX Association, pp. 729-746.

Podkopaev, A., Ramdas, A., 2022. Tracking the risk of a deployed model and detecting
harmful distribution shifts. In: International Conference on Learning Representations
(ICLR).

Roelofs, R., Cain, N., Shlens, J., Mozer, M.C., 2022. Mitigating bias in calibration error
estimation. In: Proceedings of the 25th International Conference on Artificial Intelligence
and Statistics. Proceedings of Machine Learning Research, vol. 151. PMLR, pp. 4036-4054.

Romano, Y., Sesia, M., Candès, E.J., 2020. Classification with valid and adaptive coverage.
In: Advances in Neural Information Processing Systems, vol. 33. Curran Associates,
pp. 3581-3591.

Sadinle, M., Lei, J., Wasserman, L., 2019. Least ambiguous set-valued classifiers with
bounded error levels. Journal of the American Statistical Association 114 (525), 223-234.
https://doi.org/10.1080/01621459.2017.1395341

Shafer, G., Vovk, V., 2008. A tutorial on conformal prediction. Journal of Machine Learning
Research 9, 371-421.

Sharafaldin, I., Habibi Lashkari, A., Ghorbani, A.A., 2018. Toward generating a new
intrusion detection dataset and intrusion traffic characterization. In: Proceedings of the
4th International Conference on Information Systems Security and Privacy (ICISSP).
SciTePress, pp. 108-116. https://doi.org/10.5220/0006639801080116

Tavallaee, M., Bagheri, E., Lu, W., Ghorbani, A.A., 2009. A detailed analysis of the KDD
CUP 99 data set. In: 2009 IEEE Symposium on Computational Intelligence for Security and
Defense Applications (CISDA). IEEE, pp. 1-6.
https://doi.org/10.1109/CISDA.2009.5356528

Tibshirani, R.J., Foygel Barber, R., Candès, E.J., Ramdas, A., 2019. Conformal prediction
under covariate shift. In: Advances in Neural Information Processing Systems, vol. 32.
Curran Associates, pp. 2530-2540.

Vovk, V., Gammerman, A., Shafer, G., 2005. Algorithmic Learning in a Random World.
Springer, New York. https://doi.org/10.1007/b106715

Vovk, V., Nouretdinov, I., Gammerman, A., 2003. Testing exchangeability online. In:
Proceedings of the 20th International Conference on Machine Learning (ICML). AAAI Press,
pp. 768-775.

Zadrozny, B., Elkan, C., 2002. Transforming classifier scores into accurate multiclass
probability estimates. In: Proceedings of the 8th ACM SIGKDD International Conference on
Knowledge Discovery and Data Mining. ACM, pp. 694-699.
https://doi.org/10.1145/775047.775151
