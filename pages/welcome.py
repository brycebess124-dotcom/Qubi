# Welcome page: what Qubi is, how it works, and what you need. People see this before they log in.

import streamlit as st
import course
from engine.qubits import make, run
from engine.ui import picture
from engine.parts import logo, icon, CYAN


def open_account(tab):
    """Goes to the Log in / Sign up page, opened on the right tab."""
    st.session_state.tab = tab
    st.switch_page("pages/account.py")


def step_card(number, title, text, drawing):
    return f'''
    <div class="card" style="height:100%">
        {drawing}
        <span class="label">STEP {number}</span>
        <span class="title" style="font-size:19px">{title}</span>
        <span class="small" style="font-size:15px; line-height:1.5">{text}</span>
    </div>'''


white = make("circle", "w")

# dotted background, just on this page
st.html("<style>.stApp { background-image: radial-gradient(rgba(139,139,148,0.16) 1px, transparent 1.5px); "
        "background-size: 46px 46px; }</style>")

# ---------------- top: logo and log in ----------------
with st.container(horizontal=True, vertical_alignment="center"):
    st.html(logo(120))
    if st.button("Log in", key="top_log_in"):
        open_account("Log in")

# ---------------- what we do ----------------
left, right = st.columns([1.1, 1], gap="large", vertical_alignment="center")
with left:
    st.html(f'''
    <div class="stack" style="gap:18px; padding:30px 0 10px">
        <span class="hero">Quantum computing, drawn in shapes.</span>
        <span class="lead">Learn qubits, gates and entanglement with simple pictures instead of heavy math.
            {course.TOTAL_LESSONS} short lessons, made for total beginners.</span>
    </div>''')
    with st.container(horizontal=True):
        if st.button("Get started", type="primary", icon=":material/arrow_forward:", icon_position="right"):
            open_account("Sign up")
        if st.button("I have an account"):
            open_account("Log in")
with right:
    st.html(picture(run(white, "H circle"), across=True,
                    note="A white circle goes through the H box and comes out as a mist. That's superposition."))

# ---------------- how we do it ----------------
st.html('<span class="heading" style="display:block; padding-top:40px">How it works</span>')
step1, step2, step3 = st.columns(3)
step1.html(step_card(1, "Learn with pictures",
                     "A qubit is a shape: white means 0, black means 1. A gate is a box that changes it. "
                     "A superposition is a mist.",
                     picture([white, make("square", "b")], arrows=False)))
step2.html(step_card(2, "Practice right away",
                     "A short quiz after every lesson and a test at the end of each unit, so it sticks.",
                     picture([white, "NOT", "ANSWER"], across=True)))
step3.html(step_card(3, "Build real circuits",
                     "Make your own circuits in the Circuit Lab, then run them on IBM's real quantum computers.",
                     picture(["H", "CNOT"], arrows=False)))

# ---------------- what you need ----------------
needs = ["Basic arithmetic: adding, multiplying and squaring small numbers",
         "No physics, no coding and no advanced math",
         "Any computer, tablet or phone with a web browser",
         f"About {course.MINUTES_PER_LESSON} minutes a lesson. Nothing to buy or install"]
items = "".join(f'<div class="row" style="gap:12px; align-items:flex-start">{icon("check", CYAN, 22)}'
                f'<span style="color:var(--text); font-size:16px">{need}</span></div>' for need in needs)
st.html(f'''
<span class="heading" style="display:block; padding-top:40px">What you need</span>
<div class="card" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(340px, 1fr)); gap:18px 28px; margin-top:16px">
    {items}
</div>''')

# ---------------- bottom ----------------
st.html('<div style="height:24px"></div>')
if st.button("Create your free account", type="primary", key="bottom_sign_up"):
    open_account("Sign up")
st.html('''<span class="small" style="display:block; font-size:13px; line-height:1.5; max-width:660px; padding:30px 0 10px">
    Qubi is built on the ideas in <i>Q is for Quantum</i> by Terry Rudolph. The lessons, pictures and games are
    our own, and Qubi isn't connected to or endorsed by the author.</span>''')