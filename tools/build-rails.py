"""Builds data/rails.json (module 2: Two railroads, 1886–1907) and enters the module in modules.json,
plates.json, timeline.json and compare.json.

Sources, each passage read against the page image of the Internet Archive (log: ../quellen/PRUEFUNG.md):
  South Publishing Co., Florida State Gazetteer and Business Directory, vol. I, 1886–7 (floridastategaze1886sout),
    pp. 65, 458;
  Engineering News and American Railway Journal 26/27, 4 July 1891 (sim_enr_1891-07-04_26_27), p. 20;
  Manufacturers' Record 23/22, 30 June 1893 (sim_site-selection_1893-06-30_23_22), p. 396;
  Florida Railroad Gazetteer and State Business Directory 1895 (floridarailroadg1895beld), p. 273;
  First Annual Report of the Railroad Commission of the State of Florida, 1898
    (FirstAnnualReportOfTheRailroadCommissionOfTheStateOfFlorida), pp. 12–13, 43, 81, 86, 91, 94;
  Laws of Florida 1905, chapters 5549 and 5550 (actsandresoluti03florgoog), pp. 869–870;
  R. L. Polk & Co.'s Florida Gazetteer and Business Directory 1907–1908 (floridagazetteer1907rlpo), p. 452.
All in the public domain (published before 1931; Florida state publications).
Run from the site root: python tools/build-rails.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
IA = "https://archive.org/details/"


def u(n, pg, orig, titel=None, note=None):
    x = {"n": n, "pg": pg}
    if titel:
        x["titel"] = titel
    x["orig"] = orig
    if note:
        x["note"] = note
    return x


ARCHER = [
    u(1, "Gazetteer 1886, p. 65",
      "ARCHER. ALACHUA COUNTY. Population, 200. W. C. Andruss, postmaster. Situated fifteen miles southwest of Gainesville, the county seat and nearest banking place; on the Fla. Ry. & N. Co.'s railroad. It is a post office money order office, and has express and telegraph offices, two cotton gins, saw and grist mills, Methodist, Presbyterian and Baptist churches, a school, five general stores, druggist, carriage and wagon factory. Cotton, oranges, vegetables and poultry are the principal shipments. Has mails twice daily. Lands range in price from $5 to $25 per acre. The surrounding country is a fine vegetable and orange-growing section, cotton and grain are extensively produced.",
      "Archer, on the railroad",
      "“Fla. Ry. & N. Co.”: the Florida Railway & Navigation Company. The map of 1891 (plate) names the line through Archer and Bronson to Cedar Key the Florida Central & Peninsular; module 1 will trace it back to David Levy Yulee's Florida Railroad. Archer has what Williston lacks: the railroad, the express and the telegraph."),
    u(2, "Gazetteer 1886, p. 458",
      "WILLISTON. LEVY COUNTY. Population, 100. J. B. Epperson, postmaster. Was first settled in 1840. Situated 13 miles southeast of Bronson, the county seat, 11 miles southeast of Archer, the shipping point and nearest express station. H. F. Dutton & Company, of Gainesville, are the nearest bankers. Has one general store, a steam saw and grist mill, vegetable crate factory and cotton gin, public school, Methodist and Baptist churches. Sea Island cotton, oranges and vegetables are the principal shipments. Mails Monday, Wednesday, Friday and Saturday. Land sells at $3 to $10 per acre.",
      "“Archer, the shipping point”",
      "The phrase that gives this apparatus its title, still pointing away from Williston: whatever the settlement grew went by wagon eleven miles to Archer. A vegetable crate factory already stands in 1886. J. B. Epperson, postmaster and storekeeper, appears again in 1895 (unit 5) and in 1907 as vice president of the Bank of Williston (unit 13). The year of settlement differs between sources; module 1 will set them side by side. The directory under the entry (plate) lists J. P. Reddick's “saw mill and crate manufactory” and names planters and growers with their acreage; the people who worked their fields do not appear."),
]

BUILD = [
    u(3, "Engineering News, 4 July 1891, p. 20",
      "Archer & Dunnellon.—About 350 men are reported on the railway from Archer to Dunnellon, Fla., and it is expected to have the line finished by Aug. 15. The Florida Central & Peninsular R. R. Co. will operate the road when it is completed.",
      "About 350 men",
      "The figure is unclear in the print and may read 360. Williston lies between Archer and Dunnellon (unit 2 places it eleven miles southeast of Archer), but the notice does not name it. Who the men were, and on what terms they worked, it does not say either. In 1893–94 the state's leased convicts were worked in phosphate near Albion (module 3); whether convicts also built this line is not known from these sources."),
    u(4, "Manufacturers' Record, 30 June 1893, p. 396",
      "The new connection which will give the Plant system an all-rail haul from Savannah to Tampa through the phosphate region will be made, but not exactly in the manner originally contemplated. The original plan was to run almost in a direct line south from a point a few miles above High Springs to Juliette, on the Ocala, Silver Springs & Gulf Railroad. This would have taken the road through the important Albion district and paralleled the short line running south from Archer to the Early Bird mines and other phosphate plants some twenty miles, known as the Ambler road, originally built as a timber outlet and later purchased by the Florida Central & Peninsular Railroad. But after the arrangements seemed to have been completed, surveys made and grading partly accomplished, a conference developed traffic arrangements between the rival systems, which resulted in the abandonment of the lower division of the new link and the common use of the present spur, the lower end of which is to be continued to a point something north of the original point, Juliette. The line has been graded, tied and laid to within a few miles of Archer from the north, coming in a direct line toward Albion until within a few miles, when it branches almost east to Archer. The Albion people were very anxious for the road and prepared elaborate maps, which from some cause miscarried in reaching the Plant system authorities.",
      "“Traffic arrangements between the rival systems”",
      "The Plant System was the group of railroads around the Savannah, Florida & Western Railway (unit 7). Instead of building a parallel line, it came to an arrangement with its rival and used the Florida Central & Peninsular's spur south of Archer. In 1898 that spur appears as the FC&P's Eagle Mine Branch: Archer, Montbrook, Standard Junction, Eagle Mine, Williston, Morriston, Early Bird (unit 8). The “Ambler road” is therefore very probably the line through Williston, though the article does not name the town; whether it is the same as the “Archer & Dunnellon” of 1891 (unit 3) these sources do not settle. In this account it is phosphate, not vegetables, that draws the second railroad to Williston."),
]

RATES = [
    u(5, "Railroad Gazetteer 1895, p. 273",
      "WILLISTON, Levy Co. On F C & P R R and S F div of S F & W R R, to Jacksonville 97 m, Pop 200, P O, Ex, Tel, banking town Ocala 25 m, churches, Bapt, Pres and M E, school Att 60, Masonic Lodge; All persons wanting town lots or fine vegetable land will do well to call on or address J B Epperson; terms reasonable",
      "On two roads",
      "Nine years after unit 2: the town is on two railroads, the Florida Central & Peninsular and a division of the Savannah, Florida & Western (the Plant System), and has express and telegraph of its own. Population is given as 200. The entry is an advertisement as much as a description: Epperson is selling town lots and vegetable land."),
    u(6, "Railroad Commission 1898, p. 43",
      "Williston (F C & P) .. Fla 94 17. Williston (Plant System) .. “ 86 14.",
      "Two stations named Williston",
      "From the index of stations: page and station number in the commission's rate tables. The two roads kept a station each; the shipper could choose between them."),
    u(7, "Railroad Commission 1898, pp. 81, 86",
      "Rates on vegetables, oranges and lemons to Jacksonville, Gainesville and High Springs (for beyond). Plant System of Railways. … To High Springs, Fla. (For beyond.) [Station, vegetables per standard crate, oranges and lemons per box:] 11 Archer 10 15. 12 Standard No. 1 10 16. 13 Gunnells 10 16. 14 Williston 10 16. 15 Montbrook 10 16. 16 Morriston 11 16. 17 Romeo 11 16. 18 Juliette 11 16.",
      "The Plant System's rate",
      "Heading from p. 81, rows from p. 86 (plate). The figures are cents; the report speaks of a reduction “of 3 cents per box on vegetables” (unit 10). “For beyond”: for shipments going on past High Springs to markets outside the state."),
    u(8, "Railroad Commission 1898, pp. 91, 94",
      "Rates on vegetables, oranges and lemons to Jacksonville, Fernandina, Yulee and Baldwin (for beyond). Florida Central & Peninsular Railroad. … Eagle Mine Branch. [From, vegetables per crate, oranges and lemons per box:] 13 Archer 10 15. 14 Montbrook 10 16. 15 Standard Junction 11 16. 16 Eagle Mine 11 16. 17 Williston 10 16. 18 Morriston 11 16. 19 Early Bird 11 16.",
      "The Florida Central & Peninsular's rate",
      "Heading from p. 91, rows from p. 94 (plate). From Williston the FC&P charged exactly what the Plant System charged: 10 cents a crate of vegetables, 16 a box of oranges. The rates were set by the state commission, not by the two roads competing. What a shipper could weigh between them was service, cars and connections, which these tables do not show."),
    u(9, "Railroad Commission 1898, p. 12",
      "In making rates for the roads in the State, the Commission adopted the straight mileage basis as being the fairest manner of computing charges for the transportation of freights. This system was in use on some of the roads at the time the Commission was organized, but on others their lines were in divisions, and double rates were charged on freights going from points on one division to points on another. By putting all roads, under the same control or management, on a straight mileage basis as is provided for in Rule No. 1 of the Rules and Regulations of the Commission, the injustice to shippers of paying two or more freights on the same line of road was corrected and it was made possible for them to exchange commodities at reasonable rates.",
      "One freight, not two",
      "Why the rates in units 7 and 8 rise with distance and are the same on both roads: since the commission, freight within Florida was charged by the mile."),
    u(10, "Railroad Commission 1898, pp. 12–13",
      "The reduction of 3 cents per box on vegetables and 4 cents per box on oranges, which has been made by the Commission, will, it is estimated, save to the growers and shippers for the season of 1897–98, from thirty to forty thousand dollars. There is widespread complaint against the transportation companies for excessive rates of freight on fruits and vegetables to Eastern and Western markets. Many growers contend that these rates are destroying the important industry in which they are engaged. There is no question that this complaint is not well founded, but the remedy is not in the power of the State Commission from the fact that it has no control over rates beyond the limits of the State or interstate rates. The Commission will continue its efforts to show to the railroads that proper reductions should be made and that the great industry of fruit and vegetable growing should be protected by rates sufficiently low to enable both producers and transportation lines to get a fair return for their labor.",
      "“Beyond the limits of the State”",
      "“Not well founded”: so printed; the rest of the sentence suggests the commission meant that the complaint was well founded. The state could set the ten cents to High Springs or Jacksonville, but not the charge from there to New York, which for a shipper at Williston was the larger part of the freight."),
]

TOWN = [
    u(11, "Laws of Florida 1905, ch. 5550, p. 870",
      "AN ACT to Amend Section four (4) of Chapter 4657, Laws of Florida, Being An Act to Incorporate the Town of Williston, in the County of Levy, Approved June 2nd, 1897. … Sec. 4. That the first election for municipal officers under this act shall be held on the first Tuesday in July, A. D. 1897, and said election shall be held thereafter on the second Monday in July of each and every year, and at the first election aforesaid, J. B. Peacock, J. P. Reddick and W. M. Barton shall act as inspectors, and H. H. King shall act as clerk. Books for the registration of the names of those qualified to vote at such first election shall be kept open during suitable hours at some convenient point within the corporate limits herein fixed for ten days preceding the day of said election, by the said H. H. King, who is to act as clerk thereof. H. H. King is hereby authorized to require from each person seeking to register an affidavit showing such person to possess the qualifications required by law; and the parties whose names are so registered in said books shall be qualified voters at said election. … Approved May 16, 1905.",
      "A town, 2 June 1897",
      "The act of 1897 itself (chapter 4657) has not yet been found; its date and its first election are known here from this amendment eight years later. The men named are the town's merchants and owners: J. P. Reddick ran a saw mill and crate factory in 1886 and the Williston Hotel in 1895, and was a truck grower in 1907; W. M. Barton kept a general store (directories under units 2, 5 and 13, plates). Who could swear to “the qualifications required by law”, and who was kept from the books, the act does not say; module 5 asks."),
    u(12, "Laws of Florida 1905, ch. 5549, p. 869",
      "AN ACT Declaring the Town of Williston, in Levy County, Florida, to be a Legally Incorporated Town, the Officers Thereof to be Legally Elected and Qualified, and to Declare the Ordinances of Said Town Valid and of Full Force and Effect. Be it Enacted by the Legislature of the State of Florida: Section 1. That the town of Williston, in Levy County, Florida, incorporated under the general laws for incorporating cities and towns in this State, be and is hereby declared a legally incorporated town with all the powers therein, under the laws of the State of Florida. Sec. 2. That all acts and deeds done and performed in the organization and incorporating of said town are declared to be valid and legal in law and in equity, and binding under the laws of this State. Sec. 3. That all the officers elected and qualified and all acts done by and through the Mayor and Town Council, and the other officers of said town, not in conflict with the laws of this State, be and the same are hereby declared legal, valid and of full force and effect. … Approved May 16, 1905.",
      "Made legal after the fact",
      "Passed on the same day as unit 11. The legislature declares valid, after eight years, the town's incorporation, its officers and its ordinances. Why that was needed the act does not say."),
    u(13, "Polk's Gazetteer 1907–1908, p. 452",
      "WILLISTON. Population 200. An incorporated town on the S. A. L. and A. C. L. R. R's., in Levy county, 10 miles southeast of Bronson, the judicial seat, and 128 from Jacksonville. Has Baptist and Methodist Episcopal churches, a public school, a bank, 2 hotels, a saw mill, a crate factory, and a weekly newspaper, The Advocate. Is surrounded by a fertile section of country, devoted mostly to truck farming, and is one of the greatest cucumber districts in the state. Tel., W. U. Exp., Southern. Telephone connection. John Harvey, postmaster. … BANK OF WILLISTON (Capital $15,000), L O Benton Pres, J B Epperson Vice Pres, M H De Land Cashr.",
      "The S. A. L. and the A. C. L.",
      "The two roads now run under the names of the Seaboard Air Line and the Atlantic Coast Line, the large systems into which the Florida Central & Peninsular and the Plant System had passed. Twenty-one years after unit 2 the shipping point is Williston itself, with a bank, a newspaper and a telephone; the directory under the entry has thirty-nine entries for truck growers, two of them firms (plate). The figure of 200 inhabitants is the gazetteer's and is the same as in 1895."),
]

SRC = ("South Publishing Co., Florida State Gazetteer and Business Directory, vol. I, 1886–7 (New York 1886), pp. 65, 458; "
       "Engineering News and American Railway Journal 26 (1891), no. 27, 4 July 1891, p. 20; Manufacturers' Record 23 (1893), no. 22, 30 June 1893, p. 396; "
       "Florida Railroad Gazetteer and State Business Directory 1895 (Atlanta: Cotton States Publishing & Advertising Co.), p. 273; "
       "First Annual Report of the Railroad Commission of the State of Florida, March 1, 1898 (Jacksonville: H. & W. B. Drew 1898), pp. 12–13, 43, 81, 86, 91, 94; "
       "Laws of Florida 1905, chapters 5549 and 5550, pp. 869–870; R. L. Polk & Co.'s Florida Gazetteer and Business Directory 1907–1908 (Jacksonville), p. 452. "
       "Page images: Internet Archive (" + ", ".join(["floridastategaze1886sout", "sim_enr_1891-07-04_26_27", "sim_site-selection_1893-06-30_23_22",
                                                     "floridarailroadg1895beld", "FirstAnnualReportOfTheRailroadCommissionOfTheStateOfFlorida",
                                                     "actsandresoluti03florgoog", "floridagazetteer1907rlpo"]) + "). All in the public domain.")

T = {
    "titel": "Two railroads",
    "autor": "Gazetteers, a railroad journal and a trade paper, the Railroad Commission of Florida, the Laws of Florida",
    "jahr": "1886–1907",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; abbreviations, spelling and punctuation are those of the print. “…” marks an omission; square brackets mark editorial additions, such as column headings of tables. The gazetteers are commercial publications that sold space and printed what towns and merchants sent them; their population figures and descriptions are claims, not counts. What these sources do not contain: the voices of the men who graded and laid the track, of the farm workers who filled the crates, and of Black residents of Williston, who appear nowhere in these entries.",
    "sections": [
        {"id": "archer", "titel": "Eleven miles to Archer (1886)", "zk": "Two railroads",
         "blurb": "In 1886 the railroad ran past Williston. The line from Fernandina to Cedar Key went through Archer and Bronson, and the settlement's cotton, oranges and vegetables went by wagon to Archer, “the shipping point”.",
         "plates": ["map1891_levy", "gaz1886_williston"], "viz": "rails-line", "units": ARCHER},
        {"id": "lines", "titel": "Building the lines (1891–1893)", "zk": "Two railroads",
         "blurb": "Two notices in trade papers: hundreds of men at work on a line south from Archer in 1891, and in 1893 the Plant System's plan to run its own road through the phosphate district, given up for an arrangement with its rival.",
         "plates": ["mr1893_arrangement", "poor1901_plant"], "units": BUILD},
        {"id": "rates", "titel": "Two stations, one rate (1895–1898)", "zk": "Two railroads",
         "blurb": "By 1895 Williston is on two roads. The first report of the state's Railroad Commission lists two stations of that name and, from both, the same freight on a crate of vegetables, and it admits that the larger charge, the one to the markets in the North, is out of its reach.",
         "plates": ["gaz1895_williston", "rrc1898_plant", "rrc1898_fcp"], "viz": "rails-rates", "units": RATES},
        {"id": "town", "titel": "A town on two roads (1897–1907)", "zk": "Two railroads",
         "blurb": "Williston is incorporated in 1897; in 1905 the legislature declares the incorporation lawful after the fact. By 1907 the two lines have new owners and the town is “one of the greatest cucumber districts in the state”.",
         "plates": ["laws1905_williston", "gaz1907_williston"], "units": TOWN},
    ],
}
for s in T["sections"]:
    s["zk"] = "Two railroads, " + s["titel"].split(" (")[0]
(D / "rails.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
NEW = [
    {"id": "map1891_levy", "side": "rail", "titel": "Williston without a railroad, 1891",
     "caption": "Levy County on the “Standard Guide” map of Florida, 1891: the Florida Central & Peninsular runs from Gainesville through Archer and Bronson to Cedar Key; Williston, east of it, has no line yet. Rosewood is a station near the coast.",
     "source": "“Standard Guide” Map of the State of Florida (Buffalo: Matthews-Northrup & Co. for the Jacksonville, Tampa & Key West System, 1891), detail; Library of Congress, Geography and Map Division, 2003627029, via Wikimedia Commons; public domain."},
    {"id": "gaz1886_williston", "side": "town", "titel": "“Archer, the shipping point”",
     "caption": "The Williston entry of 1886, with the lists of growers by acreage.",
     "source": "Florida State Gazetteer and Business Directory, vol. I, 1886–7, p. 458; Internet Archive floridastategaze1886sout (University of Florida); public domain."},
    {"id": "mr1893_arrangement", "side": "rail", "titel": "Traffic arrangements, 1893",
     "caption": "The Plant System gives up its own line through the Albion district for the common use of its rival's spur south of Archer.",
     "source": "Manufacturers' Record 23, no. 22, 30 June 1893, p. 396, column 2; Internet Archive sim_site-selection_1893-06-30_23_22; public domain."},
    {"id": "poor1901_plant", "side": "rail", "titel": "On the Plant System, 1901",
     "caption": "Archer, Williston, Morriston and Juliette on the map of the Plant System in Poor's Manual, 1901 (schematic, detail).",
     "source": "Poor's Manual of the Railroads of the United States 1901, p. 361, detail; via Wikimedia Commons (“1901 Poor's Plant System.jpg”); public domain."},
    {"id": "gaz1895_williston", "side": "town", "titel": "On two roads, 1895",
     "caption": "“On F C & P R R and S F div of S F & W R R”: the Williston entry of 1895, with J. B. Epperson's offer of town lots and vegetable land.",
     "source": "Florida Railroad Gazetteer and State Business Directory 1895, p. 273; Internet Archive floridarailroadg1895beld (University of Florida); public domain."},
    {"id": "rrc1898_plant", "side": "rail", "titel": "The Plant System's rates, 1898",
     "caption": "Rates to High Springs “for beyond”: Williston, station 14, ten cents a crate of vegetables and sixteen a box of oranges.",
     "source": "First Annual Report of the Railroad Commission of the State of Florida (1898), p. 86; Internet Archive FirstAnnualReportOfTheRailroadCommissionOfTheStateOfFlorida (State Library and Archives of Florida); public domain."},
    {"id": "rrc1898_fcp", "side": "rail", "titel": "The FC&P's rates, 1898",
     "caption": "The Eagle Mine Branch of the Florida Central & Peninsular: Williston, station 17, the same ten and sixteen cents.",
     "source": "First Annual Report of the Railroad Commission of the State of Florida (1898), p. 94; Internet Archive FirstAnnualReportOfTheRailroadCommissionOfTheStateOfFlorida; public domain."},
    {"id": "laws1905_williston", "side": "town", "titel": "Incorporated 2 June 1897",
     "caption": "Chapter 5550 of 1905, amending the act to incorporate the town of Williston of 2 June 1897: the first election, its inspectors and the registration of voters.",
     "source": "Laws of Florida 1905, ch. 5550, p. 870; Internet Archive actsandresoluti03florgoog (digitized by Google); public domain."},
    {"id": "gaz1907_williston", "side": "crop", "titel": "“One of the greatest cucumber districts”",
     "caption": "The Williston entry of 1907–1908 and the beginning of its directory: truck growers, the Bank of Williston, The Williston Advocate.",
     "source": "R. L. Polk & Co.'s Florida Gazetteer and Business Directory 1907–1908, p. 452; Internet Archive floridagazetteer1907rlpo (University of Florida); public domain."},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
P["credit"] = ("Photographs from the Seaboard Air Line Railway Shippers Guide (1914) and pages of gazetteers, railroad reports, trade papers and the Laws of Florida "
               "after the page images of the Internet Archive; the “Standard Guide” map of 1891 and the Sanborn fire-insurance maps of Williston, January 1923, from the "
               "Library of Congress (public domain) via Wikimedia Commons; the Plant System map from Poor's Manual (1901) via Wikimedia Commons; photograph of the Acme "
               "Phosphate pit from the Florida Geological Survey Collection, State Archives of Florida, Florida Memory (public domain).")
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "rails"), None) or next(x for x in M["shipped"] if x["id"] == "rails")
M["planned"] = [x for x in M["planned"] if x["id"] != "rails"]
m.update({"datei": "rails", "zk": "Archer · Lines · Rates · Town",
          "kurz": "2 · Two railroads",
          "warum": "In 1886 Williston's shipping point was Archer, eleven miles off. By 1895 the town was on two railroads, which in 1898 charged the same ten cents a crate; it was incorporated in 1897, and in 1905 the legislature declared the incorporation lawful after the fact.",
          "quelle": "Florida State Gazetteer 1886; Engineering News 1891; Manufacturers' Record 1893; Florida Railroad Gazetteer 1895; Railroad Commission of Florida 1898; Laws of Florida 1905; Polk's Gazetteer 1907–1908."})
order = ["before", "rails", "rock", "shipping", "line", "airfield"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "rails"] + [m], key=lambda x: order.index(x["id"]) if x["id"] in order else 99)
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "onerate", "titel": "One rate on two roads",
     "frage": "What did it cost to send a crate of vegetables from Williston in 1898, and did it matter which railroad one chose?",
     "note": "Both tables give Williston the same rates: ten cents a crate of vegetables and sixteen a box of oranges, on the Plant System to High Springs and on the Florida Central & Peninsular to Jacksonville, Fernandina, Yulee or Baldwin, each “for beyond”. The state commission set them by the mile; the charge onward to the northern markets was not in its power.",
     "voices": [{"text": "rails", "sec": "rates", "n": [7], "wer": "Railroad Commission, Plant System table"},
                {"text": "rails", "sec": "rates", "n": [8], "wer": "Railroad Commission, FC&P table"}]},
    {"id": "shippingpoint", "titel": "Where is the shipping point?",
     "frage": "How did the gazetteers describe Williston before and after the railroads?",
     "note": "In 1886 Archer is the shipping point and Williston has one general store; in 1907 Williston is an incorporated town on two railroads, with a bank, two hotels and a newspaper, and “one of the greatest cucumber districts in the state”. Both entries were supplied for commercial directories and read like advertisements; the populations they give, 100 and 200, are claims, not counts.",
     "voices": [{"text": "rails", "sec": "archer", "n": [2], "wer": "Florida State Gazetteer, 1886"},
                {"text": "rails", "sec": "town", "n": [13], "wer": "Polk's Gazetteer, 1907–1908"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
R = "#/text/rails/"
NEWST = [
    {"d": "1886", "side": "rail", "titel": "“Archer, the shipping point”",
     "text": "Williston, population 100 by the gazetteer's count, has one general store, a saw and grist mill and a vegetable crate factory. The nearest railroad, express and telegraph are at Archer, eleven miles off.",
     "cite": R + "archer/2", "citeLabel": "Two railroads [2]", "plate": "map1891_levy",
     "quelle": "Florida State Gazetteer and Business Directory 1886–7, p. 458."},
    {"d": "July 1891", "side": "rail", "titel": "About 350 men on the line from Archer",
     "text": "A trade journal reports about 350 men at work on the railway from Archer to Dunnellon, to be operated by the Florida Central & Peninsular.",
     "cite": R + "lines/3", "citeLabel": "Two railroads [3]",
     "quelle": "Engineering News, 4 July 1891, p. 20."},
    {"d": "June 1893", "side": "rail", "titel": "Traffic arrangements between rivals",
     "text": "The Plant System gives up its own line through the phosphate district near Albion and agrees with the Florida Central & Peninsular on the common use of the spur south of Archer.",
     "cite": R + "lines/4", "citeLabel": "Two railroads [4]", "plate": "mr1893_arrangement",
     "quelle": "Manufacturers' Record, 30 June 1893, p. 396."},
    {"d": "2 June 1897", "side": "town", "titel": "The town of Williston",
     "text": "The act to incorporate the town is approved; the first election is set for the first Tuesday in July. In 1905 the legislature declares the incorporation lawful after the fact.",
     "cite": R + "town/11", "citeLabel": "Two railroads [11]", "plate": "laws1905_williston",
     "quelle": "Laws of Florida 1905, ch. 5550, p. 870, and ch. 5549, p. 869."},
    {"d": "1898", "side": "rail", "titel": "Two stations, one rate",
     "text": "The state's Railroad Commission lists two stations named Williston, one on each road, and the same freight from both: ten cents a crate of vegetables, sixteen a box of oranges. The charge onward to the northern markets is beyond its control.",
     "cite": R + "rates/8", "citeLabel": "Two railroads [8]", "plate": "rrc1898_fcp",
     "quelle": "First Annual Report of the Railroad Commission of the State of Florida (1898), pp. 12–13, 43, 86, 94."},
    {"d": "1907", "side": "crop", "titel": "“One of the greatest cucumber districts”",
     "text": "Williston is an incorporated town on the Seaboard Air Line and the Atlantic Coast Line, with a bank, two hotels, a crate factory and a weekly paper.",
     "cite": R + "town/13", "citeLabel": "Two railroads [13]", "plate": "gaz1907_williston",
     "quelle": "R. L. Polk & Co.'s Florida Gazetteer and Business Directory 1907–1908, p. 452."},
]
titles = {s["titel"] for s in NEWST}
TL["stations"] = [s for s in TL["stations"] if s["titel"] not in titles] + NEWST


MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def year(s):
    """Year, then month; a span of years without a month comes after the dated stations of its first year."""
    d = s["d"]
    m_ = re.search(r"\d{4}", d)
    mon = next((i + 1 for i, x in enumerate(MONTHS) if x in d), 13 if "–" in d else 0)
    return (int(m_.group()) if m_ else 9999, mon, d)


TL["stations"].sort(key=year)
(D / "timeline.json").write_text(json.dumps(TL, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", sum(len(s["units"]) for s in T["sections"]), "units")
