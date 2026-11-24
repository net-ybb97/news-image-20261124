#!/usr/bin/env python3
"""Entry program for the make.fun competition news-image-20261124.

The front page for Tuesday 24 November 2026 was composed ahead of
time by build/composite.py and is stored in this repository as
assets/day.png. The grader runs this program twice in a sandbox with
no network; each run must produce the same bytes at the output path,
so the program does one deterministic thing: it copies the stored
image to the output directory and checks the copy against the
original before reporting success.
"""

import hashlib
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
IMAGE = REPO_ROOT / "assets" / "day.png"
OUTPUT_NAME = "entry.png"


def output_dir() -> Path:
    """Where the grader wants the image: /output, unless overridden."""
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    return Path(override) if override else Path("/output")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    if not IMAGE.is_file():
        print(f"error: stored image not found at {IMAGE}", file=sys.stderr)
        return 1

    payload = IMAGE.read_bytes()
    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / OUTPUT_NAME
    target.write_bytes(payload)

    written_hash = digest(target.read_bytes())
    if written_hash != digest(payload):
        print("error: written file does not match the stored image",
              file=sys.stderr)
        return 1

    print(f"wrote {target} ({len(payload)} bytes, sha256 {written_hash})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
