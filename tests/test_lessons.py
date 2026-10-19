# Checks every lesson: answers point at real options, and every "build the state" answer
# matches what the engine really gives. Run from the Qubi folder:  python -m tests.test_lessons

from engine.qubits import State, apply
from lessons import LESSONS

# which shapes each box goes on in quiz pictures
PEGS = {1: "circle", 2: "circle square", 3: "circle square triangle"}
ON = {"H": 1, "NOT": 1, "Z": 1, "CNOT": 2, "CZ": 2, "SWAP": 2, "TOFFOLI": 3}

problems = []
for number, lesson in enumerate(LESSONS, start=1):
    for step in lesson["steps"]:
        ask = step["ask"]
        if ask and not 0 <= ask["answer"] < len(ask["options"]):
            problems.append(f"Lesson {number}: check-in answer out of range")

    for question in lesson["quiz"]:
        kind = question["type"]
        if kind == "pick" and not 0 <= question["answer"] < len(question["options"]):
            problems.append(f"Lesson {number}: quiz answer out of range")

        if kind == "state" and question["picture"] and isinstance(question["picture"][0], State):
            start, *boxes, last = question["picture"]
            if last == "ANSWER" and all(box in ON for box in boxes) and isinstance(start.entries, dict):
                state = start
                for box in boxes:
                    state = apply(state, f"{box} {' '.join(start.shapes[:ON[box]])}")
                if not state == question["answer"]:
                    problems.append(f"Lesson {number}: wrong answer for '{question['question']}'")

        if kind == "circuit":
            for state in question["inputs"]:
                for gate in question["target"]:
                    state = apply(state, gate)               # the target circuit must run without errors
            if not question["allowed"]:
                problems.append(f"Lesson {number}: no boxes allowed")

print(f"Checked {len(LESSONS)} lessons.")
print("Problems:", problems if problems else "none")