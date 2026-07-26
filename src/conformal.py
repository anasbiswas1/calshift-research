"""Canonical conformal quantile for CALSHIFT.

One implementation, used everywhere, so no notebook re-derives it.

Split-conformal threshold (Vovk et al.; Lei et al. 2018):

    k = ceil((n + 1) * (1 - alpha))
    q = s_(k)  if k <= n, else +inf

s_(k) is the k-th SMALLEST calibration score (1-indexed), i.e. sorted[k-1].

NOTE: np.quantile(s, k/n, method='higher') is NOT equivalent. It returns
sorted[ceil((k/n)*(n-1))], which is one order statistic too high at every n,
inflating coverage by roughly 1/n. Notebook 05 used the correct form; several
later notebooks used the np.quantile form. Use conformal_q everywhere.
"""
import math
import numpy as np


def conformal_q(scores, alpha):
    """Return (q_hat, n). q_hat = +inf when the class has too few points."""
    s = np.asarray(scores, dtype=float)
    n = s.size
    if n == 0:
        return np.inf, 0
    k = math.ceil((n + 1) * (1.0 - alpha))
    if k > n:
        return np.inf, n
    return float(np.sort(s)[k - 1]), n


def min_calib_n(alpha):
    """Smallest calibration count admitting a finite quantile."""
    return math.ceil(1.0 / alpha) - 1


def coverage_band(n, alpha):
    """Finite-sample band under exchangeability: [1-a, 1-a + 1/(n+1)]."""
    return (1.0 - alpha, 1.0 - alpha + 1.0 / (n + 1))
