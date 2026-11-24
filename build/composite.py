#!/usr/bin/env python3
"""Compose the front page for Tuesday 24 November 2026.

The artwork arrives as one generated sheet holding six flat editorial
panels in a 3-by-2 grid (build/grid20261124.png). This script finds the
panels on the sheet, lifts each one out, and lays the six of them onto
a broadsheet-style page: a masthead that names the day, then two rows
of three panels, every panel captioned with a headline and a one-line
summary typeset here, so the only words on the page are crisp vector
text rather than anything the image model drew.

Output: assets/day.png, 1024x1024, at most 1 MiB.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SHEET = HERE / "grid20261124.png"
PANEL_DIR = HERE / "panels"
OUTPUT = ROOT / "assets" / "day.png"

PAGE = 1024
PAPER = (245, 240, 227)
INK = (26, 24, 20)
GREY = (92, 86, 76)
ACCENT = (176, 58, 46)

MARGIN = 22
GUTTER = 14
MASTHEAD_H = 138
FOOT = 18
IMG_H = 310

# (headline, summary) in reading order: left to right, top row first.
STORIES = [
    (
        "Ukraine sinks Russian warship off Libya",
        "Naval drones strike the corvette Merkury at Benghazi",
    ),
    (
        "NATO vows defence against space threat",
        "Alliance answers reports of a Russian nuclear satellite",
    ),
    (
        "Huang back at Nvidia as markets surge",
        "CEO reinstated after ouster; Nasdaq leaps 6.5%",
    ),
    (
        "Israeli strike kills Hamas security chief",
        "Gaza City raid kills Abu Nahel and six others",
    ),
    (
        "Iran vows to defy Hormuz blockade",
        "Tehran threatens tanker escorts; Qatar seeks talks",
    ),
    (
        "China opens station to first foreign astronaut",
        "Pakistan's Zeeshan Ali joins the Shenzhou-24 crew",
    ),
]


def find_font(candidates, size):
    """Return the first available font from a list of file names."""
    search_dirs = [
        Path("/usr/share/fonts/truetype/dejavu"),
        Path("/usr/share/fonts/truetype/liberation"),
        Path("/usr/share/fonts/truetype/noto"),
    ]
    for name in candidates:
        for directory in search_dirs:
            path = directory / name
            if path.is_file():
                return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def panel_bands(sheet):
    """Locate the six panel rectangles on the artwork sheet.

    Works on a small copy: pixels that are not the pale paper colour
    belong to a panel or its border. Rows and columns that are mostly
    non-paper form bands; the panels are where a row band and a column
    band cross.
    """
    small = sheet.convert("RGB").resize((256, 256))
    px = small.load()

    def is_art(x, y):
        r, g, b = px[x, y]
        return not (r > 205 and g > 195 and b > 175)

    def bands(flags, minimum):
        found, start = [], None
        for i, flag in enumerate(flags):
            if flag and start is None:
                start = i
            elif not flag and start is not None:
                if i - start >= minimum:
                    found.append((start, i))
                start = None
        if start is not None and len(flags) - start >= minimum:
            found.append((start, len(flags)))
        return found

    rows = bands(
        [sum(is_art(x, y) for x in range(256)) > 128 for y in range(256)], 40
    )
    cols = bands(
        [sum(is_art(x, y) for y in range(256)) > 128 for x in range(256)], 40
    )
    if len(rows) != 2 or len(cols) != 3:
        raise RuntimeError(f"expected 2x3 panels, found {len(rows)}x{len(cols)}")

    scale = sheet.width / 256
    boxes = []
    for top, bottom in rows:
        for left, right in cols:
            # Shrink by ~1.5% of the panel size to step inside the border.
            w = (right - left) * scale
            h = (bottom - top) * scale
            boxes.append(
                (
                    int(left * scale + w * 0.015),
                    int(top * scale + h * 0.015),
                    int(right * scale - w * 0.015),
                    int(bottom * scale - h * 0.015),
                )
            )
    return boxes


def fit_crop(image, target_w, target_h):
    """Centre-crop an image to the target aspect, then resize to it."""
    scale = max(target_w / image.width, target_h / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.LANCZOS,
    )
    x = (resized.width - target_w) // 2
    y = (resized.height - target_h) // 2
    return resized.crop((x, y, x + target_w, y + target_h))


def wrap(draw, text, font, width):
    """Split text into lines that fit the given pixel width."""
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def build_page():
    sheet = Image.open(SHEET)
    boxes = panel_bands(sheet)

    PANEL_DIR.mkdir(parents=True, exist_ok=True)
    panels = []
    for index, box in enumerate(boxes, start=1):
        panel = sheet.crop(box)
        panel.save(PANEL_DIR / f"panel{index}.png")
        panels.append(panel)

    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(page)

    # Masthead: the paper's name, then the day it sums up.
    title_font = find_font(
        ["DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf", "NotoSerif-Bold.ttf"],
        55,
    )
    date_font = find_font(
        ["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "NotoSans-Bold.ttf"],
        25,
    )
    title = "THE WORLD IN ONE DAY"
    title_w = draw.textlength(title, font=title_font)
    draw.text(((PAGE - title_w) / 2, 16), title, font=title_font, fill=INK)
    date_line = "Tuesday 24 November 2026"
    date_w = draw.textlength(date_line, font=date_font)
    draw.text(((PAGE - date_w) / 2, 86), date_line, font=date_font, fill=ACCENT)
    draw.line([(MARGIN, 126), (PAGE - MARGIN, 126)], fill=INK, width=3)
    draw.line([(MARGIN, 131), (PAGE - MARGIN, 131)], fill=INK, width=1)

    head_font = find_font(
        ["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "NotoSans-Bold.ttf"],
        21,
    )
    sum_font = find_font(
        ["DejaVuSans.ttf", "LiberationSans-Regular.ttf", "NotoSans-Regular.ttf"],
        16,
    )

    cell_w = (PAGE - 2 * MARGIN - 2 * GUTTER) // 3
    grid_top = MASTHEAD_H
    row_h = (PAGE - grid_top - FOOT - GUTTER) // 2

    for index, (panel, (headline, summary)) in enumerate(zip(panels, STORIES)):
        row, col = divmod(index, 3)
        x = MARGIN + col * (cell_w + GUTTER)
        y = grid_top + row * (row_h + GUTTER)

        art = fit_crop(panel, cell_w, IMG_H)
        page.paste(art, (x, y))
        draw.rectangle(
            [x, y, x + cell_w - 1, y + IMG_H - 1], outline=INK, width=2
        )

        text_y = y + IMG_H + 8
        for line in wrap(draw, headline, head_font, cell_w):
            draw.text((x, text_y), line, font=head_font, fill=INK)
            text_y += 25
        text_y += 2
        for line in wrap(draw, summary, sum_font, cell_w):
            draw.text((x, text_y), line, font=sum_font, fill=GREY)
            text_y += 20

    return page


def save(page):
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    page.save(OUTPUT, optimize=True)
    size = OUTPUT.stat().st_size
    if size > 1_048_576:
        # Flat artwork survives an adaptive palette almost untouched.
        page.convert("P", palette=Image.ADAPTIVE, colors=256).save(
            OUTPUT, optimize=True
        )
        size = OUTPUT.stat().st_size
    print(f"wrote {OUTPUT} ({size} bytes)")


if __name__ == "__main__":
    save(build_page())
