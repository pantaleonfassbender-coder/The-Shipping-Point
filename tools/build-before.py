"""Builds data/before.json (module 1: Before the rails, 1853–1886) and enters the module in modules.json,
plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/PRUEFUNG.md):
  Ocala Banner, 3 March 1911, after the Williston Advocate (UFDC UF00048734/00794);
  D. L. Yulee, Report to the Directors and Stockholders of the Florida Railroad Company, July 1855
    (IA report-to-the-directors-and-stockholders), pp. 3, 7–8, 30;
  Population of the United States in 1860 (Washington 1864) (IA populationofusin00kennrich), pp. 51, 53;
  Population schedules of the eighth census, 1860, Florida, slave schedules (NARA microfilm M653, reel 110;
    IA populationschedu110unit), Levy County, page 1;
  Florida State Gazetteer and Business Directory 1886–7 (IA floridastategaze1886sout), pp. 91, 269, 386, 458;
  U.S. Geological Survey, Florida, Williston sheet, 1:62,500, edition of 1895.
All in the public domain.
Run from the site root: python tools/build-before.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"


def u(n, pg, orig, titel=None, note=None):
    x = {"n": n, "pg": pg}
    if titel:
        x["titel"] = titel
    x["orig"] = orig
    if note:
        x["note"] = note
    return x


G = "Florida State Gazetteer 1886"

SETTLE = [
    u(1, "Ocala Banner, 3 March 1911",
      "Was Founded by an Ocalian. It may not be generally known that our neighboring city, Williston, was settled by an Ocalian, but such is a fact. The last issue of the Advocate says: In 1853 this community was a vast forest, unnamed and untrammeled by the march of civilization, and unscarred by the axe of industry. In that year Hon. Jesse M. Willis, who was tax collector and assessor of Marion county, moved from Ocala to the present site of this town. He spent the remaining twenty-eight years of his life here, maintaining a large plantation, about two-thirds of which was situated within the present corporate limits. He arrived here with a force of about thirty faithful slaves and immediately began a development which, although it has been slow, has not ceased from the fall of 1853 to the spring of 1911. Mr. Willis chose his location well, for no finer timber ever covered the lands of a southern state, and no better lands were ever sheltered by southern pines, and, with an altitude of ninety feet above sea level, pure water and no stagnant pools, the general health has always been unsurpassed.",
      "“About thirty faithful slaves”",
      "The town's own account of its founding, written by its newspaper fifty-eight years later and reprinted in Ocala. It is the only source found so far for Willis, the date and the plantation. “Faithful slaves” is the language of 1911, in which the people Willis held in bondage appear as his “force” and as loyal; they cleared the forest and worked the plantation on which the town was later built. Their names, and what became of them after emancipation, are not in this source and have not been found in any other (Texts, “Examined and not included”). The account says nothing of who lived on the land before 1853."),
    u(2, "Population of the United States in 1860, pp. 51, 53",
      "State of Florida. Table No. 1.—Population by Age and Sex. White. [Counties; Total, M., F.; Aggregate:] … Levy 696 635 1,331. … Marion 1,796 1,498 3,294. … Slave. … Levy 203 247 450. … Marion 2,689 2,625 5,314. … Aggregate. Total whites 77,747. Total free colored 932. Total slaves 61,745.",
      "450 people held in slavery",
      "The federal census of 1860, seven years after Willis's arrival. One person in four in Levy County was enslaved; in Marion, the county Willis came from, three in five. The table of free colored inhabitants has no line for Levy. Whether Willis's plantation was counted in Levy or in Marion is not clear: the county line ran only a few miles east of the later town (plate: the map of 1895)."),
    u(3, "Census of 1860, slave schedule, Levy County, p. 1",
      "Schedule 2.—Slave Inhabitants in … in the County of Levy State of Florida, enumerated by me, on the 1st day of June, 1860. … Ass't Marshal. [Columns:] Names of slave owners. Number of slaves. Description: Age. Sex. Color. Fugitives from the State. Number manumitted. Deaf & dumb, blind, insane, or idiotic. No. of slave houses. [First entries:] Margaret Barrow, 1, 37, m, b; 1, 33, f, b; 1, 15, [f], m; 1, 10, [f], m; 1, 4, m, b; 1, ½, [m], m. Thomas C. Love, 1, 58, f, b; … [Foot of the page:] No. of owners, 10. No. of houses, 23.",
      "Counted without names",
      "The census recorded the owners by name and the people they held only by age, sex and colour (“b” black, “m” mulatto); “[f]” and “[m]” stand for the ditto marks of the form. A child of six months is the sixth person listed under the first owner. The page total of the enslaved is corrected by hand on the image (plate). Jesse M. Willis has not been found on Levy County's pages of the schedule; the Marion County pages have not yet been searched."),
]

ROAD = [
    u(4, "Yulee, Report to the Florida Railroad Company (1855), p. 3",
      "To the Directors and Stockholders of the Florida Railroad Company: The work upon your road being expected to commence shortly, I have deemed it advisable to lay before you some views respecting the probable sources of its business. The route of the Florida railroad, or that part which for the present engages the efforts of the company, lies across the peninsula of Florida, from Fernandina, on the Atlantic, in latitude 30° 40′, longitude 81° 37′, to Cedar Key, on the Gulf of Mexico, in latitude 29° 07′, longitude 83° 03′. Its length, as determined by surveys of the United States engineers, will be one hundred and thirty-seven and a half miles. The track of the road will be laid upon an air line between the two terminal points, there being no natural obstacles to interfere with this purpose.",
      "Fernandina to Cedar Key",
      "D. L. Yulee signed as the company's president. The “air line” passed northwest of the later Williston, through Archer and Bronson (module 2, plate: the map of 1891). Cedar Key, the Gulf terminus, is a point of reference here, not a subject (Texts, “Examined and not included”)."),
    u(5, "Yulee, Report (1855), pp. 7–8",
      "The soil of the peninsula is very productive, and yields all the richest staples. It produces the long staple, or Sea Island cotton of commerce, over every part of it, with a productiveness surpassing the coasts of South Carolina and Georgia, to which this staple had been before limited; and can supply any quantity of it to which the consumption can ever reach. … It is a fine fruit and vegetable gardening region. Peas, and most other garden stuffs, blossom and bear throughout the winter. The value of this capability, when lines of steamers are established to New York, may be estimated from the fact that the Norfolk steamers carry on some of their trips over two thousand barrels of market stuff to New York, … It has the most valuable forest woods in great abundance—live-oak, red cedar, cypress, and yellow pine of the first quality. The road so crosses the peninsula as to command the transportation business of a great part of the agricultural productions of the best part of it. And as it passes through a finely-timbered country, the naval store and lumber business will furnish large employment throughout the year.",
      "“Garden stuffs … to New York”",
      "In 1855 the company's president already foresaw the trade that made Williston forty years later: winter vegetables for the New York market (module 4), timber and naval stores (modules 3 and 5). The cotton he describes was grown by enslaved people; the report speaks of crops and freight, not of the people who would raise them or build the road."),
    u(6, "Yulee, Report (1855), p. 30",
      "Taking into view that the large agricultural productions of one of the finest and most rapidly developing portions of the South must be thrown upon this road; that it will have a large naval store and lumber business throughout its length; … I have no doubt that the enterprise will result in public benefit, and that the road will prove a profitable investment. Respectfully submitted, D. L. Yulee, President Florida Railroad Company.",
      "“A profitable investment”",
      "The close of the report (plate: its cover)."),
]

COUNTY = [
    u(7, f"{G}, p. 269",
      "Levy County. Population, 1885, 6,678. Bronson, county seat. Post Offices.—Barco, Bronson, Cedar Key, Ellzey, Gore, Gulf Hammock, Levyville, Otter Creek, Rosewood, Wilston. Levy county has an area of 940 square miles, or 601,600 acres. … The number of acres of improved and cultivated lands in the county, according to the census reports of 1885, is 9,590 acres, and there was a total of 499,954 acres assessed for taxes. … The number of votes polled in the county at the 1884 election was 991, of which there were 654 Democratic and 337 Republican. The population of this county in 1880 was 5,767, which, compared with the recent figures, shows an increase of 911. The land surface of this county is principally level, the southern portion being flat pine lands, heavily timbered, most suited to the growth of sugar cane and rice, while the northern portion is productive of field crops, fruits and vegetables.",
      "Levy County, 1885",
      "“Wilston”: so printed for Williston. Less than one acre in sixty of the county was under cultivation. Who cast the 337 Republican votes of 1884 the gazetteer does not say."),
    u(8, f"{G}, p. 91",
      "Bronson. Levy County. Population, 300. C. E. Taylor, postmaster. This is the county seat of Levy, located on the line of the Florida Railway and Navigation Company's railroad, about 18 miles southwest of Gainesville and 200 miles southeast of Tallahassee. Gainesville is the nearest bank. Has a weekly newspaper, one school, Methodist church, cotton gin and four stores, express and telegraph offices, and is a money-order post office; mails daily. Cotton, oranges, syrup and potatoes are the chief shipments. It is an incorporated town, and was first settled in 1866.",
      "Bronson, on the railroad",
      "Yulee's road, now the Florida Railway and Navigation Company's, made Bronson the county seat. The weekly newspaper is the Levy County Times (directory under the entry)."),
    u(9, f"{G}, p. 386",
      "Rosewood. Levy County. Population, 50. C. M. Jacobs, postmaster. First settled in 1855. Situated on the Central Division of the Florida Railway and Navigation Company's railroad, 23 miles southwest of Bronson, the county seat, 10 miles northeast of Cedar Key, the nearest express and telegraph station. Gainesville is the nearest banking point. Has one general store, hotel and Episcopal church. Red cedar is the principal shipment.",
      "Rosewood, 1886",
      "Rosewood thirty-seven years before its destruction (module 5): a station on the same railroad, shipping red cedar. The directory names a postmaster, a hotel keeper, carpenters and clergy; whether the Black families of 1923 or their parents lived there in 1886 it does not show."),
    u(10, f"{G}, p. 458",
      "Williston. Levy County. Population, 100. J. B. Epperson, postmaster. Was first settled in 1840. Situated 13 miles southeast of Bronson, the county seat, 11 miles southeast of Archer, the shipping point and nearest express station. …",
      "“First settled in 1840”",
      "The full entry is in module 2 (unit 2). The gazetteer's date differs from the Advocate's 1853 (unit 1); neither source says where its date comes from."),
]

SRC = ("Ocala Banner, 3 March 1911 (after the Williston Advocate). D. L. Yulee, Report to the Directors and Stockholders of the Florida Railroad Company, July 1855 (Washington 1855), "
       "pp. 3, 7–8, 30. Population of the United States in 1860 (Washington 1864), pp. 51, 53. Eighth census of the United States, 1860, slave schedules, Florida, Levy County, p. 1 "
       "(National Archives microfilm M653, reel 110). Florida State Gazetteer and Business Directory, vol. I, 1886–7, pp. 91, 269, 386, 458. Page images: University of Florida Digital "
       "Collections (UF00048734) and Internet Archive (report-to-the-directors-and-stockholders, populationofusin00kennrich, populationschedu110unit, floridastategaze1886sout). "
       "All in the public domain.")

T = {
    "titel": "Before the rails",
    "autor": "The Williston Advocate (1911), the president of the Florida Railroad (1855), the federal census of 1860 and a state gazetteer (1886)",
    "jahr": "1853–1886",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print. “…” marks an omission; square brackets mark editorial additions, such as the column headings of a census table. The founding story comes from a town newspaper of 1911 and is the town's own memory, not a record of 1853. The people Jesse M. Willis held in slavery appear in it only as his “force”, and in the census only as numbers; none of them is named in any source found so far. Who lived on the land before 1853 is not covered by these sources.",
    "sections": [
        {"id": "settle", "titel": "A plantation in the pines (1853–1860)",
         "blurb": "The town's founding story tells of a Marion County official who came in 1853 with “about thirty faithful slaves”. The census of 1860 counts 450 enslaved people in Levy County and lists them by age, sex and colour, without names.",
         "plates": ["usgs1895_williston", "census1860_levy"], "viz": "before-census", "units": SETTLE},
        {"id": "road", "titel": "The road to the Gulf (1855)",
         "blurb": "Two years after Willis, the president of the Florida Railroad laid out a line from Fernandina to Cedar Key and the business he expected: cotton, timber, naval stores, and vegetables for New York. The line passed the later Williston by.",
         "plates": ["frr1855_cover"], "units": ROAD},
        {"id": "county", "titel": "Levy County, 1885–1886",
         "blurb": "Thirty years on, a gazetteer describes a thinly settled county: Bronson the county seat on the railroad, Rosewood a cedar station, Williston a settlement of a hundred eleven miles from its shipping point.",
         "plates": ["map1891_levy"], "units": COUNTY},
    ],
}
for s in T["sections"]:
    s["zk"] = "Before the rails, " + re.sub(r" \(.*", "", s["titel"])
(D / "before.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
NEW = [
    {"id": "usgs1895_williston", "side": "town", "titel": "Williston and its neighbours, 1895",
     "caption": "The U.S. Geological Survey's Williston sheet: Williston, Montbrook, Morriston and “Phosphate” on the Florida Central & Peninsular and its Eagle Mine Branch, the Levy–Marion county line to the east, and the ponds and sinks of the limestone country.",
     "source": "U.S. Geological Survey, Florida, Williston sheet, 1:62,500, edition of 1895, detail; USGS Historical Topographic Map Collection; public domain."},
    {"id": "census1860_levy", "side": "colour", "titel": "Levy County, 1 June 1860",
     "caption": "The first page of the slave schedule of Levy County: owners by name, the people they held by age, sex and colour only.",
     "source": "Eighth census of the United States, 1860, Schedule 2 (slave inhabitants), Florida, Levy County, p. 1; National Archives microfilm M653, reel 110, via Internet Archive populationschedu110unit; public domain."},
    {"id": "frr1855_cover", "side": "rail", "titel": "The Florida Railroad, 1855",
     "caption": "Report to the directors and stockholders of the Florida Railroad Company, July 1855, by its president, David Levy Yulee.",
     "source": "Report to the Directors and Stockholders of the Florida Railroad Company (Washington 1855), cover; Internet Archive report-to-the-directors-and-stockholders; public domain."},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
P["credit"] = P["credit"].replace("the Plant System map from Poor's Manual (1901) via Wikimedia Commons;",
                                  "the Plant System map from Poor's Manual (1901) via Wikimedia Commons; the Williston sheet of the U.S. Geological Survey (1895); the slave schedule of 1860 from the National Archives microfilm via the Internet Archive;")
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "before"), None) or next(x for x in M["shipped"] if x["id"] == "before")
M["planned"] = [x for x in M["planned"] if x["id"] != "before"]
m.update({"datei": "before", "zk": "Plantation · Railroad · County",
          "kurz": "1 · Before the rails",
          "warum": "A plantation founded in 1853 with “about thirty faithful slaves”, as the town remembered it in 1911; 450 enslaved people counted without names in Levy County in 1860; a railroad to Cedar Key that passed the place by; and in 1886 a settlement of a hundred, eleven miles from its shipping point.",
          "quelle": "Ocala Banner 1911 (after the Williston Advocate); Florida Railroad Company report 1855; Census of 1860 and its slave schedule; Florida State Gazetteer 1886; USGS Williston sheet 1895."})
order = ["before", "rails", "rock", "shipping", "line", "airfield"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "before"] + [m], key=lambda x: order.index(x["id"]) if x["id"] in order else 99)
ADD = [{"id": "willis1860", "side": "colour", "kurz": "The people of the Willis plantation",
        "warum": "The about thirty people Jesse M. Willis brought in 1853 are not named in any source found so far. Willis has not been found on Levy County's slave schedule of 1860; the Marion County pages and the census of 1870 have not yet been searched.",
        "quelle": "Census of 1860 (slave schedules) and 1870 (population schedules), Levy and Marion counties."},
       {"id": "seminole", "side": "town", "kurz": "Before 1842",
        "warum": "Who lived on the land around Williston before 1853, Seminole history included, is not covered by any source read so far; it is named here so that the apparatus does not begin as if the forest of 1853 had been empty.",
        "quelle": "To be found."}]
have = {x["id"] for x in M["missing"]}
M["missing"] += [x for x in ADD if x["id"] not in have]
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "founding", "titel": "1840 or 1853?",
     "frage": "When was Williston settled?",
     "note": "A state gazetteer of 1886 says the place “was first settled in 1840”; the town's own newspaper in 1911 dates its beginning to the fall of 1853 and the arrival of Jesse M. Willis and the people he held in slavery. Neither says where its date comes from.",
     "voices": [{"text": "before", "sec": "county", "n": [10], "wer": "Florida State Gazetteer, 1886"},
                {"text": "before", "sec": "settle", "n": [1], "wer": "Williston Advocate, 1911"}]},
    {"id": "foresight", "titel": "Foreseen in 1855",
     "frage": "What did the railroad promise, and what came?",
     "note": "In 1855 the president of the Florida Railroad expected winter vegetables for New York and a great naval store and lumber business. Sixty years later both had come to Williston, by other railroads: the cucumber trains of module 4 and the turpentine and timber camps of modules 3 and 5.",
     "voices": [{"text": "before", "sec": "road", "n": [5], "wer": "D. L. Yulee, 1855"},
                {"text": "shipping", "sec": "trainload", "n": [7], "wer": "Seaboard Air Line, 1914"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/before/"
NEWST = [
    {"d": "Fall 1853", "side": "town", "titel": "Jesse M. Willis and “about thirty” enslaved people",
     "text": "By the town's own account of 1911, a Marion County tax collector moves from Ocala into the pine forest with about thirty enslaved people and founds the plantation on which Williston later grows.",
     "cite": K + "settle/1", "citeLabel": "Before the rails [1]",
     "quelle": "Ocala Banner, 3 March 1911, after the Williston Advocate."},
    {"d": "July 1855", "side": "rail", "titel": "A railroad to Cedar Key",
     "text": "The Florida Railroad Company's president, David Levy Yulee, lays out the line from Fernandina to Cedar Key and its prospects: Sea Island cotton, timber, naval stores, vegetables for New York.",
     "cite": K + "road/4", "citeLabel": "Before the rails [4]", "plate": "frr1855_cover",
     "quelle": "Report to the Directors and Stockholders of the Florida Railroad Company (1855)."},
    {"d": "June 1860", "side": "colour", "titel": "450 enslaved people in Levy County",
     "text": "The census counts 1,331 white and 450 enslaved inhabitants in Levy County; the slave schedule lists the enslaved by age, sex and colour, without names.",
     "cite": K + "settle/2", "citeLabel": "Before the rails [2]", "plate": "census1860_levy",
     "quelle": "Population of the United States in 1860, pp. 51, 53; slave schedule, Levy County."},
    {"d": "1885", "side": "town", "titel": "Levy County, 6,678 people",
     "text": "Less than one acre in sixty of the county is under cultivation; Bronson, on the railroad, is the county seat, and “Wilston” one of ten post offices.",
     "cite": K + "county/7", "citeLabel": "Before the rails [7]",
     "quelle": "Florida State Gazetteer 1886–7, p. 269."},
]
titles = {s["titel"] for s in NEWST}
TL["stations"] = [s for s in TL["stations"] if s["titel"] not in titles] + NEWST
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def year(s):
    d = s["d"]
    m_ = re.search(r"\d{4}", d)
    mon = next((i + 1 for i, x in enumerate(MONTHS) if x in d), 10 if "Fall" in d else (13 if re.fullmatch(r"\d{4}–\d{4}", d) else 0))
    return (int(m_.group()) if m_ else 9999, mon, d)


TL["stations"].sort(key=year)
TL["lede"] = "Stations read against the page images of their sources only; each names its source."
(D / "timeline.json").write_text(json.dumps(TL, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", sum(len(s["units"]) for s in T["sections"]), "units")
