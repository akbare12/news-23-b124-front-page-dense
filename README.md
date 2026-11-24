# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b124-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b124-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-image front page summing up 23 November 2026's world news: 31 stories in one
1024×1024 image — the AI rout hitting Asian markets, the UN chief's call to regulate
AI before it's too late, and the US lead over China at a record low.

## What's inside

- **Masthead + kicker** — THE WORLD TODAY, Monday 23 November 2026.
- **Number strip** — the day's ten defining figures at a glance.
- **Region bar** — 31 stories across Asia-Pacific (7), Americas (8), Middle East (6),
  Europe (5), Africa (3) and the World (2).
- **3 hero scenes** — Kospi's −3.3% slide, the Bridgetown AI summit, the Asia Power
  Index 2026.
- **10 cards** — the rest of the day's news, each marked REPORTED (confirmed by wires)
  or CLAIM (one side's claim, independently unconfirmed).
- **World map + numbered pins** and an 18-item ALSO list.
- **DATE CHECK** — stories dated 23 Nov only; items from other days are listed as
  LEFT OUT, and open items as NOT YET.

## How to run

```sh
python3 draw.py            # regenerates entry.png (1024x1024, < 1 MiB)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # validates + copies entry.png to out/
```

`main.py` is stdlib-only: it parses the PNG header and chunk structure by hand and
writes only to `$MAKEFUN_OUTPUT_DIR/entry.png`, never next to itself.
