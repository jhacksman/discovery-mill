# Research environment

Recorded 2026-11-11. Values are what was observed on the research machine; nothing below is
a requirement of the future application.

## Host

| Item | Value |
|------|-------|
| OS | Ubuntu 22.04 (x86_64), 8 vCPU, 31 GiB RAM |
| Locale / timezone | `C.UTF-8` / UTC (set explicitly for every experiment that touches dates; recorded per finding) |
| Stock Node.js | v24.19.0 (rejected by REA's engine check, see below) |
| Pinned Node.js for REA | v24.22.2, tarball `node-v24.22.2-linux-x64.tar.xz` from nodejs.org, SHA-256 verified against `SHASUMS256.txt`, installed under `~/.local/node/` |
| Java | OpenJDK 17.0.19 (Ghidra 12.1.x would need JDK 21; not installed — no native target yet, see D-006) |
| Document tools | poppler `pdftotext`/`pdfinfo`, `tesseract`, ImageMagick `convert` present; LibreOffice, Ghostscript, qpdf, libtiff tools absent at session start |
| `ps` | procps-ng 3.3.17 (REA's Linux owned-process prerequisite) |

## REA (Reverse Engineer Anything)

| Item | Value |
|------|-------|
| Project | https://github.com/morluto/rea · https://rea.tools/ |
| Pinned release | `rea-agents@6.8.0` (GitHub release `rea-agents-6.8.0`, 2026-10-25; latest at session start) |
| Install | `npm install --save-exact rea-agents@6.8.0` in `~/discovery-mill-private/rea-env/` (outside the repo) |
| npm integrity | `sha512-9QDeRnGqEDzABZyr04eLnBXBv/c6I9/TWu/6M0MD4pEfkySI/BIgwTODIbAReX3C1x6hjw9+Jlx4A2yUSPZ9ww==` |
| npm shasum | `6a2cc197e4ff7f11ba937125b3ca7e4de939906a` |
| Tarball | https://registry.npmjs.org/rea-agents/-/rea-agents-6.8.0.tgz |
| Engine requirement | Node `^22.23.4 || ^24.22.1 || >=26.12.1` |
| Upstream checkout inspected | `morluto/rea` main @ `40d9f1a5e84b6985811d20cff030a192c23bbb2c` (docs only; not used to run REA) |
| CLI verification | `npx rea --version` → `6.8.0`; `npx rea doctor --json` → node/host checks pass with Node 24.22.2; `healthy:false` only because no deep-analysis engine (Hopper/Ghidra/IDA/JADX/Kuna) is configured and the bundled skill is not installed into an agent |
| MCP | REA ships an MCP server (`rea-agents` registers it via `rea setup`). Not registered with an agent in this environment; the CLI exposes the same workflows and Evidence contracts, which is what this research uses. Registration is re-evaluated if agent-driven analysis becomes useful. |

### Capabilities relevant to the expected targets

REA 6.8.0 CLI commands relevant to Windows desktop products (from `rea --help`):
`inspect-desktop-application`, `inspect-artifact`, `inspect-binary-layout`,
`inspect-pe-imports`, `inspect-pe-resources`, `inspect-pe-certificates`,
`inspect-native-exports`, `inspect-managed-artifact`, `inspect-managed-members`,
`inspect-managed-native-boundaries`, `project-managed-application-graph`,
`inspect-sqlite-database`, `extract-artifact`, `search`, `decompile` (needs an engine).

Engine selection is deferred until a reference binary is actually held (D-006). Expected
mix, to be confirmed by `inspect-desktop-application` on real artifacts: Concordance 10 is
a native Win32 application (Ghidra 12.1.x or Hopper would be needed for decompilation);
LAW 7.x and ReadySuite 9.x are expected to be at least partly .NET, for which REA's
managed PE/CLI inspectors need no external engine. This expectation is INFERRED from
installation documentation only (SQL Server and .NET prerequisites) and is not yet OBSERVED.

## Private workspace layout (not in the repository)

```
~/discovery-mill-private/
  rea-env/            pinned REA install (package.json, node_modules)
  acq/law-docs/       official PDFs (hashes in docs/research/artifact-catalog.md)
  acq/answercenter/   wget mirrors of the CloudNine LAW and Concordance Answer Centers
  raw-analysis/       REA Evidence JSON and any decompiler output (none yet)
```

The repository's `.gitignore` excludes `private/`, `acq/`, `raw-analysis/`, and binary
extensions as a second guard.

## Reproducing the public-document acquisition

`scripts/research/fetch-public-docs.sh` downloads the public documents listed in
`docs/research/manifests/public-docs.sha256` into a caller-chosen directory and verifies
their SHA-256. It downloads only from the recorded official or archive.org URLs.
