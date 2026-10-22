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

# ---------- the flip game: H, maybe NOT, H always gives white ----------
flipped = white.copy().H("circle").NOT("circle").H("circle")
left_alone = white.copy().H("circle").H("circle")
print("Flip game:    ", flipped == white and left_alone == white)

# ---------- measuring only some qubits ----------
three = make("circle square", "ww", "wb", "bb")
results = {seen: (round(chance, 2), state) for seen, chance, state in three.outcomes(["square"])}
print("Measure some: ", results[(0,)] == (0.33, make("circle square", "ww"))
      and results[(1,)] == (0.67, make("circle square", "wb", "bb")))

# ---------- game 3: find the gem, in every locker ----------
def flip_around(state):
    return (state.H("circle").H("square").NOT("circle").NOT("square").CZ("circle", "square")
                 .NOT("circle").NOT("square").H("circle").H("square"))

markers = {"ww": lambda s: s.NOT("circle").NOT("square").CZ("circle", "square").NOT("circle").NOT("square"),
           "wb": lambda s: s.NOT("circle").CZ("circle", "square").NOT("circle"),
           "bw": lambda s: s.NOT("square").CZ("circle", "square").NOT("square"),
           "bb": lambda s: s.CZ("circle", "square")}
lockers = make("circle square", "ww").H("circle").H("square")
print("Game 3 gem:   ", all(flip_around(mark(lockers.copy())) == make("circle square", code) for code, mark in markers.items()))

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
code = to_qasm("Bell pair", ["circle", "square"], [1, 0], [("H", ["circle"]), ("CNOT", ["circle", "square"]),
                                                          ("SWAP", ["circle", "square"])])
print("QASM:         ", code.startswith("OPENQASM 2.0;") and "x q[0];" in code and "cx q[0],q[1];" in code
      and "swap" not in code and "measure q[0] -> c[1];" in code)