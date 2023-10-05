import json
import asyncio
from kanjiApi import fetchKanjiData
import os
# print(os.listdir())

f = open("./_jouyou.json")
data = json.load(f)

# Turn json data into a list of objects
"""
Go from format:
{
  "一": {
      "strokes": 1,
      "grade": 1,
      "freq": 2,
      "jlpt_old": 4,
      "jlpt_new": 5,
      "meanings": ["One","One Radical (no.1)"],
      "readings_on": ["いち","いつ"],
      "readings_kun": ["ひと-","ひと.つ"],
      "wk_level": 1,
      "wk_meanings": ["One"],
      "wk_readings_on": ["いち","いつ"],
      "wk_readings_kun": ["!ひと"],
      "wk_radicals": ["Ground"]
  },
  "二": {
      "strokes": 2,
      "grade": 1,
      "freq": 9,
      "jlpt_old": 4,
      "jlpt_new": 5,
      "meanings": ["Two","Two Radical (no. 7)"],
      "readings_on": ["に","じ"],
      "readings_kun": ["ふた","ふた.つ","ふたたび"],
      "wk_level": 1,
      "wk_meanings": ["Two"],
      "wk_readings_on": ["に"],
      "wk_readings_kun": ["!ふた"],
      "wk_radicals": ["Two"]
  }
}

to format:
[
  {
    "kanji": "一",
    "strokes": 1,
    "grade": 1,
    "freq": 2,
    "jlpt_old": 4,
    "jlpt_new": 5,
    "meanings": ["One","One Radical (no.1)"],
    "readings_on": ["いち","いつ"],
    "readings_kun": ["ひと-","ひと.つ"],
    "wk_level": 1,
    "wk_meanings": ["One"],
    "wk_readings_on": ["いち","いつ"],
    "wk_readings_kun": ["!ひと"],
    "wk_radicals": ["Ground"]
  },
  {
    "kanji": "二",
    "strokes": 2,
    "grade": 1,
    "freq": 9,
    "jlpt_old": 4,
    "jlpt_new": 5,
    "meanings": ["Two","Two Radical (no. 7)"],
    "readings_on": ["に","じ"],
    "readings_kun": ["ふた","ふた.つ","ふたたび"],
    "wk_level": 1,
    "wk_meanings": ["Two"],
    "wk_readings_on": ["に"],
    "wk_readings_kun": ["!ふた"],
    "wk_radicals": ["Two"]
  }
]
"""
result = [{"kanji": k, **v} for k, v in data.items()]
# 2136, which is number of jouyou kanji
# print(len(result))

count = {
  "old": 0,
  "new": 0
}

newNotCounted = []

for i in result:
  count["old"] += 1 if i["jlpt_old"] != None else 0
  count["new"] += 1 if i["jlpt_new"] != None else 0

  if i["jlpt_new"] == None:
    newNotCounted.append(i["kanji"]) 

# print(count)
print(newNotCounted)
newNotCountedRes = asyncio.run(fetchKanjiData(newNotCounted))
print(newNotCountedRes)