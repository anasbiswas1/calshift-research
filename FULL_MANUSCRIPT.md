# Source-Calibrated Conformal Intrusion Detection Loses Class-Conditional Coverage under Distribution Shift: A Preregistered Diagnosis

## Abstract

Conformal prediction offers distribution-free coverage guarantees and is increasingly proposed
as a trust layer for machine-learning network intrusion detection. Its guarantee assumes
exchangeability between calibration and test data, which deployment breaks: a detector is
calibrated on past traffic and applied to future traffic, and the labels needed to recalibrate
are what an operator lacks. We ask, under preregistration, where the fixed source-calibrated
baseline loses class-conditional coverage and whether its failures can be detected without
labels. Across four datasets, against negative controls confirming validity on exchangeable
data, that baseline undercovers severely on all four feasible NSL-KDD classes, on CIC-IDS2017
denial of service and on two UGR'16 scan classes, by up to 0.86 relative to the
exchangeability-based target, while other classes and an entire fourth environment retain
practically nominal coverage. The contrast against target-supervised calibration survives
matching both protocols to identical per-class calibration sizes, so it reflects
calibration-data provenance rather than sample size. Failure is therefore selective, and an
environment-level shift statistic cannot express that selectivity, being constant within an
environment; a class-conditional one orders the affected classes at Spearman 0.86. Four further
analyses are exploratory and labelled throughout: a placebo construction showing the binary
seen-or-unseen subtype indicator is inadequate, a class-conditional shift measure, a
threshold-level decomposition of the mechanism, and a label-free diagnostic that anticipates
failure at pooled AUROC 0.93 with a demonstrated blind spot. Abstention proves anti-correlated
with need. All data, code and the preregistration are released.

**Keywords:** conformal prediction; network intrusion detection; distribution shift;
uncertainty calibration; coverage guarantees; drift detection.

# 1. Introduction

Machine-learning classifiers are routine in network intrusion detection, yet most emit point
predictions with no calibrated statement of how far they can be trusted. An operator facing an
alert needs to know whether the output is reliable for this flow, so scarce analyst attention
goes where it is warranted. Conformal prediction answers this: it wraps any classifier in a
procedure returning prediction sets with a distribution-free, finite-sample guarantee, so that
at miscoverage level alpha the set contains the true label with probability at least 1 − alpha
(Vovk et al., 2005; Shafer and Vovk, 2008; Angelopoulos and Bates, 2023). Applied per class in
the Mondrian manner it promises a class-conditional guarantee, which is especially appealing
here because the rare classes are the dangerous ones and a marginal guarantee can hide their
failure.

That guarantee rests on exchangeability between calibration and test data, and deployment breaks
it structurally. Traffic drifts: the benign baseline moves with usage and attacks evolve, so a
detector calibrated on one period is applied to a later one. The natural fix, recalibrating on
the target, is unavailable in operation, because obtaining target labels requires exactly the
analyst effort the system is meant to conserve and novel attacks are unlabelled by definition.
The simplest protocol requiring neither target labels nor target-domain adaptation is
source-held-out calibration: fix the conformal quantile on labelled source data and apply it to
the unlabelled, drifted target. Whether coverage survives that move is the question on which the
practical value of conformal intrusion detection turns.

Existing work restores validity under covariate shift when the shift is benign in a specific
sense, for example when the source-to-target density ratio is estimable (Tibshirani et al.,
2019), or when calibration adapts online against labelled feedback (Gibbs and Candès, 2021).
Intrusion detection sits outside those assumptions: its shift includes the arrival of novel
attack subtypes, a change in the support of the distribution rather than a reweighting of a
fixed one, and its operators have no stream of target labels. The practitioner's questions are
therefore not only whether validity can be restored but, more basically, when and why the
source-calibrated baseline fails, whether that failure is visible in aggregate drift statistics,
and whether it can be flagged per class without labels.

We take a diagnostic and preregistered stance. Rather than propose a method and report that it
wins, we fix in advance the datasets, shift constructions, focal classes, protocols, shift
measures and primary test, then ask what the baseline does. Preregistration is what makes a
negative or boundary result credible: because the focal classes and analysis plan were committed
before any coverage number existed, the failures cannot be an artefact of choosing conditions
that produce them, and the one class surviving feature drift is the class named in advance. This
follows the spirit of temporally and spatially honest evaluation in security machine learning
(Pendlebury et al., 2019).

The contributions are: (i) a preregistered, four-dataset, per-class measurement of where
source-calibrated conformal intrusion detection loses class-conditional coverage under realistic
network shift. That split conformal can lose coverage when exchangeability fails is established
theory and is not claimed here; what the theory does not supply, and this does, is which classes
fail, by how much, under which constructed shifts, with the protocol contrast isolated from
calibration sample size and validated against negative controls. (ii) An exploratory placebo
construction separating subtype novelty from score position, showing that composition among
already-seen subtypes is sufficient to move coverage severely, so the binary novelty indicator
is inadequate. (iii) The finding, tested rather than observed, that failure under a common
environment-level shift is selective, with the demonstration that this selectivity is
measurable: a class-conditional shift statistic orders the affected classes at Spearman 0.86
across the nine cells where coverage varies, whereas an aggregate statistic cannot order them at
all, being constant within an environment. (iv) A mechanistic account through
nonconformity-score movement at the calibrated threshold. (v) An exploratory label-free
coverage-failure diagnostic with consistent per-environment performance and a demonstrated blind
spot, developed and evaluated on the same environments and with no external validation set, so
presented as worth testing rather than validated. Figure 1 gives an overview of the study design. (vi) An open release of all pipelines,
calibrated models, coverage tables, figures and the preregistration, with deterministic seeds
and partition fingerprints.

![**Figure 1.** Overview of the study. The labelled source is partitioned to train the classifier f, tune it, fit the isotonic calibrator g, and form the source calibration pool. The three conformal calibration protocols differ only in the data that forms the class-conditional quantile: REC on the evaluation set (a transductive oracle), TSC on a labelled target sample (not deployable), and SHC on the source pool (the fixed source-calibrated baseline). Under distribution shift between source and target, SHC undercovers on the focal class while TSC and REC hold. The label-free monitor compares the predicted-class score distribution on target versus source, requiring no target labels, and flags the classes whose coverage will fail; it catches displacement-type drift but is blind to similarity-type drift, where a novel class is confidently misrouted.](figure1_overview.png)

# 2. Related work

**Conformal prediction.** Conformal prediction produces set-valued predictions with
distribution-free, finite-sample coverage under exchangeability (Vovk et al., 2005; Shafer and
Vovk, 2008), and recent expositions have made it broadly accessible (Angelopoulos and Bates,
2023). For classification, the adaptive prediction set score yields sets whose size adapts to
instance difficulty and improves conditional coverage (Romano et al., 2020), and Mondrian
conditioning provides per-class guarantees (Sadinle et al., 2019; Vovk et al., 2005), which
matter here because a marginal guarantee can be satisfied while a rare attack class is badly
undercovered. We take that combination as our instrument and ask what happens to the per-class
guarantee when exchangeability fails.

**Conformal prediction under distribution shift.** Weighted conformal prediction restores
validity under covariate shift when the source-to-target likelihood ratio is estimable
(Tibshirani et al., 2019); adaptive conformal inference maintains coverage online against
labelled feedback (Gibbs and Candès, 2021); and recent analysis characterises conformal
behaviour beyond exchangeability generally (Barber et al., 2023). These assume either an
estimable density ratio over fixed support or a stream of target labels. Intrusion detection
violates both: novel attack subtypes change the support, and deployment provides no target
labels. Our contribution is prior to method design: we diagnose when and why the
source-calibrated baseline fails, and show that whether a restoration method could help is
itself governed by where the score movement falls relative to the calibrated threshold.

**Drift and unreliability detection.** A separate literature detects distribution or risk shift
after deployment. Online exchangeability testing via test martingales flags violations of the
assumption (Vovk et al., 2003), and risk-tracking methods detect harmful shifts in a deployed
model's error (Podkopaev and Ramdas, 2022). These operate at the level of the overall distribution or risk, and several rely on labelled
feedback. The general observation that model reliability can be tracked under shift is
therefore partly anticipated by this literature, and we differ in three respects that we state
plainly so as not to overclaim. Our diagnostic is tied specifically to conformal
class-conditional coverage failure rather than to distribution change in general; it is per
class and fully label-free, using only predicted-class score distributions; and we report its
blind spot rather than only its successes.

**Intrusion detection benchmarks and evaluation practice.** Learned detectors are commonly
benchmarked on NSL-KDD (Tavallaee et al., 2009), CIC-IDS2017 (Sharafaldin et al., 2018) and
UGR'16 (Maciá-Fernández et al., 2018), and a critical literature has documented labelling and
construction errors in these corpora that change the conclusions drawn from them (Engelen et
al., 2021; Liu et al., 2022). Separately, temporally and spatially honest evaluation has been
shown to alter conclusions substantially in malware classification (Pendlebury et al., 2019).
We inherit that critical posture: we adopt corrected labels where available, audit feature
separability to rule out trivial leakage, and construct shift explicitly rather than assuming
it. We extend it by preregistering the analysis plan so that a negative or boundary result
cannot be an artefact of post hoc choices.

# 3. Datasets and preparation

We evaluate the trust layer on four intrusion detection datasets, each isolating a different
form of shift between calibration and deployment data (Table T1). All raw sources, cleaned
artefacts, partition indices and derived tables are version controlled, and every partition
carries a SHA-256 fingerprint so it can be verified without access to the underlying data.
Per-class composition tables are released with the code.

**Table T1. Study environments.** Measured shift covariates at the primary configuration and
the preregistered focal class. S_cov is an **aggregate** over all classes, retained only to
characterise environments as wholes; it is constant within an environment and cannot describe
the classes inside it, for which Table T10 gives class-conditional values ranging from 0.499 to
1.000 within one environment. The S_sup column is **not** on a common definition across rows
and must not be compared between them: for CIC-IDS2017 (†) it is global, held-out variant mass
over all target rows, so the class-conditional value for DoS is far larger; for NSL-KDD and
CIC-IoT-2023 the ladder controls the class-conditional fraction directly. Reconciling these to
one definition is outstanding work (Section 8).

| Dataset | Source → target | Shift type | S_cov (agg) | S_lab | S_sup | Focal |
|---|---|---|---|---|---|---|
| NSL-KDD | KDDTrain+ → KDDTest+, 5-rung unseen-subtype ladder | covariate + support | 0.84–0.90 | ~0.14 | 0.00–0.46 | R2L |
| CIC-IDS2017 | Wednesday DoS, 5 variant-holdout realisations | variant novelty (+prior) | 0.76–0.77 | 0.44–0.52 | 0.01–0.07 † | DoS |
| UGR'16 | July week 5 → August week 1 | temporal feature drift, fixed support | 0.69 | 0.00 | 0.00 | nerisbotnet |
| CIC-IoT-2023 | 5-rung novel-subtype ladder, 2 web-attack subtypes withheld | semantic subtype novelty | 0.50 agg / 0.65 focal | ~0.01 | 0.00–0.80 | Web |

## 3.1 NSL-KDD

We use the canonical split of NSL-KDD (Tavallaee et al., 2009), KDDTrain+ (125,973 flows) as source and KDDTest+ (22,544) as
target, across the five standard classes. Subtype labels are retained only to construct and
characterise shift, never as model input. KDDTest+ suits a support-shift study because it
deliberately contains subtypes absent from KDDTrain+.

A five-rung ladder draws a fraction f ∈ {0.00, 0.20, 0.40, 0.60, 0.80} of each class's
evaluation quota from unseen subtypes, holding the evaluation set at 2,340 flows at natural
prevalence, with twenty realisations per rung selecting unseen subtypes in randomised order.
Normal is exempt (no attack subtypes) and U2R is exempt (too rare at higher rungs); both are
recorded. Within each realisation the evaluation and target-calibration sets share identical
subtype composition, so the target-supervised protocol is not itself exposed to an uncontrolled
shift. The focal class is R2L, fixed before any coverage number existed as the rarest attack
class supporting the paired contrast in the source calibration pool. Its rarity at source is
the binding constraint, 995 source flows against 2,885 at target, with U2R rarer still at 52
and 67.

## 3.2 CIC-IDS2017

For CIC-IDS2017 (Sharafaldin et al., 2018) we adopt the corrected labelling (Engelen et al.,
2021) and a cleaned release as the version of record, since documented label errors in the
original distribution are substantial enough to change conclusions drawn from it (Liu et al.,
2022). using Wednesday denial-of-service traffic with benign traffic; the task is binary.
Support shift is constructed within the day by withholding DoS variants: Hulk is always
retained in calibration and five realisations withhold different combinations of the remainder
(Slowhttptest; Slowloris; GoldenEye; Slowloris with Slowhttptest; GoldenEye with Slowloris)
while requiring them at evaluation. The variant composition is strongly asymmetric, GoldenEye
holding 32 source flows against 7,361 at target and Slowloris 589 against none, which is what
makes the holdout bite. Because a trivially separable task would make the coverage question
vacuous, we audited feature separability: the most discriminative single feature reaches an
area under the ROC curve of 0.984 and no feature acts as an identifier, so the near-perfect
accuracy is genuine rather than label leakage. The focal class is DoS.

## 3.3 UGR'16

UGR'16 (Maciá-Fernández et al., 2018) provides the temporal-feature-drift environment: one week of July traffic as source and
one week of the following August as target, about a month apart in real
internet-service-provider traffic. Each week was streamed in chunks and subsampled to a common
composition of 200,000 background flows and 50,000 for each of four synthetic attack families
(dos, scan11, scan44, nerisbotnet).

Two provenance decisions are recorded as deviations. The July and August captures come from
different released variants, so the blacklist label is not comparable and is dropped. And the
protocol field, categorical in July, was rendered uninformative in August by an earlier numeric
coercion, so it is dropped from both weeks; the covariate representation comprises nine flow
features, twenty-seven dimensions after one-hot encoding of the TCP flag field. By construction
all four attack families appear in both weeks at equal sampled counts, so S_lab and S_sup are
zero while S_cov is 0.69 against a permutation-null threshold of 0.51. We describe this as
temporal feature drift at retained label support, not as covariate shift in the strict sense:
equal sampled counts and retained broad-label support establish no measured prior shift and a
temporal feature-distribution difference, but they do not establish that the conditional law
P(Y | X) is invariant across the two weeks, and the provenance caveats above make that
assumption unattractive. The focal class is
nerisbotnet, chosen on operational rarity rather than the capped counts.

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

The resulting environment carries large subtype novelty with little else moving in aggregate:
across the ladder the aggregate covariate shift stays at the permutation null, 0.495 to 0.506,
the label-prior shift is negligible at 0.004 to 0.014, and the class-conditional novel
fraction sweeps from 0.000 to 0.800.

We deliberately do not call this support shift in isolation. Section 5.10 measures
class-conditional covariate shift and finds S_cov,Web = 0.654 against an aggregate of 0.512,
so the focal class does carry measurable source-target feature distinguishability even though
the aggregate sits at its null. Reading isolation off an aggregate statistic is precisely the
error that Section 5.10 exists to expose, and we do not commit it here. The environment is
better described as large semantic subtype novelty with moderate focal-class feature drift. No
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
calibrating on in-distribution target data. We study SHC as the simplest fixed, source-calibrated baseline: it requires neither target
labels nor target-domain adaptation. It is not the only protocol deployable without target
labels. Recent work adapts conformal prediction using unlabelled target data or pseudo-labels,
and label-free conformal drift signals have been proposed for streaming intrusion detection.
Those methods are outside the scope of this study, which asks what happens to the fixed
baseline under shift; we do not claim they are undeployable.

The source-held-out protocol (SHC) calibrates on the source calibration pool and is the fixed source-calibrated baseline, requiring
no target labels. The primary contrast is TSC versus SHC. The two protocols differ in calibration-data
provenance and, under natural class prevalence, in class-specific calibration support: they
draw calibration sets of a common overall size, but the per-class counts entering a
class-conditional quantile follow the class composition of the pool they are drawn from. We
do not describe them as differing only in the calibration set. The two protocols draw calibration
sets of a common overall size, but the per-class counts that enter a class-conditional
quantile follow the class composition of the pool they are drawn from, so for a class
that is rare at source and common at target the source-calibrated baseline calibrates on fewer
points. Section 5.12 quantifies this asymmetry and shows that it biases the reported
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
models per dataset (Table T2). Hyperparameters are selected once per architecture on the
validation
partition by macro-averaged F1 and then frozen, or fixed a priori where noted as a
deviation. Because modern classifiers are frequently miscalibrated (Guo et al., 2017), probabilities are
calibrated by one-vs-rest isotonic regression (Zadrozny and Elkan, 2002) fitted on the
probability-calibration partition of the source and
renormalised to sum to one; the calibrator is fitted on the source only and held fixed
across all protocols and analyses. Model seeds vary the classifier only; the source
partition is drawn once and held fixed across seeds, because the matched draws of
Section 4.5 already supply calibration-set variability and re-drawing the partition per
seed would confound the partition draw with model initialisation.

**Table T2. Base classifier performance** (mean macro-F1 over ten seeds, per architecture).

| Dataset | Random forest | Gradient-boosted trees | MLP |
|---|---|---|---|
| NSL-KDD | 0.535 | 0.551 | 0.560 |
| CIC-IDS2017 | 1.000 | 1.000 | 1.000 |
| UGR'16 | 0.995 | 0.971 | 0.830 |
| CIC-IoT-2023 | 0.878 | 0.891 | 0.741 |

The NSL-KDD macro-F1 is depressed by the extreme rarity of U2R and R2L, not
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
analysis rather than as inference, for reasons set out in Section 5.15; the
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
specification curve of Section 4.11. To exclude a dependence on the classifier, the
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

## 4.11 Evaluation criteria, controls and inference

*Coverage band.* Coverage is assessed against the guarantee itself rather than the nominal
level alone. For a class calibrated on n points with the quantile at the k-th smallest score,
k = ⌈(n+1)(1−α)⌉, split conformal satisfies, under exchangeability and continuous scores,
1 − α ≤ P(Y ∈ C(X)) ≤ 1 − α + 1/(n + 1). We report this band per class, so a class below its
lower edge has not merely underperformed a target. All quantiles come from one implementation
returning the k-th order statistic exactly (`src/conformal.py`).

*Negative controls.* Because a coverage failure could arise from an implementation error rather
than shift, we split the source calibration pool at random and calibrate on one half to
evaluate on the other, over the full model panel with five splits. Source and target are
exchangeable by construction, so every feasible class should be statistically consistent with
nominal coverage. The residual deviation also bounds the pipeline's baseline conservatism,
which matters because the isotonic calibrator produces tied probabilities and hence mild atoms
in the score distribution. A second control arises on CIC-IoT-2023: an earlier construction of
that environment varied evaluation composition without withholding any subtype, so it carried
no shift of any kind and is retained as a no-shift control on modern traffic rather than
discarded. Its result, focal coverage 0.953 with every class inside its band, is what the theory
requires; the error and reclassification are in the deviation log.

*Inference.* Coverage indicators within a class share a calibration set and are not independent
draws, so uncertainty comes from a cluster bootstrap over model seeds with B = 2000 resamples,
and a violation claim requires the upper end of the interval to fall below the band's lower
edge. For classes that retain coverage we make a positive claim using two one-sided tests
against a one-percentage-point equivalence margin. Families of class-by-dataset claims are
corrected by Holm and Benjamini-Hochberg. Whether classes under a common shift share a common
coverage is tested by Cochran's Q with I², subject to the dependence caveat in Section 5.9.

*Specification curve.* Two nonconformity scores, two conditioning variants and four miscoverage
levels give sixteen specifications. We report the focal result across all sixteen rather than
the preregistered one alone, so the headline cannot be an artefact of analytical choice.

## 4.12 Preregistration status of each analysis

The study is preregistered, but not every analysis reported here has the same evidential
standing, and presenting them uniformly would overstate the confirmatory content. The
following classification is binding on how the results should be read.

**Table T3. Preregistration status by analysis.**

| Analysis | Status |
|---|---|
| Three calibration protocols; initial coverage hypothesis | Pilot-informed preregistration. Earlier exploratory results on NSL-KDD, UNSW-NB15 and CIC-IDS2017 motivated the hypothesis, as Amendment 1 records. |
| Focal-class rule, feasibility floor, partitioning | Prespecified before the corresponding coverage was computed, per environment. |
| Within-NSL dose-response (Section 5.3) | Prospectively specified, but **not** the original confirmatory test. Promoted to the principal within-dataset analysis after the preregistered pooled interaction proved unidentifiable; recorded in Amendment 3 and the deviation log. |
| CIC-IDS2017 within-day redesign | Amended after the NSL-KDD outcome was known, before any CIC coverage existed (Amendment 9). |
| CIC-IoT-2023 environment | Named in the base preregistration; constructed and gated before any CIC-IoT coverage existed (Amendments 10 and 11). |
| Placebo ladder (Section 5.4) | **Exploratory and outcome-informed.** The subtype pair was chosen after observing per-subtype coverage. |
| Class-conditional shift (Section 5.10) | Exploratory mechanistic refinement, added after the aggregate measure proved uninformative within environments. |
| Threshold-specific displacement (Section 5.11) | Exploratory refinement of the preregistered mechanism analysis. |
| Label-free monitor (Section 5.13) | Exploratory. Developed and evaluated on the same environments, with no external validation set; leave-one-environment-out validation is identified as necessary in Section 8. |
| Abstention analysis (Section 5.14) | Exploratory. |

The confirmatory content is therefore the protocol contrast itself and the per-class coverage
outcomes under the preregistered focal-class and feasibility rules. The mechanism, monitor,
placebo and class-conditional analyses are exploratory, and are marked as such in the text
rather than only here.

# 5. Results

## 5.1 The conformal implementation is validated before it is used

The negative control of Section 4.11 leaves every feasible class statistically consistent with nominal coverage. The band is a population bound under exchangeability, not a requirement that every finite empirical estimate fall inside it, so consistency rather than containment is the criterion.
For the four feasible NSL-KDD classes the observed coverages are 0.9503, 0.9503, 0.9517 and
0.9583 against bands whose lower edge is 0.95, and every seed-clustered bootstrap
interval overlaps its band (Table T4). Two point estimates sit marginally above the
upper edge, by 0.0001 for the majority class and 0.0006 for Probe, which is the expected
consequence of an isotonic calibrator producing tied probabilities and hence mild atoms
in the score distribution. That residual is the baseline conservatism of the pipeline. At 0.0006 it is comparable in size to the smallest deviations reported below, such as the 0.001 shortfall on one UGR'16 class, and two to three orders of magnitude smaller than the substantive failures. Coverage failures reported in this paper are therefore attributable to
distribution shift and not to the implementation.

**Table T4. Negative control: no shift by construction.** Source pool split at random,
calibrate on one half and evaluate on the other, over the full model panel.

| Class | n_cal | Coverage | 95% CI | Guarantee band | Inside |
|---|---|---|---|---|---|
| DoS | 3440 | 0.9503 | [0.9497, 0.9509] | [0.9500, 0.9503] | yes |
| Normal | 5053 | 0.9503 | [0.9495, 0.9509] | [0.9500, 0.9502] | yes |
| Probe | 876 | 0.9517 | [0.9500, 0.9531] | [0.9500, 0.9511] | yes |
| R2L | 75 | 0.9583 | [0.9533, 0.9633] | [0.9500, 0.9632] | yes |

## 5.2 Source-held-out calibration undercovers severely in selected classes and environments

Under shift the fixed source-calibrated baseline does not merely fall short of the nominal level
on the classes it affects; it falls below the lower edge of the band the exchangeability
guarantee would imply. The failure is selective, and the selection matters (Table T5):

- **NSL-KDD**: all four feasible classes undercover, from 0.023 below the band for the majority
  class to 0.864 for the focal class.
- **CIC-IDS2017**: DoS undercovers by 0.346; Benign retains 0.950.
- **UGR'16**: scan11 and scan44 undercover by 0.415 and 0.151; background, dos and nerisbotnet
  retain 0.949, 0.950 and 0.947.
- **CIC-IoT-2023**: no class undercovers.

**Table T5. Classes that undercover relative to the exchangeability-based band, α = 0.05.**
Shortfall is the distance below the band's lower edge. This table lists AFFECTED classes only;
classes retaining nominal coverage are named in the text and their omission here is not
evidence of universal failure. CIC-IoT-2023 has no affected class.

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

The two protocols that use target-drawn or evaluation-drawn calibration data, differing from
the baseline only in the data forming the quantile, sit inside their bands throughout, so the
failure is a property of calibration provenance rather than of conformal prediction. Table T5
therefore lists affected classes rather than demonstrating that every class is affected. What is universal, within an affected class, is that the shortfall is large relative
to any practical margin.

A point of terminology, since it recurs. The conformal guarantee is conditional on
exchangeability and these constructions deliberately break it, so nothing below shows a theorem
failing under its own hypotheses. What is shown is undercoverage relative to the level the
guarantee would deliver were exchangeability to hold, which is the level a practitioner relies
on. We use the band as a reference for that target and say "falls below the band" rather than
"violates the guarantee".

Two entries deserve separate treatment. The UGR'16 focal class and background class fall below
the band by 0.003 and 0.001, which the bootstrap resolves as statistically detectable, yet two
one-sided tests place both inside a one-percentage-point equivalence margin. They are therefore
practically equivalent to nominal while formally below the bound, a distinction that matters
when the same word would otherwise cover a shortfall of 0.001 and one of 0.864.

## 5.3 Primary analysis: a dose-response along the novelty ladder

The primary within-dataset test is the NSL-KDD ladder, which raises the fraction of focal
evaluation mass drawn from attack subtypes absent from the source while holding dataset,
model panel, partition and evaluation size fixed. Focal coverage falls monotonically from
0.143 at rung 0.00 to 0.030 at rung 0.80, with seed-clustered bootstrap intervals disjoint
between adjacent rungs at every step (Table T6). A mixed model on the empirical logit with a
random intercept per realisation gives a slope of -2.071 per unit of unseen fraction, standard
error 0.024.

**Table T6. Primary dose-response: NSL-KDD focal coverage under the source-calibrated baseline,
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
has 3. We construct a placebo ladder in which the focal evaluation mass is drawn only from
these two subtypes, varying their ratio across five rungs.

**This construction is exploratory and outcome-informed, and we label it as such.** The two
subtypes were chosen because they occupy the observed extremes of per-subtype coverage, so the
contrast is selected to be large and the ratio reported below is not an unbiased estimate of a
general effect. It is a demonstration of possibility, not a measurement of magnitude. A
confirmatory version would fix the pair using source-side information alone, or evaluate all
feasible pairs and report the distribution; neither is done here and both are identified in
Section 8. The support shift is zero
at every rung by construction and is verified rather than assumed. The non-focal portion of
each evaluation set uses identical row indices across rungs within a realisation, so nothing
but focal composition can move the result.

**Table T7. Placebo ladder: focal coverage with no support shift, α = 0.05.** Evaluation mass
drawn only from subtypes present in the source. Novelty ladder shown for comparison.

| Fraction `guess_passwd` | 0.00 | 0.25 | 0.50 | 0.75 | 1.00 | swing |
|---|---|---|---|---|---|---|
| Focal coverage | 0.3076 | 0.2331 | 0.1614 | 0.0814 | 0.0097 | **0.298** |
| S_sup | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | |
| Score movement (KS) | 0.801 | 0.836 | 0.873 | 0.914 | 0.972 | |
| *Novelty ladder coverage* | *0.143* | *0.114* | *0.085* | *0.058* | *0.030* | *0.113* |

The placebo ladder moves coverage by 0.298 against the novelty ladder's 0.113 (Table T7), a ratio of
2.63, while the binary support-shift measure stays at exactly zero. Given the outcome-informed
selection, the defensible claim is not that novelty has a quantified smaller effect but that
the binary seen/unseen indicator is inadequate: severe coverage movement can occur entirely
among nominally seen subtypes, so novelty is not necessary for the failure the ladder
produces. What moves coverage is where a subtype's scores sit relative to the source-calibrated
quantile, and introducing unseen subtypes is one way, but not the only way and not the most
effective way, of moving them.

Score movement tracks the placebo ladder monotonically, from 0.801 to 0.972, in a setting
where support shift is pinned at zero and cannot be the explanation. This is the one place in
the study where movement and novelty are separated experimentally rather than statistically,
and movement is what carries the effect.

![**Figure 2.** The placebo ladder. (a) Focal coverage against ladder position for the
novelty ladder, which introduces subtypes absent from the source, and for the placebo ladder,
which rearranges mass among subtypes the source has already seen and holds the support shift at
exactly zero. The placebo moves coverage 2.6 times further. (b) Within-subtype coverage range
across the novelty rungs for each subtype, against the class-level swing: every component is
close to invariant, so the class-level dose-response is a mixture average of fixed per-subtype
coverages.](figs/fig2_placebo.png)

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
seen subtypes. An aggregate domain-classifier AUROC of 0.849 establishes that source and target features are
distinguishable in aggregate. It does not establish covariate shift with an invariant
conditional law, it does not exclude the composition effect that Section 5.4 demonstrates
directly, and, as Section 5.10 shows, an aggregate statistic cannot characterise a
class-conditional quantity at all: the class-conditional values within NSL-KDD range from
0.789 to 0.991 while the aggregate assigns 0.893 to every class. We
withdraw the earlier attribution of 87.7 per cent of the gap to covariate shift.

This also exposes a limitation of `S_sup` as defined. A subtype with 11 calibration points
against 1,231 target instances is, for the purpose of forming a conformal quantile, effectively
unsupported, yet the binary in-source test counts it as seen. A measure of support adequacy
rather than support presence would capture what the current definition misses, and is
identified as necessary in Section 8.

## 5.6 Replication in two further environments

The failure replicates in two independent environments with different shift constructions and different focal classes. A fourth environment, treated separately in Section 5.7, does not replicate it, and that is informative rather than contradictory. On CIC-IDS2017, where support shift is induced by withholding
denial-of-service variants from calibration, focal coverage under the source-calibrated baseline
is 0.604 with an interval of [0.597, 0.611] against 0.988 for target-supervised
calibration. On UGR'16, where the shift is temporal feature drift at retained label support at fixed support, the
preregistered focal class holds at 0.947 while two other classes collapse. In every
environment the non-source-calibrated baselines retain coverage, so the failure is a property of
source-only calibration under shift and not of conformal prediction itself.

## 5.7 Subtype novelty is not sufficient to produce undercoverage

CIC-IoT-2023 supplies a case with large semantic subtype novelty: two of the six web-attack
subtypes are absent from the source entirely, and the ladder raises their share of focal
evaluation mass to 0.80. The aggregate covariate shift sits at the permutation null, but
Section 5.10 shows the focal class itself carries S_cov,Web = 0.654, so this is not an
environment with support shift alone and we do not describe it as one. If semantic novelty at
the subtype level were sufficient to break class-conditional coverage, this is where it would
show. We state the claim in those terms deliberately: the withheld subtypes are absent from the
source by label, but their feature distributions evidently remain inside the region the model
has already learned for the family, so this construction establishes the insufficiency of
*semantic* subtype novelty rather than of feature-space support loss. A construction in which
source support is genuinely absent in the model-relevant feature space might behave differently,
and we do not claim otherwise.

It does not. Focal coverage under the source-calibrated baseline is 0.949, 0.952, 0.951, 0.952
and 0.952 as the novel fraction rises from 0.00 to 0.80 against a nominal 0.95 (Table T8), with
a seed-clustered interval of [0.950, 0.954] at the top rung. All eight classes sit inside their
bands under all three protocols, none is infeasible, and mean prediction-set size differs by
0.014 between protocols. At a novel fraction nearly twice the largest reached on NSL-KDD,
nothing fails.

**Table T8. CIC-IoT-2023: focal coverage under the fixed source-calibrated baseline across the
novel-subtype ladder, α = 0.05.** Nominal 0.95. Aggregate S_cov is at the permutation null throughout, though the focal class carries S_cov,Web = 0.654 (Table T12).

| Novel fraction (S_sup) | 0.00 | 0.20 | 0.40 | 0.60 | 0.80 |
|---|---|---|---|---|---|
| SHC | 0.9491 | 0.9517 | 0.9509 | 0.9520 | 0.9519 |
| TSC | 0.9512 | 0.9532 | 0.9497 | 0.9497 | 0.9482 |
| REC | 0.9519 | 0.9519 | 0.9519 | 0.9519 | 0.9519 |

This is the mechanism's negative prediction, and testing it is the point. Section 5.11 holds
that a class undercovers when its score distribution moves past the source-calibrated quantile,
so it requires movement to be small here. It is: focal score movement at the top rung is 0.089,
and 0.108 restricted to the withheld subtypes, against 0.922 for the NSL-KDD focal class.

The reason is measurable rather than merely interpretable, and Section 5.11 supplies the
instrument. The withheld subtypes did move the score distribution, to 0.089, essentially the
same as UGR'16 nerisbotnet. What differs is *where*: only 12 per cent of that movement is
realised at the source-calibrated threshold, against 99 per cent for the NSL-KDD focal class and
96 per cent for UGR'16 scan11. The novelty is visible in the scores and irrelevant to coverage,
because coverage depends on the target distribution at one point and the movement happens
elsewhere. Support shift as counted by S_sup is therefore not the same thing as support shift
that moves scores past the threshold, which also explains why the NSL-KDD ladder of Section 5.3
yields a dose-response while the same manipulation here yields none.

One feature deserves separate comment because it shows what the trust layer contributes. The
classifier misroutes 53 per cent of true focal flows at every rung, yet class-conditional
coverage holds at 0.95. That is possible only because the prediction sets are set-valued: at a
mean size of 1.79 the true class survives even when the top-ranked prediction is wrong. A point
classifier on the same traffic would be wrong more often than not on this class.

## 5.8 A satisfied marginal guarantee conceals per-class failure

Under the two valid protocols on NSL-KDD the marginal guarantee is satisfied almost
exactly, at 0.9507 aggregate coverage against a nominal 0.95, yet under that single shared
quantile the rare focal class receives only 0.859, while class-conditional conditioning
delivers 0.956 to the same class on the same data (Table T9). A practitioner monitoring
the marginal guarantee alone would observe a system performing to specification while the
class that matters most was undercovered by nine percentage points. Under the deployable
protocol both collapse, to 0.720 aggregate and 0.071 focal. This result motivates the
class-conditional framing of the study and shows that aggregate coverage reporting is not
sufficient to certify a conformal detector.

**Table T9. Marginal versus class-conditional conditioning, NSL-KDD, α = 0.05.**

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

## 5.10 The selectivity is explained by class-conditional shift

Section 5.9 shows that classes under one aggregate shift do not share a common coverage, and
that which fail cannot be read from the aggregate. That invites the question of whether the
measure is wrong or shift is simply not what determines the outcome.

It is the measure. An aggregate domain-classifier statistic is computed over all classes pooled,
so it takes one value per environment and is constant within it, with zero within-environment
variance. It cannot order classes inside an environment even in principle. We replace it with
S_cov,c (Table T10), the cross-fitted area under the ROC curve of a domain classifier separating
source and target instances *of that class alone*, against a permutation reference from
splitting the pooled per-class data at random.

**Table T10. Class-conditional covariate shift against realised coverage.** The aggregate column
is the single value previously reported for every class in that environment. Permutation
reference is 0.49 to 0.50 throughout.

| Environment | Class | S_cov,c | Aggregate | Coverage |
|---|---|---|---|---|
| CIC-IDS2017 | DoS | 0.9997 | 0.7679 | 0.604 |
| CIC-IDS2017 | Benign | 0.4992 | 0.7679 | 0.950 |
| UGR'16 | scan11 | 0.9997 | 0.7129 | 0.535 |
| UGR'16 | scan44 | 0.9861 | 0.7129 | 0.799 |
| UGR'16 | background | 0.6696 | 0.7129 | 0.949 |
| UGR'16 | nerisbotnet | 0.5782 | 0.7129 | 0.947 |
| UGR'16 | dos | 0.5424 | 0.7129 | 0.950 |
| NSL-KDD | R2L | 0.9905 | 0.8934 | 0.030 |
| NSL-KDD | Probe | 0.9794 | 0.8934 | 0.628 |
| NSL-KDD | DoS | 0.9595 | 0.8934 | 0.399 |
| NSL-KDD | Normal | 0.7886 | 0.8934 | 0.927 |
| CIC-IoT-2023 | Web | 0.6536 | 0.5123 | 0.952 |
| CIC-IoT-2023 | seven others | 0.492-0.510 | 0.5123 | 0.950-0.956 |

CIC-IDS2017 is the sharpest case. Its two classes carry 0.9997 and 0.4992, essentially perfect
separability and none at all, the latter within 0.002 of its permutation reference. The
aggregate of 0.768 is their average and describes neither. The class that fails is the class
that is shifted, and the previous measure assigned both the same number.

Within environments where coverage varies the class-conditional measure orders it: Spearman
0.900 on UGR'16, 0.800 on NSL-KDD, and on CIC-IDS2017 the failing class carries the higher
value, the only comparison two classes admit. Pooling within-environment ranks across those
environments gives 0.862 (p = 0.003, n = 9). On CIC-IoT-2023 the correlation is −0.214 and not
distinguishable from noise, which is correct behaviour for a predictor of failure where every
class lies within 0.006 of nominal.

The aggregate cannot be compared against this on pooled data: it takes three distinct values
across the study, one per environment, which happen to rank the environments by severity, so a
pooled correlation credits it with between-environment information it does not carry within any.
This is the identification failure that defeats the pooled model of Section 5.15, and we do not
report such a comparison.

The consequence strengthens rather than repairs the argument. The claim is not that shift is
hard to measure but that the relevant shift is class-conditional, so an aggregate statistic is
the wrong instrument for a class-conditional guarantee. NSL-KDD's ordering is imperfect, with
DoS carrying less class-conditional shift than Probe yet undercovering more; we report this
rather than smooth it, and it is consistent with Section 5.11, where threshold-level movement
rather than feature distinguishability determines coverage directly.

## 5.11 Score movement explains the failures

Because the three architectures fitted to a dataset and class share data and shift, they are not
independent observations, so the relationship between score movement and undercoverage is
estimated at the class level, one ladder rung per laddered dataset. Across twenty-eight
class-level cells the Kolmogorov-Smirnov distance between source and target true-class score
distributions is rank-correlated with realised undercoverage at Spearman 0.844
(p = 1.7 × 10⁻⁸, bootstrap interval [0.610, 0.939], Figure 3), spanning movement from 0.000 to
0.922 and undercoverage from −0.050 to +0.876.

This is lower than the 0.926 over the first three datasets because the fourth is a harder test:
it occupies the low-movement, no-failure corner and forces the relationship across a range the
others never reached. Removing each dataset in turn gives 0.926 without CIC-IoT-2023, 0.873
without UGR'16, 0.785 without NSL-KDD and 0.538 without CIC-IDS2017, so the statistic never
depends on one source and leans least on the environment added last. Within-dataset values are
0.900 on NSL-KDD, 0.841 on CIC-IDS2017 and 1.000 on UGR'16. On CIC-IoT-2023 it is −0.667, which
is range restriction rather than counter-evidence: every class there lies within 0.006 of
nominal, so there is no failure for movement to predict, and a permutation test puts the
observed value at p = 0.079.

A class undercovers when target score mass crosses above the source-calibrated threshold. The
two-sided movement statistic tracks that closely enough to order outcomes, but it is a proxy and
its relationship to coverage is not constant. Coverage is the target distribution function
evaluated at the source threshold, so the deficit decomposes exactly as the signed displacement
at that threshold plus a finite-sample slack bounded by 1/(n + 1), an identity we verified
numerically to 1.1 × 10⁻¹⁶. The diagnostic is then the fraction of movement realised at the
threshold, ranging from 0.05 to 0.99 across the study. Where a class fails that fraction is near
one: 0.99 for the NSL-KDD focal class, 0.96 and 0.87 for the UGR'16 scan classes. Where a class
holds, movement occurs away from the threshold: 0.05 for UGR'16 nerisbotnet, 0.12 to 0.28 for
CIC-IoT-2023. Two distributions can share a movement statistic while one shifts mass below the
threshold and the other above; the signed displacement separates them and the two-sided
statistic cannot.

One consequence constrains what the proxy may be used for. Where nearly all movement is realised
at the threshold, the statistic and the coverage deficit become close to the same quantity: on
the NSL-KDD focal subtypes the correlation between the measured statistic and (1 − α) minus
coverage is 0.997. A within-environment correlation between movement and undercoverage there is
therefore largely definitional and is not reported as evidence. The cross-dataset correlation
retains its meaning precisely because the realised fraction varies so widely between
environments.

This unifies the preceding sections: it is movement of the score distribution *at the
threshold*, whatever its cause, that breaks the guarantee, which is why feature drift of
sufficient magnitude suffices, why failure under a common shift is class-selective, and why
subtype novelty that leaves scores in place breaks nothing at all.

![**Figure 3.** True-class nonconformity-score movement (KS distance, source vs target) versus realised undercoverage. Because architectures fitted to the same dataset and class are not independent, the reported statistic is estimated at the class level, one ladder rung per laddered dataset, where Spearman is 0.844 (n = 28 across four datasets, 95% CI [0.610, 0.939]). The NSL-KDD focal class R2L, with the largest movement, shows the largest undercoverage; CIC-IoT-2023 occupies the low-movement, no-failure corner.](figs/fig3_mechanism.png)

## 5.12 Robustness

*Prior shift.* Class-conditional coverage is invariant to reweighting the target to the source
prior by construction, verified numerically on CIC-IDS2017 and UGR'16 where focal coverage
changes by 0.0000. On CIC-IDS2017, whose aggregate coverage of 0.936 conceals the focal failure
behind a benign majority, reweighting lowers the aggregate to 0.770 and exposes it.

*Analytical choices and miscoverage level.* The focal failure appears in all sixteen
specifications of Section 4.11, formed by two nonconformity scores, two conditioning variants
and four levels, with shortfalls from 0.370 to 0.987. Outcomes are likewise stable in alpha
(Figure 4): focal coverage under the source-calibrated baseline is 0.030, 0.023 and 0.017 on
NSL-KDD at alpha 0.05, 0.10 and 0.20, and 0.604, 0.556 and 0.479 on CIC-IDS2017, while UGR'16 nerisbotnet holds at 0.947,
0.895 and 0.790 and CIC-IoT-2023 Web at 0.952, 0.908 and 0.817, and the UGR'16 scan classes fall
short at every level. Neither the failures nor the nulls depend on these choices.

*Architecture.* All three architectures fail, with pooled focal coverage of 0.111 for the
multilayer perceptron, 0.082 for the gradient-boosted ensemble and 0.064 for the random forest
against a nominal 0.95. The perceptron and random-forest intervals do not overlap, so severity
depends on the classifier by a factor of about 1.7 while the ladder slope is unchanged. The
qualitative conclusion is architecture independent; its magnitude is not, so changing the model
does not repair the trust layer.

*Efficiency and calibration.* Narrower prediction sets under the source-calibrated baseline are
a symptom of failure rather than efficiency: wherever it undercovers, its sets are both smaller
and miss coverage, 2.04 against 4.68 on NSL-KDD at coverage 0.030 against 0.953 (Figure 5).
Class-averaged expected calibration error is at or below 0.002 on all four datasets, including
0.0006 mean and 0.0015 maximum on CIC-IoT-2023 (Figure 6), so the failures are not a
base-miscalibration artefact.

*Calibration-set size.* Per-class calibration sets differ in size across protocols for a
structural reason: on NSL-KDD the source-calibrated baseline calibrates the focal class on 149
points against 297 for target-supervised, because R2L is rare at source and common at target.
Under exchangeability a smaller set biases towards over-coverage, since the band is bounded
above by 1/(n + 1), but that argument does not survive the loss of exchangeability. Rather than
assume a direction we removed the confound, subsampling both calibration sets to identical
per-class counts, n_match = min(n_SHC, n_TSC), with the evaluation set, classifier, calibrator
and realised scores unchanged.

The contrast is unaffected (Table T11). The NSL-KDD focal gap is 0.9237 at natural budgets and
0.9240 when both protocols calibrate on 149 points, retaining 100 per cent of the effect with a
seed-clustered interval of [0.9217, 0.9265]; UGR'16 retains 96.6 per cent and CIC-IoT-2023 79.3
per cent of a gap negligible in both conditions. The protocol difference is therefore an effect
of calibration-data provenance, not of sample size. That this needed testing is shown by the
size effect itself: two calibration sets of 297 and 149 points drawn from the *same*
distribution produce a spurious difference of about 0.011, real but two orders of magnitude
below the measured effect.

**Table T11. Class-budget-matched protocol contrast, focal class, α = 0.05.**

| Environment | Budget | TSC | SHC | Gap | n_cal (TSC / SHC) |
|---|---|---|---|---|---|
| NSL-KDD | natural | 0.9527 | 0.0290 | 0.9237 | 297 / 149 |
| NSL-KDD | **matched** | 0.9530 | 0.0290 | **0.9240** | 149 / 149 |
| UGR'16 | natural | 0.9495 | 0.9471 | 0.0024 | 7505 / 7500 |
| UGR'16 | **matched** | 0.9495 | 0.9472 | **0.0023** | 7471 / 7471 |
| CIC-IoT-2023 | natural | 0.9496 | 0.9515 | −0.0019 | 3665 / 2135 |
| CIC-IoT-2023 | **matched** | 0.9500 | 0.9515 | **−0.0015** | 2135 / 2135 |

CIC-IDS2017 is excluded because its source and target pools are realisation-specific and the
matched draw would need rebuilding per realisation; its natural-budget focal gap of 0.384 is
the one protocol contrast in the study that remains unmatched.

*Implementation.* An earlier quantile form used in intermediate analyses returned one order
statistic above the definition of Section 4.11, inflating coverage by approximately 1/n and
therefore conservative with respect to every undercoverage finding. Recomputation puts the
difference on reported focal coverages at 0.00005 and 0.00015, below the reporting precision.

![**Figure 4.** Alpha-sensitivity across all four environments. Focal SHC coverage versus the nominal level (1 - alpha) at alpha in {0.05, 0.10, 0.20}. NSL-KDD R2L and CIC-IDS2017 DoS undercover at every level; UGR'16 nerisbotnet and CIC-IoT-2023 Web track nominal at every level; the UGR'16 scan classes collapse at every level. Neither the failures nor the nulls depend on the choice of alpha.](figs/fig4_alpha.png)

![**Figure 5.** Efficiency across all four environments. Focal coverage versus focal prediction-set size for each protocol and dataset. Wherever SHC undercovers, its sets are smaller and miss coverage; TSC and REC pay a larger set width. On CIC-IoT-2023, where coverage holds, the three protocols sit together.](figs/fig5_efficiency.png)

![**Figure 6.** Calibration quality of the isotonic-calibrated probabilities on the held-out source calibration pool, for all four environments. (a) Per-class expected calibration error and (b) per-class Brier score, by dataset. On CIC-IoT-2023, where coverage holds, this also forecloses the converse objection that the null is an artefact of unusually good or poor calibration. All per-class ECE values fall at or below 0.002 (dashed line), confirming that the probabilities feeding the conformal layer are well calibrated in distribution.](figs/fig6_calibration.png)

## 5.13 Label-free monitoring, its per-dataset behaviour, and its boundary

Pooled across the fifty-seven feasible class cells it is rank-correlated with realised
undercoverage at 0.738 and separates undercovering classes with an area under the ROC curve
of 0.930, with a bootstrap interval of [0.851, 0.990], against an oracle using true labels
at 0.925 and 0.96; its performance is stable to the threshold defining an undercovering
class (Figure 7).

The monitor is evaluated on the three environments in which coverage actually fails; on CIC-IoT-2023 there is no failure to predict, so it does not apply there. Across those three, performance is consistent rather than carried by any one of them (Table T12): 0.926 on NSL-KDD, 0.955 on CIC-IDS2017 and 0.981 on UGR'16, with every
interval excluding chance. The intervals are nonetheless wide, since each environment
contributes between twelve and thirty class cells, so the per-environment estimates should
be read as consistent in direction rather than precisely resolved.

**Table T12. Label-free monitor by dataset.**

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

![**Figure 7.** The label-free coverage-failure monitor. (a) The monitor signal (predicted-class score drift, requiring no target labels) versus realised undercoverage across the 57 feasible class cells (Spearman 0.738, AUROC 0.930). (b) Label-free drift versus oracle (true-label) drift: points far below the diagonal are the similarity-type blind spot, where a novel class is confidently misrouted so the predicted-class distribution barely moves.](figs/fig7_monitor.png)

## 5.14 Abstention does not repair the failure, and the reason is instructive

The monitor identifies which classes will undercover, raising the question of what to do next.
The natural answer is triage: abstain on the least trustworthy alerts and retain the guarantee
on the remainder. We evaluate a policy that never consults a label. For each alert we compute
the margin

m(x) = max over classes c of ( q_c - s(x, c) ),

where q_c is the source-calibrated threshold and s(x, c) the nonconformity score, escalating in
ascending margin so the most atypical alerts reach the analyst first. A negative margin means
an empty prediction set and a certain miss. Classes with an infinite threshold under the
feasibility rule are excluded from the maximisation; scores share a common scale and are not
renormalised; ties break on class index; and the retained-coverage denominator is the count of
retained alerts whose true class is the focal class.

The policy substantially improves the marginal guarantee, raising aggregate coverage from 0.936
to 0.985 on CIC-IDS2017 and 0.879 to 0.916 on UGR'16 when a tenth of alerts are escalated. It does almost nothing for the class-conditional guarantee where that guarantee has failed
(Figure 8), and on the worst-affected classes it does something more troubling than nothing.
The diagnostic evidence is stark: on NSL-KDD the empty-set fraction is exactly zero, so every
flow receives a non-empty prediction set that simply does not contain its true class. The
alerts that break class-conditional coverage are not atypical flows near the edge of every
quantile but flows the shifted detector confidently assigns to the wrong class, which
therefore carry a large margin and are escalated last.

Evaluated on the UGR'16 classes that actually fail rather than on focal classes that largely
held, scan11 moves from 0.535 to 0.598 and scan44 from 0.799 to 0.853 when half of all alerts
are escalated, neither reaching nominal. Meanwhile classes already sound are pushed into
over-coverage, dos to 1.000 and background to 0.996, and the disparity between worst and best
served barely moves, from 0.415 to 0.402, for half the analyst budget.

The reason is that the policy is anti-correlated with need. Uniform escalation would retain
exactly one minus the escalated fraction of every class. Instead the failing classes are
retained *above* uniform at every budget, scan11 by 0.028 to 0.053 and scan44 by 0.021 to
0.044, while sound classes are retained below it, dos by -0.020 to -0.033: a mean deviation of
+0.039 against -0.009. A queue ordered by typicality reaches confident misroutes last, because a confident misroute is
by construction atypical of nothing. This is the same identifiability limit that produces the
diagnostic's similarity-type blind spot in Section 5.13, so the two results share one cause
rather than being adjacent observations. The practical consequence is that an operator can buy
back the marginal guarantee cheaply and can use the diagnostic to learn which classes are
affected, but restoring the per-class guarantee requires information the target does not
supply, which returns the argument to the lever identified in Section 6: obtaining even a small
labelled sample of target traffic.

Two limits on this result. It tests one policy, so it establishes that margin-ordered
abstention fails rather than that no label-free triage can succeed; entropy, ensemble
disagreement, density and hybrid policies are untested. And coverage on a model-dependent
retained subset is not a recovered conformal guarantee, so we report empirical retained-set
coverage rather than claiming the guarantee is restored.

![**Figure 8.** Label-free selective prediction on UGR'16, showing the classes that actually fail rather than focal classes that largely held. (a) Coverage among retained alerts against the fraction escalated to an analyst; the policy orders by margin and never consults a label. (b) The fraction of each class still retained. The failing classes scan11 and scan44 are retained above the uniform rate at every budget while the sound classes are retained below it, so the policy escalates the alerts that least need review.](figs/fig8_selective.png)

## 5.15 Secondary analysis: pooled cross-dataset model

For completeness we fit the preregistered pooled model over all 49,500 coverage cells, with
the caveat that it cannot support inference at this design. The interaction between the
source-calibrated baseline and support shift is negative under every specification, at −0.374, and
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

**The source-calibrated baseline does not deliver its promise where it matters most.** Adopting
conformal prediction as a trust layer, calibrated the simplest way an operator can, does not
deliver the advertised class-conditional coverage under realistic shift, and the failure
concentrates on the classes an operator most needs to trust: rare attack classes and novel
variants. On the two support-shift datasets the focal class is covered at 0.030 and 0.604
against a nominal 0.95, so a set-valued detector under this protocol would silently omit the
true class from a large fraction of its predictions on exactly the traffic that motivates the
system. Because target-supervised and recalibrated protocols retain nominal coverage, and
because that contrast survives matching per-class calibration sizes, the failure is a property
of calibration-data provenance rather than of conformal prediction or of sample size. A
negative control on exchangeable data places every class inside its band, so it is attributable
to shift and not to implementation. Nor is it repairable by triage: a label-free abstention
policy recovers the marginal guarantee cheaply but leaves the per-class guarantee essentially
untouched (Section 5.14), because the alerts that break it are confident misroutes rather than
atypical flows. And since all three architectures fail, though by margins differing by about a
factor of 1.7, changing the classifier does not repair the trust layer. This reframes the
practitioner's question from "should I use conformal prediction" to "can I obtain even a small
labelled sample of target traffic", since where such a sample exists the target-supervised
protocol restores coverage.

**What this study does and does not add.** That conformal prediction can lose coverage when
exchangeability fails is known theory and we do not claim it. What the theory does not say is
which classes lose coverage in a deployed detector, by how much, or whether the loss is
attributable to calibration-data provenance rather than to the smaller calibration sets that
source-only calibration yields for rare classes. Those are measurements, they require the
constructions and controls assembled here, and they are what a practitioner deciding whether to
adopt a conformal trust layer needs.

**Neither the category nor the nominal magnitude of shift predicts the failure.** A placebo
ladder built only from subtypes the source has already seen moves focal coverage by 0.298 with
support shift held at zero, against 0.113 for the novelty ladder itself. A fourth environment
closes the argument from the other side: semantic subtype novelty swept to 0.80 of focal
evaluation mass produces no failure at all. The same nominal support shift destroys coverage on
one dataset and leaves it untouched on another, and the same holds for feature drift across
classes within a dataset. What the failing classes share is not a category or a magnitude but
movement of their score distributions past the threshold.

**Aggregate drift monitoring is therefore insufficient, and this is now measured rather than
asserted.** An aggregate shift statistic is constant within an environment, so it cannot order
the classes inside it; the class-conditional version orders them at Spearman 0.86 where
coverage varies. CIC-IDS2017 makes the point without ambiguity: its two classes carry 1.000 and
0.499, the latter indistinguishable from a permutation null, while the aggregate reports 0.768
for both. An operator watching the aggregate sees one moderate number describing a class that
is entirely shifted and another that has not moved. A dashboard reporting an aggregate drift
score cannot certify a conformal detector, because the same aggregate can leave one class safe
and break another. Trust must be assessed per class.

**Why the failures happen, and what a label-free diagnostic can and cannot see.** A class
undercovers when its nonconformity-score distribution crosses the source-calibrated threshold.
This is intuitive in hindsight, since the source quantile is fixed while target scores drift out
from under it, but it is not trivial: it holds across classes, architectures and shift types,
and it explains the selective result no aggregate measure could. It is also constructive,
because a label-free signal detecting such movement predicts failure, which our exploratory
diagnostic does at pooled AUROC 0.93 across the three environments where coverage fails. Its
boundary is a genuine identifiability limit rather than an engineering shortfall: when a shifted
detector confidently misroutes a novel class into a familiar one, the novel traffic never enters
the predicted-class distribution being watched, so no predicted-class signal moves and the
failure is invisible to any label-free monitor of that form. Distinguishing displacement-type
drift, where it succeeds, from similarity-type drift, where it is blind, is the fundamental
question such a signal must confront.

**Relation to validity-restoring methods.** The distinction also clarifies when restoration
would help. Weighted conformal prediction can in principle restore coverage under covariate
shift, but it requires estimating a source-to-target likelihood ratio, an estimation undermined
by support shift and by confident misrouting of novel classes, exactly the regime where our
diagnostic is blind. The hardest cases for coverage restoration coincide with the hardest cases
for label-free failure detection.

# 7. Limitations

First, the boundary between the regime in which the diagnostic succeeds and the regime in which
it is blind is demonstrated but not formally characterised (Section 5.13), so the misroute rate
should be read as a first, insufficient proxy rather than an established predictor. Second, the
preregistered pooled cross-dataset model cannot support inference at this design, for the
reasons in Section 5.15, and no better-specified fit would repair it; the causal claim rests on
the within-dataset dose-response and its replications. Third, the diagnostic is evaluated only
on the three environments where coverage fails, since CIC-IoT-2023 provides nothing to predict,
and each contributes only twelve to thirty class cells, so per-environment intervals are wide.
Fourth, it is diagnostic and does not correct. Fifth, the mechanism and diagnostic analyses use
a deterministic mid-point randomisation of the score for reproducibility, consistent with but
not identical to the randomised score that defines coverage of record. Sixth, per-class
calibration sets are unequal in size across protocols under natural budgets (Section 5.12);
matching removes the confound on three environments but CIC-IDS2017 remains unmatched. Seventh,
the source partition is drawn once and shared across seeds, so intervals capture model and draw
variability but not partition variability and are correspondingly optimistic. Eighth, failure
severity depends on the classifier, with pooled focal coverage differing by about a factor of
1.7 across architectures, so the magnitudes here are not architecture-free constants. Ninth, the
calibration evidence covers the calibrated probabilities only; raw pre-calibration probabilities
were not cached, so a before-and-after comparison would require retraining.

Finally, three of the four datasets are established benchmarks rather than contemporary
captures. CIC-IoT-2023, collected from 105 devices and released in 2023, addresses that
directly, and the mechanism transfers to it unchanged. For the older three the objection
deserves a direct answer rather than a concession. What is under test is a property of a
calibration protocol, not detection performance on current traffic: the question is whether a
quantile fitted on labelled source data remains valid on shifted, unlabelled target data. An
environment must supply a fitted classifier's score distribution, a shift that can be
constructed and measured, and enough per-class data to calibrate, none of which depends on the
capture year. The mechanism is stated in terms of scores rather than packets and holds across
three architectures and four shift constructions. For a diagnostic study, well-characterised
benchmarks are an advantage rather than a compromise, since their labelling errors are
documented and corrected and the shift constructions can be verified independently.

What does not transfer automatically is magnitude. Encrypted traffic, different class balance
and different attack families may produce different gap sizes and a different pattern of which
classes fail, so the values here are evidence that the failure occurs and why, not calibrated
expectations for a modern deployment. Within that scope the datasets impose their own caveats:
NSL-KDD is dated, CIC-IDS2017's attacks are synthetic and its base classifier near-perfect on
the chosen day, and UGR'16 required subsampling and the dropping of a non-comparable protocol
field, so its environment represents temporal drift in one provider's traffic rather than
intrusion traffic in general.

# 8. Future work

Several analyses would strengthen the claims further. A continuous measure of support adequacy,
replacing the binary in-source test that counts a subtype with eleven calibration points against
1,231 target instances as supported, would capture what Section 5.5 shows the present definition
misses, and would reconcile the S_sup column of Table T1 onto a common definition. The
class-budget-matched contrast of Section 5.12 covers three environments; extending it to
CIC-IDS2017 requires rebuilding the matched draw per realisation and would close the one
remaining unmatched protocol comparison. The placebo construction of Section 5.4 is
outcome-informed; a confirmatory version fixing the subtype pair from source-side information
alone, or evaluating all feasible pairs and reporting the distribution, would convert a
demonstration of possibility into a measurement of magnitude.

The most immediate extension is to validate the label-free diagnostic properly. It is currently
developed and evaluated on the same environments, so leave-one-environment-out validation is
needed, with CIC-IoT-2023 included as an all-negative environment measuring specificity and
false-alarm burden rather than excluded for lacking positives, and with comparison against
simpler baselines such as predicted-score movement alone, share collapse alone, confidence or
entropy shift, and existing conformal drift monitors. Completing the characterisation of its
boundary calls for a continuous, model-internal measure of class confusability to replace the
misroute proxy, and for environments rich in similarity-type drift.

A constructive direction is to convert the diagnostic into a remedy by widening prediction sets
on the classes it flags, testing whether that restores coverage on displacement-type drift while
conceding it cannot on similarity-type drift. Section 5.14 sharpens this: because alert-level
triage cannot reach confident misroutes, a remedy must act on the calibration rather than the
alert stream. Finally, replication on contemporary traffic beyond CIC-IoT-2023 would test
whether the mechanism, being expressed in score movement rather than packet content, transfers
as expected.

# 9. Conclusion

We asked, under preregistration, whether the fixed source-calibrated conformal
protocol for network intrusion detection retains its class-conditional coverage guarantee
under distribution shift, and if not, whether its failures can be detected without target
labels. The answer to the first question is that it does not. Against a negative control
that places every class inside its guarantee band on exchangeable data, source-held-out calibration under shift falls below that band on all four feasible NSL-KDD classes, on CIC-IDS2017 DoS and on two UGR'16 scan classes, by as much as 0.86, while several other classes and an entire fourth environment retain practically nominal coverage. A placebo ladder with no support shift moves coverage more than twice as far as the novelty ladder does, and a fourth environment with large semantic subtype novelty on modern IoT traffic produces no failure at all.
Under retained-label-support temporal feature drift the failure is selective, invisible to aggregate shift
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
