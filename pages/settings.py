# Settings: daily goal, theme, streak reminder, credits and logging out.

import streamlit as st
from engine.parts import plural
from engine.progress import finish_line

user = st.session_state.user
st.html('<span class="strong" style="font-size:28px; font-weight:700">Settings</span>')


def setting(name, note):
    """The words on the left of a settings row."""
    st.html(f'<div class="stack"><span class="strong" style="font-size:15px; font-weight:600">{name}</span>'
            f'<span class="small" style="font-size:13px">{note}</span></div>')


with st.container(key="card_settings", gap="small"):
    # daily goal
    with st.container(horizontal=True, vertical_alignment="center"):
        setting("Daily goal", f"{plural(user['daily_goal'], 'lesson')} a day · finish line {finish_line(user)}")
        if st.button("Change", key="change_goal"):
            st.session_state.goal_from = "settings"
            st.switch_page("pages/goal.py")
    st.html('<div style="height:1px; background:var(--line); margin:6px 0"></div>')

    # theme
    with st.container(horizontal=True, vertical_alignment="center"):
        setting("Theme", "Diagrams always stay on light paper")
        theme = st.segmented_control("Theme", ["Dark", "Light"], default=st.session_state.get("theme", "dark").capitalize(),
                                     required=True, label_visibility="collapsed")
        if theme.lower() != st.session_state.get("theme", "dark"):
            st.session_state.theme = theme.lower()
            st.rerun()
    st.html('<div style="height:1px; background:var(--line); margin:6px 0"></div>')

    # streak reminder
    with st.container(horizontal=True, vertical_alignment="center"):
        setting("Streak reminder", "A banner on Learn when your streak is at risk")
        user["reminder"] = st.toggle("Streak reminder", value=user["reminder"], label_visibility="collapsed")
    st.html('<div style="height:1px; background:var(--line); margin:6px 0"></div>')

    # credits
    setting("About and credits", "Qubi is built on the ideas in Q is for Quantum by Terry Rudolph. The lessons, "
                                 "pictures and games are our own, and Qubi isn't connected to or endorsed by the author.")
    st.html('<div style="height:1px; background:var(--line); margin:6px 0"></div>')

    # account
    full_name = f'{user["name"]} {user["last_name"]}'.strip()
    with st.container(horizontal=True, vertical_alignment="center"):
        setting("Account", f'{full_name} · {user["email"]}')
        if st.button("Log out", icon=":material/logout:"):
            for key in list(st.session_state.keys()):
                if key != "theme":
                    del st.session_state[key]
            st.switch_page("pages/welcome.py")