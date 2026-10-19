# All 18 lessons. Each lesson has steps (things to read, predict or try) and a quiz.
# Edit the words here: the pictures are made by the quantum engine, so they always follow the rules.
#
#   make("circle", "w")            a white circle          ("w" = white, "b" = black)
#   make("circle", "w", "-b")      a mist: white circle | minus black circle
#   run(start, "H circle", ...)    a picture: start -> H box -> result -> ...
#   together(a, b)                 a picture of states side by side, no arrows
#   "ANSWER"                       the dashed ? box in a quiz picture

from engine.qubits import make, untidy, run


# ================= helpers to write steps and questions =================

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


def together(*states):
    """A picture of states side by side, with no arrows between them."""
    return {"together": list(states)}


def pick(question, options, answer, why, picture=None, hint=""):
    return {"type": "pick", "question": question, "options": options, "answer": answer,
            "why": why, "picture": picture, "hint": hint}


def build_state(question, picture, answer, why, hint=""):
    return {"type": "state", "question": question, "picture": picture, "answer": answer, "why": why, "hint": hint}


def build_circuit(question, allowed, target, inputs, why, hint=""):
    """The learner builds a circuit that does the same thing as `target` to every state in `inputs`."""
    return {"type": "circuit", "question": question, "allowed": allowed, "target": target,
            "inputs": inputs, "why": why, "hint": hint}


# ================= shapes we use a lot =================

white = make("circle", "w")
black = make("circle", "b")
mist = make("circle", "w", "b")
minus_mist = make("circle", "w", "-b")
two_white = make("circle square", "ww")


# ================= boxes for the games =================

def machine(rule):
    """Game 1: a carnival machine. The circle is the button, the square is the light."""
    return ("?", lambda state: state.box(rule))

def trick(rule):
    """Game 1: the quantum trick on one machine."""
    return make("circle square", "wb").H("circle").H("square").box(rule).H("circle")

RIGGED_OFF = lambda c: [c[0], c[1]]                 # light never changes
RIGGED_ON = lambda c: [c[0], 1 - c[1]]              # light always flips
FAIR_COPY = lambda c: [c[0], c[1] ^ c[0]]           # flips for the black button
FAIR_OPPOSITE = lambda c: [c[0], c[1] ^ (1 - c[0])] # flips for the white button

no_alarm = make("circle square", "ww").H("circle").H("circle")
alarm = make("circle square", "ww").H("circle").CNOT("circle", "square").H("circle")

MARKERS = {   # Game 3: puts a minus on the gem's locker code
    "ww": lambda s: s.NOT("circle").NOT("square").CZ("circle", "square").NOT("circle").NOT("square"),
    "wb": lambda s: s.NOT("circle").CZ("circle", "square").NOT("circle"),
    "bw": lambda s: s.NOT("square").CZ("circle", "square").NOT("square"),
    "bb": lambda s: s.CZ("circle", "square"),
}

def flip_around(state):
    """Game 3: H, NOT, Control-Z, NOT, H on both shapes. The marked entry grows, the rest cancel."""
    return (state.H("circle").H("square").NOT("circle").NOT("square").CZ("circle", "square")
                 .NOT("circle").NOT("square").H("circle").H("square"))

all_lockers = make("circle square", "ww").H("circle").H("square")
LOCKER_NAMES = {"ww": "white-white", "wb": "white-black", "bw": "black-white", "bb": "black-black"}

bell = make("circle square", "ww").H("circle").CNOT("circle", "square")
teleport_start = make("circle square triangle", "www", "wbb", "-bww", "-bbb")   # mist on circle + linked pair
after_alice = teleport_start.copy().CNOT("circle", "square").H("circle")


# ================= the lessons =================

LESSONS = [

    # ---------------- Unit 1 · Computers, bits and gates ----------------
    {"title": "What makes a computer quantum?",
     "steps": [
        learn("Computers run on bits",
              "Every photo, song and game on your phone is stored as bits. A bit is the simplest piece of "
              "information there is: 0 or 1, like a light that is off or on.\n\n"
              "A computer flips billions of bits every second. That's all it ever does.",
              picture=together(white, black), note="Off and on, 0 and 1."),
        learn("Quantum bits can do more",
              "A quantum computer uses qubits. A qubit can be 0 or 1 like a bit, but it can also be in a "
              "mist: a blend of both at the same time.\n\n"
              "When you look at a qubit in a mist, the mist disappears and you see a plain 0 or 1. "
              "Clever circuits use mists to solve some problems in far fewer steps."),
        predict("What are they good at?",
                "Quantum computers won't replace your laptop. They're built for special jobs.",
                ask("Which job is a quantum computer expected to be great at?",
                    ["Streaming videos faster", "Simulating molecules to design new medicines",
                     "Writing your essays"], 1,
                    "Nature follows quantum rules, so a quantum computer is a natural fit for simulating atoms "
                    "and molecules. That's hard for normal computers.")),
        learn("How Qubi teaches it",
              "Most quantum courses start with heavy math. Qubi uses pictures instead: shapes for qubits, "
              "boxes for gates, and a cloud of mist for superposition.\n\n"
              "Follow the pictures step by step. By Unit 3 you'll build your own circuits, and you can run "
              "them on a real quantum computer.",
              picture=run(white, "H circle"), note="You'll understand this picture by Lesson 7."),
     ],
     "quiz": [
        pick("What is a bit?", ["A tiny magnet", "A piece of information that is 0 or 1", "A small program"], 1,
             "A bit is the simplest piece of information: 0 or 1, off or on."),
        pick("What can a qubit do that a normal bit can't?",
             ["Be in a mist of 0 and 1 at once", "Store a whole photo", "Work without electricity"], 0,
             "Only qubits can be in a mist (a superposition) of 0 and 1."),
        pick("What happens when you look at a qubit that's in a mist?",
             ["You see the whole mist", "You see a plain 0 or 1", "The qubit breaks"], 1,
             "Looking (measuring) makes the mist disappear. You get one plain answer."),
     ]},

    {"title": "Bits as shapes",
     "steps": [
        learn("A qubit is a shape",
              "In Qubi every qubit is drawn as a shape. Its color is its value: a white shape means 0 and a "
              "black shape means 1.",
              picture=together(white, black), note="White circle = 0, black circle = 1."),
        learn("More shapes, more qubits",
              "Computers use many qubits, so each one gets its own shape: a circle, a square, a triangle. "
              "Read them left to right.",
              picture=[make("circle square", "wb")], note="White circle, black square: this pair reads 01."),
        predict("Counting combinations",
                "Each shape can be white or black.",
                ask("How many color combinations can a circle and a square make?", ["2", "4", "8"], 1,
                    "White-white, white-black, black-white and black-black: 2 × 2 = 4."),
                picture=together(make("circle square", "ww"), make("circle square", "wb"),
                                 make("circle square", "bw"), make("circle square", "bb"))),
        predict("Add a triangle",
                "Now add a third shape.",
                ask("How many combinations can three shapes make?", ["6", "8", "9"], 1,
                    "Every new shape doubles the count: 2 × 2 × 2 = 8. Ten shapes already give 1,024.")),
     ],
     "quiz": [
        build_state("Build a black circle and a white square.", None, make("circle square", "bw"),
                    "Black means 1 and white means 0, so this pair reads 10.",
                    hint="Use one entry. Set the circle to black and the square to white."),
        pick("A white square stands for…", ["0", "1", "It depends on the circle"], 0, "White always means 0."),
        pick("How many combinations can four shapes make?", ["8", "16", "32"], 1,
             "2 × 2 × 2 × 2 = 16. Every shape doubles it."),
     ]},

    {"title": "Boxes that flip and swap",
     "steps": [
        learn("Gates are boxes",
              "To compute, we change qubits with gates. In Qubi a gate is a box with pegs. A shape goes in "
              "the top and comes out the bottom, changed or not.",
              picture=run(white, "NOT circle"), note="The NOT box flips white to black."),
        predict("Black into NOT",
                "The NOT box always flips the color.",
                ask("What comes out when a black circle goes into NOT?", ["A black circle", "A white circle", "Nothing"], 1,
                    "NOT flips the color, so black becomes white."),
                picture=[black, "NOT", "ANSWER"]),
        predict("Two NOTs in a row",
                "Boxes can be stacked: the output of one goes into the next.",
                ask("A white circle goes through two NOT boxes. What comes out?", ["A white circle", "A black circle"], 0,
                    "The first NOT makes it black and the second makes it white again. Two flips undo each other."),
                picture=run(white, "NOT circle", "NOT circle")),
        learn("The SWAP box",
              "Some boxes take two shapes. The SWAP box trades the colors of the two shapes on its pegs.",
              picture=run(make("circle square", "bw"), "SWAP circle square"), note="The circle and square trade colors."),
     ],
     "quiz": [
        build_state("A white circle and a black square go into SWAP. What comes out?",
                    [make("circle square", "wb"), "SWAP", "ANSWER"], make("circle square", "bw"),
                    "SWAP trades the colors, so the circle becomes black and the square white."),
        pick("Which box turns white into black and black into white?", ["SWAP", "NOT", "MEASURE"], 1,
             "NOT flips a single shape's color."),
        build_circuit("Turn both shapes black: a white circle and a white square must both come out black.",
                      ["NOT", "SWAP"], ["NOT circle", "NOT square"], [two_white],
                      "One NOT on each shape flips both to black.",
                      hint="Each shape needs its own flip."),
     ]},

    {"title": "Control boxes and circuits",
     "steps": [
        learn("A box with a control",
              "The CNOT box has two pegs. The dot is the control and the ⊕ is the target.\n\n"
              "If the control shape is black, the target flips. If the control is white, nothing happens.",
              picture=run(make("circle square", "bw"), "CNOT circle square"), note="The circle is black, so the square flips."),
        predict("A white control",
                "Same box, but now the control is white.",
                ask("A white circle and a black square go into CNOT. What comes out?",
                    ["White circle, black square", "White circle, white square", "Black circle, black square"], 0,
                    "The circle (the control) is white, so nothing flips."),
                picture=[make("circle square", "wb"), "CNOT", "ANSWER"]),
        learn("Circuits are boxes in a row",
              "A circuit is a list of boxes, one after another. To follow one, push the shapes through one "
              "box at a time.",
              picture=run(two_white, "NOT circle", "CNOT circle square"),
              note="NOT makes the circle black, then CNOT flips the square."),
        predict("Does order matter?",
                "Same two boxes, opposite order. Start from a white circle and a white square.",
                ask("CNOT first, then NOT on the circle. What comes out?",
                    ["Black circle, black square", "Black circle, white square", "White circle, black square"], 1,
                    "CNOT sees a white circle, so the square stays white. Then NOT flips the circle. Changing the "
                    "order changed the answer."),
                picture=run(two_white, "CNOT circle square", "NOT circle")),
     ],
     "quiz": [
        build_state("A black circle and a black square go into CNOT. What comes out?",
                    [make("circle square", "bb"), "CNOT", "ANSWER"], make("circle square", "bw"),
                    "The circle is black, so the square flips from black to white."),
        pick("In a CNOT box, which shape decides whether the other one flips?",
             ["The target", "The control (the dot)", "Neither"], 1, "The control decides. The target is the one that flips."),
        build_circuit("Copy the circle's color onto the square. The square always starts white.",
                      ["NOT", "CNOT", "SWAP"], ["CNOT circle square"], [two_white, make("circle square", "bw")],
                      "A CNOT with the circle as control flips the white square only when the circle is black, "
                      "so the square ends up matching.",
                      hint="Which box flips the square only when the circle is black?"),
     ]},

    # ---------------- Unit 2 · Going quantum ----------------
    {"title": "Meet the mist",
     "steps": [
        learn("A new kind of state",
              "So far every shape has been plainly white or black. A qubit can also be in a mist: a cloud "
              "holding several possibilities at once.\n\n"
              "Each possibility inside is called an entry, and a bar separates the entries.",
              picture=[mist], note="A mist with two entries: a white circle and a black circle."),
        learn("Not secretly one or the other",
              "It's tempting to think the circle is really white or really black and we just don't know which. "
              "That's not what a mist is.\n\n"
              "A mist is a real state of its own. In the next lessons you'll see mists do things that no "
              "plain shape, and no coin flip, can do."),
        predict("Reading a mist",
                "Mists can hold more than one shape in each entry.",
                ask("How many entries are in this mist?", ["1", "2", "4"], 1,
                    "Two entries: a white circle with a white square, and a black circle with a black square."),
                picture=[make("circle square", "ww", "bb")]),
        learn("Minus signs",
              "An entry can also carry a minus sign. Two mists that differ only by a minus sign look alike, "
              "but they behave differently when they go through boxes. So the sign matters.",
              picture=[minus_mist], note="White circle, minus black circle."),
     ],
     "quiz": [
        pick("What is a mist?", ["A broken qubit", "A state that holds several entries at once", "A qubit that is always black"], 1,
             "A mist (a superposition) holds several entries at the same time."),
        build_state("Build a mist of a white circle and a black circle.", None, mist,
                    "Two entries, both with a plus sign.", hint="Add a second entry, then make one white and one black."),
        pick("In a mist, what separates the entries?", ["A bar |", "A plus sign", "An arrow"], 0,
             "Entries are separated by a bar."),
     ]},

    {"title": "Looking inside a mist",
     "steps": [
        learn("Measuring",
              "To read a qubit, you measure it with the measure box. If the qubit is in a mist, the mist "
              "disappears and you get just one of its entries, picked at random.",
              picture=run(mist, "measure")),
        learn("Equal entries, equal chances",
              "When the entries look the same apart from their colors, each one is equally likely. "
              "Two entries means a 50% chance each, like flipping a coin.",
              try_it=measure(mist)),
        predict("Do minus signs change the chances?",
                "Here's the mist with a minus sign on black.",
                ask("When you measure white circle | minus black circle, what's the chance of black?",
                    ["0%", "50%", "100%"], 1,
                    "Measuring ignores minus signs. They only matter when a mist goes through more boxes."),
                picture=run(minus_mist, "measure")),
        predict("After measuring",
                "Say you measured the mist and saw a black circle.",
                ask("What state is the circle in now?", ["Still the mist", "A plain black circle", "A plain white circle"], 1,
                    "Measuring ends the mist. The qubit is now plainly what you saw.")),
     ],
     "quiz": [
        pick("A mist has 4 equal entries. What's the chance of each one?", ["25%", "50%", "100%"], 0,
             "Four equally likely entries share 100%, so 25% each."),
        pick("What happens to a mist when you measure it?",
             ["It stays a mist", "It becomes one of its entries", "It gains an entry"], 1,
             "Measuring picks one entry and the mist is gone."),
        pick("You measure white circle | minus black circle. What's the chance of black?", ["0%", "50%", "100%"], 1,
             "Minus signs don't change the chances. It's still 50/50."),
     ]},

    {"title": "The H box",
     "steps": [
        learn("The mist maker",
              "The H box (named after the mathematician Jacques Hadamard) is the box that makes mists. "
              "Put a white circle in and a mist of white and black comes out.",
              picture=run(white, "H circle")),
        predict("Black into H",
                "Now send a black circle through the same box.",
                ask("What comes out when a black circle goes into H?",
                    ["The same mist as before", "A mist with a minus on the black entry", "A plain white circle"], 1,
                    "H turns black into white | minus black. The minus sign is how H remembers the input was black."),
                picture=[black, "H", "ANSWER"]),
        predict("What happens when you look at a mist?",
                "The H box turned a white circle into a mist. Measuring it makes the mist disappear, and you're "
                "left with one entry, picked at random.",
                ask("You do this 100 times. About how often do you see a black circle?",
                    ["Never", "About 50 times", "All 100 times"], 1,
                    "Both entries in this mist are equally likely, so it's a coin flip: about 50 out of 100. The mist "
                    "itself isn't random. Only what you see when you measure is."),
                picture=run(white, "H circle", "measure"), try_it=measure(mist)),
        learn("Random on purpose",
              "This is how quantum computers make truly random numbers: send a qubit through H and measure it. "
              "No pattern and no way to cheat, because the randomness comes from nature itself."),
     ],
     "quiz": [
        build_state("A black circle goes into the H box. What comes out?", [black, "H", "ANSWER"], minus_mist,
                    "H turns a black circle into white circle | minus black circle.",
                    hint="H always gives two entries. A black input puts a minus on one of them."),
        build_state("A white circle goes into the H box. What comes out?", [white, "H", "ANSWER"], mist,
                    "H turns a white circle into white circle | black circle."),
        pick("You measure the output of H on a white circle. What's the chance of white?", ["0%", "50%", "100%"], 1,
             "The two entries are equally likely, so 50%."),
     ]},

    {"title": "Tidying up mists",
     "steps": [
        learn("Why tidy?",
              "When mists go through boxes, entries can pile up. Three rules keep mists neat, and they never "
              "change what the mist does."),
        learn("Rule 1: opposites cancel",
              "If the same entry shows up once with a plus and once with a minus, the two cancel out and both "
              "disappear.",
              picture=[untidy("circle", "w", "b", "-b"), white], note="black and minus black cancel, so a white circle is left."),
        learn("Rule 2: copies shrink",
              "If every entry shows up the same number of times, keep just one of each.",
              picture=[untidy("circle", "w", "w", "b", "b"), mist], note="Two of each shrinks to one of each."),
        learn("Rule 3: an overall minus doesn't matter",
              "You can flip every sign in a mist at once. So minus white | minus black is the same as "
              "white | black, and minus white | black is the same as white | minus black.",
              picture=[untidy("circle", "-w", "b"), minus_mist], note="Flip every sign: nothing really changes."),
        predict("Your turn to tidy",
                "Use the rules one at a time.",
                ask("Tidy up white | black | white | minus black. What's left?",
                    ["A white circle", "A black circle", "white | black"], 0,
                    "black and minus black cancel. That leaves white | white, and two copies shrink to one: a plain "
                    "white circle."),
                picture=[untidy("circle", "w", "b", "w", "-b"), "ANSWER"]),
     ],
     "quiz": [
        pick("Tidy up white circle | minus white circle | black circle.", ["A black circle", "A white circle", "Nothing is left"], 0,
             "white and minus white cancel, leaving a black circle."),
        build_state("Tidy up minus white circle | minus black circle.", [untidy("circle", "-w", "-b"), "ANSWER"], mist,
                    "Every entry has a minus, so flip them all: white | black.", hint="Rule 3: flip every sign at once."),
        pick("Is minus white | black the same as white | minus black?",
             ["Yes, flipping every sign changes nothing", "No, they're different mists"], 0,
             "Flipping every sign at once never changes a mist."),
     ]},

    {"title": "Mists through boxes",
     "steps": [
        learn("One entry at a time",
              "To send a mist through a box, send each entry through on its own. Put all the results into one "
              "mist, then tidy it."),
        learn("H on a mist",
              "Send white | black through H. White becomes white | black, and black becomes white | minus black. "
              "Together that's white | black | white | minus black.\n\n"
              "Now tidy: the blacks cancel and the two whites shrink to one.",
              picture=[mist, "H", untidy("circle", "w", "b", "w", "-b"), white],
              note="The mist turns back into a plain white circle."),
        predict("H twice",
                "Put two H boxes in a row.",
                ask("A white circle goes through H, then H again. What comes out?",
                    ["A mist", "A white circle", "A black circle"], 1,
                    "The first H makes a mist and the second H turns it back into white. H undoes itself."),
                picture=run(white, "H circle", "H circle")),
        learn("This is interference",
              "The black entries canceled out, like two waves meeting and flattening. This is called "
              "interference.\n\n"
              "Quantum computers use it on purpose: they set up mists so wrong answers cancel and right answers "
              "stay. No coin flip can do that."),
        predict("Black through H twice",
                "Try it with a black circle.",
                ask("A black circle goes through H twice. What comes out?",
                    ["A white circle", "A black circle", "white | minus black"], 1,
                    "The first H gives white | minus black, and the second H turns that into black. H twice always "
                    "gives back what you started with."),
                picture=run(black, "H circle", "H circle")),
     ],
     "quiz": [
        build_state("white circle | minus black circle goes into H. What comes out?", [minus_mist, "H", "ANSWER"], black,
                    "white becomes white | black, and minus black becomes minus white | black. The whites cancel and the "
                    "two blacks shrink to one black circle.",
                    hint="Send each entry through H, write them all down, then tidy."),
        build_state("white circle | black circle goes into NOT. What comes out?", [mist, "NOT", "ANSWER"], mist,
                    "NOT turns white into black and black into white, so the mist keeps the same two entries."),
        pick("Why did the black entries vanish when white | black went through H?",
             ["They canceled out (interference)", "Measuring removed them", "H deletes black shapes"], 0,
             "black and minus black canceled. That's interference."),
     ]},

    # ---------------- Unit 3 · Your first quantum trick ----------------
    {"title": "Game: Rigged or fair?",
     "steps": [
        play("The carnival machine",
             "A carnival machine has two buttons: a white one and a black one. Press a button and a light turns "
             "on or stays off.\n\n"
             "A rigged machine does the same thing whichever button you press. A fair machine does something "
             "different for each button. Your job: find out which kind it is."),
        predict("The normal way",
                "You're allowed to press buttons and watch the light.",
                ask("Without quantum tricks, how many presses do you need to be sure?", ["1", "2", "It's impossible"], 1,
                    "You have to try both buttons and compare. One press only tells you about one button.")),
        learn("The machine as a box",
              "In Qubi the machine is a mystery box. The circle is the button you press and the square is the "
              "light. The box flips the square for some buttons.\n\n"
              "A rigged box flips the square for both buttons or for neither. A fair box flips it for exactly one.",
              picture=run(make("circle square", "bw"), machine(FAIR_COPY)),
              note="This fair machine lights up for the black button."),
        learn("The quantum trick",
              "Put the circle through H so it presses both buttons at once. Start the square black and send it "
              "through H too. Use the machine once, then send the circle through H again and measure it.\n\n"
              "A white circle means rigged. A black circle means fair. Every time.",
              picture=run(make("circle square", "wb"), "H circle", "H square", machine(FAIR_COPY), "H circle"),
              note="For a fair machine, the circle comes out black."),
        play("Play it",
             "Each round, Qubi hides one of four machines: rigged off, rigged on, fair (black button) or fair "
             "(white button). Run the trick and read the circle.",
             try_it=measure({"Rigged: the light never changes": trick(RIGGED_OFF),
                             "Rigged: the light always flips": trick(RIGGED_ON),
                             "Fair: it lights up for the black button": trick(FAIR_COPY),
                             "Fair: it lights up for the white button": trick(FAIR_OPPOSITE)},
                            shapes=["circle"], times=1, button="Play a round",
                            labels={(0,): "The circle came out white, so the machine is rigged.",
                                    (1,): "The circle came out black, so the machine is fair."})),
        predict("Why it works",
                "Count how many times the trick used the machine.",
                ask("How many uses of the machine did the quantum trick need?", ["One", "Two", "Four"], 0,
                    "One use was enough: the mist pressed both buttons at once, and interference turned the answer "
                    "into one color. This idea is called Deutsch's algorithm, one of the first quantum algorithms.")),
     ],
     "quiz": [
        pick("In the trick, what does a black circle at the end mean?",
             ["The machine is fair", "The machine is rigged", "You need to try again"], 0,
             "Fair machines always turn the circle black. Rigged ones always leave it white."),
        pick("Why does the circle go through H before the machine?",
             ["So it presses both buttons at once", "To make the machine faster", "To hide the answer"], 0,
             "The mist lets one use of the machine check both buttons."),
        pick("How many uses of the machine does the quantum trick need?", ["1", "2", "3"], 0,
             "Just one, compared to two without the trick."),
     ]},

    {"title": "Build it in the Circuit Lab",
     "steps": [
        learn("Your own workbench",
              "The Circuit Lab lets you build any circuit you like. Pick your shapes, add boxes, and watch the "
              "mist change after every step."),
        learn("How to use it",
              "1. Click a shape on the left to switch it between white and black.\n\n"
              "2. Choose a box and the shapes it goes on, then press Add.\n\n"
              "3. Use the step buttons to see the mist after each box.\n\n"
              "4. Press Measure 100× to see what you'd really get."),
        predict("Plan a circuit",
                "You want a mist of a white circle and a black circle.",
                ask("Which single box do you add to a white circle?", ["NOT", "H", "SWAP"], 1,
                    "H turns a white circle into white | black.")),
        predict("Undo a mist",
                "You've got the mist from H.",
                ask("Which box turns it back into a plain white circle?", ["Another H", "NOT", "Measure"], 0,
                    "H undoes itself. Measuring would also end the mist, but you'd get a random color.")),
        learn("Try it now",
              "Open the Circuit Lab from the sidebar. Add H on the circle, then CNOT from the circle to the "
              "square, and look at the output. You'll find a mist that can't be split in two. You'll learn all "
              "about it in Unit 6.",
              picture=run(two_white, "H circle", "CNOT circle square")),
     ],
     "quiz": [
        pick("In the Circuit Lab, what does Measure 100× show?",
             ["The results of measuring the output 100 times", "100 copies of the circuit", "How long the circuit takes"], 0,
             "It measures the final mist 100 times and counts each result."),
        build_circuit("Make the mist white circle | black circle from a white circle.", ["H", "NOT"], ["H circle"], [white],
                      "One H box turns a white circle into white | black.", hint="Only one box is needed."),
        build_circuit("A white circle and a white square must both come out black.",
                      ["H", "NOT", "CNOT"], ["NOT circle", "NOT square"], [two_white],
                      "Two NOTs work. So does NOT on the circle followed by a CNOT from the circle to the square.",
                      hint="Flip the circle first, then think about CNOT."),
     ]},

    {"title": "Running on real quantum computers",
     "steps": [
        learn("Real qubits",
              "Real quantum computers exist today. Some store qubits in tiny superconducting circuits cooled to "
              "colder than outer space. Others use single atoms held in place by lasers.\n\n"
              "IBM lets anyone run small circuits on its machines over the internet for free."),
        learn("Noise",
              "Real qubits are fragile. Heat, vibration and stray signals nudge them, so real results are a bit "
              "messy. A perfect 50/50 might come back as 52/48, and a result that should never happen might show "
              "up a few times."),
        predict("Reading real results",
                "You run H on a white circle 1,000 times on a real machine.",
                ask("Which result looks the most realistic?",
                    ["White 500, black 500 exactly", "White 512, black 488", "White 1,000, black 0"], 1,
                    "Randomness plus noise means you'll land close to 50/50, but almost never exactly.")),
        learn("Export to IBM",
              "In the Circuit Lab, press Export to IBM. Qubi writes your circuit in OpenQASM, the language IBM's "
              "machines read.\n\n"
              "Copy the code, open IBM Quantum Composer, paste it into the code editor, and run it."),
        learn("Qubi names and IBM names",
              "Your boxes have standard names: NOT is x, H is h, Z is z, CNOT is cx, Control-Z is cz, SWAP is "
              "swap and Toffoli is ccx.\n\n"
              "IBM's qubits all start as 0, which is our white shape. If a shape starts black, Qubi adds an x "
              "box at the start for you."),
     ],
     "quiz": [
        pick("Why aren't real results exactly 50/50?", ["Randomness and noise", "The computer is broken", "IBM changes them"], 0,
             "Each run is random, and real qubits are nudged by noise."),
        pick("What is the CNOT box called in OpenQASM?", ["cx", "not", "swap"], 0, "CNOT is written cx."),
        pick("In IBM Quantum Composer, every qubit starts as…", ["0, a white shape", "1, a black shape", "A mist"], 0,
             "Every qubit starts as 0, like a white shape."),
     ]},

    # ---------------- Unit 4 · More gates ----------------
    {"title": "The Z box and Control-Z",
     "steps": [
        learn("The Z box",
              "The Z box leaves white entries alone and puts a minus sign on black ones.",
              picture=run(mist, "Z circle"), note="Z puts a minus on the black entry."),
        predict("Z on a plain shape",
                "A black circle goes into Z and comes out as minus black circle.",
                ask("Did anything really change?", ["No, an overall minus doesn't matter", "Yes, it's a new color"], 0,
                    "A lone shape with a minus is the same as without one (tidy rule 3). Z only shows its effect "
                    "inside a mist.")),
        learn("Building Z from other boxes",
              "Boxes can be built from other boxes. H, then NOT, then H does exactly what Z does.",
              picture=run(mist, "H circle", "NOT circle", "H circle"), note="Same result as Z: white | minus black."),
        learn("Control-Z",
              "Control-Z takes two shapes. It puts a minus sign on an entry only when both shapes in it are black.",
              picture=run(two_white, "H circle", "H square", "CZ circle square"),
              note="Only the black-black entry gets a minus."),
        predict("Which way round?",
                "CNOT has a control and a target. What about Control-Z?",
                ask("Does it matter which shape is the control in Control-Z?",
                    ["No, it only checks if both are black", "Yes, it works differently"], 0,
                    "Control-Z only asks whether both shapes are black, so swapping them changes nothing.")),
     ],
     "quiz": [
        build_circuit("Make the Z box using only H and NOT boxes.", ["H", "NOT"], ["Z circle"],
                      [white, black, mist, minus_mist],
                      "H, NOT, H does the same as Z on every input.",
                      hint="Sandwich a NOT between two H boxes."),
        build_state("white circle | black circle goes into Z. What comes out?", [mist, "Z", "ANSWER"], minus_mist,
                    "Z puts a minus on the black entry."),
        pick("Control-Z adds a minus sign when…", ["Both shapes are black", "Either shape is black", "Both shapes are white"], 0,
             "Only the entries where both shapes are black get a minus."),
     ]},

    {"title": "The Toffoli box",
     "steps": [
        learn("Two controls",
              "The Toffoli box has three pegs: two controls and a target. It flips the target only when both "
              "controls are black.",
              picture=run(make("circle square triangle", "bbw"), "TOFFOLI circle square triangle")),
        predict("One control black",
                "Circle black, square white, triangle white.",
                ask("What comes out of the Toffoli box?", ["Nothing changes", "The triangle flips to black", "Every shape flips"], 0,
                    "Both controls have to be black. The square is white, so nothing flips."),
                picture=[make("circle square triangle", "bww"), "TOFFOLI", "ANSWER"]),
        learn("It computes AND",
              "Start the triangle white. Afterward it's black only if the circle AND the square are black.\n\n"
              "That's the AND gate inside every normal computer, and with it a quantum computer can do anything a "
              "normal computer can."),
        learn("Nothing gets lost",
              "A normal AND gate throws information away: from its answer you can't tell what went in. The "
              "Toffoli box keeps both controls, so it can always be run backwards. Every quantum box has to be "
              "reversible like this."),
        predict("Toffoli twice",
                "Put two Toffoli boxes in a row.",
                ask("What happens?", ["Everything goes back to how it started", "The triangle is always black", "The circle flips"], 0,
                    "The second Toffoli flips the triangle back whenever the first one flipped it.")),
     ],
     "quiz": [
        build_state("A black circle, black square and black triangle go into Toffoli. What comes out?",
                    [make("circle square triangle", "bbb"), "TOFFOLI", "ANSWER"], make("circle square triangle", "bbw"),
                    "Both controls are black, so the triangle flips from black to white."),
        pick("With the triangle starting white, when does Toffoli turn it black?",
             ["When the circle AND the square are black", "When the circle OR the square is black", "Never"], 0,
             "Toffoli computes AND."),
        build_circuit("Make the triangle black only when the circle and the square are both black. The triangle starts white.",
                      ["NOT", "CNOT", "TOFFOLI"], ["TOFFOLI circle square triangle"],
                      [make("circle square triangle", combo) for combo in ["www", "wbw", "bww", "bbw"]],
                      "One Toffoli box with the circle and square as controls does it.", hint="This is AND."),
     ]},

    # ---------------- Unit 5 · The game show ----------------
    {"title": "Game: The silent alarm",
     "steps": [
        play("The vault",
             "A museum vault might be guarded by a laser alarm. If the alarm is there and anything passes through "
             "the vault, it goes off.\n\n"
             "Can you find out whether the alarm is there without ever setting it off? It sounds impossible."),
        learn("Two paths",
              "Send a white circle through H. Its mist has two entries: white means it took the safe hallway, "
              "black means it went through the vault.\n\n"
              "If the vault is empty, a second H turns the mist back into a plain white circle.",
              picture=run(white, "H circle", "H circle"), note="Empty vault: always a white circle."),
        learn("When the alarm is there",
              "An alarm notices anything that passes through. We show that with a square that flips when the "
              "circle is black: a CNOT. Now the second H can't undo the mist.",
              picture=run(two_white, "H circle", "CNOT circle square", "H circle"),
              note="Four entries now, each with a 25% chance."),
        predict("Reading the results",
                "Remember: with an empty vault, the circle always comes out white.",
                ask("With the alarm there, which result proves it exists without setting it off?",
                    ["A black square", "A black circle with a white square", "A white circle with a white square"], 1,
                    "An empty vault never gives a black circle, so a black circle proves the alarm is there. The white "
                    "square means it never went off.")),
        play("Play it",
             "Each round, Qubi secretly picks an empty vault or a guarded one. Send your circle through and read "
             "what comes out.",
             try_it=measure({"The vault was empty.": no_alarm, "The alarm was there.": alarm},
                            times=1, button="Play a round",
                            labels={(0, 0): "White circle, white square: no proof yet. Try again.",
                                    (1, 0): "Black circle, white square: the alarm is there, and it never went off!",
                                    (0, 1): "Black square: the alarm went off. Busted!",
                                    (1, 1): "Black square: the alarm went off. Busted!"})),
        learn("This is real science",
              "This trick is a real experiment called interaction-free measurement. Physicists have detected objects "
              "with light that never touched them. Smarter versions push the chance of setting off the alarm close "
              "to zero."),
     ],
     "quiz": [
        pick("If the vault is empty, what comes out after H, the vault and H again?",
             ["Always a white circle", "Always a black circle", "White or black, 50/50"], 0,
             "H twice gives back the white circle."),
        pick("With the alarm there, what's the chance of finding it safely in one try?", ["25%", "50%", "100%"], 0,
             "One of the four equal entries is black circle with white square: 25%."),
        pick("What does the square stand for?", ["The alarm noticing the circle", "A museum guard", "The exit door"], 0,
             "The square flips when the circle passes through the vault, like an alarm noticing it."),
     ]},

    {"title": "Game: Find the gem",
     "steps": [
        play("Four lockers",
             "A gem is hidden in one of four lockers. Each locker has a code made of two shapes: white-white, "
             "white-black, black-white or black-black.\n\n"
             "Peeking one locker at a time could take up to 3 peeks to be sure. A quantum search needs just 1."),
        learn("Check every locker at once",
              "Send a white circle and a white square through H boxes. The mist now holds all four codes at once.",
              picture=run(two_white, "H circle", "H square")),
        learn("The marker box",
              "The game master's marker box puts a minus sign on the code of the locker with the gem. Measuring now "
              "wouldn't help: minus signs don't change the chances, so each code is still 25%.",
              picture=run(all_lockers, ("?", MARKERS["bw"])), note="Here the gem is in the black-white locker."),
        learn("The flip box",
              "Next comes a set of boxes we'll call the flip box: H, NOT, Control-Z, NOT and H on both shapes. "
              "It flips every entry around the average, so the marked entry grows and the others cancel out.",
              picture=[run(all_lockers, ("?", MARKERS["bw"]))[-1], "F", make("circle square", "bw")],
              note="Only the gem's code is left."),
        play("Play it",
             "Each round, Qubi hides the gem in a random locker. Run the search once and open the locker it points to.",
             try_it=measure({f"The gem was in the {name} locker.": flip_around(MARKERS[code](all_lockers.copy()))
                             for code, name in LOCKER_NAMES.items()},
                            times=1, button="Play a round",
                            labels={(0, 0): "The search says: white-white.", (0, 1): "The search says: white-black.",
                                    (1, 0): "The search says: black-white.", (1, 1): "The search says: black-black."})),
        predict("How many peeks?",
                "Count how many times the search used the marker box.",
                ask("How many times did the quantum search use the marker box?", ["Once", "Twice", "Four times"], 0,
                    "Once was enough for four lockers. This is Grover's search. For a million lockers it needs about "
                    "800 uses instead of up to a million peeks.")),
     ],
     "quiz": [
        pick("What does the marker box do?", ["Puts a minus on the gem's code", "Opens the locker", "Measures the shapes"], 0,
             "It marks the gem's code with a minus sign."),
        pick("Right after the marker box, what's the chance of measuring the gem's code?", ["25%", "50%", "100%"], 0,
             "Minus signs don't change chances, so it's still 25%."),
        pick("After the flip box, what's the chance of measuring the gem's code?", ["25%", "75%", "100%"], 2,
             "The other codes cancel out, leaving only the gem's code."),
     ]},

    # ---------------- Unit 6 · Entanglement at work ----------------
    {"title": "Linked mists",
     "steps": [
        learn("Two shapes, one mist",
              "Send a white circle through H, then use CNOT with the circle as the control. The result is a mist "
              "where the circle and the square always match.",
              picture=run(two_white, "H circle", "CNOT circle square")),
        predict("Measure just one",
                "You measure only the circle and see black.",
                ask("What is the square now?", ["Black", "White", "Still a mist"], 0,
                    "Every entry has matching colors, so once the circle is black, the square has to be black too.")),
        learn("Entangled",
              "This mist can't be split into one mist for the circle and a separate mist for the square. Shapes "
              "like this are entangled. Measuring one tells you about the other, even if they're far apart."),
        learn("Four linked pairs",
              "There are four basic entangled pairs, called Bell pairs. You get each one by changing the starting "
              "colors before H and CNOT.",
              picture=together(make("circle square", "ww", "bb"), make("circle square", "ww", "-bb"),
                               make("circle square", "wb", "bw"), make("circle square", "wb", "-bw"))),
        learn("Measure the pair",
              "Measure both shapes 10 times. Look at the results: they always match.",
              try_it=measure(bell)),
     ],
     "quiz": [
        build_state("A black circle and a white square go through H on the circle, then CNOT. What comes out?",
                    [make("circle square", "bw"), "H", "CNOT", "ANSWER"], make("circle square", "ww", "-bb"),
                    "H gives white-white | minus black-white, then CNOT flips the square in the black entry.",
                    hint="Do H first, then CNOT on each entry."),
        pick("What does entangled mean?",
             ["The mist can't be split into separate mists for each shape", "The shapes are tied together",
              "The shapes are always black"], 0,
             "Entangled shapes share one mist that can't be pulled apart."),
        build_circuit("From two white shapes, make the pair white-black | black-white.", ["H", "NOT", "CNOT"],
                      ["NOT square", "H circle", "CNOT circle square"], [two_white],
                      "Make the square black first, then use H and CNOT.", hint="Change a starting color first."),
     ]},

    {"title": "Teleporting a mist",
     "steps": [
        learn("The goal",
              "Alice has a circle in a mist that she wants to give to Bob. She can't send the shape itself, and "
              "measuring it would destroy the mist.\n\n"
              "Teleportation moves the mist using a linked pair and two plain colors sent as a message.",
              picture=[minus_mist], note="The mist Alice wants to send."),
        learn("Share a linked pair",
              "First Alice and Bob make a linked pair. Alice keeps the square and Bob takes the triangle.",
              picture=run(make("square triangle", "ww"), "H square", "CNOT square triangle")),
        learn("Alice's moves",
              "Alice sends her circle and square through CNOT (circle as control), then the circle through H. "
              "Then she measures both and texts Bob the two colors she saw."),
        predict("Bob's fix",
                "Bob's triangle is now close to Alice's mist. He fixes it using her message: if the square was "
                "black he uses NOT, and if the circle was black he uses Z.",
                ask("Alice saw a white circle and a white square. What does Bob do?",
                    ["Nothing: his triangle already holds the mist", "NOT", "NOT and Z"], 0,
                    "With two whites, no fix is needed. Bob's triangle already holds the mist.")),
        play("Try it",
             "Each round, Alice measures for real. Qubi shows what she saw and how Bob fixes his triangle. Every "
             "time, Bob ends up with white | minus black.",
             try_it=measure(after_alice, shapes=["circle", "square"], times=1, button="Teleport it",
                            labels={(0, 0): "Alice saw white, white. Bob does nothing.",
                                    (0, 1): "Alice saw white, black. Bob uses NOT.",
                                    (1, 0): "Alice saw black, white. Bob uses Z.",
                                    (1, 1): "Alice saw black, black. Bob uses NOT, then Z."})),
        learn("Not faster than light",
              "Bob needs Alice's message before he can fix his triangle, and messages travel no faster than light. "
              "Alice's circle lost its mist when she measured it, so the mist was moved, not copied."),
     ],
     "quiz": [
        pick("What does Alice send to Bob?", ["Two colors (two plain bits)", "Her circle", "A copy of the mist"], 0,
             "She sends just the two colors she measured."),
        pick("Alice saw a black circle and a white square. What should Bob use?", ["Z", "NOT", "Nothing"], 0,
             "A black circle means Z. A white square means no NOT."),
        pick("After teleporting, does Alice still have the mist?", ["No, measuring ended it", "Yes, now there are two copies"], 0,
             "Quantum mists can't be copied. Alice's mist ended when she measured."),
     ]},
]