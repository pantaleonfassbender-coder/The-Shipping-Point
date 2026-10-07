# The Shipping Point

Williston and its neighbours (Morriston, Montbrook, Bronson), Levy County, Florida, to 1945: a documentary apparatus in English, built from public-domain sources read against the page images — railroads, phosphate, the cucumber trade, the colour line (Rosewood included) and Montbrook Army Air Field. Cedar Key appears only as a point of reference.

**Status:** draft for review, **not yet published**. The site is not linked from elsewhere and asks search engines not to index it (`_headers`, `meta robots`). Comments come in through a Netlify form (`feedback.html`). Six modules are planned; modules 2, *Two railroads* (1886–1907), 3, *Hard rock* (1893–1920), and 4, *The shipping point* (1897–1925), are in place. The source survey is in the project folder (`QUELLENSICHTUNG.md`, not in this repository).

**Companion piece (in preparation):** *A Solid Trainload*.

## Structure

Static site without a build step: `index.html`, `app.js` (hash routes; engine adapted from *One Bridge, Two Newsreels*), `style.css`, `feedback.html` and `thanks.html` (Netlify Forms), `legal.html`, `_headers`. Data in `data/` (`modules.json`, `timeline.json`, `compare.json`, `plates.json`, one file per module, e.g. `rails.json`); each module is built by `python tools/build-<module>.py` and drawn by `python tools/viz-<module>.py`; plates built with `python tools/make-plates.py`.

Local: `python -m http.server` in the repository, then `http://localhost:8000/`. The comment form only works on Netlify. Netlify's form detection must be switched on for the site (Forms → Enable form detection); the form is named `feedback`.

## Licences

Code MIT; editorial texts CC BY 4.0; editions CC0 1.0. See [LICENSES.md](LICENSES.md).
