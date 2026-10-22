# Circuit Lab: build any circuit, step through it, measure it, and export it to IBM.

import collections
import streamlit as st
from engine.qubits import State, apply, SHAPES
from engine.qasm import to_qasm, ibm_label, COMPOSER
from engine.ui import draw_state, draw_circuit, chances_bars, as_image, draw_colors
from engine.parts import plural

PEGS = {"NOT": 1, "H": 1, "Z": 1, "CNOT": 2, "CZ": 2, "SWAP": 2, "TOFFOLI": 3}
PEG_NAMES = {1: ["On"], 2: ["Control", "Target"], 3: ["Control 1", "Control 2", "Target"]}
MAX_SHAPES = 3

lab = st.session_state.setdefault("lab", {"name": "Bell pair", "shapes": ["circle", "square"], "starts": [0, 0],
                                          "steps": [("H", ["circle"]), ("CNOT", ["circle", "square"])],
                                          "show": None, "counts": None})


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


@st.dialog("Run it on a real IBM quantum computer", width="large", icon=":material/ios_share:")
def export_to_ibm():
    """A pop-up with four steps, the code to paste into IBM Quantum Composer, and how to read IBM's answer."""
    code = to_qasm(lab["name"], lab["shapes"], lab["starts"], lab["steps"])
    st.html('''<span class="small" style="line-height:1.5">IBM lets anyone run circuits on its quantum computers for free
        (up to 10 minutes a month). No coding needed: you copy, paste and press Run.</span>''')
    steps = ["<b>Copy the code</b> below (copy button in its top corner), or download it to keep.",
             "<b>Open IBM Quantum Composer</b> and sign in. The first time, make a free account and pick the "
             "free <b>Open Plan</b>.",
             "In Composer, open <b>View → Panels → Code Editor</b>. Select everything in the editor, delete it, "
             "and paste your code. Your circuit appears, drawn IBM's way.",
             "Press <b>Run circuit</b>, pick any quantum computer, and press Run. When the job finishes, open it "
             "from <b>Workloads</b> to see the results."]
    st.html('<div class="stack" style="gap:12px">' + "".join(f'<div class="row" style="gap:12px; align-items:flex-start"><span class="node" style="width:26px; '
                    f'height:26px; font-size:13px; background:#7C3AED; color:#FFFFFF">{number}</span>'
                    f'<span style="color:var(--text); font-size:15px; line-height:1.5">{step}</span></div>'
                    for number, step in enumerate(steps, start=1)) + "</div>")
    with st.container(horizontal=True):
        st.download_button("Download the code", code, file_name="qubi-circuit.qasm", icon=":material/download:",
                           on_click="ignore")
        st.link_button("Open IBM Quantum Composer", COMPOSER, icon=":material/open_in_new:")
    st.code(code, language=None)

    final = state_after(len(lab["steps"]))
    rows = "".join(f'<div class="row" style="gap:14px; min-height:34px">'
                   f'<span style="font-family:Space Mono, monospace; font-weight:700; color:var(--strong); width:44px">{ibm_label(colors)}</span>'
                   f'<span class="paper" style="padding:5px 8px; border-radius:8px">{as_image(draw_colors(lab["shapes"], colors, 16))}</span>'
                   f'<span class="small">Qubi says {round(chance * 100)}%</span></div>'
                   for colors, chance in sorted(final.chances().items()) if chance > 0)
    order = ", ".join(lab["shapes"])
    st.html(f'''<div class="stack" style="gap:8px; padding-top:6px; border-top:1px solid var(--line)">
        <span class="strong" style="font-weight:600; padding-top:10px">How to read IBM's answer</span>
        <span class="small" style="line-height:1.5">IBM shows a bar for each result, labeled with 0s and 1s.
        0 means white and 1 means black, in the same order as your shapes ({order}).
        Real machines are a little noisy, so you'll also see small bars for results Qubi says can't happen.</span>
        {rows}</div>''')


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
        export_to_ibm()
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
    picked = st.segmented_control("Show the state after", stops, default=stops[shown], required=True,
                                  key=f"show_{len(lab['steps'])}")
    if stops.index(picked) != shown:
        lab["show"] = stops.index(picked)
        lab["counts"] = None
        st.rerun()

# ================= right: the output =================
with output:
    if state.is_entangled():
        badge, note = "Entangled", "These qubits are linked: this cloud can't be split into one cloud per qubit."
    elif state.is_superposition():
        badge, note = "Superposition", "Measuring picks one of these entries at random."
    else:
        badge, note = "Plain shapes", "No superposition: measuring always gives exactly this."
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