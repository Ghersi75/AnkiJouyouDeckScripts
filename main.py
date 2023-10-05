import json
import asyncio
from kanjiApi import asyncRequests
import os
# print(os.listdir())

f = open("./_jouyou.json")
data = json.load(f)

# Turn json data into a list of objects
"""
Go from format:
{
  "一": {
    // other fields
  },
  "二": {
    // other fields
  }
}

to format:
[
  {
    "kanji": "一",
    // other fields
  },
  {
    "kanji": "二",
    // other fields
  }
]
"""
result = [{"kanji": k, **v} for k, v in data.items()]
# 2136, which is number of jouyou kanji
# print(len(result))

# """
# Count highest kun and on reading kanji and split them up by how many readings of each they all have
c = dict()
noWaniKun = 0
noWaniOn = 0
noReading = 0
readings = {
  "kunMax": 0,
  "onMax": 0,
  "kunAmountToKanji": dict(),
  "onAmountToKanji": dict()
}
for i in result:
  grade = i["grade"]
  if i["wk_readings_on"] == [] or i["wk_readings_on"] == None:
    noWaniOn += 1
  else:
    currReadings = len(i["wk_readings_on"])
    readings["onMax"] = max(readings["onMax"], currReadings)
    if currReadings in readings["onAmountToKanji"]:
      readings["onAmountToKanji"][currReadings].append(i["kanji"])
    else:
      readings["onAmountToKanji"][currReadings] = [i["kanji"]]
  
  if i["wk_readings_kun"] == [] or i["wk_readings_kun"] == None:
    noWaniKun += 1
  else:
    currReadings = len(i["wk_readings_kun"])
    readings["kunMax"] = max(readings["kunMax"], currReadings)
    if currReadings in readings["kunAmountToKanji"]:
      readings["kunAmountToKanji"][currReadings].append(i["kanji"])
    else:
      readings["kunAmountToKanji"][currReadings] = [i["kanji"]]
  
  if i["wk_readings_kun"] == [] and i["wk_readings_on"] == []:
    noReading += 0

  # if grade == 1:
    # BAD LINE
    # print(f"Kanji: {i["kanji"]}, Kunyomi: {i["wk_readings_on"]}, Onyomi: {i["wk_readings_kun"]}")

  if grade not in c:
    c[grade] = 1
  else:
    c[grade] += 1

s = 0
for i in c.values():
  s += i

print(f"Kun: {noWaniKun}, On: {noWaniOn}, Neither: {noReading}")
print("Readings: ", readings["kunAmountToKanji"][6])
print(s)
print(c)
# """


"""
# Count old and new jlpt levels and search data for kanji missing it
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
# print(newNotCountedRes)
for i in newNotCountedRes:
  print(i["jlpt"] == None)
"""