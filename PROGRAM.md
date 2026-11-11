# Discovery Mill — Program

Durable program state for the investigation and specification phase. A fresh session
must be able to resume from this file, `BACKLOG.md`, and `CHECKPOINT.md` alone.

## Objective

Produce an evidence-backed, implementation-ready specification for an independent,
open-source, local discovery-processing application whose central workflow is:

> Import discovery → preserve originals → inventory and extract metadata → render
> documents into page images → extract text/OCR → quality-control → number and endorse
> pages → export validated production sets (images, text, metadata, natives, load files).

Reference products: **LAW / LAW PreDiscovery** (CloudNine; historically LexisNexis;
originally Legal Access Ware) is the primary processing reference. **Concordance** is the
reference for downstream review and import/export interoperability. **ReadySuite** and
other competitors are consulted only where they resolve a concrete gap.

Public-benefit objective: reliable local discovery processing for legal-aid organizations,
public defenders, small firms, journalists, and other teams with limited software budgets.

## Phase and separation rule

This phase is **investigation and specification only**. Implementation happens in
separate, fresh sessions that receive only:

- the sanitized specification (`docs/spec/`),
- approved original fixtures and acceptance tests (`fixtures/`, `docs/spec/acceptance/`),
- public references (`docs/research/evidence-index.md` entries marked public),
- the open-source dependency inventory.

They must not inherit this investigation's chat history or raw analysis workspace.
Vendor binaries, raw disassembly/decompiler output, extracted code, copied assets, and
internal implementation analysis stay outside the repository in the private workspace
described in `docs/research/environment.md`. The repository publishes an artifact index
with provenance and hashes, never the artifacts themselves.

## Scope

In scope for the specification (first release boundary is defined in `docs/spec/scope.md`
once drafted; until then, the candidate boundary is):

- Inputs: loose files and folders, ZIP, PDF, TIFF, JPEG/PNG, common Office (DOCX/XLSX/PPTX
  and legacy DOC/XLS/PPT), EML and MSG with attachments. PST/MBOX and other legacy
  containers are evaluated and explicitly classified as first-release or later.
- Processing: case creation, custodian/source tracking, original-byte preservation with
  hashes, inventory and metadata extraction, file-type identification, family
  relationships, deduplication, rendering to page images, native/rendered text and OCR,
  exceptions and recovery, numbering and endorsement, QC.
- Output: production sets with images, text, natives, metadata, and load files. Concordance
  DAT and Opticon OPT are priority formats; LFP and DII where justified by evidence.

Explicit non-goals (will be restated in `docs/spec/scope.md`):

- Hosted review platform, predictive coding, analytics, or AI enrichment as part of the
  authoritative pipeline (AI enrichment is optional and separate).
- Bit-identical renderer output versus any reference product; functional and
  interoperability equivalence is the target.
- Reproducing proprietary internal algorithms or code structures.

## Material decisions

| ID | Decision | Rationale | Date |
|----|----------|-----------|------|
| D-001 | Private workspace for acquisition and raw analysis is `~/discovery-mill-private/` on the research machine, outside the repository; the repo carries only indexes, hashes, and sanitized findings. | Contract §1/§4 clean-room requirement. | 2026-11-11 |
| D-002 | REA is pinned to `rea-agents@6.8.0` (npm, exact) with Node.js v24.22.2 verified against nodejs.org SHASUMS256. | Latest tagged release at session start; REA's engine check rejects the machine's stock Node 24.19.0. | 2026-11-11 |
| D-003 | Evidence labels are exactly OBSERVED, DOCUMENTED, INFERRED, PROPOSED, UNKNOWN, applied per finding and per requirement. | Contract §3. | 2026-11-11 |
| D-004 | Official vendor documentation (CloudNine Answer Centers for LAW and Concordance, LexisNexis-published LAW PreDiscovery manuals, KLDiscovery ReadySuite help) is the primary DOCUMENTED evidence source. Runtime/decompilation evidence is pursued only where installers can be obtained without bypassing vendor access controls. | All current installers are gated behind vendor contact forms and activation keys (see `docs/research/access-blockers.md`). | 2026-11-11 |
| D-005 | No vendor forms are submitted and no vendors are contacted without Jack's explicit authorization. | Contract §2. | 2026-11-11 |
| D-006 | Windows analysis environments are provisioned only once a runnable reference installer is in hand; documentation research does not need one. | Avoids spending compute before an unblocked use exists. | 2026-11-11 |

## Milestones

| ID | Milestone | Status |
|----|-----------|--------|
| M0 | Research foundation: program state, backlog, evidence index, environment, artifact catalog, research questions | submitted (this PR) |
| M1 | Artifact and version catalog complete for LAW, Concordance, ReadySuite documentation; access matrix final | in progress |
| M2 | Original fixture corpus with ground truth + reproducible harness | pending |
| M3 | Imaging and text-extraction behavior/contract | pending |
| M4 | Load-file and production interoperability (DAT/OPT, LFP/DII as justified) with worked examples and validators | pending |
| M5 | Exceptions, recovery, QC requirements | pending |
| M6 | Final specification, architecture, dependency/license inventory, ordered implementation backlog, clean-room handoff | pending |

## Session settings (reported, not asserted as changed)

- Session started by the user with `!ultra`. The mode selector is user-side; this session
  has no separate reasoning-effort control it can read or set, so none is claimed.
- No native persistent-goal mechanism exists in this environment beyond the session task
  list; persistence is implemented with this file, `BACKLOG.md`, and `CHECKPOINT.md`.
- No automations or scheduled sessions are created.

## Status

See `CHECKPOINT.md` for the exact next action and `BACKLOG.md` for per-item state.
States are reported separately as: submitted (PR open), reviewed, merged, blocked, verified.
