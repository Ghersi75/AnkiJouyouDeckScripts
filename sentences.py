from genericpath import isfile
import json
import asyncio
from kanjiApi import asyncRequests
from os import system
import sys
from utils import createFile, loadJson, saveJson
import urllib.parse

jouyouJson = loadJson("./_jouyou.json")

def getKanjiByGradeFromJouyou(grade):
  res = []
  for kanji, entry in jouyouJson.items():
    if entry["grade"] == grade:
      res.append(kanji)
  return res

# Must be 1-2501 index to keep it consistent with the frequency file
def getKanjiByFrequency(start = 1, end = 2501):
  freqJson = loadJson("./_frequencyNumberToKanji.json")
  if start < 1 or end > 2501:
    raise Exception("Start must be greater than or equal to 1 and end must be less than or equal to 2501")
  else:
    res = dict()
    for i in range(start, end + 1):
      res[i] = freqJson[str(i)]
      
  return res

def parseSentences(sentencesRaw, apiCallLinks, kanjiData):
  # Create initial object for storing data based on onyomi, kunyomi, and all associated fields
  parsedSentences = {
    "on": {onyomi.strip().replace("!", ""): {
      "sentences": [],
      "api_call_link": ""
    } for onyomi in kanjiData["onyomi"]},
    "kun": {kunyomi.strip().replace("!", ""): {
      "sentences": [],
      "api_call_link": ""
    } for kunyomi in kanjiData["kunyomi"]}
  }
  
  # Onyomi is run first
  numOn = len(kanjiData["onyomi"])
  numKun = len(kanjiData["kunyomi"])

  # Helper function used to extract useful data for both onyomi and kunyomi
  def parseSentencesHelper(yomi):
    offset = 0
    indexes = range(0)
    if yomi == "on":
      print("on")
      indexes = range(numOn)
    if yomi == "kun":
      print("kun")
      indexes = range(numOn, numOn + numKun)
      offset = numOn
    print(indexes)
    for i in indexes:
      currYomi = kanjiData[f"{yomi}yomi"][i - offset].strip().replace("!", "")
      parsedSentences[yomi][currYomi]["api_call_link"] = apiCallLinks[i]
      for j in range(len(sentencesRaw[i]["results"])):
        currResult = sentencesRaw[i]["results"][j]
        parsedSentences[yomi][currYomi]["sentences"].append({
          "sentence": currResult["text"],
          "translations": [translation[0]["text"] for translation in currResult["translations"] if translation != []],
          "transcription": {
            "text": currResult["transcriptions"][0]["text"] if currResult["transcriptions"] != [] else None,
            "html": currResult["transcriptions"][0]["html"] if currResult["transcriptions"] != [] else None
          }
        })
  parseSentencesHelper("on")
  parseSentencesHelper("kun")

  return { kanjiData["kanji"]: parsedSentences }

async def getSentencesFromKanji(kanjiList):

  urlStart = "https://tatoeba.org/en/api_v0/search?from=jpn&has_audio=any&native=yes&orphans=no&sort=relevance&to=eng&trans_to=eng&user=%22CK%22&orphans=no&unapproved=no&query="

  parsedSentences = { }

  for kanji in kanjiList:
    currKanjiReqs = []
    def yomiHelper(yomi):
      if yomi not in ["on", "kun"]: 
        raise Exception("Input must be \"on\" or \"kun\"")
      fullYomi = yomi + "yomi"
      for yomi in kanji[fullYomi]:
        yomi = yomi.strip().replace("!", "")
        urlParsedKanji = urllib.parse.quote(kanji["kanji"])
        urlParsedOnyomi = urllib.parse.quote(yomi)
        req = urlStart + urlParsedKanji + urlParsedOnyomi
        currKanjiReqs.append(req)

    yomiHelper("on")
    yomiHelper("kun")

    # Fetch data from api
    currKanjiSentences = await asyncRequests(currKanjiReqs)
    # Parse sentences
    parsedKanjiSentences = parseSentences(currKanjiSentences, currKanjiReqs, kanji)
    # Clear terminal and update how many kanji have been done
    system("clear")
    print(f"Completed {kanjiList.index(kanji) + 1} / {len(kanjiList)}")
    currKanji = kanji["kanji"]
    parsedSentences[currKanji] = parsedKanjiSentences[currKanji]

  return parsedSentences

def GetSentencesByFrequency(kanjiList):
  freqTestSentences = []
  for kanji in kanjiList.values():
    obj = {
      "kanji": kanji,
      "kunyomi": jouyouJson[kanji]["wk_readings_kun"] or [],
      "onyomi": jouyouJson[kanji]["wk_readings_on"] or []
    }
    freqTestSentences.append(obj)
  freqTestSentencesTest = getSentencesFromKanji(freqTestSentences)
  saveJson("_sentenceDataByFrequency.json", freqTestSentencesTest)

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

  sentencesByGrade = asyncio.run(getSentencesFromKanji(sentenceRequests))

  saveJson(f"_grade{grade}Sentences.json", sentencesByGrade)

def GetSentencesByKanjiList(kanjiList):
  sentenceRequests = []
  for kanji in kanjiList:
    obj = {
      "kanji": kanji,
      "kunyomi": jouyouJson[kanji]["wk_readings_kun"] or [],
      "onyomi": jouyouJson[kanji]["wk_readings_on"] or []
    }
    sentenceRequests.append(obj)
  sentencesByGrade = asyncio.run(getSentencesFromKanji(sentenceRequests))

  saveJson("_jouyouSentenceData.json", sentencesByGrade)

def GenerateKanjiFieldsByGrade(grade):
  path = f"_grade{grade}sentences.json"
  if not isfile(path):
    return


if __name__ == "__main__":
  system("clear")
  # GetSentencesByKanjiList(getKanjiByFrequency(4, 4).values())
  GetSentencesByJouyouGrade(1)