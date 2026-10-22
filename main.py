# Qubi starts here: the theme, every page, who can see what, and the sidebar.

from pathlib import Path
import streamlit as st
from engine.ui import load_style
from engine.parts import logo, avatar
from engine.progress import level
from engine.store import start

ICON = Path(__file__).parent / "assets" / "icon.png"     # the q from the logo, shown on the browser tab
st.set_page_config(page_title="Qubi", page_icon=str(ICON), layout="wide")
load_style()

# ---------------- pages ----------------
welcome = st.Page("pages/welcome.py", title="Welcome", default=True)
account = st.Page("pages/account.py", title="Sign in", url_path="account")
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

# ---------------- accounts: load or save progress, then who can see what ----------------
if start():                                      # just signed in with Google for the first time
    st.session_state.goal_from = "sign up"
    st.switch_page(goal)
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
        if not user.get("account"):
            st.html('<span class="small" style="display:block; padding:10px 6px; font-size:13px; line-height:1.45">'
                    'You\'re a guest, so your progress isn\'t saved. Sign out and sign in with Google to keep it.</span>')
        elif user.get("offline"):
            st.html('<span class="small" style="display:block; padding:10px 6px; font-size:13px">Saving is off right now.</span>')
else:                                            # other pages: no sidebar, not even an empty one left over
    st.html('<style>[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] { display: none; }</style>')

page.run()