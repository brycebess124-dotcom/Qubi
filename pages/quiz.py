# Quiz page: lesson quizzes, unit tests and the final test.
# Three kinds of questions: pick one, build the state, build the circuit.

import time
import streamlit as st
import course
from engine.qubits import State, apply
from engine.ui import picture, words
from engine.parts import bolt
from engine.progress import add_xp, answered, finish_lesson, finish_test, new_badges
from engine.widgets import top_bar, options, feedback, show_picture

if "quiz" not in st.session_state:
    st.switch_page("pages/home.py")

user = st.session_state.user
quiz = st.session_state.quiz
index = quiz["index"]
total = len(quiz["questions"])
lesson_number, question = quiz["questions"][index]
key = f"q{quiz['id']}_{index}"                       # keeps every question's boxes separate
checked = st.session_state.get("checked")            # set once this question's answer has been checked
if checked and checked["key"] != key:
    checked = None
target = [(gate.split()[0], gate.split()[1:]) for gate in question.get("target", [])]   # circuit questions

ROLES = {"NOT": ["On"], "H": ["On"], "Z": ["On"], "CNOT": ["Control", "Target"], "CZ": ["Control", "Target"],
         "SWAP": ["Swap", "With"], "TOFFOLI": ["Control", "Control", "Target"]}     # what each peg of a gate is for
CHIPS = {"pick": ("PICK ONE", "#5B21B6", "#EDE9FE"), "state": ("BUILD THE STATE", "#5B21B6", "#EDE9FE"),
         "circuit": ("BUILD THE CIRCUIT", "#155E75", "#CFFAFE")}
TIPS = {"pick": "Read every option before you pick.",
        "state": "The order of entries doesn't matter. Watch your signs.",
        "circuit": "The test runs update as you build. Make every one match."}


def run_gates(state, gates):
    for name, on in gates:
        state = apply(state, f"{name} {' '.join(on)}")
    return state


def check(correct, given, picked=None):
    """Saves the answer and shows the feedback bar. picked = which option, for pick-one questions."""
    if correct:
        quiz["xp"] += course.QUIZ_XP
        add_xp(user, course.QUIZ_XP)
    answered(user, correct)
    if question["type"] == "pick":
        right_answer = question["options"][question["answer"]]
    elif question["type"] == "state":
        right_answer = words(question["answer"])
    else:
        right_answer = "boxes in this order: " + ", ".join(question["target"])
    quiz["results"].append({"lesson": lesson_number, "question": question["question"], "correct": correct,
                            "given": given, "answer": right_answer})
    st.session_state.checked = {"key": key, "correct": correct, "given": given, "picked": picked}
    st.rerun()


def next_question():
    st.session_state.pop("checked", None)
    if index + 1 < total:
        quiz["index"] += 1
        st.rerun()
    right = sum(result["correct"] for result in quiz["results"])
    if quiz["kind"] == "lesson":
        finish_lesson(user, quiz["number"])
        st.session_state.completed = {"lesson": quiz["number"], "xp": quiz["xp"] + course.LESSON_XP,
                                      "badges": new_badges(user)}
        st.switch_page("pages/streak.py")
    unit = quiz["number"] if quiz["kind"] == "unit" else "final"
    percent = finish_test(user, unit, right, total)
    st.session_state.test_result = {"kind": quiz["kind"], "unit": unit, "title": quiz["title"], "right": right,
                                    "total": total, "percent": percent, "results": quiz["results"],
                                    "seconds": round(time.time() - quiz["started"]), "badges": new_badges(user)}
    st.switch_page("pages/results.py")


# ================= the answer builders =================

def state_builder():
    """Rows of entries: a sign, then a color for each shape. Returns the built state."""
    shapes = question["answer"].shapes
    ids = st.session_state.setdefault(f"{key}_entries", [0])
    columns = "".join(f'<span>{shape.upper()}</span>' for shape in shapes)
    st.html(f'<div class="label" style="display:grid; grid-template-columns:96px repeat({len(shapes)}, 1fr) 44px; '
            f'gap:12px; padding:0 14px"><span>SIGN</span>{columns}<span></span></div>')
    entries = {}
    for entry in ids:
        with st.container(key=f"entry_{key}_{entry}", horizontal=True, vertical_alignment="center"):
            sign = st.segmented_control("Sign", ["+", "−"], default="+", required=True,
                                        key=f"{key}_sign_{entry}", label_visibility="collapsed")
            colors = tuple(["White", "Black"].index(st.selectbox(shape, ["White", "Black"], key=f"{key}_{shape}_{entry}",
                                                                  label_visibility="collapsed")) for shape in shapes)
            if st.button("", icon=":material/delete:", key=f"{key}_delete_{entry}", type="tertiary", disabled=len(ids) == 1):
                ids.remove(entry)
                st.rerun()
        entries[colors] = entries.get(colors, 0) + (1 if sign == "+" else -1)
    if st.button("Add entry", icon=":material/add:", key=f"{key}_add", width="stretch"):
        ids.append(max(ids) + 1)
        st.rerun()

    built = State(shapes, {colors: sign for colors, sign in entries.items() if sign != 0})
    cloud_note = ("On: 2 or more entries make a superposition." if built.is_superposition()
                  else "Turns on by itself when you have 2 or more entries.")
    st.html(f'<div class="card" style="background:var(--well); padding:14px 16px; gap:2px">'
            f'<span class="strong" style="font-weight:600">Superposition (the cloud)</span><span class="small">{cloud_note}</span></div>')
    st.html('<span class="label">PREVIEW</span>')
    if built.entries:
        st.html(picture([built]))
    else:
        st.html('<span class="small">Your entries cancel out. Change a sign or a color.</span>')
    return built


def circuit_builder():
    """Rows of boxes: which box, and which shapes it goes on. Returns the gates and whether they're all valid."""
    shapes = question["inputs"][0].shapes
    allowed = [name for name in question["allowed"] if len(ROLES[name]) <= len(shapes)]
    chips = "".join(f'<span class="chip" style="height:34px; font-size:14px">{name}</span>' for name in allowed)
    st.html(f'<div class="row" style="gap:8px; flex-wrap:wrap"><span class="label">ALLOWED</span>{chips}</div>')
    ids = st.session_state.setdefault(f"{key}_gates", [])
    gates, valid = [], True
    for row, gate in enumerate(ids, start=1):
        with st.container(key=f"gate_row_{key}_{gate}", horizontal=True, vertical_alignment="center"):
            st.html(f'<span class="label" style="font-size:14px">{row}</span>', width="content")
            name = st.selectbox("Box", allowed, key=f"{key}_box_{gate}", label_visibility="collapsed")
            on = [st.selectbox(f"{role} {peg + 1}", shapes, index=min(peg, len(shapes) - 1), key=f"{key}_on_{gate}_{name}_{peg}",
                               format_func=lambda shape, role=role: f"{role}: {shape}", label_visibility="collapsed")
                  for peg, role in enumerate(ROLES[name])]
            if st.button("", icon=":material/delete:", key=f"{key}_delete_{gate}", type="tertiary"):
                ids.remove(gate)
                st.rerun()
        if len(set(on)) < len(on):
            valid = False
        gates.append((name, on))
    if len(ids) < 8 and st.button("Add box", icon=":material/add:", key=f"{key}_add", width="stretch"):
        ids.append(max(ids, default=0) + 1)
        st.rerun()
    if not valid:
        st.html('<span class="small" style="color:var(--bad-text)">A box with two or three pegs needs different shapes on each peg.</span>')

    st.html('<span class="label">TEST RUNS</span>')
    for start in question["inputs"]:
        expected = run_gates(start, target)
        output = run_gates(start, gates) if valid else start
        match = valid and output == expected
        mark = "✓ Matches" if match else "✗ Doesn't match yet"
        st.html(f'<div class="row" style="gap:12px; flex-wrap:wrap">{picture([start, output], across=True)}'
                f'<span class="strong" style="font-weight:700; color:{"#22C55E" if match else "var(--muted)"}">{mark}</span></div>')
    return gates, valid


# ================= the page =================

top_bar(quiz["title"], f"QUESTION {index + 1} OF {total}", index, total, f"{bolt(18)} {quiz['xp']} XP")

ask_side, build_side = st.columns([1, 1.2], gap="large")
with ask_side:
    with st.container(key="question"):
        chip, ink, paint = CHIPS[question["type"]]
        st.html(f'''
        <div class="stack" style="gap:12px">
            <span class="label" style="align-self:flex-start; color:{ink}; background:{paint}; padding:5px 10px; border-radius:8px">{chip}</span>
            <span style="font-size:24px; line-height:1.3; color:#18181B"><b>Question {index + 1}:</b> {question["question"]}</span>
        </div>''')
        if question["type"] == "circuit":
            st.html('<span style="color:#3F3F46">Your circuit has to do this:</span>')
            for start in question["inputs"]:
                st.html(picture([start, "?", run_gates(start, target)], across=True))
        else:
            show_picture(question["picture"])
        if st.session_state.get(f"{key}_hint") and question["hint"]:
            st.html(f'<span style="color:#5B21B6; font-weight:600">Hint: {question["hint"]}</span>')
        st.html(f'<span style="color:#52525B; font-size:14px; border-top:1px solid rgba(24,24,27,0.12); '
                f'padding-top:14px; display:block">{TIPS[question["type"]]}</span>')

with build_side:
    with st.container(key="builder"):
        st.html('<span class="strong" style="font-size:20px; font-weight:700">'
                + ("Pick one" if question["type"] == "pick" else "Answer builder") + '</span>')
        if question["type"] == "pick":
            clicked = options(question["options"], checked["picked"] if checked else None, question["answer"], key=key,
                              locked=checked is not None)
            if clicked is not None:
                check(clicked == question["answer"], question["options"][clicked], picked=clicked)
        elif question["type"] == "state":
            built = state_builder()
        else:
            gates, valid = circuit_builder()

# ---------------- bottom ----------------
st.html('<div style="height:18px"></div>')
if checked:
    correct = checked["correct"]
    with feedback(correct, f"Correct! +{course.QUIZ_XP} XP" if correct else "Not quite", question["why"]):
        if st.button("Finish" if index + 1 == total else "Continue", type="primary",
                     icon=":material/arrow_forward:", icon_position="right"):
            next_question()
else:
    with st.container(horizontal=True, vertical_alignment="center"):
        if question["hint"] and st.button("Hint", icon=":material/lightbulb:"):
            st.session_state[f"{key}_hint"] = True
            st.rerun()
        if st.button("Skip", type="tertiary"):
            check(False, "Skipped")
        st.space("stretch")
        if question["type"] == "state" and st.button("Check answer", type="primary"):
            check(bool(built.entries) and built == question["answer"], words(built))
        if question["type"] == "circuit" and st.button("Check answer", type="primary"):
            outputs_match = valid and all(run_gates(start, gates) == run_gates(start, target) for start in question["inputs"])
            check(outputs_match, ", ".join(f"{name} {' '.join(on)}" for name, on in gates) or "no boxes")