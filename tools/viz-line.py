"""Draws assets/viz/line-rosewood.svg for module 5 (The colour line): the weeks after 1 January 1923 as the
reports of the time give them, day by day, with the count of the dead each report gave, and the grand juries that
returned no indictment. Each label links to its passage.
Run from the site root: python tools/viz-line.py
"""
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
T = "#/text/line/"


def build():
    W, H = 900, 470
    d0, d1 = date(1922, 12, 31), date(1923, 2, 20)
    x0, x1 = 50, 870
    X = lambda d: x0 + (d - d0).days * (x1 - x0) / (d1 - d0).days
    title = "Seven weeks in 1923, as the papers told them"
    desc = ("Monday 1 January: alleged attack on a white woman at Sumner. Thursday night 4 January: armed white men besiege a house at Rosewood; two white men are killed, "
            "and by the first report two Black women and a Black man are dead in the house. Friday 5 January: the village burned at daybreak; fleeing residents fired upon. "
            "Saturday 6 January: James Carrier shot at his family's graves; seven dead by the report of 8 January. Saturday or Sunday: twelve more houses burned. "
            "17 January: Abe Wilson lynched near Newberry. 12 to 15 February: special grand jury at Bronson, eight dead by its count, no indictment.")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="lr-t lr-d" font-family="var(--serif)">',
         f'<title id="lr-t">{escape(title)}</title><desc id="lr-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         f'<text x="16" y="48" font-size="13" fill="var(--ink2)">Above the line: what happened, by the reports. Below: how many dead each report counted. Each label links to its passage.</text>']
    base = 250
    o.append(f'<line x1="{x0}" y1="{base}" x2="{x1}" y2="{base}" stroke="var(--ink2)"/>')
    for d, lab in ((date(1923, 1, 1), "1 Jan"), (date(1923, 1, 8), "8 Jan"), (date(1923, 1, 15), "15 Jan"), (date(1923, 1, 22), "22 Jan"),
                   (date(1923, 1, 29), "29 Jan"), (date(1923, 2, 5), "5 Feb"), (date(1923, 2, 12), "12 Feb"), (date(1923, 2, 19), "19 Feb")):
        o.append(f'<line x1="{X(d):.0f}" y1="{base - 4}" x2="{X(d):.0f}" y2="{base + 4}" stroke="var(--ink2)"/>'
                 f'<text x="{X(d):.0f}" y="{base + 18}" font-size="11" text-anchor="middle" fill="var(--ink2)">{lab}</text>')
    # the week of fire
    o.append(f'<rect x="{X(date(1923, 1, 4)):.0f}" y="{base - 160}" width="{X(date(1923, 1, 8)) - X(date(1923, 1, 4)):.0f}" height="160" fill="var(--colour)" opacity=".10"/>')
    ev = [(date(1923, 1, 1), "1 Jan: alleged attack at Sumner", "rosewood/3", 76),
          (date(1923, 1, 4), "4 Jan, night: house besieged", "rosewood/3", 96),
          (date(1923, 1, 5), "5 Jan: village burned, people fired upon", "rosewood/3", 116),
          (date(1923, 1, 6), "6 Jan: James Carrier killed", "rosewood/4", 136),
          (date(1923, 1, 7), "6 or 7 Jan: twelve more houses burned", "rosewood/5", 156),
          (date(1923, 1, 17), "17 Jan: Abe Wilson lynched near Newberry", "after/7", 186),
          (date(1923, 2, 12), "12 Feb: special grand jury", "after/7", 206),
          (date(1923, 2, 15), "15 Feb: no indictment", "after/8", 226)]
    for d, lab, href, y in ev:
        xx = X(d)
        o.append(f'<line x1="{xx:.0f}" y1="{y + 4}" x2="{xx:.0f}" y2="{base}" stroke="var(--line)"/><circle cx="{xx:.0f}" cy="{base}" r="3.5" fill="var(--colour)"/>')
        anchor = "end" if d > date(1923, 2, 1) else "start"
        dx = -4 if anchor == "end" else 4
        o.append(f'<a href="{T}{href}"><text x="{xx + dx:.0f}" y="{y}" font-size="12" text-anchor="{anchor}" fill="var(--ink)" text-decoration="underline">{escape(lab)}</text></a>')
    # counts: one bar per report, evenly spaced
    sc = 12
    o.append(f'<text x="16" y="{base + 52}" font-size="13" font-weight="bold" fill="var(--ink)">Dead, by report</text>')
    counts = [("5 Jan: 5 “known”", 2, 3, "rosewood/3", True), ("8 Jan: 7", 2, 5, "rosewood/5", False),
              ("12 Feb: 8", 2, 6, "after/7", False), ("17 Feb: 8", 2, 6, "after/8", False)]
    for k, (lab, w, b, href, plus) in enumerate(counts):
        xx = 170 + k * 170
        yb = base + 40
        o.append(f'<rect x="{xx}" y="{yb}" width="26" height="{w * sc}" fill="var(--ink2)"/>'
                 f'<rect x="{xx}" y="{yb + w * sc}" width="26" height="{b * sc}" fill="var(--colour)"/>')
        if plus:
            o.append(f'<rect x="{xx}" y="{yb + (w + b) * sc}" width="26" height="{3 * sc}" fill="none" stroke="var(--colour)" stroke-dasharray="3 3"/>'
                     f'<text x="{xx + 32}" y="{yb + (w + b + 2) * sc}" font-size="11" fill="var(--colour)">“many” believed</text>')
        o.append(f'<a href="{T}{href}"><text x="{xx + 32}" y="{yb + 14}" font-size="12" fill="var(--ink)" text-decoration="underline">{escape(lab)}</text></a>')
    o.append(f'<rect x="16" y="{H - 30}" width="12" height="12" fill="var(--ink2)"/><text x="32" y="{H - 20}" font-size="12" fill="var(--ink)">white dead (named from the first day)</text>'
             f'<rect x="270" y="{H - 30}" width="12" height="12" fill="var(--colour)"/><text x="286" y="{H - 20}" font-size="12" fill="var(--ink)">Black dead (counted; named only in part)</text>'
             f'<text x="560" y="{H - 20}" font-size="12" fill="var(--ink2)">The official count stayed at eight; later accounts dispute it.</text>')
    o.append("</svg>")
    return "\n".join(o)


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "line-rosewood.svg").write_text(build(), encoding="utf-8")
print("ok")
