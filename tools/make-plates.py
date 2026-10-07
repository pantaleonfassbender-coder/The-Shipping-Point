"""Lädt und skaliert die Tafeln nach assets/plates/<id>.jpg (1400 px) und <id>_t.jpg (Vorschau).

    python tools/make-plates.py              # alle Tafeln
    python tools/make-plates.py sanborn1923_1

Quellen: "ia" = Seitenbild des Internet Archive mit Ausschnitt in Promille (x0, y0, x1, y1);
"commons" = Datei auf Wikimedia Commons; "local" = Datei im Ordner ../quellen (etwa von Florida Memory,
dessen Seiten keine automatischen Abrufe zulassen und die deshalb von Hand geladen werden).
"""
import io
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "assets" / "plates"
UA = {"User-Agent": "ShippingPointResearch/1.0 (pantaleonfassbender@gmail.com)"}
SAL = "https://archive.org/download/seaboardairliner1914seab/page/n84.jpg"   # S. 71

PLATES = {
    "sal1914_cucumbers": ("ia", SAL, (478, 75, 925, 553)),
    "sal1914_trainload": ("ia", SAL, (38, 770, 913, 928)),
    "sanborn1923_1": ("commons", "File:Sanborn Fire Insurance Map from Williston, Levy County, Florida, 1923, Plate 0001.jpg", None),
    "sanborn1923_2": ("commons", "File:Sanborn Fire Insurance Map from Williston, Levy County, Florida, 1923, Plate 0002.jpg", None),
    "fm_ge0629": ("local", "../quellen/florida-memory/GE0629.jpg", None),
}


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
        return r.read()


def commons(title):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url", "iiurlwidth": 2400, "format": "json"})
    ii = next(iter(json.loads(fetch(u))["query"]["pages"].values()))["imageinfo"][0]
    return Image.open(io.BytesIO(fetch(ii.get("thumburl") or ii["url"])))


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
        elif kind == "commons":
            im = commons(src)
        else:
            im = Image.open(io.BytesIO(fetch(src)))
        if arg:
            w, h = im.size
            x0, y0, x1, y1 = arg
            im = im.crop((w * x0 // 1000, h * y0 // 1000, w * x1 // 1000, h * y1 // 1000))
        save(pid, im)


if __name__ == "__main__":
    main(sys.argv[1:])
