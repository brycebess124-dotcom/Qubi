# Circuit Lab: build any circuit, step through the mist, measure it, and export it to IBM.

import collections
import streamlit as st
from engine.qubits import State, apply, SHAPES
from engine.qasm import to_qasm
from engine.ui import draw_state, draw_circuit, chances_bars, as_image, draw_colors
from engine.parts import plural

PEGS = {"NOT": 1, "H": 1, "Z": 1, "CNOT": 2, "CZ": 2, "SWAP": 2, "TOFFOLI": 3}
PEG_NAMES = {1: ["On"], 2: ["Control", "Target"], 3: ["Control 1", "Control 2", "Target"]}
MAX_SHAPES = 3

lab = st.session_state.setdefault("lab", {"name": "Bell pair", "shapes": ["circle", "square"], "starts": [0, 0],
                                          "steps": [("H", ["circle"]), ("CNOT", ["circle", "square"])],
                                          "show": None, "counts": None, "export": False})


def state_after(count):
    """The state after the first `count` boxes."""
    state = State(lab["shapes"], {tuple(lab["starts"]): 1})
    for name, on in lab["steps"][:count]:
        state = apply(state, f"{name} {' '.join(on)}")
    return state


def changed():
    """The circuit changed, so old measurements no longer count."""
    lab["counts"] = None
    lab["show"] = None


# ---------------- title and tools ----------------
with st.container(horizontal=True, vertical_alignment="center"):
    with st.container(gap="small"):
        st.html('<span class="strong" style="font-size:28px; font-weight:700">Circuit Lab</span>')
        lab["name"] = st.text_input("Circuit name", value=lab["name"], label_visibility="collapsed", width=220)
        st.html(f'<span class="small">{plural(len(lab["shapes"]), "shape")} · {plural(len(lab["steps"]), "box", "boxes")}</span>')
    if st.button("Undo", icon=":material/undo:", disabled=not lab["steps"]):
        lab["steps"].pop()
        changed()
        st.rerun()
    if st.button("Clear", icon=":material/delete:", disabled=not lab["steps"]):
        lab["steps"] = []
        changed()
        st.rerun()
    if st.button("Export to IBM", icon=":material/ios_share:"):
        lab["export"] = not lab["export"]
        st.rerun()
    measure = st.button("Measure 100×", type="primary", icon=":material/play_arrow:")

shown = len(lab["steps"]) if lab["show"] is None else lab["show"]
state = state_after(shown)
if measure:
    lab["counts"] = collections.Counter(tuple(state.copy().measure().values()) for _ in range(100))

build, output = st.columns([1.7, 1], gap="large")

# ================= left: build the circuit =================
with build:
    # shapes and their starting colors
    with st.container(key="card_shapes"):
        st.html('<span class="label">SHAPES · CLICK ONE TO CHANGE ITS STARTING COLOR</span>')
        with st.container(horizontal=True):
            for spot, shape in enumerate(lab["shapes"]):
                color = "black" if lab["starts"][spot] else "white"
                if st.button(f"{shape.capitalize()} starts {color}", key=f"start_{shape}"):
                    lab["starts"][spot] = 1 - lab["starts"][spot]
                    changed()
                    st.rerun()
            if len(lab["shapes"]) < MAX_SHAPES and st.button("Add shape", icon=":material/add:"):
                lab["shapes"].append(SHAPES[len(lab["shapes"])])
                lab["starts"].append(0)
                changed()
                st.rerun()
            if len(lab["shapes"]) > 1 and st.button("Remove shape", icon=":material/remove:"):
                gone = lab["shapes"].pop()
                lab["starts"].pop()
                lab["steps"] = [(name, on) for name, on in lab["steps"] if gone not in on]
                changed()
                st.rerun()

    # pick a box and the shapes it goes on
    with st.container(key="card_boxes"):
        st.html('<span class="label">ADD A BOX</span>')
        usable = [name for name, pegs in PEGS.items() if pegs <= len(lab["shapes"])]
        name = st.segmented_control("Box", usable, default="H", required=True, key="box_choice",
                                    format_func=lambda box: "Toffoli" if box == "TOFFOLI" else box,
                                    label_visibility="collapsed")
        with st.container(horizontal=True, vertical_alignment="bottom"):
            on = [st.selectbox(peg, lab["shapes"], index=i % len(lab["shapes"]), key=f"peg_{name}_{i}")
                  for i, peg in enumerate(PEG_NAMES[PEGS[name]])]
            if st.button("Add", type="primary", icon=":material/add:", disabled=len(set(on)) < len(on)):
                lab["steps"].append((name, on))
                changed()
                st.rerun()
        if len(set(on)) < len(on):
            st.html('<span class="small">Pick a different shape for each peg.</span>')

    # the circuit drawing and the step picker
    st.html(f'<div class="paper" style="align-items:flex-start; overflow-x:auto">'
            f'{as_image(draw_circuit(lab["shapes"], lab["starts"], lab["steps"], upto=shown))}</div>')
    stops = ["Start"] + [f"Step {n}" for n in range(1, len(lab["steps"]) + 1)]
    picked = st.segmented_control("Show the mist after", stops, default=stops[shown], required=True,
                                  key=f"show_{len(lab['steps'])}")
    if stops.index(picked) != shown:
        lab["show"] = stops.index(picked)
        lab["counts"] = None
        st.rerun()

    # export to IBM
    if lab["export"]:
        with st.container(key="card_export"):
            st.html('''<div class="stack" style="gap:6px"><span class="title">Run it on real hardware</span>
                <span class="small" style="line-height:1.5">Copy this code (the copy button is in the corner) and paste it
                into the code editor in IBM Quantum Composer. Real machines are noisy, so expect results a little
                off from the chances shown here.</span></div>''')
            st.code(to_qasm(lab["shapes"], lab["starts"], lab["steps"]), language=None)

# ================= right: the output =================
with output:
    if state.is_entangled():
        badge, note = "Entangled", "These shapes are linked: you can't split this mist into a separate mist for each shape."
    elif state.is_mist():
        badge, note = "Mist", "Measuring picks one of these entries at random."
    else:
        badge, note = "Plain shapes", "No mist: measuring always gives exactly this."
    counts = ""
    if lab["counts"]:
        counts = "".join(f'<span class="row" style="gap:6px">{as_image(draw_colors(lab["shapes"], colors, 12))} {count}</span>'
                         for colors, count in lab["counts"].most_common())
        counts = (f'<div class="row" style="justify-content:space-between; gap:10px; padding:12px 14px; border-radius:14px; '
                  f'background:#FFFFFF; border:1px solid rgba(24,24,27,0.08); flex-wrap:wrap">'
                  f'<span style="color:#3F3F46; font-size:14px">Last 100 measurements</span>'
                  f'<span class="row" style="gap:14px; font-family:Space Mono, monospace; font-size:13px; color:#18181B">{counts}</span></div>')
    st.html(f'''
    <div class="paper" style="align-items:stretch; gap:16px">
        <div class="row" style="justify-content:space-between">
            <span style="font-size:18px; font-weight:700">Output · {stops[shown]}</span>
            <span style="padding:5px 10px; border-radius:99px; background:#CFFAFE; color:#155E75; font-size:13px; font-weight:700">{badge}</span>
        </div>
        <div style="display:flex; justify-content:center; overflow-x:auto">{as_image(draw_state(state))}</div>
        <span style="color:#3F3F46; font-size:14px; line-height:1.5; text-align:center">{note}</span>
        <div class="stack" style="gap:10px; padding-top:14px; border-top:1px solid rgba(24,24,27,0.10)">
            <span class="label" style="color:#52525B">CHANCES</span>
            {chances_bars(state)}
        </div>
        {counts}
    </div>''')