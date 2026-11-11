# Imaging, text-extraction, and numbering contract

Status: draft specification (REQ-IMG-001, REQ-TXT-001, REQ-NUM-001; M3). Evidence labels per PROGRAM.md D-004.
Sources: LAW PreDiscovery 6.2.46 User Guide (ART-001/EV-001: *Imaging Options*, *Compression*, *Storage Schema*, *TIFF Conversion*, *OCR Options / Flagging documents for OCR*, *Text Extraction*, *Print Options* (Excel/Word/PowerPoint), *Numbering*), LAW 7.14 static findings F-001/F-003, Concordance *Concordance Image* topic (ART-007). Fixtures: `fixtures/corpus` (PR #3). Nothing was executed in a reference product (activation key not held); all reference-product statements are DOCUMENTED or OBSERVED-from-schema.

## 1. Page-image contract (REQ-IMG-001)

| # | Rule | Label | Source |
|---|---|---|---|
| I1 | Default page image is single-page TIFF, CCITT Group 4, bitonal, 300 dpi, letter-size canvas unless the source page size differs (preserve source size). Reference product: G4 TIFF is "the industry standard and the recommended format for black & white images"; its print driver default is 300 DPI. | DOCUMENTED (G4, 300 DPI driver) / PROPOSED (defaults) | LAW UG *Compression*, *E-Print driver* |
| I2 | Colour/greyscale pages: when colour reduction is off and the page contains colour, emit JPEG-compressed TIFF or JPEG at the same dpi; G4 is unavailable for non-bitonal images. A per-page `color_mode ∈ {bitonal, gray, color}` is recorded (reference model has a per-page colour id). | DOCUMENTED (JPEG for colour; G4 bitonal-only) / OBSERVED (page colour id) | LAW UG *Compression*; F-003 |
| I3 | Storage: one file per page ("serialized") is the production form; multipage TIFF is an acceptable *input* and an optional archive form. Page filenames equal the page identifier (`DM000001.TIF`) once numbered; before numbering they are `<docid>-<page:04d>`. | DOCUMENTED (serialized vs multipage) / PROPOSED (naming) | LAW UG *Storage Schema* |
| I4 | Rotation: the stored image is rendered upright when the source declares orientation (PDF `/Rotate`, TIFF `Orientation`); the original value is recorded. Deskew/auto-rotate are explicit, logged cleanup operations, never silent. | PROPOSED; reference exposes deskew/auto-rotate as options | LAW UG *Auto-Deskew*, *Auto Rotate* |
| I5 | Blank-page handling: "drop blank pages" is an option that must be off by default; dropped pages are recorded as page records with `suppressed=true` so page counts remain explainable. | DOCUMENTED (option exists) / PROPOSED (default + record) | LAW UG *TIFF Conversion* |
| I6 | PDF sources: pages are rasterised at the target dpi; PDF is also an allowed *output* form (PDF or PDF/A, optionally with a hidden text layer) produced after endorsement, since endorsement and OCR operate on the raster. | DOCUMENTED (PDF output w/ hidden text; endorse/OCR need raster) | LAW UG *Imaging Options*, *OCR Output format* |
| I7 | Page limit: an optional `max_pages_per_document` (reference: "Limit output to N pages", `HasPageLimit` flag) truncates rendering and records an exception, never silently. | DOCUMENTED / OBSERVED (flag) | LAW UG *Excel print options*; F-003 |
| I8 | Every page record stores: document id, page index, filename, width, height, dpi, colour mode, compression, rotation applied, source (`rendered`, `imported`, `scanned`, `placeholder`), OCR state, redaction/annotation flags. | OBSERVED (reference page entity) / PROPOSED | F-003 |

## 2. Office rendering options (REQ-IMG-001 sub-contract)

All options are per-job profile values, logged with the job. Defaults are chosen for *disclosure completeness* (show what the custodian could have seen) and are PROPOSED unless noted.

| Format | Option | Default | Reference behaviour (DOCUMENTED) |
|---|---|---|---|
| Word | reveal hidden text (`vanish`, white-on-white) | on, "normal mode" = also tag document | Fast mode forces black text/white background without tagging; Normal mode compares colours per word and tags the document |
| Word | show comments | on (end-of-document for engines that cannot place inline) | Comments print on page for Word XP+, otherwise after the last page |
| Word | show tracked changes | on | Printed only if Track Changes was enabled in the document |
| Excel | print hidden rows/columns | on | option |
| Excel | print hidden sheets | on | option |
| Excel | honour print area | off (print full used range); when on, record `print_area` in metadata | Reference prints print area unless overridden; fixture `ledger-hidden-sheet-print-area.xlsx` has data outside `Ledger!A1:C4` |
| Excel | headers/footers | off (headers may contain dates/paths) | option |
| Excel | repeating rows/columns | suppress | option |
| Excel | comments | end of sheet | "As displayed" or "End of the sheet" |
| Excel | black & white | on for bitonal output | clears fills/patterns |
| Excel | row/column headings | off | option |
| PowerPoint | print hidden slides | on | option |
| PowerPoint | speaker notes | on, as separate pages after slides | notes/handout layouts are print options |
| PowerPoint | scale to fit | on | option |
| All | hidden-content detection | on; sets `has_hidden_text=true` and prefixes extracted text with `<<< START HIDDEN CONTENT >>> … <<< END HIDDEN CONTENT >>>` | Reference detects hidden shapes/text/sheets/columns/cells/slides, prepends the same marked section, sets `HiddenText=Y` |
| All | fonts | embed/subset the rendering host's fonts list in the job record; missing fonts are a QC warning | — (PROPOSED) |
| Email | render headers (From/To/CC/BCC/Subject/Sent) as the first page block; attachments are separate documents | Reference saves Outlook messages as RTF/HTML/MSG for printing | 

Fixture mapping: `memo-with-comment-and-hidden.docx` → one page containing both paragraphs, hidden run visible and document tagged, comment visible. `ledger-hidden-sheet-print-area.xlsx` → sheet *Ledger* rendered with row 5 ("OUTSIDE PRINT AREA") and sheet *Hidden* rendered; `has_hidden_sheet=true`.

## 3. Text contract (REQ-TXT-001)

| # | Rule | Label | Source |
|---|---|---|---|
| T1 | Three text sources are tracked separately per document: **extracted** (from the native), **printed/rendered** (captured while rendering), **OCR** (from page images). Reference fields: `TextXStatus`, `TextPStatus`, `OcrStatus`. | OBSERVED / DOCUMENTED | F-003; LAW UG *Text Extraction*, *OCR fields* |
| T2 | Status alphabet per source: `N` = not applicable/not attempted, `Y` = queued, `P` = processing, `C` = complete, `E` = error, `I` = cancelled. Reference uses exactly these letters for OCR (`OcrStatus`: Y/N/C/I/E/P; `OcrFlag` per page: Y/N/C/E) and N/E/C for extraction. | DOCUMENTED | LAW UG *Flagging Documents/Pages for OCR*, *Text Extraction errors* |
| T3 | Precedence for the production text file: extracted → printed → OCR, selectable per export; the chosen source is written to a per-document `TEXTSOURCE` field (`NATIVE`, `RENDERED`, `OCR`, `PER-PAGE` when mixed, `NONE`). Reference export offers "OCR, printed text, or extracted text" as the text to include. | DOCUMENTED (choice offered) / PROPOSED (field + mixed value) | LAW UG *Control lists / Export text* |
| T4 | A document whose extraction failed (`E`) or is unsupported (`N`) is automatically queued for OCR after imaging (reference sets `OcrStatus=Y` when no extracted text exists). Operators may re-queue. | DOCUMENTED | LAW UG *OCR fields* |
| T5 | OCR runs per *page* with per-page status so multi-worker processing and crash recovery resume at page granularity (reference `P` flag enables multiple stations to share an OCR batch). | DOCUMENTED | LAW UG *OCR fields* |
| T6 | Text files are UTF-8 with BOM, one file per document, page breaks marked by form-feed (`\f`); extracted text that contains no readable characters after control-character stripping is marked invalid and discarded (status `E`, reason `no-readable-text`). | DOCUMENTED (invalid-text discard) / PROPOSED (encoding, `\f`) | LAW UG *Text Extraction options* |
| T7 | Hidden content is included at the start of extracted text within the marked section (see §2). | DOCUMENTED | LAW UG *Identify hidden text content* |
| T8 | OCR engine: Tesseract 5 (LSTM) with language packs selected per job; the reference product's current OCR path is also Tesseract-backed (F-001), so parity targets are realistic. OCR accuracy/confidence is stored per page (`OcrAccuracy` exists in the reference model). | OBSERVED (F-001, F-003) / PROPOSED | — |
| T9 | Acceptance (fixtures): `text-3pages.pdf` → `TEXTSOURCE=NATIVE`, text equals manifest `expected_text` modulo whitespace; `image-only-2pages.pdf` → `OCR`, each page's OCR contains the digits token (`48213`, `90377`); `mixed-text-image.pdf` → `PER-PAGE` with page 1 native, page 2 OCR. | PROPOSED | `fixtures/corpus/manifest.json` |

## 4. Numbering and endorsement contract (REQ-NUM-001)

| # | Rule | Label | Source |
|---|---|---|---|
| N1 | Page identifiers (Bates) are page-level values; numbering a range updates document-level `BEGNO`/`ENDNO` automatically. | DOCUMENTED | LAW UG *Numbering* ("BegDoc#/EndDoc# updated to match") |
| N2 | Format: `<prefix><zero-padded integer>[<suffix>]`; padding width is a profile value; alpha-numeric mode increments a trailing letter (`abc001a, abc001b…`) and can be disabled so the numeric part increments instead. | DOCUMENTED | LAW UG *Use alpha-numeric Bates numbering* |
| N3 | Attachments may receive a document-level attachment suffix scheme relative to the parent (`<parent>.0001`); the separator defaults to `.`. | DOCUMENTED | LAW UG *document/page level separator*, *attachment suffix* |
| N4 | Collisions: page identifiers must be unique within a production. On collision the job **fails before writing** and reports every colliding id; it never auto-renames. (Reference either errors or appends ` -DUP1`, ` -DUP2` depending on case type — the silent rename is explicitly rejected.) | DOCUMENTED (reference) / PROPOSED (fail-closed) | LAW UG *Numbering* |
| N5 | Endorsement (header/footer stamping) burns text onto a copy of the page image; the un-endorsed image is retained. Endorsement text may include the page id and static text; position ∈ {left, centre, right} × {top, bottom}; font and size are profile values; the burned region is recorded. | DOCUMENTED (endorse batch; PageID as annotation; alignment/vertical position options) / PROPOSED (retain original) | LAW UG *Endorse*, *IPRO annotations* |
| N6 | Renumbering: a page keeps its internal page record id; Bates values are versioned per production set so re-production does not rewrite history. | PROPOSED (REQ-EXC-002) | — |
| N7 | Page count consistency: `ENDNO − BEGNO + 1 = PAGES` for imaged documents; native-only documents have one placeholder page. The pre-export validator (`scripts/loadfiles/validate_dat_opt.py`) enforces the OPT side. | PROPOSED | PR #4 |

## 5. Measurable acceptance criteria

1. For every fixture with `pages`, rendered page count equals the manifest value (I1–I6).
2. `multipage-g4-4pages.tif` page 3 is stored upright and `rotation_applied=90` recorded (I4).
3. Hidden-content fixtures produce `has_hidden_text=true` and the marked section at the top of the text (T7, §2).
4. OCR fixtures reach ≥ 95 % character accuracy on the printed tokens at 300 dpi (T8); the exact threshold is PROPOSED and must be calibrated once the harness runs.
5. Bates collision test: numbering two overlapping ranges fails with a report listing each duplicate id (N4).
6. Text file per document exists for every record with status `C` in any source; `TEXTSOURCE` matches the status matrix (T1–T3).

## 6. Unknowns / blockers

- UNKNOWN: reference default DPI/colour-reduction values for ED Loader TIFF conversion in 7.14 (6.2 guide documents the driver at 300 DPI only). Needs Windows runtime with activation key (BLK-001/003).
- UNKNOWN: how the reference orders speaker notes vs slides in output (print layout option exists; order not documented).
- Endorsement fonts: not documented; PROPOSED to use an embedded open font (DejaVu Sans) for determinism.
