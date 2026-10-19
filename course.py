# The course layout: 6 units, which lessons are in each, the XP rules, and how quizzes are put together.
# The lessons themselves are in lessons.py.

import random
import time
from lessons import LESSONS

UNITS = [
    {"title": "Computers, bits and gates", "about": "Bits as shapes, gates as boxes", "lessons": [1, 2, 3, 4]},
    {"title": "Going quantum", "about": "Mists, measuring and the H box", "lessons": [5, 6, 7, 8, 9]},
    {"title": "Your first quantum trick", "about": "Beat a puzzle, then build and run your own circuits", "lessons": [10, 11, 12]},
    {"title": "More gates", "about": "Minus signs, Z and Toffoli", "lessons": [13, 14]},
    {"title": "The game show", "about": "Quantum tricks that beat the odds", "lessons": [15, 16]},
    {"title": "Entanglement at work", "about": "Linked mists and teleporting", "lessons": [17, 18]},
]
TOTAL_LESSONS = len(LESSONS)
MINUTES_PER_LESSON = 12

# XP
CHECK_IN_XP = 10      # right answer inside a lesson
QUIZ_XP = 10          # right answer in a quiz or test
LESSON_XP = 20        # finishing a lesson
TEST_XP = 100         # passing a unit test or the final test
XP_PER_LEVEL = 200
PASS_MARK = 70        # percent needed to pass a test

PACES = {"Casual": 1, "Steady": 2, "Intense": 3}    # lessons a day

# Nothing is saved yet (no backend), so logging in shows this sample progress.
SAMPLE_PROGRESS = {"lessons_done": 6, "tests": {1: 92}, "xp": 640, "xp_week": [0, 0, 90, 120, 80, 110, 0],
                   "streak": 4, "best_streak": 9, "right": 32, "asked": 36, "joined": "October 2026"}


def new_quiz(kind, number=None):
    """Questions for a lesson quiz (kind="lesson"), a unit test ("unit") or the final test ("final").
    Each question is kept with the number of the lesson it came from."""
    if kind == "lesson":
        title = f"Lesson {number} quiz · {LESSONS[number - 1]['title']}"
        questions = [(number, question) for question in LESSONS[number - 1]["quiz"]]
    elif kind == "unit":
        title = f"Unit {number} test · {UNITS[number - 1]['title']}"
        questions = [(n, question) for n in UNITS[number - 1]["lessons"] for question in LESSONS[n - 1]["quiz"]]
        random.shuffle(questions)
    else:
        title = "Final test · All 6 units"
        questions = [(n, random.choice(LESSONS[n - 1]["quiz"])) for n in range(1, TOTAL_LESSONS + 1)]
    return {"id": int(time.time() * 1000), "kind": kind, "number": number, "title": title, "questions": questions,
            "index": 0, "results": [], "xp": 0, "started": time.time()}