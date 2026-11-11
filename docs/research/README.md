# Research method

## Evidence labels

Every finding and every requirement carries exactly one label:

| Label | Meaning |
|-------|---------|
| OBSERVED | Reproduced at runtime or by direct inspection of an artifact we hold, with a recorded fixture, configuration, steps, and output. |
| DOCUMENTED | Stated by official vendor documentation, manuals, release notes, or a format specification we hold (hash recorded). |
| INFERRED | Derived from DOCUMENTED/OBSERVED evidence plus reasoning; the reasoning is written down. Decompiler output alone is INFERRED, never OBSERVED runtime behavior. |
| PROPOSED | Our design choice where the reference products do not constrain behavior or where we deliberately diverge. |
| UNKNOWN | Needed but not established; the missing input is named in `access-blockers.md` or the finding. |

## Finding record

Each finding (in `findings/`) records: research question ID, exact target product and
version, fixture and configuration, reproduction steps and output artifacts (private
paths plus hashes where the artifact cannot be published), evidence source (EV-ID), result,
limitations, and label.

## Files

- `environment.md` — research machine, REA pin and provenance, tool versions.
- `artifact-catalog.md` — every reference artifact with provenance, hashes, and distinct
  downloaded / extracted / installed / launched / tested statuses.
- `evidence-index.md` — EV-IDs that findings and requirements cite.
- `research-questions.md` — RQ-IDs covering the contract's investigation areas.
- `access-blockers.md` — exact missing access, artifact, credential, dependency, or decision.
- `findings/` — one file per finding cluster (added by later PRs).
