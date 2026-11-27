#!/usr/bin/env python3
"""Second edition of the 27 November 2026 world-news picture for make.fun.

A 1024x1024 newspaper front page, built on the shape of the 25 November
winner ("Grand Obelisk"): a masthead with a ticker strip, a stats strip,
twelve large illustrated feature stories (each with a hand-drawn scene, a
dateline, a verification tag, a headline and a two-line summary), a
story-locator map with numbered pins, a compact "Also on Friday" index of
the remaining stories, a UTC timeline, a DATE CHECK box and a verification
legend. Forty verified stories in eleven region groups.
Deterministic: `python3 draw_day.py` writes entry.png beside this file,
byte-identical every time.
"""

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
OUT_FILE = "entry.png"

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (248, 244, 235, 255)
INK = (30, 30, 30, 255)
MUTED = (96, 96, 94, 255)
NAVY = (18, 32, 60, 255)
GOLD = (206, 164, 42, 255)
SEA = (206, 225, 234, 255)
LAND = (136, 166, 116, 255)
LAND_LINE = (94, 124, 82, 255)
PIN_RED = (196, 58, 44, 255)
CARD = (255, 253, 247, 255)
CARD_LINE = (205, 198, 182, 255)
TAG_BG = (232, 226, 210, 255)

REGION_RGB = {
    "NORTH AMERICA": (31, 78, 121),
    "MIDDLE EAST": (146, 43, 33),
    "EUROPE": (39, 92, 68),
    "EAST ASIA": (122, 48, 108),
    "SOUTH ASIA": (176, 96, 16),
    "SOUTH-EAST ASIA": (14, 120, 110),
    "OCEANIA": (64, 110, 160),
    "AFRICA": (140, 110, 20),
    "LATIN AMERICA": (90, 60, 140),
    "SPORT": (120, 60, 40),
    "WORLD & TECH": (70, 70, 70),
}

# Each story: number, region, headline, subline, source label.
# All 40 were reported on 27 November 2026. Story 11 is an unverified
# claim, marked so. Stories first reported on 27 Nov but that happened
# earlier are noted in the README.
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
    (8, "NORTH AMERICA", "Black Friday: $12.9bn expected online",
     "Adobe forecasts a record day; 126m Americans to shop", "Adobe"),
    (9, "MIDDLE EAST", "Kuwait drone attack kills two Italians",
     "Iran calls it \u201csuspicious\u201d and denies any role", "Al Jazeera"),
    (10, "MIDDLE EAST", "Houthis hit Saudi Jazan refinery",
     "One worker killed; operations halted", "Al Jazeera"),
    (11, "MIDDLE EAST", "Tankers \u201chit mines\u201d near Khasab",
     "IRGC claim, unverified", "Times Now"),
    (12, "MIDDLE EAST", "Israeli strikes kill 10 in Gaza",
     "Hamas education deputy among the dead", "Deccan Chronicle"),
    (13, "MIDDLE EAST", "Brent crude near $96 a barrel",
     "First weekly gain in a month", "Reuters"),
    (14, "MIDDLE EAST", "Saudi jets strike Mocha, Yemen",
     "Nine civilians hurt in Taiz shelling", "Al Jazeera"),
    (15, "EUROPE", "UK net migration falls to 77,000",
     "Lowest since 1997, excluding Covid", "Reuters"),
    (16, "EUROPE", "EU picks Hernandez de Cos as ECB chief",
     "Succeeds Lagarde in February 2027", "Reuters"),
    (17, "EUROPE", "Depardieu to stand trial over rape claim",
     "Paris court orders trial; he denies wrongdoing", "Al Jazeera"),
    (18, "EUROPE", "Sweden summons Russian envoy",
     "Over Polish airspace breach and Denmark plot", "government.se"),
    (19, "EUROPE", "Russian drones kill 3 in Ukraine",
     "At least 10 injured overnight", "Kyiv Post"),
    (20, "EUROPE", "Besiktas\u2013Hapoel halted 30 minutes",
     "Palestine banner, pepper spray in Batumi", "Al Jazeera"),
    (21, "EUROPE", "Davis Cup: Britain beats Germany 2\u20131",
     "First semi-final in seven years", "Devdiscourse"),
    (22, "EAST ASIA", "Taiwan votes on Saturday",
     "Cyberattacks surge ahead of local polls", "Nikkei Asia"),
    (23, "EAST ASIA", "Kim vows more nuclear weapons",
     "After ignoring US talks", "Deccan Chronicle"),
    (24, "EAST ASIA", "China protests Japan over Diaoyu waters",
     "Vessels\u2019 \u201cillegal intrusion\u201d draws a protest", "Xinhua"),
    (25, "SOUTH ASIA", "Hasina aide arrested in Bangladesh",
     "Ex-deputy press secretary held", "Economic Times"),
    (26, "SOUTH ASIA", "Afghan women renamed \u201cBibi\u201d, \u201cgoat\u201d",
     "Taliban-ruled Balkh registers new names", "Moneycontrol"),
    (27, "SOUTH ASIA", "India, UAE fast-track defence tech",
     "Co-development of next-gen equipment", "Deccan Chronicle"),
    (28, "SOUTH ASIA", "Sri Lanka A reach Asia Cup final",
     "Beat India A by eight wickets", "Apex Sports News"),
    (29, "SOUTH-EAST ASIA", "Indonesia mine flood: 13 dead",
     "Thirteen more still missing", "Al Jazeera"),
    (30, "SOUTH-EAST ASIA", "Hong Kong warns over fire remembrance",
     "Memorial for 168 killed in blaze", "SCMP"),
    (31, "OCEANIA", "NZ coalition loses its majority",
     "Luxon now needs the Opportunity Party", "Economic Times"),
    (32, "OCEANIA", "Five women \u201cburied alive\u201d in PNG",
     "Sorcery claims spark outrage", "RNZ"),
    (33, "AFRICA", "Zambia: treason trial over \u201ccoup plot\u201d",
     "Prosecutors allege Russia training", "Reuters"),
    (34, "AFRICA", "Kenya court halts Ebola centre",
     "US-backed quarantine build stopped", "Reuters"),
    (35, "AFRICA", "DRC summons Uganda diplomat",
     "Over general\u2019s Walikale posts", "OkayAfrica"),
    (36, "LATIN AMERICA", "Argentina bans money printing",
     "Central bank barred from funding government", "Economic Times"),
    (37, "LATIN AMERICA", "Brazil snubs Milei from Lula inauguration",
     "Ambassador recalled as ties sour", "Firstpost"),
    (38, "SPORT", "NZ 131\u20134 at tea in Christchurch Test",
     "Latham 59 on day one v India", "Reuters"),
    (39, "SPORT", "Chess: rest day in Geneva",
     "Game 3 drawn; Gukesh\u2013Sindarov 1\u00bd\u20131\u00bd", "The Guardian"),
    (40, "WORLD & TECH", "FIFA confirms hackers got in",
     "Limited personal, business data accessed", "Reuters"),
]

# The twelve feature stories: (story number, dateline, tag, headline, summary, scene key).
# Tags: OFFICIAL = stated by an authority; CLAIM = attributed, unconfirmed;
# CLOSE = final reported price; REPORT = press report (see legend).
FEATURES = [
    (1, "WASHINGTON / USA", "REPORT", "Trump lashes out in Thanksgiving message",
     "Foes, immigrants and the federal government in the firing line on the holiday.", "turkey"),
    (5, "EASTERN USA", "REPORT", "Storm batters the US on Thanksgiving",
     "Holiday travel hit as a nor\u2019easter moves in across the east.", "storm"),
    (7, "PHILADELPHIA / USA", "REPORT", "Eagles\u2019 21-point Thanksgiving comeback",
     "A 59-yard field goal sinks the Cowboys in the holiday classic.", "football"),
    (8, "UNITED STATES", "REPORT", "Black Friday: $12.9bn expected online",
     "Adobe forecasts a record day as 126m Americans head out to shop.", "sale"),
    (9, "KUWAIT CITY", "REPORT", "Kuwait drone attack kills two Italians",
     "Iran calls the strike \u201csuspicious\u201d and denies any role in it.", "drone"),
    (10, "JAZAN, SAUDI ARABIA", "REPORT", "Houthis hit Saudi Jazan refinery",
     "One worker killed and operations halted at the Red Sea plant.", "flame"),
    (22, "TAIPEI / TAIWAN", "REPORT", "Taiwan votes on Saturday",
     "Cyberattacks surge ahead of local polls that China is watching.", "ballot"),
    (24, "EAST CHINA SEA", "OFFICIAL", "China protests Japan over Diaoyu waters",
     "Beijing lodges a solemn protest over vessels\u2019 \u201cillegal intrusion\u201d.", "boats"),
    (29, "BOGOR, INDONESIA", "REPORT", "Indonesia mine flood: 13 dead",
     "Thirteen more still missing at the illegal gold mine in Bogor.", "helmet"),
    (32, "SOUTHERN HIGHLANDS, PNG", "REPORT", "Five women \u201cburied alive\u201d in PNG",
     "Sorcery claims spark outrage; three men arrested in Kaa village.", "candle"),
    (37, "BRAS\u00cdLIA / BUENOS AIRES", "REPORT", "Brazil snubs Milei from Lula inauguration",
     "Ambassador recalled as the two neighbours\u2019 ties sour.", "flags"),
    (40, "ZURICH / FIFA", "OFFICIAL", "FIFA confirms hackers got in",
     "Limited personal and business data accessed in the breach.", "laptop"),
]

# Verification tags shown in the compact index (features carry their own).
INDEX_TAGS = {11: "CLAIM", 13: "CLOSE"}

# (big number, label) for the stats strip.
STATS = [
    ("4.3%", "US Q3 growth, revised up"),
    ("$96", "Brent crude, near a barrel"),
    ("77,000", "UK net migration, lowest since 1997"),
    ("126m", "Americans expected to shop Black Friday"),
]

TICKER = [
    "TRUMP LASHES OUT IN THANKSGIVING MESSAGE",
    "KUWAIT DRONE ATTACK KILLS TWO ITALIANS",
    "UK NET MIGRATION FALLS TO 77,000",
]

# (time, label) along the UTC timeline.
TIMELINE = [
    ("00:20", "NZ 77\u20131 at lunch, day 1 of 2nd Test"),
    ("01:07", "Storm batters US on Thanksgiving"),
    ("01:41", "Trump defends Huang\u2019s Nvidia return"),
    ("01:57", "Trump calls GDP figures \u201cfake\u201d"),
    ("02:29", "World League condemns refinery hit"),
    ("03:40", "Araghchi: Kuwait attack \u201csuspicious\u201d"),
]

# (story number, x, y) pins on the locator map, one per feature story,
# placed near each story's true location (US pins spread so the 18px
# circles do not touch). Numbers match the feature cards and the index.
MAP_PINS = [
    (1, 674, 614), (5, 706, 588), (7, 672, 634), (8, 631, 604),
    (9, 836, 630), (10, 828, 649), (22, 931, 638), (24, 950, 620),
    (29, 913, 686), (32, 965, 690), (37, 712, 702), (40, 784, 601),
]

DATE_CHECK_LINES = [
    "Reported 27 Nov, happened earlier (noted in place): UK migration figures (26 Nov) \u00b7 Sweden summons (26 Nov) \u00b7 "
    "Kenya court ruling (26 Nov) \u00b7 Besiktas\u2013Hapoel (26 Nov) \u00b7 Davis Cup (26 Nov) \u00b7 king-tide records (25 Nov).",
    "Left out \u2014 not 27 Nov news: FIFA\u2019s 2031 host announcement (23 Nov) \u00b7 England\u2019s heat-death toll \u00b7 "
    "Senegal\u2019s Afcon reinstatement \u00b7 the North Korea aircraft story (actually Russian aircraft).",
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def shrink_to_fit(d, text, fnt, max_w, max_lines):
    """Wrap text, shrinking the font until it fits in max_lines lines."""
    size = fnt.size
    while size > 8:
        f = font(fnt.path, size)
        lines = wrap(d, text, f, max_w)
        if len(lines) <= max_lines:
            return lines, f
        size -= 1
    return wrap(d, text, font(fnt.path, 8), max_w), font(fnt.path, 8)


# ---------------------------------------------------------------- scenes
# Each scene draws inside a box (x0, y0, x1, y1) with its own palette.
# All twelve are hand-drawn vector shapes, no images.

def scene_turkey(d, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for k, ang in enumerate((-50, -25, 0, 25, 50)):
        import math as _m
        ex = cx + int(20 * _m.sin(_m.radians(ang)))
        ey = cy - 6 + int(-12 * _m.cos(_m.radians(ang)))
        d.ellipse([ex - 6, ey - 7, ex + 6, ey + 7],
                  fill=(150, 84, 44, 255), outline=(110, 58, 28, 255))
    d.ellipse([cx - 22, cy - 6, cx + 22, cy + 16], fill=(122, 68, 34, 255))
    d.ellipse([cx + 8, cy - 18, cx + 28, cy - 2], fill=(122, 68, 34, 255))
    d.polygon([(cx + 26, cy - 10), (cx + 36, cy - 7), (cx + 26, cy - 4)],
              fill=(230, 150, 40, 255))
    d.ellipse([cx + 18, cy - 13, cx + 22, cy - 9], fill=(20, 20, 20, 255))
    d.line([(cx - 8, cy + 16), (cx - 8, cy + 23)], fill=(230, 150, 40, 255), width=2)
    d.line([(cx + 8, cy + 16), (cx + 8, cy + 23)], fill=(230, 150, 40, 255), width=2)


def scene_storm(d, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 6
    d.ellipse([cx - 34, cy - 12, cx - 6, cy + 10], fill=(88, 96, 110, 255))
    d.ellipse([cx - 16, cy - 20, cx + 16, cy + 10], fill=(70, 78, 92, 255))
    d.ellipse([cx + 6, cy - 12, cx + 34, cy + 10], fill=(88, 96, 110, 255))
    d.polygon([(cx - 2, cy + 8), (cx + 8, cy + 8), (cx - 2, cy + 20),
               (cx + 6, cy + 20), (cx - 8, cy + 32), (cx - 2, cy + 22),
               (cx - 10, cy + 22)], fill=(240, 200, 60, 255))
    for dx in (-28, -10, 8, 26):
        d.line([(cx + dx, cy + 22), (cx + dx - 3, cy + 30)],
               fill=(70, 120, 180, 255), width=3)


def scene_football(d, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([cx - 34, cy - 15, cx + 34, cy + 15], fill=(122, 68, 34, 255),
              outline=(90, 48, 22, 255))
    d.line([(cx - 16, cy), (cx + 16, cy)], fill=(255, 255, 255, 255), width=2)
    for dx in (-12, -6, 0, 6, 12):
        d.line([(cx + dx, cy - 5), (cx + dx, cy + 5)],
               fill=(255, 255, 255, 255), width=2)


def scene_sale(d, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.polygon([(cx - 26, cy - 6), (cx + 26, cy - 6), (cx + 20, cy + 24),
               (cx - 20, cy + 24)], fill=(196, 58, 44, 255))
    d.arc([cx - 14, cy - 22, cx + 14, cy + 2], 180, 360,
          fill=(90, 48, 22, 255), width=3)
    f = font(SANS_BOLD, 13)
    d.text((cx, cy + 3), "%", font=f, fill=(255, 255, 255, 255), anchor="mm")
    d.polygon([(cx + 26, cy - 2), (cx + 38, cy + 6), (cx + 26, cy + 12)],
              fill=(206, 164, 42, 255))


def scene_drone(d, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for dx, dy in ((-26, -14), (26, -14), (-26, 12), (26, 12)):
        d.ellipse([cx + dx - 10, cy + dy - 3, cx + dx + 10, cy + dy + 3],
                  outline=(70, 70, 70, 255), width=2)
        d.line([(cx + dx - 8, cy + dy), (cx + dx + 8, cy + dy)],
               fill=(70, 70, 70, 255), width=1)
    d.rounded_rectangle([cx - 16, cy - 10, cx + 16, cy + 10], radius=5,
                        fill=(60, 60, 66, 255))
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(196, 58, 44, 255))
    d.line([(cx - 26, cy - 14), (cx - 16, cy - 8)], fill=(70, 70, 70, 255), width=2)
    d.line([(cx + 26, cy - 14), (cx + 16, cy - 8)], fill=(70, 70, 70, 255), width=2)
    d.line([(cx - 26, cy + 12), (cx - 16, cy + 8)], fill=(70, 70, 70, 255), width=2)
    d.line([(cx + 26, cy + 12), (cx + 16, cy + 8)], fill=(70, 70, 70, 255), width=2)


def scene_flame(d, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 34, cy - 2, cx - 22, cy + 24], fill=(110, 110, 110, 255))
    d.rectangle([cx - 8, cy - 10, cx + 6, cy + 24], fill=(90, 90, 90, 255))
    d.rectangle([cx + 16, cy + 2, cx + 30, cy + 24], fill=(120, 120, 120, 255))
    d.polygon([(cx - 2, cy - 26), (cx + 12, cy - 4), (cx + 2, cy - 4),
               (cx + 8, cy + 8), (cx - 14, cy + 8), (cx - 6, cy - 4),
               (cx - 14, cy - 4)], fill=(240, 140, 30, 255))
    d.polygon([(cx - 2, cy - 12), (cx + 6, cy + 2), (cx - 8, cy + 2)],
              fill=(250, 210, 60, 255))


def scene_ballot(d, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 26, cy - 2, cx + 26, cy + 24], fill=(31, 78, 121, 255))
    d.rectangle([cx - 26, cy - 2, cx + 26, cy + 4], fill=(24, 60, 94, 255))
    d.polygon([(cx - 12, cy - 22), (cx + 2, cy - 22), (cx + 8, cy - 6),
               (cx - 6, cy - 6)], fill=(255, 255, 255, 255),
              outline=(120, 120, 120, 255))
    d.line([(cx - 9, cy - 14), (cx - 3, cy - 8), (cx + 5, cy - 20)],
           fill=(40, 140, 70, 255), width=3)
    d.ellipse([cx + 16, cy - 20, cx + 28, cy - 8], fill=(206, 164, 42, 255))


def scene_boats(d, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for dx, dy, col in ((-18, -6, (120, 120, 120, 255)),
                        (16, 6, (70, 90, 110, 255))):
        d.polygon([(cx + dx - 20, cy + dy), (cx + dx + 20, cy + dy),
                   (cx + dx + 14, cy + dy + 10), (cx + dx - 14, cy + dy + 10)],
                  fill=col)
        d.rectangle([cx + dx - 2, cy + dy - 16, cx + dx + 2, cy + dy],
                    fill=(60, 60, 60, 255))
    for wy in (cy + 14, cy + 20):
        for wx in range(x0 + 4, x1 - 4, 16):
            d.arc([wx, wy - 4, wx + 14, wy + 4], 0, 180,
                  fill=(70, 120, 180, 255), width=2)


def scene_helmet(d, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.pieslice([cx - 26, cy - 18, cx + 26, cy + 14], 180, 360,
               fill=(240, 200, 40, 255))
    d.rectangle([cx - 30, cy + 8, cx + 30, cy + 14], fill=(220, 175, 30, 255))
    d.rectangle([cx - 4, cy - 24, cx + 4, cy - 16], fill=(220, 175, 30, 255))
    d.ellipse([cx + 10, cy - 8, cx + 22, cy + 4], fill=(255, 250, 200, 255),
              outline=(200, 160, 40, 255))
    for dx in (-20, 0, 20):
        d.ellipse([cx + dx - 2, cy + 18, cx + dx + 2, cy + 24],
                  fill=(70, 120, 180, 255))


def scene_candle(d, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([cx - 6, cy - 26, cx + 6, cy - 12], fill=(250, 210, 60, 255))
    d.ellipse([cx - 3, cy - 20, cx + 3, cy - 12], fill=(255, 240, 160, 255))
    d.rectangle([cx - 8, cy - 8, cx + 8, cy + 20], fill=(245, 240, 225, 255),
                outline=(200, 190, 170, 255))
    d.rectangle([cx - 12, cy + 20, cx + 12, cy + 24], fill=(120, 110, 100, 255))
    d.ellipse([cx - 20, cy - 24, cx + 20, cy + 2],
              outline=(250, 210, 60, 255), width=1)


def scene_flags(d, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 34, cy - 14, cx - 4, cy + 14], fill=(0, 140, 70, 255))
    d.polygon([(cx - 19, cy - 10), (cx - 8, cy), (cx - 19, cy + 10),
               (cx - 30, cy)], fill=(250, 210, 40, 255))
    d.rectangle([cx + 4, cy - 14, cx + 34, cy + 14], fill=(180, 220, 240, 255))
    d.rectangle([cx + 4, cy - 5, cx + 34, cy + 5], fill=(255, 255, 255, 255))
    d.ellipse([cx + 14, cy - 4, cx + 24, cy + 4], fill=(240, 200, 60, 255))
    d.line([(cx - 2, cy - 16), (cx + 2, cy + 16)], fill=(150, 40, 40, 255), width=2)


def scene_laptop(d, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 28, cy - 16, cx + 28, cy + 12], fill=(50, 55, 65, 255))
    d.rectangle([cx - 24, cy - 12, cx + 24, cy + 8], fill=(180, 220, 240, 255))
    d.polygon([cx - 32, cy + 12, cx + 32, cy + 12, cx + 36, cy + 20,
               cx - 36, cy + 20], fill=(80, 85, 95, 255))
    d.rounded_rectangle([cx - 8, cy - 8, cx + 8, cy + 4], radius=3,
                        fill=(120, 120, 120, 255))
    d.arc([cx - 5, cy - 12, cx + 5, cy - 4], 180, 360,
          fill=(60, 60, 60, 255), width=2)
    d.line([(cx - 12, cy - 2), (cx + 12, cy - 2)], fill=(196, 58, 44, 255), width=2)
    d.line([(cx - 12, cy + 2), (cx + 4, cy + 2)], fill=(196, 58, 44, 255), width=2)


SCENE_DRAW = {
    "turkey": scene_turkey, "storm": scene_storm, "football": scene_football,
    "sale": scene_sale, "drone": scene_drone, "flame": scene_flame,
    "ballot": scene_ballot, "boats": scene_boats, "helmet": scene_helmet,
    "candle": scene_candle, "flags": scene_flags, "laptop": scene_laptop,
}

# Simplified continent outlines as (lon, lat) points, projected onto the
# locator map (x 540-1008, y 516-808). Stylised, not to scale.
def _px(lon):
    return int(540 + (lon + 180) / 360 * 468)


def _py(lat):
    return int(532 + (90 - lat) / 180 * 288)


CONTINENTS_LATLON = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-65, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 32), (-81, 25), (-90, 21),
     (-97, 26), (-105, 30), (-114, 32), (-125, 40), (-125, 49), (-130, 58),
     (-150, 60), (-165, 60)],
    [(-58, 64), (-45, 60), (-30, 68), (-20, 70), (-35, 76), (-55, 74)],
    [(-80, 10), (-75, 0), (-80, -5), (-81, -15), (-75, -25), (-70, -35),
     (-65, -45), (-70, -55), (-60, -50), (-55, -35), (-45, -25), (-35, -15),
     (-40, -5), (-50, 0), (-60, 5), (-70, 10)],
    [(-18, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 10), (48, 0), (40, -10), (35, -20), (30, -30), (20, -35),
     (15, -30), (12, -18), (8, -5), (9, 4), (-8, 5), (-15, 10)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 68),
     (15, 70), (5, 62), (0, 58), (-5, 50), (-10, 45)],
    [(30, 62), (40, 68), (60, 70), (80, 73), (100, 77), (120, 73), (140, 72),
     (160, 70), (178, 66), (170, 60), (160, 55), (155, 50), (140, 45),
     (130, 42), (127, 38), (120, 35), (110, 30), (105, 20), (100, 15),
     (95, 10), (90, 22), (85, 20), (80, 15), (75, 8), (70, 20), (60, 25),
     (55, 26), (50, 29), (45, 30), (40, 35), (35, 36), (30, 38)],
    [(95, 5), (100, 0), (105, -5), (110, -8), (115, -5), (120, 0), (125, 2),
     (130, -2), (135, -5), (140, -8), (135, -10), (125, -8), (115, -10),
     (105, -8), (100, -5), (95, 0)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (150, -25),
     (146, -20), (142, -15), (140, -12), (135, -12), (130, -13), (125, -15),
     (120, -20), (115, -20)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 52), (-2, 51)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39),
     (141, 41), (143, 43), (145, 44), (142, 42), (140, 39), (137, 36),
     (133, 34), (130, 32)],
    [(167, -45), (170, -42), (173, -40), (176, -38), (178, -37), (175, -40),
     (172, -43), (168, -46)],
]
CONTINENTS = [[(_px(lon), _py(lat)) for lon, lat in poly]
              for poly in CONTINENTS_LATLON]


# ---------------------------------------------------------------- layout

def draw_masthead(d):
    d.rectangle([0, 0, CANVAS_W, 54], fill=NAVY)
    d.rectangle([0, 54, CANVAS_W, 57], fill=GOLD)
    title_f = font(SERIF_BOLD, 34)
    d.text((16, 6), "THE WORLD IN ONE DAY", font=title_f, fill=(255, 255, 255, 255))
    date_f = font(SANS_BOLD, 15)
    d.text((CANVAS_W - 16, 12), "FRIDAY \u00b7 27 NOVEMBER 2026", font=date_f,
           fill=GOLD, anchor="ra")
    sub_f = font(SANS, 11)
    d.text((CANVAS_W - 16, 32), "SECOND EDITION  \u00b7  40 STORIES  \u00b7  11 REGIONS",
           font=sub_f, fill=(210, 215, 225, 255), anchor="ra")


def draw_ticker(d):
    d.rectangle([0, 57, CANVAS_W, 74], fill=(232, 226, 210, 255))
    f = font(SANS_BOLD, 11)
    text = "  \u25cf  ".join(TICKER)
    d.text((16, 60), text, font=f, fill=(120, 30, 30, 255))


def draw_stats(d):
    y0, y1 = 74, 116
    d.rectangle([0, y0, CANVAS_W, y1], fill=PAPER)
    col_w = CANVAS_W // len(STATS)
    big_f = font(SERIF_BOLD, 21)
    lab_f = font(SANS, 10)
    for i, (big, label) in enumerate(STATS):
        cx = col_w * i + col_w // 2
        if i:
            d.line([(col_w * i, y0 + 6), (col_w * i, y1 - 6)],
                   fill=CARD_LINE, width=1)
        d.text((cx, y0 + 2), big, font=big_f, fill=NAVY, anchor="ma")
        d.text((cx, y1 - 13), label, font=lab_f, fill=MUTED, anchor="ma")
    d.line([(0, y1), (CANVAS_W, y1)], fill=INK, width=1)


def draw_feature(img, x, y, w, h, feat):
    num, dateline, tag, headline, summary, scene_key = feat
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=CARD_LINE)
    # Numbered scene on top, drawn on its own layer so nothing can spill
    # out of the scene box into the strip above.
    scene_h = 50
    layer = Image.new("RGBA", (w - 2, scene_h), (238, 233, 220, 255))
    ld = ImageDraw.Draw(layer)
    SCENE_DRAW[scene_key](ld, 0, 0, w - 2, scene_h)
    img.paste(layer, (x + 1, y + 1))
    num_f = font(SANS_BOLD, 11)
    d.ellipse([x + 6, y + 6, x + 24, y + 24], fill=PIN_RED)
    d.text((x + 15, y + 15), "%02d" % num, font=num_f,
           fill=(255, 255, 255, 255), anchor="mm")
    # Dateline + tag.
    ty = y + scene_h + 4
    dl_f = font(SANS_BOLD, 9)
    d.text((x + 6, ty), dateline, font=dl_f, fill=NAVY)
    tag_f = font(SANS_BOLD, 9)
    tag_w = d.textlength(tag, font=tag_f) + 8
    d.rectangle([x + w - 6 - tag_w, ty - 1, x + w - 6, ty + 11], fill=TAG_BG,
                outline=(170, 160, 135, 255))
    d.text((x + w - 6 - tag_w / 2, ty + 5), tag, font=tag_f,
           fill=(120, 30, 30, 255), anchor="mm")
    # Headline, up to two lines.
    hy = ty + 14
    head_f = font(SANS_BOLD, 11)
    lines, head_f = shrink_to_fit(d, headline, head_f, w - 12, 2)
    for i, ln in enumerate(lines):
        d.text((x + 6, hy + i * 13), ln, font=head_f, fill=INK)
    # Summary, two lines.
    sy = hy + len(lines) * 13 + 1
    sum_f = font(SANS, 9)
    slines, sum_f = shrink_to_fit(d, summary, sum_f, w - 12, 2)
    for i, ln in enumerate(slines):
        d.text((x + 6, sy + i * 11), ln, font=sum_f, fill=MUTED)


def draw_features(img):
    x0, y0 = 16, 116
    cols, rows = 4, 3
    gap = 10
    cw = (CANVAS_W - 2 * x0 - (cols - 1) * gap) // cols
    ch = (524 - y0 - (rows - 1) * 8) // rows
    for i, feat in enumerate(FEATURES):
        cx = x0 + (i % cols) * (cw + gap)
        cy = y0 + (i // cols) * (ch + 8)
        draw_feature(img, cx, cy, cw, ch, feat)


def draw_map(d):
    x0, y0, x1, y1 = 540, 532, 1008, 820
    d.rectangle([x0, y0, x1, y1], fill=SEA, outline=CARD_LINE)
    for gx in range(x0 + 60, x1, 60):
        d.line([(gx, y0), (gx, y1)], fill=(255, 255, 255, 90), width=1)
    for gy in range(y0 + 60, y1, 60):
        d.line([(x0, gy), (x1, gy)], fill=(255, 255, 255, 90), width=1)
    for poly in CONTINENTS:
        d.polygon(poly, fill=LAND, outline=LAND_LINE)
    head_f = font(SANS_BOLD, 11)
    d.text((x0 + 8, y0 + 6), "STORY LOCATOR \u2014 WHERE THE DAY HAPPENED",
           font=head_f, fill=NAVY)
    pin_f = font(SANS_BOLD, 8)
    for num, px, py in MAP_PINS:
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=PIN_RED,
                  outline=(255, 255, 255, 255))
        d.text((px, py), "%02d" % num, font=pin_f,
               fill=(255, 255, 255, 255), anchor="mm")
    cap_f = font(SANS, 10)
    d.text((x0 + 8, y1 - 16), "Pins match the twelve features; the rest are in the index.",
           font=cap_f, fill=MUTED)


def one_line(d, text, fnt, max_w):
    """Fit text on one line: shrink the font, then truncate with ellipsis."""
    size = fnt.size
    while size > 8:
        f = font(fnt.path, size)
        if d.textlength(text, font=f) <= max_w:
            return text, f
        size -= 1
    f = font(fnt.path, 8)
    while text and d.textlength(text + "\u2026", font=f) > max_w:
        text = text[:-1].rstrip()
    return text + "\u2026", f


def draw_index(d):
    x0, y0 = 16, 524
    head_f = font(SANS_BOLD, 12)
    d.text((x0, y0), "ALSO ON FRIDAY", font=head_f, fill=NAVY)
    d.line([(x0, y0 + 17), (524, y0 + 17)], fill=INK, width=1)
    remaining = [s for s in STORIES if s[0] not in {f[0] for f in FEATURES}]
    col_a = remaining[:16]
    col_b = remaining[16:]
    body_f = font(SANS, 10)
    bold_f = font(SANS_BOLD, 10)
    tag_f = font(SANS_BOLD, 8)

    def draw_column(stories, cx, cy):
        y = cy
        cur_region = None
        for num, region, headline, _sub, source in stories:
            if region != cur_region:
                cur_region = region
                col = REGION_RGB[region]
                d.rectangle([cx, y, cx + 246, y + 13], fill=col)
                d.text((cx + 4, y + 6), "%s \u2014 %d" % (
                    region, sum(1 for s in STORIES if s[1] == region)),
                    font=font(SANS_BOLD, 9), fill=(255, 255, 255, 255),
                    anchor="lm")
                y += 17
            d.text((cx, y), "%d." % num, font=bold_f, fill=INK)
            shown, hf = one_line(d, headline, body_f, 218)
            d.text((cx + 24, y), shown, font=hf, fill=INK)
            tag = INDEX_TAGS.get(num)
            if tag:
                tw = d.textlength(tag, font=tag_f) + 6
                d.rectangle([cx + 246 - tw, y - 1, cx + 246, y + 11],
                            fill=TAG_BG, outline=(170, 160, 135, 255))
                d.text((cx + 246 - tw / 2, y + 5), tag, font=tag_f,
                       fill=(120, 30, 30, 255), anchor="mm")
            y += 13
        return y

    draw_column(col_a, x0, y0 + 24)
    draw_column(col_b, 270, y0 + 24)


def draw_timeline(d):
    y0 = 832
    d.text((16, y0), "27 NOV \u00b7 UTC", font=font(SANS_BOLD, 11), fill=NAVY)
    x0, x1 = 120, 1008
    d.line([(x0, y0 + 20), (x1, y0 + 20)], fill=INK, width=2)
    step = (x1 - x0) / (len(TIMELINE) - 1)
    tf = font(SANS_BOLD, 10)
    lf = font(SANS, 9)
    for i, (t, label) in enumerate(TIMELINE):
        cx = x0 + i * step
        last = i == len(TIMELINE) - 1
        if last:
            label = "Kuwait attack \u201csuspicious\u201d"
        d.ellipse([cx - 4, y0 + 16, cx + 4, y0 + 24], fill=PIN_RED)
        d.text((cx if not last else x1 - 2, y0 + 2), t, font=tf, fill=PIN_RED,
               anchor="ra" if last else "ma")
        shown, _f = one_line(d, label, lf, 170)
        ly = y0 + 41 if last else y0 + 28
        d.text((cx if not last else x1 - 2, ly), shown, font=_f,
               fill=MUTED, anchor="ra" if last else "ma")


def draw_datecheck(d):
    y0 = 884
    d.rectangle([16, y0, 1008, y0 + 72], fill=(232, 226, 210, 255),
                outline=CARD_LINE)
    d.text((26, y0 + 6), "DATE CHECK \u2014 WHY THESE ARE 27 NOVEMBER STORIES",
           font=font(SANS_BOLD, 11), fill=NAVY)
    f = font(SANS, 10)
    y = y0 + 22
    for line in DATE_CHECK_LINES:
        for ln in wrap(d, line, f, 960):
            d.text((26, y), ln, font=f, fill=INK)
            y += 13


def draw_legend_footer(d):
    y0 = 964
    f = font(SANS_BOLD, 10)
    d.text((16, y0), "VERIFICATION \u2014 OFFICIAL = stated by an authority  \u00b7  "
           "CLAIM = attributed, unconfirmed  \u00b7  CLOSE = final reported price  "
           "\u00b7  REPORT = press report", font=f, fill=INK)
    d.line([(16, y0 + 20), (1008, y0 + 20)], fill=CARD_LINE, width=1)
    sf = font(SANS, 9)
    d.text((16, y0 + 26),
           "Sources: Reuters \u00b7 AP \u00b7 Al Jazeera \u00b7 Dawn \u00b7 Economic Times \u00b7 "
           "Deccan Chronicle \u00b7 Nikkei Asia \u00b7 The Guardian \u00b7 government.se \u00b7 "
           "OkayAfrica \u00b7 Xinhua \u00b7 Firstpost \u00b7 RNZ \u00b7 Moneycontrol \u00b7 Adobe "
           "\u2014 full story list with URLs in README.",
           font=sf, fill=MUTED)
    d.text((16, y0 + 40),
           "THE WORLD IN ONE DAY \u00b7 SECOND EDITION \u00b7 DRAWN 27 NOVEMBER 2026 \u00b7 "
           "ALL STORIES VERIFIED AGAINST REPORTS OF 27 NOVEMBER 2026.",
           font=sf, fill=MUTED)


def main():
    img = Image.new("RGBA", (CANVAS_W, CANVAS_H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_ticker(d)
    draw_stats(d)
    draw_features(img)
    draw_map(d)
    draw_index(d)
    draw_timeline(d)
    draw_datecheck(d)
    draw_legend_footer(d)
    img.convert("RGB").save(OUT_FILE, optimize=True)
    print("wrote", OUT_FILE)


if __name__ == "__main__":
    main()
