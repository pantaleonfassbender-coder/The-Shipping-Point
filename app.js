/* The Shipping Point. Williston and its neighbours, Levy County, Florida, to 1945. A documentary apparatus
   in English, built on the engine of "One Bridge, Two Newsreels" (Remagen). Vanilla JS, hash routes.
   Draft for review: not yet published. */
"use strict";

const view = document.getElementById("view");
const D = { mods: null, plates: null, timeline: null, compare: null, texts: {} };

const S = {
  title: "The Shipping Point", loading: "Loading…", allTexts: "← All texts", allCmp: "← All comparisons",
  citeAs: "cited as", cite: "Cite as", srcNote: "Source and editorial note", source: "Source",
  planned: "planned", notTaken: "not included", shipped: "Printed here", plannedH: "Planned",
  missingH: "Examined and not included", textsTag: "Texts", textsH: "The corpus",
  textsLede: "Every module can be read in full, in the words of its public-domain sources, each passage read against the page image. What was examined and not included is listed below, with the reason.",
  cmpTag: "Compare", cmpH: "Voices side by side", tlTag: "Timeline", tlH: "From the settlement to the airfield",
  platesTag: "Plates", platesH: "Photographs, maps, views", fail: "The apparatus could not be loaded: "
};
const SIDES = {
  town: "Town", rail: "Rails", rock: "Phosphate and rock", crop: "Farms and shipping", colour: "The colour line", air: "The airfield"
};

const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const side = s => `<span class="side ${s}">${esc(SIDES[s] || s)}</span>`;
const plateOf = id => (D.plates.plates || []).find(p => p.id === id);
const getJSON = url => fetch(url).then(r => { if (!r.ok) throw new Error(url); return r.json(); });

async function boot() {
  [D.mods, D.plates, D.timeline, D.compare] = await Promise.all(
    ["data/modules.json", "data/plates.json", "data/timeline.json", "data/compare.json"].map(getJSON));
  document.getElementById("navCompare").hidden = !(D.compare.pairs || []).length;
  document.getElementById("navPlates").hidden = !(D.plates.plates || []).length;
  window.addEventListener("hashchange", route);
  route();
}

async function text(id) {
  if (!D.texts[id]) D.texts[id] = await getJSON(`data/${id}.json`);
  return D.texts[id];
}

function route() {
  const parts = (location.hash.replace(/^#\/?/, "") || "").split("/").filter(Boolean);
  const [page, ...args] = parts;
  document.querySelectorAll(".top nav a").forEach(a => {
    const t = a.getAttribute("href").replace(/^#\/?/, "");
    a.classList.toggle("on", (t || "") === (page === "text" ? "texts" : page || ""));
  });
  view.innerHTML = "";
  window.scrollTo(0, 0);
  const pages = { "": overview, texts, text: reader, compare, timeline, plates, sources };
  (pages[page || ""] || overview)(args);
}

/* ------------------------------------------------------------ overview */
const OVERVIEW = {
  tag: "Levy County, Florida · Williston · Morriston · Montbrook · Bronson · to 1945",
  h: "The Shipping Point",
  lede: "In 1886 a gazetteer named Archer, eleven miles away, as “the shipping point” for the settlement at Williston. Thirty years later a correspondent wrote of “the section for which Williston is the shipping point”, and of the cucumbers for which it had become famous. In between came two railroads, the phosphate pits around Morriston and Montbrook, the vegetable trains to the northern markets, and the labour that loaded them.",
  body: "This apparatus follows Williston and its neighbours through their own public-domain sources: newspapers, gazetteers, railroad and geological reports, soil surveys, the state's reports on leased convicts, and the record of violence in the county, Rosewood included. Where the people who did the work speak only through others, it says so. Cedar Key, with its own older history of port and fishery, appears only where the rails, the timber and the work lead there.",
  q: [
    ["How did a farm settlement become a shipping point?", "By two railroads in the 1890s, by phosphate after 1889, and by cucumbers: in 1904 a federal soil survey found that “the principal money crop in the vicinity of Williston is cucumbers.”"],
    ["Who did the work?", "The sources name leased state convicts, overwhelmingly Black, in the phosphate pits near Albion and the turpentine camps near Morriston in the 1890s. Free labourers in the pits and fields are, so far, hardly visible in them; the modules say where the voices are missing."],
    ["What does the county's history of violence include?", "The lynching of Wash Bradley at Bronson in 1904, recorded by the NAACP in 1919, and Rosewood in January 1923. They are documented from the sources of their time, not used as a story device."],
    ["Can one retrace it?", "A Solid Trainload, a companion piece in preparation, will let you take the place of a shipper at Williston between the 1880s and 1945. Every card will point to its passage here."]
  ],
  none: "The first modules are in preparation; the Texts page lists them with their sources.",
  have: "What the apparatus contains", qs: "The questions"
};

function overview() {
  const O = OVERVIEW;
  view.innerHTML = `
  <div class="hero one"><div>
    <span class="tag">${esc(O.tag)}</span>
    <h1>${esc(O.h)}</h1>
    <p class="lede">${esc(O.lede)}</p>
    <p class="readable">${esc(O.body)}</p>
  </div></div>
  <h2>${esc(O.have)}</h2>
  ${D.mods.shipped.length ? `<div class="grid g2">${D.mods.shipped.map(card).join("")}</div>`
    : `<p class="fine">${esc(O.none)}</p><div class="grid g2">${(D.mods.planned || []).map(m => card(m, true)).join("")}</div>`}
  <h2>${esc(O.qs)}</h2>
  <div class="grid g2">${O.q.map(([h, p]) => `<div class="panel"><h3>${esc(h)}</h3><p>${esc(p)}</p></div>`).join("")}</div>`;
}

function card(m, planned) {
  const inner = `<div>${side(m.side)} <span class="fine">${esc(planned ? S.planned : m.zk || "")}</span></div>
    <h3>${esc(m.kurz)}</h3><p class="fine">${esc(m.warum)}</p>`;
  return planned ? `<div class="card planned">${inner}</div>` : `<a class="card" href="#/text/${m.id}">${inner}</a>`;
}

/* ------------------------------------------------------------ texts */
function texts() {
  const other = (list, label) => list.map(m => `
      <div class="card planned"><div>${side(m.side)} <span class="fine">${esc(label)}</span></div>
      <h3>${esc(m.kurz)}</h3><p class="fine">${esc(m.warum)}</p><p class="fine"><b>${esc(S.source)}:</b> ${esc(m.quelle)}</p></div>`).join("");
  view.innerHTML = `
    <span class="tag">${esc(S.textsTag)}</span><h1>${esc(S.textsH)}</h1>
    <p class="lede">${esc(S.textsLede)}</p>
    ${D.mods.shipped.length ? `<h2>${esc(S.shipped)}</h2><div class="grid g2">${D.mods.shipped.map(m => card(m)).join("")}</div>` : ""}
    ${(D.mods.planned || []).length ? `<h2>${esc(S.plannedH)}</h2><div class="grid g2">${other(D.mods.planned, S.planned)}</div>` : ""}
    ${(D.mods.missing || []).length ? `<h2 id="missing">${esc(S.missingH)}</h2><div class="grid g2">${other(D.mods.missing, S.notTaken)}</div>` : ""}`;
}

async function reader([id, secId, unitN]) {
  const m = D.mods.shipped.find(x => x.id === id);
  if (!m) { location.hash = "#/texts"; return; }
  view.innerHTML = `<p class="fine">${esc(S.loading)}</p>`;
  const t = await text(m.datei);
  const sec = t.sections.find(s => s.id === secId) || t.sections[0];
  view.innerHTML = `
    <p class="fine"><a href="#/texts">${esc(S.allTexts)}</a></p>
    <span class="tag">${side(m.side)} ${esc(t.jahr)} · ${esc(S.citeAs)} ${esc(sec.zk)} [n]</span>
    <h1>${esc(t.titel)}</h1>
    <p class="fine">${esc(t.autor)}</p>
    <nav class="toc">${t.sections.map(s => `<a href="#/text/${id}/${s.id}" class="${s.id === sec.id ? "on" : ""}">${esc(s.titel)}</a>`).join("")}</nav>
    <div class="panel readable"><h3>${esc(sec.titel)}</h3><p>${esc(sec.blurb)}</p>${sec.note ? `<p class="fine">${esc(sec.note)}</p>` : ""}</div>
    ${(sec.plates || []).length ? `<div class="grid g4 secplates">${sec.plates.map(plateOf).filter(Boolean).map(plateFig).join("")}</div>` : ""}
    ${sec.viz ? `<div class="viz" id="viz"><p class="fine">${esc(S.loading)}</p></div>` : ""}
    <div id="units"></div>
    <div class="panel readable hinweis"><span class="tag">${esc(S.srcNote)}</span>
      <p><b>${esc(S.source)}.</b> ${esc(t.quelle)}</p><p>${esc(t.hinweis)}</p></div>`;
  bindPlates(view);
  if (sec.viz) fetch(`assets/viz/${sec.viz}.svg`).then(r => r.ok ? r.text() : "").then(svg => {
    const el = document.getElementById("viz");
    if (el) el.innerHTML = svg || "";
  });
  const box = view.querySelector("#units");
  for (const u of sec.units) {
    box.insertAdjacentHTML("beforeend", `
      <div class="unit ${String(u.n) === unitN ? "hl" : ""}" id="u${u.n}">
        <div class="num"><a href="#/text/${id}/${sec.id}/${u.n}" title="${esc(S.cite)} ${esc(sec.zk)} [${u.n}]">[${u.n}]</a>
          ${u.pg ? `<span class="pg">${esc(u.pg)}</span>` : ""}</div>
        <div>${u.titel ? `<h4>${esc(u.titel)}</h4>` : ""}<div class="cols one"><div class="text">${esc(u.orig)}</div></div></div>
        ${u.note ? `<div class="note">${esc(u.note)}</div>` : ""}
      </div>`);
  }
  if (unitN) { const el = document.getElementById("u" + unitN); if (el) el.scrollIntoView({ block: "center" }); }
}

/* ------------------------------------------------------------ compare */
async function compare([pid]) {
  const CMP = D.compare;
  const pair = (CMP.pairs || []).find(p => p.id === pid);
  if (!pair) {
    view.innerHTML = `
      <span class="tag">${esc(S.cmpTag)}</span><h1>${esc(S.cmpH)}</h1>
      <p class="lede">${esc(CMP.lede)}</p>
      <div class="grid g2">${(CMP.pairs || []).map(p => `<a class="card" href="#/compare/${p.id}">
        <h3>${esc(p.titel)}</h3><p class="fine">${esc(p.frage)}</p></a>`).join("")}</div>`;
    return;
  }
  view.innerHTML = `<p class="fine"><a href="#/compare">${esc(S.allCmp)}</a></p><p class="fine">${esc(S.loading)}</p>`;
  const docs = await Promise.all(pair.voices.map(v => {
    const m = D.mods.shipped.find(x => x.id === v.text);
    return text(m.datei).then(t => ({ v, m, t }));
  }));
  const col = ({ v, m, t }) => {
    const sec = t.sections.find(s => s.id === v.sec);
    const units = v.n.map(n => sec.units.find(u => u.n === n)).filter(Boolean);
    return `<div class="voice">
      <div class="vhead">${side(m.side)} <b>${esc(v.wer || t.autor)}</b><br><span class="fine">${esc(t.jahr)} · ${esc(sec.titel)}</span></div>
      ${units.map(u => `<div class="vunit"><div class="fine"><a href="#/text/${m.id}/${sec.id}/${u.n}">${esc(sec.zk)} [${u.n}]</a>${u.titel ? ` · ${esc(u.titel)}` : ""}</div>
        <div class="text">${esc(u.orig)}</div></div>`).join("")}
    </div>`;
  };
  view.innerHTML = `
    <p class="fine"><a href="#/compare">${esc(S.allCmp)}</a></p>
    <span class="tag">${esc(S.cmpTag)}</span><h1>${esc(pair.titel)}</h1>
    <p class="lede">${esc(pair.frage)}</p>
    <div class="panel readable"><p>${esc(pair.note)}</p></div>
    <div class="cmp n${docs.length}">${docs.map(col).join("")}</div>`;
}

/* ------------------------------------------------------------ timeline */
function timeline() {
  const TL = D.timeline;
  view.innerHTML = `
    <span class="tag">${esc(S.tlTag)}</span><h1>${esc(S.tlH)}</h1>
    <p class="lede">${esc(TL.lede)}</p>
    <div class="legend">${Object.keys(SIDES).map(side).join(" ")}</div>
    <div class="tl">${TL.stations.map(s => {
      const p = s.plate && plateOf(s.plate);
      return `<div class="st" style="--c:var(--${s.side})">
        <div><div class="d">${esc(s.d)} · ${side(s.side)}</div><h3>${esc(s.titel)}</h3><p>${esc(s.text)}</p>
        ${s.cite ? `<p class="fine"><a href="${s.cite}">✦ ${esc(s.citeLabel)}</a></p>` : ""}
        ${s.quelle ? `<p class="fine">${esc(s.quelle)}</p>` : ""}</div>
        ${p ? `<img src="assets/plates/${p.id}_t.jpg" alt="${esc(p.titel)}" title="${esc(p.titel)}">` : "<span></span>"}
      </div>`;
    }).join("")}</div>`;
}

/* ------------------------------------------------------------ plates */
function plates() {
  view.innerHTML = `
    <span class="tag">${esc(S.platesTag)}</span><h1>${esc(S.platesH)}</h1>
    <p class="lede">${esc(D.plates.lede)}</p>
    <div class="grid g4">${D.plates.plates.map(plateFig).join("")}</div>
    <p class="fine">${esc(D.plates.credit)}</p>`;
  bindPlates(view);
}
function plateFig(p) {
  return `<figure class="plate card"><a href="#" data-p="${p.id}"><img src="assets/plates/${p.id}_t.jpg" alt="${esc(p.titel)}"></a>
      <figcaption>${side(p.side)} <b>${esc(p.titel)}</b><br>${esc(p.caption)}<br><i>${esc(p.source)}</i></figcaption></figure>`;
}
function bindPlates(root) {
  root.querySelectorAll("[data-p]").forEach(a => a.onclick = e => {
    e.preventDefault();
    const p = plateOf(a.dataset.p);
    const lb = document.createElement("div");
    lb.className = "lightbox";
    lb.innerHTML = `<figure><img src="assets/plates/${p.id}.jpg" alt="${esc(p.titel)}"><figcaption class="cap"><b>${esc(p.titel)}.</b> ${esc(p.caption)}</figcaption></figure>`;
    lb.onclick = () => lb.remove();
    document.body.append(lb);
  });
}

/* ------------------------------------------------------------ sources */
const METHOD = {
  tag: "Sources, method, limits", h: "How this apparatus is made",
  p: [
    ["Public domain only.", "The texts come from works of the United States government (soil surveys, geological reports, agricultural bulletins), from Florida state publications before 1931 and from newspapers, gazetteers and guides whose copyright has expired. Each module names its source; each passage is read against the page image of the print. Protected accounts and recent research are summarized and named as such, not printed."],
    ["Whose voices.", "Most of the people who loaded the cars, worked the pits and picked the crops appear in these sources only through others: officials, correspondents, railroad advertising. Where a voice is missing, the apparatus says so and does not invent it."],
    ["Violence.", "Lynchings and the destruction of Rosewood are documented from the sources of their time, with their language named for what it is, and never used as a story device."],
    ["Numbers.", "Where the sources disagree, their figures stand side by side. A figure found only in recent accounts, such as “seventy-five carloads a day”, is named as unverified until a period source carries it."],
    ["Boundaries.", "Williston, Morriston, Montbrook and Bronson, to 1945. Cedar Key, with its own history of port, fishery and cedar, appears only as a point of reference where the rails, timber and work lead there."]
  ],
  printed: "Sources printed here", plates: "Plates"
};

function sources() {
  const M = METHOD;
  view.innerHTML = `
    <span class="tag">${esc(M.tag)}</span><h1>${esc(M.h)}</h1>
    <div class="readable">${M.p.map(([b, p]) => `<p><b>${esc(b)}</b> ${esc(p)}</p>`).join("")}</div>
    ${D.mods.shipped.length ? `<h2>${esc(M.printed)}</h2>
    <div class="grid g2">${D.mods.shipped.map(m => `<div class="panel"><b>${esc(m.kurz)}</b><p class="fine" id="src-${m.id}">…</p></div>`).join("")}</div>` : ""}
    ${(D.plates.plates || []).length ? `<h2>${esc(M.plates)}</h2><p class="fine readable">${esc(D.plates.credit)}</p>` : ""}`;
  D.mods.shipped.forEach(async m => {
    const t = await text(m.datei);
    const el = document.getElementById("src-" + m.id);
    if (el) el.textContent = t.quelle;
  });
}

boot().catch(e => { view.innerHTML = `<p>${esc(S.fail)}${esc(e.message)}</p>`; });
