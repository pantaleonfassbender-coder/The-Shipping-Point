"""Builds data/rock.json (module 3: Hard rock, 1893–1920) and enters the module in modules.json,
plates.json, timeline.json and compare.json.

Sources, each passage read against the page image of the Internet Archive (log: ../quellen/PRUEFUNG.md):
  Manufacturers' Record 23/22, 30 June 1893 (sim_site-selection_1893-06-30_23_22), p. 396;
  Reports of the Commissioner of Agriculture of the State of Florida for 1893–1894 (…ForPeriod_33), pp. 67, 81,
    83–85; for 1895–1896 (…ForPeriod_604), p. 81; for 1899–1900 (…ForPeriod_614), pp. 47–48; for 1901–1902
    (…ForPeriod_570), pp. 51, 57;
  G. C. Matson, The Phosphate Deposits of Florida, U.S. Geological Survey Bulletin 604 (1915)
    (phosphatedeposi00matsgoog; plates after IA41522103_0102), pp. 9, 90–92, plates II, III, XVII;
  Florida Geological Survey, Seventh Annual Report (1915), pp. 20–22; Tenth and Eleventh Annual Reports (1918),
    pp. 105–106; Fourteenth Annual Report (1922), pp. 29–30.
All in the public domain (works of the United States government; Florida state publications before 1931; trade
paper of 1893).
Run from the site root: python tools/build-rock.py
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


CA = "Commissioner of Agriculture"

BELT = [
    u(1, "Manufacturers' Record, 30 June 1893, p. 396",
      "To make a summary of the business for the half year, we find from the various ports, the tonnage for the last two weeks of June being approximated, as follows: [Tons:] Fernandina 60,000. Port of Tampa 49,000. Punta Gorda 24,681. Savannah 11,322. Total 145,003. With the shipments from Brunswick, returns of which are not to hand, and the tonnage to the interior by rail, the output will reach over 160,000 tons. Of these amounts the shipments from Fernandina all were foreign; from Tampa but very little was taken by the home market; Punta Gorda shipped one-eighth to home ports and seven-eighths across the ocean; all of Savannah's shipments were foreign; all of the rock from Brunswick were steamer cargoes and found foreign markets, leaving about an eighth or perhaps a seventh of the output to be consumed by the home markets. These facts are significant and call for serious thought. Here the bulk of the output of Florida is going to Europe, and under a steady demand and an advancing market. …",
      "“Going to Europe”",
      "From the trade report “The Florida Phosphate Trade for the Half Year”, dated Orlando, 26 June 1893, on the same page as the railroad notice of module 2 (unit 4). Florida's phosphate went to the fertilizer works of Europe; the ports were Fernandina, Tampa, Punta Gorda, Savannah and Brunswick. Twenty years later almost all hard rock was still exported (unit 16); that dependence is what broke in 1914."),
    u(2, "Matson, Bulletin 604 (1915), p. 9",
      "The rock-phosphate region, where mining has been most active, forms a narrow belt beginning in southeastern Suwannee and southern Columbia counties and extending southeastward to High Springs, where it bends southward across western Alachua and Marion and eastern Citrus and Hernando counties. Many active mines are located along Barr's tramroad, a few miles west of the Atlantic Coast Line Railroad, extending from a point near Clark southward beyond Newberry. The number of mines decreases southward toward Archer, and mining has been discontinued at Albion, in Levy County. The Early Bird and Eagle mines were long ago abandoned, but two mines are in operation near Standard and one near Juliette, in western Marion County. Dunnellon, in southwestern Marion County, is an important center of rock-phosphate mining, several mines being located near that place on terraces bordering Withlacoochee River and others on a terrace bordering the west side of Tsala Apopka Lake.",
      "“Long ago abandoned”",
      "The federal survey of 1915 (plate: map of the deposits). Early Bird and Eagle Mine were stations on the line through Williston in 1898 (module 2, unit 8); Standard and Juliette lie on the same spur. By 1915 the pits nearest Williston had been worked out or given up; the belt's centre lay to the north, along Barr's tramroad, and south, at Dunnellon. Morriston's Acme pit (units 16–18) is not named here."),
]

LEASED = [
    u(3, f"{CA} 1893–1894, p. 67",
      "The present contractors have sub-let part of the convicts each receives, and they are worked at the following places: Hon. E. B. Bailey has about twenty-five at work near Fort White, Columbia county, in the mining of phosphate; he has about 160 near Albion, Levy county, these also mine phosphate, and do other work incidental to mining; he has sub-let about fifty men to H. F. Dutton & Co., who work them in phosphate mines near Lexington, Alachua county. T. G. and J. A. Cranford have the convicts leased by them at work as follows: Baird & Frazier work about thirty-six men in the manufacture of naval stores near Guilford, Bradford county; Knight & Hillman work about seventy near Osceola, Alachua county, in the manufacture of naval stores. They work forty-four convicts in the manufacture of naval stores near Oxford, Sumter county, and they have sub-let about fifteen men to Colonel H. L. Morris, of Morriston, Levy county; these also manufacture naval stores. … The convict camps are in charge of sober, reliable and humane men.",
      "About 160 near Albion",
      "Florida leased the prisoners of its state prison to private contractors, who paid the state a fixed sum a year and could sublet them (the same page: $21,000 a year). The Commissioner of Agriculture was responsible for the state prison, which is why these reports are in an agricultural series. H. F. Dutton & Co. of Gainesville, who worked fifty leased men in their mines, are the bankers named for Williston in 1886 (module 2, unit 2). The last sentence is the department's own judgement; units 5 and 7 put it to the test."),
    u(4, f"{CA} 1893–1894, p. 81",
      "Table No. 17. Showing Color, Sex, Education and Religion of all Convicts on Hand December 31, 1894. White females 2. White males 83. Colored females 17. Colored males 512. Total 614. Number of convicts that can read 366. Number of convicts that cannot read 248. …",
      "512 of 614",
      "More than five in six of the state's prisoners were Black (plate). How Black men and women came to fill the convict camps of the 1890s, through the courts and laws of the time, is a question for module 5; the table records only the result."),
    u(5, f"{CA} 1893–1894, pp. 83–84",
      "Report of Chaplain. Herlong, Fla., January 3, 1895. … You ask me to make a report on each camp separately. … E. B. Bailey's in Levy county: General condition, good; spiritual, good; mental and physical, good. Morris' in Levy county: General condition, bad; spiritual, poor; mental, medium; physical, good. I will say in conclusion, that the convicts have been well fed and clothed and cared for, so far as my general observation goes. … Respectfully yours, V. A. Herlong.",
      "“General condition, bad”",
      "The state prison chaplain visited the eleven camps every eight weeks. Of the two in Levy County, Bailey's phosphate camp near Albion and Morris's turpentine camp at Morriston, he found the second in bad condition, without saying why. The chaplain's report is the nearest these volumes come to an outside view of the camps; the prisoners themselves are not heard."),
    u(6, f"{CA} 1893–1894, p. 85",
      "Reports as to Health of Convicts. Albion, Fla., January 18, 1895. Hon. L. B. Wombwell, Tallahassee, Florida: Dear Sir—In reply to your inquiry in reference to the health of the convicts under my charge, I am glad to report that the health of my camp for 1894 has been most excellent; quite a contrast to the camp at Ichtucknee, which was surrounded by swamps. I attribute the good health to the good water we have in the sand hills and pine forest of Levy county. Yours truly, E. B. Bailey.",
      "Bailey, January 1895",
      "The lessee reports on his own camp, at the commissioner's request. Compare unit 7, written two years later."),
    u(7, f"{CA} 1895–1896, p. 81",
      "Report of Hon. E. B. Bailey. Albion, Fla., Jan. 15th, 1897. Hon. L. B. Wombwell, Tallahassee, Fla.: Dear Sir—The health of the camp for the past two years has been excellent, and I would state that owing to the fact that the penitentiary seems to be a dumping ground for men likely to prove a burden on the charitable institutions of the State, that the death list and sick reports from all the camps show very well. In 1895 the death roll was twenty one, two of whom were killed trying to escape, two by accident, one by being killed by a fellow convict, one by suicide, three by syphilis, and the remainder from the ordinary diseases that human flesh is heir to. In 1896 nineteen deaths are reported, one by being killed by sheriff in arresting after escape, two by accident, six from consumption, and the remainder from ordinary diseases. In many cases men are sent here in the last stages of disease, some afflicted with mental disorders, others not thirteen years of age, and others absolutely inadequate for work. This seems especially the case from counties who have chain gangs. I am, Yours truly, E. B. Bailey.",
      "Forty dead in two years",
      "Written at Albion by the lessee himself (plate). Whether the twenty-one and nineteen deaths are those of his own camps or of all the state's camps the letter leaves open (“the death list and sick reports from all the camps”). Three men were killed while escaping or being recaptured. Bailey calls the health “excellent” in the same letter, and he blames the dead on the counties that sent them. Children under thirteen were sent to the camps; he names it as a burden on the lessee, not as a wrong. None of the dead is named."),
    u(8, f"{CA} 1899–1900, p. 47",
      "State Prison. All persons convicted of offenses in the County Criminal Courts of Record and in the several Circuit Courts of the State of Florida, and sentenced to confinement at hard labor in the State prison were leased under contract made May 22d, 1897, under Act of Legislature of 1897, from January 1st, 1898, for four years, by the State Board of Commissioners of State Institutions to Messrs. A. H. West, Madison, Fla.; R. J. Knight, Crystal River, Fla.; S. L. Varnadoe, Winn, Fla., and W. N. Camp, Albion, Fla. These parties are required to take all persons sentenced by the different courts of Florida to imprisonment at hard labor in the State prison. The prisoners are taken at the various county jails and the State is at no expense for such prisoners after sentence is pronounced, each contractor giving bond for five thousand dollars for the faithful performance of his contract, and agreeing to pay to the State Treasurer, annually, the sum of five thousand, two hundred and fifty dollars, payable on the 1st days of January and July of each year, being a total of twenty-one thousand dollars per year. The prisoners have been worked during the past two years in the mining of phosphate and the manufacture of naval stores, by the different contractors and their sub-contractors. … The convict camps are located as follows: In Alachua, one at Wade, two at Dutton, Fla.; Bradford county, one at Lawtey, Fla.; Citrus county, two at Floral City, Fla.; two at Cordeal, Fla.; Hernando county, one at Brooksville, Fla.; Marion county, one at Romeo, Fla.; one at Summerfield, Fla.; Levy county, one at Elliston, Fla.; Washington county, one at Tompkins, Fla.",
      "“The State is at no expense”",
      "One of the four lessees of 1898–1901, W. N. Camp, wrote from Albion. Each paid $5,250 a year for all the prisoners he took; the state saved their keep. Elliston is not a misprint for Williston, as had been suspected: it was a station of the Silver Springs, Ocala & Gulf Railroad (Railroad Commission 1898, p. 86, station 37) in Levy County, and in 1901 Camp's camp there is named again (unit 10). Romeo, where the Meredith-Noble company later mined (unit 16), had a camp too."),
    u(9, f"{CA} 1899–1900, p. 48",
      "Report of Supervisor of State Convicts. … Sir—I have the honor to submit to you, this my first annual report as Supervisor of State Convicts and Convict Camps. I was appointed under Chapter 4758 Acts of 1899, and entered upon the duties of the office in November of that year. There were at that time 697 State Convicts, divided into 12 camps; seven camps, with 507 convicts, were engaged in mining phosphate; and five camps, with 190 convicts, were engaged in the manufacture of naval stores. There were on December 1st, 1900, 778 State Convicts, of which there are 102 white males and 2 white females, 651 colored males and 23 colored females. They are divided into thirteen camps, seven of which are engaged in mining phosphate and six in the manufacture of naval stores. The several camps are located as follows: Three in Alachua county, two in Marion county, four in Citrus county, one in Hernando county, one in Bradford county, one in Levy county and one in Washington county.",
      "507 in the phosphate pits",
      "In November 1899 nearly three in four of the state's prisoners worked in phosphate. Of the 778 counted in December 1900, 674 were Black. The supervisor, R. F. Rogers, was the first official whose task was to inspect the camps; his report goes on to say that he had “no trouble” with the lessees “with only two exceptions”."),
    u(10, f"{CA} 1901–1902, p. 51",
      "On January 1, 1901, there were 13 prison camps in the State, located as follows: and worked by W. N. Camp, at Wade, Fla.; W. N. Camp, Dutton, Fla.; W. N. Camp, at Elliston, Fla.; W. J. Hilman, at Cordeal, Fla.; W. J. Hilman, at Summerfield, Fla.; Dutton Phosphate Co., at Dutton, Fla.; C. H. Hargroves, at Romeo, Fla.; Myers Turpentine Co., at Tompkins, Fla.; J. Buttgenbach & Co., at Cordeal, Fla.; J. Buttgenbach & Co., at Cordeal, Fla.; J. Buttgenbach & Co., at Floral City, Fla.; G. W. Varn, at Brooksville, Fla.; Edwards & Durham, at Lawtey, Fla. January 1, 1902, the prisoners were divided into 20 camps, located as follows: And worked by, …",
      "The camps move on",
      "In 1902 the list of twenty camps (page image) no longer names Albion, Morriston or Elliston. In the reports examined here, the camp at Elliston is the last state convict camp in Levy County. County prisoners, worked under separate arrangements, are not in these lists."),
    u(11, f"{CA} 1901–1902, p. 57",
      "He is looked to for information as to the qualification of each captain and guard, as well as the condition of the prisoners and the camps, and is supposed, under the law, to visit each camp once in 60 days. From the Supervisor's monthly report, I have a full statement of the number of prisoners in each camp, the exact amount of food supplied daily, and the kind used each day, the articles of clothing, bedding, etc., furnished per month, the number of prisoners punished, the number of lashes applied, and for what offense.",
      "“The number of lashes applied”",
      "The commissioner describes the supervisor's monthly report as a matter of good administration. Whipping was a regular, counted punishment in the camps; the monthly reports themselves are not printed in these volumes."),
]

PIT = [
    u(12, "Matson, Bulletin 604 (1915), p. 90",
      "Stripping.—The first operation in mining rock phosphate is to remove the overburden of barren sand and clay—work that is usually done by horsepower scrapers, by picks and shovels, or, more rarely, by steam shovels. In some places hydraulic methods are employed, the overburden being first loosened by a hydraulic giant and washed into a pit, from which it is raised by a centrifugal pump and forced through pipes to the waste pile. Excavating.—Rock phosphate was first mined by pick and shovel, and in some places nothing but the bowlders were saved. … With the introduction of log washers the cruder methods first used were abandoned. However, the pick and shovel are still used in most places where the mining is done above the level of ground water, though in a few mines phosphate is excavated by steam shovels.",
      "Pick and shovel",
      "The geologist describes the methods, not the men (plate: a rock-phosphate mine with its tramway). Where the pits lay above the ground water the work was done by hand; below it, as near Dunnellon, by steam dredges (plates)."),
    u(13, "Matson, Bulletin 604 (1915), p. 91",
      "Sorting.—The coarser phosphate, held on the inner screen, falls upon a circular wooden table, while the finer material from the outer screen passes directly to the “wet” bin below this table. The table carrying the coarse material revolves slowly and a number of men and boys who stand about it remove the fragments of limestone, clay, and flint that are mixed with the phosphate. At the end of a complete revolution the phosphate is automatically scraped from the table (“picking belt”) and falls into the “wet” bin with the finer material.",
      "“Men and boys”",
      "The only sentence in the bulletin that mentions the workers, and then only at the picking table. Boys stood at the tables in 1915; Bailey's letter of 1897 (unit 7) speaks of prisoners “not thirteen years of age”."),
    u(14, "Matson, Bulletin 604 (1915), p. 92",
      "Drying.—From the “wet” bin the phosphate is conveyed in a small car running on a narrow track to the upper part of the dry shed. … In these sheds the rock is thoroughly dried by placing a layer of phosphate about 2 feet thick on the floor and stacking wood upon it to a depth of about 2 feet. This wood is so arranged that one layer lies across the other and considerable space is left between the sticks. Phosphate rock is dumped upon the wood to a depth of 10 to 15 feet and the wood is then fired and allowed to burn until it is consumed. The rock is ready for shipment as soon as it is cool enough to be loaded on cars.",
      "Dried over wood fires",
      "The hard-rock mines burned wood to dry the rock; cutting and hauling it was work of its own. The rock then went by rail to the ports of unit 1."),
]

WAR = [
    u(15, "Florida Geological Survey, 7th Annual Report (1915), pp. 20–21",
      "Production of Phosphate Rock in Florida during 1914. Owing to the interruption of European shipment the production of phosphate rock in Florida for the year 1914 shows a decrease over that of the preceding year. The output for 1913 was 2,584,794 long tons, while during 1914 the output, as reported by the producers, was 2,097,864 long tons, a decrease of 486,930 tons. The decrease occurred in both the land pebble and the hard rock districts; the percentage of decrease, however, is greater for the hard rock phosphate deposits. That the reduced output is due to the interruption of foreign shipment is shown by the fact that while the export shows a marked decrease, the amount of phosphate consigned for domestic shipments during 1914 is greater than during 1913, by about 28,918 tons. … The production of hard rock phosphate during 1914 was 310,267 tons, as against 477,538 tons during the preceding year, a reduction of 167,271.",
      "“The interruption of European shipment”",
      "The war in Europe began in August 1914; the ships and buyers of unit 1 were gone. Land pebble, from the mines of Polk County, also sold at home; hard rock, the product of the belt around Williston, hardly did."),
    u(16, "Florida Geological Survey, 7th Annual Report (1915), p. 22",
      "List of the Phosphate Mining Companies of Florida. Acme Phosphate Co. … Morriston, Fla. … Meredith-Noble Phosphate Co. … Romeo, Fla. … Summary of Production and Shipment of Florida Phosphate for the Years 1908, 1909, 1910, 1911, 1912, 1913 and 1914 (Long Tons). … Hard Rock— [1909, 1910, 1911, 1912, 1913, 1914:] Production 527,582 392,088 474,094 536,379 477,538 310,267. Exported 496,645 461,353 462,072 470,354 476,898 303,172. Domestic 17,456 18,745 16,723 15,425 12,896 6,517. Total shipments 514,101 480,098 478,795 485,779 489,794 309,689.",
      "Ninety-seven tons in a hundred abroad",
      "From 1909 to 1913 between 96 and 97 of every hundred tons of hard rock shipped went abroad (plate; graphic). The Acme Phosphate Company of Morriston heads the alphabetical list of companies; the Meredith-Noble company mined at Romeo, south of Morriston on the same railroad."),
    u(17, "Florida Geological Survey, 10th and 11th Annual Reports (1918), pp. 105–106",
      "“The shipments of hard rock phosphate necessarily continue at low ebb, since the export business is cut off and the hard rock is used only to a limited extent in the domestic trade. During 1917 soft phosphate rock entered to some extent into the phosphate production, the total combined shipments of hard rock and soft phosphate being 18,608 tons.” … Summary of Shipment of Phosphate in Florida from 1913 to 1917, Inclusive. … Hard Rock— [1913, 1914, 1915, 1916, 1917:] Exported 476,898 303,172 43,314 28,045 12,403. Domestic 12,896 6,517 6,816 19,042 6,205. Total shipment 489,794 309,689 50,130 47,087 *18,608. [* Includes soft rock phosphate.] … List of Mining Companies of Florida. Acme Phosphate Company … Morriston, Fla.",
      "“At low ebb”",
      "Quoted by the survey from its own press bulletin of May 1918. In 1915 the hard rock fields shipped about a tenth of what they had shipped in 1913; in 1917 less than a twentieth (plate). The surveys say nothing about what became of the men who had worked in the pits; Williston's other trade, the cucumbers of module 4, depended on the northern markets instead."),
    u(18, "Florida Geological Survey, 14th Annual Report (1922), pp. 29–30",
      "“The recovery of the industry from the depressing conditions attributable to the recent world war is shown both in the largely increased production from the pebble phosphate fields and the very decided increase from the hard rock fields, as compared with the output for several preceding years. The amount of hard rock phosphate marketed during 1920 is evidence of the increased demand for this high-grade rock. …” [1919:] Hard rock 285,467 [long tons], $2,452,563, $8.59 [per ton]. [1920:] Hard rock 400,249, $4,525,191, $11.31. … “The hard rock production increased 114,782 tons.” … List of Phosphate Mining Companies of Florida, 1920. Acme Phosphate Co. … Morriston, Fla.",
      "Recovery, 1920",
      "In April 1920 Herman Gunter of the Florida Geological Survey took the picture of the Acme pit five miles southwest of Morriston (plate). The figures of 1919 and 1920 are quantities marketed, not shipments abroad; the report does not divide them."),
]

SRC = ("Manufacturers' Record 23 (1893), no. 22, 30 June 1893, p. 396; Reports of the Commissioner of Agriculture of the State of Florida for 1893–1894, pp. 67, 81, 83–85, "
       "for 1895–1896, p. 81, for 1899–1900, pp. 47–48, and for 1901–1902, pp. 51, 57; G. C. Matson, The Phosphate Deposits of Florida, U.S. Geological Survey Bulletin 604 "
       "(Washington 1915), pp. 9, 90–92, plates II, III and XVII; Florida Geological Survey, Seventh Annual Report (1915), pp. 20–22, Tenth and Eleventh Annual Reports (1918), "
       "pp. 105–106, Fourteenth Annual Report (1922), pp. 29–30. Page images: Internet Archive (sim_site-selection_1893-06-30_23_22; "
       "ReportOfTheCommissionerOfAgricultureOfTheStateOfFloridaForPeriod_33, _604, _614, _570; phosphatedeposi00matsgoog and IA41522103_0102; "
       "annualreportflor71915flor, annualreportf10111918flor, annualrepor1419211922flor). All in the public domain.")

T = {
    "titel": "Hard rock",
    "autor": "A trade paper, the state's reports on its leased prisoners, the U.S. Geological Survey and the Florida Geological Survey",
    "jahr": "1893–1920",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print. “…” marks an omission; square brackets mark editorial additions, such as the years above the columns of a table. “Colored” is the word of the official tables. The reports on the convict camps were written by the officials and lessees responsible for them; their judgements (“humane men”, “excellent” health) are theirs. The prisoners who mined the phosphate near Albion speak nowhere in these sources, and none of the dead is named. The figures for production and shipment are those supplied by the companies to the surveys.",
    "sections": [
        {"id": "belt", "titel": "The hard rock belt (1893–1915)",
         "blurb": "Hard rock phosphate, dug from pits in a narrow belt running from Suwannee County through Alachua and Levy to Dunnellon, was shipped to the fertilizer works of Europe. Early Bird and Eagle Mine, on the line through Williston, and Albion in Levy County had been given up by 1915.",
         "plates": ["usgs604_map"], "viz": "rock-export", "units": BELT},
        {"id": "leased", "titel": "Leased men (1893–1902)",
         "blurb": "Among the first to work the pits near Albion were the state's prisoners, most of them Black, leased to the mine owners. The state's own reports name the camps at Albion, Morriston and Elliston, count the prisoners by colour, and record, in the lessee's words, the dead.",
         "plates": ["coa1894_table17", "coa1897_bailey", "coa1900_camps"], "viz": "rock-leased", "units": LEASED},
        {"id": "pit", "titel": "Pick, shovel and fire (1915)",
         "blurb": "How the rock was dug, washed, picked and dried, as a federal geologist described it in 1915: by hand above the water line, by dredge below it, and over wood fires before it went to the cars.",
         "plates": ["usgs604_mine", "usgs604_dredge"], "units": PIT},
        {"id": "war", "titel": "The war (1914–1920)",
         "blurb": "Almost all hard rock went abroad. When the war in Europe stopped the ships in 1914, shipments from the hard rock fields fell to a tenth within a year and stayed there until the war was over. Morriston's Acme Phosphate Company outlasted it.",
         "plates": ["fgs1915_table", "fgs1918_table", "fm_ge0629"], "units": WAR},
    ],
}
for s in T["sections"]:
    s["zk"] = "Hard rock, " + s["titel"].split(" (")[0]
(D / "rock.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
B604 = "G. C. Matson, The Phosphate Deposits of Florida, U.S. Geological Survey Bulletin 604 (1915)"
NEW = [
    {"id": "usgs604_map", "side": "rock", "titel": "The phosphate deposits of Florida",
     "caption": "Rock phosphate in a belt from Suwannee County through Alachua, Levy and Marion counties to Citrus and Hernando; land pebble in Polk County.",
     "source": B604 + ", plate III; Internet Archive IA41522103_0102; public domain."},
    {"id": "usgs604_mine", "side": "rock", "titel": "A rock-phosphate mine",
     "caption": "“General view of rock-phosphate mine”: the pit, the trestle of the tramway, the cars; people at work at the bottom. Photograph by W. L. Martin; the mine is not named.",
     "source": B604 + ", plate II; Internet Archive IA41522103_0102; public domain."},
    {"id": "usgs604_dredge", "side": "rock", "titel": "Mining by dredging",
     "caption": "“General view of pit in the rock-phosphate region, showing mining by dredging”: the dredge in the flooded pit, the washer and the incline behind. Photograph by W. L. Martin.",
     "source": B604 + ", plate XVII; Internet Archive IA41522103_0102; public domain."},
    {"id": "coa1894_table17", "side": "colour", "titel": "512 of 614",
     "caption": "Table No. 17: the state's convicts on 31 December 1894 by colour, sex, education and religion.",
     "source": "Report of the Commissioner of Agriculture of the State of Florida for 1893–1894, p. 81; Internet Archive ReportOfTheCommissionerOfAgricultureOfTheStateOfFloridaForPeriod_33 (State Library and Archives of Florida); public domain."},
    {"id": "coa1897_bailey", "side": "colour", "titel": "Bailey's letter from Albion, 1897",
     "caption": "The lessee E. B. Bailey to the Commissioner of Agriculture, 15 January 1897: twenty-one dead in 1895, nineteen in 1896.",
     "source": "Report of the Commissioner of Agriculture of the State of Florida for 1895–1896, p. 81; Internet Archive ReportOfTheCommissionerOfAgricultureOfTheStateOfFloridaForPeriod_604; public domain."},
    {"id": "coa1900_camps", "side": "colour", "titel": "The lease of 1897 and the camps",
     "caption": "The contract of 22 May 1897 with four lessees, among them W. N. Camp of Albion, and the camps of 1899–1900, “Levy county, one at Elliston”.",
     "source": "Report of the Commissioner of Agriculture of the State of Florida for 1899–1900, p. 47; Internet Archive ReportOfTheCommissionerOfAgricultureOfTheStateOfFloridaForPeriod_614; public domain."},
    {"id": "fgs1915_table", "side": "rock", "titel": "Production and shipment, 1909–1914",
     "caption": "The survey's summary table: hard rock exported 496,645 tons in 1909, 303,172 in 1914; shipped for domestic use between 6,517 and 18,745.",
     "source": "Florida Geological Survey, Seventh Annual Report (1915), p. 22; Internet Archive annualreportflor71915flor; public domain."},
    {"id": "fgs1918_table", "side": "rock", "titel": "“At low ebb”, 1913–1917",
     "caption": "Shipments of hard rock 1913–1917: exported 476,898 tons in 1913, 12,403 in 1917.",
     "source": "Florida Geological Survey, Tenth and Eleventh Annual Reports (1918), p. 106; Internet Archive annualreportf10111918flor; public domain."},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
P["credit"] = ("Photographs from the Seaboard Air Line Railway Shippers Guide (1914) and from U.S. Geological Survey Bulletin 604 (1915), and pages of gazetteers, railroad and "
               "geological reports, the state's reports on its convicts, trade papers and the Laws of Florida, after the page images of the Internet Archive; the “Standard Guide” "
               "map of 1891 and the Sanborn fire-insurance maps of Williston, January 1923, from the Library of Congress (public domain) via Wikimedia Commons; the Plant System map "
               "from Poor's Manual (1901) via Wikimedia Commons; photograph of the Acme Phosphate pit from the Florida Geological Survey Collection, State Archives of Florida, "
               "Florida Memory (public domain).")
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "rock"), None) or next(x for x in M["shipped"] if x["id"] == "rock")
M["planned"] = [x for x in M["planned"] if x["id"] != "rock"]
m.update({"datei": "rock", "zk": "Belt · Leased men · Pit · War",
          "kurz": "3 · Hard rock",
          "warum": "Phosphate dug by hand in pits around Albion and Morriston, much of it in the 1890s by leased state prisoners, most of them Black, of whom the lessee counted forty dead in two years. Nearly all of it went to Europe, until the war stopped the ships in 1914.",
          "quelle": "Manufacturers' Record 1893; Reports of the Commissioner of Agriculture of Florida 1893–1902; USGS Bulletin 604 (1915); Florida Geological Survey annual reports 1915–1922."})
order = ["before", "rails", "rock", "shipping", "line", "airfield"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "rock"] + [m], key=lambda x: order.index(x["id"]) if x["id"] in order else 99)
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "humane", "titel": "“Humane men” and the death roll",
     "frage": "How did the officials and the lessee describe the convict camps in Levy County?",
     "note": "The department wrote in 1895 that the camps were “in charge of sober, reliable and humane men”, and its chaplain found Bailey's camp in Levy County good in every respect. Two years later Bailey himself reported twenty-one dead in 1895 and nineteen in 1896, three of them killed while escaping or being recaptured, and children under thirteen among those sent to him. All three voices are those of the state and the lessee; the prisoners are not heard.",
     "voices": [{"text": "rock", "sec": "leased", "n": [3, 5], "wer": "Commissioner of Agriculture and chaplain, 1895"},
                {"text": "rock", "sec": "leased", "n": [7], "wer": "E. B. Bailey, lessee, 1897"}]},
    {"id": "abroad", "titel": "Going to Europe",
     "frage": "Where did the hard rock go, and what happened when it could not?",
     "note": "In 1893 a trade correspondent found that only an eighth or a seventh of Florida's phosphate stayed at home, and called it a fact that called “for serious thought”. In 1914 the war in Europe proved him right: the hard rock fields, which sold almost nothing at home, lost most of their trade within a year.",
     "voices": [{"text": "rock", "sec": "belt", "n": [1], "wer": "Manufacturers' Record, 1893"},
                {"text": "rock", "sec": "war", "n": [15], "wer": "Florida Geological Survey, 1915"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/rock/"
OLD = {"Leased convicts in the pits and camps", "The export trade breaks"}
NEWST = [
    {"d": "1893–1894", "side": "rock", "titel": "Leased convicts in the pits and camps",
     "text": "The state's leased convicts are worked in the county: about 160 near Albion, Levy county, mining phosphate, and about fifteen sublet to Colonel H. L. Morris of Morriston for the manufacture of naval stores. Of the state's 614 prisoners at the end of 1894, 512 are Black men.",
     "cite": K + "leased/3", "citeLabel": "Hard rock [3]", "plate": "coa1894_table17",
     "quelle": "Report of the Commissioner of Agriculture of the State of Florida, 1893–1894, pp. 67, 81."},
    {"d": "January 1897", "side": "colour", "titel": "“The death roll was twenty one”",
     "text": "The lessee E. B. Bailey, writing from Albion, reports twenty-one deaths among the convicts in 1895 and nineteen in 1896, three of them killed while escaping or being recaptured; some of the prisoners sent to him are “not thirteen years of age”.",
     "cite": K + "leased/7", "citeLabel": "Hard rock [7]", "plate": "coa1897_bailey",
     "quelle": "Report of the Commissioner of Agriculture of the State of Florida, 1895–1896, p. 81."},
    {"d": "1899–1900", "side": "rock", "titel": "507 prisoners in the phosphate pits",
     "text": "Seven of the state's twelve convict camps, with 507 prisoners, mine phosphate; one camp in Levy County, at Elliston, is worked by W. N. Camp of Albion.",
     "cite": K + "leased/9", "citeLabel": "Hard rock [9]", "plate": "coa1900_camps",
     "quelle": "Report of the Commissioner of Agriculture of the State of Florida, 1899–1900, pp. 47–48."},
    {"d": "1914", "side": "rock", "titel": "The export trade breaks",
     "text": "“Owing to the interruption of European shipment”, Florida's hard-rock phosphate falls from 477,538 tons (1913) to 310,267 tons; almost every ton shipped goes abroad. The state's list of phosphate companies opens with the Acme Phosphate Co. of Morriston.",
     "cite": K + "war/15", "citeLabel": "Hard rock [15]", "plate": "fgs1915_table",
     "quelle": "Florida Geological Survey, Seventh Annual Report (1915), pp. 20–22."},
    {"d": "1917", "side": "rock", "titel": "“At low ebb”",
     "text": "The hard rock fields export 12,403 tons, against 476,898 in 1913; “the export business is cut off”.",
     "cite": K + "war/17", "citeLabel": "Hard rock [17]", "plate": "fgs1918_table",
     "quelle": "Florida Geological Survey, Tenth and Eleventh Annual Reports (1918), pp. 105–106."},
    {"d": "April 1920", "side": "rock", "titel": "The Acme pit near Morriston",
     "text": "Herman Gunter of the state survey photographs the Acme Phosphate Company's pit five miles southwest of Morriston. In 1920 the hard rock fields market 400,249 tons, a “very decided increase”.",
     "cite": K + "war/18", "citeLabel": "Hard rock [18]", "plate": "fm_ge0629",
     "quelle": "Florida Memory GE0629; Florida Geological Survey, Fourteenth Annual Report (1922), pp. 29–30."},
]
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
