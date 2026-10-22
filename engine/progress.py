# The learner's progress: XP, streaks, levels, achievements, and what to do next.
# It lives in st.session_state.user, and engine/store.py saves it for people who sign in with Google.

import datetime
import math
from html import escape
from zoneinfo import ZoneInfo
import course


def today():
    """Today's date where Qubi is based (course.TIMEZONE), so a new day starts at midnight there."""
    return datetime.datetime.now(ZoneInfo(course.TIMEZONE)).date()


def monday():
    """The Monday of this week, as text like 2026-10-19."""
    return (today() - datetime.timedelta(days=today().weekday())).isoformat()


def new_user(name, last_name, email, sample=False):
    """A fresh account. sample=True fills in sample progress (used by the tests).
    Names are escaped because they're shown inside HTML."""
    username = "".join(letter for letter in name + last_name if letter.isalnum()) or email.split("@")[0]
    user = {"name": escape(name), "last_name": escape(last_name), "username": escape(username), "email": escape(email),
            "joined": today().strftime("%B %Y"), "last_day": None, "week_of": monday(),
            "lessons_done": 0, "tests": {}, "xp": 0, "xp_week": [0] * 7,
            "streak": 0, "best_streak": 0, "daily_goal": 1, "lessons_today": 0,
            "right": 0, "asked": 0, "reminder": True, "new": not sample}
    if sample:
        user.update(course.SAMPLE_PROGRESS)
        user["tests"] = dict(course.SAMPLE_PROGRESS["tests"])
        user["xp_week"] = list(course.SAMPLE_PROGRESS["xp_week"])
        user["last_day"] = (today() - datetime.timedelta(days=1)).isoformat()     # a streak that's still alive
    user["badges"] = {badge["name"]: badge["reached"] for badge in achievements(user)}   # already earned, so no pop-ups
    return user


# ---------- course questions ----------

def unit_of(lesson):
    """Which unit (counting from 1) a lesson is in."""
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
    user["xp_week"][today().weekday()] += amount


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
    user["last_day"] = today().isoformat()
    add_xp(user, course.LESSON_XP)
    return new


def finish_test(user, unit, right, total):
    """Saves a unit test (unit = 1 to 7) or the final test (unit = "final"). Returns the percent."""
    percent = round(right / total * 100)
    if percent >= course.PASS_MARK:
        if unit not in user["tests"]:
            add_xp(user, course.TEST_XP)
        user["tests"][unit] = max(user["tests"].get(unit, 0), percent)
    return percent


# ---------- achievements ----------

def achievements(user):
    """Every achievement from course.ACHIEVEMENTS, with how far along it is:
    reached = goals reached so far, level = the level being worked on (the last one once all are done),
    have / goal = progress toward the next goal, and text = what to do, like "Finish 10 lessons"."""
    unit_tests = {unit: score for unit, score in user["tests"].items() if unit != "final"}
    counts = {"best streak": user["best_streak"], "xp": user["xp"], "lessons": user["lessons_done"],
              "unit tests": len(unit_tests), "right answers": user["right"],
              "perfect tests": len([score for score in unit_tests.values() if score == 100]),
              "final test": int("final" in user["tests"])}
    result = []
    for badge in course.ACHIEVEMENTS:
        goals = badge["goals"]
        have = counts[badge["counts"]]
        reached = len([goal for goal in goals if have >= goal])
        goal = goals[min(reached, len(goals) - 1)]
        result.append({**badge, "reached": reached, "done": reached == len(goals), "level": min(reached + 1, len(goals)),
                       "have": min(have, goal), "goal": goal, "text": task(badge, goal)})
    return result


def task(badge, goal):
    """What to do to reach a goal, like "Reach a 7 day streak" or "Finish 1 lesson"."""
    noun = badge.get("noun")
    return badge["task"].format(f"{goal} {noun if goal == 1 else noun + 's'}" if noun else goal)


def new_badges(user):
    """Achievement levels reached since the last check, each with the goal that was just reached.
    Remembers them, so each one is only shown once (after a lesson or a test)."""
    seen = user.setdefault("badges", {})
    fresh = []
    for badge in achievements(user):
        if badge["reached"] > seen.get(badge["name"], 0):
            fresh.append({**badge, "text": task(badge, badge["goals"][badge["reached"] - 1])})
        seen[badge["name"]] = badge["reached"]
    return fresh


# ---------- dates and the week ----------

def catch_up(user):
    """Brings saved progress up to today. A new day resets today's lessons, a missed day ends the streak,
    and a new week clears the XP chart. Safe to run on every page."""
    last = user.get("last_day")
    if last != today().isoformat():
        user["lessons_today"] = 0
        if last is None or (today() - datetime.date.fromisoformat(last)).days > 1:
            user["streak"] = 0
    if user.get("week_of") != monday():
        user["xp_week"] = [0] * 7
        user["week_of"] = monday()


def week(user):
    """Monday to Sunday: "done", "today" (not done yet), "missed" or "later"."""
    today_number = today().weekday()
    done_today = user["lessons_today"] > 0
    earlier = user["streak"] - (1 if done_today else 0)       # streak days before today
    days = []
    for day in range(7):
        days_ago = today_number - day
        if days_ago < 0:
            days.append("later")
        elif days_ago == 0:
            days.append("done" if done_today else "today")
        else:
            days.append("done" if days_ago <= earlier else "missed")
    return days


def lessons_date(lessons, daily_goal):
    """The day that many more lessons will be done, at daily_goal lessons a day."""
    return today() + datetime.timedelta(days=math.ceil(lessons / daily_goal))


def finish_date(user, daily_goal=None):
    """When the whole course will be done: the lessons left, then one more day for the final test."""
    lessons_left = course.TOTAL_LESSONS - user["lessons_done"]
    if lessons_left == 0:
        return today()
    return lessons_date(lessons_left, daily_goal or user["daily_goal"]) + datetime.timedelta(days=1)


def finish_line(user, daily_goal=None):
    """The finish date as text, like OCT 31, or DONE once the final test is passed."""
    return "DONE" if "final" in user["tests"] else short_date(finish_date(user, daily_goal))


def short_date(date):
    """Like OCT 30."""
    return f"{date.strftime('%b').upper()} {date.day}"