# CALSHIFT Results Ledger (running record)

Status as of the current session. This is a running tally of what is established
and committed, NOT the paper's results section and NOT the final consolidation
(item 6). It records only committed, verified numbers, and marks what is pending.
Latest relevant commit at time of writing: nb23 (Arm B), `2150d24`.

---

## 1. Diagnosis: the deployable protocol undercovers under shift (preregistered, 3 datasets)

Three environments, three shift types, one preregistration. Protocols: REC
(recalibrate on eval), TSC (target-supervised), SHC (source-held-out, the only
deployable one). Focal class chosen in advance per dataset.

Focal class-conditional coverage under SHC at alpha 0.05 (nominal 0.95):

| dataset | shift type | focal | SHC focal coverage | TSC focal | reads |
|---|---|---|---|---|---|
| NSL-KDD | support (subtype novelty) | R2L | ~0.03 (rung 0.80) / 0.086 overall | ~0.95 | collapses |
| CIC-IDS2017 | support (DoS variant holdout) | DoS | 0.590 | 0.993 | collapses |
| UGR'16 | fixed-support covariate (Jul->Aug) | nerisbotnet | 0.947 | 0.950 | HOLDS |

Key discovered finding (UGR'16, committed `3c499f4`): the preregistered focal
(nerisbotnet) holds under pure covariate shift, but scan11 collapses to 0.535 and
scan44 to 0.799 under SHC while TSC holds both at 0.95. Same aggregate S_cov (0.69),
opposite outcomes by class. Covariate-shift failure is SELECTIVE and not predicted
by aggregate shift magnitude. Reported as discovered, not retro-promoted to focal.

## 2. Pooled cross-dataset model (nb18-19, `51caaf4`)

49,500 coverage cells, counts-based, cluster-robust binomial GLM + empirical-logit
mixed-model cross-check. TSC reference.

- beta7 (SHC x S_sup, support-shift interaction): -0.374 GLM / -0.658 mixed, both
  highly significant, SAME sign. WELL IDENTIFIED (NSL sweeps S_sup 0-0.46).
  => support shift drives coverage failure. This is the pooled headline.
- beta5 (SHC x S_cov, covariate interaction): -0.252 GLM but +0.254 mixed. SIGN
  FLIP => NOT IDENTIFIED (S_cov varies only between 3 datasets). Reported as
  sign-unstable; covariate evidence deferred to the per-dataset UGR result.
- Tooling deviation recorded: exact crossed-RE binomial GLMM to be run in R/lme4
  for camera-ready; statsmodels approximations agree on the identified effect.

## 3. Mechanism: score movement explains the failures (nb20 + nb22, `a8c1d16`)

Per class, per architecture: how far the true-class nonconformity-score
distribution moved (source->target) vs the realized undercoverage.

- Spearman(score movement KS, undercoverage) = +0.925, p=4.5e-26, n=60 class-cells,
  across ALL THREE datasets (NSL added at rung 0.80, validated against committed
  coverage). Holds per architecture (rf/xgb/mlp).
- NSL R2L is the hardest case: score shift 0.84, undercoverage 0.88 - largest in
  the study, exactly where movement is largest.
=> classes undercover precisely when their score distribution moves past the
source-calibrated quantile. Mechanistic, robust, cross-dataset.

## 4. Label-free monitor (nb21 + nb22, `a8c1d16`)

Monitor = per-class drift of the PREDICTED-class score distribution (source vs
target), fully label-free, combined with a predicted-mass-collapse fallback for
classes that vanish from predictions.

- Detector vs undercoverage: Spearman +0.73, AUC 0.90, across all 3 datasets
  (n=60). Oracle (true-label drift) +0.90 / AUC 0.96.
- Per dataset detector rho: CIC +0.77, UGR +0.82, NSL +0.38 (NSL weaker, see below).

LIMITATION (demonstrated, honest): the monitor attenuates or goes blind on
similarity-type drift, where the model confidently misroutes a novel class into a
familiar one so the predicted-class distribution barely moves.
- UGR scan11: undercovers 0.49, oracle drift sees 0.52, label-free drift only 0.14
  (misroute 0.56).
- NSL U2R: undercovers 0.41, oracle drift 0.60, label-free UNMEASURABLE (almost no
  flows predicted U2R, misroute 0.84) - caught only by the mass-collapse fallback.
Boundary characterization is INCOMPLETE: misroute vs blind-spot gap rho +0.25,
p=0.09, n too small. This is the acknowledged open edge (candidate Paper 2 work:
5G-NIDD similarity exemplar + a continuous confusability measure).

## 5. Arm B: the failures are genuine, not prior shift (nb23, `2150d24`; NSL pre-existing)

IPW reweights the target to the source class prior; does SHC undercoverage persist?

- Focal class-conditional coverage is INVARIANT to reweighting (focal shift
  +0.0000 on both CIC and UGR, exact by construction) => the focal gap CANNOT be
  a prior-shift artifact. This is the load-bearing confound-killer.
- CIC marginal: 0.936 unweighted -> 0.770 IPW-reweighted (shift -0.166). The
  benign majority was masking the DoS failure; matching the source prior (DoS
  upweighted 7-47x) exposes it. ESS min 1,744 (>> 30 threshold), reliable.
- UGR marginal: 0.879 -> 0.879 (shift -0.000), weights ~1.0, ESS ~59,996. Null
  check confirms no prior-shift confound there.

---

## PENDING (finish list, do not expand)

- item 3 alpha-sensitivity (RUNNING NOW): confirm focal failures hold at alpha
  0.10 and 0.20, not just 0.05. [fill in when nb24 returns]
- item 4 set-size / efficiency: coverage-vs-width tradeoff from recorded set sizes.
- item 5 calibration quality: Brier + ECE per class + reliability curves.
- item 6 results consolidation: assemble all of the above + these into the writeup
  skeleton. THEN hard freeze and write.

## EXPAND list (REFUSE for this paper = Paper 2)
5G-NIDD similarity exemplar; continuous confusability measure; chasing the boundary
to significance; the correction/remedy (mode 2); intermediate UGR August weeks.
