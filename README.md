# Qubi

Learn quantum computing with shapes, gates and clouds, with no heavy math. Qubi is a free course of 7 units and 31 short lessons, made for people who have never studied computers or quantum physics. Every lesson ends with a quiz, every unit ends with a test, and there's a final test at the end. Streaks, XP and achievements keep you going. In the Circuit Lab you can build your own circuits and export them to run on IBM's real quantum computers.

Made for the 2026 Congressional App Challenge.

## Run it

You need Python 3.11 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run main.py
```

Qubi opens in your browser at https://qubi-quantum.streamlit.app/

## Check it

```bash
python -m tests.test_qubits      # the quantum engine: gates, superpositions, the games, teleporting, IBM export
python -m tests.test_lessons     # every lesson and quiz answer, checked with the engine
```

## What's where

| File | What it does |
|---|---|
| `main.py` | Starts the app: theme, pages, who can see what, and the sidebar |
| `course.py` | The 7 units, the XP rules, the achievements, and how quizzes and tests are put together |
| `lessons.py` | All 31 lessons and their quizzes |
| `engine/qubits.py` | The quantum engine: shapes, superpositions, gates and measuring |
| `engine/qasm.py` | Turns a Circuit Lab circuit into OpenQASM 2.0 for IBM Quantum Composer |
| `engine/ui.py` | The dark and light themes, and every drawing |
| `engine/parts.py` | Small pieces used on many pages: logo, icons, rings, cards and achievement badges |
| `engine/landing.py` | The welcome page's styles and its animated qubit picture |
| `engine/widgets.py` | The top bar, answer buttons and feedback bar for lessons and quizzes |
| `engine/store.py` | Google sign-in, and loading and saving progress in Supabase |
| `engine/progress.py` | XP, streaks, levels, achievements and what to do next |
| `pages/` | One file per page |
| `tests/` | The two checks above |
| `.streamlit/config.toml` | Theme colors and app settings |
| `SETUP.md` | How to set up Google sign-in and saving |

## Accounts and saving

Sign in with Google and your progress is saved to a Supabase database, so it's still there on any device. You can also try Qubi as a guest, but then nothing is saved. To turn on Google sign-in and saving, follow [SETUP.md](SETUP.md).

## Credits

Qubi is built on the ideas in the Virginia Tech Quantum Information Science and Engineering Summer School notes by Sophia Economou, Edwin Barnes and Jamie Sikora, and in *Q is for Quantum* by Terry Rudolph. The lessons are written in our own words, the pictures and games are our own, and Qubi isn't connected to or endorsed by these authors or by Virginia Tech.

The numbers on the welcome page come from Google, McKinsey & Company, IBM (via The Quantum Insider) and NIST, and each one links to its source at the bottom of the page. The snow leopard photo is by Helena Lopes on Unsplash (free to use under the Unsplash License).
