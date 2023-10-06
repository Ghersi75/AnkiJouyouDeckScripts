import json
from utils import loadJson

if __name__ == "__main__":
  grade1Sentences = loadJson("./_grade1Sentences.json")
  frequencyKtoN = loadJson("./_frequencyKanjiToNumber.json")
  frequencyNtoK = loadJson("./_frequencyNumberToKanji.json")

  # Rank sentences based on the kanji used in them
  s = []
  for kanji, entry in grade1Sentences.items():
    s.append({
      kanji: entry
    })

  s = sorted(s, key=lambda x: int(frequencyKtoN[list(x.keys())[0]]))

  for e in s:
    kanji = list(e.keys())[0]
    print("Kanji: ", kanji, " Ranking: ", frequencyKtoN[kanji])
