"""Draws assets/viz/rock-export.svg and rock-leased.svg for module 3 (Hard rock).

rock-export: Florida hard rock phosphate 1909–1920, exported and domestic shipments (FGS 7th AR p. 22 for 1909–1912,
  10th/11th AR p. 106 for 1913–1917) and the quantities marketed in 1919 and 1920 (14th AR p. 29), which the
  report does not divide; no figure for 1918 in the reports examined.
rock-leased: the state's convicts by colour on 31 December 1894 (p. 81) and 1 December 1900 (p. 48), and the
  share working in phosphate in November 1899 (p. 48).
Run from the site root: python tools/viz-rock.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
T = "#/text/rock/"

# year: (exported, domestic, unit) or (marketed, None, unit)
DATA = [(1909, 496645, 17456, "war/16"), (1910, 461353, 18745, "war/16"), (1911, 462072, 16723, "war/16"),
        (1912, 470354, 15425, "war/16"), (1913, 476898, 12896, "war/17"), (1914, 303172, 6517, "war/17"),
        (1915, 43314, 6816, "war/17"), (1916, 28045, 19042, "war/17"), (1917, 12403, 6205, "war/17"),
        (1918, None, None, None), (1919, 285467, None, "war/18"), (1920, 400249, None, "war/18")]


def fmt(v):
    return f"{v:,}"


def export():
    W, H = 900, 440
    x0, base, top = 70, 360, 90
    sc = (base - top) / 550000
    bw, gap = 46, 18
    title = "Almost all of it went abroad"
    desc = ("Florida hard rock phosphate in long tons. Exported and domestic shipments: 1909 496,645 and 17,456; 1910 461,353 and 18,745; 1911 462,072 and 16,723; 1912 470,354 and 15,425; "
            "1913 476,898 and 12,896; 1914 303,172 and 6,517; 1915 43,314 and 6,816; 1916 28,045 and 19,042; 1917 12,403 and 6,205 (1917 including soft rock). "
            "No figure for 1918 in the reports examined. Marketed, not divided between export and home: 1919 285,467; 1920 400,249.")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="re-t re-d" font-family="var(--serif)">',
         f'<title id="re-t">{escape(title)}</title><desc id="re-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         f'<text x="16" y="48" font-size="13" fill="var(--ink2)">Florida hard rock phosphate, long tons, after the Florida Geological Survey. Each bar links to its passage.</text>']
    # legend
    o.append(f'<rect x="16" y="60" width="14" height="12" fill="var(--rock)"/><text x="36" y="71" font-size="12.5" fill="var(--ink)">exported</text>'
             f'<rect x="110" y="60" width="14" height="12" fill="var(--crop)"/><text x="130" y="71" font-size="12.5" fill="var(--ink)">shipped for use at home</text>'
             f'<rect x="300" y="60" width="14" height="12" fill="none" stroke="var(--rock)" stroke-dasharray="3 2"/><text x="320" y="71" font-size="12.5" fill="var(--ink)">marketed, not divided (1919–1920)</text>')
    for v in (0, 100000, 200000, 300000, 400000, 500000):
        y = base - v * sc
        o.append(f'<line x1="{x0}" y1="{y:.0f}" x2="{W - 20}" y2="{y:.0f}" stroke="var(--line)"/>'
                 f'<text x="{x0 - 6}" y="{y + 4:.0f}" font-size="11" text-anchor="end" fill="var(--ink2)">{fmt(v)}</text>')
    x = x0 + 14
    for yr, a, b, href in DATA:
        cx = x + bw / 2
        if a is None:
            o.append(f'<text x="{cx:.0f}" y="{base - 24}" font-size="11" text-anchor="middle" fill="var(--ink2)">no</text>'
                     f'<text x="{cx:.0f}" y="{base - 10}" font-size="11" text-anchor="middle" fill="var(--ink2)">figure</text>')
        elif b is None:
            h = a * sc
            o.append(f'<a href="{T}{href}"><rect x="{x}" y="{base - h:.0f}" width="{bw}" height="{h:.0f}" fill="none" stroke="var(--rock)" stroke-width="1.5" stroke-dasharray="4 3"/>'
                     f'<text x="{cx:.0f}" y="{base - h - 6:.0f}" font-size="11" text-anchor="middle" fill="var(--ink)">{fmt(a)}</text></a>')
        else:
            ha, hb = a * sc, b * sc
            o.append(f'<a href="{T}{href}"><rect x="{x}" y="{base - ha:.0f}" width="{bw}" height="{ha:.0f}" fill="var(--rock)"/>'
                     f'<rect x="{x}" y="{base - ha - hb:.0f}" width="{bw}" height="{max(hb, 1):.0f}" fill="var(--crop)"/>'
                     f'<text x="{cx:.0f}" y="{base - ha - hb - 6:.0f}" font-size="11" text-anchor="middle" fill="var(--ink)">{fmt(a + b)}</text></a>')
        o.append(f'<text x="{cx:.0f}" y="{base + 18}" font-size="12" text-anchor="middle" fill="var(--ink)">{yr}</text>')
        x += bw + gap
    # war marker
    xw = x0 + 14 + 5 * (bw + gap) + bw * 0.6
    o.append(f'<line x1="{xw:.0f}" y1="{top - 6}" x2="{xw:.0f}" y2="{base}" stroke="var(--colour)" stroke-dasharray="5 4"/>'
             f'<a href="{T}war/15"><text x="{xw + 6:.0f}" y="{top + 4}" font-size="12.5" fill="var(--colour)" text-decoration="underline">August 1914: “the interruption of European shipment”</text></a>')
    o.append(f'<text x="16" y="{base + 46}" font-size="12" fill="var(--ink2)">1909–1913: 96 to 97 of every 100 tons shipped went abroad. 1917 includes some soft rock. 1919 and 1920: quantities marketed, not divided.</text>')
    o.append(f'<text x="16" y="{base + 64}" font-size="12" fill="var(--ink2)">Sources: Seventh Annual Report (1915), p. 22; Tenth and Eleventh Annual Reports (1918), p. 106; Fourteenth Annual Report (1922), p. 29.</text>')
    o.append("</svg>")
    return "\n".join(o)


def leased():
    W, H = 900, 280
    title = "Who was leased"
    desc = ("The state's convicts on 31 December 1894: 614, of whom 512 Black men, 17 Black women, 83 white men and 2 white women. On 1 December 1900: 778, of whom 651 Black men, "
            "23 Black women, 102 white men and 2 white women. In November 1899, 507 of 697 convicts worked in seven phosphate camps, 190 in five turpentine camps.")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="rl3-t rl3-d" font-family="var(--serif)">',
         f'<title id="rl3-t">{escape(title)}</title><desc id="rl3-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         f'<text x="16" y="48" font-size="13" fill="var(--ink2)">Florida’s state convicts in the reports of the Commissioner of Agriculture; one square = five prisoners. “Colored” is the word of the tables.</text>']
    rows = [("31 Dec. 1894", "leased/4", [(512, "Black men", "var(--colour)"), (17, "Black women", "var(--colour)"), (83, "white men", "var(--ink2)"), (2, "white women", "var(--ink2)")], 614),
            ("Nov. 1899", "leased/9", [(507, "in phosphate camps", "var(--rock)"), (190, "in turpentine camps", "var(--town)")], 697),
            ("1 Dec. 1900", "leased/9", [(651, "Black men", "var(--colour)"), (23, "Black women", "var(--colour)"), (102, "white men", "var(--ink2)"), (2, "white women", "var(--ink2)")], 778)]
    y, LX, BX, S = 84, 16, 130, 7
    per_row = 100
    for label, href, parts, total in rows:
        o.append(f'<a href="{T}{href}"><text x="{LX}" y="{y + 12}" font-size="13" fill="var(--ink)" text-decoration="underline">{escape(label)}</text></a>')
        o.append(f'<text x="{LX}" y="{y + 28}" font-size="11.5" fill="var(--ink2)">{total} in all</text>')
        k = 0
        for n, _, col in parts:
            sq = round(n / 5)
            for _ in range(sq):
                cx, cy = BX + (k % per_row) * S, y + (k // per_row) * S
                o.append(f'<rect x="{cx}" y="{cy}" width="{S - 1.5}" height="{S - 1.5}" fill="{col}"/>')
                k += 1
        lx = BX
        ly = y + ((k - 1) // per_row + 1) * S + 14
        o.append(f'<text x="{lx}" y="{ly}" font-size="11.5" fill="var(--ink)">' + " · ".join(f"{n} {escape(t)}" for n, t, _ in parts) + "</text>")
        y = ly + 22
    o.append(f'<text x="16" y="{H - 14}" font-size="12" fill="var(--ink2)">Sources: Report of the Commissioner of Agriculture 1893–1894, p. 81; 1899–1900, p. 48.</text>')
    o.append("</svg>")
    return "\n".join(o)


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "rock-export.svg").write_text(export(), encoding="utf-8")
(OUT / "rock-leased.svg").write_text(leased(), encoding="utf-8")
print("ok")
