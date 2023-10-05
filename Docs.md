# Docs
This file will be used to roughly keep track of what files to what, what kind of return types to expect from api calls, and whatever else comes up.

## Tatoeba API Return Type
Since the example would have been too long, there's now a `_tatoebaExample.json` file.

## Sentence Data file type
```json
{
  [kanji]: {
    "kun": {
      [reading_n]: {
        "sentences": [
          {
            "sentence": "Example sentences",
            "translations": [
              "Translation 1",
              "Translation 2",
              "Translation 3",
            ]
          }
        ]
      }
    },
    "on": {
      [reading_n]: {
        "sentences": [
          {
            "sentence": "Example sentences",
            "translations": [
              "Translation 1",
              "Translation 2",
              "Translation 3",
            ],
            "transcription": "HTML Transcription"
          }
        ],
        "api_call_link": "link"
      }
    }
  }
}
```
Example:
```json
{
  "日": {
    "kun": {
      "ひ": {
        "sentences": [
          {
            "sentence": "雪の日は、出かけません。",
            "translations": [
              "I don't go anywhere on days when there's snow."
            ],
            "transcription": "<ruby>雪<rp>（</rp><rt>ゆき</rt><rp>）</rp></ruby>の<ruby>日<rp>（</rp><rt>ひ</rt><rp>）</rp></ruby>は、<ruby>出<rp>（</rp><rt>で</rt><rp>）</rp></ruby>かけません。"
          }
        ],
        "api_call_link": "https://tatoeba.org/en/api_v0/search?from=jpn&has_audio=yes&native=yes&orphans=no&query=%E6%97%A5%E3%81%B2&sort=relevance&to=eng&trans_to=eng&user=%22CK%22&orphans=no&unapproved=no"
      }
    },
    "on": {
      "にち": {
        "sentences": [
          {
            "sentence": "冬休み何日から？",
            "translations": [
              "When does your winter vacation begin?",
              "When do the Christmas holidays begin?"
            ],
            "transcription": "<ruby>冬<rp>（</rp><rt>ふゆ</rt><rp>）</rp></ruby><ruby>休<rp>（</rp><rt>やす</rt><rp>）</rp></ruby>み<ruby>何<rp>（</rp><rt>なん</rt><rp>）</rp></ruby><ruby>日<rp>（</rp><rt>にち</rt><rp>）</rp></ruby>から？"
          }
        ],
        "api_call_link": "https://tatoeba.org/en/api_v0/search?from=jpn&has_audio=yes&native=yes&orphans=no&query=%E6%97%A5%E3%81%AB%E3%81%A1&sort=relevance&to=eng&trans_to=eng&user=%22CK%22&orphans=no&unapproved=no"
      }
    }
  }
}

```