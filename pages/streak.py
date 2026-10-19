# Lesson complete: XP earned, the streak, and the week.

import streamlit as st
from engine.parts import flame, bolt, plural, week_dots
from engine.progress import week

if "completed" not in st.session_state:
    st.switch_page("pages/home.py")

user = st.session_state.user
completed = st.session_state.completed
goal_done = user["lessons_today"] >= user["daily_goal"]
left_today = user["daily_goal"] - user["lessons_today"]
message = (f"Daily goal done. Come back tomorrow to make it {user['streak'] + 1}." if goal_done
           else f"{plural(left_today, 'more lesson')} today to hit your goal.")

with st.container(key="celebrate", gap="medium"):
    st.html(f'''
    <div class="stack" style="align-items:center; gap:6px; position:relative">
        <div style="position:absolute; top:40px; width:260px; height:260px; border-radius:50%; background:#7C3AED;
                    opacity:0.28; filter:blur(70px)"></div>
        <div class="row" style="gap:10px; position:relative">
            <span class="label" style="font-size:13px">LESSON {completed["lesson"]} COMPLETE</span>
            <span class="row" style="gap:4px; padding:4px 10px; border-radius:99px; background:rgba(34,211,238,0.14);
                         color:#67E8F9; font-size:13px; font-weight:700">{bolt(14)} +{completed["xp"]} XP</span>
        </div>
        <span style="position:relative; margin-top:10px">{flame(120)}</span>
        <span class="big-number" style="position:relative; font-size:112px; color:#C4B5FD; line-height:0.9">{user["streak"]}</span>
        <span style="position:relative; font-size:30px; color:#C4B5FD; font-weight:700">day streak</span>
    </div>
    <div class="card" style="margin-top:24px; gap:16px">
        {week_dots(week(user), 38)}
        <div style="height:1px; background:var(--line)"></div>
        <span style="text-align:center; color:var(--text); font-size:16px">{message}</span>
    </div>''')
    if st.button("Continue", type="primary", width="stretch"):
        del st.session_state.completed
        st.switch_page("pages/home.py")