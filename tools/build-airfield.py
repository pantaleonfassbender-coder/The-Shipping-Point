"""Builds data/airfield.json (module 6: The airfield, 1942–1947) and enters the module in modules.json,
plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/PRUEFUNG.md):
  Levy County Journal (Bronson), 20 August, 17 September, 15 October 1942; 29 April, 13 May 1943; 6 April 1944;
    25 July 1946; 20 March 1947 (UFDC UF00028309; every issue July 1942 – December 1945 searched);
  Bradford County Telegraph (Starke), 19 May 1944 (UFDC UF00027795/04863);
  U.S. Geological Survey, Morriston quadrangle, 1:24,000, 1969 (plate).
The newspapers are presumed to be in the public domain by the University of Florida (published 1942–1947 without
renewal of copyright); the map is a work of the United States government.
Run from the site root: python tools/build-airfield.py
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


L = "Levy County Journal"

BUILD = [
    u(1, f"{L}, 20 August 1942, p. 1",
      "Montbrook Airfield Work Now Under Way—Located Near Williston In Levy Co. Work started last week on the new Montbrook Airfield, near to Williston, for the U. S. Army. Temporary offices are set up in the Williston City Hall, which in a few days will be turned over to the U. S. Employment Service, as the headquarters building at the Airfield will soon be completed. Williston is full of people who are interested in the work, and it will soon be hard to find an empty room in the town of Williston. Luther M. Hohan, and his fifteen to twenty surveyors are on the job and everything is progressing in fast order for the completion of the air field. All of Levy County is proud to see this field near Williston and trust that it will be a real help to the county as well as being an ideal training place for the forces which will be stationed there.",
      "“Work started last week”",
      "The county paper reports the field as a gain: work, lodgers, trade. Who did the work and on what terms, the paper does not say. The town hall offices were to pass to the U.S. Employment Service; whether Black workers were hired, and on what terms in a segregated county, is not in these sources (Texts, “Examined and not included”). Plate."),
    u(2, f"{L}, 17 September 1942, p. 3",
      "Commissioners Minutes. Regular Meeting Sept. 8, A. D. 1942. … The following letter was received and presented to the Board by Robert S. Bacon, Negotiator, Officer of the Division Engineer, Real Estate Branch: Mr. J. G. Newsom, Chairman, Board of County Commissioners, Bronson, Florida. Subject: Closing of Roads in Montbrook Airfield Area. Dear Sir: It is requested at the next regular meeting of the Board of County Commissioners of Levy County, Florida, that action be taken to close all county roads within the area of land being acquired by the government for the Montbrook Airfield. When this action is taken, it is also requested that three copies of the regulation, as passed, be furnished the Area Engineer of Montbrook Airfield. For your information and for use of your County Commission, you will find attached tract map with designated roads within the area thereon. Yours very truly, Robert S. Bacon, Negotiator, Office of the Division Engineer, Real Estate Branch. Whereupon, the Board authorized and instructed the Chairman and its Clerk to publish the following notice: Notice. Notice is hereby given that the Board of County Commissioners of Levy County, Florida, will meet on Friday, October 9th, 1942, at 10 o'clock A. M., for the purpose of closing certain County Roads, in the vicinity of what is known as the “Montbrook Airport;” said roads being within the following described lands, to-wit: SE 1-4 of Section 11, the South ½ of Section 12, all of Section 13 and the East ½ of Section 14; the East ½ of the SW 1-4 of Section 11, the NE 1-4 of Section 12; the East ½ of the West ½ of Section 14 and the North ½ of the NW 1-4 of NE 1-4; All of the above described property being in Range 18 East and Township 13 South, in Levy County, Florida.",
      "“Land being acquired by the government”",
      "The Army's real estate negotiator asks the county to close its roads across the site; the county obliges. The land lay south of Williston (plate: the runways on the map of 1969). How much of it had been farms, and whose, the minutes do not say; unit 3 names one household. Plate."),
    u(3, f"{L}, 15 October 1942, p. 4",
      "Mr. J. R. Fugate of Williston, was in Bronson Monday, and while here bought hunting license. Mr. Fugate was one of the ones living in Williston which the airbase affected very much, as his home had to be torn down. Mr. and Mrs. Rufus Stanley moved this week to Williston, where Mr. Stanley has a position with the airbase.",
      "“His home had to be torn down”",
      "Two lines from the social column, side by side: one family loses its house to the field, another moves to town for a job there. A Fugate was a truck grower at Williston in 1907 (module 2, unit 13); whether the same family, the note does not say."),
    u(4, f"{L}, 29 April 1943, p. 3",
      "Commissioners' Minutes. Regular Meeting April 6th, A. D. 1943. … Upon motion, duly seconded, the following resolution was duly adopted: Resolution Closing Roads, Levy County, Florida, OTU Site, Montbrook, Florida. Whereas, the United States of America has acquired, or is acquiring by virtue of negotiation, or other appropriate action of Condemnation and Declaration of Taking in the United States Courts, certain lands in the County of Levy, State of Florida, lying and being within Sections 11, 12, 13, 14 and 24, Township 13 South, Range 18 East, as delineated upon the photostatic copy of plat attached hereto and by this reference made a part hereof, And whereas, the said United States of America, by its duly authorized representatives has requested that certain streets, roads, highways and other public thoroughfares shown upon the aforesaid plat be vacated and closed as such streets, roads and public thoroughfares. Now, therefore, be it resolved by the Board of County Commissioners of the County of Levy, State of Florida, in regular session assembled; 1. That the Resolution adopted by the Board of County Commissioners, Levy County, Florida, on October 9, 1942, abandoning certain roads within Montbrook airport and recorded in Commissioners' Minute Book P at page 451, be and the same is herein and hereby rescinded. …",
      "“Condemnation and Declaration of Taking”",
      "Seven months later the field is an “OTU site”, an operational training unit of the Army Air Forces. The land was bought “by virtue of negotiation” or taken by condemnation in federal court; the resolution does not say which owners sold and which were condemned. The road closing of October 1942 was rescinded and replaced; the new resolution names Section 24 in addition. Plate."),
]

FIELD = [
    u(5, f"{L}, 13 May 1943, p. 1",
      "Levy's Red Cross War Fund Total Now Is $2,055.81. Additional reports on Levy County Chapter, American Red Cross 1943 War Fund, show that the county total has amounted to $2,055.81 to date. The additional report dated May 10, is as follows: Chiefland: Ethel Highsmith $1.00. Jack Highsmith 1.00. John Booth .50. 99th Bomb Squadron, Montbrook Air Base 19.91. Given by boys in service. Total previously reported 2,033.40. Total $2,055.81.",
      "“99th Bomb Squadron, Montbrook Air Base”",
      "The first unit named at the field in these sources. The paper prints it among the county's donors. Plate."),
    u(6, f"{L}, 6 April 1944, p. 1",
      "… Mrs. Gay is now a Senior in the Williston High School and expects to receive her diploma in May. Pvt. Gay is stationed in Orlando at the Pinecastle Army Air Field, but was formerly stationed with the 1160th School Squadron at the Montbrook Army Air Field in Williston. The couple plans to make their home in Orlando as soon as the bride has finished school.",
      "The 1160th School Squadron",
      "A wedding notice: a soldier from South Carolina and a Williston schoolgirl. In 1943 and 1944 the field changed units; a study of 2015 by the Air University reports that officers of a B-26 bomb group, training in Orlando, flew simulated bombing missions at Montbrook (recent literature, only summarized). When the training ended is not in the sources read so far."),
    u(7, "Bradford County Telegraph, 19 May 1944, p. 1",
      "The Race For Governor. (The following editorial appeared in the May 12, 1944 issue of the Winter Park Herald.) … Here are some of the undertakings in which Lex Green has been a leader or taken a prominent part in bringing to a successful conclusion. … 2. Establishment of Camp Blanding, and worked successfully for following military establishments at Orlando Air Base, Dale Mabry Field, Tallahassee, Avon Park bombing range, Fort Barrancas, Pensacola, Sarasota Army Air Field, Boca Raton Army Air Field, Buckingham Army Air Field (Fort Myers), Carlstrom Field (Arcaria), Eglin Field (Valpariso), Conners Field (Okeechobee), MacDill Field (Tampa), Dorr Field (Arcadia), Drane Field (Lakeland), Hendricks Field (Sebring), Homestead Army Air Field, Camp Gordon Johnston (Carabelle), Key West Barracks, Marathon Flight Strip, Morrison Field (West Palm Beach), Drew Field (Tampa), Camp Murphy (Hobe Sound), Taylor Field (Ocala), Tyndall Field (Panama City), Venice Army Air Field, Brandon Field (Perry), Fort Pierce, Marianna Army Air Field, Miami Air Depot, A. A. F. Redistribution Center No. 2 (Miami Beach), Miami Beach A. A. F. Training Base, Montbrook Air Field, Brooksville Air Field and Cross City Air Field. Total expenditure, $251,765,105.",
      "One field among many",
      "A campaign editorial for a candidate for governor, crediting a congressman with the bases; the claim of credit is the editorial's. The list itself shows the scale: Montbrook was one of dozens of Army fields and camps in wartime Florida, besides the Navy's stations listed under item 1 (graphic). Spellings as printed (“Arcaria”, “Valpariso”, “Carabelle”). Plate."),
]

AFTER = [
    u(8, f"{L}, 25 July 1946, p. 1",
      "Williston Airfield Declared To Be Surplus—City Will Be Allowed To Operate It—Study Airport Usages. War Assets Administration announced recently that 22 more government owned airfields in the United States had been declared surplus and that interim permits to operate them municipally had been issued. Five of the fields are in Florida and include: Montbrook Army Airfield, Williston; Herlong Naval Air Station, Jacksonville; Fort Pierce Naval Auxiliary Airfield, Fort Pierce; Perry Army Airfield, Perry; and Whitman Airfield, Martin County. These communities will be able to maintain the airports under CAA regulations, and will have the opportunity to study the problems of airport operation during the interval between the issuance of the interim permit and final disposition. Air service for these localities can be enhanced as a result of WAA's declaration of these fields as government surplus.",
      "“Declared to be surplus”",
      "A year after the war's end. The field passed, on an interim permit, to the town. Misprints of the original (“Nayal”, “Army Army Aairfield”, “ar”, “abie”) are corrected here. Plate."),
    u(9, f"{L}, 20 March 1947, pp. 1, 4",
      "[p. 1:] Auction Sale On April 3rd, 1947. The City of Williston last week purchased the Montbrook Army Air Base and all its buildings. Some of the buildings will be retained by the city but most of them will be sold at public auction on Thursday, April 3rd. Those interested in buying these buildings are urged to read the advertising in the Journal this week and make arrangements to be present at the sale. The City of Williston will retain the runways and adjoining lands next to the runways, amounting to over nine hundred acres. [p. 4, advertisement:] For Sale At Public Auction At Montbrook Army Airfield, April 3, 10 a.m. 42 Buildings. Also all Plumbing Fixtures and a large variety of other Fixtures and Equipment. A List of Buildings can be secured at the City Hall in Williston. All buildings and other items for sale can be seen and inspected on location at Montbrook Army Airfield from 10:00 A. M. to 4:00 P. M. Daily. For Sale by the City of Williston.",
      "Forty-two buildings at auction",
      "The town bought the field and sold most of its buildings; the runways remained (plate: Williston Municipal Airport on the map of 1969). Land taken from farms and homes in 1942 (units 2–4) thus passed to the town, not back to the families; whether any former owner bought land back, these sources do not say. Plates."),
]

SRC = ("Levy County Journal (Bronson), 20 August 1942, p. 1; 17 September 1942, p. 3; 15 October 1942, p. 4; 29 April 1943, p. 3; 13 May 1943, p. 1; 6 April 1944, p. 1; "
       "25 July 1946, p. 1; 20 March 1947, pp. 1 and 4. Bradford County Telegraph (Starke), 19 May 1944, p. 1. Page images: University of Florida Digital Collections "
       "(UF00028309, UF00027795). U.S. Geological Survey, Morriston quadrangle, 1:24,000, 1969. The newspapers are presumed by the University of Florida to be in the "
       "public domain; the map is a work of the United States government.")

T = {
    "titel": "The airfield",
    "autor": "The Levy County Journal, a Florida campaign editorial, and the U.S. Geological Survey",
    "jahr": "1942–1947",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print (obvious typesetting slips such as “sonn” for “soon” corrected and named here). “…” marks an omission; square brackets mark editorial additions. Every issue of the Levy County Journal from July 1942 to December 1945 was searched for the field. The Army's own records of the field (station and unit histories) have not been read; they are federal records, and would show what the newspaper does not: who built and worked at the field, Black and white, how many served there, and when training ended. The account of the 397th Bombardment Group (Air University, 2015) and the official history The Army Air Forces in World War II (1955, under copyright) are recent or protected literature and are only summarized.",
    "sections": [
        {"id": "build", "titel": "Building the field (1942–1943)",
         "blurb": "In August 1942 work began south of Williston on an airfield for the Army. The county closed its roads across the site; the government bought or condemned the land; at least one family lost its house.",
         "plates": ["air1942_work", "air1942_letter", "air1943_otu"], "viz": "airfield-line", "units": BUILD},
        {"id": "field", "titel": "The field at war (1943–1944)",
         "blurb": "Bomb squadrons and a school squadron at Montbrook, as the county paper glimpsed them, and the field's place among the dozens of Army fields and camps in wartime Florida.",
         "plates": ["air1943_redcross", "bct1944_fields"], "viz": "airfield-florida", "units": FIELD},
        {"id": "after", "titel": "Surplus (1946–1947)",
         "blurb": "After the war the field was declared surplus, bought by the town of Williston and its buildings sold at auction; the runways became the town's airport.",
         "plates": ["air1946_surplus", "air1947_auction", "usgs1969_airport"], "units": AFTER},
    ],
}
for s in T["sections"]:
    s["zk"] = "The airfield, " + re.sub(r" \(.*", "", s["titel"])
(D / "airfield.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
UF = "University of Florida Digital Collections (Florida Digital Newspaper Library)"
NEW = [
    {"id": "air1942_work", "side": "air", "titel": "“Work now under way”, August 1942",
     "caption": "The Levy County Journal reports the start of work on the Montbrook Airfield near Williston.",
     "source": "Levy County Journal, 20 August 1942, p. 1; " + UF + ", UF00028309; presumed public domain."},
    {"id": "air1942_letter", "side": "air", "titel": "Closing the roads, September 1942",
     "caption": "The Army's real estate negotiator asks the county commission to close the roads across the land “being acquired by the government”.",
     "source": "Levy County Journal, 17 September 1942, p. 3; " + UF + ", UF00028309; presumed public domain."},
    {"id": "air1943_otu", "side": "air", "titel": "“OTU Site, Montbrook”, April 1943",
     "caption": "The county's resolution: land acquired “by virtue of negotiation, or other appropriate action of Condemnation and Declaration of Taking”.",
     "source": "Levy County Journal, 29 April 1943, p. 3; " + UF + ", UF00028309; presumed public domain."},
    {"id": "air1943_redcross", "side": "air", "titel": "The 99th Bomb Squadron, May 1943",
     "caption": "“99th Bomb Squadron, Montbrook Air Base … Given by boys in service”: a line in the county's Red Cross war fund.",
     "source": "Levy County Journal, 13 May 1943, p. 1; " + UF + ", UF00028309; presumed public domain."},
    {"id": "bct1944_fields", "side": "air", "titel": "Florida's fields, 1944",
     "caption": "A campaign editorial lists the Army fields and camps of wartime Florida, Montbrook among them.",
     "source": "Bradford County Telegraph (Starke), 19 May 1944, p. 1; " + UF + ", UF00027795; presumed public domain."},
    {"id": "air1946_surplus", "side": "air", "titel": "“Declared to be surplus”, July 1946",
     "caption": "The War Assets Administration releases the field to the town on an interim permit.",
     "source": "Levy County Journal, 25 July 1946, p. 1; " + UF + ", UF00028309; presumed public domain."},
    {"id": "air1947_auction", "side": "air", "titel": "42 buildings at auction, April 1947",
     "caption": "The City of Williston sells the buildings of the Montbrook Army Airfield.",
     "source": "Levy County Journal, 20 March 1947, p. 4; " + UF + ", UF00028309; presumed public domain."},
    {"id": "usgs1969_airport", "side": "air", "titel": "The runways in 1969",
     "caption": "Williston Municipal Airport, the former Montbrook Army Air Field, south of the town: three runways in a triangle.",
     "source": "U.S. Geological Survey, Morriston quadrangle, 1:24,000, 1969, detail; USGS Historical Topographic Map Collection; public domain."},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "airfield"), None) or next(x for x in M["shipped"] if x["id"] == "airfield")
M["planned"] = [x for x in M["planned"] if x["id"] != "airfield"]
m.update({"datei": "airfield", "zk": "Building · At war · Surplus",
          "kurz": "6 · The airfield",
          "warum": "In August 1942 the Army began an airfield south of Williston on land bought or condemned; one family's house was torn down. Bomb squadrons trained there, one field among dozens in wartime Florida. In 1947 the town bought it, sold forty-two buildings at auction and kept the runways.",
          "quelle": "Levy County Journal 1942–1947 (every issue July 1942 – December 1945 searched); Bradford County Telegraph 1944; USGS Morriston sheet 1969."})
order = ["before", "rails", "rock", "shipping", "line", "airfield"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "airfield"] + [m], key=lambda x: order.index(x["id"]) if x["id"] in order else 99)
ADD = [{"id": "aafrecords", "side": "air", "kurz": "The Army's records of the field",
        "warum": "Station and unit histories of the Army Air Forces would cover the Montbrook Army Air Field. As federal records they are in the public domain, but they have not been found or read yet. They would show who built the field and worked there, Black and white, how many served, and when training ended; the county paper does not.",
        "quelle": "Federal records of the Army Air Forces (to be found)."}]
have = {x["id"] for x in M["missing"]}
M["missing"] += [x for x in ADD if x["id"] not in have]
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "land", "titel": "The land, taken and sold",
     "frage": "What happened to the land of the airfield?",
     "note": "In 1942–43 the government acquired the land south of Williston “by virtue of negotiation, or other appropriate action of Condemnation”; in 1947 the town bought the field, sold the buildings and kept over nine hundred acres with the runways. In between, the county paper notes one family whose house “had to be torn down”.",
     "voices": [{"text": "airfield", "sec": "build", "n": [4], "wer": "County commission, 1943"},
                {"text": "airfield", "sec": "build", "n": [3], "wer": "Levy County Journal, 1942"},
                {"text": "airfield", "sec": "after", "n": [9], "wer": "Levy County Journal, 1947"}]},
    {"id": "boom", "titel": "Booms from outside",
     "frage": "How did the town greet the great outside investments?",
     "note": "",
     "voices": [{"text": "before", "sec": "road", "n": [6], "wer": "Florida Railroad, 1855"},
                {"text": "airfield", "sec": "build", "n": [1], "wer": "Levy County Journal, 1942"}]},
]
PAIRS[1]["note"] = ("The pattern recurs: in 1855 the president of the Florida Railroad promised “public benefit” and a profitable investment; in 1942 the county paper trusted that the "
                    "airfield would be “a real help to the county”. In both cases the decision was taken elsewhere, and the land and the labour came from the county.")
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/airfield/"
NEWST = [
    {"d": "August 1942", "side": "air", "titel": "Montbrook Airfield",
     "text": "Work begins south of Williston on an airfield for the U.S. Army; the county closes its roads across land “being acquired by the government”.",
     "cite": K + "build/1", "citeLabel": "The airfield [1]", "plate": "air1942_work",
     "quelle": "Levy County Journal, 20 August and 17 September 1942."},
    {"d": "May 1943", "side": "air", "titel": "The 99th Bomb Squadron",
     "text": "The field is an “OTU site”, a training base for bomber crews; its 99th Bomb Squadron gives to the county's Red Cross war fund.",
     "cite": K + "field/5", "citeLabel": "The airfield [5]", "plate": "air1943_redcross",
     "quelle": "Levy County Journal, 29 April and 13 May 1943."},
    {"d": "July 1946", "side": "air", "titel": "Surplus",
     "text": "The War Assets Administration declares the Montbrook Army Airfield surplus and lets the town operate it.",
     "cite": K + "after/8", "citeLabel": "The airfield [8]", "plate": "air1946_surplus",
     "quelle": "Levy County Journal, 25 July 1946."},
    {"d": "April 1947", "side": "air", "titel": "Forty-two buildings at auction",
     "text": "The City of Williston buys the field, sells its buildings and keeps the runways and over nine hundred acres.",
     "cite": K + "after/9", "citeLabel": "The airfield [9]", "plate": "air1947_auction",
     "quelle": "Levy County Journal, 20 March 1947."},
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
(D / "timeline.json").write_text(json.dumps(TL, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", sum(len(s["units"]) for s in T["sections"]), "units")
