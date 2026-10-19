# Small pieces used on many pages: logo, robot, icons, rings and cards.
# Each function returns HTML for st.html().

import course
from engine.ui import SVG, as_image, color

PURPLE = "#8B5CF6"
CYAN = "#22D3EE"
GREY = "#7A8090"


def plural(number, word, many=None):
    """plural(1, "day") is "1 day", plural(3, "day") is "3 days", plural(2, "box", "boxes") is "2 boxes"."""
    return f"{number} {word if number == 1 else many or word + 's'}"


# ================= icons =================

LINE_ICONS = {
    "check":  '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "lock":   '<rect x="5" y="11" width="14" height="9" rx="2.5"/><path d="M8.5 11V8a3.5 3.5 0 0 1 7 0v3"/>',
    "trophy": '<path d="M8 4h8v5a4 4 0 0 1-8 0V4Z"/><path d="M8 6H5.5a2.5 2.5 0 0 0 2.5 4M16 6h2.5A2.5 2.5 0 0 1 16 10M12 13v4M8.5 20h7M10 17h4"/>',
    "flag":   '<path d="M5 21V4M5 4h12l-2.5 4.5L17 13H5"/>',
    "book":   '<path d="M5 4.5A1.5 1.5 0 0 1 6.5 3H19v15H6.5A1.5 1.5 0 0 0 5 19.5v-15Z"/><path d="M5 19.5A1.5 1.5 0 0 0 6.5 21H19"/>',
    "clock":  '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "x":      '<path d="M6 6l12 12M18 6L6 18"/>',
    "bulb":   '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3Z"/>',
}


def icon(name, shade, size=22, thickness=2.2):
    """A line icon from LINE_ICONS as an image."""
    return as_image(f'<svg {SVG} width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
                    f'stroke="{shade}" stroke-width="{thickness}" stroke-linecap="round" '
                    f'stroke-linejoin="round">{LINE_ICONS[name]}</svg>')


def flame(size=22):
    return as_image(f'<svg {SVG} width="{size}" height="{size}" viewBox="0 0 24 24"><path fill="#A78BFA" '
                    f'd="M12 2.6c.6 3 3.2 4.6 4.9 7.3 1.6 2.6 1.9 5.5.4 7.8A6.2 6.2 0 0 1 12 21a6.2 6.2 0 0 1-5.3-3.3'
                    f'c-1.4-2.6-.8-5.6 1-7.6.2 1.6.9 2.9 2.1 3.6-.5-3.9.4-7.9 2.2-11.1Z"/>'
                    f'<path fill="#EDE9FE" d="M12.4 12.5c.9 1.3 2.4 2.3 2.4 4.1a2.8 2.8 0 0 1-5.6 0c0-1.5.9-2.4 '
                    f'1.6-3.2.1.7.4 1.2.9 1.5-.1-.9.2-1.7.7-2.4Z"/></svg>')


def bolt(size=20):
    return as_image(f'<svg {SVG} width="{size}" height="{size}" viewBox="0 0 24 24">'
                    f'<path fill="{CYAN}" d="M13 2.5 4.5 13.5H11l-1 8 8.5-11H12l1-8Z"/></svg>')


def logo(width=98):
    """The qubi logo: the q holds a target, the dot on the i is the control, and the wire joins them like a CNOT."""
    return as_image(f'''<svg {SVG} width="{width}" height="{width * 108 / 166}" viewBox="-2 -42 166 108">
  <g fill="none" stroke="{color('strong')}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="20" cy="20" r="16"/><path d="M36 4V60"/><path d="M56 4V20A16 16 0 0 0 88 20M88 4V36"/>
    <path d="M106 -22V36"/><circle cx="122" cy="20" r="16"/><path d="M156 4V36"/></g>
  <g fill="none" stroke="{PURPLE}" stroke-width="3.4" stroke-linecap="round"><path d="M10 20H30M20 31V-34H150"/></g>
  <circle cx="156" cy="-34" r="6" fill="{PURPLE}"/><circle cx="20" cy="20" r="3.8" fill="{CYAN}"/>
</svg>''')


ROBOT = as_image(f'''<svg {SVG} width="96" height="112" viewBox="0 0 120 140">
  <path d="M60 26V12" stroke="#A1A1AA" stroke-width="3" stroke-linecap="round"/><circle cx="60" cy="9" r="6" fill="{CYAN}"/>
  <rect x="15" y="46" width="9" height="18" rx="3" fill="#A1A1AA"/><rect x="96" y="46" width="9" height="18" rx="3" fill="#A1A1AA"/>
  <rect x="22" y="26" width="76" height="58" rx="18" fill="#E4E4E7"/><rect x="31" y="35" width="58" height="40" rx="12" fill="#18181B"/>
  <circle cx="48" cy="54" r="7" fill="#F4F4F5"/><circle cx="72" cy="54" r="6" fill="#18181B" stroke="#F4F4F5" stroke-width="2.6"/>
  <path d="M54 66Q60 70 66 66" fill="none" stroke="{CYAN}" stroke-width="2.4" stroke-linecap="round"/>
  <rect x="52" y="84" width="16" height="7" fill="#A1A1AA"/><rect x="24" y="96" width="9" height="26" rx="4.5" fill="#A1A1AA"/>
  <rect x="87" y="96" width="9" height="26" rx="4.5" fill="#A1A1AA"/><rect x="34" y="90" width="52" height="40" rx="13" fill="#E4E4E7"/>
  <circle cx="60" cy="110" r="10" fill="none" stroke="#C4B5FD" stroke-width="2"/><circle cx="60" cy="110" r="5.5" fill="{PURPLE}"/>
</svg>''')


def ring(percent, size, thickness, shade):
    """A circle that fills up clockwise. percent = 0 to 100."""
    radius = (size - thickness) / 2
    around = 2 * 3.1416 * radius
    middle = size / 2
    return as_image(f'<svg {SVG} width="{size}" height="{size}">'
                    f'<circle cx="{middle}" cy="{middle}" r="{radius}" fill="none" stroke="{color("track")}" stroke-width="{thickness}"/>'
                    f'<circle cx="{middle}" cy="{middle}" r="{radius}" fill="none" stroke="{shade}" stroke-width="{thickness}" '
                    f'stroke-linecap="round" stroke-dasharray="{around * percent / 100} {around}" '
                    f'transform="rotate(-90 {middle} {middle})"/></svg>')


def avatar(name, size=40):
    return (f'<span class="node" style="width:{size}px; height:{size}px; background:#7C3AED; color:#FFFFFF; '
            f'font-size:{size * 0.4}px">{name[:1].upper()}</span>')


def steps_bar(done, total):
    """Segments: done ones purple, the current one cyan, the rest grey."""
    spans = "".join('<span class="done"></span>' if i < done else '<span class="now"></span>' if i == done
                    else "<span></span>" for i in range(total))
    return f'<div class="steps">{spans}</div>'


# ================= the lesson path (Learn page) =================

def unit_text(number, unit, done, status):
    """The words on a unit header. status = complete, current or locked."""
    total = len(unit["lessons"])
    if status == "current":
        return f'''
        <div class="stack" style="gap:4px">
            <span class="label" style="color:#E9D5FF">UNIT {number} · IN PROGRESS</span>
            <span style="color:#FFFFFF; font-size:26px; font-weight:700">{unit["title"]}</span>
            <span style="color:#EDE4FF; font-size:15px">{unit["about"]}</span>
        </div>'''
    if status == "complete":
        badge = f'<span class="node" style="width:44px; height:44px; background:{PURPLE}">{icon("check", "white", 22, 2.6)}</span>'
        label, name_color, note = f"UNIT {number} · COMPLETE", "var(--strong)", f"{total} of {total} lessons"
    else:
        badge = f'<span class="node" style="width:44px; height:44px; background:var(--locked)">{icon("lock", GREY, 20, 2)}</span>'
        label, name_color = f"UNIT {number}", "var(--soft)"
        note = f"{plural(total, 'lesson')} · ~{total * course.MINUTES_PER_LESSON} min"
    return f'''
    <div class="row">
        {badge}
        <div class="stack">
            <span class="label">{label}</span>
            <span class="title" style="color:{name_color}">{unit["title"]}</span>
            <span class="small">{note}</span>
        </div>
    </div>'''


def unit_bar(done, total):
    return f'''
    <div class="row" style="gap:12px">
        <div class="bar" style="flex:1; height:10px; background:rgba(255,255,255,0.22)">
            <div style="width:{done / total * 100}%; background:#FFFFFF"></div></div>
        <span style="color:#FFFFFF; font-size:14px; font-weight:600">{done} of {total} lessons</span>
    </div>'''


def lesson_text(number, title, status):
    """The words next to a circle on the path. status = done, now or locked."""
    if status == "done":
        label, note = f"LESSON {number}", '<span style="color:#A78BFA; font-size:14px">Done · tap to review</span>'
    elif status == "now":
        label = f'<span style="color:{CYAN}">LESSON {number} · NOW</span>'
        note = f'<span class="small">{"Start here" if number == 1 else "Up next"}</span>'
    else:
        label, note = f"LESSON {number}", '<span class="small">Locked</span>'
    name_color = "var(--soft)" if status == "locked" else "var(--strong)"
    return (f'<div class="stack" style="padding-top:4px"><span class="label">{label}</span>'
            f'<span class="title" style="color:{name_color}">{title}</span>{note}</div>')


def test_text(unit, last_lesson, status, score=None):
    """The words next to a unit test on the path. status = done, now or locked."""
    if status == "done":
        title, note = f"Passed with {score}%", "Tap to retake"
    elif status == "now":
        title, note = "Ready to take", f"~10 min · pass with {course.PASS_MARK}%"
    else:
        title, note = f"Unlocks after Lesson {last_lesson}", f"~10 min · pass with {course.PASS_MARK}%"
    return (f'<div class="stack"><span class="label">UNIT {unit} TEST</span>'
            f'<span class="title" style="color:var(--soft)">{title}</span><span class="small">{note}</span></div>')


def robot_says(text):
    return f'''
    <div class="robot stack" style="align-items:center; gap:10px; padding-top:20px">
        <div class="card" style="padding:12px 14px; border-radius:16px; font-size:14px; line-height:1.4; color:var(--text)">{text}</div>
        {ROBOT}
    </div>'''


def final_test_card(status):
    note = {"locked": "Covers all 6 units · unlocks after every unit test",
            "now": "Covers all 6 units · ready when you are",
            "done": "Passed. You finished Qubi!"}[status]
    return f'''
    <div class="card" style="flex-direction:row; align-items:center; gap:16px; padding:16px 18px;
                             background:transparent; border:1.5px dashed var(--edge)">
        <span class="node" style="width:44px; height:44px; border-radius:14px; background:var(--locked)">{icon("flag", GREY, 20, 2)}</span>
        <div class="stack">
            <span class="title" style="color:var(--soft)">Final test</span>
            <span class="small">{note}</span>
        </div>
    </div>'''


# ================= cards on the right of the Learn page =================

def banner_text(headline, note):
    return f'''
    <div class="row">
        <span class="node" style="width:48px; height:48px; border-radius:14px; background:rgba(139,92,246,0.22)">{flame(28)}</span>
        <div class="stack">
            <span style="color:var(--strong); font-weight:600; font-size:16px">{headline}</span>
            <span style="color:var(--banner-text); font-size:14px">{note}</span>
        </div>
    </div>'''


def stat_chips(streak, xp):
    return f'''
    <div class="row" style="gap:10px">
        <span class="chip">{flame(20)} {streak} <span class="small">day streak</span></span>
        <span class="chip">{bolt()} {xp} <span class="small">XP</span></span>
    </div>'''


def progress_card(done, total, level, xp, xp_next):
    percent = round(done / total * 100)
    return f'''
    <div class="card" style="align-items:center; gap:18px">
        <div class="row" style="align-self:stretch; justify-content:space-between">
            <span class="title">Course progress</span><span class="small">6 units</span>
        </div>
        <div style="position:relative; width:168px; height:168px">
            {ring(percent, 168, 14, PURPLE)}
            <div class="stack" style="position:absolute; inset:0; align-items:center; justify-content:center">
                <span class="big-number">{percent}%</span>
                <span class="small" style="font-size:13px">{done} of {total} lessons</span>
            </div>
        </div>
        <div class="stack" style="align-self:stretch; gap:8px">
            <div class="row" style="justify-content:space-between; font-size:14px">
                <span class="strong" style="font-weight:600">Level {level}</span><span class="small">{xp} / {xp_next} XP</span>
            </div>
            <div class="bar"><div style="width:{min(xp / xp_next * 100, 100)}%"></div></div>
        </div>
    </div>'''


def goal_card(today, goal, lessons_left, finish):
    """Today's lessons, and the finish line. finish is text like OCT 31, or DONE."""
    note = "Daily goal done. Nice!" if today >= goal else f"{plural(goal - today, 'lesson')} to go today"
    plan = f"{plural(lessons_left, 'lesson')} + final test at {goal} a day" if lessons_left else "Every lesson is done"
    return f'''
    <div class="card" style="gap:16px">
        <span class="title">Today's goal</span>
        <div class="row" style="gap:14px">
            {ring(min(today / goal, 1) * 100, 60, 7, CYAN)}
            <div class="stack">
                <span class="strong" style="font-weight:600; font-size:16px">{today} of {plural(goal, 'lesson')}</span>
                <span class="small">{note}</span>
            </div>
        </div>
        <div style="height:1px; background:var(--line)"></div>
        <div class="row" style="justify-content:space-between">
            <div class="stack">
                <span class="label">FINISH LINE</span>
                <span class="small">{plan}</span>
            </div>
            <span class="big-number" style="font-size:30px; color:{CYAN}; white-space:nowrap">{finish}</span>
        </div>
    </div>'''


def week_dots(week, size=34):
    """M T W T F S S with a dot for each day."""
    days = ""
    for letter, day in zip("MTWTFSS", week):
        if day == "done":
            dot = f'<span class="node" style="width:{size}px; height:{size}px; background:{PURPLE}">{icon("check", "white", size * 0.47, 3)}</span>'
        elif day == "today":
            dot = (f'<span class="node" style="width:{size}px; height:{size}px; border:2.5px solid {CYAN}; box-sizing:border-box">'
                   f'<span style="width:8px; height:8px; border-radius:50%; background:{CYAN}"></span></span>')
        else:
            dot = f'<span class="node" style="width:{size}px; height:{size}px; border:2px solid var(--edge); box-sizing:border-box"></span>'
        shade = CYAN if day == "today" else "var(--muted)"
        days += f'<div class="stack" style="align-items:center; gap:8px"><span style="font-size:12px; color:{shade}">{letter}</span>{dot}</div>'
    return f'<div style="display:grid; grid-template-columns:repeat(7, 1fr); gap:6px">{days}</div>'


def week_card(week, best, streak):
    if "today" not in week:
        note = "Lesson done today. Your streak is safe!"
    elif streak == 0:
        note = "Finish a lesson today to start your streak."
    else:
        note = f"Finish a lesson today to make it {streak + 1}."
    return f'''
    <div class="card" style="gap:16px">
        <div class="row" style="justify-content:space-between">
            <span class="title">This week</span><span class="small">Best: {plural(best, 'day')}</span>
        </div>
        {week_dots(week)}
        <span class="small">{note}</span>
    </div>'''


def lab_card():
    return '''
    <div class="card">
        <span class="title">Circuit Lab</span>
        <span class="small" style="line-height:1.45">
            Build your own circuits from shapes and boxes and watch the mist change as you go.</span>
    </div>'''


# ================= cards on the Progress page =================

def stat_card(picture, name, number, note):
    return f'''
    <div class="card" style="gap:10px">
        <span class="row small" style="gap:8px">{picture} {name}</span>
        <span class="big-number">{number}</span>
        <span class="small" style="font-size:13px">{note}</span>
    </div>'''