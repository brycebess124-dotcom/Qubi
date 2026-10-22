# Qubi engine
# A state is a set of entries. Each entry = colors + a sign.
# colors: one number per shape. 0 = white, 1 = black.
# 1 entry = plain shapes. 2+ entries = a superposition (drawn as a cloud).

import math
import random

SHAPES = ["circle", "square", "triangle", "diamond", "pentagon"]


class State:

    def __init__(self, shapes, entries):
        self.shapes = list(shapes)
        self.entries = dict(entries)

    def copy(self):
        return State(self.shapes, self.entries)

    def is_superposition(self):
        return len(self.entries) > 1

    def spot(self, shape):
        """Which position in the colors belongs to this shape."""
        return self.shapes.index(shape)

    def __eq__(self, other):
        """Two states are the same if they match after tidying."""
        if not isinstance(other, State):
            return False
        return self.shapes == other.shapes and self.copy().tidy().entries == other.copy().tidy().entries

    # ---------- tidy up ----------

    def tidy(self):
        # opposites cancel
        self.entries = {colors: sign for colors, sign in self.entries.items() if sign != 0}
        if not self.entries:
            return self
        # shrink duplicates
        divisor = 0
        for sign in self.entries.values():
            divisor = math.gcd(divisor, sign)
        for colors in self.entries:
            self.entries[colors] //= divisor
        # an overall minus doesn't matter
        if self.entries[min(self.entries)] < 0:
            for colors in self.entries:
                self.entries[colors] *= -1
        return self

    # ---------- the one helper every gate uses ----------

    def run_gate(self, gate):
        """Sends each entry through the gate, adds up the results, tidies.
        gate(colors) returns a list of (new_colors, sign)."""
        new_entries = {}
        for colors, sign in self.entries.items():
            for new_colors, new_sign in gate(list(colors)):
                key = tuple(new_colors)
                new_entries[key] = new_entries.get(key, 0) + sign * new_sign
        self.entries = new_entries
        return self.tidy()

    # ---------- gates ----------

    def NOT(self, shape):
        p = self.spot(shape)
        def gate(colors):
            colors[p] = 1 - colors[p]                      # flip
            return [(colors, 1)]
        return self.run_gate(gate)

    def H(self, shape):
        p = self.spot(shape)
        def gate(colors):
            white = colors.copy(); white[p] = 0
            black = colors.copy(); black[p] = 1
            black_sign = -1 if colors[p] == 1 else 1        # black in -> minus on black
            return [(white, 1), (black, black_sign)]
        return self.run_gate(gate)

    def Z(self, shape):
        p = self.spot(shape)
        def gate(colors):
            return [(colors, -1 if colors[p] == 1 else 1)]  # minus if black
        return self.run_gate(gate)

    def CNOT(self, control, target):
        c, t = self.spot(control), self.spot(target)
        def gate(colors):
            if colors[c] == 1:
                colors[t] = 1 - colors[t]                  # flip target if control is black
            return [(colors, 1)]
        return self.run_gate(gate)

    def CZ(self, shape1, shape2):
        a, b = self.spot(shape1), self.spot(shape2)
        def gate(colors):
            both_black = colors[a] == 1 and colors[b] == 1
            return [(colors, -1 if both_black else 1)]
        return self.run_gate(gate)

    def SWAP(self, shape1, shape2):
        a, b = self.spot(shape1), self.spot(shape2)
        def gate(colors):
            colors[a], colors[b] = colors[b], colors[a]
            return [(colors, 1)]
        return self.run_gate(gate)

    def TOFFOLI(self, control1, control2, target):
        c1, c2, t = self.spot(control1), self.spot(control2), self.spot(target)
        def gate(colors):
            if colors[c1] == 1 and colors[c2] == 1:
                colors[t] = 1 - colors[t]
            return [(colors, 1)]
        return self.run_gate(gate)

    def box(self, rule):
        """Custom box for the games. rule(colors) returns the new colors."""
        def gate(colors):
            return [(rule(colors), 1)]
        return self.run_gate(gate)

    # ---------- measuring ----------

    def chances(self):
        """Chance of each entry: sign squared, out of the total."""
        total = sum(sign * sign for sign in self.entries.values())
        return {colors: sign * sign / total for colors, sign in self.entries.items()}

    def outcomes(self, shapes=None):
        """Every possible result of measuring these shapes (all if none given), as a list of
        (colors seen, chance, the state that's left). Only the entries that match what was seen are kept."""
        shapes = shapes or self.shapes
        spots = [self.spot(shape) for shape in shapes]
        chances = {}
        for colors, chance in self.chances().items():
            seen = tuple(colors[p] for p in spots)
            chances[seen] = chances.get(seen, 0) + chance
        results = []
        for seen, chance in sorted(chances.items()):
            kept = {colors: sign for colors, sign in self.entries.items() if tuple(colors[p] for p in spots) == seen}
            results.append((seen, chance, State(self.shapes, kept).tidy()))
        return results

    def measure(self, shapes=None):
        """Measures some shapes (all if none given) for real: picks one result at random, keeps only the
        entries that match it, and returns what was seen, like {"circle": 1}."""
        shapes = shapes or self.shapes
        results = self.outcomes(shapes)
        seen, _, left = random.choices(results, [chance for _, chance, _ in results])[0]
        self.entries = left.entries
        return dict(zip(shapes, seen))

    # ---------- entanglement ----------

    def is_entangled(self):
        """True if some shape can't be pulled out into its own cloud (the state can't be fully factored)."""
        for p in range(len(self.shapes)):
            pairs = {}
            for colors, sign in self.entries.items():
                others = colors[:p] + colors[p + 1:]
                pairs.setdefault(others, [0, 0])[colors[p]] += sign
            first = list(pairs.values())[0]
            for pair in pairs.values():
                if first[0] * pair[1] != first[1] * pair[0]:
                    return True
        return False


# ================= helpers for writing lessons =================

def make(shapes, *entries):
    """make("circle", "w")              -> a white circle
       make("circle square", "wb")      -> white circle, black square
       make("circle", "w", "-b")        -> a superposition: white circle | minus black circle"""
    table = {}
    for entry in entries:
        sign = -1 if entry.startswith("-") else 1
        colors = tuple(0 if letter == "w" else 1 for letter in entry.lstrip("-"))
        table[colors] = table.get(colors, 0) + sign
    return State(shapes.split(), table)


def untidy(shapes, *entries):
    """A messy superposition for pictures only: entries keep their order and can repeat or cancel,
    like before tidying."""
    state = State(shapes.split(), {})
    state.entries = [(tuple(0 if letter == "w" else 1 for letter in entry.lstrip("-")),
                      -1 if entry.startswith("-") else 1) for entry in entries]
    return state


def apply(state, gate):
    """Sends a copy of the state through one gate, like "H circle" or "CNOT circle square".
    A gate can also be a (label, function) pair for the game boxes."""
    if isinstance(gate, tuple):
        label, function = gate
        return function(state.copy())
    name, *on = gate.split()
    return getattr(state.copy(), name)(*on)


def run(state, *gates):
    """A picture of a circuit: start state, gate, result, gate, result...
    End with "measure" to show every result and its chance, or "measure square" to measure only some shapes."""
    items = [state]
    for gate in gates:
        if isinstance(gate, str) and gate.split()[0] == "measure":
            shapes = gate.split()[1:]
            items += [" ".join(["MEASURE", *shapes]), {"outcomes": state.outcomes(shapes)}]
        else:
            state = apply(state, gate)
            items += [gate[0] if isinstance(gate, tuple) else gate, state]      # "CNOT circle square" labels the wires
    return items