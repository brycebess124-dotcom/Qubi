# Privacy policy: what Qubi saves, where, and how to delete it. Anyone can open it, signed in or not.

import streamlit as st
from engine.parts import logo

CONTACT = "brycebess124@gmail.com"     # who to email with privacy questions (the same support email as in Google)
UPDATED = "October 22, 2026"

SECTIONS = [
    ("What Qubi saves",
     "If you sign in with Google, Qubi gets your name and email address from Google. Qubi saves those along with your "
     "progress: lessons and tests finished, XP, streak, achievements, daily goal, quiz scores and your light or dark "
     "theme. Qubi never sees your Google password. If you use Qubi as a guest, nothing is saved at all."),
    ("Why",
     "Only so you can pick up where you left off on any device. Your email is how Qubi finds your saved progress."),
    ("Where it's kept",
     "Your progress is stored in a database run by Supabase, and the app runs on Streamlit Community Cloud. Google "
     "handles signing in. The database is locked so only the Qubi app can read it."),
    ("What Qubi doesn't do",
     "Qubi doesn't sell or share your information, doesn't show ads, and doesn't track you around the web. Your name "
     "and progress aren't shown to other users."),
    ("Cookies",
     "Signing in puts one cookie in your browser so you stay signed in after you close the tab. Signing out removes it."),
    ("Deleting your data",
     "Go to Settings and press Delete my account. That erases everything Qubi saved about you right away. You can also "
     f"email {CONTACT} and ask for it to be deleted."),
    ("Students",
     "Qubi is made for students. If you're under 13, ask a parent or guardian before signing in with Google, or use "
     "Qubi as a guest."),
    ("Questions",
     f"Email {CONTACT}. If this policy changes, the date at the top changes too."),
]

with st.container(horizontal=True, vertical_alignment="center"):
    st.html(logo(110), width="content")
    st.space("stretch")
    if st.button("Back", icon=":material/arrow_back:", type="tertiary"):
        st.switch_page("pages/settings.py" if "user" in st.session_state else "pages/welcome.py")

body = "".join(f'<div class="stack" style="gap:6px"><span class="title" style="font-size:19px">{title}</span>'
               f'<span class="body" style="font-size:16px">{text}</span></div>' for title, text in SECTIONS)
st.html(f'''
<div class="stack" style="gap:26px; max-width:720px; padding:30px 0 40px">
    <div class="stack" style="gap:8px">
        <span class="big-title">Privacy policy</span>
        <span class="small">Last updated {UPDATED}</span>
    </div>
    {body}
</div>''')