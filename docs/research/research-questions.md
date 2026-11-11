# Research questions

Each RQ names the contract area, the targets, the evidence we expect to reach, and the
backlog items it feeds. Status: open / answered (label) / blocked (BLK).

## Ingestion and provenance

| RQ | Question | Targets | Status |
|----|----------|---------|--------|
| RQ-I01 | How does LAW model a case, custodians, sources, and document identifiers (ID fields, folder structure, DocID/BegDoc)? | LAW 6.2 (EV-001), LAW 7.x (EV-004) | open |
| RQ-I02 | What does LAW preserve of the original bytes and path, which hashes it computes (MD5/SHA-1?), and where processing history is recorded (session reports, logs)? | EV-001, EV-004 | open |
| RQ-I03 | How are loose files, folders, archives, e-mail stores, messages and attachments related (parent/attachment, family ranges)? | EV-001, EV-004 | open |
| RQ-I04 | Which file-type identification and metadata fields are extracted (the ED Loader field list), with types and date/time semantics? | EV-004 `field_descriptions.htm`, `metadata.htm`, `timetadata.htm` | open |
| RQ-I05 | Timezone, encoding and Unicode handling for metadata and text; what is preserved verbatim versus normalized? | EV-004 `unicode_support.htm` | open |
| RQ-I06 | Deduplication scope (case, custodian, inter-case), hash inputs for e-mail versus files, and how duplicate sources/custodians are retained and reported. | EV-004 `deduplication*.htm`, `inter-case_deduplication.htm` | open |

## Imaging and text

| RQ | Question | Targets | Status |
|----|----------|---------|--------|
| RQ-T01 | Document boundaries, page order, splitting/merging; how page records relate to documents. | EV-001, EV-004 | open |
| RQ-T02 | Imaging options: resolution, color/bitonal, compression, rotation, output format (TIFF/PDF), pagination, per-type print settings. | EV-004 `imaging_options.htm`, `tiff-output.htm`, `e-print_tiff_conversion.htm` | open |
| RQ-T03 | Office rendering specifics: spreadsheet print areas, hidden rows/sheets, comments, speaker notes, fonts, embedded objects. | EV-004 `output_settings_e-print_tiff.htm` and e-print topics | open |
| RQ-T04 | Text precedence and provenance: native/extracted vs. printed vs. OCR text; when OCR is triggered; text file naming. | EV-004 `ocr*.htm`, `flagging_pages_for_ocr.htm` | open |
| RQ-T05 | Numbering and endorsement syntax and placement; incremental numbering rules. | EV-004 `numbering_pages_and_documents.htm`, `incremental_numbering_syntax_f.htm`, `endorsing.htm` | open |

## Exceptions and recovery

| RQ | Question | Targets | Status |
|----|----------|---------|--------|
| RQ-E01 | How unsupported, encrypted, corrupt, empty and partially processed files are recorded and surfaced (exception/error reports, status fields). | EV-004 `exception_report.htm`, `reviewing_errors.htm`, `turbo-import-errors.htm` | open |
| RQ-E02 | Cancel/resume semantics for imports and batch processes; crash recovery; retries. | EV-004 batch processing, ED Loader session topics | open |
| RQ-E03 | Reprocessing (re-image, re-OCR, replacement images) without changing document identity. | EV-004 `importing_replacement_images.htm` | open |

## Production and interoperability

| RQ | Question | Targets | Status |
|----|----------|---------|--------|
| RQ-P01 | Production selection and family handling in LAW export. | EV-004 `exporting.htm`, `export_utility_overview.htm` | open |
| RQ-P02 | Bates/production numbering: formats, collisions, page counts, native-only placeholders. | EV-004, EV-001 | open |
| RQ-P03 | Exact Concordance DAT contract: delimiters (þ, ¶, ®/newline substitution), encoding/BOM, header row, quoting, paths, multi-value fields. | EV-005, EV-004 `concordance2.htm`, EV-006 | open |
| RQ-P04 | Exact Opticon OPT contract: fields, document-break flag, box/folder columns, page counts, path conventions. | EV-005, EV-006 | open |
| RQ-P05 | IPRO LFP and Summation DII contracts; whether first-release support is justified. | EV-004 `ipro_intelliview2.htm`, `summation.htm`, EV-006 | open |
| RQ-P06 | Pre-export validation and consistency checks across metadata, natives, text and images; what ReadySuite validates on import. | EV-004 `validate_documents.htm`, EV-006 | open |
| RQ-P07 | Concordance import expectations (field types, max lengths, date formats, image base paths). | EV-005 | open |

## Scope classification

| RQ | Question | Targets | Status |
|----|----------|---------|--------|
| RQ-S01 | PST/MBOX/NSF and legacy formats: cost, open-source availability, and first-release classification. | open-source survey | open |
| RQ-S02 | Which open-source components cover identification, extraction, rendering, OCR, and container handling with acceptable licenses. | open-source survey | open |
| RQ-S03 | Which ingestion, recovery and source-tracing concepts in `jhacksman/librarian` are reusable. | librarian repo | open |
