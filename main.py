#!/usr/bin/env python3
"""Fortune in a Pot — writes one fortune line for the houseplant on the
windowsill to /output/entry.txt (max 120 characters, one line, UTF-8)."""

import hashlib
import os
import sys

ENTRY = (
    "Rain is coming to the window on Thursday, just to say hello. "
    "You will drink it in and stand a little taller."
)

EXPECTED_SHA256 = (
    "b08f9b565be0a696aacb16aee88810e0d453b9c7177e03710a9acd84c032a27f"
)

MAX_CHARS = 120


def validate(text: str) -> None:
    if not text:
        raise ValueError("entry must not be empty")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError(f"entry sha256 mismatch: {digest}")


def main() -> int:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)
    os.chmod(path, 0o644)
    return 0


if __name__ == "__main__":
    sys.exit(main())
