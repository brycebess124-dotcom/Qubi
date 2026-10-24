# Settings: daily goal, theme, streak reminder, credits and logging out.

import streamlit as st
from engine.parts import plural
from engine.progress import finish_line
from engine.store import sign_out, delete_account

user = st.session_state.user


@st.dialog("Delete your account?")
def confirm_delete():
    st.html('<span class="small" style="font-size:15px; line-height:1.5">This erases your saved lessons, XP, streak and '
            'achievements for good, and signs you out. You can always start again by signing in.</span>')
    with st.container(horizontal=True):
        if st.button("Delete everything", type="primary"):
            if not delete_account():
                st.error("Couldn't reach the database. Try again in a minute.")
        if st.button("Cancel"):
            st.rerun()
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
            st.session_state.theme = user["theme"] = theme.lower()
            st.rerun()
    st.html('<div style="height:1px; background:var(--line); margin:6px 0"></div>')

    # streak reminder
    with st.container(horizontal=True, vertical_alignment="center"):
        setting("Streak reminder", "A banner on Learn when your streak is at risk")
        user["reminder"] = st.toggle("Streak reminder", value=user["reminder"], label_visibility="collapsed")
    st.html('<div style="height:1px; background:var(--line); margin:6px 0"></div>')

    # preview mode
    with st.container(horizontal=True, vertical_alignment="center"):
        setting("Preview mode", "Unlock every lesson, test and Rulebook rule to look around. Your finished lessons stay the same.")
        st.session_state.preview = st.toggle("Preview mode", value=st.session_state.get("preview", False),
                                             label_visibility="collapsed")
    st.html('<div style="height:1px; background:var(--line); margin:6px 0"></div>')

    # credits
    setting("About and credits", "Qubi is built on the ideas in the Virginia Tech Quantum Information Science and "
                                 "Engineering Summer School notes by Sophia Economou, Edwin Barnes and Jamie Sikora, "
                                 "and in Q is for Quantum by Terry Rudolph. The lessons are written in our own words, "
                                 "the pictures and games are our own, and Qubi isn't connected to or endorsed by these "
                                 "authors or by Virginia Tech.")
    st.html('<div style="height:1px; background:var(--line); margin:6px 0"></div>')

    # account
    full_name = f'{user["name"]} {user["last_name"]}'.strip()
    with st.container(horizontal=True, vertical_alignment="center"):
        note = f'{full_name} · {user["email"]} · saved with Google' if user.get("account") else "Guest · progress isn't saved"
        setting("Account", note)
        if st.button("Sign out", icon=":material/logout:"):
            sign_out()
    st.html('<div style="height:1px; background:var(--line); margin:6px 0"></div>')

    # privacy, and deleting your account
    with st.container(horizontal=True, vertical_alignment="center"):
        setting("Privacy", "What Qubi saves, and how to delete it")
        st.page_link("pages/privacy.py", label="Privacy policy", icon=":material/shield:")
        if user.get("account") and st.button("Delete my account", icon=":material/delete_forever:", type="tertiary"):
            confirm_delete()