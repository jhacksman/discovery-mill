#!/usr/bin/env python3
"""Validate a Concordance DAT + Opticon OPT pair against docs/spec/loadfiles/dat-opt-contract.md.

Usage: scripts/loadfiles/validate_dat_opt.py VOL.dat VOL.opt [--root DIR] [--key BEGNO]
Checks (DAT): decodable as UTF-8-BOM or UTF-16-LE-BOM (else cp1252 with a warning); consistent field
count per record; header names unique, <=12 chars, start with a letter, [A-Z0-9_] only; every value
wrapped in the quote delimiter; no bare quote/comma delimiter inside values; CRLF line ends and a
terminating line break. (OPT): exactly 7 comma-separated fields; first field non-empty and unique;
break flags are 'Y' or ''; page count integer only on doc-break lines and equal to the lines until the
next break; every key referenced from DAT BEGNO exists as an OPT doc break; optional --root checks that
every OPT image path exists. Exit 1 on any error.
"""
import argparse, os, re, sys
COMMA, QUOTE, NEWLINE = "\x14", "\xfe", "\xae"
errors, warnings = [], []
def err(m): errors.append(m)
def warn(m): warnings.append(m)

def read_dat(path):
    raw = open(path, "rb").read()
    if raw.startswith(b"\xff\xfe"): enc = "utf-16-le"; txt = raw[2:].decode(enc)
    elif raw.startswith(b"\xef\xbb\xbf"): enc = "utf-8"; txt = raw[3:].decode(enc)
    else:
        try: txt = raw.decode("utf-8"); enc = "utf-8 (no BOM)"
        except UnicodeDecodeError: txt = raw.decode("cp1252"); enc = "cp1252"; warn("DAT has no BOM; decoded as cp1252")
    if not txt.endswith("\r\n"): err("DAT must end with CRLF (final record otherwise ignored by some importers)")
    if "\n" in txt.replace("\r\n", ""): err("DAT contains bare LF line breaks; use CRLF between records and \\xae inside fields")
    return enc, [l for l in txt.split("\r\n") if l != ""]

def split_record(line):
    if not (line.startswith(QUOTE) and line.endswith(QUOTE)): err("record not fully quoted: %r" % line[:60])
    parts = line.split(QUOTE + COMMA + QUOTE)
    if len(parts) == 1 and COMMA in line: err("record contains unquoted field separators: %r" % line[:60])
    return [p.strip(QUOTE) for p in parts]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("dat"); ap.add_argument("opt"); ap.add_argument("--root"); ap.add_argument("--key", default="BEGNO")
    a = ap.parse_args()
    enc, lines = read_dat(a.dat)
    header = split_record(lines[0]); n = len(header)
    for h in header:
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", h): err("field name %r violates Concordance naming (letter first, A-Z/0-9/_)" % h)
        if len(h) > 12: err("field name %r longer than 12 characters" % h)
    if len(set(h.upper() for h in header)) != n: err("duplicate field names (case-insensitive)")
    if a.key not in header: err("key field %s not in header" % a.key); sys.exit(report(enc, 0, 0))
    ki = header.index(a.key); keys = []
    for i, l in enumerate(lines[1:], 2):
        rec = split_record(l)
        if len(rec) != n: err("line %d has %d fields, header has %d" % (i, len(rec), n))
        for v in rec:
            if QUOTE in v or COMMA in v: err("line %d: delimiter character inside a value" % i)
        if len(rec) > ki:
            if not rec[ki]: err("line %d: empty %s" % (i, a.key))
            keys.append(rec[ki])
    if len(set(keys)) != len(keys): err("duplicate %s values in DAT" % a.key)
    raw = open(a.opt, "rb").read()
    try: otxt = raw.decode("ascii")
    except UnicodeDecodeError: otxt = raw.decode("cp1252"); warn("OPT contains non-ASCII bytes")
    olines = [l for l in otxt.replace("\r\n", "\n").split("\n") if l]
    breaks, seen, pending = {}, set(), None  # pending: [key, declared count, counted]
    for i, l in enumerate(olines, 1):
        f = l.split(",")
        if len(f) != 7: err("OPT line %d has %d fields (expected 7 / six commas): %r" % (i, len(f), l[:60])); continue
        key, vol, path, doc, folder, box, cnt = f
        if not key: err("OPT line %d: empty image key" % i)
        if key in seen: err("OPT line %d: duplicate image key %s" % (i, key))
        seen.add(key)
        for flag, nm in ((doc, "doc"), (folder, "folder"), (box, "box")):
            if flag not in ("Y", ""): err("OPT line %d: %s break must be Y or empty, got %r" % (i, nm, flag))
        if doc == "Y":
            if pending and pending[1] is not None and pending[1] != pending[2]: err("OPT doc %s declares %d pages but has %d lines" % tuple(pending))
            pending = [key, int(cnt) if cnt.isdigit() else None, 1]
            if cnt and not cnt.isdigit(): err("OPT line %d: page count not an integer" % i)
            breaks[key] = path
        else:
            if cnt: err("OPT line %d: page count only allowed on document-break lines" % i)
            if pending is None: err("OPT line %d: page before first document break" % i)
            else: pending[2] += 1
        if a.root:
            p = os.path.join(a.root, path.replace("\\", os.sep).lstrip("." + os.sep))
            if not os.path.exists(p): err("OPT line %d: image not found: %s" % (i, path))
    if pending and pending[1] is not None and pending[1] != pending[2]: err("OPT doc %s declares %d pages but has %d lines" % tuple(pending))
    for k in keys:
        if k not in breaks: err("DAT %s %s has no OPT document break" % (a.key, k))
    for k in breaks:
        if k not in keys: warn("OPT document %s not present in DAT" % k)
    sys.exit(report(enc, len(keys), len(olines)))

def report(enc, nrec, nopt):
    print("DAT encoding: %s; records: %d; OPT lines: %d" % (enc, nrec, nopt))
    for w in warnings: print("WARN ", w)
    for e in errors: print("ERROR", e)
    print("RESULT", "FAIL" if errors else "PASS"); return 1 if errors else 0

if __name__ == "__main__":
    main()
