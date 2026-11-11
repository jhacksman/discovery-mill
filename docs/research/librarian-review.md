# Review: reusable concepts from jhacksman/librarian (ingest pilot)

Reviewed 2026-11-11 at a shallow clone of `main` (MIT). Scope: `ingest/READINESS.md`, `ingest/COVERAGE-POLICY.md`, `ingest/src/ingest/local/schema.py`. Conclusion: the *architecture* (book/chunk search index with LLM agents) does not fit Discovery Mill; several *recovery and source-tracing rules* do and are adopted below as PROPOSED requirements.

| Librarian rule (OBSERVED in docs/schema) | Adopt? | Discovery Mill mapping |
|---|---|---|
| Per-file JSON outcome; continue past malformed inputs; exit 1 if any failed; each successful item commits independently | yes | REQ-EXC-001 X1/X2; job exit status semantics |
| Resume state lives in the SQLite store (`ingest_state`: source path, sha256, pipeline version, status completed/failed, attempts, error), not a separate checkpoint file; a crash before commit leaves no success receipt so rerun retries | yes | REQ-EXC-002 R1/R3: item state table in the case store; `attempts` counter; no sidecar checkpoint files |
| Skip rule = same SHA-256 **and** pipeline version **and** completed receipt **and** source path **and** expected output count; `--force` reparses | yes | Reprocess/skip predicate for imports and renders (adds pipeline/profile version to identity of derived artifacts) |
| Cited hash covers the exact parsed bytes; original filenames kept in citations, temp names never enter the index; changed bytes create a new version and old versions are retained; identical bytes are one item with the last source path | partly | Hash-of-original invariant and version retention adopted (REQ-ING-002, R5). *Not* adopted: collapsing identical bytes to one record — discovery must keep every custodian/path occurrence (REQ-ING-005) |
| Bounded private temporary snapshot for parsing (size cap), no execution or rewriting of sources | yes | Isolation requirement: parse from a read-only copy; per-stage size/time bounds (R7) |
| Schema guarded by application id + user_version; unknown versions fail before modification; migration requires explicit backup; online backup API with integrity + count verification | yes | Case-store schema versioning and backup/restore requirements (spec §Integrity) |
| Recorded extraction omissions (`pages_without_text`) surfaced as `page_omissions: reported|unknown`, `completeness: not_assessed`; never infer coverage without total page count | yes | Text contract T1–T3: per-page text provenance; a document's text completeness is `reported` only when every page has a source, else `unknown` |
| Failure isolation does **not** sandbox native parsers or enforce CPU time (stated limitation) | note | Discovery Mill must run renderers/OCR in worker subprocesses with timeouts (R7) — a stated gap in librarian |
| Validation only via a pinned coordinator; no GitHub Actions | no | Discovery Mill uses GitHub Actions on the public repo |
