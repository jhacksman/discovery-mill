# Artifact catalog

Statuses are distinct and are never collapsed: **downloaded** (bytes held, hash recorded),
**extracted**, **installed**, **launched**, **tested**. "Downloaded" does not mean runnable.
Binaries and mirrors live in the private workspace (`docs/research/environment.md`); only
provenance and hashes are published here. Acquisition date for all rows: 2026-11-11.

## Documentation held (public, official or archive.org provenance)

| ART | Product / version / component | Source URL | SHA-256 | Pages | Access conditions | Status |
|-----|-------------------------------|------------|---------|-------|-------------------|--------|
| ART-001 | LAW PreDiscovery 6.2.46 — *Using LAW PreDiscovery* User Guide (LexisNexis, © 2015; "Release Date: September 5, 2012" on the version page) | https://archive.org/download/manualzilla-id-5757459/5757459.pdf (item `manualzilla-id-5757459`, added 2021-03-06; archive.org sha1 `a4c73b4cbbf4466d14a272b3bbf2fa9d6b830c5f`) | `b63802a9ccd9edf626141854517e19b87306a1c0324d2d11dbf2e97e0e343cb7` | 782 | Public; third-party upload of a vendor manual, no license stated | downloaded |
| ART-002 | LAW PreDiscovery 5.x — *Getting Started Guide* (LexisNexis, PDF created 2010-08-02; install walkthrough names `law_full_5.2.13.exe`) | http://www.imagecap.com/Law50/docs/LAW%20PreDiscovery%20Getting%20Started.pdf (CloudNine-controlled host; browser-less fetches of the directory are Cloudflare-blocked, the file itself downloaded) | `e40f43cefd7ffc1d3b58650bf6539e90af25df3cb9a772e564ec8aa97b83d90b` | 69 | Public | downloaded |
| ART-003 | LAW PreDiscovery — product sheet "Imaging and Electronic Discovery Software" (LexisNexis) | https://www.lexisnexis.com/pdf/Litigation/LAWProductUser.pdf | `7bbf2ad1da4e6e1ce01d9be9650663e8d62bd302e1fa6d4d51cb39b91b86c5ab` | 2 | Public | downloaded |
| ART-004 | LexisNexis Early Data Analyzer + LAW PreDiscovery — product sheet | https://www.lexisnexis.com/pdf/Litigation/EDALAWProductUser.pdf | `dd243b41f6b2ccc77006740575693c3a90301434929c5967bec56b9a6c21dde1` | 4 | Public | downloaded |
| ART-005 | Concordance 10.22 — *Installation Guide* (LexisNexis, release date 2018-04-23; also lists Concordance Native Viewer 1.11, Concordance Image 5.16, FYI Server 5.14, FYI Reviewer 5.17) | https://www.lexisnexis.com/documents/cndownload/Concordance%2010%20Installation%20Guide.pdf | `395af4aad2a1d6438c86b0cb4a9390d8436db03c7e49feefbce2f15e0bff12f8` | 73 | Public | downloaded |
| ART-006 | CloudNine LAW Answer Center (current LAW 7.x documentation; HTML help site, ~1,000 topics) | https://answercenter.ediscovery.co/litigation/ac/law/ | per-file hashes in private mirror manifest (`acq/answercenter/law.sha256`, generated when the mirror completes) | — | Public | downloaded (mirror in progress) |
| ART-007 | CloudNine Concordance (classic, 10.x) Answer Center | https://answercenter.ediscovery.co/litigation/ac/cn_classic/ | per-file hashes in private mirror manifest | — | Public | downloaded (mirror in progress) |
| ART-008 | ReadySuite help (KLDiscovery / Compiled Technologies; MadCap Flare site) | https://help.ediscovery.com/readysuite/ and https://help.kldiscovery.com/readysuite/ | not yet mirrored | — | Public | identified |
| ART-009 | CloudNine Answer Center portal (lists LAW, Explore, Concordance, Concordance Desktop, Collection Manager, Data Wrangler help sets) | http://answercenter.ediscovery.co/litigation/ac/ac_portal/ | — | — | Public | identified |

## Software held (official CloudNine distribution host; direct links published in the HTML of https://cloudnine.com/software-download/; activation key required to launch)

| ART | Product / version / component | Source URL | Server Last-Modified | Size | SHA-256 | Status |
|-----|-------------------------------|------------|----------------------|------|---------|--------|
| ART-110 | CloudNine LAW 7.14 installer bundle (`LAW-7.14.zip` → `LAW_7.14.290.exe`) | https://software.cloudnine.com/LAW/LAW-7.14.zip | 2026-11-03 16:58 GMT | 556,837,346 B | `272192c558e01510aa09f365deb0ddad7851c8a02a326788b7ec7a77ba494a3d` (zip); inner `LAW_7.14.290.exe` `b0e450063087a62d9d0bf4d365f2afee54f6995876bb99314720685e7159461c`; Authenticode signer "Cloud9 Discovery LLC" (DigiCert G4 code-signing CA, cert valid 2025-10-01..2028-10-17, timestamped) | downloaded, extracted (WiX Burn bundle → `CloudNineLAW.msi` → 1,343 files); not installed/launched/tested (activation key) |
| ART-111 | Concordance 10 installer (`Concordance10_Install.exe`) | https://software.cloudnine.com/Concordance/Concordance10_Install.exe | 2026-10-19 | 634,539,688 B | `d6bf35a4b1847c791a7b5f5db6612000f441746fca76b3270809bc41b4487d8a`; InstallShield stub, FileVersion 10.26.1.153, DigiCert-signed | downloaded, extracted (347 files incl. `Concordance_10.exe`, sample DB, templates); not installed/launched/tested |
| ART-112 | Concordance Desktop 1.9.1.6 (`Concordance Desktop_1.9.1.6.zip`) | https://software.cloudnine.com/Concordance/Concordance%20Desktop_1.9.1.6.zip | 2020-11-06 | 465,988,181 B | `629dae292bdc7498035c31046f3e54eded2136217845c7b2d2f00e9265e10873` (zip); inner installer `8b0113687e89150a1913ea95e5d2bb2a3799cb8265bed4c904b40eef7a8fb3ce`, signer "CloudNine" (GoDaddy G2, cert 2017-11-03..2020-11-05) | downloaded, extracted (zip only) |
| ART-113 | Concordance FYI Reviewer 5.19.0.40 | https://software.cloudnine.com/Concordance/Classic_10.24/FYIReviewer_5.19.0.40.zip | 2021-01-07 | 4,839,861 B | `aff95e397bf185a36dc49facf38d616c0ee02da1c91cc977fb38aed402e4b377`; ActiveX cab (Dataflight_FYI_4.ocx + Black Ice imaging DLLs) | downloaded, extracted; low relevance (viewer) |
| ART-114 | LAW+Explore 7.14 / Explore 7.14 / FYI Server 5 | https://software.cloudnine.com/LAW/LAW-Explore-7.14.zip, …/Explore-7.14.zip, …/Concordance/FYI_Server_5_Install.exe | 2026-11-03 / 2025-10-03 | 840,812,942 / 840,812,934 / 63,410,272 B | — | identified (not needed yet) |

## Software identified but not held

| ART | Product / version | Where | Access conditions | Status |
|-----|-------------------|-------|-------------------|--------|
| ART-101 | superseded by ART-110/114 | | | |
| ART-102 | superseded by ART-111…114 | | | |
| ART-103 | ReadySuite 9.0.0.515-64df6265d (released 2026-06-18; 14-day trial license available) | https://www.kldiscovery.com/software/readysuite/download | HubSpot form; "Download link and/or trial information will be sent automatically to your email address." No separate trial installer. | identified — blocked (BLK-002) |
| ART-104 | LexisNexis "LAW PreDiscovery trial downloads" page | https://www.lexisnexis.com/en-us/about-us/contact-us/law-downloads.page | Page now contains only contact links; no download | dead end |
| ART-105 | Historical LAW PreDiscovery installers (5.x/6.x, e.g. `law_full_5.2.13.exe` named in ART-002) | archive.org search (`title:(LAW PreDiscovery)`, `Legal Access Ware`, `mediatype:software`) returned no software items | none found with established provenance | not found |

## Sources deliberately not used

manualzz.com, scribd.com, silo.tips, and wordpress.com re-hosts of LAW manuals were found in
search results. They duplicate ART-001/ART-002 content without provenance and are not cited.
