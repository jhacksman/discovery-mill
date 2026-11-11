# Access blockers

Exact missing inputs. Work continues on everything not listed here.

| BLK | What is missing | Why it matters | Exact unblocking input | Workaround in use |
|-----|-----------------|----------------|------------------------|-------------------|
| BLK-001 | **Installers obtained 2026-11-11** (ART-110…): CloudNine's public download page embeds direct links on `software.cloudnine.com`; no form was submitted. Still missing: an activation key, so the products cannot be *launched*. | OBSERVED runtime evidence for LAW export/load-file behavior, numbering, exception handling | A CloudNine evaluation/activation key (Jack to obtain or authorize request). Static inspection (REA) proceeds without it. | Static inspection of installers + DOCUMENTED evidence (ART-001, ART-005, ART-006, ART-007) |
| BLK-002 | ReadySuite 9.0 installer + 14-day trial key | OBSERVED load-file validation behavior; cross-check of DAT/OPT/LFP parsing rules | Jack's authorization to submit the KLDiscovery form with an email address he designates | DOCUMENTED evidence from ReadySuite help (ART-008) |
| BLK-003 | Windows analysis VM | Running any of the above once obtained | Provisioned only after BLK-001/BLK-002 clear (D-006) | — |
| BLK-004 | Sample productions from real LAW/Concordance installations | Byte-level OBSERVED confirmation of DAT/OPT/LFP/DII writer output | Any authorized, confidential-data-free sample production set (vendor training material or a redacted public court exhibit) | Format contracts built from DOCUMENTED sources plus importer-side documentation (Concordance import, ReadySuite import, third-party platform specs), cross-validated for consistency |
