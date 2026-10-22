# Turns a Circuit Lab circuit into OpenQASM 2.0, the code IBM Quantum Composer reads.
# Every qubit is a shape: q[0] is the first shape, q[1] the second, and so on.

COMPOSER = "https://quantum.cloud.ibm.com/composer"

# Qubi's box names and IBM's names for the same gates
IBM_NAMES = {"NOT": "x", "H": "h", "Z": "z", "CNOT": "cx", "CZ": "cz", "TOFFOLI": "ccx"}   # SWAP is below


def to_qasm(name, shapes, starts, steps):
    """name: "Bell pair"   shapes: ["circle", "square"]   starts: [0, 1] (0 = white, 1 = black)
    steps: [("H", ["circle"]), ("CNOT", ["circle", "square"])]"""
    count = len(shapes)
    lines = ["OPENQASM 2.0;",
             'include "qelib1.inc";',
             f"// {name}, made in the Qubi Circuit Lab",
             f"qreg q[{count}];",
             f"creg c[{count}];"]

    for spot, shape in enumerate(shapes):
        lines.append(f"// q[{spot}] is the {shape}")

    # IBM starts every qubit white (0), so a shape that starts black gets a NOT (x) first
    for spot, color in enumerate(starts):
        if color == 1:
            lines.append(f"x q[{spot}];")

    # the boxes, in order
    for box, on in steps:
        spots = [f"q[{shapes.index(shape)}]" for shape in on]
        if box == "SWAP":                  # OpenQASM 2.0 has no swap gate, but 3 CNOTs do the same thing
            a, b = spots
            lines += [f"// SWAP the {on[0]} and the {on[1]}", f"cx {a},{b};", f"cx {b},{a};", f"cx {a},{b};"]
        else:
            lines.append(f"{IBM_NAMES[box]} {','.join(spots)};")

    # IBM writes results right to left (the last bit is c[0]). Measuring the first shape into the
    # last bit makes IBM's answers read left to right, in the same order as the shapes in Qubi.
    lines.append("barrier q;")
    for spot in range(count):
        lines.append(f"measure q[{spot}] -> c[{count - 1 - spot}];")
    return "\n".join(lines)


def ibm_label(colors):
    """How IBM writes a result, like "10" for (black, white)."""
    return "".join(str(color) for color in colors)