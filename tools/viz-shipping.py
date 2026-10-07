"""Draws assets/viz/shipping-numbers.svg and shipping-farms.svg for module 4 (The shipping point).

shipping-numbers: every figure of the cucumber trade found in a source of the time, as given: crates per season
  (1897, Cammack's undated season, 1919) and cars per day (1907, 1910, 1919), with the unsourced
  “seventy-five carloads a day” of recent accounts shown dashed and marked.
shipping-farms: Bulletin 175 (1925), the 120 farms of 1923: where the receipts came from (Table 4) and what the labour
  cost, by kind and by share of farms (Table 5).
Run from the site root: python tools/viz-shipping.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
T = "#/text/shipping/"


def numbers():
    W, H = 900, 470
    title = "Every figure, as the sources give it"
    desc = ("Crates of cucumbers per season: 20,000 in 1897 (Ocala Evening Star); 57,000 in one season not named (Cammack, 1916); over 200,000 in 1919 (Lakeland Evening Telegram). "
            "Cars per day: nine in one day in 1907, by hearsay; 22 a day at the height of the 1910 season; 13 to 20 a day in the peak week of 1919. "
            "Seventy-five carloads a day appears only in recent accounts and has no source of the time.")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="sn-t sn-d" font-family="var(--serif)">',
         f'<title id="sn-t">{escape(title)}</title><desc id="sn-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         f'<text x="16" y="48" font-size="13" fill="var(--ink2)">Williston’s cucumber trade in the sources of its time. Each label links to its passage.</text>']
    # left: crates per season
    X0, base, top = 70, 400, 110
    sc = (base - top) / 220000
    o.append(f'<text x="16" y="84" font-size="14" font-weight="bold" fill="var(--ink)">Crates in a season</text>')
    for v in (0, 50000, 100000, 150000, 200000):
        y = base - v * sc
        o.append(f'<line x1="{X0}" y1="{y:.0f}" x2="400" y2="{y:.0f}" stroke="var(--line)"/>'
                 f'<text x="{X0 - 6}" y="{y + 4:.0f}" font-size="11" text-anchor="end" fill="var(--ink2)">{v:,}</text>')
    bars = [("1897", 20000, "20,000", "first/1", False), ("season?", 57000, "57,000", "trainload/9", False), ("1919", 200000, "over 200,000", "season/12", False)]
    x = X0 + 30
    for lab, v, txt, href, _ in bars:
        h = v * sc
        o.append(f'<a href="{T}{href}"><rect x="{x}" y="{base - h:.0f}" width="62" height="{h:.0f}" fill="var(--crop)"/>'
                 f'<text x="{x + 31}" y="{base - h - 6:.0f}" font-size="12" text-anchor="middle" fill="var(--ink)" text-decoration="underline">{txt}</text></a>'
                 f'<text x="{x + 31}" y="{base + 18}" font-size="12" text-anchor="middle" fill="var(--ink)">{escape(lab)}</text>')
        x += 100
    o.append(f'<text x="{X0}" y="{base + 40}" font-size="11.5" fill="var(--ink2)">“season?”: Cammack (1916) does not name the season.</text>')
    # right: cars per day
    X1, R = 470, 880
    sc2 = (base - top) / 80
    o.append(f'<text x="{X1 - 20}" y="84" font-size="14" font-weight="bold" fill="var(--ink)">Cars in a day</text>')
    for v in (0, 20, 40, 60, 80):
        y = base - v * sc2
        o.append(f'<line x1="{X1 + 10}" y1="{y:.0f}" x2="{R}" y2="{y:.0f}" stroke="var(--line)"/>'
                 f'<text x="{X1 + 4}" y="{y + 4:.0f}" font-size="11" text-anchor="end" fill="var(--ink2)">{v}</text>')
    pts = [("1907", 9, 9, "nine in one day (hearsay)", "first/5"), ("1910", 22, 22, "22 a day at the height", "trainload/6"),
           ("1919", 13, 20, "13 to 20 a day, peak week", "season/11")]
    x = X1 + 40
    for lab, lo, hi, txt, href in pts:
        if lo == hi:
            o.append(f'<rect x="{x}" y="{base - hi * sc2:.0f}" width="54" height="{hi * sc2:.0f}" fill="var(--rail)"/>')
        else:
            o.append(f'<rect x="{x}" y="{base - lo * sc2:.0f}" width="54" height="{lo * sc2:.0f}" fill="var(--rail)"/>'
                     f'<rect x="{x}" y="{base - hi * sc2:.0f}" width="54" height="{(hi - lo) * sc2:.0f}" fill="var(--rail)" opacity=".45"/>')
        o.append(f'<a href="{T}{href}"><text x="{x + 27}" y="{base - hi * sc2 - 6:.0f}" font-size="11.5" text-anchor="middle" fill="var(--ink)" text-decoration="underline">{hi if lo == hi else f"{lo}–{hi}"}</text></a>'
                 f'<text x="{x + 27}" y="{base + 18}" font-size="12" text-anchor="middle" fill="var(--ink)">{lab}</text>')
        x += 92
    # the unsourced 75
    h75 = 75 * sc2
    o.append(f'<a href="#/texts"><rect x="{x}" y="{base - h75:.0f}" width="54" height="{h75:.0f}" fill="none" stroke="var(--colour)" stroke-dasharray="5 4"/>'
             f'<text x="{x + 27}" y="{base - h75 - 6:.0f}" font-size="11.5" text-anchor="middle" fill="var(--colour)" text-decoration="underline">75?</text></a>'
             f'<text x="{x + 27}" y="{base + 18}" font-size="12" text-anchor="middle" fill="var(--colour)">recent</text>')
    o.append(f'<text x="{X1 - 20}" y="{base + 40}" font-size="11.5" fill="var(--ink2)">Dashed: “75 carloads a day”, only in recent accounts.</text>')
    o.append("</svg>")
    return "\n".join(o)


def farms():
    W, H = 900, 400
    title = "One crop, many hands"
    desc = ("Bulletin 175: on 120 farms around Williston in 1923, receipts averaged $3,087 per farm, of which cucumbers $2,230 (72.3 percent), livestock $291, peanuts $102, other crops and sources the rest. "
            "Labour cost $579 per farm, a third of all expenses: day labour $225 (on 80.8 percent of farms), cropper labour $117 (26.8 percent), family labour $133 (71.7 percent), contract labour $104 (45.0 percent, mostly picking cucumbers).")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="sf-t sf-d" font-family="var(--serif)">',
         f'<title id="sf-t">{escape(title)}</title><desc id="sf-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         f'<text x="16" y="48" font-size="13" fill="var(--ink2)">120 farms around Williston, 1923, per farm on average (Florida Experiment Station Bulletin 175, 1925).</text>']
    # receipts bar
    LX, BW = 16, 860
    tot = 3087
    parts = [("Cucumbers", 2230, "var(--crop)"), ("Livestock", 291, "var(--town)"), ("Other crops", 177, "var(--ink2)"), ("Peanuts", 102, "var(--gold)"),
             ("Other sources", 96, "var(--line)"), ("Cane, melons, cotton, potatoes", 191, "var(--rock)")]
    o.append(f'<a href="{T}farms/14"><text x="{LX}" y="84" font-size="14" font-weight="bold" fill="var(--ink)" text-decoration="underline">Where the money came from: $3,087</text></a>')
    x = LX
    for name, v, col in parts:
        w = v / tot * BW
        o.append(f'<rect x="{x:.1f}" y="96" width="{w:.1f}" height="34" fill="{col}"/>')
        if w > 300:
            o.append(f'<text x="{x + 8:.0f}" y="118" font-size="12.5" fill="#fff">{escape(name)} ${v:,} ({v / tot * 100:.1f}%)</text>')
        x += w
    o.append(f'<text x="{LX}" y="148" font-size="11.5" fill="var(--ink2)">Right of cucumbers: livestock $291, other crops $177, peanuts $102 (most peanuts went to market as hogs), other sources $96, cane, melons, cotton and potatoes $191.</text>')
    # labour
    o.append(f'<a href="{T}farms/15"><text x="{LX}" y="190" font-size="14" font-weight="bold" fill="var(--ink)" text-decoration="underline">What the work cost: $579 of $1,712 in expenses</text></a>')
    lab = [("Day labor", 225, 80.8), ("Family labor", 133, 71.7), ("Cropper labor", 117, 26.8), ("Contract labor (mostly picking cucumbers)", 104, 45.0)]
    y = 206
    for name, v, share in lab:
        o.append(f'<text x="{LX}" y="{y + 16}" font-size="13" fill="var(--ink)">{escape(name)}</text>'
                 f'<rect x="300" y="{y}" width="{v * 1.3:.0f}" height="22" fill="var(--colour)" opacity=".85"/>'
                 f'<text x="{300 + v * 1.3 + 6:.0f}" y="{y + 16}" font-size="12.5" fill="var(--ink)">${v} per farm</text>'
                 f'<rect x="740" y="{y + 4}" width="{share * 1.2:.0f}" height="14" fill="var(--ink2)" opacity=".5"/>'
                 f'<text x="{740 + share * 1.2 + 4:.0f}" y="{y + 16}" font-size="11.5" fill="var(--ink2)">{share}%</text>')
        y += 34
    o.append(f'<text x="740" y="200" font-size="11.5" fill="var(--ink2)">share of farms paying it</text>')
    o.append(f'<text x="{LX}" y="{y + 18}" font-size="12" fill="var(--ink2)">The survey counts the work as costs. Who the day labourers, pickers and sharecroppers were, and what they earned a day, it does not say.</text>')
    o.append("</svg>")
    return "\n".join(o)


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "shipping-numbers.svg").write_text(numbers(), encoding="utf-8")
(OUT / "shipping-farms.svg").write_text(farms(), encoding="utf-8")
print("ok")
