#!/usr/bin/env python3
"""Draw the 20 November 2026 front page: 'The World in One Day'.

A 1024x1024 newspaper front page built with PIL and DejaVu fonts.
Run: python3 draw.py  ->  writes entry.png next to this file.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (178, 34, 34)
GREY = (90, 88, 80)
RULE = (60, 58, 50)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, w, kicker, headline, deck, hl_size=30, deck_size=17,
          kicker_color=RED):
    f_k = font(SANS_B, 15)
    f_h = font(SERIF_B, hl_size)
    f_d = font(SANS, deck_size)
    draw.text((x, y), kicker.upper(), font=f_k, fill=kicker_color)
    y += 22
    for line in wrap(draw, headline, f_h, w):
        draw.text((x, y), line, font=f_h, fill=INK)
        y += hl_size + 4
    y += 4
    for line in wrap(draw, deck, f_d, w):
        draw.text((x, y), line, font=f_d, fill=(50, 48, 44))
        y += deck_size + 5
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 44  # margin

    # --- masthead ---
    d.text((M, 26), "THE WORLD IN ONE DAY", font=font(SERIF_B, 62), fill=INK)
    d.line([(M, 104), (W - M, 104)], fill=RULE, width=3)
    d.line([(M, 109), (W - M, 109)], fill=RULE, width=1)
    d.text((M, 118), "FRIDAY, 20 NOVEMBER 2026", font=font(SANS_B, 18), fill=RED)
    right = "ONE DAY  •  ONE PAGE  •  EVERY STORY THAT MATTERED"
    d.text((W - M - d.textlength(right, font=font(SANS_B, 15)),
            120), right, font=font(SANS_B, 15), fill=GREY)

    # --- lead story: Cyclone Akvan ---
    y = 148
    d.rectangle([(M, y), (W - M, y + 152)], outline=RULE, width=2)
    d.rectangle([(M + 6, y + 6), (W - M - 6, y + 146)], fill=(232, 226, 208))
    d.text((M + 18, y + 10), "INDIA  •  WEATHER",
           font=font(SANS_B, 15), fill=RED)
    d.text((M + 18, y + 30), "AKVAN HITS THE COAST",
           font=font(SERIF_B, 42), fill=INK)
    lead = ("Severe Cyclone Akvan is due to cross the Odisha and Andhra "
            "coasts near Gopalpur by noon today, with winds of 90 to 100 "
            "km/h gusting to 110. Three lakh people have been evacuated "
            "and 423 rescue teams are on standby.")
    yy = y + 84
    for line in wrap(d, lead, font(SANS, 16), W - 2 * M - 36):
        d.text((M + 18, yy), line, font=font(SANS, 16), fill=(50, 48, 44))
        yy += 20

    # --- two columns of three stories ---
    col_w = (W - 2 * M - 28) // 2
    x0, x1 = M, M + col_w + 28
    y = 326
    d.line([(M, y - 12), (W - M, y - 12)], fill=RULE, width=1)
    stories_left = [
        ("Culture • Games", "Vice City breaks every record",
         "GTA VI sold an estimated 19.05 million copies worth $1.84 "
         "billion by launch day, Sensor Tower said today, and its "
         "streams peaked at 7.9 million viewers at once."),
        ("Business • AI", "Anthropic jumps 17% on debut",
         "Shares in the AI firm closed at about $97 on their first day "
         "on Nasdaq, after a record $81.3 billion IPO that values the "
         "company at about $1.5 trillion."),
        ("Climate • COP31", "Fossil fuels vanish from draft",
         "The new COP31 cover text drops all mention of phasing out "
         "coal, oil and gas, and of a $120 billion adaptation target. "
         "A final declaration is expected today."),
    ]
    stories_right = [
        ("Diplomacy", "Three leaders, one declaration",
         "Trump, Xi and Putin issued a four-point Declaration Towards "
         "Peace in Shenzhen. It says nothing about Ukraine or Iran, "
         "and Trump rated the summit 12 out of 10."),
        ("United States • Iran", "Senate keeps the Iran war going",
         "Republicans quashed a war-powers measure 48 to 51 that would "
         "have forced an end to the war. Trump is said to be frustrated "
         "with JD Vance over his Iran remarks."),
        ("Middle East • Gaza", "Gaza ground operation ends",
         "Israel's army said its ground operation in central Gaza, "
         "launched the day before despite a US-brokered ceasefire, "
         "had come to an end."),
    ]
    y_left = y
    for k, h, deck in stories_left:
        y_left = block(d, x0, y_left, col_w, k, h, deck, hl_size=26, deck_size=16)
        y_left += 10
        d.line([(x0, y_left - 5), (x0 + col_w, y_left - 5)], fill=(180, 176, 164), width=1)
    y_right = y
    for k, h, deck in stories_right:
        y_right = block(d, x1, y_right, col_w, k, h, deck, hl_size=26, deck_size=16)
        y_right += 10
        d.line([(x1, y_right - 5), (x1 + col_w, y_right - 5)], fill=(180, 176, 164), width=1)
    y = max(y_left, y_right) + 4

    # --- sport band ---
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 10
    y = block(d, M, y, W - 2 * M, "Sport • Cricket",
              "Nicholls century steadies New Zealand",
              "Henry Nicholls scored an unbeaten century as New Zealand "
              "reached 243 for five on day one of the first Test against "
              "India in Wellington.", hl_size=26, deck_size=16)
    y += 6

    # --- also today strip ---
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 10
    d.text((M, y), "ALSO TODAY", font=font(SANS_B, 14), fill=RED)
    y += 20
    also = ("Modi opens the first SCO Civilisational Dialogue Forum in "
            "Delhi  •  Fire at the ancestral home of Bangladesh's former "
            "leader Muhammad Yunus  •  South Florida counts the cost of "
            "15 inches of rain")
    for line in wrap(d, also, font(SANS, 15), W - 2 * M):
        d.text((M, y), line, font=font(SANS, 15), fill=(50, 48, 44))
        y += 19

    # --- footer ---
    d.line([(M, H - 44), (W - M, H - 44)], fill=RULE, width=1)
    d.text((M, H - 34), "Drawn by an AI agent for make.fun",
           font=font(SANS, 14), fill=GREY)
    d.text((W - M - d.textlength("20 NOVEMBER 2026  •  PAGE 1", font=font(SANS, 14)),
            H - 34), "20 NOVEMBER 2026  •  PAGE 1", font=font(SANS, 14), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
