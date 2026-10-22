# Progress page: profile, stats, achievements, XP this week, and every unit.

import streamlit as st
import course
from engine.parts import avatar, flame, bolt, icon, plural, ring, stat_card, achievement_row, PURPLE, CYAN, GREY
from engine.progress import level, achievements, today

user = st.session_state.user
lessons_done = user["lessons_done"]
xp_next = level(user) * course.XP_PER_LEVEL
accuracy = round(user["right"] / user["asked"] * 100) if user["asked"] else 0
full_name = f'{user["name"]} {user["last_name"]}'.strip()


def heading(text):
    st.html(f'<span class="strong" style="font-size:22px; font-weight:700; display:block; padding-top:14px">{text}</span>')


# ---------------- profile ----------------
st.html(f'''
<div class="row" style="gap:22px; flex-wrap:wrap; padding-bottom:6px">
    <span style="box-shadow:0 0 0 5px rgba(139,92,246,0.25); border-radius:50%">{avatar(user["name"], 84)}</span>
    <div class="stack" style="flex:1 1 260px; gap:4px">
        <span class="strong" style="font-size:34px; font-weight:700">{full_name}</span>
        <span style="font-size:16px; color:var(--soft)">{user.get("username", "")}</span>
        <span class="row small" style="gap:7px; font-size:15px; margin-top:4px">{icon("clock", GREY, 16, 2)}
            Joined {user["joined"]} · Goal: {plural(user["daily_goal"], "lesson")} a day</span>
    </div>
    <div class="stack" style="gap:8px; min-width:240px">
        <div class="row" style="justify-content:space-between; font-size:14px">
            <span class="strong" style="font-weight:600">Level {level(user)}</span><span class="small">{user["xp"]} / {xp_next} XP</span>
        </div>
        <div class="bar" style="height:10px"><div style="width:{user["xp"] / xp_next * 100}%"></div></div>
        <span class="small" style="font-size:13px">{xp_next - user["xp"]} XP to Level {level(user) + 1}</span>
    </div>
</div>''')

# ---------------- four stats ----------------
heading("Statistics")
week_xp = sum(user["xp_week"])
cards = [(flame(18), "Day streak", user["streak"], f'Best: {plural(user["best_streak"], "day")}'),
         (bolt(18), "Total XP", user["xp"], f"{week_xp} this week"),
         (icon("book", "#A78BFA", 18), "Lessons done", f"{lessons_done}/{course.TOTAL_LESSONS}",
          f"{round(lessons_done / course.TOTAL_LESSONS * 100)}% of the course"),
         (icon("check", CYAN, 18, 2.6), "Quiz accuracy", f"{accuracy}%", f'{user["right"]} of {plural(user["asked"], "question")}')]
for column, card in zip(st.columns(4), cards):
    column.html(stat_card(*card))

# ---------------- achievements: each goal you reach moves one up a level ----------------
badges = achievements(user)
levels_done = sum(badge["reached"] for badge in badges)
heading("Achievements")
st.html(f'''
<div class="card" style="gap:0; padding-top:6px; padding-bottom:4px">
    <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(330px, 1fr)); column-gap:36px">
        {"".join(achievement_row(badge) for badge in badges)}
    </div>
    <span class="small" style="padding:14px 0 10px">{levels_done} of {sum(len(badge["goals"]) for badge in badges)}
        levels done. New ones show up after your lessons and tests.</span>
</div>''')

# ---------------- XP this week and the units ----------------
st.html('<div style="height:8px"></div>')
week_side, units_side = st.columns(2, gap="large")
with week_side:
    today_number = today().weekday()
    biggest = max(max(user["xp_week"]), 1)
    bars = ""
    for day, (letter, xp) in enumerate(zip("MTWTFSS", user["xp_week"])):
        shade = CYAN if day == today_number else PURPLE
        fill = f'<span style="width:100%; height:{xp / biggest * 100}%; border-radius:99px; background:{shade}"></span>' if xp else ""
        bars += (f'<div class="stack" style="align-items:center; gap:8px">'
                 f'<span style="width:100%; max-width:44px; height:240px; border-radius:99px; padding:4px; box-sizing:border-box;'
                 f' border:1.5px solid {shade if day == today_number else "var(--edge)"}; display:flex; align-items:flex-end;'
                 f' background:repeating-linear-gradient(135deg, var(--line) 0 2px, transparent 2px 10px)">{fill}</span>'
                 f'<span style="font-size:13px; color:{CYAN if day == today_number else "var(--muted)"}">{letter}</span></div>')
    st.html(f'''
    <div class="card" style="gap:20px">
        <div class="row" style="justify-content:space-between"><span class="title">XP this week</span>
            <span class="small">{week_xp} XP</span></div>
        <div style="display:grid; grid-template-columns:repeat(7, minmax(0, 1fr)); gap:10px">{bars}</div>
    </div>''')

with units_side:
    rows = ""
    for number, unit in enumerate(course.UNITS, start=1):
        done_here = sum(1 for n in unit["lessons"] if n <= lessons_done)
        percent = round(done_here / len(unit["lessons"]) * 100)
        if number in user["tests"]:
            note, note_color = f'{done_here} of {len(unit["lessons"])} lessons · test {user["tests"][number]}%', "var(--muted)"
        elif done_here or (number == 1 or number - 1 in user["tests"]):
            note, note_color = f'{done_here} of {len(unit["lessons"])} lessons · in progress', CYAN
        else:
            note, note_color = "Locked", "var(--muted)"
        if note == "Locked":
            badge = f'<span class="node" style="width:46px; height:46px; border:5px solid var(--track); box-sizing:border-box">{icon("lock", GREY, 16, 2)}</span>'
        else:
            badge = (f'<span style="position:relative; width:46px; height:46px; display:flex; align-items:center; justify-content:center">'
                     f'<span style="position:absolute; inset:0">{ring(percent, 46, 5, PURPLE)}</span>'
                     f'<span class="strong" style="position:relative; font-size:11px; font-weight:700">{percent}%</span></span>')
        rows += (f'<div class="row" style="min-height:58px; border-bottom:1px dashed var(--line)">'
                 f'<div class="stack" style="flex:1"><span class="strong" style="font-weight:600; font-size:15px">{number} · {unit["title"]}</span>'
                 f'<span style="color:{note_color}; font-size:13px">{note}</span></div>{badge}</div>')
    st.html(f'<div class="card" style="gap:6px"><span class="title" style="margin-bottom:8px">Units</span>{rows}</div>')