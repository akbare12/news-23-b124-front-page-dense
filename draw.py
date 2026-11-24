#!/usr/bin/env python3
"""news-23 b124 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
31 stories, 1024x1024, PIL only. Run: python3 draw.py -> entry.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FD, "DejaVuSerif.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")

def F(path, size):
    return ImageFont.truetype(path, size)

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (212, 175, 55)
RED = (178, 34, 34)
DARKRED = (139, 0, 0)
NAVY = (10, 30, 80)
GREEN = (27, 94, 32)
TEAL = (0, 105, 105)
PURPLE = (74, 20, 90)
GREY = (120, 120, 120)
CREAM = (250, 246, 236)
LGREEN = (200, 230, 201)
MGREEN = (165, 214, 167)
INK = (20, 20, 20)
MIDGREY = (90, 90, 90)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

# ---------- masthead ----------
d.rectangle([0, 0, W, 52], fill=BLACK)
text(12, 6, "THE WORLD TODAY", F(SERIF_B, 40), WHITE)
text(W - 12, 14, "MONDAY 23 NOVEMBER 2026", F(SANS_B, 17), GOLD, anchor="ra")

# ---------- kicker ----------
d.rectangle([0, 52, W, 72], fill=RED)
text(W // 2, 56, "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
     F(SANS_B, 14), WHITE, anchor="ma")

# ---------- number strip (2 rows x 5) ----------
strip = [
    ("-3.3%", "KOSPI"),
    ("5.3", "US-CHINA POWER GAP"),
    ("11,762", "EBOLA CASES, DRC"),
    ("10T won", "SEOUL STABILISATION FUND"),
    ("2%", "BILLIONAIRE TAX IN PARIS"),
    ("$450M", "SKUBAL DEAL"),
    ("165", "RUSSIAN MISSILES/WEEK"),
    ("12,000", "CLEARED IN MANCHESTER"),
    ("264 kg", "EXPLOSIVES SEIZED"),
    ("$107.3B", "ANTHROPIC IPO"),
]
cw = W // 5
for i, (val, lab) in enumerate(strip):
    r, c = divmod(i, 5)
    x = c * cw + 12
    yv = 84 if r == 0 else 116
    yl = 104 if r == 0 else 136
    text(x, yv, val, F(SANS_B, 24), INK)
    text(x, yl, lab, F(SANS, 10), MIDGREY)
# thin rule under strip
d.line([0, 156, W, 156], fill=(200, 200, 200), width=1)

# ---------- region bar ----------
regions = [
    ("ASIA-PACIFIC 7", NAVY, 7),
    ("AMERICAS 8", RED, 8),
    ("MIDDLE EAST 6", TEAL, 6),
    ("EUROPE 5", PURPLE, 5),
    ("AFRICA 3", GREEN, 3),
    ("WORLD 2", GREY, 2),
]
x = 0
for name, col, n in regions:
    wseg = int(round(W * n / 31.0))
    d.rectangle([x, 156, x + wseg, 176], fill=col)
    text(x + wseg // 2, 161, name, F(SANS_B, 12), WHITE, anchor="ma")
    x += wseg

# ---------- UTC strip ----------
d.rectangle([0, 176, W, 192], fill=(238, 238, 238))
text(12, 179, "THE DAY IN UTC   \u00b7   ~00:00 Kospi dives   \u00b7   ~05:30 Guterres opens   \u00b7   ~09:00 Power Index   \u00b7   ~12:00 Paris 2% tax   \u00b7   ~15:00 Kyiv missiles",
     F(SANS, 10), MIDGREY)
text(W - 12, 179, "~ APPROX", F(SANS, 10), MIDGREY, anchor="ra")

# ---------- heroes ----------
HX = [8, 350, 692]          # hero column x (each 324 wide)
HW = 324
HY_SCENE = 192
HY_HEAD = 328
HY_BODY = 368
HY_SRC = 396

def hero_scene_kospi(x0):
    d.rectangle([x0, HY_SCENE, x0 + HW, HY_SCENE + 130], fill=NAVY)
    # skyline: buildings with lit windows
    import random
    rnd = random.Random(42)
    bx = x0 + 8
    while bx < x0 + HW - 14:
        bw = rnd.randint(18, 30)
        bh = rnd.randint(45, 105)
        by = HY_SCENE + 130 - bh
        d.rectangle([bx, by, bx + bw, HY_SCENE + 130], fill=(16, 42, 100))
        for wy in range(by + 6, HY_SCENE + 124, 12):
            for wx in range(bx + 4, bx + bw - 4, 9):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
        bx += bw + 4
    # descending chart line, routed right of the big number
    pts = [(x0 + 150, 214), (x0 + 180, 226), (x0 + 210, 222), (x0 + 240, 240),
           (x0 + 270, 238), (x0 + 300, 258), (x0 + 318, 268)]
    d.line(pts, fill=(255, 140, 0), width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=WHITE)
    text(x0 + 10, HY_SCENE + 8, "-3.3%", F(SANS_B, 34), WHITE)
    # caption on solid navy band at scene bottom
    d.rectangle([x0, HY_SCENE + 108, x0 + HW, HY_SCENE + 130], fill=NAVY)
    text(x0 + 10, HY_SCENE + 112, "KOSPI 4,708.54  \u00b7  -161 PTS", F(SANS_B, 12), WHITE)

def hero_scene_guterres(x0):
    d.rectangle([x0, HY_SCENE, x0 + HW, HY_SCENE + 130], fill=GREEN)
    text(x0 + 12, HY_SCENE + 10, "150", F(SANS_B, 54), GOLD)
    text(x0 + 12, HY_SCENE + 66, "DELEGATES", F(SANS_B, 17), GOLD)
    text(x0 + 12, HY_SCENE + 86, "BACK A RISK", F(SANS_B, 17), GOLD)
    text(x0 + 12, HY_SCENE + 106, "FRAMEWORK", F(SANS_B, 17), GOLD)
    # globe, right side
    cx, cy, r = x0 + 258, HY_SCENE + 62, 48
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(220, 240, 220), outline=(180, 210, 180), width=2)
    for k in range(-2, 3):
        d.arc([cx - r + abs(k) * 12, cy - r, cx + r - abs(k) * 12, cy + r], 270, 90, fill=(140, 180, 140), width=1)
        d.arc([cx - r + abs(k) * 12, cy - r, cx + r - abs(k) * 12, cy + r], 90, 270, fill=(140, 180, 140), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(140, 180, 140), width=1)
    d.line([cx, cy - r, cx, cy + r], fill=(140, 180, 140), width=1)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(120, 160, 120), width=2)

def hero_scene_power(x0):
    d.rectangle([x0, HY_SCENE, x0 + HW, HY_SCENE + 130], fill=CREAM)
    text(x0 + 10, HY_SCENE + 6, "NARROWEST SINCE 2018", F(SANS_B, 14), INK)
    text(x0 + HW - 10, HY_SCENE + 6, "GAP 5.3", F(SANS_B, 14), RED, anchor="ra")
    bars = [("78.9", "US", NAVY, 250), ("73.6", "CHINA", RED, 232), ("40.5", "INDIA", (176, 141, 0), 128)]
    y = HY_SCENE + 32
    for val, name, col, blen in bars:
        text(x0 + 10, y, val, F(SANS_B, 14), INK)
        d.rectangle([x0 + 64, y + 2, x0 + 64 + blen, y + 22], fill=col)
        text(x0 + 70, y + 4, name, F(SANS_B, 13), WHITE)
        y += 30

def hero(x0, scene_fn, headline, body, source):
    scene_fn(x0)
    hl = wrap(headline, F(SANS_B, 19), HW)
    y = HY_HEAD
    for ln in hl[:2]:
        text(x0, y, ln, F(SANS_B, 19), INK)
        y += 22
    bl = wrap(body, F(SANS, 11), HW)
    y = HY_BODY
    for ln in bl[:2]:
        text(x0, y, ln, F(SANS, 11), INK)
        y += 13
    text(x0, HY_SRC, source, F(SANS, 9), MIDGREY)
    # REPORTED chip, right-aligned at source row
    chip = "REPORTED"
    cf = F(SANS_B, 9)
    cwpx = d.textlength(chip, font=cf) + 12
    d.rectangle([x0 + HW - cwpx, HY_SRC - 1, x0 + HW, HY_SRC + 13], fill=NAVY)
    text(x0 + HW - cwpx + 6, HY_SRC + 1, chip, cf, WHITE)

hero(HX[0], hero_scene_kospi, "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE")
hero(HX[1], hero_scene_guterres, "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS")
hero(HX[2], hero_scene_power, "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE")

# ---------- MORE strip ----------
d.rectangle([0, 416, W, 436], fill=BLACK)
text(12, 421, "MORE OF THE DAY  \u2014  10 STORIES", F(SANS_B, 13), WHITE)

# ---------- cards ----------
cards = [
    ("AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "WSJ", "REPORTED"),
    ("AMERICAS", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.", "AP", "REPORTED"),
    ("SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
CARD_W = 200
CARD_H = 68
for i, (reg, head, body, src, chip) in enumerate(cards):
    r, c = divmod(i, 5)
    x0 = 8 + c * 202
    y0 = 440 + r * 72
    # region + number
    text(x0, y0, reg, F(SANS_B, 9), RED)
    text(x0 + CARD_W - 4, y0, str(i + 1), F(SANS_B, 11), RED, anchor="ra")
    # headline, up to 2 lines
    hl = wrap(head, F(SANS_B, 12), CARD_W)
    y = y0 + 14
    for ln in hl[:2]:
        text(x0, y, ln, F(SANS_B, 12), INK)
        y += 14
    # body on its own row
    text(x0, y0 + 44, body, F(SANS, 9), INK)
    # source + chip on bottom row
    text(x0, y0 + 57, src, F(SANS, 8), MIDGREY)
    cf = F(SANS_B, 8)
    cwpx = d.textlength(chip, font=cf) + 10
    chipcol = NAVY if chip == "REPORTED" else RED
    d.rectangle([x0 + CARD_W - cwpx, y0 + 54, x0 + CARD_W, y0 + 66], fill=chipcol)
    text(x0 + CARD_W - cwpx + 5, y0 + 56, chip, cf, WHITE)

# ---------- WHERE strip ----------
d.rectangle([0, 588, W, 608], fill=BLACK)
text(12, 593, "WHERE IT HAPPENED", F(SANS_B, 13), WHITE)

# ---------- map + ALSO ----------
MAP_X0, MAP_Y0 = 8, 612
# continent blobs (stylised)
d.polygon([(20, 620), (120, 612), (138, 660), (120, 730), (70, 748), (30, 720), (16, 670)], fill=LGREEN)
d.polygon([(150, 616), (232, 612), (242, 650), (228, 690), (190, 700), (152, 672), (146, 640)], fill=LGREEN)
d.polygon([(238, 614), (322, 610), (326, 660), (310, 712), (262, 716), (238, 680)], fill=LGREEN)
d.polygon([(176, 700), (252, 698), (258, 740), (230, 762), (190, 756), (172, 728)], fill=MGREEN)
pins = [
    (1, 292, 640), (2, 60, 712), (3, 284, 620), (4, 56, 652), (5, 82, 626),
    (6, 218, 632), (7, 188, 656), (8, 172, 640), (9, 224, 652), (10, 162, 624),
    (11, 252, 688), (12, 260, 704), (13, 214, 732),
]
for n, px, py in pins:
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=WHITE, width=2)
    text(px, py - 6, str(n), F(SANS_B, 10), WHITE, anchor="ma")
# legend, 4 lines under the blobs
leg = [
    "Pins 1\u201313: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing",
    "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Paris",
    "8 London \u00b7 9 Warsaw \u00b7 10 Manchester \u00b7 11 Beirut",
    "12 Gaza \u00b7 13 Khartoum",
]
y = 768
for ln in leg:
    text(MAP_X0, y, ln, F(SANS, 9), MIDGREY)
    y += 12

# ALSO list, 2 columns x 9 rows
also = [
    "14. Paris: 100+ back 2% billionaire tax",
    "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week",
    "17. COP31: the day after Antalya pact rejected",
    "18. Israel unity talks resume",
    "19. Gaza: two killed in Israeli strike",
    "20. West Bank settler attacks",
    "21. Iran war: no deal in sight",
    "22. Lebanon seizes 264 kg explosives",
    "23. Bahrain: strike hits plant, 2 hurt",
    "24. Benghazi: UN demands probe [CLAIM]",
    "25. Sudan: defences down drones [CLAIM]",
    "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row",
    "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
text(344, 616, "ALSO ON MONDAY", F(SANS_B, 13), INK)
for i, item in enumerate(also):
    col, row = divmod(i, 9)
    x = 344 + col * 336
    y = 638 + row * 20
    # red [CLAIM] marker
    if "[CLAIM]" in item:
        base, _ = item.split(" [CLAIM]")
        text(x, y, base, F(SANS, 11), INK)
        bx = x + d.textlength(base, font=F(SANS, 11)) + 4
        text(bx, y, "[CLAIM]", F(SANS_B, 11), RED)
    else:
        text(x, y, item, F(SANS, 11), INK)

# ---------- DATE CHECK ----------
d.rectangle([8, 818, W - 8, 902], outline=DARKRED, width=2)
text(16, 826, "DATE CHECK  \u2014  READ 23 NOV 2026, 23:59 UTC  \u00b7  STORIES DATED 23 NOV ONLY",
     F(SANS_B, 12), DARKRED)
text(16, 846, "LEFT OUT \u2014 NOT 23 NOV:  Dems reach 258 (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo Isidro captured (22 Nov)",
     F(SANS, 11), INK)
text(16, 862, "EU\u2013Indonesia pact (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar ruling (19 Nov)",
     F(SANS, 11), INK)
text(16, 880, "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff",
     F(SANS, 11), INK)

# ---------- footer ----------
text(12, 912, "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
     F(SANS, 10), MIDGREY)
text(12, 928, "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's claim, independently unconfirmed \u00b7 ONGOING = still developing.",
     F(SANS, 10), MIDGREY)
text(12, 944, "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
     F(SANS, 10), MIDGREY)
text(W // 2, 968, "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions",
     F(SANS_B, 12), GOLD, anchor="ma")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
