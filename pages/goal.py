# Daily goal: step 2 of sign up, and opened again from Settings to change the pace.

import datetime
import streamlit as st
import course
from engine.parts import logo, plural, PURPLE, CYAN
from engine.progress import lessons_date, finish_date, finish_line, short_date

user = st.session_state.user
from_sign_up = st.session_state.get("goal_from") == "sign up"
pace = st.session_state.setdefault("pace", user["daily_goal"])

# ---------------- top ----------------
with st.container(horizontal=True, vertical_alignment="center"):
    st.html(logo(110))
    if from_sign_up:
        st.html('''<div class="row" style="justify-content:flex-end; gap:12px"><span class="label">STEP 2 OF 3</span>
            <div class="steps" style="width:100px"><span class="done"></span><span class="now"></span><span></span></div></div>''')

st.html('''<div class="stack" style="align-items:center; text-align:center; gap:10px; padding:10px 0 26px">
    <span class="big-title" style="font-size:42px">How much do you want to learn each day?</span>
    <span class="lead" style="font-size:18px">Pick a pace. Hitting it every day keeps your streak going. You can change it anytime.</span>
</div>''')

left, right = st.columns([1.6, 1], gap="large")

# ---------------- the three paces ----------------
with left:
    with st.container(key="paces"):
        columns = st.columns(3)
        for column, (name, lessons) in zip(columns, course.PACES.items()):
            chosen = lessons == pace
            fill = PURPLE if chosen else "var(--track)"
            column.html(f'''
            <div class="stack" style="align-items:center; gap:14px">
                <span style="width:110px; height:270px; border-radius:99px; border:1.5px solid var(--edge); padding:6px;
                             box-sizing:border-box; display:flex; align-items:flex-end;
                             background:repeating-linear-gradient(135deg, var(--line) 0 2px, transparent 2px 11px)">
                    <span style="width:100%; height:{40 + lessons * 70}px; border-radius:99px; background:{fill}"></span>
                </span>
                <span class="stack" style="align-items:center">
                    <span class="strong" style="font-weight:700; font-size:18px">{name}</span>
                    <span style="color:{'#C4B5FD' if chosen else 'var(--soft)'}; font-size:15px">{plural(lessons, 'lesson')} a day</span>
                    <span class="small">~{lessons * course.MINUTES_PER_LESSON} min</span>
                </span>
            </div>''')
            if column.button("Chosen" if chosen else f"Pick {name}", key=f"pace_{name}", width="stretch",
                             type="primary" if chosen else "secondary"):
                st.session_state.pace = lessons
                st.rerun()

# ---------------- your plan ----------------
with right:
    lessons_left = course.TOTAL_LESSONS - user["lessons_done"]
    days = (finish_date(user, pace) - datetime.date.today()).days          # the last day is for the final test
    rows = ""
    lessons_so_far = 0
    for number, unit in enumerate(course.UNITS, start=1):
        left_in_unit = sum(1 for n in unit["lessons"] if n > user["lessons_done"])
        lessons_so_far += left_in_unit
        if left_in_unit == 0:
            when, shade = "DONE", PURPLE
        else:
            when = short_date(lessons_date(lessons_so_far, pace))
            shade = CYAN if lessons_so_far == left_in_unit else None            # cyan: the unit you're on now
        dot = f"background:{shade}; border:2px solid {shade}" if shade else "border:2px solid var(--edge)"
        rows += (f'<div class="row" style="justify-content:space-between; min-height:34px">'
                 f'<span class="row" style="gap:12px"><span style="width:12px; height:12px; border-radius:50%; '
                 f'{dot}; box-sizing:border-box"></span>'
                 f'<span style="color:var(--text); font-size:14px">Unit {number} · {unit["title"]}</span></span>'
                 f'<span class="label" style="font-size:13px">{when}</span></div>')
    rows += (f'<div class="row" style="justify-content:space-between; min-height:34px">'
             f'<span class="row" style="gap:12px"><span style="width:12px; height:12px; border-radius:4px; background:{PURPLE}"></span>'
             f'<span class="strong" style="font-size:14px; font-weight:600">Final test</span></span>'
             f'<span class="label" style="font-size:13px; color:#C4B5FD">{finish_line(user, pace)}</span></div>')
    hours = round(lessons_left * course.MINUTES_PER_LESSON / 60, 1)
    summary = f"{plural(days, 'day')} · about {hours} hours in total" if lessons_left else "Every lesson is done"
    st.html(f'''
    <div class="card" style="gap:16px">
        <span class="title">Your plan</span>
        <div class="stack" style="gap:4px">
            <span class="small">At {plural(pace, 'lesson')} a day you'll finish around</span>
            <span class="big-number" style="color:{CYAN}">{finish_line(user, pace)}</span>
            <span class="small">{summary}</span>
        </div>
        <div class="stack" style="gap:0">{rows}</div>
    </div>''')
    reminder = st.toggle("Show a streak reminder when I open Qubi", value=user["reminder"])

# ---------------- bottom ----------------
st.html('<div style="height:10px"></div>')
with st.container(horizontal=True, horizontal_alignment="distribute"):
    if st.button("Back", icon=":material/arrow_back:"):
        st.session_state.pop("pace", None)
        if from_sign_up:                                   # undo step 1 and go back to the sign up form
            del st.session_state.user
            st.switch_page("pages/account.py")
        st.switch_page("pages/settings.py")
    if st.button("Continue" if from_sign_up else "Save", type="primary", icon=":material/arrow_forward:", icon_position="right"):
        user["daily_goal"] = pace
        user["reminder"] = reminder
        st.session_state.pop("pace", None)
        st.session_state.pop("goal_from", None)
        st.switch_page("pages/home.py" if from_sign_up else "pages/settings.py")