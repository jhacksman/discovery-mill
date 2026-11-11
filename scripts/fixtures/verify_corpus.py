#!/usr/bin/env python3
"""Verify the committed fixture corpus against its ground-truth manifest and rebuild.

Checks (each reported PASS/FAIL/SKIP):
  1. Every manifest item exists with the recorded SHA-256 and size.
  2. Rebuilding with build_corpus.py into a temp dir reproduces identical bytes (determinism).
  3. Where tools exist: PDF page counts (pdfinfo), TIFF frame counts (Pillow), native PDF text
     (pdftotext) contains expected text, EML attachment filenames, ZIP entry counts.
Exit status is non-zero on any FAIL. Usage: scripts/fixtures/verify_corpus.py [CORPUS_DIR]
"""
import email, email.policy, hashlib, json, os, shutil, subprocess, sys, tempfile, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "fixtures", "corpus")
fails = 0
def report(status, msg):
    global fails
    if status == "FAIL": fails += 1
    print("%-4s %s" % (status, msg))
def sha(p):
    with open(p, "rb") as f: return hashlib.sha256(f.read()).hexdigest()
def have(tool): return shutil.which(tool) is not None

manifest = json.load(open(os.path.join(CORPUS, "manifest.json"), encoding="utf-8"))
for it in manifest["items"]:
    p = os.path.join(CORPUS, it["path"])
    if not os.path.exists(p): report("FAIL", "missing %s" % it["path"]); continue
    ok = sha(p) == it["sha256"] and os.path.getsize(p) == it["size"]
    report("PASS" if ok else "FAIL", "hash/size %s" % it["path"])
    if it.get("kind") == "pdf" and not it.get("corrupt") and "pages" in it:
        if have("pdfinfo"):
            out = subprocess.run(["pdfinfo", p], capture_output=True, text=True).stdout
            n = next((int(l.split()[-1]) for l in out.splitlines() if l.startswith("Pages:")), None)
            report("PASS" if n == it["pages"] else "FAIL", "pdf pages %s expected %s got %s" % (it["path"], it["pages"], n))
        else: report("SKIP", "pdfinfo not available for %s" % it["path"])
        if it.get("text_source") == "native" and have("pdftotext"):
            txt = subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True).stdout
            missing = [t for t in it["expected_text"] for w in t.split() if w not in txt]
            report("PASS" if not missing else "FAIL", "pdf native text %s" % it["path"])
    if it.get("kind") == "tiff":
        try:
            from PIL import Image
            im = Image.open(p); report("PASS" if im.n_frames == it["pages"] else "FAIL", "tiff frames %s expected %s got %s" % (it["path"], it["pages"], im.n_frames))
        except ImportError: report("SKIP", "Pillow not available for %s" % it["path"])
    if it.get("kind") == "eml":
        m = email.message_from_binary_file(open(p, "rb"), policy=email.policy.default)
        names = [a.get_filename() for a in m.iter_attachments()]
        report("PASS" if names == it["attachments"] else "FAIL", "eml attachments %s got %s" % (it["path"], names))
    if it.get("kind") == "zip" and "entries" in it:
        n = len(zipfile.ZipFile(p).namelist()); report("PASS" if n == it["entries"] else "FAIL", "zip entries %s expected %s got %s" % (it["path"], it["entries"], n))

tmp = tempfile.mkdtemp(prefix="dm-corpus-")
try:
    subprocess.run([sys.executable, os.path.join(HERE, "build_corpus.py"), tmp], check=True, capture_output=True)
    diffs = [it["path"] for it in manifest["items"] if sha(os.path.join(tmp, it["path"])) != it["sha256"]]
    report("PASS" if not diffs else "FAIL", "deterministic rebuild (%d differing)" % len(diffs))
finally: shutil.rmtree(tmp, ignore_errors=True)
print("FAILURES:", fails); sys.exit(1 if fails else 0)
