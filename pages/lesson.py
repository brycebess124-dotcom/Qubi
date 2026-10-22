# Lesson page: one step at a time. Read, predict, try it, then Continue.

import random
import streamlit as st
import course
from lessons import LESSONS
from engine.parts import flame
from engine.ui import as_image, draw_colors
from engine.progress import add_xp
from engine.widgets import top_bar, options, feedback, show_picture

if "lesson" not in st.session_state:
    st.switch_page("pages/home.py")

user = st.session_state.user
number = st.session_state.lesson
lesson = LESSONS[number - 1]
index = st.session_state.get("step", 0)
step = lesson["steps"][index]
if st.session_state.get("at") != (number, index):          # a new step: forget the last step's answers
    for key in ["picked", "tries", "rounds"]:
        st.session_state.pop(key, None)
    st.session_state.at = (number, index)
picked = st.session_state.get("picked")                     # the option picked on this step, if any


def next_step():
    """Moves on, or starts the lesson quiz after the last step."""
    if index + 1 < len(lesson["steps"]):
        st.session_state.step = index + 1
        st.rerun()
    st.session_state.quiz = course.new_quiz("lesson", number)
    st.switch_page("pages/quiz.py")


def try_it(spec):
    """The Measure / Play button: measures for real and shows the results."""
    if "rounds" not in st.session_state:
        st.session_state.rounds = []
    rounds = st.session_state.rounds
    with st.container(key="card_tryit"):
        if st.button(spec["button"], icon=":material/play_arrow:", key="try_button"):
            name = random.choice(list(spec["states"]))              # games hide one of several states
            for _ in range(spec["times"]):
                state = spec["states"][name].copy()
                seen = tuple(state.measure(spec["shapes"]).values())
                rounds.append((name, seen))
        if not rounds:
            st.html('<span class="small">Press the button to try it for real.</span>')
            return
        state = list(spec["states"].values())[0]
        shapes = spec["shapes"] or state.shapes
        if spec["times"] == 1:                                         # a game: show the last round
            name, seen = rounds[-1]
            st.html(f'''
            <div class="row" style="gap:14px; align-items:center">
                <span class="paper" style="padding:10px 14px; border-radius:14px">{as_image(draw_colors(shapes, seen, 26))}</span>
                <div class="stack" style="gap:4px">
                    <span class="strong" style="font-weight:600">{spec["labels"].get(seen, "")}</span>
                    <span class="small">{name} · Round {len(rounds)}</span>
                </div>
            </div>''')
        else:                                                          # measuring: dots for the last results
            last = rounds[-spec["times"]:]
            dots = "".join(as_image(draw_colors(shapes, seen, 18)) for _, seen in last)
            counts = {}
            for _, seen in last:
                words = "-".join("black" if color else "white" for color in seen)
                counts[words] = counts.get(words, 0) + 1
            summary = " · ".join(f"{count} {words}" for words, count in sorted(counts.items()))
            st.html(f'''
            <div class="row" style="gap:14px; flex-wrap:wrap">
                <span class="paper" style="flex-direction:row; flex-wrap:wrap; gap:8px; padding:10px 12px; border-radius:12px">{dots}</span>
                <span class="small">{summary}</span>
            </div>''')


# ---------------- top bar ----------------
top_bar(f"Lesson {number} · {lesson['title']}", f"STEP {index + 1} OF {len(lesson['steps'])}",
        index, len(lesson["steps"]), f"{flame(18)} {user['streak']}")

# ---------------- the step ----------------
words, drawing = st.columns([1, 1.1], gap="large")
with words:
    paragraphs = "".join(f'<span class="body">{part}</span>' for part in step["text"].split("\n\n"))
    question = f'<span class="body strong" style="font-weight:600">{step["ask"]["question"]}</span>' if step["ask"] else ""
    st.html(f'''
    <div class="stack" style="gap:18px">
        <span class="label" style="color:#22D3EE; font-size:13px">STEP {index + 1} · {step["kind"]}</span>
        <span class="big-title">{step["title"]}</span>
        {paragraphs}
        {question}
    </div>''')
    if step["ask"]:
        clicked = options(step["ask"]["options"], picked, step["ask"]["answer"], key=f"{number}_{index}")
        if clicked is not None:
            st.session_state.picked = clicked
            st.session_state.tries = st.session_state.get("tries", 0) + 1
            if clicked == step["ask"]["answer"] and st.session_state.tries == 1:
                add_xp(user, course.CHECK_IN_XP)
            st.rerun()

with drawing:
    show_picture(step["picture"], step["note"])
    if step["try_it"]:
        try_it(step["try_it"])

# ---------------- bottom: feedback and Continue ----------------
st.html('<div style="height:18px"></div>')
last_step = index + 1 == len(lesson["steps"])
next_label = "Start the quiz" if last_step else "Continue"
if step["ask"] and picked is not None:
    correct = picked == step["ask"]["answer"]
    first_try = st.session_state.get("tries", 1) == 1
    if correct and first_try:
        title, text = f"Correct! +{course.CHECK_IN_XP} XP", step["ask"]["why"]
    elif correct:
        title, text = "Correct!", step["ask"]["why"]
    else:
        title, text = "Not quite", "Have another look at the picture, then try again."
    with feedback(correct, title, text):
        if correct:
            if st.button(next_label, type="primary", icon=":material/arrow_forward:", icon_position="right"):
                next_step()
        elif st.button("Try again", type="primary"):
            st.session_state.pop("picked")
            st.rerun()
elif not step["ask"]:
    with st.container(horizontal=True, horizontal_alignment="right"):
        if st.button(next_label, type="primary", icon=":material/arrow_forward:", icon_position="right"):
            next_step()