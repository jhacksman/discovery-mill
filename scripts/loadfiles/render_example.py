#!/usr/bin/env python3
"""Render a worked Concordance DAT + Opticon OPT example production from the fixture corpus.

Usage: scripts/loadfiles/render_example.py [OUT_DIR]   (default: docs/spec/loadfiles/examples/VOL001)

This is a *specification example generator*, not the Discovery Mill implementation: it takes
fixtures/corpus/manifest.json, assigns deterministic Bates numbers (DM000001…), and writes
VOL001.dat / VOL001.opt plus a text file per document, exactly following the contract in
docs/spec/loadfiles/dat-opt-contract.md. Page images are represented by their expected
filenames only (no renderer is run here); page counts come from the manifest ground truth.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MANIFEST = os.path.join(ROOT, "fixtures", "corpus", "manifest.json")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "docs", "spec", "loadfiles", "examples", "VOL001")
VOLUME = "VOL001"
COMMA, QUOTE, NEWLINE = "\x14", "\xfe", "\xae"   # Concordance defaults: ASCII 20, 254, 174
FIELDS = ["BEGNO", "ENDNO", "BEGATT", "ENDATT", "PARENT_DOCID", "DOCID", "CUSTODIAN", "FILENAME", "FILEPATH",
          "DOCEXT", "PAGES", "MD5HASH", "SHA256HASH", "DATECREATED", "TIMECREATED", "FROM", "TO", "SUBJECT",
          "DATESENT", "TIMESENT", "TEXTSOURCE", "NATIVEPATH", "TEXTPATH", "EXCEPTION"]

def bates(n): return "DM%06d" % n
def esc(v):
    v = "" if v is None else str(v)
    return QUOTE + v.replace(QUOTE, "").replace(COMMA, "").replace("\r\n", NEWLINE).replace("\n", NEWLINE) + QUOTE

def main():
    items = [i for i in json.load(open(MANIFEST, encoding="utf-8"))["items"] if i["path"] != "manifest.json"]
    # Build families: EML parents own their attachments (from manifest 'attachments' names)
    docs, n = [], 1
    for it in items:
        pages = it.get("pages", 1 if not it.get("corrupt") else 0)
        exception = ""
        if it.get("corrupt"): exception = "UNREADABLE:%s" % it["corrupt"]; pages = 1  # slip-sheet placeholder page
        children = it.get("attachments", [])
        d = {"src": it, "pages": pages, "exception": exception, "beg": bates(n), "end": bates(n + pages - 1), "kids": []}
        n += pages
        for name in children:
            kid_pages = 1
            d["kids"].append({"name": name, "pages": kid_pages, "beg": bates(n), "end": bates(n + kid_pages - 1)})
            n += kid_pages
        docs.append(d)
    os.makedirs(os.path.join(OUT, "IMAGES"), exist_ok=True); os.makedirs(os.path.join(OUT, "TEXT"), exist_ok=True)
    dat, opt = [COMMA.join(esc(f) for f in FIELDS)], []
    def row(beg, end, begatt, endatt, parent, it, pages, exception, name=None, custodian=""):
        path = it["path"] if it else name
        base = os.path.basename(path)
        rec = {"BEGNO": beg, "ENDNO": end, "BEGATT": begatt, "ENDATT": endatt, "PARENT_DOCID": parent if parent != beg else "",
               "DOCID": beg, "CUSTODIAN": custodian or (it or {}).get("custodian", "fixture"), "FILENAME": base,
               "FILEPATH": os.path.dirname(path), "DOCEXT": os.path.splitext(base)[1].lstrip(".").upper(), "PAGES": pages,
               "MD5HASH": "", "SHA256HASH": (it or {}).get("sha256", ""), "DATECREATED": "11/14/2023", "TIMECREATED": "22:13:20",
               "FROM": "", "TO": "", "SUBJECT": "", "DATESENT": "", "TIMESENT": "",
               "TEXTSOURCE": (it or {}).get("text_source", "native" if not exception else "none").upper(),
               "NATIVEPATH": ".\\%s\\NATIVES\\%s" % (VOLUME, base), "TEXTPATH": ".\\%s\\TEXT\\%s.txt" % (VOLUME, beg), "EXCEPTION": exception}
        if (it or {}).get("kind") == "eml":
            rec.update(FROM="Avery Fixture <avery@fixture.example>", TO="Blake Fixture <blake@fixture.example>", SUBJECT="Fixture thread: Q3 figures",
                       DATESENT=it["sent"][:10].split("-")[1] + "/" + it["sent"][8:10] + "/" + it["sent"][:4], TIMESENT=it["sent"][11:19])
        dat.append(COMMA.join(esc(rec[f]) for f in FIELDS))
        for p in range(pages):
            key = bates(int(beg[2:]) + p)
            opt.append(",".join([key, VOLUME, ".\\%s\\IMAGES\\%s.TIF" % (VOLUME, key), "Y" if p == 0 else "", "", "", str(pages) if p == 0 else ""]))
        with open(os.path.join(OUT, "TEXT", beg + ".txt"), "w", encoding="utf-8") as f:
            f.write("\n".join((it or {}).get("expected_text", [])) + ("\n" if (it or {}).get("expected_text") else ""))
    for d in docs:
        begatt, endatt = d["beg"], (d["kids"][-1]["end"] if d["kids"] else d["end"])
        row(d["beg"], d["end"], begatt, endatt, d["beg"], d["src"], d["pages"], d["exception"])
        for k in d["kids"]:
            row(k["beg"], k["end"], begatt, endatt, d["beg"], None, k["pages"], "", name=os.path.join(os.path.dirname(d["src"]["path"]), k["name"]))
    with open(os.path.join(OUT, VOLUME + ".dat"), "w", encoding="utf-8", newline="") as f:
        f.write("\ufeff" + "\r\n".join(dat) + "\r\n")
    with open(os.path.join(OUT, VOLUME + ".opt"), "w", encoding="ascii", newline="") as f:
        f.write("\r\n".join(opt) + "\r\n")
    print("wrote %d DAT records, %d OPT lines to %s" % (len(dat) - 1, len(opt), OUT))

if __name__ == "__main__":
    main()
