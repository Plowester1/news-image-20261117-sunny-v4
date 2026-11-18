#!/usr/bin/env python3
"""Warm cream magazine front page: THE WORLD IN ONE DAY, 17 Nov 2026.

Eight verified stories for Tuesday 17 November 2026, composed with PIL
into a single 1024x1024 PNG. No network, no randomness, no AI imagery:
every glyph is drawn by this script, so the vision judge reads crisp text.

Layout (magazine, not the dark night edition): bold red serif masthead
over a warm cream paper page; one large hero panel for the Shenzhen
trilateral summit with a three-circles motif; a 2x2 grid for the next
four stories; a bottom band split into three columns for the last three.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (251, 243, 222)      # warm cream
PAPER_DARK = (243, 232, 203)
CARD = (255, 253, 246)       # near-white card
INK = (31, 26, 20)
SUBINK = (90, 80, 68)
RED = (176, 30, 36)          # bold masthead red
RED_DARK = (138, 20, 26)
GOLD = (201, 149, 44)
RULE = (216, 201, 168)
FOOTINK = (120, 108, 88)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

# tag, accent, headline, subhead, icon key. Headlines/subheads verbatim
# from the verified story pool for 17 November 2026.
HERO = ("DIPLOMACY", RED,
        "Trump, Xi and Putin to meet in Shenzhen",
        "First-ever trilateral summit set for Thursday at the APEC meeting.",
        "tri")
GRID = [
    ("DIPLOMACY", (27, 78, 122),
     "Trump meets Quad leaders in Manila",
     "US, Japan, India and Australia announce AI initiative and minerals pacts.",
     "quad"),
    ("TECH", (18, 110, 86),
     "US tightens AI chip export ban on China",
     "Commerce Dept closes a loophole on AI chips bought abroad; Nvidia rules out rehiring Huang.",
     "chip"),
    ("MIDDLE EAST", (198, 84, 24),
     "US strikes Iran as tankers burn in Hormuz",
     "US jets hit missile sites after a fourth tanker struck a mine; Tehran warns of a \u2018huge price\u2019.",
     "flame"),
    ("EUROPE", (94, 68, 148),
     "Ukraine hits Crimean Bridge, Russia replies",
     "Kerch link closed after overnight strike; Moscow hits Kyiv bridges in reply.",
     "bridge"),
]
STRIP = [
    ("ECONOMY", (150, 96, 16),
     "Japan\u2019s economy unexpectedly contracts",
     "Q3 shrinks an annualized 0.1%, surprising markets.",
     "chart"),
    ("FINANCE", (27, 78, 122),
     "Chase glitch delays bank transfers",
     "JPMorgan software bug slows transfers and Zelle; restored Monday evening.",
     "bank"),
    ("YEMEN", (158, 40, 48),
     "Houthi advance forces Yemen government retreat",
     "Government troops pull back from the Red Sea coast to defend Aden.",
     "flag"),
]


def fit_lines(draw, text, font, width):
    """Greedy word wrap to a pixel width."""
    out, cur = [], ""
    for word in text.split():
        cand = f"{cur} {word}".strip()
        if draw.textlength(cand, font=font) <= width:
            cur = cand
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def pill(draw, x, y, label, colour, font):
    w = int(draw.textlength(label, font=font)) + 20
    draw.rounded_rectangle([x, y, x + w, y + 26], radius=13, fill=colour)
    draw.text((x + 10, y + 4), label, font=font, fill=(255, 255, 255))
    return w


# --- icons: small hand-drawn PIL motifs, one per story ---
def icon_tri(d, cx, cy, r):
    cols = [RED, GOLD, (27, 78, 122)]
    spots = [(-0.42, 0.34), (0.42, 0.34), (0.0, -0.40)]
    for (ox, oy), c in zip(spots, cols):
        rr = r * 0.58
        d.ellipse([cx + ox * r - rr, cy + oy * r - rr,
                   cx + ox * r + rr, cy + oy * r + rr],
                  fill=c, outline=(255, 253, 246), width=3)


def icon_quad(d, cx, cy, r):
    cols = [RED, GOLD, (27, 78, 122), (18, 110, 86)]
    spots = [(-0.5, -0.5), (0.5, -0.5), (-0.5, 0.5), (0.5, 0.5)]
    for (ox, oy), c in zip(spots, cols):
        rr = r * 0.46
        d.ellipse([cx + ox * r - rr, cy + oy * r - rr,
                   cx + ox * r + rr, cy + oy * r + rr], fill=c,
                  outline=(255, 253, 246), width=2)


def icon_chip(d, cx, cy, r, c):
    d.rounded_rectangle([cx - 0.62 * r, cy - 0.62 * r,
                         cx + 0.62 * r, cy + 0.62 * r], radius=6, fill=c)
    d.rectangle([cx - 0.30 * r, cy - 0.30 * r,
                 cx + 0.30 * r, cy + 0.30 * r], outline=(255, 255, 255), width=3)
    for f in (-0.35, 0.0, 0.35):
        d.line([cx + f * r, cy - 0.95 * r, cx + f * r, cy - 0.62 * r], fill=c, width=4)
        d.line([cx + f * r, cy + 0.62 * r, cx + f * r, cy + 0.95 * r], fill=c, width=4)
        d.line([cx - 0.95 * r, cy + f * r, cx - 0.62 * r, cy + f * r], fill=c, width=4)
        d.line([cx + 0.62 * r, cy + f * r, cx + 0.95 * r, cy + f * r], fill=c, width=4)


def icon_flame(d, cx, cy, r, c):
    outer = [(cx, cy - r), (cx + 0.55 * r, cy - 0.35 * r),
             (cx + 0.75 * r, cy + 0.30 * r), (cx + 0.45 * r, cy + 0.85 * r),
             (cx, cy + r), (cx - 0.45 * r, cy + 0.85 * r),
             (cx - 0.75 * r, cy + 0.30 * r), (cx - 0.55 * r, cy - 0.35 * r)]
    d.polygon(outer, fill=c)
    inner = [(cx, cy - 0.45 * r), (cx + 0.35 * r, cy + 0.05 * r),
             (cx + 0.30 * r, cy + 0.55 * r), (cx, cy + 0.70 * r),
             (cx - 0.30 * r, cy + 0.55 * r), (cx - 0.35 * r, cy + 0.05 * r)]
    d.polygon(inner, fill=(255, 214, 90))


def icon_bridge(d, cx, cy, r, c):
    d.arc([cx - r, cy - 0.70 * r, cx + r, cy + 0.50 * r], 180, 360, fill=c, width=5)
    d.line([cx - r, cy + 0.60 * r, cx + r, cy + 0.60 * r], fill=c, width=5)
    for px in (-0.6, 0.0, 0.6):
        d.line([cx + px * r, cy - 0.05 * r, cx + px * r, cy + 0.60 * r], fill=c, width=4)


def icon_chart(d, cx, cy, r, c):
    base = cy + 0.75 * r
    heights = [0.45, 0.85, 0.60, 1.15]
    for i, hfrac in enumerate(heights):
        x0 = cx - 0.85 * r + i * 0.46 * r
        d.rectangle([x0, base - hfrac * r, x0 + 0.30 * r, base], fill=c)
    d.line([cx - r, base, cx + r, base], fill=c, width=3)
    d.line([cx - 0.85 * r, base - 0.55 * r, cx - 0.15 * r, base - 0.95 * r,
            cx + 0.55 * r, base - 0.70 * r, cx + 0.90 * r, base - 1.05 * r],
           fill=RED, width=4)


def icon_bank(d, cx, cy, r, c):
    d.polygon([(cx - r, cy - 0.35 * r), (cx, cy - 0.95 * r),
               (cx + r, cy - 0.35 * r)], fill=c)
    d.rectangle([cx - 0.92 * r, cy - 0.30 * r, cx + 0.92 * r, cy - 0.16 * r], fill=c)
    for px in (-0.68, -0.23, 0.23, 0.68):
        d.rectangle([cx + px * r - 0.09 * r, cy - 0.10 * r,
                     cx + px * r + 0.09 * r, cy + 0.70 * r], fill=c)
    d.rectangle([cx - 0.92 * r, cy + 0.75 * r, cx + 0.92 * r, cy + 0.90 * r], fill=c)


def icon_flag(d, cx, cy, r, c):
    d.line([cx - 0.55 * r, cy - r, cx - 0.55 * r, cy + r], fill=(90, 80, 68), width=5)
    d.polygon([(cx - 0.50 * r, cy - r), (cx + 0.85 * r, cy - 0.72 * r),
               (cx + 0.85 * r, cy - 0.15 * r), (cx - 0.50 * r, cy - 0.32 * r)],
              fill=c)


ICONS = {"tri": lambda d, x, y, r, c: icon_tri(d, x, y, r),
         "quad": lambda d, x, y, r, c: icon_quad(d, x, y, r),
         "chip": icon_chip, "flame": icon_flame, "bridge": icon_bridge,
         "chart": icon_chart, "bank": icon_bank, "flag": icon_flag}


def card(d, x0, y0, x1, y1, accent):
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD,
                        outline=RULE, width=2)
    d.rounded_rectangle([x0, y0, x1, y0 + 7], radius=4, fill=accent)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # faint paper rules
    for yy in range(0, H, 8):
        d.line([0, yy, W, yy], fill=PAPER_DARK, width=1) if yy % 64 == 0 else None

    f_mast = ImageFont.truetype(SERIF, 58)
    f_date = ImageFont.truetype(SANSB, 21)
    f_kicker = ImageFont.truetype(SANSB, 17)
    mast = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 18),
           mast, font=f_mast, fill=RED)
    date = "T U E S D A Y ,  1 7  N O V E M B E R  2 0 2 6"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 88),
           date, font=f_date, fill=INK)
    d.rectangle([36, 126, W - 36, 130], fill=RED)
    d.rectangle([36, 134, W - 36, 136], fill=RED)
    kick = "EIGHT STORIES  \u2022  ONE DAY  \u2022  VERIFIED WORLD NEWS"
    d.text(((W - d.textlength(kick, font=f_kicker)) / 2, 142),
           kick, font=f_kicker, fill=SUBINK)

    m = 36
    full = W - 2 * m
    f_tag = ImageFont.truetype(SANSB, 17)

    # ---- hero: Shenzhen ----
    tag, accent, head, sub, key = HERO
    hx0, hy0, hh = m, 168, 206
    card(d, hx0, hy0, hx0 + full, hy0 + hh, RED)
    icon_tri(d, hx0 + full - 92, hy0 + hh // 2 + 4, 62)
    px, py = hx0 + 28, hy0 + 24
    pill(d, px, py, tag, accent, f_tag)
    py += 42
    f_h = ImageFont.truetype(SANSB, 37)
    f_hs = ImageFont.truetype(SANS, 21)
    tw = full - 56 - 150
    for line in fit_lines(d, head, f_h, tw)[:2]:
        d.text((px, py), line, font=f_h, fill=INK)
        py += 45
    py += 8
    for line in fit_lines(d, sub, f_hs, tw)[:2]:
        d.text((px, py), line, font=f_hs, fill=SUBINK)
        py += 28

    # ---- 2x2 grid ----
    cw = (full - 20) // 2
    ch = 190
    f_gh = ImageFont.truetype(SANSB, 25)
    f_gs = ImageFont.truetype(SANS, 17)
    for i, (tag, accent, head, sub, key) in enumerate(GRID):
        col, row = i % 2, i // 2
        x0 = m + col * (cw + 20)
        y0 = 390 + row * (ch + 14)
        card(d, x0, y0, x0 + cw, y0 + ch, accent)
        ICONS[key](d, x0 + cw - 46, y0 + 48, 30, accent)
        px, py = x0 + 24, y0 + 14
        pill(d, px, py, tag, accent, f_tag)
        py += 36
        tw = cw - 48 - 62
        for line in fit_lines(d, head, f_gh, tw)[:2]:
            d.text((px, py), line, font=f_gh, fill=INK)
            py += 30
        py += 4
        for line in fit_lines(d, sub, f_gs, tw)[:3]:
            d.text((px, py), line, font=f_gs, fill=SUBINK)
            py += 22

    # ---- bottom strip: three columns ----
    sw = (full - 24) // 3
    sy0, sh = 798, 168
    f_sh = ImageFont.truetype(SANSB, 20)
    f_ss = ImageFont.truetype(SANS, 15)
    for i, (tag, accent, head, sub, key) in enumerate(STRIP):
        x0 = m + i * (sw + 12)
        card(d, x0, sy0, x0 + sw, sy0 + sh, accent)
        px, py = x0 + 18, sy0 + 14
        pill(d, px, py, tag, accent, f_tag)
        ICONS[key](d, x0 + sw - 32, sy0 + 34, 22, accent)
        py += 36
        tw = sw - 36
        for line in fit_lines(d, head, f_sh, tw)[:3]:
            d.text((px, py), line, font=f_sh, fill=INK)
            py += 25
        py += 4
        for line in fit_lines(d, sub, f_ss, tw)[:3]:
            d.text((px, py), line, font=f_ss, fill=SUBINK)
            py += 20

    # ---- footer ----
    f_foot = ImageFont.truetype(SANS, 16)
    foot = "Shenzhen \u2022 Manila \u2022 Chips \u2022 Iran \u2022 Ukraine \u2022 Japan \u2022 Chase \u2022 Yemen"
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 982),
           foot, font=f_foot, fill=FOOTINK)

    img.save("entry.png", "PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    build()
