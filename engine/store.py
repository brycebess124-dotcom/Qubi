# Accounts and saving. Google sign-in (st.login) says who you are, and a Supabase table keeps your progress.
# How to set both up is in SETUP.md. Without that setup Qubi still runs, but only as a guest, and nothing is saved.

import datetime
import json
import requests
import streamlit as st
from engine.progress import new_user, catch_up

TABLE = "progress"     # columns: email (the key), data (the progress), updated_at


def settings(section):
    """A section of .streamlit/secrets.toml, or None if it isn't there."""
    try:
        return dict(st.secrets[section])
    except Exception:
        return None


def google_ready():
    return settings("auth") is not None


def database_ready():
    return settings("supabase") is not None


# ================= the database =================

def _ask(method, **options):
    """One request to the Supabase table. Raises an error if it fails."""
    database = settings("supabase")
    headers = {"apikey": database["key"], "Content-Type": "application/json", **options.pop("headers", {})}
    response = requests.request(method, database["url"].rstrip("/") + "/rest/v1/" + TABLE,
                                headers=headers, timeout=10, **options)
    response.raise_for_status()
    return response


def for_saving(user):
    """The progress as JSON text. JSON keys must be text, so test numbers like 1 become "1"."""
    return json.dumps({**user, "tests": {str(unit): score for unit, score in user["tests"].items()}}, sort_keys=True)


def load(email):
    """The saved progress for this email, or None for someone new."""
    rows = _ask("GET", params={"email": f"eq.{email}", "select": "data"}).json()
    if not rows:
        return None
    user = rows[0]["data"]
    user["tests"] = {int(unit) if unit.isdigit() else unit: score for unit, score in user["tests"].items()}
    return user


def save(email, user):
    """Saves the progress, adding a row the first time and replacing it after that."""
    _ask("POST", data=json.dumps({"email": email, "data": json.loads(for_saving(user)),
                                  "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}),
         headers={"Prefer": "resolution=merge-duplicates,return=minimal"})


# ================= the session =================

def signed_in():
    """Who signed in with Google, as a dict with email and names, or None."""
    if not google_ready() or not st.user.is_logged_in:
        return None
    email = st.user.get("email", "")
    return {"email": email, "first": st.user.get("given_name") or st.user.get("name") or email.split("@")[0],
            "last": st.user.get("family_name") or ""}


def start():
    """Runs before every page. Right after Google sign-in it loads your progress (or makes a new account),
    and on every run it saves anything that changed. Returns True when a brand-new account was just made."""
    state = st.session_state
    person = signed_in()
    brand_new = False
    if "user" not in state and person:
        saved, offline = None, False
        if database_ready():
            try:
                saved = load(person["email"])
            except Exception:
                offline = True             # don't start a new account over one we just couldn't read
        if saved:
            user = saved
        else:
            user = new_user(person["first"], person["last"], person["email"])
            brand_new = not offline        # if we couldn't check, don't treat them as new
        user["account"] = person["email"]
        user["offline"] = offline or not database_ready()
        state.user = user
        state.theme = user.get("theme", state.get("theme", "dark"))
        state.saved = for_saving(user) if saved else None
        if offline:
            st.toast("Couldn't reach your saved progress, so this visit won't be saved.", icon=":material/cloud_off:")
    if "user" in state:
        catch_up(state.user)
        keep(state.user)
    return brand_new


def keep(user):
    """Saves the progress if it changed since the last save (only for Google accounts that can be saved)."""
    if not user.get("account") or user.get("offline"):
        return
    text = for_saving(user)
    if text == st.session_state.get("saved"):
        return
    try:
        save(user["account"], user)
        st.session_state.saved = text
    except Exception:
        st.toast("Couldn't save just now. Qubi will try again on your next step.", icon=":material/cloud_off:")


def start_as_guest():
    """A guest account: everything works, but nothing is saved."""
    st.session_state.user = new_user("Guest", "", "")
    st.session_state.goal_from = "sign up"
    st.switch_page("pages/goal.py")


def sign_out():
    """Saves, forgets this visit (except the theme), and signs out of Google too."""
    if "user" in st.session_state:
        keep(st.session_state.user)
    for key in list(st.session_state.keys()):
        if key != "theme":
            del st.session_state[key]
    if signed_in():
        st.logout()                        # starts the app again, signed out
    st.switch_page("pages/welcome.py")