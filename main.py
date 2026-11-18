#!/usr/bin/env python3
"""World news of Tuesday 17 November 2026, summed up in one image.

Deterministic: no network, no clock, no randomness. Draws a 1024x1024
PNG with Pillow from the fixed story list below and writes it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

Stories were researched on 18 Nov 2026 from Reuters, CNN, PAHO and IOM
reporting of 17 Nov 2026; full sources are in SOURCES.md.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 234)
NAVY = (11, 37, 69)
GOLD = (232, 184, 75)
INK = (17, 24, 39)
GREY = (71, 85, 105)
CARD = (255, 255, 255)
LINE = (216, 210, 196)

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def font(bold, size):
    for p in FONT_PATHS:
        if bold and "Bold" in p and os.path.exists(p):
            return ImageFont.truetype(p, size)
        if not bold and "Bold" not in p and os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


STORIES = [
    {
        "kicker": "MIDDLE EAST  •  HORMUZ",
        "color": (180, 35, 24),
        "headline": "U.S. Jets Strike Iran's Qeshm Island",
        "fact": "Retaliation for a drone attack on a U.S. radar base in Bahrain. An ADNOC vessel was also attacked in the Strait; 11 crew hurt, 1 missing.",
        "icon": "ship",
    },
    {
        "kicker": "UKRAINE  •  EUROPE",
        "color": (29, 78, 216),
        "headline": "Ukraine Destroys Crimea Bridge Span",
        "fact": "Second day of strikes on the 19 km bridge; 2 killed, traffic halted. Russia hit Kyiv bridges in reply.",
        "icon": "bridge",
    },
    {
        "kicker": "GAZA  •  MIDDLE EAST",
        "color": (124, 58, 237),
        "headline": "Gaza Winter Rains Flood Tents, Babies at Risk",
        "fact": "UN warns of more hypothermia deaths; a 9-month-old died of cold. About 100,000 tents are waiting to enter.",
        "icon": "tent",
    },
    {
        "kicker": "JAPAN  •  ASIA",
        "color": (14, 116, 144),
        "headline": "Russian Jets Breach Japan Airspace",
        "fact": "Two suspected Russian jets entered near Okinoshima for about 3 minutes each — first breach since Sept 2024.",
        "icon": "jet",
    },
    {
        "kicker": "UNITED STATES  •  HEALTH",
        "color": (21, 128, 61),
        "headline": "U.S. Loses Measles-Free Status After 26 Years",
        "fact": "PAHO confirms 12 months of spread; 5,412 cases in 2026, the most in 35 years.",
        "icon": "virus",
    },
    {
        "kicker": "DIPLOMACY  •  APEC",
        "color": (180, 83, 9),
        "headline": "Trump, Xi, Putin to Meet Thursday",
        "fact": "First trilateral summit set for Thu 19 Nov in Shenzhen, at APEC. Nuclear arms cuts are on the agenda.",
        "icon": "summit",
    },
]


def draw_icon(d, kind, x, y, s, color):
    if kind == "ship":
        d.polygon([(x, y + 40), (x + s, y + 40), (x + s - 12, y + 58),
                   (x + 12, y + 58)], fill=color)
        d.rectangle([x + 24, y + 20, x + 46, y + 40], fill=color)
        d.rectangle([x + 32, y + 8, x + 38, y + 20], fill=color)
        for wx in [x, x + 22, x + 44]:
            d.arc([wx, y + 58, wx + 24, y + 70], 0, 180, fill=color, width=4)
        d.polygon([(x + 54, y + 2), (x + 60, y + 12), (x + 70, y + 4),
                   (x + 63, y + 14), (x + 70, y + 22), (x + 58, y + 20),
                   (x + 56, y + 30), (x + 51, y + 20), (x + 42, y + 22),
                   (x + 49, y + 13), (x + 43, y + 6), (x + 52, y + 11)],
                  fill=(245, 158, 11))
    elif kind == "bridge":
        d.arc([x, y + 10, x + s, y + 62], 180, 360, fill=color, width=7)
        d.line([x, y + 34, x + s, y + 34], fill=color, width=7)
        d.line([x + 12, y + 34, x + 12, y + 62], fill=color, width=5)
        d.line([x + s - 12, y + 34, x + s - 12, y + 62], fill=color, width=5)
        d.line([x + s // 2 - 14, y + 8, x + s // 2 + 14, y + 38],
               fill=(180, 35, 24), width=6)
        d.line([x + s // 2 + 14, y + 8, x + s // 2 - 14, y + 38],
               fill=(180, 35, 24), width=6)
    elif kind == "tent":
        d.polygon([(x + s // 2, y + 6), (x + 4, y + 52), (x + s - 4, y + 52)],
                  outline=color, width=6)
        d.line([x + s // 2, y + 6, x + s // 2, y + 52], fill=color, width=4)
        for rx in [x + 8, x + 28, x + 48]:
            d.line([rx, y + 58, rx - 6, y + 70], fill=(29, 78, 216), width=4)
    elif kind == "jet":
        d.polygon([(x + s - 4, y + s // 2), (x + 10, y + 10), (x + 20, y + s // 2 - 6),
                   (x + 20, y + s // 2 + 6), (x + 10, y + s - 10)], fill=color)
        d.polygon([(x + 14, y + s // 2 - 4), (x + 34, y + 4), (x + 34, y + s // 2 - 4)],
                  fill=color)
        d.polygon([(x + 14, y + s // 2 + 4), (x + 34, y + s - 4), (x + 34, y + s // 2 + 4)],
                  fill=color)
        for i in range(3):
            d.line([x, y + 16 + i * 16, x - 12, y + 16 + i * 16],
                   fill=(100, 116, 139), width=3)
    elif kind == "virus":
        d.ellipse([x + 14, y + 14, x + s - 14, y + s - 14], fill=color)
        for a in range(0, 360, 45):
            import math
            r = math.radians(a)
            x1 = x + s // 2 + int(24 * math.cos(r))
            y1 = y + s // 2 + int(24 * math.sin(r))
            x2 = x + s // 2 + int(34 * math.cos(r))
            y2 = y + s // 2 + int(34 * math.sin(r))
            d.line([x1, y1, x2, y2], fill=color, width=5)
        d.ellipse([x + 26, y + 26, x + 38, y + 38], fill=(255, 255, 255))
        d.ellipse([x + 42, y + 40, x + 50, y + 48], fill=(255, 255, 255))
    elif kind == "summit":
        cols = [(180, 35, 24), (29, 78, 216), (245, 158, 11)]
        for i, c in enumerate(cols):
            cx = x + 14 + i * 22
            d.ellipse([cx, y + 18, cx + 26, y + 44], fill=c,
                      outline=(255, 255, 255), width=2)
        d.rectangle([x + 8, y + 50, x + s - 8, y + 62], fill=NAVY)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 156], fill=GOLD)
    f_date = font(True, 56)
    f_sub = font(True, 28)
    d.text((W // 2, 52), "TUESDAY 17 NOVEMBER 2026", font=f_date,
           fill=(255, 255, 255), anchor="mm")
    d.text((W // 2, 112), "THE WORLD IN ONE DAY  •  SIX STORIES",
           font=f_sub, fill=GOLD, anchor="mm")

    # Story grid: 2 columns x 3 rows
    gx, gy = 16, 168
    pw, ph, gap = 490, 262, 12
    f_kick = font(True, 17)
    f_head = font(True, 27)
    f_fact = font(False, 18)
    for i, s in enumerate(STORIES):
        x = gx + (i % 2) * (pw + gap)
        y = gy + (i // 2) * (ph + gap)
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=10,
                            fill=CARD, outline=LINE, width=2)
        d.rectangle([x, y, x + pw, y + 8], fill=s["color"])
        d.text((x + 18, y + 26), s["kicker"], font=f_kick, fill=s["color"])
        draw_icon(d, s["icon"], x + pw - 88, y + 18, 68, s["color"])
        tx = x + 18
        tw = pw - 36
        lines = wrap(d, s["headline"], f_head, tw - 96)
        ly = y + 56
        for ln in lines[:3]:
            d.text((tx, ly), ln, font=f_head, fill=INK)
            ly += 33
        flines = wrap(d, s["fact"], f_fact, tw)
        ly += 6
        for ln in flines[:3]:
            d.text((tx, ly), ln, font=f_fact, fill=GREY)
            ly += 23

    # Footer
    f_foot = font(False, 16)
    d.text((W // 2, 1002),
           "Sources: Reuters  •  CNN  •  PAHO  •  IOM  —  All events reported on 17 November 2026",
           font=f_foot, fill=GREY, anchor="mm")

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "entry.png")
    img.save(out, "PNG", compress_level=6)
    print("wrote", out)


if __name__ == "__main__":
    main()
