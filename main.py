# Qubi starts here: the theme, every page, who can see what, and the sidebar.

import streamlit as st
from engine.ui import load_style
from engine.parts import logo, avatar
from engine.progress import level

st.set_page_config(page_title="Qubi", page_icon="⚛️", layout="wide")
load_style()

# ---------------- pages ----------------
welcome = st.Page("pages/welcome.py", title="Welcome", default=True)
account = st.Page("pages/account.py", title="Log in", url_path="account")
goal = st.Page("pages/goal.py", title="Daily goal", url_path="goal")
home = st.Page("pages/home.py", title="Learn", icon=":material/route:", url_path="learn")
lesson = st.Page("pages/lesson.py", title="Lesson", url_path="lesson")
quiz = st.Page("pages/quiz.py", title="Quiz", url_path="quiz")
results = st.Page("pages/results.py", title="Results", url_path="results")
streak = st.Page("pages/streak.py", title="Lesson complete", url_path="complete")
lab = st.Page("pages/lab.py", title="Circuit Lab", icon=":material/memory:", url_path="lab")
progress = st.Page("pages/progress.py", title="Progress", icon=":material/bar_chart:", url_path="progress")
settings = st.Page("pages/settings.py", title="Settings", icon=":material/tune:", url_path="settings")

page = st.navigation([welcome, account, goal, home, lesson, quiz, results, streak, lab, progress, settings],
                     position="hidden")

# ---------------- who can see what ----------------
logged_in = "user" in st.session_state
if not logged_in and page not in [welcome, account]:
    st.switch_page(welcome)                      # log in first
if logged_in and page in [welcome, account]:
    st.switch_page(home)                         # already logged in, so go straight to Learn

# ---------------- sidebar (only on the main pages) ----------------
if logged_in and page in [home, lab, progress, settings]:
    user = st.session_state.user
    with st.sidebar:
        st.html(f'<div style="padding:0 10px 18px">{logo()}</div>')
        for link in [home, lab, progress, settings]:
            st.page_link(link)
        st.html(f'''
        <div class="row" style="gap:12px; margin-top:40px; padding:12px; border-radius:16px; background:var(--card)">
            {avatar(user["name"])}
            <div class="stack">
                <span class="strong" style="font-weight:600; font-size:15px">{user["name"]}</span>
                <span class="small" style="font-size:13px">Level {level(user)} · {user["xp"]} XP</span>
            </div>
        </div>''')

page.run()