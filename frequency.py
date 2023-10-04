# File is from jisho forum in which admin responded with link below https://jisho.org/forum/55a771a26e733423e86a0700-most-used-kanji-in-newspapers
# Direct link: https://gist.github.com/Kimtaro/50da080ff3cf6202f55a
file = open("2500frequency.txt", "r")
lines = [line.strip() for line in file.readlines() if line.strip()]
file.close()

res = dict()

for line in lines:
  n = int(line[0:line.index(":")])
  kanji = line[-1]
  res[n] = kanji
  
import json

jsonRes = json.dumps(res)
with open("frequency.json", "w+") as f:
  f.write(jsonRes)
