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

## Software identified but not held

| ART | Product / version | Where | Access conditions | Status |
|-----|-------------------|-------|-------------------|--------|
| ART-101 | CloudNine LAW 7.14 ("LAW and Explore 7.14", "LAW 7.14", "Explore 7.14") | https://cloudnine.com/software-download/ | Vendor form (name, company, organizational type…) and "All downloads require an activation key to launch and are subject to the license agreement." | identified — blocked (BLK-001) |
| ART-102 | Concordance 10.26.1.132; Concordance Desktop 1.9.1.6; Concordance FYI Reviewer 5.19.0.40; FYI Server 5.18.1.57 | same page | same form; activation key required | identified — blocked (BLK-001) |
| ART-103 | ReadySuite 9.0.0.515-64df6265d (released 2026-06-18; 14-day trial license available) | https://www.kldiscovery.com/software/readysuite/download | HubSpot form; "Download link and/or trial information will be sent automatically to your email address." No separate trial installer. | identified — blocked (BLK-002) |
| ART-104 | LexisNexis "LAW PreDiscovery trial downloads" page | https://www.lexisnexis.com/en-us/about-us/contact-us/law-downloads.page | Page now contains only contact links; no download | dead end |
| ART-105 | Historical LAW PreDiscovery installers (5.x/6.x, e.g. `law_full_5.2.13.exe` named in ART-002) | archive.org search (`title:(LAW PreDiscovery)`, `Legal Access Ware`, `mediatype:software`) returned no software items | none found with established provenance | not found |

## Sources deliberately not used

manualzz.com, scribd.com, silo.tips, and wordpress.com re-hosts of LAW manuals were found in
search results. They duplicate ART-001/ART-002 content without provenance and are not cited.
