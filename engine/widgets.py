# Pieces shared by the Lesson and Quiz pages: the top bar, answer options and the feedback bar.

import streamlit as st
from engine.parts import steps_bar, icon
from engine.ui import picture


def top_bar(title, counter, done, total, chip):
    """Exit button, title, STEP 3 OF 7, the segment bar, and a chip on the right."""
    with st.container(key="topbar", horizontal=True, vertical_alignment="center"):
        if st.button("", icon=":material/close:", key="exit", type="tertiary"):
            st.switch_page("pages/home.py")
        st.html(f'''
        <div class="stack" style="gap:8px">
            <div class="row" style="justify-content:space-between">
                <span class="strong" style="font-weight:600; font-size:15px">{title}</span>
                <span class="label" style="font-size:13px">{counter}</span>
            </div>
            {steps_bar(done, total)}
        </div>''')
        st.html(f'<span class="chip" style="height:40px">{chip}</span>', width="content")


def options(choices, picked, answer, key, locked=False):
    """Big A / B / C buttons. After a pick, the picked one turns green or red. Returns a new pick or None.
    locked=True stops more picks (used after skipping)."""
    clicked = None
    for i, text in enumerate(choices):
        if picked is None:
            style = f"pick_{key}_{i}"
        elif i == picked:
            style = f"pick_right_{key}_{i}" if i == answer else f"pick_wrong_{key}_{i}"
        else:
            style = f"pick_{key}_{i}"
        if st.button(f"`{'ABCDE'[i]}` {text}", key=style, width="stretch", disabled=picked is not None or locked, wrap=True):
            clicked = i
    return clicked


def feedback(correct, title, text):
    """A green or red bar with a reason. Returns the bar so the page can put buttons in it."""
    bar = st.container(key="good" if correct else "bad", horizontal=True, vertical_alignment="center")
    badge = ("#22C55E", "check") if correct else ("#F43F5E", "x")
    bar.html(f'''
    <div class="row" style="gap:16px; align-items:center">
        <span class="node" style="width:48px; height:48px; background:{badge[0]}">{icon(badge[1], "white", 24, 3)}</span>
        <div class="stack" style="gap:4px">
            <span style="color:var({'--good-text' if correct else '--bad-text'}); font-size:20px; font-weight:700">{title}</span>
            <span style="color:var({'--good-body' if correct else '--bad-body'}); font-size:16px; line-height:1.5">{text}</span>
        </div>
    </div>''')
    return bar


def show_picture(spec, note=""):
    """Draws a lesson or quiz picture: a list (with arrows) or together(...) (side by side)."""
    if spec is None:
        return
    if isinstance(spec, dict):
        st.html(picture(spec["together"], note, arrows=False))
    else:
        st.html(picture(spec, note))