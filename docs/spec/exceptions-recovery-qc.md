# Exceptions, recovery, and quality-control requirements

Status: draft specification (REQ-EXC-001, REQ-EXC-002, REQ-EXP-003 and new REQ-QC-001..004; M5). Evidence labels per PROGRAM.md D-004.
Sources: LAW 6.2.46 User Guide (ART-001: *Quality Control After Import*, *Cancelling and Resuming Sessions*, *Session Browser and Session Viewer*, *File Type Manager / Auto Assign Suspect Extensions*, *Compound documents*, *Exclude empty files*, *Reviewing Exceptions* (Early Data Analyzer), *Placeholder text files*); LAW Answer Center (ART-006: *Exception report*, *ED Loader Session Report*, *Deduplication*); LAW 7.14 case model (F-003). Fixtures: `fixtures/corpus/exceptions/*`, `containers/nested-outer.zip`, `custodians/*`. No reference product was executed.

## 1. Exception model (REQ-EXC-001)

| # | Requirement | Label | Source |
|---|---|---|---|
| X1 | Every input item produces exactly one of: a document record, a *filtered* record (excluded by policy: NIST/NSRL, dedup, file-type, date range, 0-byte), or an *exception* record. Nothing is silently dropped; counts reconcile: `items_discovered = records_written + filtered + exceptions_not_written`. Reference report distinguishes items processed (pre-expansion), discovered (post-expansion), written, and not written. | DOCUMENTED (report structure) / PROPOSED (reconciliation invariant) | AC *Exception report* |
| X2 | Exceptions are first-class, per-item records with: `item_id`, `stage` (identify, expand, extract-text, render, ocr, number, export), `class` (see X3), `severity` (`warning` = record written with degraded content; `error` = record written but a stage failed; `commit-error` = record not written), `message`, `previous_message` (kept when re-run), `remediation_state` (`open`, `retried`, `resolved`, `accepted`), `created_by_job`. Reference keeps `ErrorMsg`/`PrevErrMsg` per document and reports processing vs commit errors separately. | OBSERVED (F-003 fields) / DOCUMENTED (error classes) / PROPOSED (state machine) | F-003; AC *Exception report* |
| X3 | Exception classes (minimum): `unsupported-type`, `encrypted` (needs password), `corrupt`, `empty` (0 bytes), `suspect-extension` (content type ≠ extension), `embedded-unopenable`, `extraction-failed`, `render-failed`, `ocr-failed`, `page-limit`, `timeout`, `cancelled`, `container-partial` (archive volume missing / entry unreadable), `path-too-long`, `name-invalid`. Reference exposes encrypted files and corrupted mail stores as monitored exception categories and logs unopenable embedded files as warnings. | DOCUMENTED / PROPOSED (class list) | LAW UG *Reviewing Exceptions*, *Compound documents* |
| X4 | Suspect extensions: content-based identification always runs; when the extension disagrees, the record gets `suspect_ext=true`, keeps `orig_ext`, and (only if the profile enables auto-assign) receives the inferred extension in `doc_ext`. Reference: `SuspectExt=Y`; with auto-assign, `DocExt` rewritten and `OrigExt` recorded. | DOCUMENTED | LAW UG *Auto Assign Suspect Extensions* |
| X5 | Empty files are *recorded* as exceptions (`empty`) by default; a profile option may exclude them from processing, but even then they appear in the filtered count. | DOCUMENTED (exclude option) / PROPOSED (record by default) | LAW UG *Exclude empty files (0 bytes)* |
| X6 | Encrypted/password-protected items are recorded as `encrypted`; operators may supply passwords (per job or per item) and re-run; successful re-run resolves the exception and preserves the original record identity. Reference supports password lists for Office files and recommends re-import with passwords. | DOCUMENTED | LAW UG *passwords for password-protected files*, *Extracting Missing Text* |
| X7 | Placeholder outputs: for a document with no text, exports write a placeholder text file; for a document with no image (native-only or render-failed), the production includes a slip-sheet image whose text names the reason. The placeholder content is a profile value and the fact is recorded on the record (`placeholder_reason`). | DOCUMENTED (placeholder text) / PROPOSED (slip-sheet) | LAW UG *Placeholder text files*; F-003 `Placeholder_Name` |
| X8 | Exception review UI/CLI must list exceptions by class with counts, allow opening the source, tagging, bulk re-queue, and export of the exception list as CSV (reference: *All Exceptions.csv*, Re-Analyze returns the item to the queue while keeping family relationships). | DOCUMENTED | LAW UG *Reviewing Exceptions* |

## 2. Cancellation, resumability, and reprocessing (REQ-EXC-002)

| # | Requirement | Label | Source |
|---|---|---|---|
| R1 | Every long-running operation is a *job* with persisted state; items move `queued → processing → complete|error|cancelled` individually, so a crash leaves at most the in-flight items in `processing`, which are re-queued on resume. Reference OCR uses a `P` (processing) flag so multiple stations can share and recover a batch. | DOCUMENTED (OCR flags) / PROPOSED (generalised) | LAW UG *OCR fields* |
| R2 | Cancel has two modes: **safe** (finish current item, then stop — default) and **immediate** (stop now; in-flight items are marked `incomplete`). | DOCUMENTED | LAW UG *Cancelling and Resuming Sessions* |
| R3 | A cancelled or crashed import session is listed as *cancelled-recoverable* and can be resumed; resume processes only items not yet complete and does not duplicate already-written records. | DOCUMENTED | LAW UG *To resume a session* |
| R4 | Items that failed to commit are reprocessed by an explicit *reprocess* action that reuses the existing item id, keeps the previous error message in `previous_message`, and retains family relationships and ordering (reference *Insert* preserves order; *Re-Analyze* retains family). | DOCUMENTED | LAW UG *Quality Control After Import*, *Re-Analyze* |
| R5 | Document identity (`document_id`, content hashes, custodian, source path, family links) never changes on reprocessing; only derived artifacts (images, text, OCR) are replaced, and the replaced versions are kept until the production that used them is retired. | PROPOSED | — |
| R6 | Loss of the case-store connection pauses jobs and retries reconnection rather than failing items (reference dedup "pauses until the connection is re-established"). | DOCUMENTED | AC *Deduplication* |
| R7 | Timeouts per stage are profile values; a timed-out item becomes an `timeout` exception, the worker is recycled, and the job continues with the next item. | PROPOSED | — |
| R8 | Processing history: each item carries an append-only log of (job, stage, worker/station, start, end, result). Reference records `ImportStation`/`BatchStation` per document. | OBSERVED (F-003) / PROPOSED | F-003 |

## 3. Quality-control workflow (REQ-QC-001..004)

| ID | Requirement | Acceptance criterion | Label |
|---|---|---|---|
| REQ-QC-001 | After every import job a *session report* is produced: items processed/discovered/written/not-written, filter counts by type with post-filter sizes, error counts by severity, warnings list, and the session list. Exportable as CSV/JSON/PDF. | Report totals reconcile with X1 on `fixtures/corpus` (19 files + 7 container entries → N written, 1 empty, 2 corrupt, 1 suspect-extension). | DOCUMENTED (report content) / PROPOSED (formats) |
| REQ-QC-002 | Post-import QC view lists: incomplete/uncommitted items, items with error messages, items without text by text status, suspect extensions, hidden-content documents, page-limited documents. Each list supports bulk re-queue to the relevant stage. | Every exception fixture appears in exactly one list with a remediation action. | DOCUMENTED (reference 3-step QC: session log → ErrorMsg → TextXStatus) / PROPOSED |
| REQ-QC-003 | Image QC: page-level review with rotate/deskew/re-render/replace-image actions that are logged and reversible; page counts, blank-page suppression, and `has_redaction/has_annotation` flags are visible per document. | Rotating page 3 of the G4 fixture records `rotation_applied` and a history entry; original bytes remain. | DOCUMENTED (image cleanup batch; page edits) / PROPOSED |
| REQ-QC-004 | Deduplication QC: a duplicate viewer shows each hash group with every custodian/path occurrence; duplicate relationships can be applied/removed without deleting records; dedup method and scope are recorded per job. | `custodians/avery/report.pdf` and `custodians/blake/Report (1).pdf` form one group with two occurrences; `report-modified.pdf` is not in the group. | DOCUMENTED (Duplicate Viewer, Apply Duplicate Relationships) / OBSERVED (F-003 dup fields) |

## 4. Pre-export validation (REQ-EXP-003, consolidated)

Fail-closed checks before any production file is written: Bates uniqueness (N4), page-count reconciliation, DAT↔OPT key coverage, every referenced native/text/image exists, families complete (parent and all attachments either all in or all explicitly withheld with reason), no open `commit-error` exceptions among selected items, field-name grammar (D6), encoding/BOM per profile. Output: an actionable report with one line per violation (item id, rule id, message) and a non-zero exit. The DAT/OPT portion is implemented by `scripts/loadfiles/validate_dat_opt.py` (PR #4).

## 5. Fixture → expected outcome matrix

| Fixture | Expected class / state | Rule |
|---|---|---|
| `exceptions/zero-byte.pdf` | `empty`, recorded, placeholder on export | X5, X7 |
| `exceptions/corrupt-truncated.pdf` | `corrupt` at render/extract stage; record written; slip-sheet on export | X2, X7 |
| `exceptions/wrong-extension-is-png.pdf` | identified `image/png`; `suspect_ext=true`, `orig_ext=pdf`; rendered as image | X4 |
| `containers/nested-outer.zip` → `inner/empty.txt` | `empty` inside nested container; parent path recorded as `nested-outer.zip?inner/nested.zip?inner/empty.txt` (reference nested-filename notation `archive.zip?file`) | X5; LAW UG *Archives* |
| `containers/nested-outer.zip` → `CON.txt`, `trailing space .txt`, 20-level path | `name-invalid`/`path-too-long` warnings only if the target filesystem rejects them; content still processed under a safe internal name | X3 |
| `email/parent-with-2-attachments.eml` | family of 3; cancelling mid-family then resuming yields exactly 3 records | R3, R4 |
| `custodians/*` | one dup group, two occurrences retained | REQ-QC-004 |

## 6. Unknowns

- UNKNOWN: reference behaviour for a resumed session whose source files changed on disk (not documented). PROPOSED: re-hash and raise `source-changed` exception.
- UNKNOWN: exact exception category names in LAW 7.14 Explore/EDA (6.2 guide shows the UI but not the category list). Low impact — Discovery Mill defines its own classes (X3).
