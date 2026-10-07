"""Builds data/line.json (module 5: The colour line, 1904–1924) and enters the module in modules.json,
plates.json, timeline.json and compare.json.

Sources, each passage read against the page image (log: ../quellen/PRUEFUNG.md):
  Ocala Evening Star, 7 September 1904 (UFDC UF00075908/01686);
  NAACP, Thirty Years of Lynching in the United States, 1889–1918 (New York 1919) (IA thirtyyearsoflyn00nati), p. 55;
  Palatka Daily News, 5, 7, 8 and 10 January 1923 (UFDC AA00023799), Associated Press reports and an editorial;
  Miami Daily Metropolis, 12 February 1923 (UFDC AA00020298); Fort Pierce News-Tribune, 20 February 1923 (UFDC AA00081508);
  The Crisis 25/5 (March 1923), p. 224, and 26/2 (June 1923), p. 84 (IA sim_crisis_1923-03_25_5, sim_crisis_1923-06_26_2);
  Palm Beach Post, 17 February 1924 (UFDC UF00098049).
All published before 1931 and in the public domain.
Run from the site root: python tools/build-line.py
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


PDN = "Palatka Daily News"

BRONSON = [
    u(1, "Ocala Evening Star, 7 September 1904, p. 1",
      "A Lynching at Levyville. Wash Bradley, the Negro Who Killed Mrs. Barrow, Summarily and Dreadfully Punished. Bronson, Fla., Sept. 6.—Wash Bradley, the negro turpentine hand who murdered Mrs. N. B. Barrow, a highly respected lady near Levyville last Friday afternoon, was captured yesterday not far from the scene of his crime, and this morning suffered death at the hands of a mob. The murderer was caught by two negroes, George and Walter Howard, and they carried their prisoner to Levyville yesterday afternoon. The whole town of Levyville was soon excited, and a message was sent to the husband of the murdered woman who came to the town and shot off both the negro's arms. According to information received here, the arms of the negro were completely amputated, and his bleeding body was then turned over to the mob of infuriated men who hanged it to a tree. The negro cried piteously for mercy, but was only given curses in return. Before life was extinct, members of the mob began firing at the swaying body, which was soon riddled with bullets. The body was still hanging at 8 o'clock this morning. The mob completed its work shortly after 3 o'clock, and quietly dispersed. The negro Bradley on last Friday attempted to shoot Mrs. Barrow's daughter, when she intervened, receiving the load of shot, which took effect in the left breast, near the heart. Bradley escaped, but a score of citizens have been searching for him since. The negroes who captured him will get the reward of $150.—Metropolis.",
      "“Summarily and dreadfully punished”",
      "Reprinted by the Ocala paper from the Jacksonville Metropolis. Two people died: Mrs. N. B. Barrow, shot on Friday, 2 September, when, by this report, she stepped between the gun and her daughter; and Wash Bradley, a turpentine worker, tortured and killed by a mob on the morning of 6 September. The paper calls Bradley a murderer; he was never tried, and what happened at the Barrow house is known only from this kind of report. It names the two Black men who caught him and the reward they were to get, but none of the mob. Levyville lay near Bronson, the county seat. The headline calls a lynching a punishment; the report describes it in detail as if for an audience. It is printed in full here because it is the only account of the time found so far."),
    u(2, "NAACP, Thirty Years of Lynching (1919), p. 55",
      "Chronological List of Persons Lynched. Florida—Continued. … 1904. Jan. 15 Clark, Jumbo, High Springs, Alachua Co., Rape. May 20 Unknown, Mulberry, Polk Co., Unknown offence. Sept. 6 Bradley, Wash, Bronson, Levy Co., Murder. Oct. 4 Rivers, —, Perry, Taylor Co., Attempted rape.",
      "One line in a list",
      "The National Association for the Advancement of Colored People counted lynchings from newspaper reports and its own inquiries; the last column is the accusation that the mob gave, not a finding of guilt. By the book's count Florida had 178 victims in the thirty years. Wash Bradley's line is the only trace of him in the national record; there is no record of an inquest, an arrest or a trial."),
]

ROSEWOOD = [
    u(3, f"{PDN}, 5 January 1923, p. 1",
      "Burn Otter Creek Following Deaths of Two Citizens. Heavy Fire All Night at Hut Containing Negroes. Martial Law Exists. Governor Will Order Out State Troops If Necessary. (By Associated Press) Otter Creek, Fla., Jan. 5.—Two white men, two negresses and one negro are known to be dead, and there are believed to be many other casualties as a result of the racial trouble last night and early this morning at Rosewood, twelve miles from here. With the exception of three buildings this entire village was burned by the mob at daybreak, according to reports. Fighting began when a party of citizens of Sumner went to Rosewood seeking a negro alleged to have attacked a white woman on Monday, and they were fired on by a party of negroes barricaded in a house. Sumner citizens, with two members of the party slain in the first volley, established a cordon around the house and opened fire. During the night when the attackers ran out of ammunition and several left to replenish the supply, the negroes escaped, leaving the bodies of two women and one man in the house. Bloodstains indicated that several of the negroes had been wounded. Immediately after the mob began firing the buildings in the village. While the village was in flames, it is said, members of the mob fired upon negroes fleeing from their homes. About twenty families, many of them negroes, resided in Rosewood. … Deputized posses and citizens said to be numbering in the thousands were pouring into this village early this morning. Automobile after automobile heavily laden with armed men have arrived, some coming from a distance of about 75 miles. … The white dead are: Henry Andrews, superintendent of the Cummer Lumber company's saw mill. Boly Wilkerson, of Sumner. The wounded: Man believed to be R. J. Odom, of Jacksonville, employed at a box factory at Otter Creek. Sephus Studstill, of Rosewood. Warner Kirkland, of Rosewood. The bodies of Andrews and Wilkerson lay all night where they fell. … Andrews leaves a wife and three children; Wilkerson a wife and five children.",
      "Thursday night and Friday morning",
      "The first Associated Press report, as printed on 5 January. The headline puts the fire at Otter Creek; the text places it at Rosewood, a settlement on the railroad to Cedar Key, near the mill town of Sumner. The white dead and wounded are named with their families; the Black dead are “two negresses and one negro”, without names. The report already gives the white crowd's account of how it began (an “alleged” attack on a white woman at Sumner on Monday, 1 January). Henry Andrews was superintendent of the Cummer Lumber Company's mill."),
    u(4, f"{PDN}, 7 January 1923, p. 1",
      "[Banner:] Mad Mob Shoots Down Negro Beside Mother's Grave. … Refused to Give Names of Gunmen to Captors. Buried Beside Mother and Sister Killed in Riot. Possee After Hunter. Further Trouble Is Not Probable in Levy County. (By Associated Press) Rosewood, Fla., Jan. 6.—A new grave was dug in the negro cemetery at Sumner near here late today and in it Sheriff Elias Walker placed the body of James Carrier, whose death at the hands of several white men this morning was the sequel of the clash between the races at Rosewood Thursday night. He was shot to death while standing on the grave of the four other negroes who fell in the fighting that followed an attempt of a crowd of white men to enter a negro house in search of Jesse Hunter, wanted for alleged implication in an attack on a white girl at Sumner. According to information received by officials, Carrier was seized by several white men this morning and accused of having been in the house from which negroes fired on the approaching white men, killing two of their number. When he is said to have refused to reveal the names of the negroes who did the shooting, the white men, officers were informed, led him to the negro graveyard and made him stand on the newly-dug grave of his brother and mother, also victims of the fighting, while they riddled his body with shots. Meanwhile Hunter, search for whom has resulted in the seven deaths, still is at large. … The negroes of Rosewood have been in hiding in the woods since Thursday night and those in the nearby villages do not venture from their quarters, it was reported.",
      "James Carrier, 6 January",
      "The first name of a Black victim in these reports. The headline says “mother and sister”, the text “brother and mother”: the paper did not know which. The men who shot James Carrier are “several white men”; officers “were informed”; none is named. Jesse Hunter, the man the crowd said it was looking for, was not found. The banner line above, “Victims of Hooded Gang Tortured”, belongs to another story on the same page (Mer Rouge, Louisiana)."),
    u(5, f"{PDN}, 8 January 1923, p. 1",
      "Rosewood Is Passive Following Race Riots. Homeless Negroes Are Still Secreted in Woods. No Clue to Hunter. Twelve Houses Burned in Negro Section of Rosewood. (By Associated Press) Rosewood, Fla., Jan. 8.—Rosewood is quiet today following the racial disturbances of the past few days, in which seven persons were killed as the result of a search by officers and citizens posses for Jesse Hunter, negro, wanted for an alleged attack on a young white woman at Sumner last Monday. Officers are still without a clew as to the whereabouts of Hunter. Officers are inclined to believe that the burning of twelve houses, all that was left of the negro quarter of Rosewood Sunday afternoon marks the end of the racial clashes, they assert. The negroes whose houses were fired are still taking refuge in nearby woods out of fear. The houses were burned by a number of white men while a crowd looked on, but no one could be found who would say that he saw the houses burned, according to county officers. The burning Saturday afternoon came as a sequel to the previous destruction of a large part of the negro section and the clashes between white men and negroes, in which the fatalities occurred. Two white men were killed in the conflicts and five negroes fell victims, two of the negroes being shot to death in a rain of bullets on a dwelling in which the blacks barricaded themselves, the other three being slain at different times. Authorities have in custody several negroes in connection with the clashes, the officers stating that these prisoners who have been spirited away for safe keeping, were among those who barricaded themselves in the house and were fired on.",
      "“No one could be found who would say that he saw”",
      "The report gives the burning both to “Sunday afternoon” and to “Saturday afternoon”. A crowd watched; the county officers found no witness. The Black survivors were in the woods; some of those who had been fired on in the house were in custody, “for safe keeping”. In five days the count of the dead had moved from five known and “many” believed (unit 3) to seven."),
]

AFTER = [
    u(6, f"{PDN}, 10 January 1923, p. 2",
      "Levy County People Deserve No Censure. By no means should the riots which have so recently startled the state and have so upset Levy county be classed in the same category as troubles which have many times been thrust upon communities to the northward and even in states to the westward. The tragedy is as nothing when compared with the race riots at East St. Louis a few years ago. Or with the Herrin murders, also in Illinois, during the past year. … Levy county is not a progressive county. It has lost nearly five per cent of its population during the past decade. It has, however, some remarkably fine people—and while they deplore the tragedy they are not actually ashamed of it. The occurrences following the attack upon the white woman by a negro stirred the people there to a frenzy. It would have been the same had the attacker been a white man. The crowd sought to find the miscreant, and in their search were fired upon by a body of negroes barricaded within a house. Two of the whites were killed by the bullets. It would have made no difference to the crowd searching for the ravisher whether the men taking the lives of their fellows were black, white or yellow; the shooting and maiming and the firing of homes would have taken place just the same. … The entire affair is regrettable—but no portion of it more so than that a woman suffered so great an indignity as to place her life in danger at the hands of a brute. It is to be regretted that race fealty to protect an indecent man snuffed out the lives of those, perhaps, who were innocent; …",
      "“Not actually ashamed of it”",
      "An editorial in a Florida daily five days after the burning. It treats as proven what the reports call “alleged”, blames the dead for protecting a man nobody had found, and says the killing and burning would have happened whatever the colour of the accused. Printed as a document of how the event was justified at the time; the paper's words are its own."),
    u(7, "Miami Daily Metropolis, 12 February 1923, p. 1",
      "Rosewood Riot Probe Under Way in Florida. Special Grand Jury Called in Eighth Judicial Circuit to Investigate Eight Deaths. (By Associated Press.) Bronson, Fla., Feb. 12.—Investigation of the rioting at Rosewood, near here, last month in which eight persons—two white men and six negroes—lost their lives, was scheduled to begin here today by a special grand jury called by Judge A. V. Long, eighth judicial district, who was to preside over its deliberations. The rioting grew out of an attempt by armed men to enter a negro dwelling near Rosewood in search of a negro charged with a criminal attack upon a young white woman, wife of a saw mill employe, at Sumner, two miles distant. A number of negroes in the house refused admittance to the men and an exchange of shots followed which continued for several hours. Two white men were killed and three wounded among those surrounding the house while two negroes were killed and several wounded inside the building. Subsequently four negroes were shot and killed and every house in Rosewood was burned to the ground. The Alachua county grand jury called by Judge Long last week to investigate the lynching of Abe Wilson, a negro, near Newberry January 17, another outgrowth of the attack upon the woman, failed to find sufficient evidence upon which to base an indictment. George Decottes, of Sanford, prosecuting attorney of the seventh judicial district, was ordered by Gov. Hardee to assist in the investigation of the case by the grand jury here today.",
      "A special grand jury",
      "By February the count stood at eight, two white and six Black. The report adds a further killing that the January reports did not tie to Rosewood: Abe Wilson, lynched near Newberry in Alachua County on 17 January, “another outgrowth”. Its grand jury had already found no evidence. The governor sent a prosecutor from another circuit."),
    u(8, "Fort Pierce News-Tribune, 20 February 1923, p. 6",
      "No Indictment Returned by Grand Jury in Case of Recent Rosewood Riot. Bronson, Feb. 17.—Investigation of the Rosewood rioting, closed here Thursday when the grand jury reported that sufficient evidence had not been found upon which to return indictments. George Decottes, prosecuting attorney, returned to Bronson yesterday. Testimony received from witnesses called before the grand jury had not been strong enough to warrant the return of any indictments, he said. Eight persons, two white and six negroes, were killed in the Rosewood rioting which started when a posse attempting to enter a house in search of a negro wanted for an alleged attack upon a young white woman, was fired upon. Two white men were instantly killed and three others wounded. Six negroes were killed in the rioting which followed and the entire negro settlement of Rosewood was burned to the ground.",
      "No indictment",
      "Thursday was 15 February 1923. Nobody was charged for any of the killings or for the burning of Rosewood. The names of the witnesses are not given; whether Black survivors testified, these reports do not say. The figure of eight dead is the official one; later accounts hold that more people died (unit 11, note)."),
    u(9, "The Crisis 25, no. 5 (March 1923), p. 224",
      "Mr. M. L. Studstill, a white mill operator of Sumner, Florida, was the leader of the band who led the mob that raided the Negro houses at Rosewood, Florida, killing and burning men, women and children, and destroying the property of the whole colored settlement. He was slightly wounded in the arm. We present the picture of this eminent citizen that our readers may see the type of man who is defending civilization in Florida.",
      "The Crisis names a leader",
      "The monthly magazine of the NAACP: the Black press's answer to the silence of the grand jury. It printed a photograph of the man it accused (not reproduced here). This is the magazine's charge; no court ever heard it. The Associated Press of 5 January lists among the wounded a “Sephus Studstill, of Rosewood” (unit 3); whether the two are the same man these sources do not show."),
    u(10, "The Crisis 26, no. 2 (June 1923), p. 84",
      "India Speaks. America's lynching fame spreads over the world. We find in a Hindu newspaper the Swarajya, published in Madras, India, an account of the riot in Rosewood, Fla., and the following comment: The full significance of the news item that appears elsewhere that the town of Rosewood in Florida was destroyed as the result of a collision between the Negroes and whites, we fear, will not be realized by most people in our country. … But it calls our attention to a great blot on American civilization, namely, the rivalry between the colored and the white peoples of the States. Racial animosity is artificially kept up by Jim Crow institutions, … It is this unmistakable rivalry that is responsible for the frequent cases of lynching Negroes, for which even the powerful administrative machinery of America could not find a preventive. … But the general attitude of the whites towards the Negroes has continued to be one of hostility. They cannot bring themselves to treat them as equals. Lynching of Negroes has become a scandal and those responsible for it are let go unpunished.",
      "From Madras",
      "Five months after the burning, a newspaper in India read the same news report as the Palatka editor (unit 6) and drew the opposite conclusion. The Crisis reprinted it."),
    u(11, "Palm Beach Post, 17 February 1924, p. 9",
      "The Twentieth Century club of Gainesville did many splendid pieces of community service work during the year; among which should be mentioned the tree of light, which was kept on the square during Christmas week; a Christmas tree for the children at the farm colony; looking after the refugees from the Rosewood riot; making 12 sweaters and 20 pairs of pajamas for the ex-soldiers at Lake City, and 100 flannel petticoats for the Russians.",
      "“The refugees from the Rosewood riot”",
      "A year later, in a list of a women's club's good works. The people of Rosewood did not return; the settlement was not rebuilt. Who the refugees were and where they went, these sources do not say. Seventy years later came a report to the state (1993) and an act of the Florida Legislature compensating survivors (1994); neither is printed here (Texts, “Examined and not included”). Later accounts, among them the Jacksonville Free Press (23 February 2006), dispute the official count of eight dead."),
]

SRC = ("Ocala Evening Star, 7 September 1904, p. 1. NAACP, Thirty Years of Lynching in the United States, 1889–1918 (New York 1919), p. 55. Palatka Daily News, 5 January 1923, p. 1; "
       "7 January 1923, p. 1; 8 January 1923, p. 1; 10 January 1923, p. 2 (all Associated Press reports except the editorial of 10 January). Miami Daily Metropolis, 12 February 1923, p. 1. "
       "Fort Pierce News-Tribune, 20 February 1923, p. 6. The Crisis 25, no. 5 (March 1923), p. 224, and 26, no. 2 (June 1923), p. 84. Palm Beach Post, 17 February 1924, p. 9. "
       "Page images: University of Florida Digital Collections (UF00075908, AA00023799, AA00020298, AA00081508, UF00098049) and Internet Archive (thirtyyearsoflyn00nati, "
       "sim_crisis_1923-03_25_5, sim_crisis_1923-06_26_2). All in the public domain.")

T = {
    "titel": "The colour line",
    "autor": "Florida newspapers and the Associated Press, the NAACP and its magazine The Crisis",
    "jahr": "1904–1924",
    "quelle": SRC,
    "hinweis": "Each passage is transcribed from the page image; spelling and punctuation are those of the print. “…” marks an omission; square brackets mark editorial additions. These are the words of white newspapers, the Associated Press and the NAACP; the language of the white papers (“negro”, “brute”, “punished”) is theirs and is printed because it is part of the record of how the violence was told and excused. Accusations made by mobs and papers against the dead are not findings: Wash Bradley was never tried, and no one was ever charged for any of the killings in this module. The people of Rosewood speak nowhere in these sources. The convict lease that brought Black prisoners into the county's pits and camps is in module 3. The Black press of 1923 beyond The Crisis (Chicago Defender, Baltimore Afro-American and others) has not yet been read.",
    "sections": [
        {"id": "bronson", "titel": "Bronson, September 1904",
         "blurb": "A white woman shot near Levyville; a Black turpentine worker caught by two Black men, handed to her husband and a mob, tortured and hanged near Bronson, the county seat. The only accounts are a newspaper report and one line in the NAACP's count.",
         "plates": ["oes1904_levyville", "naacp1919_florida"], "units": BRONSON},
        {"id": "rosewood", "titel": "Rosewood, January 1923",
         "blurb": "From the night of Thursday, 4 January, armed white men besieged a house in Rosewood, a Black settlement on the railroad near Sumner, burned the village in the following days and killed at least six of its people; two white men were killed at the house. The Associated Press reports of that week, as one Florida daily printed them.",
         "plates": ["pdn1923_jan5", "pdn1923_jan7", "pdn1923_jan8"], "viz": "line-rosewood", "units": ROSEWOOD},
        {"id": "after", "titel": "No indictment (1923–1924)",
         "blurb": "An editorial excusing the violence, a special grand jury that found no evidence, the NAACP's magazine naming a man the courts never named, a newspaper in India, and a year later a line about refugees.",
         "plates": ["mdm1923_probe", "fpnt1923_noindictment", "crisis1923_india"], "units": AFTER},
    ],
}
for s in T["sections"]:
    s["zk"] = "The colour line, " + re.sub(r" \(.*", "", s["titel"])
(D / "line.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- plates
P = json.loads((D / "plates.json").read_text(encoding="utf-8"))
UF = "University of Florida Digital Collections (Florida Digital Newspaper Library)"
NEW = [
    {"id": "oes1904_levyville", "side": "colour", "titel": "“A Lynching at Levyville”, 1904",
     "caption": "The report of the lynching of Wash Bradley near Bronson, 6 September 1904, as the Ocala Evening Star reprinted it from the Jacksonville Metropolis.",
     "source": "Ocala Evening Star, 7 September 1904, p. 1; " + UF + ", UF00075908; public domain."},
    {"id": "naacp1919_florida", "side": "colour", "titel": "Florida, 1904",
     "caption": "The NAACP's chronological list of persons lynched in Florida: “Sept. 6 Bradley, Wash, Bronson, Levy Co.”",
     "source": "NAACP, Thirty Years of Lynching in the United States, 1889–1918 (1919), p. 55; Internet Archive thirtyyearsoflyn00nati; public domain."},
    {"id": "pdn1923_jan5", "side": "colour", "titel": "5 January 1923",
     "caption": "The first Associated Press report from Rosewood: a house besieged through the night, the village burned at daybreak.",
     "source": "Palatka Daily News, 5 January 1923, p. 1; " + UF + ", AA00023799; public domain."},
    {"id": "pdn1923_jan7", "side": "colour", "titel": "James Carrier, 6 January 1923",
     "caption": "“Refused to give names of gunmen to captors”: the killing of James Carrier at the graves of his family in the cemetery at Sumner.",
     "source": "Palatka Daily News, 7 January 1923, p. 1; " + UF + ", AA00023799; public domain."},
    {"id": "pdn1923_jan8", "side": "colour", "titel": "“Homeless negroes are still secreted in woods”",
     "caption": "8 January 1923: twelve more houses burned while a crowd looked on; no witness found.",
     "source": "Palatka Daily News, 8 January 1923, p. 1; " + UF + ", AA00023799; public domain."},
    {"id": "mdm1923_probe", "side": "colour", "titel": "The special grand jury, February 1923",
     "caption": "“Rosewood Riot Probe Under Way in Florida”: eight dead, every house burned, and the lynching of Abe Wilson near Newberry.",
     "source": "Miami Daily Metropolis, 12 February 1923, p. 1; " + UF + ", AA00020298; public domain."},
    {"id": "fpnt1923_noindictment", "side": "colour", "titel": "“No indictment returned”",
     "caption": "The end of the inquiry, 15 February 1923, as reported from Bronson.",
     "source": "Fort Pierce News-Tribune, 20 February 1923, p. 6; " + UF + ", AA00081508; public domain."},
    {"id": "crisis1923_india", "side": "colour", "titel": "“India Speaks”, 1923",
     "caption": "The Crisis reprints a comment on Rosewood from the Swarajya of Madras.",
     "source": "The Crisis 26, no. 2 (June 1923), p. 84; Internet Archive sim_crisis_1923-06_26_2; public domain."},
]
ids = {p["id"] for p in NEW}
P["plates"] = [p for p in P["plates"] if p["id"] not in ids] + NEW
(D / "plates.json").write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- modules
M = json.loads((D / "modules.json").read_text(encoding="utf-8"))
m = next((x for x in M["planned"] if x["id"] == "line"), None) or next(x for x in M["shipped"] if x["id"] == "line")
M["planned"] = [x for x in M["planned"] if x["id"] != "line"]
m.update({"datei": "line", "zk": "Bronson 1904 · Rosewood 1923 · No indictment",
          "kurz": "5 · The colour line",
          "warum": "The lynching of Wash Bradley near Bronson in 1904 and the destruction of Rosewood in January 1923, from the reports of their time: who was named and who was not, how the violence was excused, and a grand jury that charged no one.",
          "quelle": "Ocala Evening Star 1904; NAACP, Thirty Years of Lynching (1919); Palatka Daily News, January 1923; Miami Daily Metropolis and Fort Pierce News-Tribune, February 1923; The Crisis 1923; Palm Beach Post 1924."})
order = ["before", "rails", "rock", "shipping", "line", "airfield"]
M["shipped"] = sorted([x for x in M["shipped"] if x["id"] != "line"] + [m], key=lambda x: order.index(x["id"]) if x["id"] in order else 99)
ADD = [
    {"id": "blackpress1923", "side": "colour", "kurz": "The Black press of 1923",
     "warum": "The Chicago Defender, the Baltimore Afro-American, the New York Amsterdam News and other Black newspapers reported on Rosewood in January 1923. They are in the public domain but were not accessible from here; only The Crisis has been read so far. They are the nearest the record of the time comes to the voices of Rosewood's people.",
     "quelle": "Black newspapers, January–March 1923."},
    {"id": "rosewood1994", "side": "colour", "kurz": "The Rosewood act of 1994",
     "warum": "In 1994 the Florida Legislature compensated survivors of Rosewood and their descendants. The act, an official text, can be printed once it has been read at the source; it has not been read yet.",
     "quelle": "Laws of Florida, 1994."},
    {"id": "levy1902", "side": "colour", "kurz": "The rumours of 1902",
     "warum": "After the murder of Mr. and Mrs. L. B. Lewis south of Bronson in 1902, the Ocala Evening Star reported rumours of lynchings. They are not confirmed and are not in the NAACP's list; they are not printed.",
     "quelle": "Ocala Evening Star, 1 September 1902, p. 2 (OCR only)."},
]
have = {x["id"] for x in M["missing"]}
M["missing"] += [x for x in ADD if x["id"] not in have]
(D / "modules.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- compare
C = json.loads((D / "compare.json").read_text(encoding="utf-8"))
PAIRS = [
    {"id": "count", "titel": "How many died at Rosewood?",
     "frage": "How did the count of the dead change in the reports of the time?",
     "note": "On 5 January five dead were “known” and many more “believed”. On 8 January the Associated Press counted seven, two white and five Black. In February the grand jury reports gave eight, two white and six Black, and the Miami report tied a ninth killing, the lynching of Abe Wilson near Newberry, to the same events. Only the white dead were named from the first day. The figure of eight remained the official one; later accounts dispute it.",
     "voices": [{"text": "line", "sec": "rosewood", "n": [3], "wer": "Associated Press, 5 January"},
                {"text": "line", "sec": "rosewood", "n": [5], "wer": "Associated Press, 8 January"},
                {"text": "line", "sec": "after", "n": [8], "wer": "Bronson, 17 February"}]},
    {"id": "judgement", "titel": "Two judgements",
     "frage": "How was the destruction of Rosewood judged in 1923?",
     "note": "A Florida editor found that Levy County's people deserved “no censure” and were “not actually ashamed”; a newspaper in Madras, reprinted by the NAACP, saw a “great blot on American civilization” and those responsible “let go unpunished”. The grand jury in between returned no indictment.",
     "voices": [{"text": "line", "sec": "after", "n": [6], "wer": "Palatka Daily News, 10 January"},
                {"text": "line", "sec": "after", "n": [10], "wer": "Swarajya (Madras), in The Crisis, June"}]},
    {"id": "named", "titel": "Who is named",
     "frage": "Whom do the reports name, and whom not?",
     "note": "In 1904 the paper names the victim of the shooting, the lynched man and the two Black men who caught him, but no one in the mob. In 1923 it names the white dead and wounded with their families on the first day, and the first Black victim, James Carrier, only when describing his killing; his killers are “several white men”. The only person ever named as a leader of the mob was named by the NAACP's magazine, not by any court.",
     "voices": [{"text": "line", "sec": "bronson", "n": [1], "wer": "Ocala Evening Star, 1904"},
                {"text": "line", "sec": "rosewood", "n": [4], "wer": "Associated Press, 6 January 1923"},
                {"text": "line", "sec": "after", "n": [9], "wer": "The Crisis, March 1923"}]},
]
pid = {p["id"] for p in PAIRS}
C["pairs"] = [p for p in C.get("pairs", []) if p["id"] not in pid] + PAIRS
(D / "compare.json").write_text(json.dumps(C, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- timeline
TL = json.loads((D / "timeline.json").read_text(encoding="utf-8"))
K = "#/text/line/"
NEWST = [
    {"d": "6 September 1904", "side": "colour", "titel": "Wash Bradley",
     "text": "Wash Bradley, a Black turpentine worker accused of killing Mrs. N. B. Barrow near Levyville, is tortured and lynched by a mob near Bronson. No one is charged.",
     "cite": K + "bronson/1", "citeLabel": "The colour line [1]", "plate": "oes1904_levyville",
     "quelle": "Ocala Evening Star, 7 September 1904, p. 1; NAACP, Thirty Years of Lynching (1919), p. 55."},
    {"d": "4–8 January 1923", "side": "colour", "titel": "Rosewood",
     "text": "Armed white men besiege a house at Rosewood and burn the Black settlement over several days; two white men and, by the official count, six Black residents are killed, among them James Carrier at his family's graves. The survivors flee into the woods.",
     "cite": K + "rosewood/3", "citeLabel": "The colour line [3]", "plate": "pdn1923_jan5",
     "quelle": "Palatka Daily News, 5, 7 and 8 January 1923 (Associated Press)."},
    {"d": "15 February 1923", "side": "colour", "titel": "No indictment",
     "text": "A special grand jury at Bronson finds that “sufficient evidence had not been found” to charge anyone for the killings and the burning of Rosewood.",
     "cite": K + "after/8", "citeLabel": "The colour line [8]", "plate": "fpnt1923_noindictment",
     "quelle": "Miami Daily Metropolis, 12 February 1923; Fort Pierce News-Tribune, 20 February 1923."},
]
titles = {s["titel"] for s in NEWST}
TL["stations"] = [s for s in TL["stations"] if s["titel"] not in titles] + NEWST
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def year(s):
    d = s["d"]
    m_ = re.search(r"\d{4}", d)
    mon = next((i + 1 for i, x in enumerate(MONTHS) if x in d), 13 if re.fullmatch(r"\d{4}–\d{4}", d) else 0)
    return (int(m_.group()) if m_ else 9999, mon, d)


TL["stations"].sort(key=year)
(D / "timeline.json").write_text(json.dumps(TL, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", sum(len(s["units"]) for s in T["sections"]), "units")
