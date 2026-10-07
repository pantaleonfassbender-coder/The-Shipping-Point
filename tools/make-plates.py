"""Lädt und skaliert die Tafeln nach assets/plates/<id>.jpg (1400 px) und <id>_t.jpg (Vorschau).

    python tools/make-plates.py              # alle Tafeln
    python tools/make-plates.py sanborn1923_1

Quellen: "ia" = Seitenbild des Internet Archive mit Ausschnitt in Promille (x0, y0, x1, y1);
"commons" = Datei auf Wikimedia Commons (2400 px; "commonsfull" in voller Größe); "ufdc" = Seitenbild (JPEG 2000) der University of Florida Digital Collections; "local" = Datei im Ordner ../quellen (etwa von Florida Memory,
dessen Seiten keine automatischen Abrufe zulassen und die deshalb von Hand geladen werden).
"""
import io
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "assets" / "plates"
UA = {"User-Agent": "ShippingPointResearch/1.0 (pantaleonfassbender@gmail.com)"}
SAL = "https://archive.org/download/seaboardairliner1914seab/page/n84.jpg"   # S. 71
IAP = "https://archive.org/download/{}/page/n{}.jpg"
RRC = "FirstAnnualReportOfTheRailroadCommissionOfTheStateOfFlorida"
COA = "ReportOfTheCommissionerOfAgricultureOfTheStateOfFloridaForPeriod"

PLATES = {
    "sal1914_cucumbers": ("ia", SAL, (478, 75, 925, 553)),
    "sal1914_trainload": ("ia", SAL, (38, 770, 913, 928)),
    "sanborn1923_1": ("commons", "File:Sanborn Fire Insurance Map from Williston, Levy County, Florida, 1923, Plate 0001.jpg", None),
    "sanborn1923_2": ("commons", "File:Sanborn Fire Insurance Map from Williston, Levy County, Florida, 1923, Plate 0002.jpg", None),
    "fm_ge0629": ("local", "../quellen/florida-memory/GE0629.jpg", None),
    # Modul 2: Two railroads
    "map1891_levy": ("commonsfull", 'File:"Standard guide" map of the state of Florida. LOC 2003627029.jpg', (267, 203, 555, 322)),
    "poor1901_plant": ("commons", "File:1901 Poor's Plant System.jpg", (427, 372, 736, 551)),
    "gaz1886_williston": ("ia", IAP.format("floridastategaze1886sout", 471), (20, 115, 515, 945)),
    "mr1893_arrangement": ("ia", IAP.format("sim_site-selection_1893-06-30_23_22", 5), (288, 527, 500, 846)),
    "gaz1895_williston": ("ia", IAP.format("floridarailroadg1895beld", 278), (15, 220, 503, 610)),
    "rrc1898_plant": ("ia", IAP.format(RRC, 80), (100, 120, 870, 870)),
    "rrc1898_fcp": ("ia", IAP.format(RRC, 88), (120, 120, 880, 670)),
    "laws1905_williston": ("ia", IAP.format("actsandresoluti03florgoog", 437), (240, 100, 945, 770)),
    "gaz1907_williston": ("ia", IAP.format("floridagazetteer1907rlpo", 419), (20, 350, 985, 890)),
    # Modul 3: Hard rock (fünfte Zahl: Drehung in Grad vor dem Ausschnitt)
    "usgs604_map": ("ia", IAP.format("IA41522103_0102", 16), (15, 10, 990, 995)),
    "usgs604_mine": ("ia", IAP.format("IA41522103_0102", 12), (64, 46, 936, 951, -90)),
    "usgs604_dredge": ("ia", IAP.format("IA41522103_0102", 116), (68, 64, 936, 965, -90)),
    "coa1894_table17": ("ia", IAP.format(COA + "_33", 88), (60, 60, 940, 600)),
    "coa1897_bailey": ("ia", IAP.format(COA + "_604", 76), (60, 40, 960, 610)),
    "coa1900_camps": ("ia", IAP.format(COA + "_614", 44), (30, 90, 960, 950)),
    "fgs1915_table": ("ia", IAP.format("annualreportflor71915flor", 25), (30, 672, 1000, 995)),
    "fgs1918_table": ("ia", IAP.format("annualreportf10111918flor", 127), (40, 410, 980, 860)),
    # Modul 4: The shipping point ("ufdc" = BIBID/VID/Datei auf dem Bildserver der University of Florida)
    "oes1897_cukes": ("ufdc", "UF00075908/09569/0358.jp2", (514, 626, 667, 717)),
    "oes1907_bank": ("ufdc", "UF00075908/00592/0043.jp2", (231, 326, 362, 443)),
    "fir1910_cukes": ("ufdc", "UF00076685/00034/00014.jp2", (376, 270, 630, 425)),
    "oes1916_shipping": ("ufdc", "UF00075908/06487/0098.jp2", (564, 63, 712, 275)),
    "let1919_review": ("ufdc", "AA00048605/02171/0290.jp2", (345, 55, 512, 460)),
    "b175_cover": ("ufdc", "UF00026891/00001/00001.jp2", None),
    # Modul 1: Before the rails
    "usgs1895_williston": ("local", "../quellen/before/topo/williston1895.png", None),
    "census1860_levy": ("ia", "https://archive.org/download/populationschedu110unit/page/n484.jpg", (60, 50, 960, 960)),
    "frr1855_cover": ("ia", "https://archive.org/download/report-to-the-directors-and-stockholders/page/n0.jpg", None),
    # Modul 5: The colour line
    "oes1904_levyville": ("ufdc", "UF00075908/01686/00228.jp2", (557, 126, 686, 440)),
    "naacp1919_florida": ("ia", "https://archive.org/download/thirtyyearsoflyn00nati/page/n58.jpg", (60, 90, 905, 625)),
    "pdn1923_jan5": ("ufdc", "AA00023799/00485/00001.jp2", (398, 150, 524, 860)),
    "pdn1923_jan7": ("ufdc", "AA00023799/00486/00001.jp2", (776, 225, 914, 900)),
    "pdn1923_jan8": ("ufdc", "AA00023799/00487/00001.jp2", (520, 222, 648, 830)),
    "mdm1923_probe": ("ufdc", "AA00020298/01590/00001.jp2", (26, 680, 150, 942)),
    "fpnt1923_noindictment": ("ufdc", "AA00081508/00274/00006.jp2", (486, 765, 602, 928)),
    "crisis1923_india": ("ia", "https://archive.org/download/sim_crisis_1923-06_26_2/page/n35.jpg", (540, 280, 985, 845)),
    "sal1914_labor": ("ia", "https://archive.org/download/seaboardairliner1914seab/page/n83.jpg", (30, 70, 970, 960)),
}


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
        return r.read()


def commons(title, full=False):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url", "iiurlwidth": 2400, "format": "json"})
    ii = next(iter(json.loads(fetch(u))["query"]["pages"].values()))["imageinfo"][0]
    return Image.open(io.BytesIO(fetch(ii["url"] if full else (ii.get("thumburl") or ii["url"]))))


def save(pid, im):
    im = im.convert("RGB")
    if im.width > 1400:
        im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
    DEST.mkdir(parents=True, exist_ok=True)
    im.save(DEST / f"{pid}.jpg", quality=86)
    t = im.copy()
    t.thumbnail((420, 420))
    t.save(DEST / f"{pid}_t.jpg", quality=82)
    print(pid, im.size)


def main(ids):
    for pid in ids or PLATES:
        kind, src, arg = PLATES[pid]
        if kind == "local":
            path = ROOT / src
            if not path.exists():
                print(pid, "fehlt noch:", path)
                continue
            im = Image.open(path)
        elif kind == "ufdc":
            b, v, f = src.split("/")
            im = Image.open(io.BytesIO(fetch("https://ufdcimages.uflib.ufl.edu/" + "/".join(b[i:i + 2] for i in range(0, 10, 2)) + f"/{v}/{f}")))
        elif kind in ("commons", "commonsfull"):
            im = commons(src, kind == "commonsfull")
        else:
            im = Image.open(io.BytesIO(fetch(src)))
        if arg:
            if len(arg) == 5:
                im = im.rotate(arg[4], expand=True)
            w, h = im.size
            x0, y0, x1, y1 = arg[:4]
            im = im.crop((w * x0 // 1000, h * y0 // 1000, w * x1 // 1000, h * y1 // 1000))
        save(pid, im)


if __name__ == "__main__":
    main(sys.argv[1:])
