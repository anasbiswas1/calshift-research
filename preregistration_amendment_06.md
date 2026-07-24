# Preregistration Amendment 6

**Status:** binding on commit. Made before any CIC-IDS2017 coverage number is computed; `reports/` contains no `*_cicids2017` coverage output at the time of writing, only the acquisition inventory, hashes, and manifest from notebook 09.
**Scope:** corrects the CIC-IDS2017 dataset version named in section 3 and in Amendment 5. No analysis decision changes; only the version of record and its citation.

---

## A6.1 Correction to the CIC-IDS2017 version of record

Amendment 5 and section 3 name the CIC-IDS2017 second environment as "WTMC-2021 corrected (Engelen et al. 2021)". On downloading and inspecting the actual files (SHA-256 recorded in `reports/dataset_hashes.json`; five per-day parquet files obtained from the Kaggle mirror `dhoogla/distrinetcicids2017`), the release is identified as the later IEEE CNS 2022 refinement, not base WTMC-2021. Two lines of evidence:

1. The mirror's own version history runs V1 (base CSV) to V5, where V4 and V5 are the IEEE CNS update and its parquet cleaning, and the V2 WTMC-2021 parquet was removed at V3. The parquet files in the current version are therefore the CNS-2022 release, not the WTMC-2021 parquet.
2. The label scheme carries the CNS-2022 refinement's handling: attempted-attack flows relabelled to benign, and the Thursday infiltration port-scan phase tagged separately from the Friday PortScan attack.

**Decision.** The version of record for the CIC-IDS2017 environment is the IEEE CNS 2022 corrected release:

> Liu, L., Engelen, G., Lynar, T., Essam, D., and Joosen, W. (2022). Error Prevalence in NIDS Datasets: A Case Study on CIC-IDS-2017 and CSE-CIC-IDS-2018. 2022 IEEE Conference on Communications and Network Security (CNS), pp. 254-262.

This release descends from and supersedes the Engelen et al. (2021) WTMC-2021 correction, which remains cited as its origin. Every reference to "WTMC-2021" as the CIC version of record in section 3 and Amendment 5 is read as referring to this CNS-2022 release. The exact bytes are pinned by the SHA-256 hashes in `reports/dataset_hashes.json`, so provenance does not depend on the release name. The Drive folder name `cicids2017-wtmc2021` is retained as a path only and does not assert the version.

---

## A6.2 Known feature caveat, recorded for later handling

The CNS-2022 and WTMC-2021 releases use a fixed CICFlowMeter that no longer expires a TCP flow on a single FIN or RST, which produces anomalously high FIN and RST flag counts in some flow records relative to the original CICFlowMeter. This is recorded now so that feature handling in the modelling notebook treats those flag-count features with awareness of the artifact rather than discovering it after coverage is computed. No decision is fixed here; the note exists to keep the choice visible before results.

---

## A6.3 Unchanged

Every analysis decision in Amendment 5 (A5.1 Attempted policy, A5.2 taxonomy, A5.3 source and target per condition) and in the base preregistration is unchanged. Only the dataset version name and citation are corrected.
