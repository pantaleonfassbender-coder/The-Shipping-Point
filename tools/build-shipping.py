"""Builds data/shipping.json (module 4: The shipping point, 1897–1925) and enters the module in modules.json,
plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/PRUEFUNG.md):
  Ocala Evening Star, 16 June 1897, 12 July 1907, 15 June 1916 (UFDC UF00075908);
  Rice and Geib, Soil Survey of the Gainesville Area, Florida, Field Operations of the Bureau of Soils 1904
    (IA usda-soil-survey-of-the-gainesville-area-florida-1904), pp. 278–279, 286–289;
  Florida's Financial and Industrial Record, Jacksonville, 18 June 1910 (UFDC UF00076685), p. 12;
  Seaboard Air Line Railway, Shippers Guide 1914 (IA seaboardairliner1914seab), pp. 70–71;
  F. M. Cammack, What about Florida? (1916) (IA whataboutflorida00camm), pp. 52–53;
  USDA Bulletin 462, Irrigation in Florida (1917) (IA irrigationinflor462stan), pp. 30–32;
  Lakeland Evening Telegram, 11 and 28 June 1919 (UFDC AA00048605);
  J. E. Turlington and H. G. Hamilton, Factors Affecting Farm Profits in the Williston Area, University of Florida
    Agricultural Experiment Station Bulletin 175 (July 1925) (UFDC UF00026891).
All published before 1931 and in the public domain. The Library of Congress newspaper pages were not used because
the site now sits behind a bot check; the same papers were read in the Florida Digital Newspaper Library (UFDC).
Run from the site root: python tools/build-shipping.py
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


SS = "Soil Survey 1904"
B175 = "Bulletin 175 (1925)"

FIRST = [
    u(1, "Ocala Evening Star, 16 June 1897, p. 1",
      "$20,000 for Cukes. The Star is reliably informed that the section of country tributary to Williston grew 20,000 crates of cucumbers this season, for which the growers received $20,000 net. In consequence the people of that section of Marion county are felicitating themselves on their good fortune.",
      "“$20,000 for Cukes”, 1897",
      "The season in which the town was incorporated (module 2, unit 11), with both railroads in place. A dollar a crate, net, by the paper's information. Williston lies in Levy County; the paper counts the growers of its “tributary” country in Marion County, its own: the shipping point served farms across the county line. Plate."),
    u(2, f"{SS}, pp. 278–279",
      "Before 1895 the orange groves took the time and attention of the farmer, and in many cases were his sole dependence for an income. Since the destruction of the groves more attention has been given to the general farm crops, and corn, potatoes, fruits, and vegetables for home needs have been grown. The greatest advancement, however, has been made in the production of pork for home or local consumption. Peanuts are grown to fatten the hogs, … The principal money crop in the vicinity of Williston is cucumbers. For several years the farmers have made a specialty of this crop, to which the Norfolk sandy loam seems especially well adapted, and large average returns have been secured. It must be kept in mind that this profit is almost clear, as it is made after the home needs have been supplied from the farm. As a result of this system of agriculture, there are few farmers that are not in better circumstances than before the loss of the groves.",
      "“The principal money crop”",
      "A federal soil survey, mapped on the topographic sheet of Williston. The freeze of the winter of 1894–95 had destroyed the orange groves (“before 1895”); cucumbers and hogs fattened on peanuts took their place. The surveyors speak of “the farmers” and their “contentment”; who worked their fields is the subject of unit 3."),
    u(3, f"{SS}, pp. 286–287",
      "The greater number of the farms of the area are worked by the owners. When renting is practiced it is done on shares. When the owner of the farm furnishes one-half the fertilizer, half the stock, and half the implements, the returns are equally divided. When the tenant furnishes everything he usually gets two-thirds or sometimes three-fourths of the returns. Comparatively few of the farms are incumbered, and this is considered an indication of prosperity. In the growing of vegetables more or less speculation is always involved, and on account of a season of low prices or poor management the farmer is frequently obliged to borrow money with which to begin another crop. … The question of labor is an important one, and the farmer is often handicapped in not being able to secure competent help when most needed. Approximately half the population of the area is colored. The average wage by the day is 75 cents. Italian labor has been successfully introduced into some of the phosphate mines, but as yet this has not been tried by the farmers.",
      "75 cents a day",
      "The surveyors write from the farmer's side: labour is a “question”, its supply a handicap. They do not say who the hired hands were; they place the remark that half the population was Black next to the problem of “competent help”. The Gainesville area of the survey reaches from Gainesville to Williston; the figures are for the whole area."),
    u(4, f"{SS}, pp. 288–289",
      "New York, Philadelphia, Baltimore, and Washington furnish a ready market for all the vegetables grown within the area. Agents of the commission houses are kept in the field during the growing season, to deal directly with the farmer. The vegetables are consigned to the commission men, who sell them on a commission of 10 per cent. In order that the vegetables may be put on the market in a fresh condition, they must be crated, carefully and transported safely and quickly. A fancy price must be received if the grower is to make a profit on his crop, for the express rates are high, and the commission, plus the first cost of production, makes the total cost very high. … The transportation facilities of the area are equal to the demands of production. The Cedar Keys division of the Seaboard Air Line and a branch of the Atlantic Coast Line pass through the area and intersect at Gainesville. … Rock-surfaced roads are built out from Gainesville and Micanopy, and between Flemington and Williston, a total distance of 35 miles. The rock used is the limestone found throughout the area. … The county roads are kept in repair by a county road commissioner, who keeps a gang of men continually at work repairing and grading.",
      "Consigned to the commission men",
      "How the trade worked: the grower did not sell his crop; he consigned it to a commission house in a northern city, which sold it and kept a tenth. Price risk and freight stayed with the grower. The two lines of module 2 now appear as the Seaboard Air Line and the Atlantic Coast Line. “Crated, carefully”: so printed."),
    u(5, "Ocala Evening Star, 12 July 1907, p. 2",
      "The Williston Bank. County Commissioner J. M. Mathews yesterday in speaking of good times and the money brought in by the truck crops in the different sections of the county referred to what Dr. Paisley said about the condition of the Williston Bank because of the excellent returns received by the farmers and truckers. He said that in one day nine cars of cucumbers were snipped from Williston and in one week $29,000 were received for the same. That a Mr. Woosly has sent out from the Williston station 106 cars of watermelons and in consequence of the satisfactory returns received for the produce the vaults of the bank were literally bulging with money, in fact they had stacks of it and that it was a difficult thing to shut the doors of the vault they had so much money.",
      "Nine cars in a day, 1907",
      "Hearsay at third hand (a commissioner reporting a doctor's report), and so the figures should be read; “snipped” is a misprint for “shipped”. The Bank of Williston of module 2 (unit 13) is the measure of the season. Plate."),
]

TRAIN = [
    u(6, "Florida's Financial and Industrial Record, 18 June 1910, p. 12",
      "Big Crops of “Cukes.” The Ocala Star tells in a most interesting way of the cucumber crop and its handling in the neighborhood of Williston. It seems that nearly 300 acres have been planted in that section, without irrigation, and about 135 acres irrigated. One grower is mentioned who had 84 acres of “cukes” and another with ten acres, both of whom made an excellent showing. Williston was shipping 22 cars of cucumbers a day during the height of the season, which has now about passed. This is one of the truck crops that brings ready money into Florida.",
      "Twenty-two cars a day, 1910",
      "A Jacksonville business paper summarizing the Ocala Star; the original report has not yet been found. About 435 acres, a third of them irrigated (unit 10 describes the irrigation plants). Plate."),
    u(7, "Seaboard Air Line Railway, Shippers Guide 1914, pp. 70–71",
      "[Caption of two photographs, p. 70:] The cultivation of cucumbers requires a small amount of labor and little expense; they find a ready market and good profits are realized from this industry in Florida on the S. A. L. Ry. 1. A field of cucumbers. 2. The harvest. … [p. 71:] At Williston is located the greatest cucumber industry in the State of Florida and the production of cabbage is also enormous. This product is shipped from here over the Seaboard Air Line Railway by the trainload to the great northern and western markets. One of these trains is featured by a cut made from a photograph and inserted herein for the purpose of giving prospective settlers an idea of the magnitude of this industry.",
      "“A small amount of labor and little expense”",
      "The railroad's guide was written to bring settlers and freight to its line. The photographs on p. 70 are not located; those on p. 71 are captioned “Cucumber industry at Williston” and show people at work in the field and at the hampers (plates). The claim of little labour is the railroad's; the survey of 1923 found labour the largest single expense (unit 15)."),
    u(8, "Ocala Evening Star, 15 June 1916, p. 2",
      "Williston and Oak Vale. Williston, June 14—After two years of failure, the early vegetable raisers are enjoying a prosperous year again in the section for which Williston is the shipping point. Cucumbers, for the growing of which Williston has become famous, have been leaving in large quantities and still continue to bring fair prices. … Dan Warren, while standing on a wagon loaded with cucumbers near the packing house on the McKennon farm was struck and instantly killed by lightning. The team drawing the load was also killed.",
      "“The section for which Williston is the shipping point”",
      "The sentence that gives this apparatus its title, thirty years after Archer was “the shipping point” for Williston (module 2, unit 2). Two years of failure, 1914 and 1915: the paper does not say why. Dan Warren, who died hauling the crop to the packing house, is one of the few people at work whom these sources name. Plate."),
    u(9, "Cammack, What about Florida? (1916), pp. 52–53",
      "Twenty miles to the Southwest is Williston, which might commonly be known as a water-tank station, were it not for “cukes.” The cucumber has put Williston on the map. Carrying cucumbers to Williston would be the equivalent of carrying coals to New Castle. The world likes cucumbers, especially when they are high-priced, and it pays a fancy price for them in the early spring. The growers around Williston have a congenial soil and a favorable climate for raising cucumbers in quantities—hence it is that the demand in the Northern market finds supply in Levy County, and while the gales of March are sweeping over the barren fields of the North, the Williston trucker is imitating the busy little bee from early morn till dewy eve, and with jealous care, coaxing his coming crop. In April and May the crating and shipping begin, and buyers throng the local depot platform. Fifty-seven thousand crates of “cukes” have left this one station in a single season. Small wonder, then, that King “Cuke” is held in great reverence.",
      "“The cucumber has put Williston on the map”",
      "A promotional book on Florida. The season of the 57,000 crates is not named. “Buyers throng the local depot platform”: by 1916 some of the crop was sold at the station, not only consigned (unit 4). The same page of the book describes Black workers on a river steamer in the racist language of its day; that passage is not printed here."),
    u(10, "USDA Bulletin 462, Irrigation in Florida (1917), pp. 30–32",
      "The above system is in operation on about 150 acres within a few miles of Williston, in the north-central part of the State. The plants are mostly small, usually irrigating not more than 10 acres, one plant which irrigates 55 acres being an exception. … The owner burns wood, which is plentiful in this section. … Cucumbers are the principal crop grown in the Williston section. There is much controversy concerning the effect of spray irrigation upon this crop, although all the systems were installed for the purpose of watering cucumbers. Some of the farmers owning irrigation plants are very much opposed to spraying cucumbers, claiming that the water applied on the leaves by the spray systems materially increases blight or rust. Many owners are willing to sell their systems at a great sacrifice. … The trucking section in Sumter County is considerably larger than that in Levy County. … the disastrous droughts of 1907–1910 were the direct cause of the installation of most of the plants.",
      "Overhead pipes and steam pumps",
      "The federal irrigation engineers found the Williston growers divided over their own investment. By 1923 none of the eleven plants among the 120 farms surveyed was working (unit 13)."),
]

SEASON = [
    u(11, "Lakeland Evening Telegram, 11 June 1919, p. 2",
      "Review of Florida Vegetable Situation. … (New York Packer.) Jacksonville, Fla., June 11.—Florida is shipping vegetables daily on a heavy carlot basis. … Cucumbers are moving from Williston and points further north. Last week evidently saw the height of the cucumber movement and this week the movement is much lighter. The output last week from May 23 to May 29 inclusive was from 13 to 20 cars daily, and up to June 1 Williston had shipped more than 150,000 hampers. All of last week cars had been moving over the Atlantic Coast Line from Williston alone in mostly solid train loads.",
      "Thirteen to twenty cars a day, 1919",
      "From the New York trade paper of the produce business, reprinted in Lakeland and, a week later, in the Miami Daily Metropolis. The peak lasted about a week. In 1914 it was the Seaboard that advertised the trainloads (unit 7); in 1919 they ran on the Atlantic Coast Line. The reports count in hampers (baskets) and in crates; whether they meant the same package is not clear. Plate."),
    u(12, "Lakeland Evening Telegram, 28 June 1919, p. 6",
      "Williston shipped over 200,000 crates of cucumbers this season. A plan is under way to establish a pickle factory at that place Heinze, who died recently, started his great canning industry with pickles, and left an estate of $7,000,000. Williston should have a pickle factory.",
      "Over 200,000 crates",
      "Ten times the crates of 1897 (unit 1). Whether the pickle factory was built is not known from these sources. “At that place Heinze”: so printed; H. J. Heinz had died in May 1919."),
]

FARMS = [
    u(13, f"{B175}, pp. 4–5",
      "A business analysis of 120 farms for the year 1923 in the vicinity of Williston was secured. With a prepared questionnaire each farm was visited during January and February 1924, and a record of the farm business was obtained from the operator. … Of the 120 farms studied, 11 at one time maintained irrigation plants. But none of these plants were operated at the time of this survey. … Contractor—One who furnishes seed, fertilizer, spray material, one half the containers and sometimes land to the farmer. He gets in return one half the gross receipts of the crop. … Thirty-nine percent of these farms made a minus labor income, 19 percent made an average labor income of minus $1,350 and 20 percent made an average labor income of minus $180. Sixty-one percent of the farms made plus labor incomes; 16 percent made an average labor income of $168; 18 percent, $507; 13 percent, $1,116; and 14 percent $5,512.",
      "120 farms, 1923",
      "The first farm business survey of the Florida College of Agriculture (plate: the cover). The “contractor” financed the crop in return for half its gross proceeds; the survey counts the farm as if the farmer had paid everything himself. In 1923 almost two farms in five lost money on the year; one in seven averaged $5,512. The farm operators were interviewed; the hands they hired were not asked."),
    u(14, f"{B175}, p. 8",
      "Cucumbers furnished 72.3 percent of the receipts, or about 25 times as much as any other crop, and more than seven times as much as livestock. Most of the farmers apparently grew about all the cucumbers that they could care for and then grew what other crops they could. The greater part of the labor on cucumbers was done from January to May, about half of it coming the last of April and first of May when the crop was harvested. The amount of cucumbers the farmer was able to harvest determined largely how many cucumbers he grew.",
      "72.3 percent",
      "The town lived on one crop. The harvest came in two or three weeks at the turn of April and May, and how much a farmer grew depended on how much he could harvest (graphic)."),
    u(15, f"{B175}, pp. 10–11",
      "Expenses. The distribution of expenses is shown in Table 5. Labor was the biggest item of expense and constituted about one-third of the total. The labor was composed of day labor, family labor, contract labor and cropper labor; in addition to this the operator on the average valued his labor at $251 per year. Day labor was the most important, 80 percent of the farmers employing day labor. Forty-five percent had contract labor which was used mostly in picking cucumbers. Share-cropper labor was less popular in this area and only 27 percent of the farmers employed this type. Seventy-one percent had labor done by the family in addition to the operator. … Table 5.—Distribution of Expense and Percent of Farms Having Each Item of Expense. [Expense, percent of farms having this expense, expense per farm in dollars, percent of total:] Family labor 71.7, 133, 7.8. Day labor 80.8, 225, 13.1. Contract labor 45.0, 104, 6.1. Cropper labor 26.8, 117, 6.8. Total labor 97.3, 579, 33.8. Fertilizer 93.3, 394, 23.0. … Containers 90.0, 154, 9.0. … Total 1712, 100.0.",
      "Day labor, contract labor, croppers",
      "The only source of this module that counts the people who did the work, and only as costs. It does not say who they were. Day labourers, pickers hired by contract and sharecroppers are the hands of units 3, 7 and 11; whether they were Black or white, local or migrant, how much they earned a day and where they lived, the survey does not record, and no source found so far does. Compare unit 7."),
]

SRC = ("Ocala Evening Star, 16 June 1897, p. 1; 12 July 1907, p. 2; 15 June 1916, p. 2. Rice and Geib, Soil Survey of the Gainesville Area, Florida, in: Field Operations of the "
       "Bureau of Soils, 1904 (Washington 1905), pp. 278–279, 286–289. Florida's Financial and Industrial Record (Jacksonville), 18 June 1910, p. 12. Seaboard Air Line Railway, "
       "Shippers Guide 1914, pp. 70–71. F. M. Cammack, What about Florida? (1916), pp. 52–53. U.S. Department of Agriculture Bulletin 462, Irrigation in Florida (1917), pp. 30–32. "
       "Lakeland Evening Telegram, 11 June 1919, p. 2, and 28 June 1919, p. 6. J. E. Turlington and H. G. Hamilton, Factors Affecting Farm Profits in the Williston Area, University "
       "of Florida Agricultural Experiment Station Bulletin 175 (July 1925), cover and pp. 4–5, 8, 10–11. Page images: University of Florida Digital Collections (UF00075908, "
       "UF00076685, AA00048605, UF00026891) and Internet Archive (usda-soil-survey-of-the-gainesville-area-florida-1904, seaboardairliner1914seab, whataboutflorida00camm, "
       "irrigationinflor462stan). All in the public domain.")

T = {
    "titel": "The shipping point",
    "autor": "Florida newspapers, federal soil and irrigation surveys, a railroad's shippers guide, a promotional book and the Florida Agricultural Experiment Station",
    "jahr": "1897–1925",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print, misprints included and named. “…” marks an omission; square brackets mark editorial additions. Newspaper figures are often reported at second or third hand and are given as the papers gave them. The pages of Chronicling America (Library of Congress) could not be used, as the site now sits behind a bot check; the same newspapers were read in the Florida Digital Newspaper Library of the University of Florida. The figure of “seventy-five carloads a day” is not in any source of the time found so far (Texts, “Examined and not included”). The people who picked, packed and loaded the crop speak nowhere in these sources.",
    "sections": [
        {"id": "first", "titel": "The first cars (1897–1907)",
         "blurb": "In the first seasons after the railroads the cucumbers began to leave by the crate, consigned to commission men in New York and the other cities of the East. A federal soil survey called them the principal money crop, and a county commissioner told of a bank vault too full to close.",
         "plates": ["oes1897_cukes", "oes1907_bank"], "viz": "shipping-numbers", "units": FIRST},
        {"id": "trainload", "titel": "By the trainload (1910–1917)",
         "blurb": "Twenty-two cars a day in 1910, a railroad's boast of “the greatest cucumber industry in the State” in 1914, and in 1916 the sentence that names this apparatus: “the section for which Williston is the shipping point”.",
         "plates": ["sal1914_labor", "sal1914_cucumbers", "sal1914_trainload", "fir1910_cukes", "oes1916_shipping"], "units": TRAIN},
        {"id": "season", "titel": "The season of 1919",
         "blurb": "One season seen from the produce trade: thirteen to twenty cars a day at the peak, solid trains on the Atlantic Coast Line, and over 200,000 crates by the end of June.",
         "plates": ["let1919_review"], "units": SEASON},
        {"id": "farms", "titel": "Who did the work (1923)",
         "blurb": "In 1923 the state's agricultural college surveyed 120 farms around Williston. Cucumbers brought nearly three quarters of their income; labour was their largest expense, paid to day labourers, contract pickers and sharecroppers whom the survey counts but does not describe.",
         "plates": ["b175_cover"], "viz": "shipping-farms", "units": FARMS},
    ],
}
for s in T["sections"]:
    s["zk"] = "The shipping point, " + s["titel"].split(" (")[0]
(D / "shipping.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
UF = "University of Florida Digital Collections (Florida Digital Newspaper Library)"
NEW = [
    {"id": "oes1897_cukes", "side": "crop", "titel": "“$20,000 for Cukes”, 1897",
     "caption": "Twenty thousand crates from the country around Williston in the first season after the railroads came.",
     "source": "Ocala Evening Star, 16 June 1897, p. 1; " + UF + ", UF00075908; public domain."},
    {"id": "oes1907_bank", "side": "crop", "titel": "“The Williston Bank”, 1907",
     "caption": "Nine cars of cucumbers in one day and a vault too full to close, as a county commissioner told it.",
     "source": "Ocala Evening Star, 12 July 1907, p. 2; " + UF + ", UF00075908; public domain."},
    {"id": "fir1910_cukes", "side": "crop", "titel": "Twenty-two cars a day, 1910",
     "caption": "“Big Crops of ‘Cukes’”: about 435 acres around Williston, a third of them irrigated.",
     "source": "Florida's Financial and Industrial Record, Jacksonville, 18 June 1910, p. 12; " + UF + ", UF00076685; public domain."},
    {"id": "sal1914_labor", "side": "crop", "titel": "“A small amount of labor”",
     "caption": "The railroad's photographs of a cucumber field and of the harvest, with people at work among the hampers; the place is not named.",
     "source": "Seaboard Air Line Railway, Shippers Guide 1914, p. 70; Internet Archive seaboardairliner1914seab; public domain."},
    {"id": "oes1916_shipping", "side": "crop", "titel": "“The shipping point”, 1916",
     "caption": "The Williston and Oak Vale column of 15 June 1916: the sentence that names this apparatus, and the death of Dan Warren at the packing house.",
     "source": "Ocala Evening Star, 15 June 1916, p. 2; " + UF + ", UF00075908; public domain."},
    {"id": "let1919_review", "side": "crop", "titel": "The season of 1919",
     "caption": "“Review of Florida Vegetable Situation”, after the New York Packer: thirteen to twenty cars a day from Williston.",
     "source": "Lakeland Evening Telegram, 11 June 1919, p. 2; " + UF + ", AA00048605; public domain."},
    {"id": "b175_cover", "side": "crop", "titel": "A cucumber field near Williston, about 1924",
     "caption": "“Cucumbers are one of the main crops in the Williston area”: the cover of the farm business survey of 1925.",
     "source": "Turlington and Hamilton, Factors Affecting Farm Profits in the Williston Area, University of Florida Agricultural Experiment Station Bulletin 175 (July 1925), cover, fig. 57; University of Florida Digital Collections, UF00026891; public domain."},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
P["credit"] = ("Photographs from the Seaboard Air Line Railway Shippers Guide (1914), from U.S. Geological Survey Bulletin 604 (1915) and from Florida Agricultural Experiment Station "
               "Bulletin 175 (1925); pages of gazetteers, railroad and geological reports, the state's reports on its convicts, trade papers and the Laws of Florida after the page images "
               "of the Internet Archive; newspaper pages from the Florida Digital Newspaper Library, University of Florida Digital Collections; the “Standard Guide” map of 1891 and the "
               "Sanborn fire-insurance maps of Williston, January 1923, from the Library of Congress (public domain) via Wikimedia Commons; the Plant System map from Poor's Manual (1901) "
               "via Wikimedia Commons; photograph of the Acme Phosphate pit from the Florida Geological Survey Collection, State Archives of Florida, Florida Memory (public domain).")
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "shipping"), None) or next(x for x in M["shipped"] if x["id"] == "shipping")
M["planned"] = [x for x in M["planned"] if x["id"] != "shipping"]
m.update({"datei": "shipping", "zk": "First cars · Trainload · 1919 · Who did the work",
          "kurz": "4 · The shipping point",
          "warum": "Cucumbers from 20,000 crates in 1897 to over 200,000 in 1919, nine to twenty-two cars a day, consigned to commission men in the North. In 1923 they brought nearly three quarters of the farms' income; the work was done by day labourers, contract pickers and sharecroppers whom no source names.",
          "quelle": "Ocala Evening Star 1897–1916; USDA Soil Survey 1904; Florida's Financial and Industrial Record 1910; SAL Shippers Guide 1914; Cammack 1916; USDA Bulletin 462 (1917); Lakeland Evening Telegram 1919; Florida Experiment Station Bulletin 175 (1925)."})
order = ["before", "rails", "rock", "shipping", "line", "airfield"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "shipping"] + [m], key=lambda x: order.index(x["id"]) if x["id"] in order else 99)
for x in M.get("missing", []):
    if x["id"] == "seventyfive":
        x.update({"warum": "A figure found only in recent accounts of Williston's cucumber trade, for example as something “reportedly” shipped in the 1920s (Levy County Journal, 26 October 2006). No source of the time carrying it has been found. The period figures are nine cars in a day (1907), twenty-two cars a day at the height of the season (1910) and thirteen to twenty cars daily (1919); a local history of 1983 gives seventeen. Recent texts are under copyright and are cited, not printed.",
                  "quelle": "Levy County Journal, 26 Oct. 2006; Search for Yesterday, ch. 13 (Levy County Archives Committee, 1983), both in the University of Florida Digital Collections."})
if not any(x["id"] == "cuke1930s" for x in M.get("missing", [])):
    M["missing"].append({"id": "cuke1930s", "side": "crop", "kurz": "The cucumber surveys of 1928–1932",
                         "warum": "The Experiment Station followed Bulletin 175 with “Factors Affecting Cucumber Yields, Costs, and Profits: A Study of the Williston Area, Florida, for 1923, 1928, 1930 and 1932”. Published after 1930, its copyright status has to be checked before anything is printed from it.",
                         "quelle": "University of Florida Agricultural Experiment Station, 1930s."})
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "labor", "titel": "“A small amount of labor”",
     "frage": "How much work did the cucumbers take, and whose?",
     "note": "The railroad told prospective settlers in 1914 that cucumbers required “a small amount of labor and little expense”. The agricultural college's survey of the 1923 season found labour the largest single expense of the farms around Williston, a third of the total, paid to day labourers, contract pickers and sharecroppers. Neither source says who these workers were.",
     "voices": [{"text": "shipping", "sec": "trainload", "n": [7], "wer": "Seaboard Air Line, 1914"},
                {"text": "shipping", "sec": "farms", "n": [15], "wer": "Experiment Station, 1925"}]},
    {"id": "carsaday", "titel": "How many cars a day?",
     "frage": "How many carloads of cucumbers left Williston in a day?",
     "note": "Nine in one day by hearsay in 1907; twenty-two a day at the height of the 1910 season; thirteen to twenty a day in the peak week of 1919, by the produce trade's count. The “seventy-five carloads a day” of recent accounts has no source of the time.",
     "voices": [{"text": "shipping", "sec": "first", "n": [5], "wer": "Ocala Evening Star, 1907"},
                {"text": "shipping", "sec": "trainload", "n": [6], "wer": "Financial and Industrial Record, 1910"},
                {"text": "shipping", "sec": "season", "n": [11], "wer": "New York Packer, 1919"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/shipping/"
NEWST = [
    {"d": "June 1897", "side": "crop", "titel": "“$20,000 for Cukes”",
     "text": "In the season of 1897 the country around Williston grows 20,000 crates of cucumbers, worth $20,000 net to the growers.",
     "cite": K + "first/1", "citeLabel": "The shipping point [1]", "plate": "oes1897_cukes",
     "quelle": "Ocala Evening Star, 16 June 1897, p. 1."},
    {"d": "1904", "side": "crop", "titel": "“The principal money crop”",
     "text": "A federal soil survey finds that “the principal money crop in the vicinity of Williston is cucumbers”; peanuts are grown to fatten hogs, and the orange groves were lost in 1895. Day wages in the area are 75 cents.",
     "cite": K + "first/2", "citeLabel": "The shipping point [2]",
     "quelle": "Rice and Geib, Soil Survey of the Gainesville Area, Florida, in: Field Operations of the Bureau of Soils, 1904, pp. 278, 287."},
    {"d": "July 1907", "side": "crop", "titel": "Nine cars in one day",
     "text": "A county commissioner tells of nine cars of cucumbers shipped from Williston in one day and $29,000 received in a week.",
     "cite": K + "first/5", "citeLabel": "The shipping point [5]", "plate": "oes1907_bank",
     "quelle": "Ocala Evening Star, 12 July 1907, p. 2."},
    {"d": "June 1910", "side": "crop", "titel": "Twenty-two cars a day",
     "text": "At the height of the season Williston ships 22 cars of cucumbers a day, from about 435 acres.",
     "cite": K + "trainload/6", "citeLabel": "The shipping point [6]", "plate": "fir1910_cukes",
     "quelle": "Florida's Financial and Industrial Record, 18 June 1910, p. 12."},
    {"d": "1914", "side": "crop", "titel": "“The greatest cucumber industry”",
     "text": "The Seaboard Air Line's guide for shippers and settlers prints a photograph of a “solid trainload of cucumbers leaving Williston … destined to eastern markets”.",
     "cite": K + "trainload/7", "citeLabel": "The shipping point [7]", "plate": "sal1914_trainload",
     "quelle": "Seaboard Air Line Railway, Shippers Guide 1914, pp. 70–71."},
    {"d": "June 1916", "side": "crop", "titel": "“The shipping point”",
     "text": "“After two years of failure” the growers prosper again “in the section for which Williston is the shipping point”. Dan Warren is killed by lightning on a wagon of cucumbers at a packing house.",
     "cite": K + "trainload/8", "citeLabel": "The shipping point [8]", "plate": "oes1916_shipping",
     "quelle": "Ocala Evening Star, 15 June 1916, p. 2."},
    {"d": "June 1919", "side": "crop", "titel": "Over 200,000 crates",
     "text": "Thirteen to twenty cars a day leave Williston in the peak week, mostly in solid trains on the Atlantic Coast Line; by the end of June the season's count is over 200,000 crates.",
     "cite": K + "season/11", "citeLabel": "The shipping point [11]", "plate": "let1919_review",
     "quelle": "Lakeland Evening Telegram, 11 and 28 June 1919."},
    {"d": "1923", "side": "crop", "titel": "Three quarters from one crop",
     "text": "On 120 farms around Williston cucumbers bring 72.3 percent of all receipts; labour is the largest expense, paid to day labourers, contract pickers and sharecroppers; two farms in five lose money.",
     "cite": K + "farms/15", "citeLabel": "The shipping point [15]", "plate": "b175_cover",
     "quelle": "Turlington and Hamilton, Bulletin 175 (1925), pp. 5, 8, 10–11."},
]
OLD = {"“The principal money crop”", "“The greatest cucumber industry”", "Cucumbers by the trainload"}
titles = {s["titel"] for s in NEWST} | OLD
TL["stations"] = [s for s in TL["stations"] if s["titel"] not in titles] + NEWST
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def year(s):
    d = s["d"]
    m_ = re.search(r"\d{4}", d)
    mon = next((i + 1 for i, x in enumerate(MONTHS) if x in d), 13 if "–" in d else 0)
    return (int(m_.group()) if m_ else 9999, mon, d)


TL["stations"].sort(key=year)
(D / "timeline.json").write_text(json.dumps(TL, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", sum(len(s["units"]) for s in T["sections"]), "units")
