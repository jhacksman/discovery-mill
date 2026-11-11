# Discovery Mill — specification index and first-release definition

Version 0.1 (research phase output). This document binds the component contracts into one specification for a fresh implementation session. Evidence labels per PROGRAM.md D-004; every requirement's evidence class is in BACKLOG.md.

## 1. Scope and non-goals

**First release (R1) completes one useful workflow end to end, locally, on one machine:**
import loose files, folders, ZIP, EML/MSG with attachments, PDF, TIFF, JPEG/PNG, DOCX/XLSX/PPTX (and legacy DOC/XLS/PPT via the same converter) → preserve originals and hashes → inventory + metadata → render page images → extract/OCR text → QC and exceptions → Bates numbering + endorsement → export Concordance DAT + OPT with images, text, natives, validated before writing.

**Deferred (R2+), evaluated and classified:** PST/OST and MBOX mail stores (R2 — needs `libpff`/`readpst`-class dependency and large-store resumability tests); LFP/DII/other load files (R2); NSF, legacy WordPerfect/Lotus, CAD, forensic images (later); near-duplicate and e-mail threading (R2); distributed multi-machine processing (later); review UI, redaction, privilege logging (non-goal — Concordance/other review tools are the downstream); AI enrichment (optional plugin, never in the authoritative pipeline; outputs are marked `generated`).

**Non-goals:** case review platform, cloud/multi-tenant service, compatibility with proprietary case databases (DCB, LAW SQL/Access cases), byte-identical renderer output.

## 2. Reference products, versions, and access (M1)

| Product | Version held | Access | Status | Used for |
|---|---|---|---|---|
| CloudNine LAW | 7.14.290 installer (ART-110) | public URL, signed | downloaded, extracted, statically inspected; **not installed/launched** (activation key) | component model, case data model, field catalog (F-001, F-003) |
| LAW PreDiscovery User Guide | 6.2.46 (ART-001) + 7.x Answer Center (ART-006) | public | read | DOCUMENTED behaviour throughout |
| Concordance | 10.26.1.153 installer (ART-111) + Answer Center (ART-007) | public | downloaded, partially extracted, inspected; **not installed** | DAT/OPT contract, templates (F-002) |
| Concordance Desktop / FYI Reviewer | 1.9.1.6 / 5.19.0.40 | public | hashed only | — |
| ReadySuite | — | vendor form only | **not acquired** (BLK-002) | gap check deferred |

## 3. Workflow and behaviour matrix

| Stage | Contract | Key rules |
|---|---|---|
| Import / preserve | BACKLOG REQ-ING-001..005; F-003 | originals copied read-only, SHA-256 + MD5, source path + custodian + session per item; containers expanded recursively with `archive.zip?member` notation; e-mail families; dedup keeps every occurrence |
| Identify / metadata | REQ-ING-004; exceptions X4 | content-based type; declared field set with split date/time + timezone; suspect-extension handling |
| Render | `imaging-text-contract.md` §1–2 | G4 TIFF 300 dpi default; Office options with disclosure-complete defaults; blank-page policy; page records |
| Text | `imaging-text-contract.md` §3 | extracted / rendered / OCR tracked separately; status alphabet; `TEXTSOURCE` |
| QC / exceptions | `exceptions-recovery-qc.md` | reconciliation invariant; exception classes; cancel/resume; QC lists |
| Number / endorse | `imaging-text-contract.md` §4 | page-level Bates; fail-closed on collision; endorse on a copy |
| Export | `loadfiles/dat-opt-contract.md`; `validate_dat_opt.py` | DAT/OPT rules D1–D12, O1–O9; pre-export validation §3 |

## 4. Data model and state machine (PROPOSED, informed by F-003 and librarian review)

Entities: `Case`, `Custodian`, `Source` (path/media + session), `ImportSession`, `Item` (one per discovered file/message; parent link + depth; original blob ref; hashes; identification; metadata JSON), `Document` (production-facing view of an Item; family id; Bates range per production), `Page` (per rendered page; see I8), `TextArtifact` (per document × source ∈ {extracted, rendered, ocr}; status; path; hash), `Exception` (X2), `Job` / `JobItem` (R1), `Production` (profile, volume, Bates allocation, validation report), `ProductionItem`, `AuditEvent` (append-only).

Item state: `discovered → preserved → identified → (filtered | exception | ready) → rendered? → texted? → qc → numbered → produced`. Each derived-artifact stage records `pipeline_version` + `profile_hash`; skip predicate = same input hash + pipeline version + profile hash + completed status (librarian rule).

Store: single SQLite file per case with `application_id` + `user_version`; migrations explicit with verified backup; one writer, N read-only workers; blobs on disk under the case directory with hash-named paths.

## 5. Independent architecture (PROPOSED)

Core: Python 3.12 service `dm-core` (case store, job queue, pipeline orchestrator) with worker subprocesses per stage (identify, render, ocr, text) communicating through the SQLite job table; CLI `dm` for all operations; optional local web UI (FastAPI + HTMX) for QC. Renderers and OCR run in short-lived subprocesses with timeouts and memory limits; a worker crash converts in-flight items to `timeout`/`render-failed` exceptions. Plugins: converters (LibreOffice), rasterisers (pdfium), OCR (Tesseract), identifiers (libmagic/Siegfried), mail parsers. AI enrichment is a separate optional process writing to `generated_*` tables only.

## 6. Dependency and license inventory (candidates; verify licence text at pin time)

| Need | Candidate | Licence | Note |
|---|---|---|---|
| File identification | `python-magic`/libmagic; Siegfried (PRONOM) | BSD-2 / Apache-2.0 | both content-based |
| Metadata extraction | Apache Tika (server) or `exiftool` | Apache-2.0 / GPL-1+/Artistic (subprocess) | Tika also gives text for many types |
| Office → PDF | LibreOffice headless (`soffice --convert-to pdf`) | MPL-2.0 | options via filter params; hidden-text/notes handling must be verified against the fixtures |
| PDF rasterise/text | pypdfium2 (pdfium) | Apache-2.0 / BSD-3 | avoids AGPL (MuPDF, Ghostscript) in-process |
| PDF repair/inspection | qpdf / pikepdf | Apache-2.0 / MPL-2.0 | |
| TIFF/JPEG/PNG | Pillow + libtiff | HPND / libtiff | G4 write supported |
| OCR | Tesseract 5 (`pytesseract` or `tesserocr`) | Apache-2.0 | eng + selectable packs |
| E-mail | stdlib `email`; `extract-msg` for MSG | PSF / GPL-3 (check: isolate as subprocess or pick `olefile`+own MAPI parser, MIT) | MSG licence decision needed before R1 |
| Archives | stdlib `zipfile`, `py7zr`, libarchive | PSF / LGPL-2.1 / BSD | encrypted archives → exception |
| Hashing / store | hashlib, SQLite | PSF / public domain | |
| PST (R2) | libpff / readpst | LGPL-3 / GPL-2 (subprocess) | deferred |
| Load files | own writer/validator (PR #4) | project licence | |

## 7. Integrity, audit, isolation, recovery

Originals read-only and hash-verified on every read; every write is attributable (`AuditEvent`: who/which job, when, what); derived artifacts versioned; parsers run on copies in subprocesses with bounds; backup/restore verified by integrity check and counts; schema version guard (librarian rule); exports never overwrite existing volume directories.

## 8. Ordered implementation backlog (PR-sized)

1. Repo skeleton, `dm` CLI, case store schema + migrations + backup/restore, fixture verifier wired into CI.
2. Import: walk sources, preserve originals, hash, custodian/session, ZIP expansion with `?` notation; exception records; session report (REQ-ING-001..003, X1–X5, REQ-QC-001).
3. Identification + metadata (libmagic/Siegfried + Tika), suspect extension, dates with timezone (REQ-ING-004, X4).
4. E-mail families (EML, MSG) with attachments and threading fields (REQ-ING-003).
5. Dedup with occurrence retention + duplicate viewer data (REQ-ING-005, REQ-QC-004).
6. Rendering: PDF/TIFF/images → page records (I1–I8); Office via LibreOffice with option matrix (§2 of imaging contract) verified on DOCX/XLSX fixtures.
7. Text: extraction, rendered-text capture, OCR with per-page status and `TEXTSOURCE` (T1–T9).
8. Jobs: cancel/resume, timeouts, reprocess, processing history (R1–R8).
9. Numbering + endorsement (N1–N7).
10. Export: DAT/OPT writer using the validator as a gate, natives/text/images layout, placeholder/slip-sheets (D1–D12, O1–O9, §4 validation).
11. QC web UI (REQ-QC-002/003).
12. Acceptance suite: all §5 criteria across contracts run against `fixtures/corpus`; interrupted-processing harness.
R2 backlog: PST/MBOX, LFP/DII, near-dup/threading, ReadySuite gap review.

## 9. Remaining uncertainties and external blockers

- BLK-001 LAW / Concordance activation keys → no runtime OBSERVED evidence; UNKNOWNs listed in each contract (UTF-8 DAT acceptance, page-count disagreement handling, 7.14 default DPI/colour reduction, field type codes 8/10/11, status-letter semantics beyond documented sets).
- BLK-002 ReadySuite installer/trial key (vendor form only; no form submitted).
- BLK-003 Windows runtime VM — only useful once BLK-001 is resolved.
- Licence decision for MSG parsing (GPL `extract-msg` vs MIT alternative) before R1 item 4.
