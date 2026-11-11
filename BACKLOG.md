# Backlog

Two item kinds: **RT** (research tasks for this phase) and **REQ** (requirements for the
future application). REQ items gain acceptance criteria and an evidence label as research
lands; an item without both is not first-release-ready. Priorities: P0 first release,
P1 first release if cheap, P2 later. States: pending / in progress / submitted (PR) /
reviewed / merged / blocked / verified.

## Research tasks

| ID | Task | Priority | Depends on | Acceptance | Evidence | PR | State | Next action |
|----|------|----------|------------|------------|----------|----|-------|-------------|
| RT-001 | Research foundation: PROGRAM, BACKLOG, evidence index, environment, artifact catalog, RQs, checkpoint | P0 | — | Files exist; fresh session can resume | EV-009 | this PR | submitted | — |
| RT-002 | Pin and verify REA; record provenance | P0 | — | `rea --version` = 6.8.0, doctor node/host pass | EV-009 | this PR | submitted | revisit engine choice when a binary is held |
| RT-003 | Mirror and hash the LAW and Concordance Answer Centers; record per-file manifest in private workspace | P0 | — | Mirror complete, manifest generated, topic index published | EV-004, EV-005 | — | in progress | finish wget; publish topic index |
| RT-004 | Mirror ReadySuite help topics on import/export/validation | P1 | — | Topic index published | EV-006 | — | pending | |
| RT-005 | Read EV-001/EV-004 and answer RQ-I01…I06 with cited findings | P0 | RT-003 | Findings file with labels | | — | pending | |
| RT-006 | Answer RQ-T01…T05 (imaging/text/numbering) | P0 | RT-003 | Findings file | | — | pending | feeds M3 |
| RT-007 | Answer RQ-P03/P04 (DAT/OPT exact contracts) from Concordance import docs + LAW export docs + ReadySuite; cross-validate | P0 | RT-003, RT-004 | Contract with worked examples, no unresolved ambiguity | | — | pending | feeds M4 |
| RT-008 | Answer RQ-P05 (LFP/DII) and classify | P1 | RT-007 | Classification recorded | | — | pending | |
| RT-009 | Answer RQ-E01…E03 (exceptions, recovery, reprocessing) | P0 | RT-003 | Findings file | | — | pending | feeds M5 |
| RT-010 | Open-source component survey (RQ-S02) with license inventory | P0 | — | Table of candidates per stage with license, maturity, platform | | — | pending | |
| RQ-S03 | Review `jhacksman/librarian` for reusable ingestion/recovery/source-tracing concepts | P1 | — | Short findings note | | — | pending | |
| RT-011 | Original fixture corpus + ground truth + harness (M2) | P0 | — | Corpus generated deterministically by script; ground-truth manifest; harness runs | | — | pending | |
| RT-012 | Request authorization for BLK-001/BLK-002 (vendor forms) | P0 | — | Jack's yes/no recorded | | — | blocked | asked in thread; continue docs work meanwhile |
| RT-013 | Final spec, architecture, dependency inventory, ordered implementation backlog, handoff (M6) | P0 | RT-005…RT-011 | Completion criteria in contract §6 met or blockers named | | — | pending | |

## Requirements (seed; refined by later PRs)

| ID | Requirement | Priority | Depends on | Acceptance criteria | Evidence | RQ | State |
|----|-------------|----------|------------|---------------------|----------|----|-------|
| REQ-ING-001 | Create a case with custodians and sources; every imported item records source path, custodian, import session, and a stable internal identifier | P0 | — | TBD | UNKNOWN | RQ-I01 | pending |
| REQ-ING-002 | Preserve original bytes read-only; record SHA-256 (and MD5 where interoperability requires) at import; never mutate originals | P0 | — | TBD | PROPOSED | RQ-I02 | pending |
| REQ-ING-003 | Expand ZIP, EML, MSG with attachment relationships retained (parent/child, family range) | P0 | — | TBD | UNKNOWN | RQ-I03 | pending |
| REQ-ING-004 | Identify file types by content, not extension; extract a defined metadata field set with declared types and original-value preservation | P0 | — | TBD | UNKNOWN | RQ-I04/I05 | pending |
| REQ-ING-005 | Deduplicate with configurable scope while retaining every source/custodian occurrence | P0 | REQ-ING-002 | TBD | UNKNOWN | RQ-I06 | pending |
| REQ-IMG-001 | Render supported types to page images with configurable resolution/color/compression; record renderer, settings, and per-page provenance | P0 | — | TBD | UNKNOWN | RQ-T02/T03 | pending |
| REQ-TXT-001 | Produce document text with a precedence policy (native → rendered → OCR) and record which source produced each text | P0 | REQ-IMG-001 | TBD | UNKNOWN | RQ-T04 | pending |
| REQ-NUM-001 | Number pages/documents with a configurable prefix/padding scheme; detect collisions before endorsement | P0 | REQ-IMG-001 | TBD | UNKNOWN | RQ-T05/P02 | pending |
| REQ-EXC-001 | Every failed or partial item has an explicit exception record with cause class and remediation state; no silent drops | P0 | — | TBD | UNKNOWN | RQ-E01 | pending |
| REQ-EXC-002 | Imports and batch jobs are cancellable and resumable; reprocessing preserves document identity and history | P0 | REQ-EXC-001 | TBD | UNKNOWN | RQ-E02/E03 | pending |
| REQ-EXP-001 | Export production sets (images, text, natives, metadata) with Concordance DAT and Opticon OPT load files conforming to the documented contracts | P0 | REQ-NUM-001 | TBD | UNKNOWN | RQ-P03/P04 | pending |
| REQ-EXP-002 | Pre-export validation: every referenced image/text/native exists, counts agree, numbering is unique and contiguous; actionable report | P0 | REQ-EXP-001 | TBD | UNKNOWN | RQ-P06 | pending |
| REQ-EXP-003 | LFP / DII export | P1/P2 (to classify) | REQ-EXP-001 | TBD | UNKNOWN | RQ-P05 | pending |
| REQ-SCOPE-001 | PST/MBOX ingestion classification | TBD | — | TBD | UNKNOWN | RQ-S01 | pending |

## Future work (out of defined scope, recorded only)

- AI enrichment (summaries, classification) as an optional, clearly separated layer.
- Hosted/multi-user review.
