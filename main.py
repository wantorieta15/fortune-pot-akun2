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
    if not isinstance(text, str):
        raise ValueError(f"entry must be str, got {type(text).__name__}")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise ValueError(
            f"entry must be 1-{MAX_CHARS} characters, got {len(text)}"
        )
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text or "\u2028" in text or "\u2029" in text:
        raise ValueError("entry must be exactly one line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")
    try:
        encoded = text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(f"entry must be valid UTF-8: {exc}") from exc
    if len(encoded) != len(text.encode("utf-8")):
        raise ValueError("entry UTF-8 encoding is not stable")
    digest = hashlib.sha256(encoded).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError(f"entry sha256 mismatch: {digest}")


def main() -> int:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    path = os.path.join(out_dir, "entry.txt")
    expected = ENTRY.encode("utf-8")
    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(ENTRY)
        os.chmod(path, 0o644)
        with open(path, "rb") as f:
            written = f.read()
    except OSError as exc:
        print(f"error: cannot write entry to {path}: {exc}", file=sys.stderr)
        return 1
    if written != expected:
        raise ValueError(
            "round-trip check failed: entry.txt bytes differ from entry"
        )
    mode = os.stat(path).st_mode & 0o777
    if mode != 0o644:
        raise ValueError(f"entry.txt mode is {oct(mode)}, expected 0o644")
    return 0


if __name__ == "__main__":
    sys.exit(main())
