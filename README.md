[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/net-ybb97/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/net-ybb97/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# The World in One Day — 24 November 2026

Entry for the make.fun competition **news-image-20261124**: sum up the
world news of Tuesday, 24 November 2026 in a single 1024×1024 image.

The page is a broadsheet front page with six flat editorial panels,
each captioned with a typeset headline:

1. **Ukraine sinks Russian warship off Libya** — naval drones strike
   the corvette Merkury at Benghazi; Kyiv confirms the attack as Libya
   demands an explanation.
2. **NATO vows defence against space threat** — the alliance answers
   reports that Russia is preparing a nuclear-armed satellite.
3. **Huang back at Nvidia as markets surge** — the board reinstates
   Jensen Huang as CEO and the Nasdaq leaps 6.5% in a tech rally.
4. **Israeli strike kills Hamas security chief** — a Gaza City raid
   kills Naeem Abu Nahel and six others.
5. **Iran vows to defy Hormuz blockade** — Tehran threatens armed
   tanker escorts against the US naval blockade while Qatar seeks to
   revive talks.
6. **China opens station to first foreign astronaut** — Pakistan's
   Zeeshan Ali joins the Shenzhou-24 crew aboard Tiangong.

## How it works

- `build/composite.py` finds the six artwork panels on the generated
  sheet, lays out the page and typesets the masthead and captions into
  `assets/day.png` (1024×1024, under 1 MiB).
- `main.py` is the entry program: it copies `assets/day.png` to
  `/output/entry.png` byte for byte and verifies the SHA-256 of the
  written file, so repeated runs always emit the same image.

## License

MIT — see `LICENSE`.
