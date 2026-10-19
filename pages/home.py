# Learn page: the course map on the left, progress cards on the right.

import streamlit as st
import course
from lessons import LESSONS
from engine import parts
from engine.progress import next_step, unit_of, level, week, finish_line


def open_lesson(number):
    st.session_state.lesson = number
    st.session_state.step = 0
    st.session_state.pop("at", None)                  # start the lesson fresh
    st.switch_page("pages/lesson.py")


def open_test(kind, unit=None):
    st.session_state.quiz = course.new_quiz(kind, unit)
    st.switch_page("pages/quiz.py")


user = st.session_state.user
done = user["lessons_done"]
kind, number = next_step(user)
current_unit = number if kind == "test" else unit_of(number) if kind == "lesson" else None
open_units = st.session_state.setdefault("open_units", set())
if st.session_state.get("last_unit") != current_unit:      # a new unit opens by itself
    open_units.add(current_unit)
    st.session_state.last_unit = current_unit

left, right = st.columns([1.8, 1], gap="large")

# ================= left: the course map =================
with left:
    greeting = "Welcome" if user["new"] and done == 0 else "Welcome back"
    st.html(f'''
    <div class="stack" style="gap:6px">
        <span class="strong" style="font-size:30px; font-weight:700">{greeting}, {user["name"]}</span>
        <span class="small" style="font-size:16px">Intro to Quantum Computing · 6 units · {course.TOTAL_LESSONS} lessons</span>
    </div>''')

    # ---------- the banner: what to do next ----------
    if kind == "lesson":
        left_today = user["daily_goal"] - user["lessons_today"]
        if left_today <= 0:
            headline = "Daily goal done!"
        elif user["lessons_today"] > 0:                       # the streak is safe once a lesson is done today
            headline = f"{parts.plural(left_today, 'more lesson')} to hit today's goal"
        elif user["streak"] == 0:
            headline = "Start your streak today"
        elif user["reminder"]:
            headline = f"Your {user['streak']}-day streak ends at midnight"
        else:
            headline = f"Keep your {user['streak']}-day streak going"
        note, button = f"Lesson {number} is next: {LESSONS[number - 1]['title']}", "Continue"
    elif kind == "test":
        unlocks = "the final test" if number == len(course.UNITS) else "the next unit"
        headline, note, button = f"Unit {number} test is ready", f"Pass with {course.PASS_MARK}% to unlock {unlocks}.", "Start test"
    elif kind == "final":
        headline, note, button = "The final test is ready", "One question from every lesson.", "Start final test"
    else:
        headline, note, button = "You finished Qubi!", "Every lesson, every test. Try the Circuit Lab anytime.", None

    with st.container(key="banner", horizontal=True, vertical_alignment="center"):
        st.html(parts.banner_text(headline, note))
        if button and st.button(button, key="go_continue", icon=":material/arrow_forward:", icon_position="right"):
            if kind == "lesson":
                open_lesson(number)
            else:
                open_test(kind, number)

    # ---------- the units ----------
    for unit_number, unit in enumerate(course.UNITS, start=1):
        lessons = unit["lessons"]
        done_here = sum(1 for n in lessons if n <= done)
        if unit_number in user["tests"]:
            status, tag = "complete", "done"
        elif unit_number == current_unit:
            status, tag = "current", "now"
        else:
            status, tag = "locked", "lock"
        is_open = unit_number in open_units

        # header with an open/close button
        with st.container(key=f"unit_{tag}_{unit_number}"):
            with st.container(horizontal=True, vertical_alignment="center"):
                st.html(parts.unit_text(unit_number, unit, done_here, status))
                if st.button("", icon=":material/expand_less:" if is_open else ":material/expand_more:", key=f"open_{unit_number}"):
                    open_units.symmetric_difference_update({unit_number})
                    st.rerun()
            if status == "current":
                st.html(parts.unit_bar(done_here, len(lessons)))

        if not is_open:
            continue

        # the path: one row per lesson, winding left and right
        st.html('<div style="height:18px"></div>')
        for i, lesson in enumerate(lessons):
            if lesson <= done:
                status, label, icon = "done", "", ":material/check:"
            elif kind == "lesson" and lesson == number:
                status, label, icon = "now", str(lesson), None
            else:
                status, label, icon = "lock", "", ":material/lock:"
            indent = 0.4 if status == "now" else [0.22, 0.34, 0.42, 0.34][i % 4]
            space, row = st.columns([indent, 1 - indent], vertical_alignment="center")
            if status == "now":
                space.html(parts.robot_says(f"You've got this! Next up: {LESSONS[lesson - 1]['title']}"))
            with row:
                with st.container(horizontal=True, vertical_alignment="center", gap="medium", wrap=False, key=f"row_{lesson}"):
                    if st.button(label, icon=icon, key=f"node_{status}_{lesson}", disabled=status == "lock"):
                        open_lesson(lesson)
                    st.html(parts.lesson_text(lesson, LESSONS[lesson - 1]["title"], status))

        # the unit test at the end of the path
        if unit_number in user["tests"]:
            status, key = "done", f"node_testdone_{unit_number}"
        elif kind == "test" and number == unit_number:
            status, key = "now", f"node_test_{unit_number}"
        else:
            status, key = "lock", f"node_lock_test_{unit_number}"
        space, row = st.columns([0.12, 0.88], vertical_alignment="center")
        with row:
            with st.container(horizontal=True, vertical_alignment="center", gap="medium", wrap=False, key=f"row_test_{unit_number}"):
                if st.button("", icon=":material/emoji_events:", key=key, disabled=status == "lock"):
                    open_test("unit", unit_number)
                st.html(parts.test_text(unit_number, lessons[-1], status, user["tests"].get(unit_number)))
        st.html('<div style="height:22px"></div>')

    # ---------- the final test ----------
    final_status = "done" if "final" in user["tests"] else "now" if kind == "final" else "locked"
    st.html(parts.final_test_card(final_status))
    if final_status != "locked" and st.button("Take the final test", key="final_test", icon=":material/flag:"):
        open_test("final")

# ================= right: progress =================
with right:
    st.html(parts.stat_chips(user["streak"], user["xp"]))
    st.html(parts.progress_card(done, course.TOTAL_LESSONS, level(user), user["xp"], level(user) * course.XP_PER_LEVEL))
    st.html(parts.goal_card(user["lessons_today"], user["daily_goal"], course.TOTAL_LESSONS - done, finish_line(user)))
    st.html(parts.week_card(week(user), user["best_streak"], user["streak"]))
    st.html(parts.lab_card())
    if st.button("Open the Circuit Lab", icon=":material/memory:", width="stretch"):
        st.switch_page("pages/lab.py")