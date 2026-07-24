# Preregistration Amendment 8

**Status:** binding on commit. Made before any CIC-IDS2017 coverage number is computed. Timing evidence in A8.7.
**Scope:** corrects errors in Amendment 6 and in the notebook 09 taxonomy, all identified by reading the exact hashed files rather than the source literature. Supersedes the affected lines of Amendments 5 and 6. Changes no NSL-KDD result and no CIC analysis decision except the two the files force.

The corrections in this amendment were prompted by a structural audit of the actual parquet files. Several statements in Amendment 6 were imported from the CNS-2022 and WTMC-2021 papers and did not match the acquired artifact. The controlling record is the file contents, reported in `reports/cicids2017_compatibility.json`.

---

## A8.1 Attempted flows: policy corrected to match the artifact

The acquired artifact has a single `Label` column with 17 values and no `Attempted Category` column. All 8,966 attempted flows carry one label, `Attempted-relabel-as-Benign`, with no parent attack family attached. The per-family `X - Attempted` labels of the official CNS release are not present; the mirror collapsed them. Parent identity is therefore not recoverable from this artifact.

Consequences:

- Amendment 5 A5.1 specified excluding attempted rows in the primary and merging them into the parent family in sensitivity. The merge-to-parent sensitivity **cannot be implemented** on this artifact and is **withdrawn**.
- Amendment 6's statement that this is simply "attempted-attack flows relabelled to benign" was a simplification; the accurate statement is that the mirror relabelled them to a single benign-tagged label without preserving family.

**Decision.**
- **Primary:** the 8,966 `Attempted-relabel-as-Benign` flows are retained as Benign. This matches the artifact's own labelling and the release authors' explicit recommendation to treat payload-absent attack attempts as benign.
- **Sensitivity (replaces the withdrawn merge):** exclude the 8,966 flows entirely. This is implementable because they carry a distinct label, and it confirms the results do not hinge on their inclusion.

The flows are flagged in the data as `attempted_relabelled_benign` for auditability.

---

## A8.2 Infiltration port-scan taxonomy corrected

The files contain two distinct scan labels: `Infiltration - Portscan` (5,485 rows, all Thursday, the NMAP scan phase of the infiltration scenario) and `Portscan` (1,683 rows, all Friday, the standalone PortScan attack). The first notebook 09 mapping folded `Infiltration - Portscan` into the PortScan family, which merged a Thursday attack into a Friday family and overrode the authors' own label.

**Decision, corrected mapping:**

```
Infiltration - Portscan   ->  family = Infiltration,  subtype = Infiltration-NMAP-Portscan
Portscan                  ->  family = PortScan,      subtype = Friday-PortScan
```

A unit test in notebook 09 asserts that these two never collapse into one family and that each remains day-pure (infiltration scan Thursday only, PortScan Friday only). The test must pass before any downstream artifact is written.

**Feasibility impact, recorded.** With the correction, Infiltration becomes 36 + 5,485 = 5,521 rows and is feasible at alpha = 0.05; PortScan becomes 1,683 rows and remains feasible. The excluded rare-attack set is therefore **Web Attack (104) and Heartbleed (11)**, not the three families named earlier. This does not change the Amendment 7 focal class, which is DoS within Wednesday and does not involve Thursday or Friday families.

---

## A8.3 FIN and RST feature wording corrected; treated as diagnostic, not defect

Amendment 6 described the CICFlowMeter change as symmetric and called the resulting flag counts anomalous. Both are corrected.

**Correct wording.** The corrected CICFlowMeter no longer terminates a TCP flow after the first FIN; it waits for mutual FIN exchange. In contrast, an RST is no longer ignored and now terminates the flow. The CNS version also adds directional RST-related features (`Fwd RST Flags`, `Bwd RST Flags`). These changes can alter the distribution and interpretation of FIN/RST-derived features relative to the original CICFlowMeter output.

**Diagnostic, not defect.** The corrected data can contain FIN/RST count values above one. That observation alone does not establish that the values are erroneous, anomalous, or caused by the termination change; they may reflect long flows, repeated control packets, counting behaviour, timeout behaviour, attack-specific traffic, or extraction artifacts. Before model fitting, the ranges, quantiles, class association and day association of `FIN Flag Count`, `RST Flag Count`, `Fwd RST Flags` and `Bwd RST Flags` are reported. No feature is removed solely because of this observation.

**Preregistered sensitivity.** The primary model uses the ordinary eligible feature set. A sensitivity model excludes `FIN Flag Count`, `RST Flag Count`, `Fwd RST Flags` and `Bwd RST Flags`. This is fixed now to avoid selecting features after seeing coverage.

---

## A8.4 Two-layer provenance

The version of record has two layers, both recorded.

**Scientific lineage.** The IEEE CNS 2022 corrected release: Liu, L., Engelen, G., Lynar, T., Essam, D., Joosen, W. (2022). Error Prevalence in NIDS Datasets: A Case Study on CIC-IDS-2017 and CSE-CIC-IDS-2018. IEEE CNS 2022, pp. 254-262. This descends from Engelen et al. (2021), WTMC-2021.

**Exact acquired artifact.** The D'Hooge Kaggle V5 cleaned-parquet derivative of that release: owner/slug `dhoogla/distrinetcicids2017`, Kaggle version V5, five per-day parquet files, acquired 2026-07-24, SHA-256 per file in `reports/dataset_hashes.json`. The mirror performed type coercion, missing-value and duplicate removal, parquet conversion, and a label transformation that collapsed the per-family `X - Attempted` labels into a single `Attempted-relabel-as-Benign` label. The hashes identify the bytes; this paragraph records the transformations that produced them.

The Drive folder name `cicids2017-wtmc2021` is a path only and does not assert the version.

---

## A8.5 Bibliographic note

Page range 254-262 is used, consistent with the authors' project page, the GitHub citation, and DBLP. Some institutional metadata lists 254-263. The DOI is the authoritative identifier; the final page range follows the IEEE bibliographic export. No experimental time is spent on this.

---

## A8.6 Amendment 5 "unchanged" claim, qualified

Amendment 6's statement that all Amendment 5 decisions remain unchanged is withdrawn as stated and replaced by this record, made after confirming compatibility against the files:

- A5.1 Attempted policy: amended by A8.1.
- A5.2 taxonomy: corrected by A8.2 for the two scan labels; the family/subtype principle is otherwise intact.
- A5.3 and Amendment 7 ladder: structurally unchanged; feasibility inputs updated by A8.2.
- Feasibility inventory: updated; excluded rare set is now Web Attack and Heartbleed.
- Focal-class rule (section 12) and Amendment 7 focal environment: unchanged; focal class remains DoS within Wednesday, computed in notebook 10.

`reports/cicids2017_compatibility.json` records rows per day, per family, per subtype, the attempted count, the feasibility projection at alpha = 0.05, and the projected focal family, generated from the hashed files before any coverage.

---

## A8.7 Timing, backed by commit hashes

- Acquisition commit (notebook 09, first CIC data in repo): `d057f5b`
- Prior amendment commits: `c21ce51` (A5), `6ed7f6a` (A6)
- First modelling or coverage commit: none exists at the time of this amendment; `reports/` contains no `*_cicids2017` coverage file.

This amendment and the corrected notebook 09 are committed together; their hash is recorded on commit.

---

## A8.8 Unchanged

The base preregistration sections 4 to 15, all NSL-KDD results, and Amendment 7's ladder structure are unchanged except where A8.1 to A8.6 state otherwise.
