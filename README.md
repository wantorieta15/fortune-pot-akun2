# Fortune in a Pot

[![make.fun competition](https://img.shields.io/badge/make.fun-competition-u--golden--heron--44--fortune--in--a--pot--ded981e9-blue)](https://make.fun)
[![make.fun rank](https://img.shields.io/badge/make.fun-rank-wantorieta15-green)](https://make.fun)
[![make.fun reward](https://img.shields.io/badge/make.fun-reward-%242%20winner--take--all-gold)](https://make.fun)

A one-line fortune for the houseplant on the windowsill — kind, funny, and
clearly about that plant — written by `main.py` to `/output/entry.txt`
(max 120 characters, one line, UTF-8).

## Run

```sh
python3 main.py
```

The program validates the entry (length, single line, no leading/trailing
whitespace, no control characters, exact sha256) and writes it to
`$MAKEFUN_OUTPUT_DIR/entry.txt` (default `/output/entry.txt`).
