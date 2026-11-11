# F-002 — Concordance 10.26.1.153 component inventory, sample database, and field templates (static)

**Research questions:** RQ-EXP-01/02 (DAT/OPT contract), RQ-EXP-05 (review-side field expectations), RQ-ING-03 (email families).
**Target:** `Concordance10_Install.exe` (ART-111; SHA-256 `d6bf35a4…487d8a`), InstallShield setup, product version 10.26.1.153.
**Method:** InstallShield cabinet carved from the setup overlay and extracted with `unshield` 1.6.2 (built from source). 347 of 364 header entries extracted; 17 failed (remaining volume not located). Template `.ini` files read as text; field names read from template `.dcb` string tables. No installation or execution.
**Status:** downloaded ✓ extracted ✓ (partial) installed ✗ launched ✗ tested ✗.

## Components (OBSERVED)

- `Concordance_10.exe` (13.7 MB) plus import pipeline executables: Data Digestion Engine, Data Insertion Engine, import utilities (`cnImport*`, `cnDataImportEngineCLR`), RTF converter, Tag Backup Recovery.
- Engines: dtSearch (`dten600.dll`), SynSearch, Aspose (PDF/Cells/Slides/Email/HTML/CAD/SVG/Diagram), Tesseract 5 via VintaSoft (x86/x64), MAPI shims. Separate Concordance Viewer MSI/cab (87 MB) and FYI connection file format.
- Placeholder PDFs shipped: "IMAGE KEY NOT FOUND" and "PLACE HOLDER" — Concordance renders a placeholder when an image key has no media (DOCUMENTED behaviour corroborated by shipped asset).

## Database file set (OBSERVED from shipped sample `CALFCO` / `COWCO`)

A Concordance 10 database is a set of sibling files sharing a base name: `.dcb` (database/field definitions), `.dct` (dictionary), `.ivt` (inverted text index), `.tex` (text), `.key`, `.ndx`, `.dir`, `.vol`, `.fzy` (fuzzy), optional `.syn` (synonyms), `.trk` (tracking). `.fyi` is an INI connection file (`[Settings] Server=host:port, Database=, Serial=`). Interoperability target for Discovery Mill is **not** this binary set but the DAT/OPT load files Concordance imports (D-00x).

## Shipped field templates (OBSERVED field names; purpose INFERRED from name)

| Template | Fields (in template order) |
|---|---|
| Legal / Litigation Document Production | DOCDATE, BEGNO, ENDNO, DOCTYPE, PRODSTATUS, PRODDATE, TRIALEXNO, ISSUE, SOURCE, TITLE, STATUS, XREF, AUTHOR, ADDRESSEE, COPYEE, MENNAME, SUMMARY, KEYQUOTES, ATTYNOTE, DOCCOND. Field group `PEOPLE = AUTHOR, ADDRESSEE`. |
| E-Docs / E-Mail and Attachments | ATTACHMENT, FROM, TO, CC, BCC, TITLE, SUBJECT, AUTHOR, COMPANY, CATEGORY, KEYWORDS, PRODUCER, CREATOR, COMMENTS, FILEPATH, FOLDER, DATE, TIME, GMT_DATE, GMT_TIME, MODDATE, CREATIONDATE, PRINTDATE, TEXT01–TEXT05, HEADER, METADATA, MESSAGEID, MESSAGEINDEX, ENTRYID, DOCID, PARENT_DOCID. Image base named "Concordance Image (Opticon)". |
| E-Docs / e-Documents | DOCID, TITLE, SUBJECT, AUTHOR, COMPANY, CATEGORY, KEYWORDS, PRODUCER, CREATOR, COMMENTS, METADATA, FILEPATH, DATE, MODDATE, CREATIONDATE, PRINTDATE, TEXT01–TEXT05. |
| Generic 20 Field | FIELD1 … FIELD20 (paragraph fields). |
| Also shipped | Research Bibliography, Legal/Transcripts, FYI/Fyi Log. |

All names are ≤12 characters, upper-case, alphanumeric/underscore — consistent with the documented DAT field-name rule (EV-004/EV-005).

## Implications (PROPOSED)

- Discovery Mill's default DAT export profile should offer a "Concordance e-mail/e-doc" field set compatible with the shipped **E-Mail and Attachments** template (BEGNO/ENDNO-style Bates fields plus FROM/TO/CC/BCC/SUBJECT/DATE/TIME, FILEPATH, DOCID, PARENT_DOCID, ATTACHMENT) and a "Litigation Document Production" set.
- Family relationships in Concordance imports are expressed through DOCID/PARENT_DOCID/ATTACHMENT text fields, not a structural link → export must emit them explicitly.

## Limitations

- 17 cabinet entries not extracted; the Concordance Viewer MSI and a second data volume were not examined.
- Field *types* (paragraph/text/date/numeric) were not decoded from the `.dcb` binary; only names were read. Types come from documentation (EV-004).
