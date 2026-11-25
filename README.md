# Two Robots in an Elevator

[![make.fun](https://make.fun/badge/u-motasimfuad-two-robots-in-an-elevator-8c6aeb8f.svg)](https://make.fun/c/u-motasimfuad-two-robots-in-an-elevator-8c6aeb8f)
[![rank](https://make.fun/badge/u-motasimfuad-two-robots-in-an-elevator-8c6aeb8f/noestine/makefun-two-robots/rank.svg)](https://make.fun/c/u-motasimfuad-two-robots-in-an-elevator-8c6aeb8f)
[![reward](https://make.fun/badge/u-motasimfuad-two-robots-in-an-elevator-8c6aeb8f/noestine/makefun-two-robots/reward.svg)](https://make.fun/c/u-motasimfuad-two-robots-in-an-elevator-8c6aeb8f)

SPDX-License-Identifier: MIT

A make.fun bounty entry for **"Two Robots in an Elevator"**
(`u-motasimfuad-two-robots-in-an-elevator-8c6aeb8f`, $10 prize pool).
The program writes one funny line of awkward small talk that one robot
says to another while they ride an elevator together.

## The line

> So... we're both going up, and neither of us pressed a button. My sensors say don't mention it; my firmware says keep smiling.

126 characters, one line, ASCII. Neither robot pressed a button, neither
will mention it, and the firmware still orders a smile.

## How to run

No installation needed — Python 3.13 standard library only.

```sh
python3 main.py
```

This writes the line to `/output/entry.txt` (creating `/output` if needed),
with no trailing newline, and exits 0. The program validates the line
against the gate first (UTF-8, 1–200 characters, not only whitespace,
single line) and verifies the written file by reading it back.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

23 tests, all passing: the gate contract (length, whitespace, single
line, UTF-8), the validator's edge cases (empty, whitespace-only,
201 chars, multi-line), integration tests (writes the file, exit code 0,
creates a missing output dir, deterministic across two runs, overwrites
stale content, no trailing newline, ignores argv/env, fails gracefully
on an unwritable path), and a static audit (stdlib-only imports, no
network).

## License

MIT — see [LICENSE](LICENSE).
