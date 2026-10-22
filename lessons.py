# Every lesson in Qubi: 7 units, one for each chapter of the course notes.
# Each lesson has steps (read, predict, try it) and a short quiz at the end.
# Edit the words freely: the pictures are worked out by the quantum engine, so they always follow the rules.
#
#   make("circle", "w")                 a white circle           ("w" = white, "b" = black)
#   make("circle", "w", "-b")           a superposition: white circle | minus black circle
#   untidy("circle", "w", "w", "-b")    a messy superposition, drawn exactly as written (for the tidying rules)
#   run(start, "H circle", ...)         start → gate → result → ...  ("measure" shows every result and its chance)
#   results(state, "square")            the results of measuring just some shapes, with their chances
#   table("NOT circle", a, b)           a rule table: each input → gate → output
#   same(a, b)                          a = b
#   together(a, b)                      side by side, no arrows
#   diagram("circle", "w", ["H circle"])  a circuit diagram, drawn like the Circuit Lab and IBM draw them
#   "ANSWER"                            the dashed ? box in a question

from engine.qubits import make, untidy, run, apply


# ================= helpers to write lessons =================

def lesson(unit, title, steps, quiz):
    return {"unit": unit, "title": title, "steps": steps, "quiz": quiz}


def ask(question, options, answer, why):
    """A multiple choice question. answer = the number of the right option (first = 0)."""
    return {"question": question, "options": options, "answer": answer, "why": why}


def measure(states, shapes=None, labels=None, times=10, button="Measure 10 times"):
    """A button that measures a state for real. For games, states is {name: state} and one is picked at random."""
    return {"states": states if isinstance(states, dict) else {"": states}, "shapes": shapes,
            "labels": labels or {}, "times": times, "button": button}


def learn(title, text, picture=None, note="", try_it=None):
    return {"kind": "LEARN", "title": title, "text": text, "picture": picture, "note": note, "ask": None, "try_it": try_it}


def predict(title, text, question, picture=None, note="", try_it=None):
    return {"kind": "PREDICT", "title": title, "text": text, "picture": picture, "note": note, "ask": question, "try_it": try_it}


def play(title, text, picture=None, note="", try_it=None, question=None):
    return {"kind": "GAME", "title": title, "text": text, "picture": picture, "note": note, "ask": question, "try_it": try_it}


def pick(question, options, answer, why, picture=None, hint=""):
    return {"type": "pick", "question": question, "options": options, "answer": answer,
            "why": why, "picture": picture, "hint": hint}


def build_state(question, picture, answer, why, hint=""):
    return {"type": "state", "question": question, "picture": picture, "answer": answer, "why": why, "hint": hint}


def build_circuit(question, allowed, target, inputs, why, hint=""):
    """The learner builds a circuit that does the same thing as `target` to every state in `inputs`."""
    return {"type": "circuit", "question": question, "allowed": allowed, "target": target,
            "inputs": inputs, "why": why, "hint": hint}


def together(*items):
    """A picture of things side by side, with no arrows between them."""
    return {"together": list(items)}


def same(*items):
    """Things that are equal, with = signs between them."""
    parts = []
    for item in items:
        parts += [item, "="]
    return together(*parts[:-1])


def table(gates, *inputs):
    """A rule table worked out by the engine: each input, the gate (or gates), and what comes out."""
    gates = [gates] if isinstance(gates, (str, tuple)) else gates
    rows = []
    for state in inputs:
        row = [state]
        for gate in gates:
            state = apply(state, gate)
            row.append(gate[0] if isinstance(gate, tuple) else gate)
        rows.append(row + [state])
    return {"rows": rows}


def rows(*lines):
    """A rule table written by hand, for outputs the engine would tidy away (like a lone minus sign)."""
    return {"rows": [list(line) for line in lines]}


def diagram(shapes, starts, gates):
    """A circuit diagram: one line per qubit, time going left to right."""
    steps = [(gate.split()[0], gate.split()[1:]) for gate in gates]
    return {"circuit": (shapes.split(), [0 if color == "w" else 1 for color in starts], steps)}


def results(state, shapes=None):
    """Every result of measuring some shapes (all if none given), with its chance and what's left."""
    return {"outcomes": state.outcomes(shapes.split() if shapes else None)}


def after(state, *gates):
    """The state after some gates."""
    for gate in gates:
        state = apply(state, gate)
    return state


# ================= states used a lot =================

white = make("circle", "w")
black = make("circle", "b")
plus = make("circle", "w", "b")                  # what H makes from a white circle
minus = make("circle", "w", "-b")                # what H makes from a black circle
ww, wb, bw, bb = (make("circle square", pair) for pair in ("ww", "wb", "bw", "bb"))
square_plus = make("square", "w", "b")
three = make("circle square", "ww", "wb", "bb")
all_four = make("circle square", "ww", "wb", "bw", "bb")
bell = make("circle square", "ww", "bb")
TRIO = "circle square triangle"


# ================= the games =================

def machine(rule):
    """Unit 5: the carnival machine M. The circle is the button you press, the square is the light."""
    return ("M", lambda state: state.box(rule))


RIGGED_OFF = lambda c: [c[0], c[1]]                  # the light never flips
RIGGED_ON = lambda c: [c[0], 1 - c[1]]               # the light always flips
FAIR_COPY = lambda c: [c[0], c[1] ^ c[0]]            # flips only for the black button
FAIR_OPPOSITE = lambda c: [c[0], c[1] ^ (1 - c[0])]  # flips only for the white button
ready = after(wb, "H circle", "H square")            # the trick's first step


def trick(rule):
    """Unit 5: the whole quantum trick on one machine."""
    return after(ready, machine(rule), "H circle")


MARKERS = {   # Unit 6: the marker ★ puts a minus sign on the gem's locker code
    "ww": lambda s: s.NOT("circle").NOT("square").CZ("circle", "square").NOT("circle").NOT("square"),
    "wb": lambda s: s.NOT("circle").CZ("circle", "square").NOT("circle"),
    "bw": lambda s: s.NOT("square").CZ("circle", "square").NOT("square"),
    "bb": lambda s: s.CZ("circle", "square"),
}


def marker(code):
    return ("★", MARKERS[code])


def flip_around(state):
    """Unit 6: H, NOT, Control-Z, NOT, H on both qubits. The marked entry grows and the rest cancel."""
    return (state.H("circle").H("square").NOT("circle").NOT("square").CZ("circle", "square")
                 .NOT("circle").NOT("square").H("circle").H("square"))


all_lockers = after(ww, "H circle", "H square")
LOCKER_NAMES = {"ww": "white-white", "wb": "white-black", "bw": "black-white", "bb": "black-black"}

teleport_start = make(TRIO, "www", "wbb", "-bww", "-bbb")     # Ψ = white | minus black on the circle, plus a Bell pair
after_sender = after(teleport_start, "CNOT circle square", "H circle")


# ================= the lessons =================

LESSONS = [

    # ======== Unit 1 · Bits, qubits and the rules (chapter 1) ========

    lesson(1, "What is a bit?", [
        learn("Computers run on bits",
              "Phones, laptops and game consoles all do one basic thing: they store and change <b>bits</b>.\n\n"
              "A bit is the smallest piece of information there is. It has only two possible values: <b>0</b> or "
              "<b>1</b>. Think of a light switch: off is 0 and on is 1."),
        learn("Everything is bits",
              "One bit can't say much, but long strings of bits can store anything. The letter A is stored as the "
              "8 bits 01000001. A photo takes millions of bits, and a movie takes billions.\n\n"
              "Inside a computer, tiny switches called <b>transistors</b> hold the bits. Each one is either off (0) "
              "or on (1)."),
        learn("Bits as shapes",
              "In Qubi we draw each bit as a shape. The color is the value: a <b>white</b> shape means 0 and a "
              "<b>black</b> shape means 1.\n\n"
              "The shape itself (circle, square, triangle) is just a name tag that tells bits apart. A black circle "
              "simply means: the circle bit is 1.",
              picture=together(white, black), note="White circle = 0. Black circle = 1."),
        predict("Read the shapes",
                "A row of shapes is a <b>bit string</b>. Read it left to right, one shape per bit.",
                ask("Which bit string do these shapes show?", ["011", "100", "110"], 0,
                    "White circle = 0, black square = 1, black triangle = 1. Left to right, that's 011."),
                picture=[make(TRIO, "wbb")]),
        predict("Count the patterns",
                "Two bits can make four patterns: 00, 01, 10 and 11.",
                ask("How many patterns can 3 bits make?", ["6", "8", "9"], 1,
                    "Each extra bit doubles the count: 2 × 2 × 2 = 8. With 8 bits you get 256 patterns, enough for "
                    "every key on a keyboard."),
                picture=together(ww, wb, bw, bb)),
    ], [
        pick("A bit can be…", ["Only 0 or 1", "Any number from 0 to 9", "0, 1 or 2"], 0,
             "A bit has exactly two values, 0 and 1, like a switch that's off or on.", hint="Think of a light switch."),
        build_state("Build the bit string 10 using a circle and a square.", None, bw,
                    "1 is black and 0 is white, so the circle is black and the square is white.",
                    hint="Read left to right: the circle is the first bit."),
        pick("How many patterns can 4 bits make?", ["8", "16", "32"], 1,
             "2 × 2 × 2 × 2 = 16. Every extra bit doubles the count."),
    ]),

    lesson(1, "Gates change bits", [
        learn("What is a gate?",
              "Storing bits isn't enough: a computer has to change them. It does that with <b>gates</b>.\n\n"
              "A gate is a simple rule. Bits go in, and bits come out. In our pictures, bits enter a gate from the "
              "top and leave from the bottom.",
              picture=run(white, "NOT circle"), note="A white circle goes into a gate and comes out black."),
        learn("The NOT gate",
              "The simplest gate is <b>NOT</b>. It flips a bit: white becomes black and black becomes white. "
              "NOT is drawn as ⊕.\n\n"
              "A list of every possible input and its output is called a gate's <b>rule table</b>.",
              picture=table("NOT circle", white, black), note="NOT's rule table: input on the left, output on the right."),
        predict("Your turn",
                "A black circle goes into NOT.",
                ask("What comes out?", ["A black circle", "A white circle", "Nothing"], 1,
                    "NOT always flips the color, so black becomes white."),
                picture=[black, "NOT circle", "ANSWER"]),
        predict("Two in a row",
                "Gates can be chained: whatever comes out of one gate goes straight into the next.",
                ask("A white circle goes through NOT twice. What comes out?", ["A white circle", "A black circle"], 0,
                    "The first NOT makes it black and the second makes it white again. Two flips cancel out."),
                picture=[white, "NOT circle", "NOT circle", "ANSWER"]),
        learn("Every quantum gate can be undone",
              "In a quantum computer, every gate is <b>reversible</b>: some gate can always take you back to the "
              "input. NOT is its own undo.\n\n"
              "Normal computers also use gates that can't be undone. An AND gate outputs 1 only when both of its "
              "inputs are 1, so if it outputs 0, you can't tell what went in.",
              picture=run(black, "NOT circle", "NOT circle"), note="Two NOTs bring you back to the start."),
    ], [
        build_state("A black circle goes through three NOT gates. What comes out?",
                    [black, "NOT circle", "NOT circle", "NOT circle", "ANSWER"], white,
                    "Each NOT flips it: black, white, black, white.", hint="Count the flips."),
        pick("What does it mean that a gate is reversible?",
             ["Another gate can always undo it", "It works upside down", "It can only be used once"], 0,
             "A reversible gate never loses information, so you can always get the input back."),
        build_circuit("Build a circuit that flips any circle: white to black, and black to white.", ["NOT"],
                      ["NOT circle"], [white, black], "One NOT gate is all it takes.", hint="Add one gate."),
    ]),

    lesson(1, "SWAP and CNOT", [
        learn("Gates with two inputs",
              "Some gates work on two bits at once. Each symbol acts on the shape right above it.\n\n"
              "The <b>SWAP</b> gate, drawn ✕—✕, trades the colors of its two bits.",
              picture=run(bw, "SWAP circle square"), note="Black circle and white square in. White circle and black square out."),
        learn("CNOT: a NOT with a condition",
              "<b>CNOT</b> stands for controlled-NOT. One bit is the <b>control</b>, drawn as a dot (•). The other "
              "is the <b>target</b>, drawn as ⊕.\n\n"
              "If the control is black, the target flips. If the control is white, nothing happens.",
              picture=run(bw, "CNOT circle square"), note="The control circle is black, so the square flips."),
        predict("A white control",
                "Now the control is white.",
                ask("What comes out?", ["White circle, black square", "White circle, white square",
                                        "Black circle, black square"], 0,
                    "The control is white, so nothing flips. The bits come out exactly as they went in."),
                picture=[wb, "CNOT circle square", "ANSWER"]),
        learn("CNOT's rule table",
              "Two bits make four possible inputs. Here is what CNOT does to each one. Only the inputs with a black "
              "control change.",
              picture=table("CNOT circle square", ww, wb, bw, bb)),
        predict("The other direction",
                "A CNOT can point either way. In this one, the square is the control and the circle is the target.",
                ask("What comes out?", ["Black circle, black square", "White circle, black square",
                                        "Black circle, white square"], 0,
                    "The control is now the square. It's black, so the circle flips from white to black."),
                picture=[wb, "CNOT square circle", "ANSWER"]),
    ], [
        build_state("Two black bits go into this CNOT. What comes out?", [bb, "CNOT circle square", "ANSWER"], bw,
                    "The control circle is black, so the square flips from black to white."),
        pick("In a CNOT, when does the target flip?",
             ["Only when the control is black", "Only when the control is white", "Every time"], 0,
             "CNOT does a NOT on the target, but only if the control is black."),
        build_circuit("Build a circuit that copies the circle's color onto the square. The square always starts white.",
                      ["NOT", "SWAP", "CNOT"], ["CNOT circle square"], [ww, bw],
                      "A CNOT with the circle as control flips the white square only when the circle is black. "
                      "That copies the color.", hint="One two-bit gate is enough."),
    ]),

    lesson(1, "Circuits", [
        learn("Gates in a row",
              "A <b>circuit</b> is a list of gates used one after another. The bits come out of one gate and go "
              "straight into the next.\n\n"
              "Deep down, everything a computer does, from adding numbers to running a game, is done by circuits "
              "of gates.",
              picture=run(bw, "CNOT circle square", "NOT circle"), note="Follow the bits down, one gate at a time."),
        predict("Follow the bits",
                "Work through this circuit one gate at a time.",
                ask("What comes out at the bottom?", ["White circle, black square", "Black circle, white square",
                                                      "Black circle, black square"], 2,
                    "SWAP turns white-black into black-white. Then the black circle makes CNOT flip the square: "
                    "black-black."),
                picture=[wb, "SWAP circle square", "CNOT circle square", "ANSWER"]),
        predict("Does the order matter?",
                "Two circuits use the same gates in a different order: NOT on the circle then CNOT, or CNOT then "
                "NOT on the circle.",
                ask("Do they always give the same output?", ["No", "Yes"], 0,
                    "Try two white bits. NOT first makes the circle black, so CNOT flips the square: black-black. "
                    "CNOT first does nothing (the control is white), then NOT gives black-white. Different, so "
                    "order matters.")),
        learn("Same job, different circuits",
              "Two circuits do the <b>same job</b> if they give the same output for every possible input. Only "
              "the rule table matters, not how the circuit looks.\n\n"
              "For example, two NOT gates do the same job as no gate at all. In Unit 3 you'll find a surprising "
              "circuit that does the same job as SWAP."),
    ], [
        build_state("Follow the circuit. What comes out?",
                    [bw, "SWAP circle square", "CNOT circle square", "NOT circle", "ANSWER"], bb,
                    "SWAP gives white-black. The control is white, so CNOT does nothing. NOT then flips the circle: "
                    "black-black."),
        build_circuit("Build a circuit that turns two white bits into two black bits.", ["NOT", "CNOT", "SWAP"],
                      ["NOT circle", "NOT square"], [ww],
                      "Flip each bit with its own NOT. NOT on the circle followed by a CNOT works too.",
                      hint="Each bit needs to flip once."),
        pick("Two circuits do the same job when…",
             ["They give the same output for every input", "They have the same number of gates",
              "They use the same kinds of gates"], 0,
             "Only the rule table matters, not how the circuit looks."),
    ]),

    lesson(1, "Qubits and superposition", [
        learn("From bits to qubits",
              "A quantum computer uses <b>qubits</b>, short for quantum bits. A qubit can be white (0) or black "
              "(1), just like a bit.\n\n"
              "But a qubit can also be in a state that no normal bit can ever be in. That state is called a "
              "<b>superposition</b>.",
              picture=together(white, black)),
        learn("The cloud means superposition",
              "We draw a superposition as a <b>cloud</b>. Inside are its <b>entries</b>, separated by bars. Each "
              "entry is a possible result.\n\n"
              "This cloud means the circle is in a superposition of white and black. If you look at it, you'll see "
              "white or black, each with a 50% chance. Until you look, it isn't white and it isn't black.",
              picture=[plus], note="One qubit in a superposition of white and black."),
        learn("Measuring",
              "Looking at a qubit is called <b>measuring</b>. We draw it as a dark gate with a dial.\n\n"
              "Measuring ends the superposition. You get one plain result, picked at random from the entries, and "
              "the cloud is gone.",
              picture=run(plus, "measure"), note="White or black, 50% each."),
        predict("Measure it yourself",
                "Press the button to measure 10 qubits that are each in this superposition.",
                ask("What should you expect?", ["A mix of white and black, about half each", "All white", "All black"], 0,
                    "Every measurement is random, 50/50. Over many tries it comes out roughly half and half."),
                picture=[plus], try_it=measure(plus)),
        learn("Many qubits, one cloud",
              "A superposition can include several qubits. Then every entry has one shape for each qubit.\n\n"
              "This cloud holds two entries: white circle with white square, and black circle with black square. "
              "Measuring both gives white-white or black-black, 50% each. You'll never see the colors mixed.",
              picture=run(bell, "measure")),
    ], [
        pick("What does a cloud in a picture mean?",
             ["The qubits are in a superposition", "The qubits are broken", "The qubits are hidden"], 0,
             "A cloud shows a superposition. Each entry inside it is a possible result of measuring."),
        pick("What happens when you measure a qubit in a superposition?",
             ["You get one entry at random, and the superposition ends", "You see the whole cloud", "Nothing changes"], 0,
             "Measuring picks one entry at random and ends the superposition."),
        pick("You measure both qubits in this cloud. Which result is impossible?",
             ["Black circle, white square", "White circle, white square", "Black circle, black square"], 0,
             "Only entries in the cloud can show up, and black circle with white square isn't one of them.",
             picture=[bell]),
    ]),

    lesson(1, "Measuring", [
        learn("Equal entries, equal chances",
              "When no entry repeats, every entry in a cloud is equally likely. Two entries: 50% each. Three "
              "entries: about 33% each. Four entries: 25% each.",
              picture=run(three, "measure")),
        learn("Measuring just one qubit",
              "You don't have to measure every qubit. Measure only some, and you keep only the entries that agree "
              "with what you saw. Every other entry disappears.\n\n"
              "Here only the square is measured. White leaves one entry. Black leaves two, so the circle is still "
              "in a superposition.",
              picture=run(three, "measure square")),
        predict("What's left?",
                "This time you measure only the circle, and it's black.",
                ask("Which entries are left?", ["Just black circle, black square", "Both entries with a black square",
                                                "None of them"], 0,
                    "Only entries with a black circle survive. In this cloud, that's black-black."),
                picture=[three, "MEASURE circle", "ANSWER"]),
        predict("Four entries",
                "This cloud has four entries, one for each pattern.",
                ask("What's the chance of measuring white circle, black square?", ["25%", "50%", "100%"], 0,
                    "Four equally likely entries: each has a 1 in 4 chance, which is 25%."),
                picture=[all_four]),
        learn("See it for yourself",
              "Measure both qubits of this cloud 10 times. You'll only ever see its three entries. Black circle "
              "with white square never shows up, because it isn't in the cloud.",
              picture=[three], try_it=measure(three)),
    ], [
        pick("A cloud has three entries and none of them repeat. What's the chance of each?",
             ["About 33%", "50%", "25%"], 0, "Three equally likely entries: 1 out of 3, about 33%."),
        build_state("You measure only the circle and see white. What's left?", [three, "MEASURE circle", "ANSWER"],
                    make("circle square", "ww", "wb"),
                    "Keep only the entries with a white circle: white-white and white-black. They're still in a "
                    "superposition.", hint="Cross out every entry with a black circle."),
        pick("You measure only the square. What's the chance it's black?", ["About 67%", "About 33%", "50%"], 0,
             "Two of the three entries have a black square: 2 out of 3, about 67%.", picture=[three]),
    ]),

    lesson(1, "The Hadamard gate", [
        learn("A gate only qubits can use",
              "NOT, SWAP and CNOT work on normal bits too. The <b>Hadamard gate</b>, drawn as a box with an "
              "<b>H</b>, is different: it puts a qubit into a superposition. No normal computer can do that.",
              picture=run(white, "H circle"), note="White circle in. White | black out."),
        learn("H on a black qubit",
              "Put a black circle into H and you also get white and black, but now the black entry has a <b>minus "
              "sign</b> (−) in front of it.\n\n"
              "The minus sign makes this a <b>different</b> superposition from the one a white circle gives. Picture "
              "each entry as a wave: the minus sign means that wave is upside down.",
              picture=run(black, "H circle")),
        learn("H's rule table",
              "Here are both rules side by side. You'll use them in almost every lesson from here on.",
              picture=table("H circle", white, black)),
        predict("Does the minus sign show?",
                "Measuring only ever shows white or black. It can't see signs.",
                ask("You measure what comes out of H when a black circle goes in. What's the chance of black?",
                    ["50%", "0%", "100%"], 0,
                    "Minus signs don't change the chances. It's 50% white and 50% black."),
                picture=[black, "H circle", minus, "MEASURE", "ANSWER"]),
        learn("Random results, exact state",
              "Measured right after H, the results look like coin flips. But the state before you measure isn't "
              "random at all: it's an exact superposition, minus signs included.\n\n"
              "Those signs are where the quantum tricks happen. The next lessons show how.",
              picture=[minus], try_it=measure(minus)),
    ], [
        build_state("What comes out of H when a white circle goes in?", [white, "H circle", "ANSWER"], plus,
                    "H turns white into a superposition: white | black."),
        build_state("What comes out of H when a black circle goes in?", [black, "H circle", "ANSWER"], minus,
                    "H turns black into white | minus black. Don't forget the minus sign.",
                    hint="One entry needs a minus sign."),
        pick("What does the minus sign change when you measure?",
             ["Nothing: the chances stay 50/50", "Black becomes impossible", "White becomes more likely"], 0,
             "Measuring can't see signs. Signs matter when the qubit goes through more gates."),
    ]),

    lesson(1, "Tidying superpositions", [
        learn("Rules for clouds",
              "Superpositions follow a few simple rules that let you tidy a messy cloud into its simplest form.\n\n"
              "<b>Order doesn't matter.</b> You can write the entries in a cloud in any order.",
              picture=same(untidy("circle", "b", "w"), plus)),
        learn("Opposites cancel",
              "<b>Opposites cancel.</b> If two entries are exactly the same except that one has a minus sign, they "
              "cancel out. Remove both.",
              picture=same(untidy("circle square", "ww", "wb", "bb", "-wb"), bell)),
        learn("Equal repeats shrink",
              "<b>Equal repeats shrink.</b> If every entry appears the same number of times, shrink each one down "
              "to a single copy.\n\n"
              "If some entries repeat more than others, they can't shrink: that would change the chances.",
              picture=same(untidy("circle", "w", "b", "w", "b"), plus)),
        learn("One entry, no cloud",
              "<b>One entry means no cloud.</b> If only one entry is left, it's not a superposition anymore, so drop "
              "the cloud.",
              picture=same(untidy("circle", "w", "b", "-b"), white), note="Black and minus black cancel, leaving one entry."),
        learn("Moving minus signs",
              "<b>You can pull a minus sign out of a whole cloud</b>, flipping every sign inside. And an overall "
              "minus sign in front of everything doesn't matter, so you can drop it.\n\n"
              "So minus white | black is the same state as white | minus black.",
              picture=same(untidy("circle", "-w", "b"), minus)),
        predict("Tidy it up",
                "Use the rules to simplify this cloud.",
                ask("What does it simplify to?", ["A white circle", "A black circle", "White | black"], 0,
                    "Black and minus black cancel. The two whites shrink to one, and with one entry left, the cloud "
                    "goes away."),
                picture=[untidy("circle", "w", "b", "w", "-b")]),
    ], [
        build_state("Simplify this cloud as much as you can.", [untidy("circle square", "ww", "bb", "-bb", "wb")],
                    make("circle square", "ww", "wb"),
                    "Black-black and minus black-black cancel. White-white and white-black are left.",
                    hint="Find two entries that match except for a minus sign."),
        pick("When can you drop the cloud?", ["When only one entry is left", "When there are two entries",
                                              "When there's a minus sign"], 0,
             "One entry means it's a plain state, not a superposition."),
        build_state("Simplify this cloud as much as you can.", [untidy("circle", "-w", "b", "-w", "b")], minus,
                    "The repeats shrink to minus white | black. Pull a minus sign out of the whole cloud and drop it: "
                    "white | minus black.", hint="Shrink the repeats first, then look at the signs."),
    ]),

    lesson(1, "Joining and splitting clouds", [
        learn("Joining qubits into one cloud",
              "Two qubits, each in its own state, can be written as one cloud. Pair every entry of the first with "
              "every entry of the second, like FOIL in algebra.\n\n"
              "Two entries times two entries gives four entries.",
              picture=together(plus, square_plus, "=", all_four)),
        predict("Join these",
                "A white circle (no superposition) and a square in white | black.",
                ask("What single cloud do they make?", ["White-white | white-black", "White-white | black-black",
                                                         "Black-white | black-black"], 0,
                    "The circle is white in every pairing. Pair it with each square entry: white-white and "
                    "white-black."),
                picture=together(white, square_plus)),
        learn("Watch the signs",
              "When you pair entries, multiply their signs. Plus times minus gives minus. Minus times minus gives plus.",
              picture=together(minus, make("square", "w", "-b"), "=", make("circle square", "ww", "-wb", "-bw", "bb"))),
        learn("Factoring: splitting a cloud",
              "Going the other way is called <b>factoring</b>. If a qubit has the same color in every entry, you can "
              "pull it out of the cloud.",
              picture=together(make("circle square", "ww", "wb"), "=", white, square_plus)),
        learn("Clouds that won't split",
              "Some clouds can't be split into one cloud per qubit, no matter what you try. In this one, the circle "
              "and square always match, so neither can be pulled out on its own.\n\n"
              "Qubits like these are <b>entangled</b>. They'll be important later.",
              picture=[bell]),
        learn("Clouds inside clouds",
              "One last rule. Sometimes a gate turns each entry into a superposition of its own, so you get clouds "
              "inside a cloud. That's fine: pour all the entries into one big cloud, then tidy up. You'll do this "
              "in the next lesson."),
    ], [
        build_state("Join these into one cloud.", together(plus, square_plus), all_four,
                    "Pair every entry with every entry: 2 × 2 = 4 entries.",
                    hint="Each circle entry pairs with each square entry."),
        pick("Can this cloud be split into a circle cloud and a square cloud?",
             ["Yes: a black circle, and a square in white | black", "No, the qubits are entangled"], 0,
             "The circle is black in every entry, so it factors out.", picture=[make("circle square", "bw", "bb")]),
        pick("Can this cloud be split?", ["No: the qubits are entangled", "Yes"], 0,
             "The square is always the opposite color of the circle. There's no way to write it as two separate "
             "clouds.", picture=[make("circle square", "wb", "bw")]),
    ]),

    lesson(1, "Superpositions through gates", [
        learn("One entry at a time",
              "How does a superposition go through a gate? Send each entry through on its own, then put all the "
              "results into one cloud and tidy up.\n\n"
              "Here NOT turns the white entry black and the black entry white. The cloud ends up the same as before.",
              picture=run(plus, "NOT circle")),
        learn("H, then H again",
              "Now put white | black through H. The white entry becomes white | black. The black entry becomes "
              "white | minus black. Pour all four entries into one cloud.",
              picture=[plus, "H circle", untidy("circle", "w", "b", "w", "-b")], note="Before tidying up."),
        predict("Tidy it up",
                "Use the rules on that cloud.",
                ask("What does it simplify to?", ["A white circle", "A black circle", "White | black"], 0,
                    "Black and minus black cancel. The two whites shrink to one, and with one entry left, the cloud "
                    "disappears."),
                picture=[untidy("circle", "w", "b", "w", "-b")]),
        learn("More than a coin flip",
              "Here's the big idea. If a superposition were just a hidden coin flip (secretly white or secretly "
              "black), a second H would give random results again.\n\n"
              "Instead, H then H always gives back white, because the black parts cancel each other out. This "
              "canceling is called <b>interference</b>, and it's the source of a quantum computer's power.",
              picture=run(white, "H circle", "H circle"), try_it=measure(after(white, "H circle", "H circle"))),
        learn("Two qubits: entanglement",
              "Two-qubit gates work the same way: each entry goes through on its own. Here H puts the circle into a "
              "superposition, then CNOT acts on each entry.\n\n"
              "The result can't be split into separate clouds. The qubits are <b>entangled</b>: measure the circle, "
              "and you instantly know the square.",
              picture=run(ww, "H circle", "CNOT circle square")),
    ], [
        build_state("What comes out?", [minus, "H circle", "ANSWER"], black,
                    "White gives white | black. Minus black gives minus white | black. The whites cancel, and the "
                    "two blacks shrink to one: black.", hint="Send each entry through H, then tidy."),
        build_state("What comes out?", [bw, "H circle", "CNOT circle square", "ANSWER"], make("circle square", "ww", "-bb"),
                    "H on the black circle gives white-white | minus black-white. CNOT then flips the square in the "
                    "entry with the black circle.", hint="Do H first, then CNOT on each entry."),
        pick("Why does H then H always give back white?",
             ["The black entries cancel each other out", "The second H measures it", "H is broken"], 0,
             "That canceling is interference. It's what makes quantum computers more than random coin flippers."),
    ]),

    # ======== Unit 2 · Practice puzzles (chapter 2) ========

    lesson(2, "Simplify and join", [
        learn("Practice like a scientist",
              "This unit is all practice: the kinds of problems students solve with pencil and paper. Grab some "
              "scrap paper and work each one out before you answer.\n\n"
              "The rules: order doesn't matter, opposites cancel, equal repeats shrink, one entry means no cloud, "
              "and an overall minus sign doesn't matter."),
        predict("Simplify #1",
                "Use the rules.",
                ask("What does this cloud simplify to?", ["White-white | black-black", "Just white-white",
                                                         "It can't be simplified"], 0,
                    "White-black and minus white-black cancel. White-white and black-black are left."),
                picture=[untidy("circle square", "ww", "-wb", "wb", "bb")]),
        predict("Simplify #2",
                "Watch the signs.",
                ask("What does it simplify to?", ["White-white | minus white-black", "Just white-black",
                                                  "White-white | white-black"], 0,
                    "The repeats shrink to minus white-white | white-black. Pull out the overall minus sign: "
                    "white-white | minus white-black."),
                picture=[untidy("circle square", "wb", "-ww", "wb", "-ww")]),
        predict("Join three qubits",
                "Here are three separate qubits.",
                ask("How many entries does the joined cloud have?", ["4", "3", "8"], 0,
                    "2 × 1 × 2 = 4. The plain black square doesn't add any new entries."),
                picture=together(plus, make("square", "b"), make("triangle", "w", "-b"))),
        learn("The joined cloud",
              "Here it is. The square is black in every entry, and the minus signs come from the triangle.",
              picture=[make(TRIO, "wbw", "-wbb", "bbw", "-bbb")]),
    ], [
        build_state("Simplify as much as you can.", [untidy("circle square", "wb", "bw", "-wb", "bw")], bw,
                    "White-black cancels. Black-white appears twice, so it shrinks to one. One entry left means no "
                    "cloud."),
        build_state("Join these into one cloud.", together(minus, make("square", "b")), make("circle square", "wb", "-bb"),
                    "The square is black in every pairing: white-black, and minus black-black."),
        build_state("Join these into one cloud.", together(minus, make("square", "w", "-b")),
                    make("circle square", "ww", "-wb", "-bw", "bb"),
                    "Multiply the signs: plus-plus is plus, plus-minus is minus, minus-plus is minus, and minus-minus "
                    "is plus."),
    ]),

    lesson(2, "Factoring", [
        learn("Splitting clouds apart",
              "<b>Factoring</b> means splitting one big cloud into smaller clouds, one per qubit, when that's "
              "possible. It's joining in reverse.",
              picture=together(all_four, "=", plus, square_plus)),
        learn("The trick",
              "Look for a qubit with the same color in every entry and pull it out. Then check whether what's left "
              "splits again.",
              picture=together(make(TRIO, "wbw", "wbb"), "=", white, make("square", "b"), make("triangle", "w", "b"))),
        predict("Factor this",
                "Group the entries by the circle's color.",
                ask("What does it split into?", ["Circle: white | black. Square: white | minus black",
                                                 "It can't be split", "Circle: white. Square: black"], 0,
                    "With a white circle the square's part is white | minus black, and with a black circle it's the "
                    "same. So the square's part pulls out."),
                picture=[make("circle square", "ww", "-wb", "bw", "-bb")]),
        predict("Can it split?",
                "Same cloud, but one sign is different.",
                ask("Can this cloud be split?", ["No, the qubits are entangled", "Yes"], 0,
                    "With a white circle the square's part is white | black, but with a black circle it's white | "
                    "minus black. The square's part depends on the circle, so it can't be pulled out."),
                picture=[make("circle square", "ww", "wb", "bw", "-bb")]),
        learn("Why factoring matters",
              "If a cloud splits, each qubit has its own state and you can think about them one at a time. If it "
              "doesn't split, the qubits are entangled and must be thought about together. The games in Units 5 "
              "and 6 depend on spotting this."),
    ], [
        pick("Which qubits can be pulled out of this cloud?",
             ["The circle (always white) and the triangle (always black)", "Only the square", "None of them"], 0,
             "A qubit with the same color in every entry factors out.", picture=[make(TRIO, "wwb", "wbb")]),
        pick("Is this cloud entangled?", ["Yes", "No"], 0,
             "The square is always the opposite of the circle, so it can't be split.",
             picture=[make("circle square", "wb", "bw")]),
        pick("Factor out the black circle. What's left for the square?",
             ["White | minus black", "White | black", "A black square"], 0,
             "Every entry has a black circle, and the square's part is white | minus black.",
             picture=[make("circle square", "bw", "-bb")]),
    ]),

    lesson(2, "Measuring practice", [
        learn("Measure some, keep the rest",
              "When you measure some qubits, keep only the entries that match what you saw. The other qubits stay in "
              "whatever superposition is left.",
              picture=run(make(TRIO, "wbw", "bbw", "bwb"), "measure square")),
        predict("What's left?",
                "You measure only the square, and it's black.",
                ask("What's left?", ["Circle in white | black, with a black square and a white triangle",
                                     "Black circle, white square, black triangle", "Nothing changes"], 0,
                    "Only the two entries with a black square stay. In both, the triangle is white, and the circle is "
                    "white in one and black in the other."),
                picture=[make(TRIO, "wbw", "bbw", "bwb"), "MEASURE square", "ANSWER"]),
        predict("The chances",
                "The same cloud, before measuring.",
                ask("What's the chance the square comes out black?", ["About 67%", "About 33%", "100%"], 0,
                    "Two of the three entries have a black square: 2 out of 3."),
                picture=[make(TRIO, "wbw", "bbw", "bwb")]),
        predict("Measure two",
                "Now you measure the square and the triangle, and see black, white.",
                ask("What's the circle now?", ["Still white | black", "White", "Black"], 0,
                    "Both entries with a black square and a white triangle stay, so the circle is still white | black."),
                picture=[make(TRIO, "wbw", "bbw", "bwb"), "MEASURE square triangle", "ANSWER"]),
        learn("Try it",
              "Measure only the square 10 times. About 2 out of every 3 results should be black.",
              picture=[make(TRIO, "wbw", "bbw", "bwb")], try_it=measure(make(TRIO, "wbw", "bbw", "bwb"), shapes=["square"])),
    ], [
        build_state("You measure only the circle and see black. What's left?",
                    [make("circle square", "wb", "-bb", "bw"), "MEASURE circle", "ANSWER"], make("circle square", "bw", "-bb"),
                    "Keep the entries with a black circle: minus black-black and black-white. That's a black circle "
                    "with the square in white | minus black.", hint="Cross out the entry with a white circle."),
        pick("You measure both qubits. What's the chance of black-white?", ["25%", "50%", "0%"], 0,
             "Four equally likely entries. The minus sign doesn't change the chances.",
             picture=[make("circle square", "ww", "wb", "-bw", "bb")]),
        pick("You measure only the triangle and see black. How many entries are left?", ["3", "1", "2"], 0,
             "Three entries have a black triangle, and they all stay.", picture=[make(TRIO, "wwb", "wbw", "bwb", "bbb")]),
    ]),

    lesson(2, "Circuit puzzles", [
        learn("Two kinds of puzzles",
              "<b>Circuit output:</b> you get a circuit and an input. Work out what comes out.\n\n"
              "<b>Circuit finding:</b> you get the input and the output you want. Find a circuit that does it. "
              "There's usually more than one right answer."),
        predict("Output, with bits",
                "Follow the bits one gate at a time.",
                ask("What comes out?", ["White circle, black square, black triangle", "Black, black, black",
                                        "White, white, black"], 0,
                    "The black circle flips the square: black-black-white. The black square flips the triangle: "
                    "black-black-black. Then NOT flips the circle: white-black-black."),
                picture=[make(TRIO, "bww"), "CNOT circle square", "CNOT square triangle", "NOT circle", "ANSWER"]),
        predict("Output, with qubits",
                "Now with superpositions. Take it one gate at a time.",
                ask("How many entries does the final cloud have?", ["4", "2", "1"], 0,
                    "H and CNOT make white-white | black-black. The last H turns each entry into two, and nothing "
                    "cancels: four entries."),
                picture=[ww, "H circle", "CNOT circle square", "H circle", "ANSWER"]),
        predict("Find a circuit",
                "A circuit takes two black qubits and must output white-white | minus black-white.",
                ask("Which circuit works?", ["NOT on the square, then H on the circle", "H on the circle, then CNOT",
                                             "SWAP, then H on the square"], 0,
                    "NOT on the square gives black-white. H on the black circle then gives white-white | minus "
                    "black-white."),
                picture=[bb, "ANSWER", make("circle square", "ww", "-bw")]),
        learn("Why plain inputs are enough",
              "If two circuits do the same thing to every plain input (just white and black qubits), they also do "
              "the same thing to every superposition. That's because a superposition goes through a circuit one "
              "entry at a time."),
    ], [
        build_state("Find the output.", [bw, "SWAP circle square", "CNOT circle square", "ANSWER"], wb,
                    "SWAP gives white-black. The circle is white, so CNOT does nothing."),
        build_circuit("Find a circuit that turns two black qubits into white-white | minus black-white.",
                      ["H", "NOT", "CNOT"], ["NOT square", "H circle"], [bb],
                      "One answer: NOT on the square, then H on the circle. CNOT and then H on the circle works too.",
                      hint="First make the square white, then put the circle in a superposition."),
        pick("Two circuits do the same thing to all plain inputs. What about superpositions?",
             ["They do the same thing to those too", "They might act differently", "Superpositions can't go into circuits"], 0,
             "A superposition goes through one entry at a time, and each entry is a plain input."),
    ]),

    lesson(2, "Game: Flip or no flip?", [
        play("The game",
             "You hand a qubit to a prankster in a sealed box. The prankster secretly does one of two things, each "
             "half the time: flips it with NOT, or leaves it alone.\n\n"
             "Then you get the qubit back and must guess its color before you look. Guess right and you win the prize."),
        predict("Should you play?",
                "Say you hand over a plain white qubit.",
                ask("What's your chance of winning?", ["50%", "100%", "0%"], 0,
                    "The prankster's choice is random and hidden, so your guess is a coin flip. Not a great game, "
                    "unless you're quantum.")),
        predict("A state NOT can't change",
                "What if you hand over a superposition instead?",
                ask("Which of these stays exactly the same when it goes through NOT?",
                    ["White | black", "A white qubit", "A black qubit"], 0,
                    "NOT turns the white entry black and the black entry white. The cloud still holds white | black, "
                    "so nothing changed.")),
        learn("The winning strategy",
              "Put a white qubit through H to get white | black, and hand it over. Whatever the prankster does, the "
              "state doesn't change.\n\n"
              "When you get it back, put it through H again. H turns white | black back into plain white. Guess "
              "white, and you win every time.",
              picture=run(white, "H circle", "NOT circle", "H circle"), note="Even if the prankster uses NOT, the answer is white."),
        play("Play it",
             "Each round, the prankster secretly flips or doesn't. You use the strategy and guess white.",
             try_it=measure({"The prankster flipped it": after(white, "H circle", "NOT circle", "H circle"),
                             "The prankster left it alone": after(white, "H circle", "H circle")},
                            times=1, button="Play a round",
                            labels={(0,): "It came back white. You guessed white: you win!"})),
        predict("Why it works",
                "Think about what NOT does to white | black.",
                ask("Why does the strategy always win?", ["NOT can't change white | black", "The prankster always flips",
                                                          "H hides the flip"], 0,
                    "The prankster's NOT has no effect on white | black, so the second H always brings back white.")),
    ], [
        pick("In the winning strategy, what do you hand the prankster?",
             ["White | black (a white qubit after H)", "A white qubit", "A black qubit"], 0,
             "White | black is a state NOT can't change."),
        build_state("What comes out?", [white, "H circle", "NOT circle", "H circle", "ANSWER"], white,
                    "H makes white | black, NOT leaves it unchanged, and the second H turns it back into white."),
        pick("What if you handed over white | minus black instead?",
             ["You'd still win, but by guessing black", "You'd lose every time", "It would be random"], 0,
             "NOT turns white | minus black into minus (white | minus black), and an overall minus sign doesn't "
             "matter. H then gives black every time."),
    ]),

    # ======== Unit 3 · Real quantum computers (chapter 3) ========

    lesson(3, "Circuit diagrams", [
        learn("Real quantum computers",
              "Real quantum computers exist today, and you can try some of them online for free with IBM's "
              "<b>Quantum Composer</b>.\n\n"
              "The Composer uses <b>circuit diagrams</b>. They show exactly what our pictures show, just turned on "
              "their side."),
        learn("Lines are qubits",
              "In a circuit diagram, each horizontal line is one qubit. Time runs left to right: gates on the left "
              "happen first.\n\n"
              "This diagram is H on the circle, then a CNOT. Qubi's Circuit Lab draws circuits the same way.",
              picture=diagram("circle square", "ww", ["H circle", "CNOT circle square"])),
        learn("Every qubit starts white",
              "In the Composer, every qubit starts white (0). Need a black qubit? Put a NOT gate first.",
              picture=diagram("circle square", "ww", ["NOT circle", "H circle"]),
              note="The circle becomes black, then goes through H."),
        predict("Reading the bars",
                "The Composer shows results as bars: one bar for each possible result, as tall as its chance.",
                ask("A circuit leaves one qubit in white | black. What do the bars show?",
                    ["Two bars, each at 50%", "One bar at 100%", "Two bars, each at 25%"], 0,
                    "Two possible results, each with a 50% chance.")),
        learn("Shots and noise",
              "Each run of a circuit on real hardware is called a <b>shot</b>. The computer runs thousands of shots "
              "and counts the results.\n\n"
              "Real quantum computers make small errors, so you might get 48% and 52% instead of 50% and 50%. The "
              "Composer's simulator gives perfect results."),
        learn("Try it in Qubi",
              "Qubi's Circuit Lab works like the Composer. Build a circuit, press Measure 100×, then press Export "
              "to IBM to get code you can paste into the real Composer and run on real hardware."),
    ], [
        pick("In a circuit diagram, what does each horizontal line stand for?", ["One qubit", "One gate", "One measurement"], 0,
             "Each line is a qubit, and time goes left to right."),
        pick("How do you start a qubit black in the Composer?", ["Put a NOT gate first", "Qubits start black",
                                                                 "Measure it first"], 0,
             "Every qubit starts white, so a NOT at the start makes it black."),
        pick("Why are results from real hardware a little off?",
             ["Real quantum computers make small errors", "The rules are wrong", "Measuring is fake"], 0,
             "Today's hardware is noisy. The simulator shows the perfect answer."),
    ]),

    lesson(3, "Warm-up experiments", [
        predict("NOT",
                "Predict first, then press the button to test it.",
                ask("You put a white qubit through NOT and measure it. What do you get?",
                    ["Black, every time", "Black half the time", "White, every time"], 0,
                    "NOT flips white to black. No superposition, so no randomness."),
                picture=diagram("circle", "w", ["NOT circle", "MEASURE circle"]), try_it=measure(black)),
        predict("H",
                "Same idea, different gate.",
                ask("You put a white qubit through H and measure it. What do you get?",
                    ["White or black, 50% each", "Black, every time", "White, every time"], 0,
                    "H makes white | black, so each result has a 50% chance."),
                picture=diagram("circle", "w", ["H circle", "MEASURE circle"]), try_it=measure(plus)),
        predict("H twice",
                "Two H gates in a row.",
                ask("What do you get?", ["White, every time", "White or black, 50% each", "Black, every time"], 0,
                    "The black parts cancel out (interference), so you get white every time."),
                picture=diagram("circle", "w", ["H circle", "H circle", "MEASURE circle"]),
                try_it=measure(after(white, "H circle", "H circle"))),
        predict("H on a black qubit",
                "Start black (NOT first), then use H.",
                ask("What do you get?", ["White or black, 50% each", "Black, every time", "White, every time"], 0,
                    "H gives white | minus black. Measuring can't see the minus sign, so it's 50/50."),
                picture=diagram("circle", "w", ["NOT circle", "H circle", "MEASURE circle"]), try_it=measure(minus)),
        learn("CNOT on every input",
              "On the Composer you'd test CNOT by trying all four inputs, using NOT gates to make the black ones. "
              "The results match the rule table from Unit 1.",
              picture=table("CNOT circle square", ww, wb, bw, bb)),
    ], [
        pick("NOT, then H, then H on a white qubit. What do you measure?",
             ["Black, every time", "White, every time", "White or black, 50% each"], 0,
             "NOT makes it black. H then H gives back whatever went in: black."),
        pick("H, then NOT, then H on a white qubit. What do you measure?",
             ["White, every time", "Black, every time", "White or black, 50% each"], 0,
             "H makes white | black, NOT can't change it, and the second H gives white."),
        build_circuit("Starting from a white qubit, make white | minus black.", ["H", "NOT"], ["NOT circle", "H circle"],
                      [white], "NOT makes the qubit black, and H turns black into white | minus black.",
                      hint="Which input does H turn into white | minus black?"),
    ]),

    lesson(3, "Entanglement and a SWAP trick", [
        learn("The entangling circuit",
              "Here's a circuit worth running on real hardware: H on the circle, then CNOT. Work it out before you "
              "test it.",
              picture=run(ww, "H circle", "CNOT circle square")),
        predict("What will you measure?",
                "Measure both qubits.",
                ask("Which results can you get?", ["White-white or black-black", "Any of the four", "Only white-white"], 0,
                    "The cloud has two entries, white-white and black-black, so those are the only possible results, "
                    "50% each."),
                picture=[bell, "MEASURE", "ANSWER"], try_it=measure(bell)),
        learn("Always matching",
              "The two qubits always match, even though each one on its own is random. This cloud can't be split, so "
              "the qubits are <b>entangled</b>.\n\n"
              "On real hardware you'll see the same thing, plus a few mismatches caused by noise."),
        learn("Three CNOTs",
              "Now a strange-looking circuit: three CNOTs, with the middle one pointing the other way. What could it do?",
              picture=diagram("circle square", "ww", ["CNOT circle square", "CNOT square circle", "CNOT circle square"])),
        predict("Find out",
                "Follow a black circle and a white square through it.",
                ask("What comes out?", ["White circle, black square", "Black circle, white square",
                                        "Black circle, black square"], 0,
                    "Black-white becomes black-black, then white-black, then stays white-black. The colors swapped! "
                    "Three CNOTs do the same job as one SWAP."),
                picture=[bw, "CNOT circle square", "CNOT square circle", "CNOT circle square", "ANSWER"]),
    ], [
        pick("After H and CNOT on two white qubits, you measure the circle and get black. What is the square?",
             ["Black, for sure", "White, for sure", "White or black, 50% each"], 0,
             "Only the black-black entry has a black circle, so the square must be black too."),
        build_circuit("Build a SWAP using only CNOT gates.", ["CNOT"], ["SWAP circle square"], [ww, wb, bw, bb],
                      "Three CNOTs: circle to square, square to circle, then circle to square again.",
                      hint="You need three, and the middle one points the other way."),
        pick("You add a SWAP after the three CNOTs. What does the whole circuit do?",
             ["Nothing: every input comes out unchanged", "It becomes a CNOT", "It entangles the qubits"], 0,
             "Three CNOTs make a SWAP, and two SWAPs undo each other."),
    ]),

    # ======== Unit 4 · Z, Control-Z and Toffoli (chapter 4) ========

    lesson(4, "The Z gate", [
        learn("A gate that adds minus signs",
              "The <b>Z gate</b> leaves a white qubit alone and puts a minus sign in front of a black qubit.\n\n"
              "On a plain qubit that minus sign changes nothing, because an overall minus sign doesn't matter. Z "
              "matters when the qubit is in a superposition.",
              picture=rows([white, "Z circle", white], [black, "Z circle", untidy("circle", "-b")])),
        learn("Z on a superposition",
              "In a superposition, Z flips the sign of the black entry only. White | black becomes white | minus "
              "black, which is a different state.",
              picture=run(plus, "Z circle")),
        predict("Make Z from H and NOT",
                "Z isn't really new. You can build it from gates you already know.",
                ask("Which circuit does the same job as Z?", ["H, then NOT, then H", "NOT, then H", "H, then H"], 0,
                    "H, NOT, H turns white | black into white | minus black, just like Z, and it matches Z on every "
                    "input."),
                picture=run(plus, "H circle", "NOT circle", "H circle")),
        predict("Can you see a Z?",
                "You get two qubits: one in white | black and one in white | minus black.",
                ask("Can measuring tell them apart?", ["No: both give white or black, 50% each",
                                                       "Yes: the minus sign shows up"], 0,
                    "Measuring can't see signs. To tell them apart, put them through H first: one comes out white "
                    "and the other black.")),
        learn("Why minus signs matter",
              "Minus signs decide which entries cancel later. That canceling is how quantum algorithms find answers, "
              "and Z lets you put a minus sign exactly where you want it.",
              picture=run(plus, "Z circle", "H circle"), note="Z, then H: black every time."),
    ], [
        build_state("What comes out?", [plus, "Z circle", "ANSWER"], minus, "Z puts a minus sign on the black entry."),
        build_state("What comes out?", [minus, "Z circle", "ANSWER"], plus,
                    "Z flips the black entry's sign again: minus becomes plus."),
        build_circuit("Build a Z gate using only H and NOT.", ["H", "NOT"], ["Z circle"], [white, black, plus],
                      "H, NOT, H does the same job as Z.", hint="Three gates, and the middle one is NOT."),
    ]),

    lesson(4, "Control-Z", [
        learn("Z with a control",
              "Like NOT, Z has a controlled version: <b>Control-Z</b>, or CZ. It puts a minus sign on an entry only "
              "when both qubits are black.",
              picture=rows([ww, "CZ circle square", ww], [wb, "CZ circle square", wb], [bw, "CZ circle square", bw],
                           [bb, "CZ circle square", untidy("circle square", "-bb")])),
        learn("CZ on a superposition",
              "Here CZ acts on a cloud holding all four patterns. Only the black-black entry gets a minus sign.",
              picture=run(all_four, "CZ circle square")),
        predict("CZ twice",
                "Use CZ two times in a row.",
                ask("What happens?", ["Nothing: the second minus sign undoes the first", "The minus sign doubles",
                                      "Both qubits flip"], 0,
                    "Minus times minus is plus, so two CZs do nothing at all.")),
        predict("Which one is the control?",
                "In CZ's symbol, one end is a dot and the other is a Z.",
                ask("If you swap which qubit is the control, does CZ change?",
                    ["No: it only cares whether both are black", "Yes"], 0,
                    "CZ adds a minus sign when both qubits are black, so it treats them exactly the same. Control and "
                    "target are interchangeable.")),
        learn("CZ in disguise",
              "Put an H on the square before and after a CZ. The result does exactly the same job as a CNOT with the "
              "circle as control.",
              picture=run(bw, "H square", "CZ circle square", "H square"),
              note="Black-white comes out black-black, just like with CNOT."),
    ], [
        build_state("What comes out?", [make("circle square", "wb", "bb"), "CZ circle square", "ANSWER"],
                    make("circle square", "wb", "-bb"), "Only the black-black entry gets a minus sign."),
        build_circuit("Build a CNOT (circle controls the square) using H and CZ.", ["H", "CZ"], ["CNOT circle square"],
                      [ww, wb, bw, bb], "H on the square, CZ, then H on the square again.",
                      hint="The H gates go on the target."),
        pick("Which of these gates undo themselves?", ["CZ, CNOT, H and NOT", "Only NOT", "None of them"], 0,
             "Use any of these twice in a row and you get back what you started with."),
    ]),

    lesson(4, "The Toffoli gate", [
        learn("Two controls",
              "The <b>Toffoli</b> gate works on three qubits. It has two controls (two dots) and one target (⊕). "
              "The target flips only when both controls are black.",
              picture=run(make(TRIO, "bbw"), "TOFFOLI circle square triangle")),
        predict("One black control",
                "Only the circle is black this time.",
                ask("What happens to the triangle?", ["Nothing", "It flips"], 0,
                    "Both controls must be black. The square is white, so nothing flips."),
                picture=[make(TRIO, "bww"), "TOFFOLI circle square triangle", "ANSWER"]),
        predict("Toffoli twice",
                "Use Toffoli two times in a row.",
                ask("What does the pair do?", ["Nothing: the second undoes the first", "Flips the triangle twice as often",
                                               "Swaps the controls"], 0,
                    "If the target flipped once, the second Toffoli flips it back. Toffoli is its own undo, like NOT "
                    "and CNOT.")),
        learn("Fixing a broken CNOT",
              "Say your CNOT is broken, but you have a Toffoli. Make one control a helper qubit that's always black. "
              "Now the target flips exactly when the other control is black. That's a CNOT!",
              picture=table("TOFFOLI circle square triangle", make(TRIO, "wbw"), make(TRIO, "bbw")),
              note="The square is the helper, always black."),
        learn("Bigger and bigger",
              "You can imagine gates with three, four or more controls: the target flips only when every control "
              "is black.\n\n"
              "Toffoli is also how a quantum computer can do normal logic. With a white target, the target ends up "
              "black only when both inputs are black. That's an AND gate, made reversible."),
    ], [
        build_state("What comes out?", [make(TRIO, "bbb"), "TOFFOLI circle square triangle", "ANSWER"], make(TRIO, "bbw"),
                    "Both controls are black, so the black triangle flips to white."),
        pick("When does Toffoli flip its target?",
             ["Only when both controls are black", "When either control is black", "Every time"], 0,
             "It needs both controls to be black."),
        build_circuit("Make the triangle turn black only when the circle and square are both black. The triangle starts white.",
                      ["TOFFOLI", "CNOT", "NOT"], ["TOFFOLI circle square triangle"],
                      [make(TRIO, colors) for colors in ("www", "wbw", "bww", "bbw")],
                      "One Toffoli does it. This is the AND gate.", hint="One three-qubit gate."),
    ]),

    # ======== Unit 5 · Game: Rigged or fair? (chapter 5) ========

    lesson(5, "The carnival machine", [
        play("The game",
             "A carnival machine has a white button and a black button. Press a button, and a light either flips or "
             "doesn't.\n\n"
             "A <b>rigged</b> machine does the same thing for both buttons. A <b>fair</b> machine does something "
             "different for each button. Your job: find out which kind it is."),
        learn("The machine as a gate",
              "We can treat the machine as a two-qubit gate, M. The circle is the button you press. The square is "
              "the light: M may flip it. M never changes the circle.\n\n"
              "Here's the rule table of one fair machine. It flips the light only for the black button.",
              picture=table(machine(FAIR_COPY), ww, wb, bw, bb)),
        predict("Rigged or fair?",
                "Here's another machine's rule table.",
                ask("What kind of machine is it?", ["Rigged: it does the same thing for both buttons",
                                                    "Fair: it does something different for each button"], 0,
                    "It flips the light for the white button and for the black button. Same thing both times: rigged."),
                picture=table(machine(RIGGED_ON), ww, bw)),
        predict("The normal way",
                "You can press buttons and watch the light.",
                ask("How many presses do you need to be sure?", ["2", "1", "4"], 0,
                    "One press only tells you about one button. You have to try both and compare.")),
        learn("The question to ask",
              "Notice what you actually want to know: same for both buttons, or different? You don't care which "
              "button does what. Quantum computers are very good at questions like that. In the next lesson, one "
              "press will be enough."),
    ], [
        pick("A machine flips the light only for the white button. Rigged or fair?", ["Fair", "Rigged"], 0,
             "It does something different for each button, so it's fair."),
        build_state("This fair machine flips the light only for the black button. What comes out?",
                    [bw, "M", "ANSWER"], after(bw, machine(FAIR_COPY)),
                    "The black button flips the light, so the square goes from white to black."),
        pick("Without quantum tricks, how many presses do you need?", ["2", "1", "3"], 0,
             "You have to test both buttons."),
    ]),

    lesson(5, "The quantum trick", [
        learn("Step 1: get ready",
              "Start with a white circle and a black square, and put both through H. The circle becomes white | "
              "black, ready to press both buttons at once. The square becomes white | minus black.",
              picture=run(wb, "H circle", "H square")),
        learn("Step 2: use the machine once",
              "Send that into a fair machine that flips the light for the black button. In the entries with a black "
              "circle, the square's white | minus black flips into minus (white | minus black).\n\n"
              "The minus sign jumps from the square onto the circle's black entry!",
              picture=run(ready, machine(FAIR_COPY))),
        predict("Factor it",
                "Pull the square out of this cloud.",
                ask("What is the circle's part?", ["White | minus black", "White | black", "Just black"], 0,
                    "Every entry has the square in white | minus black. What's left for the circle is white | minus "
                    "black: the machine's mark."),
                picture=[after(ready, machine(FAIR_COPY))]),
        learn("Rigged machines leave no mark",
              "With a rigged machine, the circle stays white | black. At most, the whole state picks up an overall "
              "minus sign, and that doesn't matter.",
              picture=run(ready, machine(RIGGED_ON))),
        predict("Step 3: read the answer",
                "Put the circle through H one more time.",
                ask("For a fair machine the circle is white | minus black. What does H turn it into?",
                    ["Black", "White", "White or black at random"], 0,
                    "H turns white | minus black into black, and white | black into white. So black means fair, and "
                    "white means rigged.")),
    ], [
        build_state("What comes out?", [wb, "H circle", "H square", "ANSWER"], ready,
                    "The circle becomes white | black and the square white | minus black. Joined into one cloud, "
                    "that's four entries.", hint="Do each H, then pair up the entries and multiply the signs."),
        pick("After a fair machine, where is the minus sign?", ["On the circle's black entry", "Only on the square",
                                                                "Nowhere"], 0,
             "The square's flip turns into a minus sign on the circle."),
        pick("At the end, the circle comes out black. The machine is…", ["Fair", "Rigged"], 0,
             "Black means fair, and white means rigged."),
    ]),

    lesson(5, "Play: Rigged or fair?", [
        learn("The whole trick",
              "Here's the complete circuit: H on both qubits, the machine once, H on the circle, then measure the "
              "circle. White means rigged. Black means fair.",
              picture=diagram("circle square", "wb", ["H circle", "H square", "M circle square", "H circle", "MEASURE circle"])),
        play("Play it",
             "Each round, Qubi hides one of four machines. Run the trick and read the circle.",
             try_it=measure({"Rigged: the light never flips": trick(RIGGED_OFF),
                             "Rigged: the light always flips": trick(RIGGED_ON),
                             "Fair: it flips for the black button": trick(FAIR_COPY),
                             "Fair: it flips for the white button": trick(FAIR_OPPOSITE)},
                            shapes=["circle"], times=1, button="Play a round",
                            labels={(0,): "The circle came out white, so the machine is rigged.",
                                    (1,): "The circle came out black, so the machine is fair."})),
        predict("How many presses?",
                "Count how many times the trick used the machine.",
                ask("How many uses of the machine did it need?", ["One", "Two", "Four"], 0,
                    "Just one, where the normal way needs two. This is <b>Deutsch's algorithm</b>, one of the very "
                    "first quantum algorithms.")),
        learn("What it doesn't tell you",
              "The trick tells you rigged or fair, but not which button flips the light. Quantum computers answer "
              "certain questions faster. They don't speed up everything."),
    ], [
        pick("In the trick, which qubit do you measure at the end?", ["The circle", "The square", "Both"], 0,
             "The circle carries the answer."),
        pick("Why does the circle go through H before the machine?",
             ["So one use of the machine tests both buttons", "To make the machine faster", "To hide the answer"], 0,
             "In a superposition, the circle presses both buttons in one go."),
        pick("What can't the trick tell you?", ["Which button flips the light", "Whether the machine is fair",
                                                "Whether it's rigged"], 0,
             "It answers only one question: same or different."),
    ]),

    # ======== Unit 6 · Game: Find the gem (chapter 6) ========

    lesson(6, "Four lockers", [
        play("The game",
             "A gem is hidden in one of four lockers. Each locker has a two-color code: white-white, white-black, "
             "black-white or black-black.\n\n"
             "You have a marker gate (★) that checks codes for you. Normally you'd test one code at a time."),
        predict("The normal way",
                "Test one code at a time.",
                ask("How many tests might you need to be sure where the gem is?", ["3", "1", "4"], 0,
                    "If the first three codes are wrong, the gem must be behind the fourth. So up to 3 tests.")),
        learn("Every code at once",
              "Put a white circle and a white square through H. The cloud now holds all four codes, each with a 25% "
              "chance.",
              picture=run(ww, "H circle", "H square")),
        learn("The marker",
              "The marker puts a minus sign on the gem's code. Inside, it uses a helper qubit, just like the machine "
              "in Unit 5: the helper's flip turns into a minus sign.",
              picture=run(all_lockers, marker("bw")), note="Here the gem is in the black-white locker."),
        predict("Measure now?",
                "Say you measure right after the marker.",
                ask("What's the chance of getting the gem's code?", ["25%", "100%", "0%"], 0,
                    "Minus signs don't change the chances. Every code is still 25%.")),
    ], [
        pick("What does the marker do?", ["Puts a minus sign on the gem's code", "Opens the gem's locker",
                                          "Measures the qubits"], 0,
             "It marks the right code with a minus sign."),
        build_state("The gem is in the white-white locker. What comes out of the marker?", [all_lockers, "★", "ANSWER"],
                    after(all_lockers, marker("ww")),
                    "Only the white-white entry gets a minus sign. Pulling an overall minus sign out gives the same "
                    "state."),
        pick("How many tests can the normal way need?", ["Up to 3", "Always 1", "Up to 10"], 0,
             "With four lockers, three tests always tell you where the gem is."),
    ]),

    lesson(6, "The flip-around", [
        learn("Turning a sign into an answer",
              "Measuring can't see the marker's minus sign. To find the gem, we need a circuit that turns that sign "
              "into a result we can measure.\n\n"
              "That's the <b>flip-around</b> circuit: H on both, NOT on both, CZ, NOT on both, and H on both.",
              picture=diagram("circle square", "ww", ["H circle", "H square", "NOT circle", "NOT square",
                                                      "CZ circle square", "NOT circle", "NOT square", "H circle", "H square"])),
        learn("Watch it work",
              "Feed in the marked cloud. The gem's entry grows and all the others cancel out. Only the gem's code "
              "is left.",
              picture=[after(all_lockers, marker("bw")), "F", flip_around(after(all_lockers, marker("bw")))],
              note="F is the whole flip-around circuit."),
        predict("Measure it",
                "Now measure both qubits.",
                ask("What's the chance of getting the gem's code?", ["100%", "25%", "50%"], 0,
                    "Every other entry canceled out, so the gem's code is the only possible result.")),
        learn("Why it works",
              "The flip-around flips every entry around the average. The marked entry is far from the average, so "
              "it grows, and the others shrink to nothing.\n\n"
              "It's interference again: entries cancel on purpose, just like H then H."),
    ], [
        pick("What does the flip-around do?", ["Leaves only the marked code", "Adds more minus signs",
                                               "Measures the qubits"], 0,
             "It turns the marker's minus sign into a sure result."),
        build_state("The gem is in the black-black locker. What comes out of the flip-around?",
                    [after(all_lockers, marker("bb")), "F", "ANSWER"], bb,
                    "The flip-around leaves only the marked code: black-black."),
        pick("Why can't you just measure right after the marker?",
             ["Minus signs don't change the chances", "The marker breaks the qubits", "You can"], 0,
             "Right after the marker, every code still has a 25% chance."),
    ]),

    lesson(6, "Play: Find the gem", [
        play("Play it",
             "Each round, Qubi hides the gem in a random locker. Run the search once and open the locker it points to.",
             try_it=measure({f"The gem was in the {name} locker": flip_around(after(all_lockers, marker(code)))
                             for code, name in LOCKER_NAMES.items()},
                            times=1, button="Play a round",
                            labels={(0, 0): "The search says white-white.", (0, 1): "The search says white-black.",
                                    (1, 0): "The search says black-white.", (1, 1): "The search says black-black."})),
        predict("How many uses?",
                "Count how many times the search used the marker.",
                ask("How many?", ["Once", "Twice", "Four times"], 0,
                    "Once! For four lockers, one use of the marker always finds the gem.")),
        learn("Grover's search",
              "This is a small version of <b>Grover's algorithm</b>, a famous quantum search. Bigger searches need "
              "more uses of the marker, but far fewer than checking one by one.\n\n"
              "For a million lockers it takes about 800 uses, instead of up to 999,999 tests."),
    ], [
        pick("For four lockers, how many uses of the marker does the quantum search need?", ["1", "3", "4"], 0,
             "One use of the marker, then the flip-around, always finds the gem."),
        pick("What is this search called?", ["Grover's algorithm", "Deutsch's algorithm", "Teleportation"], 0,
             "Grover's algorithm searches through many options much faster than checking them one by one."),
        pick("For a million lockers, about how many marker uses does Grover's search need?",
             ["About 800", "About 500,000", "Just 1"], 0,
             "It grows like the square root: the square root of a million is 1,000, and Grover needs a bit less "
             "than that."),
    ]),

    # ======== Unit 7 · Bell states and teleportation (chapter 7) ========

    lesson(7, "The four Bell states", [
        learn("The Bell state generator",
              "Remember H on the circle followed by CNOT? From now on we'll call this circuit the <b>Bell state "
              "generator</b>.",
              picture=diagram("circle square", "ww", ["H circle", "CNOT circle square"])),
        learn("Four inputs, four Bell states",
              "Feed in each of the four plain inputs and you get four different entangled states. They're called "
              "the <b>Bell states</b>.",
              picture=table(["H circle", "CNOT circle square"], ww, wb, bw, bb)),
        predict("Can any of them split?",
                "Try to factor each Bell state into a circle cloud and a square cloud.",
                ask("How many of the four can be split?", ["None: all four are entangled", "All four", "Two of them"], 0,
                    "In every Bell state the square's color depends on the circle's, so none of them split.")),
        predict("Just measure?",
                "Someone hands you one of the four Bell states.",
                ask("If you just measure it, can you always tell which one it is?", ["No", "Yes"], 0,
                    "White-white | black-black and white-white | minus black-black give exactly the same results: "
                    "white-white or black-black, 50% each. Measuring can't see the minus sign."),
                picture=together(bell, make("circle square", "ww", "-bb"))),
        learn("See for yourself",
              "Measure white-white | minus black-black 10 times. The results look exactly like white-white | "
              "black-black.",
              picture=[make("circle square", "ww", "-bb")], try_it=measure(make("circle square", "ww", "-bb"))),
    ], [
        build_state("What does the generator make from a black circle and a white square?",
                    [bw, "H circle", "CNOT circle square", "ANSWER"], make("circle square", "ww", "-bb"),
                    "H gives white-white | minus black-white, then CNOT flips the square in the entry with the black "
                    "circle."),
        pick("Which two Bell states give the same measurement results?",
             ["White-white | black-black and white-white | minus black-black",
              "White-white | black-black and white-black | black-white", "No two of them"], 0,
             "They differ only by a minus sign, and measuring can't see signs."),
        build_circuit("Build the Bell state generator.", ["H", "CNOT", "NOT"], ["H circle", "CNOT circle square"],
                      [ww, wb, bw, bb], "H on the circle, then CNOT with the circle as control.", hint="Two gates."),
    ]),

    lesson(7, "Telling Bell states apart", [
        learn("Run it backwards",
              "To tell Bell states apart, run the generator backwards: CNOT first, then H on the circle. This is the "
              "<b>Bell state identifier</b>. Each Bell state turns back into its own plain input, which you can "
              "measure.",
              picture=run(bell, "CNOT circle square", "H circle")),
        predict("Identify this one",
                "Follow it through the identifier.",
                ask("What comes out?", ["Black circle, black square", "White circle, white square",
                                        "White circle, black square"], 0,
                    "CNOT gives white-black | minus black-black. H on the circle then cancels the white-black "
                    "entries, leaving black-black."),
                picture=[make("circle square", "wb", "-bw"), "CNOT circle square", "H circle", "ANSWER"]),
        predict("Generator, then identifier",
                "Run the generator and then the identifier, one after the other.",
                ask("What comes out?", ["Exactly what went in", "A Bell state", "Random results"], 0,
                    "The identifier undoes the generator: the same gates in reverse order, and each one undoes itself. "
                    "Together they do nothing.")),
        learn("Switching Bell states",
              "One gate on one qubit can switch between Bell states. NOT on the square turns white-white | "
              "black-black into white-black | black-white.",
              picture=run(bell, "NOT square")),
        predict("Which gate?",
                "You want to turn white-white | black-black into white-white | minus black-black.",
                ask("Which gate does it?", ["Z on the circle", "NOT on the circle", "H on the square"], 0,
                    "Z puts a minus sign on every entry where the circle is black. Here that's just black-black."),
                picture=[bell, "ANSWER", make("circle square", "ww", "-bb")]),
    ], [
        build_state("Send it through the identifier. What comes out?",
                    [make("circle square", "wb", "bw"), "CNOT circle square", "H circle", "ANSWER"], wb,
                    "CNOT gives white-black | black-black. H on the circle then cancels the black-black entries, "
                    "leaving white-black."),
        build_circuit("Build the Bell state identifier.", ["H", "CNOT"], ["CNOT circle square", "H circle"],
                      [bell, make("circle square", "wb", "bw"), make("circle square", "ww", "-bb"),
                       make("circle square", "wb", "-bw")],
                      "CNOT first, then H on the circle: the generator backwards.", hint="Reverse the generator."),
        pick("NOT on the square turns white-white | black-black into…",
             ["White-black | black-white", "White-white | minus black-black", "A plain state"], 0,
             "NOT flips the square in both entries."),
    ]),

    lesson(7, "Teleportation: the setup", [
        learn("The goal",
              "A Sender has a qubit in some state we'll call Ψ (psi). She wants a Receiver far away to end up with "
              "exactly that state.\n\n"
              "She can't just measure it and describe it: measuring would destroy the superposition. And she won't "
              "send the qubit itself.",
              picture=[minus], note="Our example Ψ: white | minus black."),
        learn("Share a Bell state",
              "First, they make a Bell state with a square and a triangle. The Sender keeps the square. The Receiver "
              "takes the triangle far away.",
              picture=run(make("square triangle", "ww"), "H square", "CNOT square triangle")),
        learn("All three qubits",
              "The Sender's circle (holding Ψ) and the shared pair make one three-qubit state. Joined into one "
              "cloud, it has four entries.",
              picture=[teleport_start]),
        learn("The teleporter",
              "The Sender puts her circle and square through the <b>teleporter</b>: a CNOT with the circle as "
              "control, then H on the circle. Then she measures both, and sends the two colors to the Receiver in "
              "a normal message.",
              picture=diagram(TRIO, "www", ["H square", "CNOT square triangle", "CNOT circle square", "H circle",
                                            "MEASURE circle square"]),
              note="The circle starts in Ψ. The first two gates make the shared Bell state."),
        predict("Is it there yet?",
                "Right after the Sender measures, before her message arrives…",
                ask("Does the Receiver's triangle already hold Ψ?",
                    ["Not yet: it may need a fix that depends on the message", "Yes, always", "No, Ψ is destroyed"], 0,
                    "The triangle is close to Ψ, but depending on what the Sender saw, it may need a NOT, a Z or both.")),
    ], [
        pick("What do the Sender and Receiver share before teleporting?", ["A Bell state", "The qubit holding Ψ", "Nothing"], 0,
             "Each keeps one half of an entangled pair."),
        pick("What does the Sender send to the Receiver?", ["Two colors, in a normal message", "Her qubit", "A copy of Ψ"], 0,
             "Just the two colors she measured."),
        pick("Why can't the Sender just measure Ψ and describe it?",
             ["Measuring destroys the superposition", "Measuring is too slow", "She can"], 0,
             "Measuring gives one plain result and ends the superposition, so Ψ would be lost."),
    ]),

    lesson(7, "Teleportation: the fix", [
        learn("Four possible messages",
              "The Sender's measurement gives one of four results, each 25% of the time. For each one, the "
              "Receiver's triangle is left in a slightly different state. Here Ψ is white | minus black.",
              picture=results(after_sender, "circle square"), note="Each message, its chance, and what's left."),
        learn("The state adjuster",
              "The Receiver fixes the triangle using the message. This fix is called the <b>state adjuster</b>: if "
              "the square was black, use NOT. If the circle was black, use Z. If both were black, use NOT and then Z.\n\n"
              "After that, the triangle holds exactly Ψ. Sometimes a fix only adds an overall minus sign, which "
              "doesn't matter, but the rule always works."),
        predict("Fix it",
                "The message says: black circle, white square. The triangle is in white | black.",
                ask("What does the Receiver do?", ["Use Z", "Use NOT", "Nothing"], 0,
                    "A black circle means Z. Z turns white | black into white | minus black, which is Ψ."),
                picture=[make("triangle", "w", "b"), "ANSWER", make("triangle", "w", "-b")]),
        predict("Another state",
                "Now teleport Ψ = white. The message says white circle, black square, and the triangle is black.",
                ask("What does the Receiver do?", ["Use NOT", "Use Z", "Nothing"], 0,
                    "A black square means NOT. NOT turns the black triangle white, which is Ψ.")),
        play("Teleport it",
             "Each round, the Sender measures for real. Qubi shows her message and the Receiver's fix.",
             try_it=measure(after_sender, shapes=["circle", "square"], times=1, button="Teleport it",
                            labels={(0, 0): "White, white: the Receiver does nothing.",
                                    (0, 1): "White, black: the Receiver uses NOT.",
                                    (1, 0): "Black, white: the Receiver uses Z.",
                                    (1, 1): "Black, black: the Receiver uses NOT, then Z."})),
        learn("No faster than light, no copies",
              "The Receiver can't finish until the message arrives, and messages can't travel faster than light. "
              "So teleportation can't send information faster than light.\n\n"
              "And the Sender's circle lost Ψ when she measured it. Ψ was moved, not copied. In fact, an unknown "
              "quantum state can never be perfectly copied."),
    ], [
        pick("The message says white circle, black square. The Receiver uses…", ["NOT", "Z", "Nothing"], 0,
             "A black square means NOT."),
        pick("After teleporting, does the Sender still have Ψ?", ["No, measuring ended it", "Yes, now there are two copies"], 0,
             "Ψ was moved, not copied."),
        pick("Why can't teleportation send messages faster than light?",
             ["The Receiver needs the Sender's normal message first", "Qubits move slowly", "It can"], 0,
             "Without the two colors, the Receiver doesn't know which fix to use."),
    ]),
]