# Turns a Qubi circuit into OpenQASM 2.0 code you can paste into IBM Quantum Composer.

IBM_NAMES = {"NOT": "x", "H": "h", "Z": "z", "CNOT": "cx", "CZ": "cz", "SWAP": "swap", "TOFFOLI": "ccx"}


def to_qasm(shapes, starts, steps):
    """shapes: ["circle", "square"]   starts: [0, 1] (0 = white, 1 = black)
    steps: [("H", ["circle"]), ("CNOT", ["circle", "square"])]"""
    count = len(shapes)
    lines = ["OPENQASM 2.0;", 'include "qelib1.inc";', f"qreg q[{count}];", f"creg c[{count}];"]

    for spot, color in enumerate(starts):              # IBM starts every qubit white,
        if color == 1:                                  # so black shapes need a NOT first
            lines.append(f"x q[{spot}];")

    for name, on in steps:
        wires = ",".join(f"q[{shapes.index(shape)}]" for shape in on)
        lines.append(f"{IBM_NAMES[name]} {wires};")

    lines.append("measure q -> c;")
    return "\n".join(lines)