#!/usr/bin/env python3
"""The World in One Day - Friday 27 November 2026. Third edition.

Draws entry.png (1024x1024) with Pillow: a four-column newspaper
broadsheet. Twelve large illustrated headlines, each with a dateline, a
verification tag, a headline, a two-line summary and a WHY IT MATTERS
line; a story-locator map; a around-the-world strip; a DATE CHECK box; a
HOW SURE source column; a stats strip; and an "Also on Friday" index of
the remaining stories. 40 verified stories, 11 regions, fields counted
from the data.

Every story below was reported on 27 November 2026. Events that happened
late on 26 November but were first reported on 27 November are noted in
place. Unconfirmed claims are tagged CLAIM, never stated as fact.
Tags: OFFICIAL = stated by an authority; CLAIM = attributed, unconfirmed;
CLOSE = final reported price; REPORT = press report.

Run:  python3 draw_v3.py
Then:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
"""

import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

# ---------------------------------------------------------------- data
# field = the beat / domain of the story; the stats strip counts distinct
# fields from this list, so the number on the page is never invented.
STORIES = [
    dict(n=1, region="North America", field="Politics",
         place="WASHINGTON", tag="OFFICIAL",
         headline="Trump lashes out in Thanksgiving message",
         summary="President attacks foes, immigrants and the federal "
                 "government in his holiday message.",
         why="The administration's targets for the weeks ahead.",
         scene="turkey"),
    dict(n=2, region="North America", field="Economy",
         place="WASHINGTON", tag="REPORT",
         headline="Trump calls GDP figures \u201cfake\u201d, demands probe",
         summary="Q3 growth is revised up to 4.3% after the midterms; the "
                 "president calls the figures a \u201cmassive error\u201d.",
         why=None, scene=None),
    dict(n=3, region="North America", field="Technology",
         place="NEW YORK", tag="REPORT",
         headline="Trump defends Huang's return as Nvidia chief",
         summary="\u201cEverybody's replaceable,\u201d the president says of "
                 "the chipmaker's leadership.",
         why=None, scene=None),
    dict(n=4, region="North America", field="Diplomacy",
         place="WASHINGTON", tag="REPORT",
         headline="Trump: Putin \u201cwould like a deal\u201d",
         summary="The president says Putin can attend the G20 summit in "
                 "Miami.",
         why=None, scene=None),
    dict(n=5, region="North America", field="Weather",
         place="US EAST COAST", tag="REPORT",
         headline="Storm batters the US on Thanksgiving",
         summary="A nor'easter moves in as millions travel for the "
                 "holiday; flights and roads are hit.",
         why="Thanksgiving is the year's busiest US travel day.",
         scene="storm"),
    dict(n=6, region="North America", field="Climate",
         place="CALIFORNIA", tag="REPORT",
         headline="King tides flood the California coast",
         summary="Pacifica Pier collapses as record water levels, set on "
                 "25 November, keep flooding the coast.",
         why=None, scene=None),
    dict(n=7, region="North America", field="American Football",
         place="DALLAS", tag="REPORT",
         headline="Eagles' 21-point Thanksgiving comeback",
         summary="A 59-yard field goal sinks the Cowboys after Dallas led "
                 "by 21.",
         why=None, scene=None),
    dict(n=8, region="North America", field="Retail",
         place="NEW YORK", tag="REPORT",
         headline="Black Friday: $12.9bn expected online",
         summary="Adobe forecasts a record online day, with 126 million "
                 "Americans set to shop.",
         why="A read on how US consumers feel.",
         scene="shopping"),
    dict(n=9, region="Middle East", field="War & Conflict",
         place="KUWAIT CITY", tag="REPORT",
         headline="Kuwait drone attack kills two Italians",
         summary="A drone strike kills two Italians in Kuwait; Iran calls "
                 "the attack \u201csuspicious\u201d and denies any role.",
         why="The attack widens a Gulf crisis; oil is near $96.",
         scene="drone"),
    dict(n=10, region="Middle East", field="Energy",
         place="JAZAN, SAUDI ARABIA", tag="REPORT",
         headline="Houthis hit Saudi refinery; one worker killed",
         summary="A strike on the Jazan refinery kills one worker and "
                 "halts operations.",
         why="Gulf oil infrastructure is now in the firing line.",
         scene="refinery"),
    dict(n=11, region="Middle East", field="Maritime",
         place="STRAIT OF HORMUZ", tag="CLAIM",
         headline="Tankers \u201chit mines\u201d near Khasab, IRGC claims",
         summary="Iran's Revolutionary Guard claims tankers struck mines; "
                 "the claim is unverified.",
         why=None, scene=None),
    dict(n=12, region="Middle East", field="War & Conflict",
         place="GAZA", tag="REPORT",
         headline="Israeli strikes kill 10 in Gaza",
         summary="Hamas's education deputy is among the dead, reports say.",
         why=None, scene=None),
    dict(n=13, region="Middle East", field="Oil Markets",
         place="LONDON", tag="CLOSE",
         headline="Brent crude near $96 a barrel",
         summary="Oil heads for its first weekly gain in a month.",
         why=None, scene=None),
    dict(n=14, region="Middle East", field="War & Conflict",
         place="MOCHA, YEMEN", tag="REPORT",
         headline="Saudi jets strike Mocha; nine hurt in Taiz",
         summary="Nine civilians are hurt in shelling in Taiz, reports say.",
         why=None, scene=None),
    dict(n=15, region="Europe", field="Migration",
         place="LONDON", tag="OFFICIAL",
         headline="UK net migration falls to 77,000",
         summary="Annual net migration drops to its lowest since 1997, "
                 "excluding the Covid years. Figures released 26 November.",
         why="The lowest since 1997 \u2014 Britain will argue over it.",
         scene="migration"),
    dict(n=16, region="Europe", field="Finance",
         place="FRANKFURT", tag="OFFICIAL",
         headline="EU picks de Cos as next ECB chief",
         summary="Spain's Pablo Hern\u00e1ndez de Cos will succeed "
                 "Christine Lagarde in February 2027.",
         why="He takes the ECB job amid war, tariffs, slow growth.",
         scene="ecb"),
    dict(n=17, region="Europe", field="Justice",
         place="PARIS", tag="REPORT",
         headline="Depardieu to stand trial over rape claim",
         summary="A Paris court orders a trial; the actor denies "
                 "wrongdoing.",
         why=None, scene=None),
    dict(n=18, region="Europe", field="Diplomacy",
         place="STOCKHOLM", tag="OFFICIAL",
         headline="Sweden summons Russian envoy",
         summary="The summons, issued 26 November, follows a Polish "
                 "airspace breach and a Denmark plot.",
         why=None, scene=None),
    dict(n=19, region="Europe", field="War & Conflict",
         place="KYIV", tag="REPORT",
         headline="Russian drones kill 3 in Ukraine",
         summary="At least 10 are injured in overnight drone attacks.",
         why=None, scene=None),
    dict(n=20, region="Europe", field="Football",
         place="BATUMI", tag="REPORT",
         headline="Besiktas\u2013Hapoel halted 30 minutes",
         summary="A Palestine banner and pepper spray stop play; Besiktas "
                 "won 2\u20131. Match played 26 November.",
         why=None, scene=None),
    dict(n=21, region="Europe", field="Tennis",
         place="BOLOGNA", tag="REPORT",
         headline="Davis Cup: Britain beats Germany 2\u20131",
         summary="Britain reach their first semi-final in seven years. Tie "
                 "played 26 November.",
         why=None, scene=None),
    dict(n=22, region="East Asia", field="Cybersecurity",
         place="TAIPEI", tag="REPORT",
         headline="Taiwan votes Saturday as cyberattacks surge",
         summary="A wave of cyberattacks hits ahead of local elections "
                 "that China is watching closely.",
         why="The vote is a bellwether for cross-strait politics.",
         scene="cyber"),
    dict(n=23, region="East Asia", field="Nuclear",
         place="PYONGYANG", tag="REPORT",
         headline="Kim vows more nuclear weapons",
         summary="North Korea's leader pledges a bigger arsenal after "
                 "ignoring US offers of talks.",
         why="Pyongyang chooses weapons over negotiation.",
         scene="missile"),
    dict(n=24, region="East Asia", field="Diplomacy",
         place="BEIJING", tag="OFFICIAL",
         headline="China protests Japan over Diaoyu waters",
         summary="Beijing lodges a solemn protest over vessels' \u201cillegal "
                 "intrusion\u201d.",
         why=None, scene=None),
    dict(n=25, region="South Asia", field="Politics",
         place="DHAKA", tag="REPORT",
         headline="Hasina aide arrested in Bangladesh",
         summary="The former prime minister's ex-deputy press secretary is "
                 "held.",
         why=None, scene=None),
    dict(n=26, region="South Asia", field="Human Rights",
         place="BALKH, AFGHANISTAN", tag="REPORT",
         headline="Afghan women renamed \u201cBibi\u201d, \u201cgoat\u201d",
         summary="Taliban-ruled Balkh registers women under new names, an "
                 "investigation finds.",
         why=None, scene=None),
    dict(n=27, region="South Asia", field="Defence",
         place="NEW DELHI", tag="REPORT",
         headline="India, UAE fast-track defence tech",
         summary="The two countries will co-develop next-generation "
                 "equipment.",
         why=None, scene=None),
    dict(n=28, region="South Asia", field="Cricket",
         place="COLOMBO", tag="REPORT",
         headline="Sri Lanka A reach Asia Cup final",
         summary="Sri Lanka A beat India A by eight wickets.",
         why=None, scene=None),
    dict(n=29, region="South-East Asia", field="Mining",
         place="INDONESIA", tag="REPORT",
         headline="Indonesia mine flood: 13 dead, 13 missing",
         summary="A gold-mine flood kills thirteen; rescuers search for "
                 "thirteen more.",
         why="The toll may still rise as rescuers fight floodwater.",
         scene="mine"),
    dict(n=30, region="South-East Asia", field="Society",
         place="HONG KONG", tag="REPORT",
         headline="Hong Kong mourns 168 fire victims",
         summary="Residents return to mourn the 168 killed in the Tai Po "
                 "blaze.",
         why="168 lives in one fire \u2014 why the city still gathers.",
         scene="candles"),
    dict(n=31, region="Oceania", field="Politics",
         place="WELLINGTON", tag="REPORT",
         headline="NZ coalition loses its majority",
         summary="Prime Minister Luxon now needs the Opportunity Party to "
                 "govern.",
         why=None, scene=None),
    dict(n=32, region="Oceania", field="Human Rights",
         place="PORT MORESBY", tag="REPORT",
         headline="Five women \u201cburied alive\u201d in PNG",
         summary="Sorcery claims spark outrage after five women were "
                 "allegedly buried alive.",
         why=None, scene=None),
    dict(n=33, region="Africa", field="Justice",
         place="LUSAKA", tag="CLAIM",
         headline="Zambia treason trial over \u201ccoup plot\u201d",
         summary="Prosecutors allege a Russia-trained plot to overthrow "
                 "the government; the accused deny it.",
         why="Alleged, not proven \u2014 the trial will test the claim.",
         scene="court"),
    dict(n=34, region="Africa", field="Health",
         place="NAIROBI", tag="OFFICIAL",
         headline="Kenya court halts Ebola centre",
         summary="A court stops a US-backed quarantine build. The ruling "
                 "came on 26 November.",
         why=None, scene=None),
    dict(n=35, region="Africa", field="Diplomacy",
         place="KINSHASA", tag="REPORT",
         headline="DRC summons Uganda diplomat",
         summary="Kinshasa protests a Ugandan general's posts on Walikale.",
         why=None, scene=None),
    dict(n=36, region="Latin America", field="Monetary Policy",
         place="BUENOS AIRES", tag="OFFICIAL",
         headline="Argentina bans money printing",
         summary="The central bank is barred from funding the government.",
         why=None, scene=None),
    dict(n=37, region="Latin America", field="Diplomacy",
         place="BRASILIA", tag="REPORT",
         headline="Brazil snubs Milei from Lula inauguration",
         summary="Argentina's president gets no invite as ties sour; the "
                 "ambassador is recalled.",
         why=None, scene=None),
    dict(n=38, region="Sport", field="Cricket",
         place="CHRISTCHURCH", tag="REPORT",
         headline="NZ 131\u20134 at tea in Christchurch Test",
         summary="Latham makes 59 on day one against India.",
         why=None, scene=None),
    dict(n=39, region="Sport", field="Chess",
         place="GENEVA", tag="REPORT",
         headline="Chess: rest day in Geneva, Game 3 drawn",
         summary="Gukesh and Sindarov stand at 1\u00bd\u20131\u00bd. Game 3 "
                 "was played 26 November.",
         why=None, scene=None),
    dict(n=40, region="World & Tech", field="Cybersecurity",
         place="ZURICH", tag="OFFICIAL",
         headline="FIFA confirms hackers got in",
         summary="Limited personal and business data was accessed, FIFA "
                 "says.",
         why=None, scene=None),
]

# The twelve illustrated headlines, three per column, in column order.
FEATURES = [1, 5, 9, 10, 15, 16, 22, 23, 29, 30, 33, 8]

# Stories deliberately left out because they are NOT 27 November news.
DATE_CHECK = [
    ("FIFA names 2031 World Cup hosts", "announced 23 November"),
    ("England's heat-death toll", "reported earlier in the week"),
    ("Senegal's Afcon reinstatement", "reported earlier in the week"),
    ("\u201cNorth Korean aircraft\u201d", "the aircraft was Russian"),
]

# Events released 26 November, first reported 27 November: counted here.
REPORTED_NOTE = ("UK migration figures, the Sweden summons, the Kenya court "
                 "ruling, the Besiktas\u2013Hapoel halt and the Davis Cup tie "
                 "were released or played 26 Nov and first reported 27 Nov.")

# ---------------------------------------------------------------- style
PAPER = (247, 243, 232)
INK = (20, 20, 20)
MUTED = (90, 86, 76)
RULE = (60, 58, 52)
RED = (163, 22, 33)
BLUE = (31, 78, 121)
GOLD = (176, 141, 44)
GREEN = (46, 110, 72)
TEAL = (18, 110, 110)
TAG_FILL = {
    "OFFICIAL": (31, 78, 121),
    "CLAIM": (163, 22, 33),
    "CLOSE": (46, 110, 72),
    "REPORT": (90, 86, 76),
}


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
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


def draw_tag(d, x, y, tag):
    """Small filled chip with the verification tag, returns its width."""
    fnt = F_SANS_B(10)
    w = int(d.textlength(tag, font=fnt)) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3,
                        fill=TAG_FILL[tag])
    d.text((x + 5, y + 2), tag, font=fnt, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- scenes
# Each scene is a small hand-drawn picture on a 243x92 box. Simple flat
# shapes, one motif per story, distinct sky and ground colours.

def scene_base(d, x, y, w, h, sky, ground):
    d.rectangle([x, y, x + w, y + h], fill=sky)
    d.rectangle([x, y + h - 22, x + w, y + h], fill=ground)


def scene_turkey(d, x, y, w, h):
    scene_base(d, x, y, w, h, (246, 214, 170), (122, 74, 40))
    cx, cy = x + w // 2, y + 52
    for i, a in enumerate(range(-60, 61, 30)):
        import math
        r = math.radians(a - 90)
        ex, ey = cx + int(34 * math.cos(r)), cy + int(30 * math.sin(r))
        d.line([cx, cy, ex, ey], fill=(163, 22, 33), width=5)
        d.ellipse([ex - 6, ey - 8, ex + 6, ey + 8], fill=(176, 141, 44))
    d.ellipse([cx - 20, cy - 8, cx + 20, cy + 20], fill=(94, 58, 28))
    d.ellipse([cx - 8, cy - 22, cx + 8, cy - 6], fill=(94, 58, 28))
    d.polygon([(cx + 8, cy - 18), (cx + 18, cy - 14), (cx + 8, cy - 10)],
              fill=(214, 148, 40))
    d.rectangle([x + 8, y + 8, x + 64, y + 20], fill=(255, 255, 255))
    d.text((x + 12, y + 9), "THANKSGIVING", font=F_SANS_B(9), fill=RED)


def scene_storm(d, x, y, w, h):
    scene_base(d, x, y, w, h, (58, 72, 96), (38, 44, 58))
    d.ellipse([x + 30, y + 6, x + 110, y + 34], fill=(30, 36, 52))
    d.ellipse([x + 90, y + 2, x + 180, y + 32], fill=(44, 52, 72))
    d.ellipse([x + 150, y + 10, x + 220, y + 36], fill=(30, 36, 52))
    d.polygon([(x + 120, y + 36), (x + 104, y + 62), (x + 118, y + 62),
               (x + 100, y + 86), (x + 132, y + 52), (x + 118, y + 52),
               (x + 134, y + 36)], fill=(255, 214, 64))
    for rx in (x + 40, x + 70, x + 170, x + 200):
        d.line([rx, y + 44, rx - 6, y + 78], fill=(150, 180, 220), width=3)
    d.rectangle([x + 18, y + 66, x + 62, y + 78], fill=(163, 22, 33))
    d.ellipse([x + 24, y + 60, x + 34, y + 70], fill=(20, 20, 20))
    d.ellipse([x + 46, y + 60, x + 56, y + 70], fill=(20, 20, 20))


def scene_drone(d, x, y, w, h):
    scene_base(d, x, y, w, h, (232, 196, 140), (150, 110, 62))
    for bx in (x + 14, x + 96, x + 178):
        d.rectangle([bx, y + 52, bx + 34, y + 70], fill=(120, 92, 60))
        d.polygon([(bx + 6, y + 52), (bx + 17, y + 36), (bx + 28, y + 52)],
                  fill=(96, 74, 48))
    cx, cy = x + w // 2, y + 26
    d.line([cx - 26, cy - 12, cx + 26, cy + 12], fill=(40, 40, 40), width=4)
    d.line([cx - 26, cy + 12, cx + 26, cy - 12], fill=(40, 40, 40), width=4)
    for px, py in ((cx - 26, cy - 12), (cx + 26, cy + 12),
                   (cx - 26, cy + 12), (cx + 26, cy - 12)):
        d.ellipse([px - 8, py - 3, px + 8, py + 3], fill=(90, 90, 90))
    d.rectangle([cx - 10, cy - 6, cx + 10, cy + 6], fill=(20, 20, 20))
    for sx, sy, r in ((x + 190, y + 14, 5), (x + 200, y + 26, 3),
                      (x + 182, y + 30, 4)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(163, 22, 33))


def scene_refinery(d, x, y, w, h):
    scene_base(d, x, y, w, h, (250, 196, 120), (70, 60, 52))
    for tx in (x + 30, x + 80, x + 130):
        d.rectangle([tx, y + 26, tx + 22, y + 70], fill=(120, 118, 110))
        d.rectangle([tx + 6, y + 14, tx + 16, y + 26], fill=(90, 88, 82))
    d.polygon([(x + 178, y + 70), (x + 190, y + 18), (x + 202, y + 70)],
              fill=(150, 148, 140))
    d.polygon([(x + 190, y + 18), (x + 184, y + 34), (x + 196, y + 34)],
              fill=(255, 140, 40))
    d.polygon([(x + 190, y + 30), (x + 186, y + 44), (x + 194, y + 44)],
              fill=(255, 200, 60))
    d.ellipse([x + 60, y + 8, x + 92, y + 24], fill=(255, 255, 255))
    d.ellipse([x + 100, y + 14, x + 150, y + 26], fill=(240, 240, 240))


def scene_migration(d, x, y, w, h):
    scene_base(d, x, y, w, h, (214, 228, 240), (31, 78, 121))
    pts = [(x + 20, y + 66), (x + 70, y + 66), (x + 70, y + 52),
           (x + 120, y + 52), (x + 120, y + 38), (x + 170, y + 38),
           (x + 170, y + 22), (x + 220, y + 22)]
    d.line(pts, fill=RED, width=4, joint="curve")
    d.polygon([(x + 220, y + 22), (x + 204, y + 16), (x + 204, y + 28)],
              fill=RED)
    for bx in (x + 40, x + 90, x + 140, x + 190):
        d.rectangle([bx, y + 66, bx + 10, y + 70], fill=(255, 255, 255))
    d.rectangle([x + 8, y + 8, x + 96, y + 22], fill=(255, 255, 255))
    d.text((x + 12, y + 9), "77,000 \u2193 LOWEST SINCE 1997",
           font=F_SANS_B(9), fill=BLUE)


def scene_ecb(d, x, y, w, h):
    scene_base(d, x, y, w, h, (226, 232, 240), (96, 104, 116))
    for cx in (x + 40, x + 80, x + 120, x + 160, x + 200):
        d.rectangle([cx - 6, y + 30, cx + 6, y + 66], fill=(240, 240, 235))
        d.rectangle([cx - 10, y + 26, cx + 10, y + 30], fill=(240, 240, 235))
    d.rectangle([x + 24, y + 18, x + 216, y + 26], fill=(240, 240, 235))
    d.rectangle([x + 24, y + 66, x + 216, y + 72], fill=(240, 240, 235))
    d.ellipse([x + 96, y + 70, x + 146, y + 86], fill=(255, 214, 64),
              outline=(176, 141, 44), width=2)
    d.text((x + 114, y + 71), "\u20ac", font=F_SERIF_B(12), fill=(120, 90, 20))


def scene_cyber(d, x, y, w, h):
    scene_base(d, x, y, w, h, (24, 32, 54), (52, 120, 90))
    for i in range(5):
        d.arc([x + 70 + i * 8, y + 14 + i * 8, x + 170 - i * 8, y + 78 - i * 4],
              start=200, end=340, fill=(80, 200, 160), width=3)
    d.rectangle([x + 96, y + 30, x + 146, y + 56], fill=(255, 255, 255),
                outline=(31, 78, 121), width=2)
    d.line([x + 104, y + 48, x + 114, y + 38, x + 124, y + 50, x + 138, y + 34],
           fill=(46, 110, 72), width=3)
    d.text((x + 160, y + 12), "01 10 11", font=F_SANS_B(9),
           fill=(80, 200, 160))
    d.text((x + 160, y + 60), "VOTE SAT", font=F_SANS_B(9),
           fill=(255, 255, 255))


def scene_missile(d, x, y, w, h):
    scene_base(d, x, y, w, h, (30, 34, 48), (70, 74, 82))
    d.ellipse([x + 150, y + 10, x + 210, y + 40], fill=(250, 220, 140))
    d.ellipse([x + 160, y + 18, x + 200, y + 36], fill=(255, 240, 180))
    d.polygon([(x + 30, y + 62), (x + 96, y + 58), (x + 116, y + 48),
               (x + 130, y + 54), (x + 116, y + 62), (x + 96, y + 66)],
              fill=(180, 180, 180))
    d.polygon([(x + 30, y + 62), (x + 44, y + 52), (x + 44, y + 72)],
              fill=(163, 22, 33))
    for fx, fy in ((x + 20, y + 56), (x + 12, y + 64), (x + 20, y + 70)):
        d.polygon([(fx, fy - 5), (fx - 12, fy), (fx, fy + 5)],
                  fill=(255, 140, 40))
    d.text((x + 150, y + 62), "MORE WEAPONS", font=F_SANS_B(9),
           fill=(255, 255, 255))


def scene_mine(d, x, y, w, h):
    scene_base(d, x, y, w, h, (210, 226, 235), (96, 84, 66))
    d.polygon([(x + 10, y + 70), (x + 90, y + 10), (x + 170, y + 70)],
              fill=(120, 108, 88))
    d.polygon([(x + 90, y + 10), (x + 120, y + 34), (x + 70, y + 34)],
              fill=(240, 240, 240))
    d.pieslice([x + 100, y + 40, x + 150, y + 78], start=180, end=360,
               fill=(30, 26, 22))
    d.rectangle([x + 100, y + 58, x + 150, y + 70], fill=(40, 90, 160))
    for wy in (y + 62, y + 67):
        d.line([x + 104, wy, x + 146, wy], fill=(140, 190, 240), width=2)
    d.rectangle([x + 146, y + 30, x + 238, y + 44], fill=(255, 255, 255))
    d.text((x + 150, y + 32), "13 DEAD \u00b7 13 MISSING",
           font=F_SANS_B(8), fill=RED)


def scene_candles(d, x, y, w, h):
    scene_base(d, x, y, w, h, (40, 40, 62), (24, 24, 34))
    for bx in (x + 20, x + 40, x + 60, x + 80, x + 100):
        d.rectangle([bx, y + 18, bx + 46, y + 34], fill=(70, 70, 96))
        d.rectangle([bx + 4, y + 22, bx + 10, y + 30], fill=(180, 190, 220))
    for cx in (x + 40, x + 80, x + 120, x + 160, x + 200):
        d.rectangle([cx - 3, y + 48, cx + 3, y + 72], fill=(240, 230, 210))
        d.ellipse([cx - 4, y + 38, cx + 4, y + 48], fill=(255, 200, 60))
        d.ellipse([cx - 2, y + 41, cx + 2, y + 46], fill=(255, 240, 180))
    d.text((x + 8, y + 6), "168 LIVES", font=F_SANS_B(9),
           fill=(255, 255, 255))


def scene_court(d, x, y, w, h):
    scene_base(d, x, y, w, h, (232, 226, 210), (140, 124, 96))
    d.polygon([(x + 30, y + 26), (x + 121, y + 8), (x + 212, y + 26)],
              fill=(176, 141, 44))
    for cx in (x + 52, x + 92, x + 132, x + 172):
        d.rectangle([cx - 5, y + 26, cx + 5, y + 66], fill=(240, 236, 224))
    d.rectangle([x + 36, y + 66, x + 206, y + 72], fill=(240, 236, 224))
    d.rectangle([x + 96, y + 76, x + 146, y + 82], fill=(96, 74, 48))
    d.line([x + 118, y + 76, x + 118, y + 58], fill=(96, 74, 48), width=3)
    d.rectangle([x + 96, y + 54, x + 140, y + 60], fill=(96, 74, 48))
    d.text((x + 148, y + 12), "\u201cCOUP PLOT\u201d?", font=F_SANS_B(8),
           fill=RED)


def scene_shopping(d, x, y, w, h):
    scene_base(d, x, y, w, h, (250, 222, 170), (163, 22, 33))
    for bx, col in ((x + 30, (31, 78, 121)), (x + 100, (46, 110, 72)),
                    (x + 170, (176, 141, 44))):
        d.rectangle([bx, y + 34, bx + 44, y + 70], fill=col)
        d.arc([bx + 10, y + 22, bx + 34, y + 44], start=180, end=360,
              fill=INK, width=3)
    d.ellipse([x + 178, y + 6, x + 228, y + 40], fill=(255, 255, 255),
              outline=RED, width=2)
    d.text((x + 186, y + 12), "$12.9bn", font=F_SANS_B(11), fill=RED)
    d.text((x + 188, y + 26), "ONLINE", font=F_SANS_B(8), fill=INK)


SCENES = {
    "turkey": scene_turkey, "storm": scene_storm, "drone": scene_drone,
    "refinery": scene_refinery, "migration": scene_migration,
    "ecb": scene_ecb, "cyber": scene_cyber, "missile": scene_missile,
    "mine": scene_mine, "candles": scene_candles, "court": scene_court,
    "shopping": scene_shopping,
}

# ---------------------------------------------------------------- layout
COL_X = [14, 265, 516, 767]
COL_W = 243
GRID_TOP = 104
FEAT_H = 202
SCENE_H = 88

BY_NUM = {s["n"]: s for s in STORIES}

# lon, lat, nudge dx, dy for the 12 feature pins on the locator map.
PINS = [
    (-77, 39, 0, 0), (-82, 32, -8, 6), (-74, 41, -4, -8), (48, 29, 0, 0),
    (42, 17, 0, 0), (0, 51, 0, -6), (8, 50, 10, 4), (121, 25, 0, 0),
    (126, 39, 0, 0), (107, -6, 0, 0), (114, 22, 0, 0), (28, -15, 0, 0),
]
PIN_NUMS = [1, 5, 8, 9, 10, 15, 16, 22, 23, 29, 30, 33]

# Rough continent outlines (lon, lat), equirectangular, stylised.
CONTINENTS = [
    [(-168, 65), (-150, 70), (-130, 71), (-110, 68), (-90, 69), (-82, 66),
     (-75, 62), (-65, 60), (-55, 52), (-60, 47), (-70, 44), (-75, 39),
     (-80, 32), (-84, 30), (-90, 29), (-97, 26), (-105, 20), (-110, 23),
     (-115, 30), (-125, 40), (-125, 49), (-135, 58), (-155, 58),
     (-165, 60)],
    [(-58, 64), (-45, 60), (-30, 68), (-22, 70), (-40, 76), (-58, 74)],
    [(-80, 9), (-72, 12), (-62, 10), (-52, 5), (-50, -2), (-40, -5),
     (-35, -9), (-40, -20), (-48, -28), (-55, -35), (-65, -41),
     (-70, -50), (-73, -53), (-70, -40), (-72, -25), (-77, -12),
     (-81, -6), (-80, 2)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (3, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62),
     (25, 66), (20, 70), (15, 70), (25, 71), (30, 70), (40, 68),
     (45, 66), (50, 69), (55, 68), (60, 69), (68, 68), (70, 72),
     (60, 70), (50, 68), (44, 60), (40, 55), (35, 50), (30, 46),
     (28, 44), (23, 40), (20, 40), (15, 38), (10, 38), (3, 38),
     (-2, 37), (-6, 36)],
    [(-17, 15), (-16, 20), (-10, 30), (-5, 35), (0, 36), (10, 37),
     (20, 32), (30, 31), (32, 31), (35, 28), (38, 22), (40, 15),
     (43, 11), (48, 11), (51, 10), (46, 0), (40, -10), (35, -20),
     (32, -29), (28, -33), (20, -35), (15, -30), (12, -18), (12, -8),
     (9, 0), (9, 4), (-8, 5), (-13, 8), (-17, 12)],
    [(30, 70), (40, 68), (50, 69), (60, 70), (70, 72), (80, 73),
     (90, 75), (100, 77), (110, 76), (120, 73), (130, 72), (140, 72),
     (150, 70), (160, 69), (170, 67), (178, 65), (170, 60), (162, 56),
     (158, 52), (150, 59), (142, 55), (140, 50), (135, 45), (130, 42),
     (127, 40), (122, 38), (120, 32), (122, 28), (118, 25), (110, 20),
     (108, 15), (105, 10), (100, 8), (98, 12), (95, 16), (92, 20),
     (88, 22), (85, 18), (80, 15), (77, 8), (75, 12), (72, 20),
     (68, 23), (62, 25), (58, 26), (55, 26), (52, 28), (50, 29),
     (48, 30), (44, 29), (40, 28), (38, 24), (35, 28), (35, 36),
     (32, 36), (28, 38), (26, 40), (30, 42), (35, 45), (40, 48),
     (45, 50), (50, 55), (55, 60), (50, 65), (45, 68), (40, 70)],
    [(95, 5), (100, 2), (103, -2), (105, -5), (110, -7), (115, -8),
     (120, -10), (125, -8), (130, -4), (135, -3), (138, -5), (140, -8),
     (135, -8), (130, -6), (125, -3), (120, 0), (115, 2), (110, 5),
     (105, 8), (100, 10)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32),
     (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15),
     (142, -11), (137, -12), (135, -15), (132, -12), (130, -13),
     (126, -14), (122, -17), (118, -20), (114, -21)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 36), (140, 38),
     (141, 40), (142, 42), (144, 44), (142, 44), (140, 40), (138, 38),
     (136, 36), (134, 34), (131, 32)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
     (-2, 50)],
]

# Feature cities east to west, with UTC offsets, for the world strip.
WORLD_STRIP = [
    ("PYONGYANG", 126, "+9"), ("TAIPEI", 121, "+8"),
    ("HONG KONG", 114, "+8"), ("INDONESIA", 107, "+7"),
    ("KUWAIT", 48, "+3"), ("JAZAN", 42, "+3"), ("LUSAKA", 28, "+2"),
    ("FRANKFURT", 8, "+1"), ("LONDON", 0, "+0"),
    ("NEW YORK", -74, "\u22125"), ("WASHINGTON", -77, "\u22125"),
    ("US EAST", -82, "\u22125"),
]


def draw_labeled(d, x, y, label, text, lfnt, tfnt, width, max_lines=2,
                 line_h=13):
    """'LABEL text...' with the label bold and the rest in tfnt; wraps to
    max_lines. Returns the y after the last line."""
    lw = d.textlength(label, font=lfnt)
    words = text.split()
    lines, cur, first = [], "", True
    for w in words:
        avail = width - (lw + 4 if first else 0)
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=tfnt) <= avail or not cur:
            cur = trial
        else:
            lines.append((cur, first))
            cur, first = w, False
    if cur:
        lines.append((cur, first))
    lines = lines[:max_lines]
    for i, (ln, is_first) in enumerate(lines):
        yy = y + i * line_h
        tx = x
        if is_first:
            d.text((x, yy), label, font=lfnt, fill=RED)
            tx = x + lw + 4
        d.text((tx, yy), ln, font=tfnt, fill=INK)
    return y + len(lines) * line_h


def draw_feature(d, x, y, story):
    d.text((x, y), f"{story['n']:02d}", font=F_SANS_B(13), fill=RED)
    num_w = d.textlength(f"{story['n']:02d}", font=F_SANS_B(13))
    d.text((x + num_w + 6, y + 2), story["place"], font=F_SANS_B(10),
           fill=INK)
    tag_w = draw_tag(d, x + COL_W - 62, y, story["tag"])
    d.line([x, y + 17, x + COL_W, y + 17], fill=RULE, width=1)
    SCENES[story["scene"]](d, x, y + 21, COL_W, SCENE_H)
    yy = y + 21 + SCENE_H + 5
    for ln in wrap(d, story["headline"], F_SANS_B(13), COL_W)[:2]:
        d.text((x, yy), ln, font=F_SANS_B(13), fill=INK)
        yy += 15
    yy += 2
    for ln in wrap(d, story["summary"], F_SANS(10), COL_W)[:2]:
        d.text((x, yy), ln, font=F_SANS(10), fill=MUTED)
        yy += 12
    yy += 2
    yy = draw_labeled(d, x, yy, "WHY IT MATTERS:", story["why"],
                      F_SANS_B(9), F_SERIF(10), COL_W, max_lines=2)
    return yy


def draw_map(d, x, y, w, h):
    d.text((x, y), "WHERE THE NEWS HAPPENED", font=F_SANS_B(10), fill=INK)
    my = y + 15
    mh = h - 30
    d.rectangle([x, my, x + w, my + mh], fill=(214, 228, 238),
                outline=RULE)
    def px(lon, lat):
        return (x + (lon + 180) / 360 * w,
                my + (75 - lat) / 135 * mh)
    for poly in CONTINENTS:
        d.polygon([px(lon, lat) for lon, lat in poly],
                  fill=(240, 232, 205), outline=(120, 116, 104))
    for (lon, lat, dx, dy), num in zip(PINS, PIN_NUMS):
        cx, cy = px(lon, lat)
        cx += dx
        cy += dy
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(num)
        d.text((cx - d.textlength(t, font=F_SANS_B(8)) / 2, cy - 5), t,
               font=F_SANS_B(8), fill=(255, 255, 255))
    d.text((x, my + mh + 4), "Numbered pins mark the 12 illustrated stories. "
           "Stylised map.", font=F_SANS(8), fill=MUTED)


def draw_world_strip(d, x, y, w, h):
    d.text((x, y), "THE DAY AROUND THE WORLD", font=F_SANS_B(10), fill=INK)
    mid = y + 58
    d.line([x, mid, x + w, mid], fill=RULE, width=2)
    rows = (-30, -16, 12, 26)
    for i, (city, lon, off) in enumerate(WORLD_STRIP):
        cx = x + (i + 0.5) / len(WORLD_STRIP) * w
        d.ellipse([cx - 5, mid - 5, cx + 5, mid + 5], fill=BLUE,
                  outline=(255, 255, 255), width=1)
        lab = f"{city} {off}"
        lw = d.textlength(lab, font=F_SANS_B(8))
        lx = min(max(cx - lw / 2, x), x + w - lw)
        d.text((lx, mid + rows[i % 4]), lab, font=F_SANS_B(8), fill=INK)
    d.text((x, mid + 40), "From Pyongyang's morning to New York's night \u2014 "
           "one Friday, every time zone. East to west.", font=F_SANS(8),
           fill=MUTED)
    d.text((x, mid + 50), "Dots run east to west; offsets are each city's "
           "UTC offset on 27 November.", font=F_SANS(8), fill=MUTED)


def draw_date_check(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RED, width=2)
    d.text((x + 8, y + 6), "DATE CHECK \u2014 NOT 27 NOVEMBER NEWS",
           font=F_SANS_B(10), fill=RED)
    yy = y + 24
    for name, note in DATE_CHECK:
        for ln in wrap(d, f"{name} \u2014 {note}", F_SANS(9), w - 16)[:2]:
            d.text((x + 8, yy), ln, font=F_SANS(9), fill=INK)
            yy += 11
        yy += 2
    yy += 2
    d.line([x + 8, yy, x + w - 8, yy], fill=RULE, width=1)
    yy += 5
    for ln in wrap(d, REPORTED_NOTE, F_SERIF(9), w - 16)[:3]:
        d.text((x + 8, yy), ln, font=F_SERIF(9), fill=MUTED)
        yy += 11


def draw_index(d, x, y, w):
    d.text((x, y), "ALSO ON FRIDAY \u2014 28 MORE STORIES",
           font=F_SANS_B(11), fill=INK)
    d.line([x, y + 15, x + w, y + 15], fill=RULE, width=1)
    rest = [s for s in STORIES if s["n"] not in FEATURES]
    yy = y + 20
    per_col = 7
    for col in range(4):
        cx = x + col * (COL_W + 8)
        for row in range(per_col):
            s = rest[col * per_col + row]
            num = f"{s['n']:02d} \u00b7 "
            nw = d.textlength(num, font=F_SANS_B(9))
            d.text((cx, yy + row * 12), num, font=F_SANS_B(9), fill=RED)
            head = s["headline"]
            while (d.textlength(head, font=F_SANS(9)) > COL_W - nw
                   and len(head) > 4):
                head = head[:-2]
            if head != s["headline"]:
                head = head.rstrip() + "\u2026"
            d.text((cx + nw, yy + row * 12), head, font=F_SANS(9),
                   fill=INK)


def build():
    regions = sorted({s["region"] for s in STORIES})
    fields = sorted({s["field"] for s in STORIES})
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    title = "THE WORLD IN ONE DAY"
    tf = F_SERIF_B(46)
    d.text(((W - d.textlength(title, font=tf)) / 2, 8), title, font=tf,
           fill=INK)
    sub = "FRIDAY, 27 NOVEMBER 2026  \u00b7  THE DAY'S NEWS IN ONE PICTURE"
    sf = F_SANS_B(13)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 60), sub, font=sf,
           fill=INK)
    d.line([14, 78, W - 14, 78], fill=INK, width=2)

    # Stats strip.
    stats = (f"{len(STORIES)} STORIES  \u00b7  {len(regions)} REGIONS  "
             f"\u00b7  {len(fields)} FIELDS  \u00b7  {len(FEATURES)} "
             f"ILLUSTRATED HEADLINES  \u00b7  ALL REPORTED 27 NOVEMBER 2026")
    d.rectangle([14, 82, W - 14, 100], fill=INK)
    stf = F_SANS_B(12)
    d.text(((W - d.textlength(stats, font=stf)) / 2, 86), stats, font=stf,
           fill=(255, 255, 255))

    # Four-column broadsheet grid: three illustrated features per column.
    for col in range(4):
        cx = COL_X[col]
        for row in range(3):
            n = FEATURES[col * 3 + row]
            y0 = GRID_TOP + row * FEAT_H
            end = draw_feature(d, cx, y0, BY_NUM[n])
            if end > y0 + FEAT_H - 4:
                print(f"WARNING: feature {n} overflows slot by "
                      f"{end - (y0 + FEAT_H - 4):.0f}px")
            if row < 2:
                d.line([cx, y0 + FEAT_H - 4, cx + COL_W, y0 + FEAT_H - 4],
                       fill=(200, 196, 186), width=1)
        if col < 3:
            d.line([cx + COL_W + 4, GRID_TOP, cx + COL_W + 4,
                    GRID_TOP + 3 * FEAT_H - 8], fill=(200, 196, 186),
                   width=1)

    # Bottom band: map, world strip, date check.
    band_y = GRID_TOP + 3 * FEAT_H + 6
    band_h = 134
    d.line([14, band_y - 4, W - 14, band_y - 4], fill=INK, width=2)
    draw_map(d, 14, band_y, 316, band_h)
    draw_world_strip(d, 338, band_y, 322, band_h)
    draw_date_check(d, 668, band_y, W - 14 - 668, band_h)

    # "Also on Friday" index.
    idx_y = band_y + band_h + 10
    draw_index(d, 14, idx_y, W - 28)

    # Footer: HOW SURE legend, sources, credit.
    fy = idx_y + 20 + 7 * 12 + 8
    d.line([14, fy, W - 14, fy], fill=INK, width=2)
    fy += 6
    how = ("HOW SURE \u2014  OFFICIAL: stated by an authority  \u00b7  "
           "CLAIM: attributed, unconfirmed  \u00b7  CLOSE: final reported "
           "price  \u00b7  REPORT: press report")
    d.text((14, fy), how, font=F_SANS(9), fill=INK)
    fy += 13
    src = ("SOURCES: AP \u00b7 REUTERS \u00b7 AL JAZEERA \u00b7 DAWN \u00b7 "
           "DECCAN CHRONICLE \u00b7 SCMP \u00b7 RNZ \u00b7 KYIV POST \u00b7 "
           "NIKKEI ASIA \u00b7 XINHUA \u00b7 THE GUARDIAN \u00b7 ADOBE")
    d.text((14, fy), src, font=F_SANS(8), fill=MUTED)
    fy += 12
    d.text((14, fy), "All 40 stories were reported on Friday 27 November "
           "2026. Drawn from verified reports only \u2014 nothing invented.",
           font=F_SERIF(9), fill=MUTED)
    if fy + 12 > H - 6:
        print(f"WARNING: footer ends at {fy + 12}, page is {H}px")
    return img, len(regions), len(fields)


if __name__ == "__main__":
    image, n_regions, n_fields = build()
    image.save("entry.png", format="PNG", optimize=True)
    data = open("entry.png", "rb").read()
    print(f"entry.png: {len(data)} bytes, "
          f"sha256 {hashlib.sha256(data).hexdigest()}")
    print(f"stories={len(STORIES)} regions={n_regions} "
          f"fields={n_fields} features={len(FEATURES)} "
          f"index={len(STORIES) - len(FEATURES)}")
