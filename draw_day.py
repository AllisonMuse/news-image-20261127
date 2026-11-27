#!/usr/bin/env python3
"""Draw the 27 November 2026 world-news image for make.fun.

One self-contained picture: header, a drawn world map with numbered pins,
five small drawn scenes, the day's stories grouped by region, a UTC timeline
and a date-check footer. Output is a deterministic 1024x1024 PNG.
Run:  python3 draw_day.py   (writes entry.png next to this file)
"""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (247, 243, 234, 255)
INK = (28, 28, 28, 255)
GREY = (90, 90, 88, 255)
NAVY = (20, 33, 61, 255)
GOLD = (201, 162, 39, 255)
SEA = (205, 224, 233, 255)
LAND = (133, 164, 115, 255)
LAND_EDGE = (92, 122, 80, 255)
PIN = (192, 57, 43, 255)

REGION_COLOURS = {
    "NORTH AMERICA": (31, 78, 121),
    "MIDDLE EAST": (146, 43, 33),
    "EUROPE": (39, 92, 68),
    "EAST ASIA": (122, 48, 108),
    "SOUTH ASIA": (176, 96, 16),
    "SOUTH-EAST ASIA": (14, 120, 110),
    "OCEANIA": (64, 110, 160),
    "AFRICA": (140, 110, 20),
    "LATIN AMERICA": (90, 60, 140),
    "WORLD & SPORT": (70, 70, 70),
}

# (number, region, headline, subline, source)
STORIES = [
    (1, "NORTH AMERICA", "Trump lashes out in Thanksgiving message",
     "Foes, immigrants and the federal government in the firing line", "AP"),
    (2, "NORTH AMERICA", "Trump calls GDP figures \u201cfake\u201d, demands probe",
     "Q3 growth revised up to 4.3% after the midterms", "AP"),
    (3, "NORTH AMERICA", "Trump defends Huang\u2019s return as Nvidia chief",
     "\u201cEverybody\u2019s replaceable,\u201d he says of the CEO", "Economic Times"),
    (4, "NORTH AMERICA", "Trump: Putin \u201cwould like to make a deal\u201d",
     "Says Putin can attend the G20 in Miami", "Deccan Chronicle"),
    (5, "NORTH AMERICA", "Storm batters the US on Thanksgiving",
     "Holiday travel hit as a nor\u2019easter moves in", "Deccan Chronicle"),
    (6, "NORTH AMERICA", "King tides flood the California coast",
     "Pacifica Pier collapses; records fall", "weather.com"),
    (7, "NORTH AMERICA", "Eagles\u2019 21-point Thanksgiving comeback",
     "59-yard field goal sinks the Cowboys", "AP"),
    (8, "MIDDLE EAST", "Kuwait drone attack kills two Italians",
     "Iran calls it \u201csuspicious\u201d and denies any role", "Al Jazeera"),
    (9, "MIDDLE EAST", "Houthis hit Saudi Jazan refinery",
     "One worker killed; operations halted", "Al Jazeera"),
    (10, "MIDDLE EAST", "Tankers \u201chit mines\u201d near Khasab",
     "IRGC claim, unverified", "Times Now"),
    (11, "MIDDLE EAST", "Israeli strikes kill 10 in Gaza",
     "Hamas education deputy among the dead", "Deccan Chronicle"),
    (12, "MIDDLE EAST", "Brent crude near $96 a barrel",
     "First weekly gain in a month", "Reuters"),
    (13, "MIDDLE EAST", "Saudi jets strike Mocha, Yemen",
     "Nine civilians hurt in Taiz shelling", "Al Jazeera"),
    (14, "EUROPE", "UK net migration falls to 77,000",
     "Lowest since 1997, excluding Covid", "Reuters"),
    (15, "EUROPE", "EU picks Hernandez de Cos as ECB chief",
     "Succeeds Lagarde in February 2027", "Reuters"),
    (16, "EUROPE", "Depardieu to stand trial over rape claim",
     "Paris court orders trial; he denies wrongdoing", "Al Jazeera"),
    (17, "EUROPE", "Sweden summons Russian envoy",
     "Over Polish airspace breach and Denmark plot", "government.se"),
    (18, "EUROPE", "Russian drones kill 3 in Ukraine",
     "At least 10 injured overnight", "Kyiv Post"),
    (19, "EUROPE", "Besiktas\u2013Hapoel halted 30 minutes",
     "Palestine banner, pepper spray in Batumi", "Al Jazeera"),
    (20, "EUROPE", "Davis Cup: Britain beats Germany 2\u20131",
     "First semi-final in seven years", "Devdiscourse"),
    (21, "EAST ASIA", "Taiwan votes on Saturday",
     "Cyberattacks surge ahead of local polls", "Nikkei Asia"),
    (22, "EAST ASIA", "Kim vows more nuclear weapons",
     "After ignoring US talks", "Deccan Chronicle"),
    (23, "SOUTH ASIA", "Hasina aide arrested in Bangladesh",
     "Ex-deputy press secretary held", "Economic Times"),
    (24, "SOUTH ASIA", "Afghan women renamed \u201cBibi\u201d, \u201cgoat\u201d",
     "Taliban-ruled Balkh registers new names", "Economic Times"),
    (25, "SOUTH ASIA", "India, UAE fast-track defence tech",
     "Co-development of next-gen equipment", "Deccan Chronicle"),
    (26, "SOUTH ASIA", "Sri Lanka A reach Asia Cup final",
     "Beat India A by eight wickets", "Apex Sports"),
    (27, "SOUTH-EAST ASIA", "Indonesia mine flood: 13 dead",
     "Thirteen more still missing", "Al Jazeera"),
    (28, "SOUTH-EAST ASIA", "Hong Kong warns over fire remembrance",
     "Memorial for 168 killed in blaze", "SCMP"),
    (29, "OCEANIA", "NZ coalition loses its majority",
     "Luxon now needs the Opportunity Party", "Economic Times"),
    (30, "OCEANIA", "Five women \u201cburied alive\u201d in PNG",
     "Sorcery claims spark outrage", "Scoop"),
    (31, "AFRICA", "Zambia: treason trial over \u201ccoup plot\u201d",
     "Prosecutors allege Russia training", "Lansing Institute"),
    (32, "AFRICA", "Kenya court halts Ebola centre",
     "US-backed quarantine build stopped", "Reuters"),
    (33, "AFRICA", "DRC summons Uganda diplomat",
     "Over general\u2019s Walikale posts", "OkayAfrica"),
    (34, "LATIN AMERICA", "Argentina bans money printing",
     "Central bank barred from funding government", "Economic Times"),
    (35, "WORLD & SPORT", "Global trade \u201cset for zero growth\u201d",
     "UN sees flat 2026 maritime trade", "Economic Times"),
    (36, "WORLD & SPORT", "FIFA confirms hackers got in",
     "Limited personal, business data accessed", "Reuters"),
    (37, "WORLD & SPORT", "NZ 131\u20134 at tea in Christchurch Test",
     "Latham 59 on day one v India", "Reuters"),
    (38, "WORLD & SPORT", "Chess: rest day in Geneva",
     "Game 3 drawn; Gukesh\u2013Sindarov 1\u00bd\u20131\u00bd", "The Guardian"),
]

# (story number, lon, lat)
PINS = [
    (1, -77, 39), (6, -122, 37), (8, 48, 29), (11, 34.5, 31.5),
    (14, -0.1, 51.5), (18, 30.5, 50.4), (21, 121.5, 25),
    (29, 174.8, -41.3), (34, -58.4, -34.6), (17, 18, 59),
]

# (UTC time, label) — all reported on 27 November 2026
TIMELINE = [
    ("00:20", "NZ 77\u20131 at lunch, day 1 of 2nd Test"),
    ("01:07", "Storm batters US on Thanksgiving"),
    ("01:41", "Trump defends Huang\u2019s Nvidia return"),
    ("01:57", "Trump calls GDP figures \u201cfake\u201d"),
    ("02:29", "World League condemns refinery hit"),
    ("03:40", "Araghchi: Kuwait attack \u201csuspicious\u201d"),
]

# Simplified continent outlines, (lon, lat) pairs.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-70, 62), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
     (-80, 32), (-81, 25), (-90, 21), (-97, 16), (-94, 17), (-86, 13),
     (-83, 9), (-79, 9), (-92, 15), (-105, 20), (-110, 23), (-114, 29),
     (-120, 34), (-125, 40), (-124, 48), (-135, 58), (-150, 60), (-165, 60)],
    # Greenland
    [(-45, 60), (-30, 68), (-22, 70), (-30, 76), (-55, 76), (-58, 70), (-53, 64)],
    # South America
    [(-79, 9), (-72, 12), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-39, -15), (-48, -27), (-58, -35), (-65, -41), (-68, -52),
     (-70, -54), (-73, -44), (-73, -30), (-70, -18), (-77, -12), (-81, -5),
     (-80, 1)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (3, 53), (8, 57),
     (10, 59), (5, 60), (12, 61), (18, 56), (21, 55), (24, 58), (28, 60),
     (30, 62), (32, 70), (40, 68), (44, 66), (40, 60), (35, 55), (30, 52),
     (28, 45), (30, 46), (28, 44), (23, 40), (26, 38), (22, 37), (19, 42),
     (12, 44), (8, 44), (3, 42), (0, 40), (-2, 37), (-6, 36)],
    # Africa
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (32, 31),
     (35, 28), (37, 22), (39, 18), (43, 12), (51, 11), (48, 3), (41, -2),
     (40, -10), (35, -18), (32, -26), (28, -33), (20, -35), (17, -32),
     (14, -22), (12, -12), (13, -5), (9, 4), (-8, 4), (-13, 8), (-17, 12)],
    # Asia
    [(32, 70), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75),
     (100, 77), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70),
     (158, 66), (162, 60), (158, 55), (150, 59), (142, 52), (140, 45),
     (135, 43), (130, 38), (127, 35), (122, 32), (120, 28), (115, 22),
     (109, 18), (105, 10), (103, 7), (100, 8), (98, 12), (94, 17), (91, 22),
     (88, 22), (85, 19), (80, 15), (77, 8), (75, 12), (72, 20), (68, 23),
     (62, 25), (57, 26), (52, 27), (50, 29), (48, 30), (44, 29), (40, 30),
     (38, 32), (36, 36), (33, 36), (30, 36), (27, 38), (26, 40), (30, 42),
     (35, 44), (38, 46), (40, 48), (42, 50), (45, 55), (48, 60), (50, 65),
     (45, 68), (40, 68)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -11), (140, -17),
     (136, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (141, 39),
     (141, 42), (143, 44), (145, 44), (142, 42), (140, 39), (139, 36),
     (137, 35), (135, 33), (133, 34), (131, 32)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    # New Zealand
    [(167, -45), (168, -44), (170, -43), (172, -41), (174, -41), (176, -38),
     (178, -37), (176, -40), (174, -42), (172, -43), (169, -46)],
    # Borneo / Sumatra / Java hints
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -4), (109, -2)],
    [(95, 5), (98, 3), (101, 0), (103, -3), (106, -6), (104, -6), (100, -1), (97, 2)],
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_map(draw, box):
    x0, y0, w, h = box
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA)
    # graticule
    for lon in range(-150, 181, 30):
        gx = x0 + (lon + 180) / 360 * w
        draw.line([(gx, y0), (gx, y0 + h)], fill=(255, 255, 255, 90), width=1)
    for lat in range(-30, 91, 30):
        gy = y0 + (85 - lat) / 140 * h
        draw.line([(x0, gy), (x0 + w, gy)], fill=(255, 255, 255, 90), width=1)

    def proj(lon, lat):
        return (x0 + (lon + 180) / 360 * w, y0 + (85 - lat) / 140 * h)

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # pins
    f_pin = font(SANS_B, 11)
    for num, lon, lat in PINS:
        px, py = proj(lon, lat)
        r = 11
        draw.ellipse([px - r, py - r, px + r, py + r], fill=PIN,
                     outline=(255, 255, 255, 255), width=2)
        tw = draw.textlength(str(num), font=f_pin)
        draw.text((px - tw / 2, py - 8), str(num), font=f_pin,
                  fill=(255, 255, 255, 255))
    return proj


def scene_turkey(d, x, y, s):
    # tail fan, kept inside the panel
    for i, ang in enumerate(range(-60, 61, 30)):
        rad = math.radians(ang - 90)
        ex, ey = x + 30 * math.cos(rad), y + 20 + 18 * math.sin(rad)
        d.ellipse([ex - 7, ey - 10, ex + 7, ey + 10],
                  fill=(150, 90, 40, 255), outline=(110, 60, 20, 255))
    d.ellipse([x - 22, y + 16, x + 22, y + 46], fill=(120, 70, 30, 255))
    d.ellipse([x - 8, y + 2, x + 8, y + 18], fill=(120, 70, 30, 255))
    d.polygon([(x + 7, y + 7), (x + 14, y + 10), (x + 7, y + 12)],
              fill=(230, 150, 40, 255))
    d.ellipse([x + 2, y + 5, x + 5, y + 8], fill=(20, 20, 20, 255))


def scene_flame(d, x, y, s):
    # refinery tower on the left, flame on the right
    d.rectangle([x + 8, y + 14, x + 32, y + 46], fill=(120, 120, 120, 255),
                outline=(70, 70, 70, 255))
    for yy in (20, 28, 36):
        d.line([(x + 8, y + yy), (x + 32, y + yy)], fill=(70, 70, 70, 255),
               width=1)
    d.rectangle([x + 16, y + 6, x + 24, y + 14], fill=(90, 90, 90, 255))
    d.polygon([(x + 56, y + 46), (x + 63, y + 22), (x + 70, y + 6),
               (x + 77, y + 22), (x + 84, y + 46)],
              fill=(230, 120, 30, 255))
    d.polygon([(x + 63, y + 46), (x + 68, y + 32), (x + 72, y + 22),
               (x + 76, y + 32), (x + 79, y + 46)],
              fill=(250, 200, 60, 255))


def scene_ballot(d, x, y, s):
    d.rectangle([x + 8, y + 16, x + 82, y + 48], fill=(31, 78, 121, 255))
    d.rectangle([x + 28, y + 48, x + 62, y + 52], fill=(31, 78, 121, 255))
    d.rectangle([x + 30, y + 0, x + 60, y + 20], fill=(255, 255, 255, 255),
                outline=(28, 28, 28, 255), width=2)
    d.line([(x + 36, y + 10), (x + 44, y + 17), (x + 56, y + 4)],
           fill=(39, 140, 60, 255), width=3)
    d.ellipse([x + 66, y + 2, x + 84, y + 20], fill=(201, 162, 39, 255))


def scene_football(d, x, y, s):
    d.ellipse([x + 4, y + 8, x + 52, y + 40], fill=(120, 70, 30, 255),
              outline=(255, 255, 255, 255), width=2)
    d.line([(x + 12, y + 24), (x + 44, y + 24)], fill=(255, 255, 255, 255),
           width=2)
    for lx in (18, 24, 30, 36, 42):
        d.line([(lx, y + 19), (lx, y + 29)], fill=(255, 255, 255, 255), width=2)
    d.ellipse([x + 58, y + 6, x + 86, y + 34], fill=(255, 255, 255, 255),
              outline=(28, 28, 28, 255), width=2)
    d.polygon([(x + 72, y + 12), (x + 78, y + 16), (x + 76, y + 23),
               (x + 69, y + 23), (x + 67, y + 16)], fill=(28, 28, 28, 255))


def scene_wave(d, x, y, s):
    for i, yy in enumerate((8, 18, 28)):
        col = (30, 110, 180, 255) if i % 2 == 0 else (80, 160, 210, 255)
        d.arc([x + 2, y + yy, x + 88, y + yy + 18], 180, 360, fill=col, width=4)
        d.arc([x + 2, y + yy + 6, x + 88, y + yy + 24], 180, 360,
              fill=col, width=3)
    d.polygon([(x + 40, y + 0), (x + 46, y + 10), (x + 34, y + 10)],
              fill=(192, 57, 43, 255))


SCENES = [
    (scene_turkey, "Thanksgiving"),
    (scene_flame, "Refinery hit"),
    (scene_ballot, "Taiwan votes"),
    (scene_football, "Football"),
    (scene_wave, "King tides"),
]


def main():
    img = Image.new("RGBA", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 68], fill=NAVY)
    f_title = font(SERIF_B, 34)
    f_date = font(SANS_B, 20)
    f_sub = font(SANS, 13)
    d.text((24, 14), "THE WORLD IN ONE DAY", font=f_title,
           fill=(255, 255, 255, 255))
    date_txt = "FRIDAY \u00b7 27 NOVEMBER 2026"
    dw = d.textlength(date_txt, font=f_date)
    d.text((W - 24 - dw, 20), date_txt, font=f_date, fill=GOLD)
    d.rectangle([0, 68, W, 72], fill=GOLD)

    # ---- map ----
    f_mapcap = font(SANS, 11)
    draw_map(d, (24, 80, 976, 208))
    d.text((24, 292), "Pinned: the day\u2019s flashpoints \u2014 numbers match the stories below.",
           font=f_mapcap, fill=GREY)

    # ---- scenes ----
    f_cap = font(SANS_B, 11)
    px, py, pw, ph = 24, 308, 188, 68
    for i, (fn, cap) in enumerate(SCENES):
        sx = px + i * (pw + 10)
        d.rectangle([sx, py, sx + pw, py + ph], fill=(255, 255, 255, 255),
                    outline=(200, 195, 185, 255), width=1)
        fn(d, sx + 48, py + 6, 1)
        cw = d.textlength(cap, font=f_cap)
        d.text((sx + (pw - cw) / 2, py + ph - 15), cap, font=f_cap, fill=INK)

    # ---- stories, three columns ----
    f_head = font(SANS_B, 13)
    f_hl = font(SANS_B, 12)
    f_sub2 = font(SANS, 10)
    f_num = font(SANS_B, 10)
    cols = [
        ["NORTH AMERICA", "MIDDLE EAST"],
        ["EUROPE", "EAST ASIA", "SOUTH ASIA"],
        ["SOUTH-EAST ASIA", "OCEANIA", "AFRICA", "LATIN AMERICA",
         "WORLD & SPORT"],
    ]
    col_x = [24, 352, 680]
    col_w = 320
    y_top, y_bottom = 390, 928
    for ci, groups in enumerate(cols):
        x = col_x[ci]
        y = y_top
        for g in groups:
            col = REGION_COLOURS[g]
            d.rectangle([x, y, x + 10, y + 16], fill=col + (255,))
            d.text((x + 15, y), g, font=f_head, fill=col + (255,))
            y += 20
            for num, region, hl, sub, src in STORIES:
                if region != g:
                    continue
                # number chip
                d.rectangle([x, y + 1, x + 16, y + 15], fill=col + (255,))
                nw = d.textlength(str(num), font=f_num)
                d.text((x + (16 - nw) / 2, y + 2), str(num), font=f_num,
                       fill=(255, 255, 255, 255))
                hl_lines = wrap(d, hl, f_hl, col_w - 22)
                sub_lines = wrap(d, sub + "  \u00b7 " + src, f_sub2,
                                 col_w - 22)
                ty = y
                for line in hl_lines[:2]:
                    d.text((x + 22, ty), line, font=f_hl, fill=INK)
                    ty += 15
                for line in sub_lines[:1]:
                    d.text((x + 22, ty), line, font=f_sub2, fill=GREY)
                    ty += 13
                y = ty + 4
            y += 4

    # ---- UTC timeline ----
    f_tl = font(SANS_B, 10)
    f_tll = font(SANS, 9)
    ty0 = 922
    d.text((24, ty0 - 4), "27 NOV \u00b7 UTC", font=f_tl, fill=NAVY)
    d.line([(120, ty0 + 8), (1000, ty0 + 8)], fill=NAVY, width=2)
    n = len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        cx = 140 + i * (840 / (n - 1))
        d.ellipse([cx - 5, ty0 + 3, cx + 5, ty0 + 13], fill=PIN,
                  outline=(255, 255, 255, 255), width=2)
        tw = d.textlength(t, font=f_tl)
        d.text((cx - tw / 2, ty0 - 16), t, font=f_tl, fill=PIN)
        lines = wrap(d, label, f_tll, 140)
        ly = ty0 + 18
        for line in lines[:2]:
            lw = d.textlength(line, font=f_tll)
            lx = min(max(cx - lw / 2, 24), 1000 - lw)
            d.text((lx, ly), line, font=f_tll, fill=GREY)
            ly += 11

    # ---- footer ----
    f_foot = font(SANS, 10)
    d.rectangle([0, 982, W, 984], fill=(200, 195, 185, 255))
    d.text((24, 990),
           "Date check: every story above was reported on 27 November 2026. "
           "Claims marked \u201cclaim\u201d are attributed, not confirmed.",
           font=f_foot, fill=GREY)
    d.text((24, 1004), "Sources: Reuters \u00b7 AP \u00b7 Al Jazeera \u00b7 Dawn \u00b7 "
           "Economic Times \u00b7 Deccan Chronicle \u00b7 Nikkei Asia \u00b7 The Guardian "
           "\u00b7 government.se \u00b7 OkayAfrica \u2014 full list in README.",
           font=f_foot, fill=GREY)

    img.convert("RGB").save(OUT, optimize=True)


if __name__ == "__main__":
    main()
    print("wrote", OUT)
