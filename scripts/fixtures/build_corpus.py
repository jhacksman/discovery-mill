#!/usr/bin/env python3
"""Build the Discovery Mill original synthetic fixture corpus deterministically.

Usage: scripts/fixtures/build_corpus.py [OUT_DIR]   (default: fixtures/corpus)

Everything here is original, synthetic content. No vendor material, no real people,
no case data. Output is byte-deterministic (fixed timestamps, no randomness) so the
SHA-256 manifest (fixtures/corpus/manifest.json) is reproducible and reviewable.
Only the Python standard library and Pillow are required.
"""
import hashlib, io, json, os, struct, sys, zipfile, zlib
from email.message import EmailMessage
from email.utils import formatdate
from PIL import Image, ImageDraw, ImageFont

EPOCH = 1700000000  # 2023-11-14T22:13:20Z, fixed mtime for every file
ZIP_DT = (2023, 11, 14, 22, 13, 20)
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "fixtures", "corpus")
TRUTH = {"fixture_set": "dm-corpus", "version": 1, "items": []}

def font(sz=28):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()

def write(rel, data, **truth):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f: f.write(data)
    os.utime(path, (EPOCH, EPOCH))
    TRUTH["items"].append({"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data), **truth})
    return data

# ---------- minimal PDF writer (text pages and/or image pages) ----------
def pdf(pages):
    """pages: list of dicts {text:[lines]} or {jpeg:bytes,w,h}. Letter size, 612x792 pt."""
    objs = []  # list of bytes bodies; object n = index+1
    def add(b): objs.append(b); return len(objs)
    font_id = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    page_ids = []
    pages_id_placeholder = add(b"")  # filled later
    for pg in pages:
        res = b"<< /Font << /F1 %d 0 R >> >>" % font_id
        if "text" in pg:
            ops = ["BT /F1 12 Tf 72 720 Td 16 TL"]
            for ln in pg["text"]:
                ln = ln.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
                ops.append("(%s) Tj T*" % ln)
            ops.append("ET")
            content = "\n".join(ops).encode("cp1252", "replace")
        else:
            img_id = add(b"<< /Type /XObject /Subtype /Image /Width %d /Height %d /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length %d >>\nstream\n" % (pg["w"], pg["h"], len(pg["jpeg"])) + pg["jpeg"] + b"\nendstream")
            res = b"<< /XObject << /Im1 %d 0 R >> >>" % img_id
            content = b"q 612 0 0 792 0 0 cm /Im1 Do Q"
        c_id = add(b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream")
        page_ids.append(add(b"<< /Type /Page /Parent %d 0 R /MediaBox [0 0 612 792] /Resources %s /Contents %d 0 R >>" % (pages_id_placeholder, res, c_id)))
    objs[pages_id_placeholder - 1] = b"<< /Type /Pages /Kids [%s] /Count %d >>" % (b" ".join(b"%d 0 R" % i for i in page_ids), len(page_ids))
    cat = add(b"<< /Type /Catalog /Pages %d 0 R >>" % pages_id_placeholder)
    info = add(b"<< /Title (Discovery Mill synthetic fixture) /Producer (dm-fixtures) /CreationDate (D:20231114221320Z) >>")
    out = io.BytesIO(); out.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"); offs = []
    for i, b in enumerate(objs, 1):
        offs.append(out.tell()); out.write(b"%d 0 obj\n" % i + b + b"\nendobj\n")
    xref = out.tell()
    out.write(b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1))
    for o in offs: out.write(b"%010d 00000 n \n" % o)
    out.write(b"trailer\n<< /Size %d /Root %d 0 R /Info %d 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, cat, info, xref))
    return out.getvalue()

def page_image(lines, size=(1700, 2200), mode="RGB", rotate=0, noise=False):
    im = Image.new(mode, size, "white" if mode != "1" else 1)
    d = ImageDraw.Draw(im); f = font(44); y = 150
    for ln in lines:
        d.text((150, y), ln, fill="black" if mode != "1" else 0, font=f); y += 70
    d.rectangle([100, 100, size[0] - 100, size[1] - 100], outline="black" if mode != "1" else 0, width=4)
    if rotate: im = im.rotate(rotate, expand=True, fillcolor="white" if mode != "1" else 1)
    return im

def to_bytes(im, fmt, **kw):
    b = io.BytesIO(); im.save(b, fmt, **kw); return b.getvalue()

def tiff_multi(images, compression="group4"):
    b = io.BytesIO()
    images[0].save(b, "TIFF", save_all=True, append_images=images[1:], compression=compression, dpi=(200, 200))
    return b.getvalue()

# ---------- minimal OOXML writers ----------
def ooxml(parts, content_types):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in [("[Content_Types].xml", content_types)] + parts:
            zi = zipfile.ZipInfo(name, ZIP_DT); zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)
    return b.getvalue()

def docx(paragraphs, comment=None, hidden=None):
    body = "".join('<w:p><w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % p for p in paragraphs)
    if hidden:
        body += '<w:p><w:r><w:rPr><w:vanish/></w:rPr><w:t>%s</w:t></w:r></w:p>' % hidden
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
           '<w:body>%s<w:sectPr><w:pgSz w:w="12240" w:h="15840"/></w:sectPr></w:body></w:document>' % body)
    parts = [("_rels/.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>'),
             ("word/document.xml", doc),
             ("docProps/core.xml", '<?xml version="1.0" encoding="UTF-8"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>Fixture memo</dc:title><dc:creator>Avery Fixture</dc:creator><cp:lastModifiedBy>Blake Fixture</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">2023-11-01T09:00:00Z</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">2023-11-14T22:13:20Z</dcterms:modified></cp:coreProperties>')]
    rels = '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">%s</Relationships>'
    ct_extra = ""
    if comment:
        parts.append(("word/comments.xml", '<?xml version="1.0" encoding="UTF-8"?><w:comments xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:comment w:id="0" w:author="Casey Fixture" w:date="2023-11-02T10:00:00Z"><w:p><w:r><w:t>%s</w:t></w:r></w:p></w:comment></w:comments>' % comment))
        parts.append(("word/_rels/document.xml.rels", rels % '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments" Target="comments.xml"/>'))
        ct_extra = '<Override PartName="/word/comments.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/>'
    ct = ('<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>%s</Types>' % ct_extra)
    return ooxml(parts, ct)

def xlsx(rows, hidden_sheet_rows=None, print_area="A1:C4"):
    def sheet(rows):
        xr = "".join('<row r="%d">%s</row>' % (i, "".join('<c r="%s%d" t="inlineStr"><is><t>%s</t></is></c>' % (chr(65 + j), i, v) for j, v in enumerate(r))) for i, r in enumerate(rows, 1))
        return '<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>%s</sheetData></worksheet>' % xr
    sheets = '<sheet name="Ledger" sheetId="1" r:id="rId1"/>'
    defined = '<definedNames><definedName name="_xlnm.Print_Area" localSheetId="0">Ledger!$%s</definedName></definedNames>' % print_area.replace(":", ":$").replace("A1", "A$1", 1)
    wb_rels = '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
    parts = [("_rels/.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>'),
             ("xl/worksheets/sheet1.xml", sheet(rows))]
    overrides = '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
    if hidden_sheet_rows:
        sheets += '<sheet name="Hidden" sheetId="2" state="hidden" r:id="rId2"/>'
        wb_rels += '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>'
        parts.append(("xl/worksheets/sheet2.xml", sheet(hidden_sheet_rows)))
        overrides += '<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
    parts += [("xl/workbook.xml", '<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>%s</sheets>%s</workbook>' % (sheets, defined)),
              ("xl/_rels/workbook.xml.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">%s</Relationships>' % wb_rels)]
    ct = ('<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>%s</Types>' % overrides)
    return ooxml(parts, ct)

def eml(subject, frm, to, date, body, attachments=(), message_id=None, in_reply_to=None):
    m = EmailMessage()
    m["From"] = frm; m["To"] = to; m["Subject"] = subject; m["Date"] = date
    m["Message-ID"] = message_id or "<%s@fixture.example>" % hashlib.sha1(subject.encode()).hexdigest()[:16]
    if in_reply_to: m["In-Reply-To"] = in_reply_to
    m.set_content(body)
    for name, data, mt in attachments:
        main, sub = mt.split("/")
        m.add_attachment(data, maintype=main, subtype=sub, filename=name)
    if m.is_multipart(): m.set_boundary("dm-fixture-boundary-" + hashlib.sha1(subject.encode()).hexdigest()[:12])
    return m.as_bytes(policy=m.policy.clone(linesep="\r\n"))

def zipped(entries):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in entries:
            zi = zipfile.ZipInfo(name, ZIP_DT); zi.compress_type = zipfile.ZIP_DEFLATED; z.writestr(zi, data)
    return b.getvalue()

def main():
    os.makedirs(OUT, exist_ok=True)
    D = "2023-11-14T22:13:20Z"
    # 1 text PDF, 3 pages
    t3 = [["Discovery Mill fixture PDF-TEXT-001", "Page 1 of 3", "The quick brown fox jumps over the lazy dog."],
          ["Page 2 of 3", "Invoice total: 1,234.56", "Reference: DM-FIX-0001"],
          ["Page 3 of 3", "End of document."]]
    write("loose/pdf/text-3pages.pdf", pdf([{"text": p} for p in t3]), kind="pdf", pages=3, text_source="native", expected_text=[" ".join(p) for p in t3])
    # 2 image-only PDF (scanned look), 2 pages -> OCR required
    imgs = [page_image(["SCANNED PAGE ONE", "OCR TARGET 48213"]), page_image(["SCANNED PAGE TWO", "OCR TARGET 90377"])]
    jp = [to_bytes(i.resize((850, 1100)), "JPEG", quality=85) for i in imgs]
    write("loose/pdf/image-only-2pages.pdf", pdf([{"jpeg": j, "w": 850, "h": 1100} for j in jp]), kind="pdf", pages=2, text_source="ocr", expected_text=["SCANNED PAGE ONE OCR TARGET 48213", "SCANNED PAGE TWO OCR TARGET 90377"])
    # 3 mixed PDF: page1 text, page2 image
    write("loose/pdf/mixed-text-image.pdf", pdf([{"text": ["MIXED PDF page one is native text", "Token: MIXED-7781"]}, {"jpeg": jp[0], "w": 850, "h": 1100}]), kind="pdf", pages=2, text_source="per-page", expected_text=["MIXED PDF page one is native text Token: MIXED-7781", "SCANNED PAGE ONE OCR TARGET 48213"])
    # 4 multipage TIFF bitonal G4, 4 pages, page 3 rotated 90
    pages = [page_image(["TIFF PAGE %d" % i, "G4 BITONAL"], mode="1", rotate=(90 if i == 3 else 0)) for i in range(1, 5)]
    write("loose/tiff/multipage-g4-4pages.tif", tiff_multi(pages), kind="tiff", pages=4, bits=1, compression="group4", rotated_pages=[3])
    # 5 single-page color TIFF LZW
    write("loose/tiff/single-color-lzw.tif", tiff_multi([page_image(["COLOR TIFF", "LZW"]).convert("RGB")], "tiff_lzw"), kind="tiff", pages=1, bits=24, compression="lzw")
    # 6 JPEG / PNG with Unicode names
    write("loose/images/photo-façade-ÄÖÜ.jpg", to_bytes(page_image(["JPEG FIXTURE", "façade ÄÖÜ"]).resize((850, 1100)), "JPEG", quality=90), kind="jpeg", pages=1)
    write("loose/images/диаграмма-図-🙂.png", to_bytes(page_image(["PNG FIXTURE", "Unicode filename"]).resize((425, 550)), "PNG"), kind="png", pages=1)
    # 7 Office
    write("loose/office/memo-with-comment-and-hidden.docx", docx(["Memo to file: Discovery Mill fixture DOCX-001.", "Second paragraph with Unicode: café, naïve, 日本語."], comment="Reviewer comment: verify paragraph two.", hidden="HIDDEN TEXT SHOULD BE FLAGGED"), kind="docx", pages_expected_min=1, has_comments=True, has_hidden_text=True, expected_text_contains=["Memo to file", "café", "日本語"])
    write("loose/office/ledger-hidden-sheet-print-area.xlsx", xlsx([["Item", "Qty", "Amount"], ["Widget", "2", "10.00"], ["Gadget", "1", "25.50"], ["Total", "", "35.50"], ["OUTSIDE PRINT AREA", "", ""]], hidden_sheet_rows=[["HIDDEN SHEET VALUE", "secret-7"]], print_area="A1:C4"), kind="xlsx", has_hidden_sheet=True, print_area="Ledger!A1:C4", expected_text_contains=["Widget", "35.50"], expected_text_hidden=["HIDDEN SHEET VALUE", "OUTSIDE PRINT AREA"])
    # 8 e-mail family: parent EML with PDF + DOCX attachments, plus reply
    att_pdf = pdf([{"text": ["Attachment PDF", "ATTACH-PDF-0001"]}])
    att_docx = docx(["Attachment DOCX ATTACH-DOCX-0001"])
    parent = eml("Fixture thread: Q3 figures", "Avery Fixture <avery@fixture.example>", "Blake Fixture <blake@fixture.example>, Casey Fixture <casey@fixture.example>", "Tue, 14 Nov 2023 22:13:20 +0000", "Blake, Casey — attached are the Q3 figures. Please review.\n\nUnicode check: naïve café 日本語 🙂\n", [("Q3-figures.pdf", att_pdf, "application/pdf"), ("notes — final.docx", att_docx, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")], message_id="<parent-0001@fixture.example>")
    write("email/parent-with-2-attachments.eml", parent, kind="eml", family="FAM-001", role="parent", attachments=["Q3-figures.pdf", "notes — final.docx"], sent="2023-11-14T22:13:20+00:00")
    write("email/reply-no-attachments.eml", eml("Re: Fixture thread: Q3 figures", "Blake Fixture <blake@fixture.example>", "Avery Fixture <avery@fixture.example>", "Wed, 15 Nov 2023 09:05:00 -0500", "Looks good, one typo on page 2.\n", message_id="<reply-0001@fixture.example>", in_reply_to="<parent-0001@fixture.example>"), kind="eml", family="FAM-002", role="parent", attachments=[], sent="2023-11-15T09:05:00-05:00", in_reply_to="<parent-0001@fixture.example>")
    # 9 nested containers: zip containing folder, zip-in-zip, duplicate of text PDF, empty file, odd names
    inner = zipped([("inner/attachment-copy.pdf", att_pdf), ("inner/empty.txt", b"")])
    outer = zipped([("folder one/text-3pages (copy).pdf", pdf([{"text": p} for p in t3])), ("folder one/nested.zip", inner), ("trailing space .txt", b"name with trailing space\n"), ("CON.txt", b"reserved device name on Windows\n"), ("very/deep/" + "/".join(["d%02d" % i for i in range(1, 21)]) + "/leaf.txt", b"deep path\n")])
    write("containers/nested-outer.zip", outer, kind="zip", entries=5, nested_zip=True, contains_duplicate_of="loose/pdf/text-3pages.pdf", contains_empty=True)
    # 10 exception cases
    write("exceptions/encrypted-placeholder.zip", zipped([("readme.txt", b"this zip is NOT encrypted; see encrypted.zip generated by make_encrypted()\n")]), kind="zip", note="placeholder; password-protected archives are produced by scripts/fixtures/make_encrypted.sh (needs zip CLI)")
    write("exceptions/corrupt-truncated.pdf", pdf([{"text": ["TRUNCATED"]}])[:300], kind="pdf", corrupt="truncated", expect="exception: unreadable or partial")
    write("exceptions/zero-byte.pdf", b"", kind="pdf", corrupt="empty", expect="exception: empty file")
    write("exceptions/wrong-extension-is-png.pdf", to_bytes(page_image(["I AM A PNG"]).resize((200, 260)), "PNG"), kind="png", declared_ext="pdf", expect="identified by content as PNG; SuspectExt-style flag")
    # 11 duplicates across custodians
    dup = pdf([{"text": ["DUPLICATE CANDIDATE", "same bytes in two custodians"]}])
    write("custodians/avery/report.pdf", dup, kind="pdf", dup_group="DUP-001", custodian="avery")
    write("custodians/blake/Report (1).pdf", dup, kind="pdf", dup_group="DUP-001", custodian="blake")
    write("custodians/blake/report-modified.pdf", pdf([{"text": ["DUPLICATE CANDIDATE", "same text, different metadata? no: different bytes"]}]), kind="pdf", dup_group=None, custodian="blake", near_dup_of="DUP-001")
    TRUTH["items"].sort(key=lambda x: x["path"])
    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(TRUTH, f, indent=1, ensure_ascii=False, sort_keys=True); f.write("\n")
    print("wrote %d fixtures to %s" % (len(TRUTH["items"]), OUT))

if __name__ == "__main__":
    main()
