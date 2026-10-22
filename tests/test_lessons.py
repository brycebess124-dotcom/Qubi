# Checks every lesson: answers point at real options, every "build the state" answer matches what the engine
# really gives, and every "build the circuit" question can be solved with the gates it allows.
# Run from the Qubi folder:  python -m tests.test_lessons

import itertools
from engine.qubits import State, apply, SHAPES
from lessons import LESSONS

GATES = {"NOT": 1, "H": 1, "Z": 1, "CNOT": 2, "CZ": 2, "SWAP": 2, "TOFFOLI": 3}


def tidied(state):
    """A tidy copy of a state, even a messy one written with untidy()."""
    entries = {}
    for colors, sign in (state.entries.items() if isinstance(state.entries, dict) else state.entries):
        entries[colors] = entries.get(colors, 0) + sign
    return State(state.shapes, entries).tidy()


def join(states):
    """Pairs every entry with every entry, like joining separate qubits into one cloud."""
    shapes, entries = [], {(): 1}
    for state in states:
        shapes += state.shapes
        entries = {a + b: x * y for a, x in entries.items() for b, y in tidied(state).entries.items()}
    return State(shapes, entries).tidy()


def is_gate(item):
    name, *on = item.split()
    return name in GATES and len(on) == GATES[name] and all(shape in SHAPES for shape in on)


def worked_out(picture):
    """What a question's picture leads to, or None when it can't be worked out from the picture alone
    (game boxes and measurements)."""
    if isinstance(picture, dict) and all(isinstance(item, State) for item in picture["together"]):
        return join(picture["together"])
    if not isinstance(picture, list) or not isinstance(picture[0], State):
        return None
    state, *rest = picture
    state = tidied(state)
    for item in rest:
        if item == "ANSWER":
            break
        if not (isinstance(item, str) and is_gate(item)):
            return None
        state = apply(state, item)
    return state


def run_all(state, gates):
    for gate in gates:
        state = apply(state, gate)
    return state


def fewest_gates(question, most=3):
    """The smallest circuit size (up to `most`) that answers a circuit question, or None if none does."""
    shapes = question["inputs"][0].shapes
    moves = [" ".join([name, *on]) for name in question["allowed"] if GATES[name] <= len(shapes)
             for on in itertools.permutations(shapes, GATES[name])]
    goals = [run_all(state, question["target"]) for state in question["inputs"]]
    for size in range(most + 1):
        for circuit in itertools.product(moves, repeat=size):
            if all(run_all(state, circuit) == goal for state, goal in zip(question["inputs"], goals)):
                return size
    return None


problems = []
questions = 0
for number, lesson in enumerate(LESSONS, start=1):
    for step in lesson["steps"]:
        ask = step["ask"]
        if ask and not 0 <= ask["answer"] < len(ask["options"]):
            problems.append(f"Lesson {number}: check-in answer out of range")

    for question in lesson["quiz"]:
        questions += 1
        kind = question["type"]
        if kind == "pick" and not 0 <= question["answer"] < len(question["options"]):
            problems.append(f"Lesson {number}: quiz answer out of range")
        if kind == "state":
            result = worked_out(question["picture"])
            if result is not None and not result == question["answer"]:
                problems.append(f"Lesson {number}: wrong answer for '{question['question']}'")
        if kind == "circuit":
            size = fewest_gates(question)
            if size is None:
                problems.append(f"Lesson {number}: '{question['question']}' can't be built from {question['allowed']}")
            elif size == 0:
                problems.append(f"Lesson {number}: '{question['question']}' is already solved with no gates")

print(f"Checked {len(LESSONS)} lessons and {questions} quiz questions.")
print("Problems:", problems if problems else "none")