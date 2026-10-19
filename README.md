# Qubi

Learn quantum computing with shapes, boxes and mists, with no heavy math. Qubi is a free course of 6 units and 18 short lessons. Every lesson ends with a quiz, every unit ends with a test, and there's a final test at the end. In the Circuit Lab you can build your own circuits and export them to run on IBM's real quantum computers.

Made for the 2026 Congressional App Challenge.

## Run it

You need Python 3.11 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run main.py
```

Qubi opens in your browser at http://localhost:8501.

## Check it

```bash
python -m tests.test_qubits      # the quantum engine: boxes, mists, the games, teleporting, IBM export
python -m tests.test_lessons     # every lesson and quiz answer, checked with the engine
```

## What's where

| File | What it does |
|---|---|
| `main.py` | Starts the app: theme, pages, who can see what, and the sidebar |
| `course.py` | The 6 units, the XP rules, and how quizzes and tests are put together |
| `lessons.py` | All 18 lessons and their quizzes |
| `engine/qubits.py` | The quantum engine: shapes, mists and boxes (gates) |
| `engine/qasm.py` | Turns a Circuit Lab circuit into OpenQASM 2.0 for IBM Quantum Composer |
| `engine/ui.py` | The dark and light themes, and every drawing |
| `engine/parts.py` | Small pieces used on many pages: logo, icons, rings and cards |
| `engine/widgets.py` | The top bar, answer buttons and feedback bar for lessons and quizzes |
| `engine/progress.py` | XP, streaks, levels and what to do next |
| `pages/` | One file per page |
| `tests/` | The two checks above |
| `.streamlit/config.toml` | Theme colors and app settings |

## Good to know

Accounts are a demo for now and nothing is saved yet. Refreshing the page logs you out, Log in shows sample progress, and Google sign-in is coming soon.

## Credits

Qubi is built on the ideas in *Q is for Quantum* by Terry Rudolph. The lessons, pictures and games are our own, and Qubi isn't connected to or endorsed by the author.