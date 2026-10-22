# The course layout: 7 units (one for each chapter of the course notes), the XP rules,
# and how quizzes and tests are put together. The lessons themselves are in lessons.py.

import random
import time
from lessons import LESSONS

UNITS = [
    {"title": "Bits, qubits and the rules", "about": "Bits, gates, superposition, measuring and the H gate"},
    {"title": "Practice puzzles", "about": "Simplify, factor, measure, find circuits, and a flip game"},
    {"title": "Real quantum computers", "about": "Circuit diagrams, IBM's Quantum Composer and entanglement"},
    {"title": "Z, Control-Z and Toffoli", "about": "Gates that place minus signs, and a gate with two controls"},
    {"title": "Game: Rigged or fair?", "about": "One use of a machine answers a two-press question"},
    {"title": "Game: Find the gem", "about": "A quantum search through four lockers"},
    {"title": "Bell states and teleportation", "about": "Four entangled states, and moving a qubit's state"},
]
for number, unit in enumerate(UNITS, start=1):              # each lesson says which unit it belongs to
    unit["lessons"] = []
    for n, lesson in enumerate(LESSONS, start=1):
        if lesson["unit"] == number:
            unit["lessons"].append(n)

TOTAL_LESSONS = len(LESSONS)
MINUTES_PER_LESSON = 10

# XP
CHECK_IN_XP = 10      # right answer inside a lesson
QUIZ_XP = 10          # right answer in a quiz or test
LESSON_XP = 20        # finishing a lesson
TEST_XP = 100         # passing a unit test or the final test
XP_PER_LEVEL = 200
PASS_MARK = 70        # percent needed to pass a test
TEST_QUESTIONS = 12   # most questions in a unit test
FINAL_PER_UNIT = 2    # the final test asks about this many lessons from every unit

PACES = {"Casual": 1, "Steady": 2, "Intense": 3}    # lessons a day
TIMEZONE = "America/New_York"   # when a new day starts for streaks

# Achievements: each has goals that get harder. Reaching a goal moves it up a level.
# "counts" is what it keeps track of (see achievements() in engine/progress.py). {} in the task is the goal,
# and "noun" is added after the number, like "Finish 10 lessons".
ACHIEVEMENTS = [
    {"name": "Hot Streak", "icon": "flame", "counts": "best streak", "goals": [3, 7, 14, 30],
     "task": "Reach a {} day streak"},
    {"name": "Energy Level", "icon": "bolt", "counts": "xp", "goals": [100, 500, 1000, 2500], "task": "Earn {} XP"},
    {"name": "Pathfinder", "icon": "route", "counts": "lessons", "goals": [1, 10, 20, TOTAL_LESSONS],
     "task": "Finish {}", "noun": "lesson"},
    {"name": "Gatekeeper", "icon": "cnot", "counts": "unit tests", "goals": [1, 3, 5, len(UNITS)],
     "task": "Pass {}", "noun": "unit test"},
    {"name": "Spot On", "icon": "target", "counts": "right answers", "goals": [25, 100, 250, 500],
     "task": "Answer {} right", "noun": "question"},
    {"name": "Perfect Score", "icon": "star", "counts": "perfect tests", "goals": [1, 3, len(UNITS)],
     "task": "Score 100% on {}", "noun": "unit test"},
    {"name": "Graduate", "icon": "cap", "counts": "final test", "goals": [1], "task": "Pass the final test"},
]

# Nothing is saved yet (no backend), so logging in shows this sample progress: Unit 1 done, two lessons into Unit 2.
SAMPLE_PROGRESS = {"lessons_done": len(UNITS[0]["lessons"]) + 2, "tests": {1: 92}, "xp": 640,
                   "xp_week": [0, 0, 90, 120, 80, 110, 0], "streak": 4, "best_streak": 9,
                   "right": 32, "asked": 36, "joined": "October 2026"}


def new_quiz(kind, number=None):
    """Questions for a lesson quiz (kind="lesson"), a unit test ("unit") or the final test ("final").
    Each question is kept with the number of the lesson it came from."""
    if kind == "lesson":
        title = f"Lesson {number} quiz · {LESSONS[number - 1]['title']}"
        questions = [(number, question) for question in LESSONS[number - 1]["quiz"]]
    elif kind == "unit":
        title = f"Unit {number} test · {UNITS[number - 1]['title']}"
        questions = []
        for n in UNITS[number - 1]["lessons"]:                  # every quiz question in the unit...
            for question in LESSONS[n - 1]["quiz"]:
                questions.append((n, question))
        questions = random.sample(questions, min(len(questions), TEST_QUESTIONS))   # ...then pick some at random
    else:
        title = f"Final test · All {len(UNITS)} units"
        questions = []
        for unit in UNITS:                                          # a few random lessons from every unit,
            for n in sorted(random.sample(unit["lessons"], FINAL_PER_UNIT)):
                questions.append((n, random.choice(LESSONS[n - 1]["quiz"])))   # one question from each
    return {"id": int(time.time() * 1000), "kind": kind, "number": number, "title": title, "questions": questions,
            "index": 0, "results": [], "xp": 0, "started": time.time()}