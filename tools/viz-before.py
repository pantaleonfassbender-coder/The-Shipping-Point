"""Draws assets/viz/before-census.svg for module 1 (Before the rails): the free and the enslaved population of
Levy and Marion counties in 1860 (Population of the United States in 1860, pp. 51, 53), and Levy County's total
population in 1880 and 1885 (Florida State Gazetteer 1886, p. 269).
Run from the site root: python tools/viz-before.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "viz"
T = "#/text/before/"


def build():
    W, H = 900, 330
    title = "Counted in 1860"
    desc = ("Census of 1860. Levy County: 1,331 white inhabitants and 450 enslaved, no free people of colour listed. Marion County: 3,294 white, 5,314 enslaved, 1 free person of colour. "
            "Levy County in all: 5,767 in 1880 and 6,678 in 1885, by the gazetteer of 1886.")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="bc-t bc-d" font-family="var(--serif)">',
         f'<title id="bc-t">{escape(title)}</title><desc id="bc-d">{escape(desc)}</desc>',
         f'<text x="16" y="28" font-size="17" font-weight="bold" fill="var(--ink)">{escape(title)}</text>',
         f'<text x="16" y="48" font-size="13" fill="var(--ink2)">The free and the enslaved in the two counties around Williston, by the federal census of 1860. Each label links to its passage.</text>']
    sc = 480 / 9000
    rows = [("Levy, 1860", 1331, 450), ("Marion, 1860", 3294, 5314)]
    y = 80
    for name, w, s in rows:
        o.append(f'<a href="{T}settle/2"><text x="16" y="{y + 20}" font-size="13.5" fill="var(--ink)" text-decoration="underline">{escape(name)}</text></a>')
        o.append(f'<rect x="150" y="{y}" width="{w * sc:.0f}" height="30" fill="var(--ink2)"/>'
                 f'<rect x="{150 + w * sc:.0f}" y="{y}" width="{s * sc:.0f}" height="30" fill="var(--colour)"/>')
        o.append(f'<text x="{156 + (w + s) * sc:.0f}" y="{y + 20}" font-size="12.5" fill="var(--ink)">{w:,} free (white) · {s:,} enslaved ({s / (w + s) * 100:.0f}%)</text>')
        y += 56
    y += 10
    o.append(f'<text x="16" y="{y + 20}" font-size="13.5" fill="var(--ink)">Levy, all</text>')
    for yr, v, href in ((1880, 5767, "county/7"), (1885, 6678, "county/7")):
        o.append(f'<rect x="150" y="{y}" width="{v * sc:.0f}" height="22" fill="var(--town)" opacity=".75"/>'
                 f'<a href="{T}{href}"><text x="{156 + v * sc:.0f}" y="{y + 16}" font-size="12.5" fill="var(--ink)" text-decoration="underline">{yr}: {v:,}</text></a>')
        y += 30
    o.append(f'<rect x="16" y="{H - 30}" width="12" height="12" fill="var(--ink2)"/><text x="32" y="{H - 20}" font-size="12" fill="var(--ink)">free (white)</text>'
             f'<rect x="140" y="{H - 30}" width="12" height="12" fill="var(--colour)"/><text x="156" y="{H - 20}" font-size="12" fill="var(--ink)">enslaved, counted without names</text>'
             f'<text x="420" y="{H - 20}" font-size="12" fill="var(--ink2)">Free people of colour: none listed in Levy, one in Marion.</text>')
    o.append("</svg>")
    return "\n".join(o)


OUT.mkdir(parents=True, exist_ok=True)
(OUT / "before-census.svg").write_text(build(), encoding="utf-8")
print("ok")
