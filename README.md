# Anki Jouyou Deck Scripts
The goal of this project is to create an anki deck with all jouyou kanji, meanings, sentences, ideally pictures, voice recording of sentences, and most common readings. Additional data may be provided as well.

## What this project will make
- Jouyou deck split by grade, and cards sorted by frequency based on top 2500 most frequent kanji. If not in that set, the kanji will go towards the end
- Frequency deck based on frequency from frequency 2500 json/txt file pulled from jisho admin's github. This file is 8 years old so it might be slightly off, but I assume it will hold up for the most part
- Wanikani levels maybe? This would be useful for those of us who want to follow this level based system but don't wanna have deal with wanikani locking you in at each level without option to move on on your own

## Tools Used
- Scripting: Python is being used for all scripting needs since it's simple to work with.
- Kanji Data:
  - [KanjiApi](https://kanjiapi.dev/): Used to retrieve any necessary data for kanji such as jlpt level, readings, and a couple other fields
  - [Kanji Datasets](https://github.com/davidluzgouveia/kanji-data): A couple json files already containing some good starting data in terms of kanji. I was mistaken in my initial understanding of this data set. I initially assumed JLPT and Jouyou kanji aligned perfectly, but they do not. This set contains the kanji as needed, and there's actually nothing missing from it. Some kanji are in here and may not be in the N1 and vice versa. If everything goes well, I will likely create a separate deck for JLPT Kanji as well for the missing Kanji, or all of it as a deck. Have yet to see what happens.
  - [Amazon Polly](https://aws.amazon.com/polly/): This will likely be used for the Text-To-Speech functionality for sentences and readings. May change in the future
  - [Tatoeba API](https://en.wiki.tatoeba.org/articles/show/api#api): This will likely end up being used for example sentences. A discord user from a large english-japanese exchange server did mention that tatoeba may not be the most accurate, so I will try my best to be careful. Unfortunately I don't have the comprehension level nor the time to look through what will likely be thousands of sentences, so I'll try to add some sort of feedback system at some point later down the line. Or I'll just release it and let people change sentences as they see fit within their own Anki application.

This is still a WIP. Once everything is finalized, anki deck links and additional info will be added here.
