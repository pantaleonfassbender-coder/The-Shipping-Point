"""Draws assets/viz/airfield-line.svg and airfield-florida.svg for module 6 (The airfield).

airfield-line: the field from the start of work (August 1942) to the auction of its buildings (April 1947), as the
  Levy County Journal reported it; the gap in the record between 1944 and 1946 is marked.
airfield-florida: the Army fields and camps of item 2 of the campaign editorial of May 1944 (Bradford County
  Telegraph, 19 May 1944), with Montbrook marked.
Run from the site root: python tools/viz-airfield.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
T = "#/text/airfield/"


def line():
    W, H = 900, 300
    x0, x1 = 50, 860
    t0, t1 = 1942 + 6 / 12, 1947 + 5 / 12
    X = lambda t: x0 + (t - t0) * (x1 - x0) / (t1 - t0)
    title = "Five years of an airfield"
    desc = ("August 1942: work begins. September and October 1942: roads closed, land acquired, a house torn down. April 1943: the OTU site, land taken by negotiation or condemnation. "
            "May 1943: 99th Bomb Squadron. April 1944: a school squadron, mentioned as former. No report of the end of training found. July 1946: declared surplus. "
            "March and April 1947: bought by the town, 42 buildings auctioned.")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="al-t al-d" font-family="var(--serif)">',
         f'<title id="al-t">{escape(title)}</title><desc id="al-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         f'<text x="16" y="48" font-size="13" fill="var(--ink2)">The Montbrook Army Air Field in the Levy County Journal. Each label links to its passage.</text>']
    base = 210
    o.append(f'<line x1="{x0}" y1="{base}" x2="{x1}" y2="{base}" stroke="var(--ink2)"/>')
    for y in range(1943, 1948):
        o.append(f'<line x1="{X(y):.0f}" y1="{base - 4}" x2="{X(y):.0f}" y2="{base + 4}" stroke="var(--ink2)"/>'
                 f'<text x="{X(y):.0f}" y="{base + 20}" font-size="12" text-anchor="middle" fill="var(--ink2)">{y}</text>')
    o.append(f'<rect x="{X(1942 + 7 / 12):.0f}" y="{base - 12}" width="{X(1944 + 4 / 12) - X(1942 + 7 / 12):.0f}" height="12" fill="var(--air)" opacity=".7"/>')
    o.append(f'<rect x="{X(1944 + 4 / 12):.0f}" y="{base - 12}" width="{X(1946 + 6 / 12) - X(1944 + 4 / 12):.0f}" height="12" fill="none" stroke="var(--air)" stroke-dasharray="4 4"/>')
    o.append(f'<text x="{(X(1944 + 4 / 12) + X(1946 + 6 / 12)) / 2:.0f}" y="{base + 40}" font-size="11.5" text-anchor="middle" fill="var(--ink2)">no report of the end of training found</text>')
    ev = [(1942 + 7.5 / 12, "Aug. 1942: work begins", "build/1", 80), (1942 + 8.2 / 12, "Sept. 1942: roads closed", "build/2", 100),
          (1942 + 9.4 / 12, "Oct. 1942: a house torn down", "build/3", 120), (1943 + 3.2 / 12, "Apr. 1943: “OTU site”, condemnation", "build/4", 140),
          (1943 + 4.4 / 12, "May 1943: 99th Bomb Squadron", "field/5", 160), (1944 + 3.2 / 12, "Apr. 1944: “formerly” 1160th School Sq.", "field/6", 180),
          (1946 + 6.8 / 12, "July 1946: surplus", "after/8", 120), (1947 + 2.6 / 12, "Mar.–Apr. 1947: bought, 42 buildings sold", "after/9", 150)]
    for t, lab, href, y in ev:
        xx = X(t)
        anchor = "end" if t > 1945 else "start"
        dx = -4 if anchor == "end" else 4
        o.append(f'<line x1="{xx:.0f}" y1="{y + 4}" x2="{xx:.0f}" y2="{base - 12}" stroke="var(--line)"/><circle cx="{xx:.0f}" cy="{base - 6}" r="3.5" fill="var(--air)"/>'
                 f'<a href="{T}{href}"><text x="{xx + dx:.0f}" y="{y}" font-size="12" text-anchor="{anchor}" fill="var(--ink)" text-decoration="underline">{escape(lab)}</text></a>')
    o.append("</svg>")
    return "\n".join(o)


FIELDS = ["Camp Blanding", "Orlando Air Base", "Dale Mabry Field", "Tallahassee", "Avon Park bombing range", "Fort Barrancas", "Pensacola",
          "Sarasota AAF", "Boca Raton AAF", "Buckingham AAF", "Carlstrom Field", "Eglin Field", "Conners Field", "MacDill Field", "Dorr Field",
          "Drane Field", "Hendricks Field", "Homestead AAF", "Camp Gordon Johnston", "Key West Barracks", "Marathon Flight Strip", "Morrison Field",
          "Drew Field", "Camp Murphy", "Taylor Field", "Tyndall Field", "Venice AAF", "Brandon Field", "Fort Pierce", "Marianna AAF", "Miami Air Depot",
          "AAF Redistribution Center No. 2", "Miami Beach AAF Training Base", "Montbrook Air Field", "Brooksville Air Field", "Cross City Air Field"]


def florida():
    cols, cw, rh = 4, 214, 26
    rows = (len(FIELDS) + cols - 1) // cols
    W, H = 900, 90 + rows * rh + 40
    title = "One of many"
    desc = (f"The Army fields and camps in Florida listed in a campaign editorial of May 1944: {len(FIELDS)} names, among them Montbrook Air Field; "
            "total expenditure claimed $251,765,105. The Navy's stations are listed separately in the same editorial.")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="af-t af-d" font-family="var(--serif)">',
         f'<title id="af-t">{escape(title)}</title><desc id="af-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         f'<a href="{T}field/7"><text x="16" y="48" font-size="13" fill="var(--ink2)" text-decoration="underline">Army fields and camps in Florida as a campaign editorial listed them, May 1944 ({len(FIELDS)} names, some abbreviated)</text></a>']
    for i, name in enumerate(FIELDS):
        c, r = i // rows, i % rows
        x, y = 16 + c * cw, 70 + r * rh
        hl = name.startswith("Montbrook")
        fill = "var(--air)" if hl else "var(--line)"
        op = 1 if hl else 0.45
        tf = "#fff" if hl else "var(--ink)"
        fw = 'font-weight="bold"' if hl else ""
        o.append(f'<rect x="{x}" y="{y}" width="{cw - 10}" height="{rh - 5}" rx="4" fill="{fill}" opacity="{op}"/>'
                 f'<text x="{x + 6}" y="{y + 15}" font-size="12" fill="{tf}" {fw}>{escape(name)}</text>')
    o.append(f'<text x="16" y="{H - 14}" font-size="12" fill="var(--ink2)">AAF: Army Air Field. Total expenditure claimed: $251,765,105. The Navy’s stations are a separate list in the same editorial.</text>')
    o.append("</svg>")
    return "\n".join(o)


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "airfield-line.svg").write_text(line(), encoding="utf-8")
(OUT / "airfield-florida.svg").write_text(florida(), encoding="utf-8")
print("ok")
