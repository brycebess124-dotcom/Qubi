# Results page: the score for a unit test or the final test.

import streamlit as st
import course
from lessons import LESSONS
from engine.parts import ring, icon, bolt, unlocked_card, PURPLE, CYAN

if "test_result" not in st.session_state:
    st.switch_page("pages/home.py")

result = st.session_state.test_result
user = st.session_state.user
passed = result["percent"] >= course.PASS_MARK
unit = result["unit"]
minutes, seconds = divmod(result["seconds"], 60)

# ---------------- top bar ----------------
with st.container(key="topbar", horizontal=True, vertical_alignment="center"):
    if st.button("", icon=":material/close:", key="exit", type="tertiary"):
        st.switch_page("pages/home.py")
    st.html(f'<span class="strong" style="font-weight:600; font-size:15px">{result["title"].split(" · ")[0]} · Results</span>')

# ---------------- the score ----------------
with st.container(key="card_score", horizontal=True, vertical_alignment="center", gap="large"):
    st.html(f'''
    <div style="position:relative; width:220px; height:220px">
        {ring(result["percent"], 220, 18, PURPLE if passed else "#F43F5E")}
        <div class="stack" style="position:absolute; inset:0; align-items:center; justify-content:center; gap:4px">
            <span class="big-number" style="font-size:60px">{result["percent"]}%</span>
            <span class="small" style="font-size:15px">{result["right"]} of {result["total"]} right</span>
        </div>
    </div>''', width="content")
    with st.container(gap="medium"):
        if passed:
            badge = ("rgba(34,197,94,0.14)", "var(--good-text)",
                     "PASSED · " + ("FINAL TEST" if unit == "final" else f"UNIT {unit} COMPLETE"))
        else:
            badge = ("rgba(244,63,94,0.14)", "var(--bad-text)", f"NOT YET · YOU NEED {course.PASS_MARK}%")
        name = f"All {len(course.UNITS)} units" if unit == "final" else course.UNITS[unit - 1]["title"]
        xp = f"+{course.TEST_XP} XP" if passed else "+0 XP"
        st.html(f'''
        <div class="stack" style="gap:16px">
            <span style="align-self:flex-start; padding:6px 12px; border-radius:99px; background:{badge[0]}; color:{badge[1]};
                         font-weight:700; font-size:14px; letter-spacing:0.04em">{badge[2]}</span>
            <span class="big-title" style="font-size:40px">{name}</span>
            <div class="row" style="gap:10px; flex-wrap:wrap">
                <span class="chip">{bolt(18)} {xp}</span>
                <span class="chip">{icon("clock", CYAN, 18)} {minutes} min {seconds} s</span>
                <span class="chip small" style="font-weight:500">Pass mark {course.PASS_MARK}%</span>
            </div>
        </div>''')
        with st.container(horizontal=True):
            if st.button("Continue" if passed else "Back to Learn", type="primary", icon=":material/arrow_forward:",
                         icon_position="right"):
                st.switch_page("pages/home.py")
            if st.button("Retake test"):
                st.session_state.quiz = course.new_quiz(result["kind"], None if unit == "final" else unit)
                st.switch_page("pages/quiz.py")

# ---------------- by lesson, and the one you missed ----------------
by_lesson, missed_side = st.columns(2, gap="large")
with by_lesson:
    scores = {}
    for answer in result["results"]:
        right, asked = scores.get(answer["lesson"], (0, 0))
        scores[answer["lesson"]] = (right + answer["correct"], asked + 1)
    bars = ""
    for lesson, (right, asked) in sorted(scores.items()):
        fill = PURPLE if right == asked else CYAN
        height = max(right / asked * 100, 18)
        bars += f'''
        <div class="stack" style="align-items:center; gap:10px">
            <span style="width:100%; max-width:80px; height:200px; border-radius:99px; border:1.5px solid var(--edge); padding:5px;
                         box-sizing:border-box; display:flex; align-items:flex-end;
                         background:repeating-linear-gradient(135deg, var(--line) 0 2px, transparent 2px 11px)">
                <span style="width:100%; height:{height}%; border-radius:99px; background:{fill}; color:{'#FFFFFF' if fill == PURPLE else '#0B1220'};
                             font-weight:700; display:flex; align-items:flex-end; justify-content:center; padding-bottom:12px; box-sizing:border-box">{right}/{asked}</span>
            </span>
            <span class="small" style="text-align:center; line-height:1.3; color:var(--text)">{LESSONS[lesson - 1]["title"]}</span>
        </div>'''
    columns = min(len(scores), 6)
    st.html(f'''
    <div class="card" style="gap:20px">
        <div class="row" style="justify-content:space-between"><span class="title">By lesson</span>
            <span class="small">{result["total"]} questions</span></div>
        <div style="display:grid; grid-template-columns:repeat({columns}, minmax(0, 1fr)); gap:14px; align-items:start">{bars}</div>
    </div>''')

with missed_side:
    missed = [answer for answer in result["results"] if not answer["correct"]]
    if missed:
        first = missed[0]
        st.html(f'''
        <div class="card" style="gap:16px">
            <span class="title">{"The one you missed" if len(missed) == 1 else f"You missed {len(missed)}. Here's the first"}</span>
            <span style="color:var(--text); font-size:16px; line-height:1.5">{first["question"]}</span>
            <div class="row" style="gap:10px; padding:10px 12px; border-radius:14px; background:rgba(244,63,94,0.10); border:1px solid rgba(244,63,94,0.35)">
                {icon("x", "#F43F5E", 18, 3)}<span style="color:var(--bad-body); font-size:14px">You said: {first["given"]}</span></div>
            <div class="row" style="gap:10px; padding:10px 12px; border-radius:14px; background:rgba(34,197,94,0.10); border:1px solid rgba(34,197,94,0.35)">
                {icon("check", "#22C55E", 18, 3)}<span style="color:var(--good-body); font-size:14px">Answer: {first["answer"]}</span></div>
        </div>''')
        if st.button(f"Review Lesson {first['lesson']}: {LESSONS[first['lesson'] - 1]['title']}", icon=":material/menu_book:"):
            st.session_state.lesson = first["lesson"]
            st.session_state.step = 0
            st.session_state.pop("at", None)
            st.switch_page("pages/lesson.py")
    else:
        st.html('<div class="card"><span class="title">A perfect score</span>'
                '<span class="small">You got every question right. Nice work!</span></div>')

    if passed and unit != "final":
        if unit < len(course.UNITS):
            next_unit = course.UNITS[unit]
            first = next_unit["lessons"][0]
            title, note = f"Unit {unit + 1} · {next_unit['title']}", f"Next: Lesson {first}, {LESSONS[first - 1]['title']}"
        else:
            title = "The final test"
            note = f"{course.FINAL_PER_UNIT * len(course.UNITS)} questions from all {len(course.UNITS)} units."
        st.html(f'''
        <div class="card" style="background:var(--banner); border-color:rgba(139,92,246,0.4); gap:4px">
            <span class="label" style="color:#C4B5FD">UNLOCKED</span>
            <span class="title">{title}</span>
            <span style="color:var(--banner-text); font-size:14px">{note}</span>
        </div>''')

    if result.get("badges"):
        st.html(unlocked_card(result["badges"]))