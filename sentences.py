import json
import asyncio
from kanjiApi import asyncRequests

freq = open("./_frequency.json")
freqJson = json.load(freq)
freq.close()

jouyou = open("./_jouyou.json")
jouyouJson = json.load(jouyou)
jouyou.close()

def getKanjiByGradeFromJouyou(grade):
  res = []
  for kanji, entry in jouyouJson.items():
    if entry["grade"] == grade:
      res.append(kanji)
  return res

# Must be 1-2501 index to keep it consistent with the frequency file
def getKanjiByFrequency(start = 1, end = 2501):
  if start < 1 or end > 2501:
    raise Exception("Start must be greater than or equal to 1 and end must be less than or equal to 2501")
  else:
    res = dict()
    for i in range(start, end + 1):
      res[i] = freqJson[str(i)]
      
  return res

# [
#   {
#     "kanji": 
#     "onyomi": 
#     "kunyomi": 
#   }
# ]

import urllib.parse
# Gonna need some magic async stuff here too for each kanji to fetch all the sentences it needs for all the readings
def getSentencesFromKanji(kanjiList):
  urlStart = "https://tatoeba.org/en/api_v0/search?from=jpn&has_audio=yes&native=yes&orphans=no&query="
  urlEnd = "&sort=relevance&to=eng&trans_to=eng&user=%22CK%22&orphans=no&unapproved=no"
  reqs = []
  for kanji in kanjiList:
    for onyomi in kanji["onyomi"]:
      onyomi = onyomi.replace("!", "")
      req = urlStart + f"""{urllib.parse.quote(kanji["kanji"])}{urllib.parse.quote(onyomi)}""" + urlEnd
      reqs.append(req)
    for kunyomi in kanji["kunyomi"]:
      kunyomi = kunyomi.replace("!", "")
      req = urlStart + f"""{urllib.parse.quote(kanji["kanji"])}{urllib.parse.quote(kunyomi)}""" + urlEnd
      reqs.append(req)
  for i in reqs:
    print(i)
  # print[requests[0]]
  res = asyncio.run(asyncRequests(reqs))
  # print(res)
  return res

grade1 = getKanjiByGradeFromJouyou(1)
# print(grade1)
freqTest = getKanjiByFrequency(1,1)
print(freqTest)
freqTestSentences = []
for kanji in freqTest.values():
  obj = {
    "kanji": kanji,
    "kunyomi": jouyouJson[kanji]["wk_readings_kun"] or [],
    "onyomi": jouyouJson[kanji]["wk_readings_on"] or []
  }
  freqTestSentences.append(obj)
# print(freqTestSentences)
freqTestSentencesTest = getSentencesFromKanji(freqTestSentences)
# print(freqTestSentencesTest)
f = open("_sentenceData.json", "w+")
# print(freqTestSentencesTest)
# print(json.dumps(freqTestSentencesTest))
f.write(json.dumps(freqTestSentencesTest))
f.close()
# Works good
# print(getKanjiByFrequency(2001,2003))


"""
# Count jouyou not in frequency set (97)
fset = set()
for f in freqJson.values():
  fset.add(f)

# print(fset)
c = 0
for j in jouyouJson.keys():
  if j not in fset:
    c += 1

# 97 not in top 2500 frequency kanji list
print(c)
"""
  