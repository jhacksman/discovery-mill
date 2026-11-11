# Continuation checkpoint

Updated: 2026-11-11 (session 1). Read `PROGRAM.md` then `BACKLOG.md` before acting.

## State

- Branch/PR: research-foundation PR (M0) submitted; nothing merged yet.
- Private workspace on the research machine: `~/discovery-mill-private/` (REA env, PDFs,
  Answer Center mirrors). If the machine is gone, rebuild with
  `scripts/research/fetch-public-docs.sh` and the wget commands in
  `docs/research/environment.md`; the mirrors are public sites.
- Open blockers: BLK-001 (CloudNine installers), BLK-002 (ReadySuite installer) — both need
  Jack's authorization to submit vendor forms. BLK-003/004 follow from them.

## Exact next action

1. Finish Answer Center mirrors; generate per-file sha256 manifests in the private
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
