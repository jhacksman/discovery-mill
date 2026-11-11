# Continuation checkpoint

Updated: 2026-11-11 (session 1). Read `PROGRAM.md` then `BACKLOG.md` before acting.

## State

- Branch/PR: PR #1 `devin/1794403948-research-foundation` (M0) submitted, not merged. PR 2 `devin/1794403948-installer-findings` (stacked on PR #1) adds findings F-001..F-003 + EV-011..014. PR #3 `devin/1794403948-fixtures-harness` (base main, independent) adds fixture corpus + verifier + CI. PR #4 `devin/1794403948-loadfile-contracts` (stacked on #3) adds DAT/OPT contract + validator. Nothing merged yet.
- Private workspace on the research machine: `~/discovery-mill-private/` (REA env, PDFs,
  Answer Center mirrors). If the machine is gone, rebuild with
  `scripts/research/fetch-public-docs.sh` and the wget commands in
  `docs/research/environment.md`; the mirrors are public sites.
- Jack (2026-11-11) authorized acquiring binaries from the open internet. LAW 7.14 and
  Concordance 10 installers were found as direct links on CloudNine's own download page and
  are in the private workspace (`acq/installers/`, see artifact catalog ART-110…113).
  Remaining: activation key to *launch* (BLK-001), ReadySuite installer (BLK-002, form-only),
  Windows VM (BLK-003, now justified: provision next).

## Exact next action

0c. DONE 2026-11-11: PR #4 DAT/OPT contract submitted. NEXT (PR 5, branch from fixtures-harness): docs/spec/imaging-text-contract.md — page image contract (TIFF G4 bitonal default, JPEG colour, DPI, rotation, page naming), text precedence NATIVE→RENDERED→OCR with per-page provenance, Office rendering options (comments, hidden text, print areas, notes), endorsement/numbering contract; cite LAW UG TIFF Conversion/OCR/Endorse topics + F-001/F-003. Then PR 6 exceptions/QC, PR 7 handoff.
0b. DONE 2026-11-11: PR #2 findings F-001..F-003 and PR #3 fixtures submitted. (PR 4 plan was: branch from main): docs/spec/loadfiles/ — DAT/OPT contract (delimiters 0x14/0xFE/0xAE, UCS-2/UTF-8 BOM rules, 12-char field names, OPT 7-field lines, Y breaks, path notation) with worked examples generated from fixtures/corpus by scripts/loadfiles/render_example.py, plus scripts/loadfiles/validate_dat_opt.py; cite EV-004/005 + F-002 templates; then PR 5 imaging/text contract (F-001/F-003), PR 6 exceptions/QC, PR 7 handoff.
0. DONE 2026-11-11: all four installers hashed, extracted (7-Zip/unshield), REA `inspect-artifact`/`inspect-managed-artifact` run; private NOTES-session1.md holds component inventory. NEXT: write sanitized findings (LAW/Concordance component + dependency inventory, LAW case-schema entity list, Concordance sample DB/template formats) under docs/research/findings/, then PR 2 (artifact catalog + findings).
0a. (superseded) run REA `inspect-desktop-application`/`inspect-artifact`
   on `LAW_7.14.290.exe` and the Concordance installer (output stays in private
   `raw-analysis/`); publish only sanitized component/version inventory.
1. Finish Answer Center mirrors (done: 609 + 458 files, manifests in private workspace); generate per-file sha256 manifests in the private
   workspace; publish topic indexes (RT-003).
2. Start RT-005/RT-007 reading (LAW export topics `exporting.htm`, `concordance2.htm`,
   `export_utility_overview.htm`; Concordance `managing-data-files.htm`, import topics) and
   write `docs/research/findings/` files with EV citations and labels.
3. Begin RT-011 fixture corpus generator in parallel (deterministic Python, synthetic content
   only).

## Continuation prompt (for a fresh session)

> Resume the Discovery Mill investigation phase in jhacksman/discovery-mill. Read
> PROGRAM.md, BACKLOG.md, CHECKPOINT.md, docs/research/. Check open PRs and branches first.
> Continue from "Exact next action" in CHECKPOINT.md, keep the clean-room rules in
> PROGRAM.md, and update BACKLOG.md/CHECKPOINT.md in every PR.
