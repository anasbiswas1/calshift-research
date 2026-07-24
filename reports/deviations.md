
## notebook 03
- S_cov subsample reduced from the preregistered 20000 per side to 2000, because Amendment 1 fixed D_eval at 2340 rows and 20000 per side is unattainable on the evaluation side. Recorded in Amendment 2 B5.

## notebook 06
- Amendment 3 C4 specifies a beta-binomial GLMM in glmmTMB. Substituted a binomial GLM with cluster-robust standard errors clustered on ladder realization, because no pure-Python package supports the specified structure on the count interface. Architecture and class enter as fixed effects. The Gaussian secondary model retains random intercepts.

## nb10 note: amendments 7-8 committed within 5b5cfc5 (nb09 message); provenance intact, before any coverage.
