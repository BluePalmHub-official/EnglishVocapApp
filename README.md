# Vocabulary Master

A desktop app that helps 11th-grade students build their vocabulary. It has **400 words in 20 lists of 20**, two kinds of quiz, and charts that show progress over time.

Built with Python, Tkinter, SQLite and Matplotlib.

## Features

- **Spelling Test:** the app shows a definition and part of speech, and the student types the word.
- **Meaning Test:** the app shows a word, and the student picks the right definition from four choices.
- **Choose your lists:** take a quiz on one list, several, or all 20.
- **Analytics:** overall statistics, a history of recent quizzes, and performance charts.
- **Works offline:** all words and results are stored in a small local SQLite database.

## Requirements

- Python 3 (developed and tested on 3.13)
- Tkinter, which comes with the standard Python installers for Windows and macOS. On Debian or Ubuntu Linux, install it with `sudo apt install python3-tk`.
- Matplotlib, for the analytics charts:

```bash
pip install -r requirements.txt
```

## Run it

```bash
git clone https://github.com/BluePalmHub-official/EnglishVocapApp.git
cd EnglishVocapApp
pip install -r requirements.txt
python3 main.py
```

The first time it starts, the app creates `vocabulary.db` next to the program and fills it with the 400 words. Quiz results are saved there afterwards. The file stays on your computer and is listed in `.gitignore`.

To start fresh, close the app and delete `vocabulary.db`. It is rebuilt on the next launch.

## Project layout

```
main.py             Main menu and list selection
spelling_quiz.py   Spelling test screens and scoring
meaning_quiz.py    Multiple-choice meaning test
analytics.py       Statistics, quiz history and charts
table.py           Database setup, the 400-word list, and saving results
vocabulary_app.spec   PyInstaller build recipe
requirements.txt   Python packages needed
```

### Database tables

| Table | Holds |
| --- | --- |
| `words` | word, part of speech, definition, list number |
| `quiz_history` | each quiz: type, lists used, score, date |
| `quiz_details` | each question: word, the answer given, right or wrong |
| `users` | created for future student profiles, not used yet |

To change or add words, edit the word list in `table.py`, delete `vocabulary.db`, and run the app again.

## Build a standalone app

```bash
pip install pyinstaller
pyinstaller vocabulary_app.spec
```

The program, named `VocabularyMaster`, appears in `dist/`. Build on the system you want to run it on.

## Contributing and reuse

This is a free, open project. Read it, learn from it and adapt it for your own classroom or project under the MIT License. Issues and suggestions are welcome.

## License

[MIT](LICENSE) © 2026 Dennis Quijano

Made by [BluePalm Hub](https://bluepalmhub.com), custom software for businesses and schools.
