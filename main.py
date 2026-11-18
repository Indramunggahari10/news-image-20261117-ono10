"""Write the entry image for make.fun news-image-20261117.

The repository holds the finished image (entry.png): one picture summing up
the world news of Tuesday 17 November 2026. This program copies it, byte
for byte, to the grader's output directory, so both graded runs produce
identical bytes. Standard library only; no network, no randomness, no clock.
"""

import hashlib
import os
import shutil
import sys

IMAGE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, OUTPUT_NAME)

    with open(source, "rb") as handle:
        magic = handle.read(len(PNG_MAGIC))
    if magic != PNG_MAGIC:
        print("entry.png is not a whole PNG file", file=sys.stderr)
        return 1

    expected = _sha256(source)
    shutil.copyfile(source, target)
    actual = _sha256(target)
    if actual != expected:
        print("copy mismatch: output differs from entry.png", file=sys.stderr)
        return 1
    size = os.path.getsize(target)
    print("wrote %s (%d bytes, sha256 %s)" % (target, size, actual))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
