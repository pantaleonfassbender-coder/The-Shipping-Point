"""Draws assets/viz/rails-line.svg and rails-rates.svg for module 2 (Two railroads).

rails-line: Williston's railroads 1886–1907 as two bands, each step linked to its passage; dashed where the
  sources only announce or arrange, solid from the first entry that places the town on the line.
rails-rates: the commission's rates of 1898 from the stations of the Archer spur on both roads (pp. 86, 94),
  and the onward charge to the northern markets, which the state did not set (pp. 12–13).
Run from the site root: python tools/viz-rails.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
T = "#/text/rails/"


def a(href, inner):
    return f'<a href="{href}">{inner}</a>'


def line():
    W, H = 900, 370
    x0, x1, y0, y1 = 60, 860, 1885, 1908
    X = lambda y: x0 + (y - y0) * (x1 - x0) / (y1 - y0)
    title = "Eleven miles to Archer, then two roads"
    desc = ("Timeline 1886 to 1907. In 1886 Williston has no railroad; Archer, eleven miles off, is its shipping point. In 1891 about 350 men work on the line from Archer to Dunnellon, "
            "to be operated by the Florida Central & Peninsular. In 1893 the Plant System agrees with its rival on the common use of the spur south of Archer. In 1895 a gazetteer places Williston on both roads; "
            "the town is incorporated in 1897; in 1898 the Railroad Commission lists two Williston stations with the same rates. In 1905 the legislature declares the incorporation lawful. "
            "In 1907 the lines appear as the Seaboard Air Line and the Atlantic Coast Line.")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="rl-t rl-d" font-family="var(--serif)">',
         f'<title id="rl-t">{escape(title)}</title><desc id="rl-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         f'<text x="16" y="48" font-size="13" fill="var(--ink2)">Dashed: announced or arranged, not yet attested for Williston. Each label links to its passage.</text>']
    # axis
    o.append(f'<line x1="{x0}" y1="260" x2="{x1}" y2="260" stroke="var(--ink2)"/>')
    for y in range(1886, 1908, 2):
        o.append(f'<line x1="{X(y):.0f}" y1="256" x2="{X(y):.0f}" y2="264" stroke="var(--ink2)"/>'
                 f'<text x="{X(y):.0f}" y="279" font-size="11.5" text-anchor="middle" fill="var(--ink2)">{y}</text>')
    # bands
    bands = [
        (100, "Florida Central & Peninsular", "Seaboard Air Line", [(1891.55, 1895, True), (1895, 1907, False)]),
        (150, "Plant System (Savannah, Florida & Western)", "Atlantic Coast Line", [(1893.5, 1895, True), (1895, 1907, False)]),
    ]
    for yb, name, later, segs in bands:
        o.append(f'<text x="{X(1886):.0f}" y="{yb - 12}" font-size="12.5" fill="var(--rail)" font-weight="bold">{escape(name)}</text>')
        for s0, s1, dashed in segs:
            dash = 'stroke-dasharray="6 5" opacity=".65"' if dashed else ""
            o.append(f'<line x1="{X(s0):.0f}" y1="{yb}" x2="{X(s1):.0f}" y2="{yb}" stroke="var(--rail)" stroke-width="7" {dash}/>')
        o.append(f'<line x1="{X(1907):.0f}" y1="{yb}" x2="{X(1907.9):.0f}" y2="{yb}" stroke="var(--crop)" stroke-width="7"/>')
        o.append(a(T + "town/13", f'<text x="{X(1907.9):.0f}" y="{yb - 12}" font-size="12" text-anchor="end" fill="var(--crop)" text-decoration="underline">{escape(later)}</text>'))
    # wagon road 1886
    o.append(f'<line x1="{X(1886):.0f}" y1="200" x2="{X(1891.5):.0f}" y2="200" stroke="var(--town)" stroke-width="3" stroke-dasharray="2 4"/>')
    o.append(a(T + "archer/2", f'<text x="{X(1886):.0f}" y="220" font-size="12.5" fill="var(--town)" text-decoration="underline">by wagon to Archer, 11 miles: “the shipping point”</text>'))
    # events
    A, B, C, Dd = 300, 318, 336, 354
    ev = [(1886, "1886 · no railroad", "archer/2", A), (1891.5, "1891 · ~350 men, Archer–Dunnellon", "lines/3", B),
          (1893.5, "1893 · rivals share the spur", "lines/4", A), (1895, "1895 · on both roads", "rates/5", C),
          (1897.4, "1897 · town incorporated", "town/11", B), (1898, "1898 · two stations, one rate", "rates/8", Dd),
          (1905.4, "1905 · made lawful after the fact", "town/12", C), (1907, "1907 · S. A. L. and A. C. L.", "town/13", B)]
    for y, lab, href, ty in ev:
        o.append(f'<line x1="{X(y):.0f}" y1="260" x2="{X(y):.0f}" y2="{ty - 12}" stroke="var(--line)"/>'
                 f'<circle cx="{X(y):.0f}" cy="260" r="4" fill="var(--rail)"/>')
        anchor = "end" if y > 1904 else "start"
        o.append(a(T + href, f'<text x="{X(y) + (-4 if anchor == "end" else 4):.0f}" y="{ty}" font-size="12" text-anchor="{anchor}" fill="var(--ink)" text-decoration="underline">{escape(lab)}</text>'))
    o.append("</svg>")
    return "\n".join(o)


def rates():
    W, H = 900, 430
    title = "Ten cents a crate, on either road"
    rows = [("Archer", 10, 15, 10, 15), ("Montbrook", 10, 16, 10, 16), ("Williston", 10, 16, 10, 16),
            ("Morriston", 11, 16, 11, 16), ("Juliette", 11, 16, None, None), ("Early Bird", None, None, 11, 16)]
    desc = ("Rates of the Railroad Commission of Florida, 1898, in cents, vegetables per crate and oranges per box. Plant System to High Springs: Archer 10 and 15, Montbrook 10 and 16, "
            "Williston 10 and 16, Morriston 11 and 16, Juliette 11 and 16. Florida Central & Peninsular to Jacksonville and the other junctions: Archer 10 and 15, Montbrook 10 and 16, "
            "Williston 10 and 16, Morriston 11 and 16, Early Bird 11 and 16. The charge onward to the northern markets was an interstate rate the commission could not set.")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="rr-t rr-d" font-family="var(--serif)">',
         f'<title id="rr-t">{escape(title)}</title><desc id="rr-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         f'<text x="16" y="48" font-size="13" fill="var(--ink2)">Rates set by the Railroad Commission of Florida, 1898, in cents: bar = vegetables per crate, figure in brackets = oranges per box.</text>']
    LX, BX, SC = 20, 150, 22
    cols = [("Plant System, to High Springs", T + "rates/7", 1), ("Florida Central & Peninsular, to Jacksonville", T + "rates/8", 3)]
    o.append(a(cols[0][1], f'<text x="{BX}" y="84" font-size="13" font-weight="bold" fill="var(--rail)" text-decoration="underline">{escape(cols[0][0])}</text>'))
    o.append(a(cols[1][1], f'<text x="{BX + 330}" y="84" font-size="13" font-weight="bold" fill="var(--rail)" text-decoration="underline">{escape(cols[1][0])}</text>'))
    y = 104
    for name, pv, po, fv, fo in rows:
        hl = name == "Williston"
        if hl:
            o.append(f'<rect x="{LX - 6}" y="{y - 4}" width="{W - 2 * LX + 12}" height="30" rx="5" fill="var(--crop)" opacity=".12"/>')
        bold = 'font-weight="bold"' if hl else ""
        o.append(f'<text x="{LX}" y="{y + 16}" font-size="13.5" fill="var(--ink)" {bold}>{escape(name)}</text>')
        for k, (v, orr) in enumerate(((pv, po), (fv, fo))):
            bx = BX + k * 330
            if v is None:
                o.append(f'<text x="{bx}" y="{y + 16}" font-size="12" fill="var(--ink2)">not on this road</text>')
                continue
            o.append(f'<rect x="{bx}" y="{y}" width="{v * SC}" height="22" fill="var(--rail)" opacity="{1 if hl else .7}"/>'
                     f'<text x="{bx + v * SC + 6}" y="{y + 16}" font-size="13" fill="var(--ink)">{v}¢ <tspan fill="var(--ink2)">({orr}¢)</tspan></text>')
        y += 34
    # onward
    y += 14
    o.append(f'<text x="{LX}" y="{y + 16}" font-size="13.5" fill="var(--ink)">Onward</text>')
    o.append(f'<rect x="{BX}" y="{y}" width="{W - BX - 30}" height="22" fill="none" stroke="var(--colour)" stroke-dasharray="6 4"/>')
    o.append(a(T + "rates/10", f'<text x="{BX + 10}" y="{y + 16}" font-size="13" fill="var(--colour)" text-decoration="underline">'
               "to New York and the other markets: an interstate rate, “beyond the limits of the State”, not set by the commission</text>"))
    y += 52
    o.append(f'<text x="{LX}" y="{y}" font-size="12" fill="var(--ink2)">Same rate from both Williston stations: the commission charged by the mile (unit 9).</text>')
    o.append(f'<text x="{LX}" y="{y + 17}" font-size="12" fill="var(--ink2)">What a shipper could weigh between the roads was service, cars and connections, which the tables do not show.</text>')
    o.append("</svg>")
    return "\n".join(o)


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "rails-line.svg").write_text(line(), encoding="utf-8")
(OUT / "rails-rates.svg").write_text(rates(), encoding="utf-8")
print("ok")
