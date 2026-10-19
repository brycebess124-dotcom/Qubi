# The learner's progress: XP, streaks, levels, and what to do next.
# Everything lives in st.session_state.user for now (no backend yet).

import datetime
import math
from html import escape
import course


def new_user(name, last_name, email, sample=False):
    """A fresh account. sample=True fills in sample progress (used by Log in until accounts are real).
    What people type is escaped because it's shown inside HTML."""
    user = {"name": escape(name), "last_name": escape(last_name), "email": escape(email),
            "joined": datetime.date.today().strftime("%B %Y"),
            "lessons_done": 0, "tests": {}, "xp": 0, "xp_week": [0] * 7,
            "streak": 0, "best_streak": 0, "daily_goal": 1, "lessons_today": 0,
            "right": 0, "asked": 0, "reminder": True, "new": not sample}
    if sample:
        user.update(course.SAMPLE_PROGRESS)
        user["tests"] = dict(course.SAMPLE_PROGRESS["tests"])
        user["xp_week"] = list(course.SAMPLE_PROGRESS["xp_week"])
    return user


# ---------- course questions ----------

def unit_of(lesson):
    """Which unit (1 to 6) a lesson is in."""
    for number, unit in enumerate(course.UNITS, start=1):
        if lesson in unit["lessons"]:
            return number


def level(user):
    return user["xp"] // course.XP_PER_LEVEL + 1


def next_step(user):
    """What the learner should do next: ("lesson", 7), ("test", 2), ("final", None) or ("done", None)."""
    for number, unit in enumerate(course.UNITS, start=1):
        for lesson in unit["lessons"]:
            if lesson > user["lessons_done"]:
                return "lesson", lesson
        if number not in user["tests"]:
            return "test", number
    if "final" not in user["tests"]:
        return "final", None
    return "done", None


# ---------- earning things ----------

def add_xp(user, amount):
    user["xp"] += amount
    user["xp_week"][datetime.date.today().weekday()] += amount


def answered(user, correct):
    user["asked"] += 1
    user["right"] += int(correct)


def finish_lesson(user, lesson):
    """Counts a finished lesson: progress, streak and XP. Returns True if it was a new lesson."""
    new = lesson == user["lessons_done"] + 1
    if new:
        user["lessons_done"] += 1
    if user["lessons_today"] == 0:            # first lesson today keeps the streak going
        user["streak"] += 1
        user["best_streak"] = max(user["best_streak"], user["streak"])
    user["lessons_today"] += 1
    add_xp(user, course.LESSON_XP)
    return new


def finish_test(user, unit, right, total):
    """Saves a unit test (unit = 1 to 6) or the final test (unit = "final"). Returns the percent."""
    percent = round(right / total * 100)
    if percent >= course.PASS_MARK:
        if unit not in user["tests"]:
            add_xp(user, course.TEST_XP)
        user["tests"][unit] = max(user["tests"].get(unit, 0), percent)
    return percent


# ---------- dates and the week ----------

def week(user):
    """Monday to Sunday: "done", "today" (not done yet), "missed" or "later"."""
    today = datetime.date.today().weekday()
    done_today = user["lessons_today"] > 0
    earlier = user["streak"] - (1 if done_today else 0)       # streak days before today
    days = []
    for day in range(7):
        days_ago = today - day
        if days_ago < 0:
            days.append("later")
        elif days_ago == 0:
            days.append("done" if done_today else "today")
        else:
            days.append("done" if days_ago <= earlier else "missed")
    return days


def lessons_date(lessons, daily_goal):
    """The day that many more lessons will be done, at daily_goal lessons a day."""
    return datetime.date.today() + datetime.timedelta(days=math.ceil(lessons / daily_goal))


def finish_date(user, daily_goal=None):
    """When the whole course will be done: the lessons left, then one more day for the final test."""
    lessons_left = course.TOTAL_LESSONS - user["lessons_done"]
    if lessons_left == 0:
        return datetime.date.today()
    return lessons_date(lessons_left, daily_goal or user["daily_goal"]) + datetime.timedelta(days=1)


def finish_line(user, daily_goal=None):
    """The finish date as text, like OCT 31, or DONE once the final test is passed."""
    return "DONE" if "final" in user["tests"] else short_date(finish_date(user, daily_goal))


def short_date(date):
    """Like OCT 30."""
    return f"{date.strftime('%b').upper()} {date.day}"