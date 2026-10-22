# Sign in page: Google sign-in saves your progress, or try Qubi as a guest (nothing saved).

import streamlit as st
from engine.parts import logo
from engine.store import google_ready, start_as_guest

left, middle, right = st.columns([1, 1.3, 1])
with middle:
    st.html(f'<div style="display:flex; justify-content:center; padding:10px 0">{logo(140)}</div>')

    with st.container(key="account_card", gap="medium"):
        st.html('<div class="stack" style="gap:6px; padding:4px 0 8px"><span class="heading">Sign in to Qubi</span>'
                '<span class="small" style="font-size:15px">New here or coming back, it\'s the same button. Your lessons, '
                'streak and achievements are saved to your Google account, so you can pick up on any device.</span></div>')
        if st.button("Continue with Google", type="primary", icon=":material/account_circle:", width="stretch",
                     disabled=not google_ready()):
            st.login("google")
        if not google_ready():
            st.html('<span class="small" style="font-size:13px">Google sign-in isn\'t set up on this copy of Qubi yet '
                    '(see SETUP.md). You can still try it as a guest.</span>')

        st.html('<div class="row small" style="gap:12px; font-size:13px; padding:4px 0">'
                '<span style="flex:1; height:1px; background:var(--line)"></span>or'
                '<span style="flex:1; height:1px; background:var(--line)"></span></div>')
        if st.button("Try it as a guest", icon=":material/person:", width="stretch"):
            start_as_guest()
        st.html('<span class="small" style="font-size:13px">As a guest everything works, but your progress is gone '
                'when you close the page.</span>')

    if st.button("Back", icon=":material/arrow_back:", type="tertiary"):
        st.switch_page("pages/welcome.py")