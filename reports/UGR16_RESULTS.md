# UGR'16 Result: July-to-August covariate shift (criterion 1)
Commit `3dce2df`, 26 July 2026.

## Environment
Fixed-support temporal covariate shift. Source = July week5, target = august_week1, about one month apart. Background plus the four synthetic attack classes (dos, scan11, scan44, nerisbotnet) are present in both weeks at fixed support, so S_sup = 0 and S_lab = 0; the only shift is covariate. Measured S_cov = 0.69 (domain-classifier AUC on nine flow features), well above the permutation null of 0.51. This is the only environment in the study carrying genuine fixed-support covariate shift; NSL-KDD and CIC-IDS2017 carry support shift.

## Preregistered focal result: nerisbotnet HOLDS
Focal class nerisbotnet, chosen in advance on rarity and temporal-structure grounds. At alpha = 0.05 (nominal 0.95):
- REC 0.950, TSC 0.950, SHC 0.947. Focal gap TSC - SHC = +0.002.
- Consistent across architectures (SHC: RF 0.949, XGB 0.950, MLP 0.943).

The deployable protocol's coverage of the botnet survives a month of covariate drift.

## Discovered finding: the scan classes COLLAPSE under SHC
Not the preregistered focal class; reported as a discovered result. Class-conditional coverage at alpha = 0.05:

| class        | REC   | SHC       | TSC   |
|--------------|-------|-----------|-------|
| background   | 0.950 | 0.949     | 0.950 |
| dos          | 0.950 | 0.950     | 0.950 |
| nerisbotnet  | 0.950 | 0.947     | 0.950 |
| scan11       | 0.950 | **0.535** | 0.950 |
| scan44       | 0.982 | **0.799** | 0.982 |

scan11 undercovers to 0.535 and scan44 to 0.799 under the deployable protocol, while TSC holds both at 0.95. Same shift, same run, opposite outcomes by class. background, dos, and nerisbotnet are unaffected.

## Interpretation (criterion 1)
Criterion 1, SHC undercoverage under covariate shift, was disclosed-inconclusive on NSL-KDD and untestable on CIC. UGR'16 answers it, conditionally:

- Covariate shift CAN break the deployable protocol (scan11, scan44).
- It does so SELECTIVELY. Which classes fail is not predictable from the aggregate S_cov: the same 0.69 covariate shift leaves dos and botnet coverage intact and craters scan coverage.
- The determinant is per-class, whether the drift moved that class's nonconformity-score distribution, not the overall covariate-shift magnitude. The scan classes' score geometry shifted July-to-August; the botnet's and DoS's did not.

This is a stronger and more defensible claim than a uniform pass or fail: aggregate shift magnitude does not predict per-class conformal failure under covariate drift.

## Honesty and provenance
The focal class (nerisbotnet) was fixed before any coverage and is reported as preregistered; it holds. The scan collapse is reported as a discovered finding and is NOT retroactively promoted to focal, which would be the outcome-dependent choice the preregistration exists to prevent. Both are reported in their correct roles.

Caveats carried into the writeup: coverage is measured on the capped, class-balanced target, which does not affect class-conditional coverage since it conditions on the class; and TSC/REC over-cover slightly on scan44 (0.982), the expected small-alpha Mondrian conservativeness seen on CIC too.
