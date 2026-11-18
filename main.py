"""news-image-20261117 (sunny v4): copy the bundled image to /output/entry.png.

Deterministic: a pure file copy, no network, no randomness — both runs
write the same bytes. The image (entry.png, beside this file) is a
1024x1024 warm-cream magazine front page summing up Tuesday 17 November
2026's world news in eight verified stories (see build_image.py).
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


if not os.path.isfile(SRC):
    raise SystemExit(f"bundled image missing: {SRC}")

# Robust output-dir handling: create it if absent, and fail loudly if
# it exists as a file or is not writable, rather than dying mid-copy.
os.makedirs(DST_DIR, exist_ok=True)
if not os.path.isdir(DST_DIR) or not os.access(DST_DIR, os.W_OK):
    raise SystemExit(f"output dir not usable: {DST_DIR}")

DST = os.path.join(DST_DIR, "entry.png")
shutil.copyfile(SRC, DST)

# Fail loudly rather than silently submitting a truncated/corrupt copy:
# the competition runs this program twice and both runs must write the
# same bytes, so verify the output is byte-identical to the source.
if _sha256(DST) != _sha256(SRC):
    raise SystemExit("entry.png copy mismatch: output differs from source")
print(f"wrote entry.png ({_sha256(DST)[:12]}...)")
