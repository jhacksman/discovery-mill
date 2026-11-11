# Evidence index

EV-IDs are cited by findings (`docs/research/findings/`), requirements (`BACKLOG.md`,
`docs/spec/`), and the artifact catalog. "Public" means a future implementer may consult
the source directly; "private" means only this index and derived sanitized findings are
published.

| EV | Kind | Source | Artifact | Public? | Notes |
|----|------|--------|----------|---------|-------|
| EV-001 | Vendor manual | *Using LAW PreDiscovery* User Guide, v6.2.46 | ART-001 | yes (archive.org) | Primary DOCUMENTED source for LAW 6.x processing behavior |
| EV-002 | Vendor manual | LAW PreDiscovery Getting Started Guide (5.x) | ART-002 | yes | Install, case creation, TIFF conversion walkthrough; evaluation limits (30 launches, 100 docs/case) |
| EV-003 | Vendor manual | Concordance 10.22 Installation Guide | ART-005 | yes | Component versions, prerequisites |
| EV-004 | Vendor help site | CloudNine LAW Answer Center (7.x) | ART-006 | yes | Topic-level citations use the topic file name, e.g. `EV-004:exporting.htm` |
| EV-005 | Vendor help site | CloudNine Concordance Answer Center | ART-007 | yes | Topic-level citations as above, e.g. `EV-005:managing-data-files.htm` |
| EV-006 | Vendor help site | ReadySuite help | ART-008 | yes | Topic-level citations by URL |
| EV-007 | Vendor web page | CloudNine Software Download page (version list, access conditions) | ART-101/102 | yes | Captured text 2026-11-11 |
| EV-008 | Vendor web page | KLDiscovery ReadySuite download page (version, release date, access conditions) | ART-103 | yes | Captured text 2026-11-11 |
| EV-009 | Tool provenance | REA `rea-agents@6.8.0` npm metadata and `rea doctor --json` output | — | yes | See `environment.md` |
| EV-010 | Vendor product sheets | LAW / EDA+LAW product sheets | ART-003/004 | yes | Marketing-level; used only for scope context |
| EV-011 | Static artifact inspection | LAW 7.14.290 installer: bundle manifest, MSI payload inventory, PE version resources, Authenticode chain | ART-110 | hashes yes; raw listings private | Findings F-001, F-003; no execution |
| EV-012 | Static artifact inspection | LAW 7.14 schema-manager assembly: embedded case-schema resources (entity/field names only published) | ART-110 | private | Finding F-003; script text not published |
| EV-013 | Static artifact inspection | Concordance 10.26.1.153 setup: extracted component list, sample database file set, shipped field templates | ART-111 | private | Finding F-002; 17/364 entries not extracted |
| EV-014 | Static artifact inspection | Concordance Desktop 1.9.1.6 / FYI Reviewer 5.19.0.40: hashes and signer metadata only | ART-112/113 | private | Low relevance; not analysed further |

