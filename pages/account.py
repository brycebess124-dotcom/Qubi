# Log in / Sign up page. UI only for now: nothing gets saved yet (the backend comes later).

import streamlit as st
from engine.parts import logo
from engine.progress import new_user


left, middle, right = st.columns([1, 1.3, 1])
with middle:
    st.html(f'<div style="display:flex; justify-content:center; padding:10px 0">{logo(120)}</div>')

    with st.container(key="account_card"):                       # dark card, styled in ui.py
        sign_up_tab, log_in_tab = st.tabs(["Sign up", "Log in"], default=st.session_state.get("tab", "Sign up"))

        with sign_up_tab:
            st.html('<div class="stack" style="gap:6px; padding:8px 0"><span class="heading">Create your free account</span>'
                    '<span class="small" style="font-size:15px">Your progress and streak save to your account.</span></div>')
            first_box, last_box = st.columns(2)
            name = first_box.text_input("First name", placeholder="Alex")
            last_name = last_box.text_input("Last name", placeholder="Smith")
            email = st.text_input("Email", placeholder="you@example.com", key="sign_up_email")
            password = st.text_input("Password", type="password", placeholder="At least 8 characters", key="sign_up_password")

            if st.button("Create account", type="primary", width="stretch"):
                if not name.strip() or not last_name.strip():
                    st.error("Type your first and last name.")
                elif "@" not in email:
                    st.error("Type a real email address.")
                elif len(password) < 8:
                    st.error("Use at least 8 characters for your password.")
                else:
                    st.session_state.user = new_user(name.strip(), last_name.strip(), email.strip())
                    st.session_state.goal_from = "sign up"
                    st.switch_page("pages/goal.py")                  # step 2: pick a daily goal

        with log_in_tab:
            st.html('<div class="stack" style="gap:6px; padding:8px 0"><span class="heading">Welcome back</span>'
                    '<span class="small" style="font-size:15px">Log in to pick up where you left off.</span></div>')
            email = st.text_input("Email", placeholder="you@example.com", key="log_in_email")
            password = st.text_input("Password", type="password", key="log_in_password")

            if st.button("Log in", type="primary", width="stretch"):
                if "@" not in email or not password:
                    st.error("Type your email and password.")
                else:
                    name = email.split("@")[0].capitalize()      # no saved accounts yet, so the name comes from the email
                    st.session_state.user = new_user(name, "", email.strip(), sample=True)
                    st.switch_page("pages/home.py")

        st.html('<div class="row small" style="gap:12px; font-size:13px; padding:4px 0">'
                '<span style="flex:1; height:1px; background:var(--line)"></span>or'
                '<span style="flex:1; height:1px; background:var(--line)"></span></div>')
        if st.button("Continue with Google", icon=":material/account_circle:", width="stretch"):
            st.toast("Google sign-in is coming soon.")

    if st.button("Back", icon=":material/arrow_back:", type="tertiary"):
        st.switch_page("pages/welcome.py")