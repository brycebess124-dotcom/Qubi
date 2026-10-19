# Qubi look: the theme (dark or light) and every drawing (shapes, mists, boxes, circuits).

import base64
import streamlit as st
from engine.qubits import State

BLACK = "#18181B"
WHITE = "#FFFFFF"
PAPER = "#F6F5F1"      # diagrams always sit on light paper, in both themes
TEAL = "#0891B2"
SIZE = 34              # size of one shape
GAP = 12               # space on each side of the | bar
SVG = 'xmlns="http://www.w3.org/2000/svg"'   # needed so drawings show as images


# ================= 1. theme =================

THEMES = {
    "dark": {"page": "#141A26", "bar": "#111113", "card": "#1C1C21", "well": "#141A26", "edge": "#3A4050",
             "line": "rgba(255,255,255,0.07)", "text": "#D4D4D8", "strong": "#F4F4F5", "muted": "#8B8B94",
             "soft": "#A1A1AA", "track": "#262B38", "locked": "#262B36", "drop": "#1A1E27",
             "banner": "#221B3A", "banner-text": "#C9C3DE", "good": "#0E2A1C", "good-text": "#4ADE80",
             "good-body": "#D1E7D9", "bad": "#2A1018", "bad-text": "#FB7185", "bad-body": "#FECDD3"},
    "light": {"page": "#F2F2F6", "bar": "#FFFFFF", "card": "#FFFFFF", "well": "#F4F4F7", "edge": "#D4D4DC",
              "line": "rgba(24,24,27,0.08)", "text": "#3F3F46", "strong": "#18181B", "muted": "#71717A",
              "soft": "#52525B", "track": "#E4E4EA", "locked": "#E4E4EA", "drop": "#CDCDD5",
              "banner": "#EFEAFE", "banner-text": "#5B4B8A", "good": "#E7F8EE", "good-text": "#15803D",
              "good-body": "#166534", "bad": "#FDECEF", "bad-text": "#BE123C", "bad-body": "#9F1239"},
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&family=Doto:wght@900&display=swap');
html, body, p, h1, h2, h3, a, button, input, label, li,
span:not([data-testid="stIconMaterial"]) { font-family: 'Space Grotesk', sans-serif !important; }

/* page */
.stApp { background: var(--page); color: var(--text); }
header[data-testid="stHeader"] { background: transparent; }
.stAppDeployButton { display: none; }
.block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1180px; }
[data-testid="stSidebar"] { background: var(--bar); border-right: 1px solid var(--line); }
[data-testid="stSidebarContent"] a { border-radius: 14px; min-height: 48px; padding-left: 14px; }
.stApp p, .stApp label, [data-testid="stSidebarContent"] span { color: var(--text); }
a, a:hover { text-decoration: none !important; }

/* text */
.stApp .label { font-family: 'Space Mono', monospace !important; font-size: 12px; letter-spacing: 0.08em; color: var(--muted); }
.stApp .big-number { font-family: 'Doto', monospace !important; font-weight: 900; font-size: 46px; color: var(--strong); line-height: 1; }
.title { color: var(--strong); font-weight: 600; font-size: 17px; }
.small { color: var(--muted); font-size: 14px; }
.strong { color: var(--strong); }
.hero  { color: var(--strong); font-size: 56px; line-height: 1.05; font-weight: 700; letter-spacing: -0.02em; }
.lead  { color: var(--soft); font-size: 19px; line-height: 1.55; }
.heading { color: var(--strong); font-size: 26px; font-weight: 700; line-height: 1.2; }
.big-title { color: var(--strong); font-size: 36px; font-weight: 700; line-height: 1.15; letter-spacing: -0.01em; }
.body { color: var(--text); font-size: 18px; line-height: 1.55; }
@media (max-width: 640px) { .hero { font-size: 40px; } .big-title { font-size: 28px; } }

/* building blocks */
.card  { background: var(--card); border: 1px solid var(--line); border-radius: 22px;
         padding: 20px 22px; display: flex; flex-direction: column; gap: 14px; }
.row   { display: flex; align-items: center; gap: 16px; }
.stack { display: flex; flex-direction: column; gap: 3px; min-width: 0; }
.chip  { display: flex; align-items: center; gap: 8px; height: 44px; padding: 0 14px; border-radius: 14px;
         background: var(--card); border: 1px solid var(--line); color: var(--strong); font-weight: 700; }
.bar   { height: 8px; border-radius: 99px; background: var(--track); overflow: hidden; }
.bar > div { height: 100%; border-radius: 99px; background: #8B5CF6; }
.node  { width: 76px; height: 76px; border-radius: 50%; flex: none; display: flex;
         align-items: center; justify-content: center; font-size: 32px; font-weight: 700; }
.paper { display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 26px; border-radius: 26px;
         border: 1px solid rgba(24,24,27,0.07);
         color: #18181B; background: #F6F5F1 radial-gradient(rgba(24,24,27,0.09) 1px, transparent 1px);
         background-size: 18px 18px; }
.paper .note { color: #3F3F46; font-size: 15px; text-align: center; }
.steps { display: flex; gap: 6px; }
.steps span { flex: 1; height: 8px; border-radius: 99px; background: var(--track); }
.steps .done { background: #8B5CF6; }
.steps .now  { background: #22D3EE; }
@media (max-width: 900px) { .robot { display: none !important; } }

/* buttons */
.stButton button { border-radius: 14px; font-weight: 700; min-height: 44px; }
[data-testid="stBaseButton-secondary"] { background: var(--card); color: var(--strong); border: 1.5px solid var(--edge); }
[data-testid="stBaseButton-secondary"]:hover { border-color: #8B5CF6; color: var(--strong); }
[data-testid="stBaseButton-secondary"]:disabled { background: var(--card); color: var(--muted); border-color: var(--line); }
[data-testid="stBaseButton-primary"] { background: #7C3AED; color: #FFFFFF; border: none; box-shadow: 0 4px 0 #4C1D95; min-height: 50px; }
[data-testid="stBaseButton-primary"]:hover { background: #8B5CF6; color: #FFFFFF; border: none; }
[data-testid="stBaseButton-tertiary"] { color: var(--muted); }
[data-testid="stBaseButton-tertiary"]:hover { color: var(--strong); }
[data-testid="stBaseButton-primary"] p { color: #FFFFFF; }
[data-testid="stBaseButton-secondary"] p { color: var(--strong); }
[data-testid="stBaseButton-secondary"]:disabled p { color: var(--muted); }
[data-testid="stBaseButton-tertiary"] p { color: inherit; }
[class*="st-key-go_"] button { background: #22D3EE; color: #0B1220; border: none; }      /* cyan: key starts with go_ */
[class*="st-key-go_"] button:hover { background: #67E8F9; color: #0B1220; border: none; }
[class*="st-key-go_"] button p { color: #0B1220; }

/* answer options in lessons and quizzes: key starts with pick_ */
[class*="st-key-pick_"] button { min-height: 60px; justify-content: flex-start; text-align: left; padding: 0 18px;
                                  border-radius: 16px; border: 2px solid var(--edge); font-size: 17px; font-weight: 500; }
[class*="st-key-pick_"] button p { font-size: 17px; color: var(--strong); white-space: normal; text-align: left; line-height: 1.35; }
[class*="st-key-pick_"] button { padding-top: 10px; padding-bottom: 10px; height: auto; }
[class*="st-key-pick_"] button div, [class*="st-key-pick_"] button span { justify-content: flex-start; }
[class*="st-key-pick_"] button code { background: transparent; border: 1.5px solid var(--edge); border-radius: 8px;
                                       padding: 3px 9px; margin-right: 10px; color: var(--muted); font-size: 13px; }
[class*="st-key-pick_"] button:disabled { background: var(--card) !important; color: var(--soft) !important; }
[class*="st-key-pick_right"] button:disabled { background: rgba(34,197,94,0.12) !important; border-color: #22C55E !important;
                                               color: var(--strong) !important; font-weight: 600; }
[class*="st-key-pick_wrong"] button:disabled { background: rgba(244,63,94,0.12) !important; border-color: #F43F5E !important;
                                               color: var(--strong) !important; font-weight: 600; }
[class*="st-key-pick_"] button:disabled p { color: var(--soft) !important; }
[class*="st-key-pick_right"] button:disabled p, [class*="st-key-pick_wrong"] button:disabled p { color: var(--strong) !important; }

/* lesson circles on the path: key starts with node_ */
[class*="st-key-node_"] button { width: 76px; height: 76px; min-height: 76px; padding: 0; border-radius: 50%; border: none; }
[class*="st-key-node_"] button p { font-size: 30px; font-weight: 700; }
[class*="st-key-node_"] button [data-testid="stIconMaterial"] { font-size: 34px; }
[class*="st-key-node_done"] button { background: #8B5CF6; color: #FFFFFF; box-shadow: 0 6px 0 #5B21B6; }
[class*="st-key-node_done"] button:hover { background: #A78BFA; color: #FFFFFF; }
[class*="st-key-node_now"] { position: relative; margin-top: 44px; }
[class*="st-key-node_now"]::before { content: "CONTINUE"; position: absolute; top: -42px; left: 50%; transform: translateX(-50%);
    background: #22D3EE; color: #0B1220; font: 700 13px 'Space Grotesk', sans-serif; letter-spacing: 0.08em;
    padding: 7px 12px; border-radius: 10px; white-space: nowrap; }
[class*="st-key-node_now"] button { background: #22D3EE; color: #0B1220;
    box-shadow: 0 6px 0 #0E7490, 0 0 0 9px var(--page), 0 0 0 15px rgba(34,211,238,0.35); }
[class*="st-key-node_now"] button:hover { background: #67E8F9; color: #0B1220; }
[class*="st-key-node_now"] button p { color: #0B1220; }
[class*="st-key-node_lock"] button, [class*="st-key-node_lock"] button:disabled {
    background: var(--locked) !important; color: #7A8090 !important; box-shadow: 0 6px 0 var(--drop); opacity: 1; border: none !important; }
[class*="st-key-node_lock_test"] button { border-radius: 24px; }
[class*="st-key-row_"] { overflow: visible !important; padding: 0 0 4px 16px; }
[class*="st-key-node_test"] button { border-radius: 24px; background: #123A44; color: #22D3EE; box-shadow: 0 6px 0 #0B2530; }
[class*="st-key-node_test"] button:hover { background: #164E5C; color: #67E8F9; }
[class*="st-key-node_testdone"] button { background: #8B5CF6; color: #FFFFFF; box-shadow: 0 6px 0 #5B21B6; }

/* unit headers: key starts with unit_ */
[class*="st-key-unit_"] { border-radius: 22px; padding: 16px 18px; background: var(--card); border: 1px solid var(--line); }
[class*="st-key-unit_now"] { background: #6D28D9; border: none; box-shadow: 0 6px 0 #4C1D95; padding: 20px 22px; }
[class*="st-key-unit_"] button { width: 44px; min-height: 44px; padding: 0; border-radius: 12px; }
[class*="st-key-unit_now"] button { background: rgba(255,255,255,0.16); border: none; color: #FFFFFF; }

/* boxes: containers whose key starts with card_ look like cards */
[class*="st-key-card_"] { background: var(--card); border: 1px solid var(--line); border-radius: 22px; padding: 18px 20px; }
.st-key-banner { background: var(--banner); border: 1px solid rgba(139,92,246,0.4); border-radius: 20px; padding: 16px 18px; }
.st-key-account_card, .st-key-builder, .st-key-paces {
    background: var(--card); border: 1px solid var(--line); border-radius: 24px; padding: 26px; }
.st-key-question { border-radius: 28px; padding: 30px; color: #18181B;
    background: #F6F5F1 radial-gradient(rgba(24,24,27,0.09) 1px, transparent 1px); background-size: 18px 18px; }
.st-key-question p { color: #3F3F46; }
.st-key-topbar { background: var(--bar); border-bottom: 1px solid var(--line); padding: 10px 6px 14px; margin-bottom: 18px; }
[class*="st-key-entry_"], [class*="st-key-gate_row_"] { background: var(--well); border: 1px solid var(--line); border-radius: 16px; padding: 10px 12px; }
.st-key-good { background: var(--good); border-top: 2px solid #22C55E; border-radius: 18px; padding: 18px 22px; }
.st-key-bad  { background: var(--bad);  border-top: 2px solid #F43F5E; border-radius: 18px; padding: 18px 22px; }
.st-key-celebrate { max-width: 520px; margin: 0 auto; background: var(--bar); border: 1px solid var(--line);
                    border-radius: 30px; padding: 34px 30px; }

/* inputs */
[data-testid="stTextInputRootElement"], [data-testid="stNumberInputContainer"] {
    background: var(--card); border: 1.5px solid var(--edge); border-radius: 14px; }
[data-testid="stTextInputRootElement"]:focus-within { border-color: #8B5CF6; }
.stTextInput input { min-height: 46px; font-size: 16px; color: var(--strong); }
[data-testid="stSelectbox"] [role="group"] { background: var(--card); border: 1.5px solid var(--edge); border-radius: 12px; }
[data-testid="stSelectbox"] input { color: var(--strong); }
[data-testid="stSelectboxVirtualDropdown"] { background: var(--card); border: 1px solid var(--line); }
[data-testid="stSelectboxVirtualDropdown"] [role="option"] { color: var(--strong); }
[data-testid="stTab"] p { color: var(--muted); font-weight: 600; }
[data-testid="stTab"][aria-selected="true"] p { color: #8B5CF6; }
button[data-variant="segmented_control"] { background: var(--card); color: var(--soft); border-color: var(--edge); }
button[data-variant="segmented_control"][aria-checked="true"] { background: rgba(139,92,246,0.16); color: var(--strong); border-color: #8B5CF6; }
button[data-variant="segmented_control"] p { color: inherit; }
[data-testid="stCode"] pre { background: #0E1119; border-radius: 14px; }
[data-testid="stCode"] code { color: #C4C4CC; font-family: 'Space Mono', monospace !important; font-size: 13px; }
"""


def load_style():
    """Fonts, colors and building blocks for the chosen theme. Called once in main.py."""
    colors = "".join(f"--{name}: {value}; " for name, value in THEMES[theme()].items())
    st.html("<style>:root { " + colors + "} " + CSS + "</style>")


def theme():
    return st.session_state.get("theme", "dark")


def color(name):
    """A theme color for drawings (images can't read the CSS colors above)."""
    return THEMES[theme()][name]


# ================= 2. shapes and mists =================

def draw_shape(shape, color, x, y, size=SIZE):
    """One qubit. color 0 = white, 1 = black."""
    fill = WHITE if color == 0 else BLACK
    style = f'fill="{fill}" stroke="{BLACK}" stroke-width="2.5"'
    m = size / 2

    if shape == "circle":
        return f'<circle cx="{x + m}" cy="{y + m}" r="{m - 2}" {style}/>'
    if shape == "square":
        return f'<rect x="{x + 2}" y="{y + 2}" width="{size - 4}" height="{size - 4}" {style}/>'
    if shape == "triangle":
        return f'<polygon points="{x + m},{y + 2} {x + size - 2},{y + size - 2} {x + 2},{y + size - 2}" {style}/>'
    if shape == "diamond":
        return f'<polygon points="{x + m},{y + 1} {x + size - 1},{y + m} {x + m},{y + size - 1} {x + 1},{y + m}" {style}/>'
    if shape == "pentagon":
        top = size * 0.4
        return (f'<polygon points="{x + m},{y + 2} {x + size - 2},{y + top} {x + size - 7},{y + size - 2} '
                f'{x + 7},{y + size - 2} {x + 2},{y + top}" {style}/>')


def draw_cloud(width, height):
    """Mist outline made of little loops, drawn clockwise around the edges."""
    left, top, right, bottom = 7, 7, width - 7, height - 7
    loops_across = max(round((right - left) / 15), 1)
    loops_down = max(round((bottom - top) / 15), 1)
    step_x = (right - left) / loops_across
    step_y = (bottom - top) / loops_down

    path = f"M {left} {top} "
    for i in range(1, loops_across + 1):
        path += f"A 8 8 0 0 1 {left + i * step_x} {top} "       # top edge
    for i in range(1, loops_down + 1):
        path += f"A 8 8 0 0 1 {right} {top + i * step_y} "      # right edge
    for i in range(1, loops_across + 1):
        path += f"A 8 8 0 0 1 {right - i * step_x} {bottom} "   # bottom edge
    for i in range(1, loops_down + 1):
        path += f"A 8 8 0 0 1 {left} {bottom - i * step_y} "    # left edge

    return f'<path d="{path}Z" fill="none" stroke="{BLACK}" stroke-width="2"/>'


def draw_state(state, size=SIZE):
    """Draws a state: shapes, | bars, minus signs, and a cloud if it's a mist."""
    mist = state.is_mist()
    padding = 26 if mist else 2
    x = padding
    y = padding
    parts = []

    entries = state.entries.items() if isinstance(state.entries, dict) else state.entries   # untidy mists are lists
    for number, (colors, sign) in enumerate(sorted(entries)):
        if number > 0:                                         # bar between entries
            x += GAP
            parts.append(f'<rect x="{x}" y="{y}" width="2" height="{size}" fill="{BLACK}"/>')
            x += 2 + GAP
        if sign < 0:                                           # minus sign
            parts.append(f'<rect x="{x}" y="{y + size / 2 - 1}" width="10" height="3" fill="{BLACK}"/>')
            x += 14
        if abs(sign) > 1:                                      # a weight, like 2
            parts.append(f'<text x="{x}" y="{y + size * 0.7}" font-size="18" font-weight="700" '
                         f'font-family="monospace" fill="{BLACK}">{abs(sign)}</text>')
            x += 16
        for i, color in enumerate(colors):                     # the shapes
            if i > 0:
                x += 6                                         # small gap between shapes
            parts.append(draw_shape(state.shapes[i], color, x, y, size))
            x += size

    width = x + padding
    height = size + padding * 2
    if mist:
        parts.insert(0, draw_cloud(width, height))
    return f'<svg {SVG} width="{width}" height="{height}">{"".join(parts)}</svg>'


def words(state):
    """A state in words, like 'white circle | minus black circle'."""
    entries = []
    for colors, sign in sorted(state.entries.items()):
        shapes = ", ".join(f"{'black' if color else 'white'} {shape}" for shape, color in zip(state.shapes, colors))
        entries.append(("minus " if sign < 0 else "") + shapes)
    return " | ".join(entries) if entries else "nothing (everything canceled)"


def draw_colors(shapes, colors, size=18):
    """Small plain shapes in a row, for labels like the chances bars."""
    parts = [draw_shape(shape, color, i * (size + 4), 0, size) for i, (shape, color) in enumerate(zip(shapes, colors))]
    return f'<svg {SVG} width="{len(shapes) * (size + 4)}" height="{size}">{"".join(parts)}</svg>'


# ================= 3. boxes (gates) =================

# what is drawn on each peg of a box, from left to right
SLOTS = {"NOT": ["plus"], "H": ["H"], "Z": ["Z"], "CNOT": ["dot", "plus"], "CZ": ["dot", "Zdot"],
         "SWAP": ["x", "x"], "TOFFOLI": ["dot", "dot", "plus"]}
LABEL_COLORS = {"H": "#F87171", "Z": "#67E8F9"}


def draw_symbol(kind, x, y=31):
    """One symbol on a box: plus (flip), dot (control), H, Z, x (swap) or any short label."""
    if kind == "plus":
        return (f'<circle cx="{x}" cy="{y}" r="9" fill="#FFFFFF" stroke="{TEAL}" stroke-width="2"/>'
                f'<path d="M{x - 9} {y}H{x + 9}M{x} {y - 9}V{y + 9}" stroke="{TEAL}" stroke-width="2"/>')
    if kind == "dot":
        return f'<circle cx="{x}" cy="{y}" r="4.5" fill="{TEAL}"/>'
    if kind == "x":
        return (f'<path d="M{x - 6} {y - 6}L{x + 6} {y + 6}M{x + 6} {y - 6}L{x - 6} {y + 6}" '
                f'stroke="{BLACK}" stroke-width="2.2" stroke-linecap="round"/>')
    if kind == "Zdot":
        return (f'<circle cx="{x}" cy="{y}" r="10" fill="#67E8F9" stroke="{TEAL}" stroke-width="1.5"/>'
                f'<text x="{x}" y="{y + 5}" text-anchor="middle" font-family="sans-serif" font-size="13" '
                f'font-weight="700" fill="{BLACK}">Z</text>')
    color = LABEL_COLORS.get(kind, "#C4B5FD")                   # H, Z, or a game box like "?"
    return (f'<rect x="{x - 11}" y="{y - 11}" width="22" height="22" rx="3" fill="{color}" stroke="#52525B"/>'
            f'<text x="{x}" y="{y + 5}" text-anchor="middle" font-family="sans-serif" font-size="15" '
            f'font-weight="700" fill="{BLACK}">{kind}</text>')


def draw_gate(name):
    """A box with pegs, like the notes. Wider boxes take more shapes."""
    if name == "MEASURE":
        return (f'<svg {SVG} width="68" height="60">'
                f'<polygon points="2,12 10,6 66,6 58,12" fill="#52525B" stroke="{BLACK}" stroke-width="1.2"/>'
                f'<polygon points="58,12 66,6 66,44 58,50" fill="#27272A" stroke="{BLACK}" stroke-width="1.2"/>'
                f'<rect x="2" y="12" width="56" height="38" fill="#3F3F46" stroke="{BLACK}" stroke-width="1.2"/>'
                f'<path d="M17 37A13 13 0 0 1 43 37" fill="none" stroke="#F4F4F5" stroke-width="2"/>'
                f'<path d="M30 37L37 27" stroke="#F4F4F5" stroke-width="2" stroke-linecap="round"/></svg>')

    slots = SLOTS.get(name, [name])
    width = 8 + 60 * len(slots)
    parts = []
    for i in range(len(slots)):                                 # pegs on top and bottom
        x = 30 + 60 * i
        parts.append(f'<rect x="{x - 4}" y="4" width="16" height="5" fill="#DCDCE1" stroke="#6B6B73"/>'
                     f'<ellipse cx="{x + 4}" cy="4" rx="8" ry="2.4" fill="#F6F6F8" stroke="#6B6B73"/>'
                     f'<rect x="{x - 8}" y="50" width="16" height="5" fill="#DCDCE1" stroke="#6B6B73"/>'
                     f'<ellipse cx="{x}" cy="55" rx="8" ry="2.4" fill="#DCDCE1" stroke="#6B6B73"/>')
    parts.append(f'<polygon points="2,12 10,6 {width - 2},6 {width - 10},12" fill="#F6F6F8" stroke="#6B6B73" stroke-width="1.2"/>'
                 f'<polygon points="{width - 10},12 {width - 2},6 {width - 2},44 {width - 10},50" fill="#BBBBC2" stroke="#6B6B73" stroke-width="1.2"/>'
                 f'<rect x="2" y="12" width="{width - 12}" height="38" fill="#E9E9EC" stroke="#6B6B73" stroke-width="1.2"/>')
    if len(slots) > 1:                                          # line joining the pegs
        color = BLACK if name == "SWAP" else TEAL
        parts.append(f'<path d="M30 31H{30 + 60 * (len(slots) - 1)}" stroke="{color}" stroke-width="2"/>')
    for i, kind in enumerate(slots):
        parts.append(draw_symbol(kind, 30 + 60 * i))
    return f'<svg {SVG} width="{width}" height="60">{"".join(parts)}</svg>'


def draw_arrow(direction="down"):
    """Thick arrow pointing down or right."""
    if direction == "right":
        return (f'<svg {SVG} width="30" height="22"><rect x="0" y="7" width="18" height="8" fill="{BLACK}"/>'
                f'<polygon points="17,0 17,22 30,11" fill="{BLACK}"/></svg>')
    return (f'<svg {SVG} width="22" height="30"><rect x="7" y="0" width="8" height="18" fill="{BLACK}"/>'
            f'<polygon points="0,17 22,17 11,30" fill="{BLACK}"/></svg>')


# ================= 4. putting pictures on the page =================

def as_image(svg):
    """Turns an SVG drawing into an image (Streamlit blocks raw SVG)."""
    encoded = base64.b64encode(svg.encode()).decode()
    return f'<img src="data:image/svg+xml;base64,{encoded}">'


def draw_chances(state):
    """Every possible result of measuring, with its chance: 'white 50% or black 50%'."""
    parts = []
    for colors, chance in sorted(state.chances().items()):
        plain = as_image(draw_state(State(state.shapes, {colors: 1})))
        parts.append(f'<div class="stack" style="align-items:center; gap:6px">{plain}'
                     f'<span style="font-family:Space Mono, monospace; font-size:13px; color:#3F3F46">{round(chance * 100)}%</span></div>')
    joiner = '<span style="color:#52525B; font-size:16px; padding-bottom:22px">or</span>'
    return f'<div class="row" style="gap:18px; flex-wrap:wrap; justify-content:center; align-items:flex-end">{joiner.join(parts)}</div>'


def draw_item(item, small=False):
    """One thing in a picture: a state, a box name, the chances after measuring, or the ANSWER slot."""
    if item == "ANSWER":
        width, height = (72, 52) if small else (120, 72)
        return (f'<span style="width:{width}px; height:{height}px; border-radius:14px; border:2.5px dashed #71717A; display:flex; '
                f'align-items:center; justify-content:center; font-size:30px; font-weight:700; color:#71717A">?</span>')
    if isinstance(item, dict):
        return draw_chances(item["chances"])
    if isinstance(item, str):
        return as_image(draw_gate(item))
    return as_image(draw_state(item))


def picture(items, note="", across=False, arrows=True):
    """A paper card with the items in order, joined by arrows. across=True lays them out left to right.
    arrows=False just shows the items side by side."""
    arrow = as_image(draw_arrow("right" if across else "down")) if arrows else ""
    inside = arrow.join(draw_item(item, small=across) for item in items)
    direction = "row; flex-wrap:wrap; justify-content:center" if across or not arrows else "column"
    note = f'<span class="note">{note}</span>' if note else ""
    gap = "12px" if arrows else "26px"
    return (f'<div class="paper"><div style="display:flex; flex-direction:{direction}; align-items:center; gap:{gap}; '
            f'max-width:100%; overflow-x:auto">{inside}</div>{note}</div>')


# ================= 5. circuits (for the Circuit Lab) =================

def draw_circuit(shapes, starts, steps, upto=None):
    """Wires left to right with boxes on them. Steps after `upto` are faded."""
    rows = {shape: 44 + 70 * i for i, shape in enumerate(shapes)}
    width = 120 + 70 * max(len(steps), 5)
    height = 44 + 70 * (len(shapes) - 1) + 44
    parts = []
    for shape, y in rows.items():                               # wires and starting shapes
        parts.append(f'<rect x="76" y="{y - 1}" width="{width - 90}" height="2" fill="#52525B"/>'
                     f'<rect x="14" y="{y - 22}" width="54" height="44" rx="11" fill="#FFFFFF" stroke="rgba(24,24,27,0.18)"/>'
                     + draw_shape(shape, starts[shapes.index(shape)], 28, y - 13, 26))
    for k, (name, on) in enumerate(steps):
        x = 120 + 70 * k
        fade = ' opacity="0.3"' if upto is not None and k >= upto else ""
        group = [f'<text x="{x}" y="14" text-anchor="middle" font-family="monospace" font-size="12" fill="#71717A">{k + 1}</text>']
        ys = [rows[shape] for shape in on]
        if len(on) > 1:
            group.append(f'<path d="M{x} {min(ys)}V{max(ys)}" stroke="{BLACK if name == "SWAP" else TEAL}" stroke-width="2"/>')
        for kind, y in zip(SLOTS[name], ys):
            if kind in ("H", "Z"):
                group.append(f'<rect x="{x - 20}" y="{y - 20}" width="40" height="40" rx="8" fill="#E9E9EC" stroke="#6B6B73"/>')
            group.append(draw_symbol(kind, x, y))
        parts.append(f'<g{fade}>{"".join(group)}</g>')
    return f'<svg {SVG} width="{width}" height="{height}">{"".join(parts)}</svg>'


def chances_bars(state):
    """Purple bars: the chance of every result, including the impossible ones."""
    count = len(state.shapes)
    chances = state.chances()
    bars = ""
    for number in range(2 ** count):
        colors = tuple((number >> (count - 1 - i)) & 1 for i in range(count))
        chance = round(chances.get(colors, 0) * 100)
        weight = "700" if chance else "400"
        bars += (f'<div class="stack" style="align-items:center; gap:6px">'
                 f'<span style="font-family:Space Mono, monospace; font-size:13px; font-weight:{weight}; color:#18181B">{chance}%</span>'
                 f'<span style="width:100%; max-width:46px; height:120px; border-radius:10px; background:#E4E4E7; '
                 f'display:flex; align-items:flex-end; overflow:hidden"><span style="width:100%; height:{chance}%; background:#8B5CF6"></span></span>'
                 f'{as_image(draw_colors(state.shapes, colors, 14))}</div>')
    return f'<div style="display:grid; grid-template-columns:repeat({2 ** count}, minmax(0, 1fr)); gap:10px; align-items:end">{bars}</div>'