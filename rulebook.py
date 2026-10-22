# The Rulebook: every rule from the lessons, one short card each.
# A lesson's rules unlock when you finish that lesson.

from lessons import LESSONS, table, together, run, white, black, plus, minus, wb, bw


def rule(name, text, picture=None):
    return {"name": name, "text": text, "picture": picture}


def from_lesson(number, step_title):
    """The picture from one step of a lesson, found by the step's title."""
    for step in LESSONS[number - 1]["steps"]:
        if step["title"] == step_title:
            return step["picture"]
    raise ValueError(f"Lesson {number} has no step called {step_title}")


RULES = {
    # ---------------- Unit 1: bits, gates, qubits ----------------
    1: [rule("Bits as shapes",
             "A bit is 0 or 1. White means 0, black means 1. The shape is just a name tag.",
             together(white, black))],
    2: [rule("NOT flips",
             "NOT turns white into black and black into white.",
             table("NOT circle", white, black)),
        rule("Gates can be undone",
             "Every quantum gate can be undone. NOT undoes itself.",
             run(white, "NOT circle", "NOT circle"))],
    3: [rule("SWAP trades",
             "SWAP trades the colors of its two shapes.",
             table("SWAP circle square", wb, bw)),
        rule("CNOT",
             "The control is the dot (•), the target is ⊕. If the control is black, the target flips. "
             "If the control is white, nothing happens.",
             from_lesson(3, "CNOT's rule table"))],
    4: [rule("Circuits",
             "A circuit is gates used one after another. What comes out of one gate goes into the next.",
             from_lesson(4, "Gates in a row")),
        rule("Same job",
             "Two circuits do the same job if they give the same output for every input. "
             "Two NOTs in a row do the same job as no gate at all.",
             table(["NOT circle", "NOT circle"], white, black))],
    5: [rule("The cloud",
             "A cloud is a superposition. Its entries are split by bars, and each entry is a possible result.",
             from_lesson(5, "The cloud means superposition")),
        rule("Measuring",
             "Measuring picks one entry at random. The cloud is gone and you get plain shapes.",
             from_lesson(5, "Measuring"))],
    6: [rule("Equal chances",
             "If no entry repeats, every entry is equally likely: 2 entries = 50% each, 3 = about 33%, 4 = 25%.",
             from_lesson(6, "Equal entries, equal chances")),
        rule("Measuring some qubits",
             "Measure only some shapes, and keep only the entries that match what you saw.",
             from_lesson(6, "Measuring just one qubit"))],
    7: [rule("The H gate",
             "H puts a qubit into a superposition. White → white | black. Black → white | minus black.",
             from_lesson(7, "H's rule table")),
        rule("Measuring can't see signs",
             "Minus signs never show up when you measure, but they change what happens next.",
             run(minus, "measure"))],
    8: [rule("Order doesn't matter",
             "You can write a cloud's entries in any order.",
             from_lesson(8, "Rules for clouds")),
        rule("Opposites cancel",
             "Two entries that are the same except for a minus sign cancel. Remove both.",
             from_lesson(8, "Opposites cancel")),
        rule("Equal repeats shrink",
             "If every entry appears the same number of times, shrink each to one copy.",
             from_lesson(8, "Equal repeats shrink")),
        rule("One entry, no cloud",
             "If only one entry is left, it's not a superposition. Drop the cloud.",
             from_lesson(8, "One entry, no cloud")),
        rule("Moving minus signs",
             "You can flip every sign in a cloud. A minus sign in front of everything doesn't matter.",
             from_lesson(8, "Moving minus signs"))],
    9: [rule("Joining clouds",
             "Pair every entry of one cloud with every entry of the other, like FOIL.",
             from_lesson(9, "Joining qubits into one cloud")),
        rule("Multiply the signs",
             "When you pair entries, multiply their signs. Plus × minus = minus. Minus × minus = plus.",
             from_lesson(9, "Watch the signs")),
        rule("Factoring",
             "If a shape has the same color in every entry, you can pull it out of the cloud.",
             from_lesson(9, "Factoring: splitting a cloud")),
        rule("Entangled",
             "A cloud that can't be split into one cloud per shape is entangled.",
             from_lesson(9, "Clouds that won't split"))],
    10: [rule("Superpositions through gates",
              "Send each entry through the gate on its own, pour the results into one cloud, then tidy.",
              from_lesson(10, "One entry at a time")),
         rule("H then H",
              "H twice gives back what you started with. The extra entries cancel, which a coin flip can't do.",
              run(white, "H circle", "H circle")),
         rule("H then CNOT entangles",
              "H on the circle, then CNOT, makes an entangled cloud.",
              from_lesson(10, "Two qubits: entanglement"))],

    # ---------------- Unit 2: practice ----------------
    11: [rule("Joining three qubits",
              "Join one pair at a time. A shape with one color in every entry keeps that color everywhere.",
              from_lesson(11, "The joined cloud"))],
    12: [rule("The factoring trick",
              "Pull out a shape with the same color in every entry, then check if what's left splits again.",
              from_lesson(12, "The trick")),
         rule("Why factoring matters",
              "If a cloud splits, think about each shape on its own. If not, they're entangled: think about them together.")],
    13: [rule("Chances when measuring some",
              "The chance of seeing a color is the share of entries with that color.",
              from_lesson(13, "Measure some, keep the rest"))],
    14: [rule("Plain inputs are enough",
              "If two circuits match on every plain input (just white and black), they match on every superposition too.")],
    15: [rule("NOT can't change white | black",
              "NOT swaps the two entries, so white | black stays the same. That's how you beat the prankster: "
              "H, hand it over, H again, guess white.",
              run(plus, "NOT circle"))],

    # ---------------- Unit 3: real quantum computers ----------------
    16: [rule("Circuit diagrams",
              "Each line is a qubit. Time runs left to right. Every qubit starts white, so use NOT to start black.",
              from_lesson(16, "Lines are qubits")),
         rule("Shots and noise",
              "Each run is a shot. Real hardware makes small errors, so 50% might show up as 48%.")],
    17: [rule("Test every input",
              "To check a gate on real hardware, try every plain input. Use NOT gates to make the black ones.",
              from_lesson(17, "CNOT on every input"))],
    18: [rule("The entangling circuit",
              "H then CNOT gives white-white | black-black. The two qubits always match when measured.",
              from_lesson(18, "The entangling circuit")),
         rule("Three CNOTs = SWAP",
              "Three CNOTs, with the middle one pointing the other way, do the same job as SWAP.",
              from_lesson(18, "Three CNOTs"))],

    # ---------------- Unit 4: more gates ----------------
    19: [rule("The Z gate",
              "Z leaves white alone and puts a minus sign on black. "
              "In a superposition it flips the sign of the black entry only.",
              from_lesson(19, "Z on a superposition")),
         rule("Z from H and NOT",
              "H, then NOT, then H does the same job as Z.",
              run(plus, "H circle", "NOT circle", "H circle"))],
    20: [rule("Control-Z (CZ)",
              "CZ puts a minus sign on an entry only when both shapes are black.",
              from_lesson(20, "Z with a control")),
         rule("CZ in disguise",
              "H on the target, CZ, H on the target again does the same job as CNOT.",
              from_lesson(20, "CZ in disguise"))],
    21: [rule("Toffoli",
              "Two controls and one target. The target flips only when both controls are black.",
              from_lesson(21, "Two controls")),
         rule("Toffoli as a CNOT",
              "Make one control always black, and Toffoli works like a CNOT.",
              from_lesson(21, "Fixing a broken CNOT"))],

    # ---------------- Unit 5: the carnival machine ----------------
    22: [rule("The machine M",
              "The circle is the button, the square is the light. Rigged: same for both buttons. "
              "Fair: different for each button. M never changes the circle.",
              from_lesson(22, "The machine as a gate"))],
    23: [rule("The minus sign jumps",
              "With the square in white | minus black, a flip of the square turns into a minus sign on the circle's black entry.",
              from_lesson(23, "Step 2: use the machine once")),
         rule("Rigged leaves no mark",
              "A rigged machine leaves the circle in white | black. At most it adds an overall minus, which doesn't matter.",
              from_lesson(23, "Rigged machines leave no mark"))],
    24: [rule("The whole trick",
              "H on both, use the machine once, H on the circle, measure the circle. White = rigged. Black = fair.",
              from_lesson(24, "The whole trick"))],

    # ---------------- Unit 6: finding the gem ----------------
    25: [rule("Every code at once",
              "H on two white qubits makes all four codes, each with a 25% chance.",
              from_lesson(25, "Every code at once")),
         rule("The marker ★",
              "The marker puts a minus sign on the gem's code. Measuring can't see it yet.",
              from_lesson(25, "The marker"))],
    26: [rule("The flip-around",
              "H on both, NOT on both, CZ, NOT on both, H on both. The marked entry grows and the rest cancel.",
              from_lesson(26, "Turning a sign into an answer"))],
    27: [rule("Grover's search",
              "Mark, then flip around. For 4 lockers, once is enough. Bigger searches need more rounds, "
              "but far fewer than checking one by one.")],

    # ---------------- Unit 7: Bell states and teleportation ----------------
    28: [rule("The Bell states",
              "The Bell state generator is H on the circle, then CNOT. The four plain inputs give the four Bell states. "
              "None of them can be split.",
              from_lesson(28, "Four inputs, four Bell states"))],
    29: [rule("The Bell state identifier",
              "Run the generator backwards: CNOT, then H on the circle. Each Bell state turns back into its plain input.",
              from_lesson(29, "Run it backwards")),
         rule("Switching Bell states",
              "One gate on one qubit switches Bell states. NOT on the square turns always-match into always-opposite.",
              from_lesson(29, "Switching Bell states"))],
    30: [rule("The teleporter",
              "Share a Bell state. The Sender does CNOT (circle → square), then H on the circle, "
              "measures both, and sends the two colors.",
              from_lesson(30, "The teleporter"))],
    31: [rule("The state adjuster",
              "Square black: NOT. Circle black: Z. Both black: NOT, then Z. Now the triangle holds Ψ.",
              from_lesson(31, "Four possible messages")),
         rule("No copies, no faster than light",
              "The Sender's qubit loses Ψ when she measures, so it's moved, not copied. "
              "And the Receiver has to wait for the message.")],
}