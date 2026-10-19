# Checks that the quantum engine and every trick in the lessons work.
# Run from the Qubi folder:  python -m tests.test_qubits     (every line should say True)

from engine.qubits import State, make, apply
from engine.qasm import to_qasm

white = make("circle", "w")
black = make("circle", "b")

# ---------- the basic boxes ----------
print("NOT:          ", white.copy().NOT("circle") == black)
print("H on white:   ", white.copy().H("circle") == make("circle", "w", "b"))
print("H on black:   ", black.copy().H("circle") == make("circle", "w", "-b"))
print("H twice:      ", white.copy().H("circle").H("circle") == white)
print("H Z H = NOT:  ", make("circle", "w", "b").H("circle").Z("circle").H("circle") == make("circle", "w", "b").NOT("circle"))

# ---------- entanglement ----------
pair = make("circle square", "ww").H("circle").CNOT("circle", "square")
print("Entanglement: ", pair == make("circle square", "ww", "bb"))
print("Is entangled: ", pair.is_entangled() == True)
print("Not entangled:", make("circle square", "ww").H("circle").H("square").is_entangled() == False)
print("Measure:      ", pair.copy().measure(["circle"])["circle"] in [0, 1])


def flip_if_black(colors):
    if colors[0] == 1:
        return [0]
    return colors


print("Custom box:   ", black.copy().box(flip_if_black) == white)

# ---------- game 1: rigged or fair ----------
machines = {"rigged": [lambda c: [c[0], c[1]], lambda c: [c[0], 1 - c[1]]],
            "fair":   [lambda c: [c[0], c[1] ^ c[0]], lambda c: [c[0], c[1] ^ (1 - c[0])]]}
for kind, rules in machines.items():
    for rule in rules:
        result = make("circle square", "wb").H("circle").H("square").box(rule).H("circle")
        circle_color = {colors[0] for colors in result.entries}
        print(f"Game 1 {kind}:".ljust(15), circle_color == ({0} if kind == "rigged" else {1}))

# ---------- game 2: the silent alarm ----------
no_alarm = make("circle square", "ww").H("circle").H("circle")
alarm = make("circle square", "ww").H("circle").CNOT("circle", "square").H("circle")
print("Game 2 empty: ", no_alarm == make("circle square", "ww"))
print("Game 2 alarm: ", alarm.chances()[(1, 0)] == 0.25)

# ---------- game 3: find the gem ----------
def flip_around(state):
    return (state.H("circle").H("square").NOT("circle").NOT("square").CZ("circle", "square")
                 .NOT("circle").NOT("square").H("circle").H("square"))

gem = make("circle square", "ww").H("circle").H("square").CZ("circle", "square")    # gem in the black-black locker
print("Game 3 gem:   ", flip_around(gem) == make("circle square", "bb"))

# ---------- teleportation ----------
message = make("circle", "w", "-b")
start = make("circle square triangle", "www", "wbb", "-bww", "-bbb")           # message, then a pair
sent = start.CNOT("circle", "square").H("circle")
all_good = True
for circle in (0, 1):
    for square in (0, 1):
        kept = State(sent.shapes, {c: s for c, s in sent.entries.items() if c[:2] == (circle, square)})
        if square == 1:
            kept = apply(kept, "NOT triangle")
        if circle == 1:
            kept = apply(kept, "Z triangle")
        triangle = State(["triangle"], {(c[2],): s for c, s in kept.entries.items()})
        all_good = all_good and triangle.entries == make("triangle", "w", "-b").entries
print("Teleport:     ", all_good)

# ---------- export to IBM ----------
code = to_qasm(["circle", "square"], [0, 0], [("H", ["circle"]), ("CNOT", ["circle", "square"])])
print("QASM:         ", "cx q[0],q[1];" in code)