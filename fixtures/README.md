# Discovery Mill fixture corpus

`fixtures/corpus/` is an **original, synthetic** test corpus with known ground truth, generated
deterministically by `scripts/fixtures/build_corpus.py` (standard library + Pillow only) and
verified by `scripts/fixtures/verify_corpus.py`. It contains no vendor material, no real
people, and no case data; names like "Avery Fixture" and domain `fixture.example` are invented.

| Area | Fixtures | Exercises |
|---|---|---|
| `loose/pdf` | 3-page native-text PDF; 2-page image-only PDF; mixed text+image PDF | text precedence (native vs OCR), per-page provenance, page counts |
| `loose/tiff` | 4-page bitonal Group 4 TIFF (page 3 rotated 90°); single-page 24-bit LZW TIFF | multipage TIFF handling, rotation, colour/bit depth, compression |
| `loose/images` | JPEG and PNG with non-ASCII filenames (`façade-ÄÖÜ`, Cyrillic/CJK/emoji) | Unicode paths, single-page image documents |
| `loose/office` | DOCX with a comment and hidden (vanish) run; XLSX with a hidden sheet and a print area smaller than the data | Office rendering options: comments, hidden content, print areas |
| `email` | EML with PDF + DOCX attachments (Unicode attachment name); reply EML with `In-Reply-To` | families (parent/attachment), threading, date/timezone preservation (`-0500` offset) |
| `containers` | ZIP with folder, nested ZIP, duplicate of a loose PDF, empty file, trailing-space and `CON.txt` names, 20-level deep path | recursive extraction, duplicate detection across containers, hostile filenames |
| `exceptions` | truncated PDF, zero-byte PDF, PNG with `.pdf` extension, placeholder for encrypted archives | exception records, content-based type identification |
| `custodians` | byte-identical PDF under two custodians; near-identical variant | dedup retaining both custodian occurrences; near-dup distinction |

## Ground truth

`fixtures/corpus/manifest.json` lists every file with `sha256`, `size`, `kind`, and
fixture-specific expectations (`pages`, `expected_text`, `attachments`, `family`,
`dup_group`, `has_hidden_text`, `print_area`, `corrupt`, …). Acceptance tests in later PRs
reference these keys; the manifest is the contract, not the generator.

## Reproducing

```sh
python3 scripts/fixtures/build_corpus.py          # regenerates fixtures/corpus (byte-identical)
python3 scripts/fixtures/verify_corpus.py         # hash/size, page counts, text, attachments, determinism
```

Byte-level determinism comes from fixed timestamps (`EPOCH`, `ZIP_DT`), fixed e-mail boundaries,
and no randomness. Renderer outputs (page images produced by Discovery Mill or a reference
product) are compared semantically (page count, OCR text, dimensions), never byte-for-byte.

## Not yet covered (tracked in BACKLOG)

MSG (Outlook) files, PST/MBOX, password-protected archives/PDFs (needs a `zip`/`qpdf` CLI;
see `exceptions/encrypted-placeholder.zip`), large (>100 MB) inputs, interrupted-processing
scenarios (harness-level, not file-level).
