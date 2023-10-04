# Anki Jouyou Deck Scripts
The goal of this project is to create an anki deck with all jouyou kanji, meanings, sentences, ideally pictures, voice recording of sentences, and most common readings. Additional data may be provided as well.

## Tools Used
- Scripting: Python is being used for all scripting needs since it's simple to work with.
- Kanji Data:
  - [KanjiApi](https://kanjiapi.dev/): Used to retrieve any necessary data for kanji such as jlpt level, readings, and a couple other fields
  - [Kanji Datasets](https://github.com/davidluzgouveia/kanji-data): A couple json files already containing some good starting data in terms of kanji. Some things are missing, such as accurate new jlpt count, which falls short a couple hundred. This issue is fixed by using the kanjiapi on those kanji missing levels info
  - [Amazon Polly](https://aws.amazon.com/polly/): This will likely be used for the Text-To-Speech functionality for sentences and readings. May change in the future

This is still a WIP. Once everything is finalized, anki deck links and additional info will be added here.