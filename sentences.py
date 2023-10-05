import json
import asyncio
from kanjiApi import asyncRequests
from os import system

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

def parseSentences(sentencesRaw, apiCallLinks, kanjiData):
  kanjiString = kanjiData["kanji"]
  """
  {
    "kanji": {
      "on": {
        "on1": ...,
        "on2": ...
      },
      "kun": {
        "kun1": ...,
        "kun2": ...
      }
    }
  }
  """
  parsedSentences = {
    kanjiString: {
      "on": {onyomi.strip().replace("!", ""): {
        "sentences": [],
        "api_call_link": ""
      } for onyomi in kanjiData["onyomi"]},
      "kun": {kunyomi.strip().replace("!", ""): {
        "sentences": [],
        "api_call_link": ""
      } for kunyomi in kanjiData["kunyomi"]}
    }
  }
  # print(parsedSentences)

  def parseSentencesHelper(start = 0, end = 0):
    for i in range(start, end):
      for j in range():
        return
  
  # Onyomi is run first
  numOn = len(kanjiData["onyomi"])
  numKun = len(kanjiData["kunyomi"])

  # Go through Onyomi first
  for i in range(numOn):
    currOn = kanjiData["onyomi"][i].strip().replace("!", "")
    parsedSentences[kanjiString]["on"][currOn]["api_call_link"] = apiCallLinks[i]
    # print("CurrOn: ", currOn)
    for j in range(len(sentencesRaw[i]["results"])):
      currResult = sentencesRaw[i]["results"][j]
      # [print(translation[0]["text"]) for translation in currResult["translations"] if translation != []]
      parsedSentences[kanjiString]["on"][currOn]["sentences"].append({
        "sentence": currResult["text"],
        "translations": [translation[0]["text"] for translation in currResult["translations"] if translation != []],
        "transcription": {
          "text": currResult["transcriptions"][0]["text"] if currResult["transcriptions"] != [] else None,
          "html": currResult["transcriptions"][0]["html"] if currResult["transcriptions"] != [] else None
        }
      })
  
  # print("\n")
  for i in range(numOn, numOn + numKun):
    currKun = kanjiData["kunyomi"][i - numOn].strip().replace("!", "")
    parsedSentences[kanjiString]["kun"][currKun]["api_call_link"] = apiCallLinks[i]
    # print("CurrKun: ", currKun)
    for j in range(len(sentencesRaw[i]["results"])):
      currResult = sentencesRaw[i]["results"][j]
      parsedSentences[kanjiString]["kun"][currKun]["sentences"].append({
        "sentence": currResult["text"],
        "translations": [translation[0]["text"] for translation in currResult["translations"] if translation != []],
        "transcription": {
          "text": currResult["transcriptions"][0]["text"] if currResult["transcriptions"] != [] else None,
          "html": currResult["transcriptions"][0]["html"] if currResult["transcriptions"] != [] else None
        }
      })
    
  # return ""
  return parsedSentences

import urllib.parse
# Gonna need some magic async stuff here too for each kanji to fetch all the sentences it needs for all the readings
async def getSentencesFromKanji(kanjiList):
  urlStart = "https://tatoeba.org/en/api_v0/search?from=jpn&has_audio=any&native=yes&orphans=no&query="
  urlEnd = "&sort=relevance&to=eng&trans_to=eng&user=%22CK%22&orphans=no&unapproved=no"
  # print(kanjiList[0])
  reqs = [{
    kanji["kanji"]: {}
  } for kanji in kanjiList]
  # print(reqs)
  parsedSentences = {
    kanji["kanji"]: {} for kanji in kanjiList
  }
  for kanji in kanjiList:
    # print(kanji)
    currKanjiReqs = []
    # print(f"Kanji: {kanji} \nOn: ")
    for onyomi in kanji["onyomi"]:
      onyomi = onyomi.replace("!", "")
      # print(onyomi)
      req = urlStart + f"""{urllib.parse.quote(kanji["kanji"])}{urllib.parse.quote(onyomi)}""" + urlEnd
      currKanjiReqs.append(req)
    # print("Kun: ")
    for kunyomi in kanji["kunyomi"]:
      kunyomi = kunyomi.replace("!", "")
      # print(kunyomi)
      req = urlStart + f"""{urllib.parse.quote(kanji["kanji"])}{urllib.parse.quote(kunyomi)}""" + urlEnd
      currKanjiReqs.append(req)
    currKanjiSentences = await asyncRequests(currKanjiReqs)
    parsedKanjiSentences = parseSentences(currKanjiSentences, currKanjiReqs, kanji)
    system("clear")
    print(f"Completed {kanjiList.index(kanji) + 1} / {len(kanjiList)}")
    parsedSentences[kanji["kanji"]] = parsedKanjiSentences[kanji["kanji"]]

  return parsedSentences
    # print(currKanjiReqs) 
  # for i in reqs:
  #   print(i)
  # # print[requests[0]]
  # res1 = asyncio.run(asyncRequests(reqs[0:len(reqs) // 2]))
  # res2 = asyncio.run(asyncRequests(reqs[len(reqs) // 2:]))
  # # print(res)
  # return res1 + res2

# freqTest = getKanjiByGradeFromJouyou(1)
# print(grade1)
# freqTest = getKanjiByFrequency(1555,1555)
# print(freqTest)
def GetSentencesByFrequency(kanjiList):
  freqTestSentences = []
  for kanji in kanjiList.values():
    obj = {
      "kanji": kanji,
      "kunyomi": jouyouJson[kanji]["wk_readings_kun"] or [],
      "onyomi": jouyouJson[kanji]["wk_readings_on"] or []
    }
    freqTestSentences.append(obj)
  # print(freqTestSentences)
  freqTestSentencesTest = getSentencesFromKanji(freqTestSentences)
  # print(freqTestSentencesTest)
  f = open(f"_sentenceDataByFrequency.json", "w+")
  # print(freqTestSentencesTest)
  # print(json.dumps(freqTestSentencesTest))
  f.write(json.dumps(freqTestSentencesTest))
  f.close()

def GetSentencesByJouyouGrade(grade):
  gradeKanji = getKanjiByGradeFromJouyou(grade)
  sentenceRequests = []
  for kanji in gradeKanji:
    obj = {
      "kanji": kanji,
      "kunyomi": jouyouJson[kanji]["wk_readings_kun"] or [],
      "onyomi": jouyouJson[kanji]["wk_readings_on"] or []
    }
    sentenceRequests.append(obj)
  # print(freqTestSentences)
  sentencesByGrade = asyncio.run(getSentencesFromKanji(sentenceRequests))
  # print(freqTestSentencesTest)
  f = open(f"_grade{grade}Sentences.json", "w+")
  # print(freqTestSentencesTest)
  # print(json.dumps(freqTestSentencesTest))
  f.write(json.dumps(sentencesByGrade))
  f.close()

def GetSentencesByKanjiList(kanjiList):
  sentenceRequests = []
  for kanji in kanjiList:
    obj = {
      "kanji": kanji,
      "kunyomi": jouyouJson[kanji]["wk_readings_kun"] or [],
      "onyomi": jouyouJson[kanji]["wk_readings_on"] or []
    }
    sentenceRequests.append(obj)
  # print(freqTestSentences)
  sentencesByGrade = asyncio.run(getSentencesFromKanji(sentenceRequests))
  # print(freqTestSentencesTest)
  # print(sentencesByGrade)
  f = open("_jouyouSentenceData.json", "w+")
  # print(freqTestSentencesTest)
  # print(json.dumps(freqTestSentencesTest))
  f.write(json.dumps(sentencesByGrade))
  f.close()

if __name__ == "__main__":
  GetSentencesByJouyouGrade(2)
  # GetSentencesByKanjiList(getKanjiByFrequency(4, 4).values())
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
  