# Source-Calibrated Conformal Intrusion Detection Loses Class-Conditional Coverage under Distribution Shift: A Preregistered Diagnosis

## Abstract

Conformal prediction offers distribution-free coverage guarantees and is increasingly proposed as
a trust layer for network intrusion detection. Its guarantee assumes exchangeability, which
deployment breaks: a detector is calibrated on past traffic and applied to future traffic, and
the labels needed to recalibrate are what an operator lacks. Under preregistration we ask where the
fixed source-calibrated baseline loses class-conditional coverage, and why. Across four
datasets it undercovers severely on all four feasible NSL-KDD classes, on CIC-IDS2017 denial of
service and on two UGR'16 scan classes, by up to 0.86, while other classes and a fourth
environment hold nominal coverage. The contrast against target-supervised calibration survives
matching per-class calibration sizes, so it reflects calibration-data provenance rather than
sample size. Failure is selective, and no environment-level shift statistic can express that
selectivity, being constant within an environment. Neither the category nor the magnitude of
shift predicts which classes fail: a placebo construction shows that rearranging evaluation mass
among subtypes the source has already seen moves coverage further than introducing unseen ones,
and an environment sweeping subtype novelty to 0.80 of focal mass produces no failure at all.
What the failing classes share is movement of their nonconformity scores past the calibrated
threshold, which orders undercoverage across twenty-eight class cells at rank correlation 0.84.
A label-free diagnostic anticipates failure at pooled AUROC 0.93 with a demonstrated blind spot,
and abstention proves anti-correlated with need. All data, code and the preregistration are released.

**Keywords:** conformal prediction; network intrusion detection; distribution shift;
uncertainty calibration; coverage guarantees; drift detection.

# 1. Introduction

Machine-learning classifiers are routine in network intrusion detection, yet most emit point
predictions with no calibrated statement of how far they can be trusted. An operator facing an
alert needs to know whether the output is reliable for this flow, so scarce analyst attention
goes where it is warranted. Conformal prediction answers this: it wraps any classifier in a
procedure returning prediction sets with a distribution-free, finite-sample guarantee, so that
at miscoverage level alpha the set contains the true label with probability at least 1 − alpha
[1, 27, 31]. Applied per class in
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
sense, for example when the source-to-target density ratio is estimable [30], or when calibration adapts online against labelled feedback [11].
Intrusion detection sits outside those assumptions: its shift includes the arrival of novel
attack subtypes, a change in the support of the distribution rather than a reweighting of a
fixed one, and its operators have no stream of target labels. The practitioner's questions are therefore not only whether validity can be restored but, more
basically, when and why the source-calibrated baseline fails, whether that failure is visible in
aggregate drift statistics, and whether it can be flagged per class without labels.

We take a diagnostic and preregistered stance. Rather than propose a method and report that it
wins, we fix in advance the datasets, shift constructions, focal classes, protocols, shift
measures and primary test, then ask what the baseline does. Preregistration is what makes a
negative or boundary result credible: because the focal classes and analysis plan were committed
before any coverage number existed, the failures cannot be an artefact of choosing conditions
that produce them, and the one class surviving feature drift is the class named in advance. This
follows the spirit of temporally and spatially honest evaluation in security machine learning
[21].

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
presented as worth testing rather than validated. (vi) A deployment-time proxy for the class-conditional shift statistic, weighting each target
flow by its predicted class probability rather than selecting on true labels, which separates the
classes that lose coverage from those that retain it across seventeen classes with no overlap,
together with an explicit account of its upward bias where the model misroutes. (vii) An open
release of all pipelines,
calibrated models, coverage tables, figures and the preregistration, with deterministic seeds
and partition fingerprints. Fig. 1 gives an overview of the study design.

![**Fig. 1** Overview of the study. The labelled source is partitioned to train the classifier f, tune it, fit the isotonic calibrator g, and form the source calibration pool. The three conformal calibration protocols differ only in the data that forms the class-conditional quantile: REC on the evaluation set itself (same-sample reuse, an upper bound by construction), TSC on a labelled target sample (not deployable), and SHC on the source pool (the fixed source-calibrated baseline). Under distribution shift between source and target, SHC undercovers on the focal class while TSC and REC hold. The label-free monitor compares the predicted-class score distribution on target versus source, requiring no target labels, and flags the classes whose coverage will fail; it catches displacement-type drift but is blind to similarity-type drift, where a novel class is confidently misrouted](figure1_overview.png)

# 2. Related work

**Conformal prediction.** Conformal prediction produces set-valued predictions with
distribution-free, finite-sample coverage under exchangeability [27, 31], and recent expositions have made it broadly accessible [1]. For classification, the adaptive prediction set score yields sets whose size adapts to
instance difficulty and improves conditional coverage [25], and Mondrian
conditioning provides per-class guarantees [26, 31], which
matter here because a marginal guarantee can be satisfied while a rare attack class is badly
undercovered. We take that combination as our instrument and ask what happens to the per-class
guarantee when exchangeability fails.

**Conformal prediction under distribution shift.** Four lines of work address shift directly.
Weighted conformal prediction restores validity under covariate shift when the source-to-target
likelihood ratio is estimable [30]. Adaptive conformal inference maintains
coverage online against labelled feedback [11]. Recent analysis
characterises conformal behaviour beyond exchangeability in general [2]. And
the weighted argument has been extended to generalized covariate shift with posterior drift,
where the conditional law is also allowed to move [23]. These assume either an estimable density ratio over fixed
support or a stream of target labels. Intrusion detection violates both: novel attack subtypes
change the support, and deployment provides no target labels.

**Label-free and source-free conformal adaptation.** A newer line adapts conformal prediction
using unlabelled target data alone. Entropy-based conformal prediction and its test-time-adapted
variant rescale the nonconformity score by an entropy quantile computed on unlabelled target
inputs, recovering marginal coverage under corruption shift [14]. Source-free
conformal prediction estimates target thresholds from pseudo-labels and requires no true target
labels. In intrusion detection specifically, label-free class-aware conformal signals have been
proposed for streaming drift monitoring [3]. These methods and ours address
different questions: they adjust thresholds to restore coverage, mostly marginal, while we ask
where and why the fixed baseline loses the class-conditional guarantee. They are complementary
rather than competing, and a study evaluating them against a class-conditional criterion on
network traffic would be a useful successor to this one.

Our contribution is prior to method design: we diagnose when and why the source-calibrated
baseline fails, and show that whether a restoration method could help is itself governed by
where the score movement falls relative to the calibrated threshold.

**Drift and unreliability detection.** A separate literature detects distribution or risk shift
after deployment. Online exchangeability testing via test martingales flags violations of the
assumption [32], and risk-tracking methods detect harmful shifts in a deployed
model's error [22]. These operate at the level of the overall distribution or risk, and several rely on labelled
feedback. The general observation that model reliability can be tracked under shift is
therefore partly anticipated by this literature, and we differ in three respects that we state
plainly so as not to overclaim. Our diagnostic is tied specifically to conformal
class-conditional coverage failure rather than to distribution change in general; it is per
class and fully label-free, using only predicted-class score distributions; and we report its
blind spot rather than only its successes.

**Intrusion detection benchmarks and evaluation practice.** Learned detectors are commonly
benchmarked on NSL-KDD [29], CIC-IDS2017 [28] and
UGR'16 [18], and a critical literature has documented labelling and
construction errors in these corpora that change the conclusions drawn from them [10, 16]. Separately, temporally and spatially honest evaluation has been
shown to alter conclusions substantially in malware classification [21].
We inherit that critical posture: we adopt corrected labels where available, audit feature
separability to rule out trivial leakage, and construct shift explicitly rather than assuming
it. We extend it by preregistering the analysis plan so that a negative or boundary result
cannot be an artefact of post hoc choices.

# 3. Datasets and preparation

We evaluate the trust layer on four intrusion detection datasets, each isolating a different
form of shift between calibration and deployment data (Table 1). All raw sources, cleaned
artefacts, partition indices and derived tables are version controlled, and every partition
carries a SHA-256 fingerprint so it can be verified without access to the underlying data.
Per-class composition tables are released with the code.

**Table 1. Study environments.** Measured shift covariates at the primary configuration and
the preregistered focal class. Source and target are: NSL-KDD, KDDTrain+ to KDDTest+ under a
five-rung unseen-subtype ladder; CIC-IDS2017, Wednesday denial-of-service traffic under five
variant-holdout realisations; UGR'16, July week 5 to August week 1; CIC-IoT-2023, a five-rung
novel-subtype ladder with two web-attack subtypes withheld. S_cov is an **aggregate** over all
classes, retained only to characterise environments as wholes; it is constant within an
environment and cannot describe the classes inside it, for which Table 9 gives
class-conditional values ranging from 0.499 to 1.000 within one environment. S_sup is the class-conditional
form S_sup,c throughout, the fraction of the focal class's target evaluation mass in subtypes
absent from the source, so the rows are comparable.

| Dataset | Shift type | S_cov | S_lab | S_sup | Focal |
|---|---|---|---|---|---|
| NSL-KDD | covariate + support | 0.84–0.90 | ~0.14 | 0.00–0.46 | R2L |
| CIC-IDS2017 | variant novelty (+prior) | 0.76–0.77 | 0.44–0.52 | 0.00–0.54 | DoS |
| UGR'16 | temporal feature drift | 0.69 | 0.00 | 0.00 | nerisbotnet |
| CIC-IoT-2023 | semantic subtype novelty | 0.50 agg, 0.65 focal | ~0.01 | 0.00–0.80 | Web |

## 3.1 NSL-KDD

We use the canonical split of NSL-KDD [29], KDDTrain+ (125,973 flows) as source and KDDTest+ (22,544) as
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

For CIC-IDS2017 [28] we adopt the corrected labelling [10] and a cleaned release as the version of record, since documented label errors in the
original distribution are substantial enough to change conclusions drawn from it [16]. We use Wednesday denial-of-service traffic with benign traffic; the task is binary.
Support shift is constructed within the day by withholding DoS variants: Hulk is always retained
in calibration and five realisations withhold different combinations of the remainder
(Slowhttptest; Slowloris; GoldenEye; Slowloris with Slowhttptest; GoldenEye with Slowloris)
while requiring them at evaluation. The variant composition is strongly asymmetric, GoldenEye holding 32 source flows against 7,361
at target and Slowloris 589 against none. That asymmetry makes the class-conditional support
shift highly uneven across realisations, from 0.000 where the withheld variant has no target
instances to 0.542 where it dominates the target block, and Section 5.6 notes that coverage does
not follow it. Because a trivially separable task would make the coverage question
vacuous, we audited feature separability: the most discriminative single feature reaches an
area under the ROC curve of 0.984 and no feature acts as an identifier, so the near-perfect
accuracy is genuine rather than label leakage. The focal class is DoS.

## 3.3 UGR'16

UGR'16 [18] provides the temporal-feature-drift environment: one week of July traffic as source and
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
zero while S_cov is 0.69 against a permutation-null threshold of 0.51. We describe this as temporal feature drift at retained label support rather than covariate shift
in the strict sense. Equal sampled counts and retained broad-label support establish two things:
no measured prior shift, and a temporal difference in the feature distribution. They do not
establish that the conditional law P(Y | X) is invariant across the two weeks, and the provenance
caveats above make that assumption unattractive. The focal class is
nerisbotnet, chosen on operational rarity rather than the capped counts.

## 3.4 CIC-IoT-2023

CIC-IoT-2023 [20] supplies a contemporary environment, collected from 105 real IoT
devices in 2023. The release as acquired carries 35 distinct labels, grouped here into seven
attack families plus benign traffic. Its
recency and its subtype hierarchy make it suitable for a novelty ladder on modern traffic.

The release exceeds the compute budget, so it is subsampled by a per-label cap of 60,000 rows
applied as a keep-fraction while streaming, which retains every rare label in full and yields a
working frame of 1,510,142 rows. The cap is conservative for a support-shift study because it
compresses the class-prior gap rather than widening it, though it also raises the Web family
from roughly 0.05 to 1.64 per cent of the working frame, which makes that family easier to learn
than it would be at natural prevalence. Both effects are recorded as deviations.

Support shift is constructed by designating two of the six web-attack subtypes,
`Uploading_Attack` and `Backdoor_Malware`, as novel and removing them from the source. A
five-rung ladder raises their share of focal evaluation mass from 0.00 to 0.80 while the
remaining non-novel rows are split 70/30 between source and target. The focal class is Web,
selected by the preregistered focal-class rule as the rarest attack family with sufficient
source support, at 12,159 source calibration flows.

Across the ladder the aggregate covariate shift stays at the permutation null, 0.495 to 0.506,
the label-prior shift is negligible at 0.004 to 0.014, and the class-conditional novel fraction
sweeps from 0.000 to 0.800. We deliberately do not call this support shift in isolation:
Section 5.10 measures S_cov,Web = 0.654 against an aggregate of 0.512, so the focal class does
carry measurable source-target feature distinguishability even where the aggregate sits at its
null. Reading isolation off an aggregate is the error Section 5.10 exists to expose. The
environment is better described as large semantic subtype novelty with moderate focal-class
feature drift.

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

The object of study is the calibration set used to form conformal prediction sets [27, 31], not the classifier. We compare three protocols, holding the
classifier and probability calibrator fixed.

The **recalibrated protocol (REC)** calibrates the conformal quantile on the evaluation set
itself and then evaluates on those same observations. It is deliberately circular and serves as
an upper bound whose coverage sits at the nominal level by construction. We do not call it
transductive: full or transductive conformal prediction refits the nonconformity score for each
candidate label, whereas REC simply reuses the evaluation sample for calibration. The **target-supervised protocol (TSC)** calibrates on a labelled
target sample; it requires target labels and is not deployable in practice, but it isolates the
effect of calibrating on in-distribution target data. The **source-held-out protocol (SHC)**
calibrates on the source calibration pool and requires no target labels.

We study SHC as the simplest fixed, source-calibrated baseline, requiring neither target labels
nor target-domain adaptation. It is not the only protocol deployable without target labels:
recent work adapts conformal prediction using unlabelled target data or pseudo-labels, and
label-free conformal drift signals have been proposed for streaming intrusion detection. Those
methods are outside the scope of a study that asks what happens to the fixed baseline under
shift, and we do not claim they are undeployable.

The primary contrast is TSC versus SHC. The two protocols differ in calibration-data provenance and,
under natural class prevalence, in class-specific calibration support. Both draw calibration sets
of a common overall size. But the per-class counts entering a class-conditional quantile follow
the class composition of the pool they come from, so for a class that is rare at source and
common at target, the source-calibrated baseline calibrates on fewer points. We therefore do not
describe the protocols as differing only in the calibration set. Section 5.12 quantifies this
asymmetry and removes it by matching per-class calibration sizes.

## 4.2 Nonconformity score and prediction sets

Nonconformity is measured with the adaptive prediction set (APS) score [25]. For
a calibrated probability vector p(x) and candidate label y, the score accumulates the
probability mass ranked above y and adds a randomised fraction of the mass at y,
s(x, y) = Σ_{j: p_j(x) > p_y(x)} p_j(x) + U·p_y(x), with U uniform on [0, 1]. The
randomising draws are produced by a counter-based generator keyed by model seed, sample
and label, so that the three protocols observe identical realised scores on identical
points and differ only in their calibration set. Prediction sets are formed per class in
the Mondrian manner [31]: for miscoverage level α the conformal quantile of a
class is its k-th smallest calibration score with k = ⌈(n+1)(1−α)⌉, or ∞ when k > n. A
class whose calibration count falls below ⌈1/α⌉ − 1 returns an infinite quantile and a
trivially full set; such cells are reported as infeasible and excluded from analysis
rather than counted as covered. The primary miscoverage level is 0.05, with 0.10 and
0.20 reported as sensitivity levels.

## 4.3 Model panel and probability calibration

To ensure the coverage findings are not an artefact of a single classifier, each dataset
is fitted with three architectures, a random forest, a gradient-boosted tree ensemble
[9] and a multilayer perceptron, across ten seeds, giving thirty calibrated
models per dataset (Table 2). Hyperparameters are selected once per architecture on the
validation
partition by macro-averaged F1 and then frozen, or fixed a priori where noted as a
deviation. Because modern classifiers are frequently miscalibrated [12], probabilities are
calibrated by one-vs-rest isotonic regression [33] fitted on the
probability-calibration partition of the source and
renormalised to sum to one; the calibrator is fitted on the source only and held fixed
across all protocols and analyses. Model seeds vary the classifier only; the source
partition is drawn once and held fixed across seeds, because the matched draws of
Section 4.5 already supply calibration-set variability and re-drawing the partition per
seed would confound the partition draw with model initialisation.

**Table 2. Base classifier performance** (mean macro-F1 over ten seeds, per architecture).

| Dataset | Random forest | Boosted trees | MLP |
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
assumed, along three axes. The covariate shift S_cov is the cross-fitted area under the ROC curve of a domain classifier trained to distinguish source from target covariates at a fixed per-side subsample, a classifier two-sample test [5, 17]; a value near one half indicates indistinguishable
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
value of 0.80 corresponds to a global value near 0.011. Table 1 reports S_sup,c for the focal class of every environment, on a single definition; the
earlier global values are retained in the repository. The three axes are exercised differently across
datasets (Table 1). The NSL-KDD ladder sweeps S_sup,c from 0.00 to 0.46 while its S_cov stays
in 0.84–0.90. CIC-IDS2017 carries label shift together with a class-conditional support shift
that varies sharply across realisations, from 0.000 where the withheld variant has no target
instances to 0.542 where it dominates. UGR'16 carries temporal feature drift with S_lab and
S_sup,c fixed at zero.

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
[6] with the protocol-by-shift interactions as the terms of interest and
the target-supervised protocol as reference. We report it as a secondary and descriptive
analysis rather than as inference, for reasons set out in Section 5.15; the
crossed-random-effects fit is additionally not reliably estimable in the available tooling
and is deferred to a specialised estimator [4], recorded as a deviation. No causal claim
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
on data from another dataset; the statistic is therefore computable in deployment rather than requiring cross-dataset access. The monitor is graded against realised undercoverage and against the oracle
score movement, and its blind spot is characterised by the misroute rate, the fraction of a
class's true target flows the detector predicts as some other class. We distinguish
displacement-type drift, where the novel behaviour is still predicted as its class, from
similarity-type drift, where it is confidently misrouted; the monitor is expected to
detect the former and to attenuate on the latter.

## 4.9 Robustness analyses

Several analyses guard against alternative explanations. To exclude label-prior shift, an
inverse-probability-weighting analysis [13] reweights the target evaluation
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
[7] and expected calibration error [19] of the calibrated probabilities are
reported on the source calibration pool, held out from the calibrator's fitting partition,
using equal-mass binning [24].

## 4.10 Preregistration and reproducibility

The study is preregistered. Focal classes, protocols, shift measures, the primary test
and the analysis plan were fixed before any coverage number was computed, and all
subsequent departures are logged as dated amendments and deviations. Data partitions,
calibrated probabilities, coverage tables and every derived result are committed with
deterministic seeds, and partition fingerprints permit independent verification.

**Use of AI assistance.** A large language model assistant was used in implementing the analysis
code, in preparing the manuscript text, and in building the verification tooling described in
this section. The research questions, study design, analytical choices and all interpretations
are the author's, and the assistant is not credited as an author. Every numerical value reported
here is produced by the committed analysis code and checked programmatically against the
released result files, so no reported quantity rests on assistant output; that check is part of
the released code and can be re-run independently. The author accepts full responsibility for
the content.

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

The classification below is binding on how the results should be read.

**Pilot-informed preregistration.** The three calibration protocols and the initial coverage
hypothesis. Earlier exploratory results on NSL-KDD, UNSW-NB15 and CIC-IDS2017 motivated the
hypothesis, as Amendment 1 records.

**Prespecified before the corresponding coverage existed.** The focal-class rule, the
feasibility floor and the partitioning, per environment. Also the CIC-IoT-2023 environment,
named in the base preregistration and gated before any of its coverage existed (Amendments 10
and 11).

**Prospectively specified but not the original confirmatory test.** The within-NSL
dose-response of Section 5.3, promoted to the principal within-dataset analysis after the
preregistered pooled interaction proved unidentifiable (Amendment 3 and the deviation log). The
CIC-IDS2017 within-day redesign was amended after the NSL-KDD outcome was known but before any
CIC coverage existed (Amendment 9).

**Exploratory.** Five analyses. The placebo ladder of Section 5.4, which is additionally
outcome-informed, since the subtype pair was chosen after observing per-subtype coverage. The
class-conditional shift measure of Section 5.10. The threshold-level decomposition of Section
5.11. The label-free diagnostic of Section 5.13, developed and evaluated on the same environments
with no external validation set. And the abstention analysis of Section 5.14.

The confirmatory content is therefore the protocol contrast itself and the per-class coverage
outcomes under the preregistered focal-class and feasibility rules. The mechanism, monitor,
placebo and class-conditional analyses are exploratory, and are marked as such in the text
rather than only here.

# 5. Results

## 5.1 The conformal implementation is validated before it is used

The negative control of Section 4.11 leaves every feasible class statistically consistent with nominal coverage. The band is a population bound under exchangeability, not a requirement that every finite empirical estimate fall inside it, so consistency rather than containment is the criterion.
For the four feasible NSL-KDD classes the observed coverages are 0.9503, 0.9503, 0.9517 and
0.9583 against bands whose lower edge is 0.95, and every seed-clustered bootstrap
interval overlaps its band (Table 3). Two point estimates sit marginally above the
upper edge, by 0.0001 for the majority class and 0.0006 for Probe, which is the expected
consequence of an isotonic calibrator producing tied probabilities and hence mild atoms
in the score distribution. That residual is the baseline conservatism of the pipeline. At 0.0006 it is comparable in size to the smallest deviations reported below, such as the 0.001 shortfall on one UGR'16 class, and two to three orders of magnitude smaller than the substantive failures. Coverage failures reported in this paper are therefore attributable to
distribution shift and not to the implementation.

**Table 3. Negative control: no shift by construction.** Source pool split at random,
calibrate on one half and evaluate on the other, over the full model panel.

| Class | n_cal | Coverage | 95% CI | Band | Inside |
|---|---|---|---|---|---|
| DoS | 3440 | 0.9503 | [0.9497, 0.9509] | [0.9500, 0.9503] | yes |
| Normal | 5053 | 0.9503 | [0.9495, 0.9509] | [0.9500, 0.9502] | yes |
| Probe | 876 | 0.9517 | [0.9500, 0.9531] | [0.9500, 0.9511] | yes |
| R2L | 75 | 0.9583 | [0.9533, 0.9633] | [0.9500, 0.9632] | yes |

## 5.2 Source-held-out calibration undercovers severely in selected classes and environments

Under shift the fixed source-calibrated baseline does not merely fall short of the nominal level
on the classes it affects; it falls below the lower edge of the band the exchangeability
guarantee would imply. The failure is selective, and the selection matters (Table 4):

- **NSL-KDD**: all four feasible classes undercover, from 0.023 below the band for the majority
  class to 0.864 for the focal class.
- **CIC-IDS2017**: DoS undercovers by 0.346; Benign retains 0.950.
- **UGR'16**: scan11 and scan44 undercover by 0.415 and 0.151; background, dos and nerisbotnet
  hold at 0.949, 0.950 and 0.947, the first two falling below the band's edge by 0.001 and 0.003
  but within a one-percentage-point equivalence margin.
- **CIC-IoT-2023**: no class undercovers.

Two thresholds appear in this paper and are kept distinct. A class *falls below the band* when
its coverage lies under the lower edge implied by the exchangeability guarantee, which is a
formal criterion satisfied by nine class cells including two whose shortfall is 0.001 and 0.003.
A class *fails practically* when its shortfall exceeds one percentage point, which is the
criterion used wherever this paper counts failures, and which seven cells meet: all four NSL-KDD
classes, CIC-IDS2017 DoS and the two UGR'16 scan classes. UGR'16 nerisbotnet and background meet
the formal criterion but not the practical one.
Where a later section requires a coarser split, such as the class-level comparisons of Sections
5.10 and 5.16, a five-percentage-point threshold is used and stated there.

**Table 4. Classes falling below the exchangeability-based band, α = 0.05.** Shortfall is the
distance below the band's lower edge. The last two rows meet the formal criterion but not the
practical one, with shortfalls of 0.003 and 0.001 inside a one-percentage-point equivalence
margin; they are listed for completeness and are not counted as failures elsewhere. Classes
retaining nominal coverage are named in the text; their omission is not evidence of universal
failure, and CIC-IoT-2023 has no affected class.

| Dataset | Class | n_cal | Observed | Band edge | Shortfall |
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
failure is a property of calibration provenance rather than of conformal prediction. Table 4
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
between adjacent rungs at every step (Table 5). A mixed model on the empirical logit with a
random intercept per realisation gives a slope of -2.071 per unit of unseen fraction, standard
error 0.024.

**Table 5. Primary dose-response: NSL-KDD focal coverage under the source-calibrated baseline,
α = 0.05.** Seed-clustered bootstrap intervals, B = 2000.

| Rung | S_cov | S_sup | Coverage | 95% CI |
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

**Table 6. Placebo ladder: focal coverage with no support shift, α = 0.05.** Evaluation mass
drawn only from subtypes present in the source. Novelty ladder shown for comparison.

| `guess_passwd` share | 0.00 | 0.25 | 0.50 | 0.75 | 1.00 | swing |
|---|---|---|---|---|---|---|
| Focal coverage | 0.3076 | 0.2331 | 0.1614 | 0.0814 | 0.0097 | **0.298** |
| S_sup | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | |
| Score movement (KS) | 0.801 | 0.836 | 0.873 | 0.914 | 0.972 | |
| *Novelty ladder coverage* | *0.143* | *0.114* | *0.085* | *0.058* | *0.030* | *0.113* |

The placebo ladder moves coverage by 0.298 against the novelty ladder's 0.113 (Table 6), a ratio of
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

![**Fig. 2** The placebo ladder. (a) Focal coverage against ladder position for the
novelty ladder, which introduces subtypes absent from the source, and for the placebo ladder,
which rearranges mass among subtypes the source has already seen and holds the support shift at
exactly zero. The placebo moves coverage 2.6 times further. (b) Within-subtype coverage range
across the novelty rungs for each subtype, against the class-level swing: every component is
close to invariant, so the class-level dose-response is a mixture average of fixed per-subtype
coverages](figs/fig2_placebo.png)

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
distinguishable in aggregate. It does not establish covariate shift with an invariant conditional law, and it does not exclude
the composition effect that Section 5.4 demonstrates directly. Section 5.10 adds a further limit:
an aggregate statistic cannot characterise a class-conditional quantity at all. Within NSL-KDD
the class-conditional values range from 0.789 to 0.991 while the aggregate assigns 0.893 to every
class. We
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

CIC-IoT-2023 carries large semantic subtype novelty: two of six web-attack subtypes are absent
from the source entirely, and the ladder raises their share of focal evaluation mass to 0.80. If
semantic novelty at the subtype level were sufficient to break class-conditional coverage, this
is where it would show.

It does not. Focal coverage under the source-calibrated baseline is 0.9491, 0.9517, 0.9509, 0.9520 and
0.9519 as the novel fraction rises from 0.00 to 0.80 against a nominal 0.95 (Table 7), with a
seed-clustered interval of [0.950, 0.954] at the top rung. All eight classes sit inside their
bands under all three protocols, none is infeasible, and mean prediction-set size differs by
0.014 between protocols. At a novel fraction nearly twice the largest reached on NSL-KDD, nothing
fails.

**Table 7. CIC-IoT-2023: focal coverage under the fixed source-calibrated baseline across the
novel-subtype ladder, α = 0.05.** Nominal 0.95. Aggregate S_cov is at the permutation null
throughout, though the focal class carries S_cov,Web = 0.654 (Table 9).

| Novel fraction | 0.00 | 0.20 | 0.40 | 0.60 | 0.80 |
|---|---|---|---|---|---|
| SHC | 0.9491 | 0.9517 | 0.9509 | 0.9520 | 0.9519 |
| TSC | 0.9512 | 0.9532 | 0.9497 | 0.9497 | 0.9482 |
| REC | 0.9519 | 0.9519 | 0.9519 | 0.9519 | 0.9519 |

This is the mechanism's negative prediction, and Section 5.11 supplies the instrument that
explains it. The withheld subtypes did move the score distribution, to 0.089, essentially the
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
delivers 0.956 to the same class on the same data (Table 8). A practitioner monitoring
the marginal guarantee alone would observe a system performing to specification while the
class that matters most was undercovered by nine percentage points. Under the deployable
protocol both collapse, to 0.720 aggregate and 0.071 focal. This result motivates the
class-conditional framing of the study and shows that aggregate coverage reporting is not
sufficient to certify a conformal detector.

**Table 8. Marginal versus class-conditional conditioning, NSL-KDD, α = 0.05.**

| Protocol | Marginal, all | Marginal, R2L | Class-conditional, R2L |
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
is reported as a descriptive measure of heterogeneity magnitude rather than as a test. Read descriptively, an I² of 100 per cent implies that essentially all of the between-class
variation is heterogeneity rather than sampling noise. The heterogeneity is large by any
reading, but a class-by-protocol interaction model or a paired cluster bootstrap would be
required before calling it decisive. Which classes fail cannot be read from the aggregate shift magnitude. The
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
S_cov,c (Table 9), the cross-fitted area under the ROC curve of a domain classifier separating
source and target instances *of that class alone*, against a permutation reference from
splitting the pooled per-class data at random.

**Table 9. Class-conditional covariate shift against realised coverage.** The aggregate column
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

Within environments where coverage varies, the class-conditional measure orders it: Spearman
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

One limitation of this statistic must be stated where it is defined. Selecting the target
instances of class c requires the target labels, so S_cov,c explains outcomes after the fact and
cannot be computed by an operator. Section 5.16 examines whether a version using only predicted
probabilities behaves similarly.

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
(p = 1.7 × 10⁻⁸, bootstrap interval [0.610, 0.939], Fig. 3), spanning movement from 0.000 to
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

![**Fig. 3** True-class nonconformity-score movement (KS distance, source vs target) versus realised undercoverage. Because architectures fitted to the same dataset and class are not independent, the reported statistic is estimated at the class level, one ladder rung per laddered dataset, where Spearman is 0.844 (n = 28 across four datasets, 95% CI [0.610, 0.939]). The NSL-KDD focal class R2L, with the largest movement, shows the largest undercoverage; CIC-IoT-2023 occupies the low-movement, no-failure corner](figs/fig3_mechanism.png)

## 5.12 Robustness

*Prior shift.* Class-conditional coverage is invariant to reweighting the target to the source
prior by construction, verified numerically on CIC-IDS2017 and UGR'16 where focal coverage
changes by 0.0000. On CIC-IDS2017, whose aggregate coverage of 0.936 conceals the focal failure
behind a benign majority, reweighting lowers the aggregate to 0.770 and exposes it.

*Analytical choices and miscoverage level.* The focal failure appears in all sixteen
specifications of Section 4.11, formed by two nonconformity scores, two conditioning variants
and four levels, with shortfalls from 0.370 to 0.987. Outcomes are likewise stable in alpha (Fig. 4). At alpha 0.05, 0.10
and 0.20 the focal class covers at 0.030, 0.023 and 0.017 on NSL-KDD, and at 0.604, 0.556 and
0.479 on CIC-IDS2017. Over the same levels UGR'16 nerisbotnet holds at 0.947, 0.895 and 0.790,
and CIC-IoT-2023 Web at 0.952, 0.908 and 0.817. The UGR'16 scan classes fall short at every
level. Neither the failures nor the nulls depend on these choices.

![**Fig. 4** Alpha-sensitivity across all four environments. Focal SHC coverage versus the nominal level (1 - alpha) at alpha in {0.05, 0.10, 0.20}. NSL-KDD R2L and CIC-IDS2017 DoS undercover at every level; UGR'16 nerisbotnet and CIC-IoT-2023 Web track nominal at every level; the UGR'16 scan classes collapse at every level. Neither the failures nor the nulls depend on the choice of alpha](figs/fig4_alpha.png)

*Architecture.* All three architectures fail, with pooled focal coverage of 0.111 for the
multilayer perceptron, 0.082 for the gradient-boosted ensemble and 0.064 for the random forest
against a nominal 0.95. The perceptron and random-forest intervals do not overlap, so severity
depends on the classifier by a factor of about 1.7 while the ladder slope is unchanged. The
qualitative conclusion is architecture independent; its magnitude is not, so changing the model
does not repair the trust layer.

*Efficiency and calibration.* Narrower prediction sets under the source-calibrated baseline are
a symptom of failure rather than efficiency: wherever it undercovers, its sets are both smaller
and miss coverage, 2.04 against 4.68 on NSL-KDD at coverage 0.030 against 0.953 (Fig. 5).
Class-averaged expected calibration error is at or below 0.002 on all four datasets, including
0.0006 mean and 0.0015 maximum on CIC-IoT-2023 (Fig. 6), so the failures are not a
base-miscalibration artefact.

![**Fig. 5** Efficiency across all four environments. Focal coverage versus focal prediction-set size for each protocol and dataset. Wherever SHC undercovers, its sets are smaller and miss coverage; TSC and REC pay a larger set width. On CIC-IoT-2023, where coverage holds, the three protocols sit together](figs/fig5_efficiency.png)

![**Fig. 6** Calibration quality of the isotonic-calibrated probabilities on the held-out source calibration pool, for all four environments. (a) Per-class expected calibration error and (b) per-class Brier score, by dataset. On CIC-IoT-2023, where coverage holds, this also forecloses the converse objection that the null is an artefact of unusually good or poor calibration. All per-class ECE values fall at or below 0.002 (dashed line), confirming that the probabilities feeding the conformal layer are well calibrated in distribution](figs/fig6_calibration.png)

*Calibration-set size.* Per-class calibration sets differ in size across protocols for a
structural reason: on NSL-KDD the source-calibrated baseline calibrates the focal class on 149
points against 297 for target-supervised, because R2L is rare at source and common at target.
Under exchangeability a smaller set biases towards over-coverage, since the band is bounded
above by 1/(n + 1), but that argument does not survive the loss of exchangeability. Rather than
assume a direction we removed the confound, subsampling both calibration sets to identical
per-class counts, n_match = min(n_SHC, n_TSC), with the evaluation set, classifier, calibrator
and realised scores unchanged.

The contrast is unaffected (Table 10). The NSL-KDD focal gap is 0.9237 at natural budgets and
0.9240 when both protocols calibrate on 149 points, retaining 100 per cent of the effect with a
seed-clustered interval of [0.9217, 0.9265]; UGR'16 retains 96.6 per cent and CIC-IoT-2023 79.3
per cent of a gap negligible in both conditions. The protocol difference is therefore an effect
of calibration-data provenance, not of sample size. That this needed testing is shown by the
size effect itself: two calibration sets of 297 and 149 points drawn from the *same*
distribution produce a spurious difference of about 0.011, real but two orders of magnitude
below the measured effect.

**Table 10. Class-budget-matched protocol contrast, focal class, α = 0.05.**

| Environment | Budget | TSC | SHC | Gap | n_cal TSC/SHC |
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

## 5.13 Label-free monitoring, its per-dataset behaviour, and its boundary

A monitor that ranks classes by the drift of their predicted-class score distributions can be
computed without any target labels. Pooled across the fifty-seven feasible class cells, it is
rank-correlated with realised undercoverage at 0.738 and separates undercovering classes at an
area under the ROC curve of 0.930, with a bootstrap interval of [0.851, 0.990]. An oracle using
true labels reaches 0.925 and 0.96 on the same two measures. Performance is stable to the
threshold that defines an undercovering class (Fig. 7).

The monitor is evaluated on the three environments in which coverage actually fails; on CIC-IoT-2023 there is no failure to predict, so it does not apply there. Across those three, performance is consistent rather than carried by any one of them (Table 11): 0.926 on NSL-KDD, 0.955 on CIC-IDS2017 and 0.981 on UGR'16, with every
interval excluding chance. The intervals are nonetheless wide, since each environment
contributes between twelve and thirty class cells, so the per-environment estimates should
be read as consistent in direction rather than precisely resolved.

**Table 11. Label-free monitor by dataset.**

| Dataset | Cells | Failing | Monitor ρ | AUROC | 95% CI | Oracle ρ |
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

![**Fig. 7** The label-free coverage-failure monitor. (a) The monitor signal (predicted-class score drift, requiring no target labels) versus realised undercoverage across the 57 feasible class cells (Spearman 0.738, AUROC 0.930). (b) Label-free drift versus oracle (true-label) drift: points far below the diagonal are the similarity-type blind spot, where a novel class is confidently misrouted so the predicted-class distribution barely moves](figs/fig7_monitor.png)

## 5.14 Abstention does not repair the failure, and the reason is instructive

The monitor identifies which classes will undercover, raising the question of what to do next.
The natural answer is triage: abstain on the least trustworthy alerts and retain the guarantee on
the remainder. We evaluate a policy that never consults a label, escalating alerts in ascending
order of the margin m(x) = max over classes c of (q_c − s(x, c)), where q_c is the
source-calibrated threshold and s(x, c) the nonconformity score, so the most atypical alerts
reach the analyst first. A negative margin means an empty prediction set and a certain miss.
Classes with an infinite threshold under the feasibility rule are excluded from the
maximisation; scores share a common scale and are not renormalised; ties break on class index;
and the retained-coverage denominator is the count of retained alerts whose true class is the
focal class.

The policy substantially improves the marginal guarantee, raising aggregate coverage from 0.936
to 0.985 on CIC-IDS2017 and 0.879 to 0.916 on UGR'16 when a tenth of alerts are escalated. It
does almost nothing for the class-conditional guarantee where that guarantee has failed
(Fig. 8), and on the worst-affected classes it does something more troubling than nothing. The
diagnostic evidence is stark: on NSL-KDD the empty-set fraction is exactly zero, so every flow
receives a non-empty prediction set that simply does not contain its true class. The alerts that
break class-conditional coverage are not atypical flows near the edge of every quantile but flows
the shifted detector confidently assigns to the wrong class, which therefore carry a large margin
and are escalated last.

Evaluated on the UGR'16 classes that actually fail rather than on focal classes that largely
held, scan11 moves from 0.535 to 0.598 and scan44 from 0.799 to 0.853 when half of all alerts are
escalated, neither reaching nominal. Meanwhile classes already sound are pushed into
over-coverage, dos to 1.000 and background to 0.996, and the disparity between worst and best
served barely moves, from 0.415 to 0.402, for half the analyst budget.

The reason is that the policy is anti-correlated with need. Uniform escalation would retain
exactly one minus the escalated fraction of every class. Instead the failing classes are retained
*above* uniform at every budget, scan11 by 0.028 to 0.053 and scan44 by 0.021 to 0.044, while
sound classes are retained below it, dos by −0.020 to −0.033: a mean deviation of +0.039 against
−0.009. A queue ordered by typicality reaches confident misroutes last, because a confident
misroute is by construction atypical of nothing. This is the same identifiability limit that
produces the diagnostic's similarity-type blind spot in Section 5.13, so the two results share
one cause. The practical consequence is that an operator can buy back the marginal guarantee cheaply, and
can use the diagnostic to learn which classes are affected. Restoring the per-class guarantee
requires information the target does not supply. That returns the argument to the lever identified
in Section 6: obtaining even a small labelled sample of target traffic.

Two limits on this result. It tests one policy, so it establishes that margin-ordered abstention
fails rather than that no label-free triage can succeed; entropy, ensemble disagreement, density
and hybrid policies are untested. And coverage on a model-dependent retained subset is not a
recovered conformal guarantee, so we report empirical retained-set coverage rather than claiming
the guarantee is restored.

![**Fig. 8** Label-free selective prediction on UGR'16, showing the classes that actually fail rather than focal classes that largely held. (a) Coverage among retained alerts against the fraction escalated to an analyst; the policy orders by margin and never consults a label. (b) The fraction of each class still retained. The failing classes scan11 and scan44 are retained above the uniform rate at every budget while the sound classes are retained below it, so the policy escalates the alerts that least need review](figs/fig8_selective.png)

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
[8]. We
therefore treat the pooled coefficients as descriptive and rest the causal claim on the
within-dataset dose-response of Section 5.3 and the decomposition of Section 5.5.

## 5.16 A deployment-time proxy for the class-conditional shift statistic

Section 5.10 measures class-conditional shift with a domain classifier separating source and
target instances *of that class*. Constructing the target side requires target labels, so that
statistic is retrospective: it explains outcomes after the fact and cannot be computed by an
operator. This section asks whether a version exists that uses only quantities available at
deployment.

The proxy replaces true-label selection with the model's own predicted responsibilities. Every
target flow enters the comparison weighted by its calibrated probability of belonging to class
c, making the statistic a weighted domain-classifier area under the ROC curve that uses no
labels. Two coarser variants, restricting to flows whose top prediction is c and to the top
decile of predicted responsibility, are reported alongside it.

**Table 12. Deployment-time proxies against the retrospective statistic.** Misroute is the
fraction of true class-c target flows the model assigns elsewhere. Ten of seventeen classes
shown; the full table is released with the code.

| Environment | Class | Oracle | Soft proxy | Misroute | Undercoverage |
|---|---|---|---|---|---|
| NSL-KDD | R2L | 0.9960 | 0.9611 | 0.909 | 0.920 |
| NSL-KDD | DoS | 0.9601 | 0.9422 | 0.193 | 0.551 |
| UGR'16 | scan11 | 0.9997 | 0.9816 | 0.517 | 0.415 |
| NSL-KDD | Probe | 0.9792 | 0.9600 | 0.306 | 0.322 |
| UGR'16 | scan44 | 0.9844 | 0.9572 | 0.317 | 0.151 |
| NSL-KDD | Normal | 0.7841 | 0.8346 | 0.025 | 0.023 |
| UGR'16 | nerisbotnet | 0.5778 | 0.7144 | 0.487 | 0.003 |
| CIC-IoT-2023 | Web | 0.6402 | 0.7101 | 0.729 | −0.002 |
| CIC-IoT-2023 | BruteForce | 0.4873 | 0.6822 | 0.787 | −0.006 |
| CIC-IoT-2023 | Mirai | 0.5032 | 0.5003 | 0.005 | −0.000 |

We count a class as losing coverage when its shortfall exceeds five
percentage points, the coarser of the two thresholds defined in Section 5.2. On that criterion
the proxy separates the two groups across seventeen classes in three environments. Every class
that loses coverage lies between 0.942 and 0.982, every class that retains it between 0.500 and
0.835: a margin of 0.108 with no overlap.
It ranks undercoverage at Spearman 0.721 against 0.860 for the retrospective statistic, and
tracks that statistic at 0.801 with a mean absolute difference of 0.061. Dropping each
environment in turn preserves the separation in all three folds, and a bootstrap resampling
whole datasets separates in every one of 4,000 resamples, with the margin in [0.108, 0.243].

We expected this to fail, and the reason it did not is informative. The proxy discards flows the
model misroutes, and misrouting on the affected classes is severe, 0.91 for the NSL-KDD focal
class and 0.52 for UGR'16 scan11. Were the drift concentrated in that misrouted traffic the
proxy would be blind to it. It is not: the focal class reads 0.961 from the nine per cent of its
traffic the model still assigns correctly, against an oracle of 0.996. Class-conditional drift
is distributed across a class rather than confined to the flows the model gets wrong.

**One property means the proxy is not an estimator of the quantity it approximates.** It is
biased upward, by 0.076 on average across classes that retain coverage and by −0.024 across
those that lose it, and the inflation tracks the misroute rate at Spearman 0.853. CIC-IoT-2023
BruteForce is the clearest case: the retrospective statistic puts it at 0.487, indistinguishable
from the permutation null, while the proxy reads 0.682. Misrouted traffic from other classes
enters the weighted comparison and is genuinely distinguishable from source traffic of class c,
so the proxy detects real shift that is not shift *of that class*. The bias points the safe way
for a screening signal, toward false alarms rather than missed failures, but a value near 0.7 is
not evidence that a class has shifted.

We therefore report an association, not a mechanism or a decision rule. The separating threshold
was identified after the outcomes were known, the comparison rests on seventeen classes of which
five lose coverage, and the proxy and the coverage outcome derive from the same fitted model, so
they are not independent measurements. What the result establishes is narrower and still useful:
the diagnosis of Section 5.10 is not confined to retrospect, since a signal computable from
predicted probabilities alone orders the same outcomes on this benchmark. Whether the separation
survives on environments not used to observe it is the obvious next question and we have not
answered it.

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
for both. An operator watching the aggregate sees one moderate number describing a class that is entirely
shifted and another that has not moved. A dashboard reporting an aggregate drift score cannot
certify a conformal detector, because the same aggregate can leave one class safe and break
another. Trust must be assessed per class.

Whether an operator can do that without labels is a separate question, and Section 5.16 gives a
partial answer. The class-conditional statistic as defined uses target labels, but a version
weighting each flow by its predicted class probability separates the classes that lose coverage
from those that retain it on this benchmark, with no overlap across seventeen classes. It is
biased upward where the model misroutes, so it raises false alarms rather than missing failures,
and the threshold that separates the groups was identified after the outcomes were known. It is
therefore a signal worth testing rather than a rule to deploy.

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

**Relation to validity-restoring methods.** The mixture account of Section 5.4 suggests a
remedy: if class coverage is a mixture average of near-fixed per-subtype coverages, estimate the
target composition and reweight the calibration scores to match it. We attempted this on the
NSL-KDD focal class and it failed, for two reasons that are worth recording. Confusion-corrected
composition estimation [15] assumes the class-conditional feature distribution
is invariant between source and target, and for that class the measured class-conditional shift
is 0.9905, so the assumption does not hold. Separately, eight of the fourteen target subtypes
have no source instances at all, carrying 24.5 per cent of target mass, so no reweighting of
existing calibration scores can represent them: this is a failure of support, not of estimation.
We report the attempt rather than a result, since one class of one dataset is not a basis for a
general claim, and Section 8 sets out what a proper study of repair would require.

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

Tenth, the deployment-time proxy of Section 5.16 is evaluated on the same seventeen classes used
to observe its behaviour, its separating threshold was identified after the outcomes were known,
and only five classes lose coverage, so the separation is reported as observed rather than
validated. The proxy and the coverage outcome also derive from the same fitted model and are not
independent measurements.

Eleventh, the study diagnoses without repairing. We attempted one repair, reweighting calibration
scores to an estimated target composition, and it failed on the class we tried it on for reasons
given in Section 6; we do not report it as a result and it should not be read as evidence that
repair is impossible in general.

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
misses, and would reconcile the S_sup column of Table 1 onto a common definition. The
class-budget-matched contrast of Section 5.12 covers three environments; extending it to
CIC-IDS2017 requires rebuilding the matched draw per realisation and would close the one
remaining unmatched protocol comparison. The placebo construction of Section 5.4 is
outcome-informed; a confirmatory version fixing the subtype pair from source-side information
alone, or evaluating all feasible pairs and reporting the distribution, would convert a
demonstration of possibility into a measurement of magnitude.

The most immediate extension is to validate the label-free diagnostic properly. It is currently developed and evaluated on the same environments, so
leave-one-environment-out validation is needed. That validation should include CIC-IoT-2023 as an
all-negative environment measuring specificity and false-alarm burden, rather than excluding it
for lacking positives. It should also compare against simpler baselines: predicted-score movement
alone, share collapse alone, confidence or entropy shift, and existing conformal drift monitors. Completing the characterisation of its
boundary calls for a continuous, model-internal measure of class confusability to replace the
misroute proxy, and for environments rich in similarity-type drift.

The most immediate test of Section 5.16 is external: the proxy should be evaluated on
environments not used to observe its separation, with the threshold fixed in advance, since
nothing here establishes that it transfers. Correcting its upward bias, which arises because
misrouted traffic from other classes enters the weighted comparison, would also make it an
estimator of the retrospective statistic rather than a correlate of it.

A proper study of repair is the largest gap this paper leaves, and our failed attempt indicates
what it would require. Composition-based reweighting must be evaluated by reporting coverage
after reweighting rather than the accuracy of the composition estimate, with the weighted
quantile, its normalisation, its handling of subtypes absent from the source, and the
uncertainty induced by estimated weights all specified. It must also state which invariance it
assumes, since the condition that matters is invariance of the subtype-conditional feature
distribution rather than of the class-conditional one, and these are not the same: a change in
subtype composition alters the class-conditional distribution even when every subtype-conditional
distribution is invariant. Whether class-conditional shift can serve as a practical screen for
that condition is an open question our data cannot settle, and it would in any case require a
label-free surrogate, since the statistic as defined here uses target labels. A constructive
direction that avoids composition estimation entirely is to convert the diagnostic into a remedy
by widening prediction sets on the classes it flags, testing whether that restores coverage on displacement-type drift while
conceding it cannot on similarity-type drift. Section 5.14 sharpens this: because alert-level
triage cannot reach confident misroutes, a remedy must act on the calibration rather than the
alert stream. Finally, replication on contemporary traffic beyond CIC-IoT-2023 would test
whether the mechanism, being expressed in score movement rather than packet content, transfers
as expected.

# 9. Conclusion

We asked, under preregistration, whether the fixed source-calibrated conformal protocol for
network intrusion detection retains its class-conditional coverage when calibration and
deployment traffic differ. Across four datasets it does not, on the classes that matter most.
Coverage falls to 0.030 on the rarest attack class of NSL-KDD and to 0.604 on CIC-IDS2017 denial
of service against a nominal 0.95, while target-supervised calibration holds throughout. That
contrast survives matching both protocols to identical per-class calibration sizes, so it is an
effect of where the calibration data comes from and not of how much of it there is.

The failure is selective and its selection is not predictable from the shift measures a
practitioner would naturally compute. Environment-level statistics are constant within an
environment and cannot order the classes inside it. Neither the category nor the magnitude of
shift decides the outcome: a placebo construction moves coverage further by rearranging mass
among subtypes the source has already seen than by introducing unseen ones, and a fourth
environment sweeping subtype novelty to 0.80 of focal evaluation mass produces no failure at
all. We reduced the phenomenon to a single measurable cause, the movement of a class's
nonconformity-score distribution past the source-calibrated quantile, which orders undercoverage
across twenty-eight class-level cells spanning four datasets at a rank correlation of 0.84.

For practitioners the consequences are concrete. A conformal trust layer calibrated the simplest way an
operator can does not deliver its advertised per-class guarantee under realistic drift.
Aggregate drift monitoring cannot certify it, because the relevant shift is class-conditional.
And alert-level triage does not repair it: the alerts that break the guarantee are confident
misroutes rather than atypical flows, and a queue ordered by typicality reaches them last. What does restore coverage is calibration data drawn from the target, which reframes the
question from whether to adopt conformal prediction to whether even a small labelled sample of
deployment traffic can be obtained.

We report the study with its negative and inconclusive results intact, including a preregistered
analysis that proved unidentifiable at this design, a monitor whose blind spot we characterise
rather than conceal, and an attempted repair that failed. All pipelines, calibrated models,
coverage tables, figures and the preregistration with its amendments are released, and every
numerical claim in this paper is checked against the committed result files.

# Statements and Declarations

**Funding.** No funding was received for conducting this study.

**Competing interests.** The author has no competing interests to declare that are relevant to
the content of this article.

**Data, materials and code availability.** The source datasets are third-party and publicly
available from their original providers, and are not redistributed here. NSL-KDD is distributed
by the Canadian Institute for Cybersecurity as KDDTrain+ and KDDTest+ [29]. CIC-IDS2017 is
distributed by the same institute [28]; we use the corrected labelling of Engelen et al. [10] and
a cleaned release as the version of record. UGR'16 is distributed by the University of Granada
[18], from which we use the July week 5 and August week 1 captures. CIC-IoT-2023 is distributed
by the Canadian Institute for Cybersecurity [20] and was obtained as a 162-file, 12.97 GB
release. No new data were collected and none were obtained under restricted access, so every
dataset analysed here can be acquired independently.

Code, data-acquisition instructions, split manifests, partition fingerprints with their seeds,
the thirty calibrated model probability arrays, all coverage tables, the figures, and the
preregistration with its dated amendments are deposited in a public repository. Every numerical
claim in this paper is checked against those committed files by a script included in the deposit,
which a reader can re-run. An anonymised repository mirror is available to reviewers at
[ANONYMOUS REVIEW LINK]; the citable link will be included on acceptance.

**Ethics approval.** Not applicable. This study uses only publicly available network traffic
datasets and involves no human participants or animals.

# References

1. Angelopoulos, A.N., Bates, S.: Conformal prediction: a gentle introduction. Foundations and Trends in Machine Learning 16 (4), 494-591 (2023). https://doi.org/10.1561/2200000101

2. Barber, R.F., Candès, E.J., Ramdas, A., Tibshirani, R.J.: Conformal prediction beyond exchangeability. The Annals of Statistics 51 (2), 816-845 (2023). https://doi.org/10.1214/23-AOS2276

3. Barrett, S., et al.: FADES: adaptive drift estimation via conformal signals for streaming intrusion detection. Electronics 15 (10), 2114 (2026)

4. Bates, D., Mächler, M., Bolker, B., Walker, S.: Fitting linear mixed-effects models using lme4. Journal of Statistical Software 67 (1), 1-48 (2015). https://doi.org/10.18637/jss.v067.i01

5. Ben-David, S., Blitzer, J., Crammer, K., Kulesza, A., Pereira, F., Vaughan, J.W.: A theory of learning from different domains. Machine Learning 79 (1-2), 151-175 (2010). https://doi.org/10.1007/s10994-009-5152-4

6. Breslow, N.E., Clayton, D.G.: Approximate inference in generalized linear mixed models. Journal of the American Statistical Association 88 (421), 9-25 (1993). https://doi.org/10.1080/01621459.1993.10594284

7. Brier, G.W.: Verification of forecasts expressed in terms of probability. Monthly Weather Review 78 (1), 1-3 (1950). https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2

8. Cameron, A.C., Miller, D.L.: A practitioner's guide to cluster-robust inference. Journal of Human Resources 50 (2), 317-372 (2015). https://doi.org/10.3368/jhr.50.2.317

9. Chen, T., Guestrin, C.: XGBoost: a scalable tree boosting system. In: Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining. ACM, pp. 785-794 (2016). https://doi.org/10.1145/2939672.2939785

10. Engelen, G., Rimmer, V., Joosen, W.: Troubleshooting an intrusion detection dataset: the CICIDS2017 case study. In: 2021 IEEE Security and Privacy Workshops (SPW). IEEE, pp. 7-12 (2021). https://doi.org/10.1109/SPW53761.2021.00009

11. Gibbs, I., Candès, E.J.: Adaptive conformal inference under distribution shift. In: Advances in Neural Information Processing Systems, vol. 34. Curran Associates, pp. 1660-1672 (2021)

12. Guo, C., Pleiss, G., Sun, Y., Weinberger, K.Q.: On calibration of modern neural networks. In: Proceedings of the 34th International Conference on Machine Learning. Proceedings of Machine Learning Research, vol. 70. PMLR, pp. 1321-1330 (2017)

13. Horvitz, D.G., Thompson, D.J.: A generalization of sampling without replacement from a finite universe. Journal of the American Statistical Association 47 (260), 663-685 (1952). https://doi.org/10.1080/01621459.1952.10483446

14. Kasa, K., Zhang, Z., Yang, H., Taylor, G.W.: Adapting prediction sets to distribution shifts without labels. In: Proceedings of the 41st Conference on Uncertainty in Artificial Intelligence (UAI) (2025)

15. Lipton, Z.C., Wang, Y.-X., Smola, A.: Detecting and correcting for label shift with black box predictors. In: Proceedings of the 35th International Conference on Machine Learning, PMLR 80, 3122-3130 (2018)

16. Liu, L., Engelen, G., Lynar, T., Essam, D., Joosen, W.: Error prevalence in NIDS datasets: a case study on CIC-IDS-2017 and CSE-CIC-IDS-2018. In: 2022 IEEE Conference on Communications and Network Security (CNS). IEEE, pp. 254-262 (2022). https://doi.org/10.1109/CNS56114.2022.9947235

17. Lopez-Paz, D., Oquab, M.: Revisiting classifier two-sample tests. In: International Conference on Learning Representations (ICLR) (2017)

18. Maciá-Fernández, G., Camacho, J., Magán-Carrión, R., García-Teodoro, P., Therón, R.: UGR'16: a new dataset for the evaluation of cyclostationarity-based network IDSs. Computers & Security 73, 411-424 (2018). https://doi.org/10.1016/j.cose.2017.11.004

19. Naeini, M.P., Cooper, G.F., Hauskrecht, M.: Obtaining well calibrated probabilities using Bayesian binning. In: Proceedings of the Twenty-Ninth AAAI Conference on Artificial Intelligence. AAAI Press, pp. 2901-2907 (2015)

20. Neto, E.C.P., Dadkhah, S., Ferreira, R., Zohourian, A., Lu, R., Ghorbani, A.A.: CICIoT2023: a real-time dataset and benchmark for large-scale attacks in IoT environment. Sensors 23 (13), 5941 (2023). https://doi.org/10.3390/s23135941

21. Pendlebury, F., Pierazzi, F., Jordaney, R., Kinder, J., Cavallaro, L.: TESSERACT: eliminating experimental bias in malware classification across space and time. In: Proceedings of the 28th USENIX Security Symposium. USENIX Association, pp. 729-746 (2019)

22. Podkopaev, A., Ramdas, A.: Tracking the risk of a deployed model and detecting harmful distribution shifts. In: International Conference on Learning Representations (ICLR) (2022)

23. Qiu, H., Dobriban, E., Tchetgen Tchetgen, E.: Prediction sets adaptive to unknown covariate shift. Journal of the Royal Statistical Society Series B 85 (5), 1680-1705 (2023)

24. Roelofs, R., Cain, N., Shlens, J., Mozer, M.C.: Mitigating bias in calibration error estimation. In: Proceedings of the 25th International Conference on Artificial Intelligence and Statistics. Proceedings of Machine Learning Research, vol. 151. PMLR, pp. 4036-4054 (2022)

25. Romano, Y., Sesia, M., Candès, E.J.: Classification with valid and adaptive coverage. In: Advances in Neural Information Processing Systems, vol. 33. Curran Associates, pp. 3581-3591 (2020)

26. Sadinle, M., Lei, J., Wasserman, L.: Least ambiguous set-valued classifiers with bounded error levels. Journal of the American Statistical Association 114 (525), 223-234 (2019). https://doi.org/10.1080/01621459.2017.1395341

27. Shafer, G., Vovk, V.: A tutorial on conformal prediction. Journal of Machine Learning Research 9, 371-421 (2008)

28. Sharafaldin, I., Habibi Lashkari, A., Ghorbani, A.A.: Toward generating a new intrusion detection dataset and intrusion traffic characterization. In: Proceedings of the 4th International Conference on Information Systems Security and Privacy (ICISSP). SciTePress, pp. 108-116 (2018). https://doi.org/10.5220/0006639801080116

29. Tavallaee, M., Bagheri, E., Lu, W., Ghorbani, A.A.: A detailed analysis of the KDD CUP 99 data set. In: 2009 IEEE Symposium on Computational Intelligence for Security and Defense Applications (CISDA). IEEE, pp. 1-6 (2009). https://doi.org/10.1109/CISDA.2009.5356528

30. Tibshirani, R.J., Foygel Barber, R., Candès, E.J., Ramdas, A.: Conformal prediction under covariate shift. In: Advances in Neural Information Processing Systems, vol. 32. Curran Associates, pp. 2530-2540 (2019)

31. Vovk, V., Gammerman, A., Shafer, G.: Algorithmic Learning in a Random World. Springer, New York (2005). https://doi.org/10.1007/b106715

32. Vovk, V., Nouretdinov, I., Gammerman, A.: Testing exchangeability online. In: Proceedings of the 20th International Conference on Machine Learning (ICML). AAAI Press, pp. 768-775 (2003)

33. Zadrozny, B., Elkan, C.: Transforming classifier scores into accurate multiclass probability estimates. In: Proceedings of the 8th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining. ACM, pp. 694-699 (2002). https://doi.org/10.1145/775047.775151
