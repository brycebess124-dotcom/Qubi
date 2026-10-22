# Welcome page: the first page people see, before they log in. One short scroll: what Qubi is, why quantum
# computing matters now, our mission, how Qubi teaches, the course, and a last nudge to sign up.
# Every number on the page has a source, listed at the bottom. The styles are in engine/landing.py.

import streamlit as st
import course
from engine.qubits import make, run
from engine.ui import picture, as_image, draw_state
from engine.parts import logo, icon
from engine.landing import style, trip, accent, PHOTO_BY, PHOTO_PAGE


def open_account():
    """Goes to the sign in page (Google, or try it as a guest)."""
    st.switch_page("pages/account.py")


def cite(number):
    """A small source number that jumps to the list at the bottom of the page."""
    return f'<sup><a href="#source-{number}">{number}</a></sup>'


def dotted(number):
    """A big number in the dot font. Its decimal point looks like a +, so the point uses the normal font,
    and long numbers may only break after a comma."""
    return number.replace(".", '<span class="lp-point">.</span>').replace(",", ",<wbr>")


SOURCES = [   # who, title, date, link
    ("Google", "Meet Willow, our state-of-the-art quantum chip", "December 9, 2024",
     "https://blog.google/technology/research/google-willow-quantum-chip/"),
    ("McKinsey & Company", "McKinsey Quantum Technology Monitor 2026: A commercial tipping point", "April 28, 2026",
     "https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/"
     "mckinsey-quantum-technology-monitor-2026-a-commercial-tipping-point"),
    ("The Quantum Insider", "IBM offers roadmap toward large-scale, fault-tolerant quantum computer", "June 10, 2025",
     "https://thequantuminsider.com/2025/06/10/"
     "ibm-offers-roadmap-toward-large-scale-fault-tolerant-quantum-computer-at-new-ibm-quantum-data-center/"),
    ("NIST", "NIST releases first 3 finalized post-quantum encryption standards", "August 13, 2024",
     "https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards"),
    ("McKinsey & Company", "Five lessons from AI on closing quantum's talent gap, before it's too late", "December 1, 2022",
     "https://www.mckinsey.com.br/capabilities/tech-and-ai/our-insights/"
     "five-lessons-from-ai-on-closing-quantums-talent-gap-before-its-too-late"),
]

STOPS = ["A qubit: white means 0", "The H gate", "Now it's a superposition", "Measure it", "White or black, 50/50"]

STATS = [("$2.7T", f"Value quantum computing could create worldwide by 2035, at the top of McKinsey's range{cite(2)}"),
         ("$12.6B", f"Invested in quantum start-ups in 2025, 6.3 times more than in 2024{cite(2)}"),
         ("2029", f"When IBM plans to deliver Starling, a large quantum computer that corrects its own errors{cite(3)}")]

USES = [("molecule", "Medicine and materials",
         "Molecules follow quantum rules, so quantum computers could simulate them in ways today's computers can't. "
         "That could help design new medicines, batteries and fertilizers."),
        ("lock", "Online security",
         "A big enough quantum computer could break the encryption that protects much of the internet. In 2024, NIST "
         f"released the first encryption standards built to stand up to quantum computers.{cite(4)}"),
        ("route", "Planning, finance and AI",
         "Researchers are testing quantum methods on hard planning and prediction problems. Some will work and some "
         "won't, and knowing how qubits work is how you tell the difference.")]

JOBS = ["Quantum software engineer", "Cryptographer", "Chemist", "Materials scientist", "Hardware engineer",
        "Data scientist", "Research scientist"]

white = make("circle", "w")
STEPS = [("Shapes are qubits", "A white shape means 0 and a black shape means 1, like the bits inside every computer.",
          picture([white, make("square", "b")], arrows=False)),
         ("Gates change them", "A gate is a box that changes shapes. NOT flips white to black, and CNOT flips one shape "
                               "only when another is black.",
          picture(run(white, "NOT circle"), across=True)),
         ("Clouds are superpositions", "The H gate puts a shape in a cloud. Measure it and you see white or black, and "
                                       "other gates can make those chances cancel out or add up.",
          picture([run(white, "H circle")[-1]]))]

FEATURES = [("A quiz after every lesson", "Three questions, like the practice problems in a textbook"),
            ("A test after every unit", f"Pass with {course.PASS_MARK}% to unlock the next unit"),
            ("The Circuit Lab", "Build your own circuits and watch the cloud change"),
            ("Streaks, XP and achievements", "Small daily goals that add up")]

NEEDS = ["Adding and multiplying", "A phone, tablet or computer", f"About {course.MINUTES_PER_LESSON} minutes a lesson"]

CREDIT = ("Qubi is built on the ideas in the Virginia Tech Quantum Information Science and Engineering Summer School "
          "notes by Sophia Economou, Edwin Barnes and Jamie Sikora, and in <i>Q is for Quantum</i> by Terry Rudolph. "
          "The lessons are written in our own words, the pictures and games are our own, and Qubi isn't connected to or "
          "endorsed by these authors or by Virginia Tech.")

st.html(style())

# ---------------- top bar ----------------
with st.container(key="lp_nav", horizontal=True, vertical_alignment="center"):
    st.html(logo(118), width="content")
    st.space("stretch")
    st.html('<nav class="lp-links"><a href="#why">Why quantum</a><a href="#how">How it works</a>'
            '<a href="#course">The course</a></nav>', width="content")
    if st.button("Sign in", key="top_log_in"):
        open_account()

# ---------------- the big idea, and a qubit's trip on paper ----------------
st.html('<h1 class="lp-h1">Quantum computing, for the generation that will build it.</h1>')
pitch, buttons = st.columns([1.7, 1], gap="large", vertical_alignment="bottom")
pitch.html(f'<p class="lp-lead">Qubi teaches qubits, gates and superposition with shapes instead of equations. '
           f'{course.TOTAL_LESSONS} short lessons take you from your first bit to quantum teleportation. '
           f"It's free and made for total beginners.</p>")
with buttons.container(key="lp_start", horizontal=True, horizontal_alignment="right"):
    if st.button("Get started", type="primary"):
        open_account()
    if st.button("I have an account"):
        open_account()

stops = "".join(f"<span>{stop}</span>" for stop in STOPS)
st.html(f'''
<div class="lp-stage">
    <div class="lp-wide">{trip()}<div class="lp-stops">{stops}</div></div>
    <div class="lp-tall">{trip(vertical=True)}<div class="lp-stops">{stops}</div></div>
    <p class="lp-stage-note">That's three lessons of Qubi in one picture. Inside, you'll find out why the cloud is more
        than a coin flip.</p>
</div>''')

# ---------------- why quantum, why now ----------------
stats = "".join(f'<div><span class="lp-num">{dotted(number)}</span><p>{text}</p></div>' for number, text in STATS)
uses = "".join(f'<div><span class="lp-icon">{icon(name, accent("link"), 30, 1.8)}</span><h4 class="lp-h3">{title}</h4>'
               f'<p class="lp-text">{text}</p></div>' for name, title, text in USES)
st.html(f'''
<section id="why" class="lp-section lp-band">
    <h2 class="lp-h2">Why learn quantum now?</h2>
    <p class="lp-intro">Quantum computers use the rules of atoms and light to solve some problems in a completely new
        way. They're leaving research labs and moving into real companies.</p>
    <div class="lp-race">
        <div class="lp-race-row">
            <span class="lp-race-unit">Under</span><span class="lp-num lp-fast">5</span><span class="lp-race-unit">minutes</span>
            <p>Google's Willow quantum chip, on a test problem in December 2024{cite(1)}</p>
        </div>
        <div class="lp-race-row">
            <span class="lp-num">{dotted("10,000,000,000,000,000,000,000,000")}</span><span class="lp-race-unit">years</span>
            <p>How long one of today's fastest supercomputers would need for the same problem{cite(1)}</p>
        </div>
        <p class="lp-fine">The problem was made to test the chip, not to do useful work. The race now is to build
            quantum computers big and reliable enough for real problems.</p>
    </div>
    <div class="lp-stats">{stats}</div>
    <h3 class="lp-h3" style="margin-top:88px; font-size:24px">What it could change</h3>
    <div class="lp-uses" style="margin-top:28px">{uses}</div>
</section>''')

# ---------------- our mission ----------------
jobs = "".join(f"<li>{job}</li>" for job in JOBS)
st.html(f'''
<section id="mission" class="lp-section lp-split">
    <figure class="lp-photo" role="img" aria-label="A snow leopard">
        <figcaption>Photo: {PHOTO_BY}, Unsplash</figcaption>
    </figure>
    <div class="lp-mission">
        <h2 class="lp-h2">Empowering the next generation to learn quantum computing</h2>
        <p>Snow leopards are called the ghosts of the mountains because so few people ever see one. People who
            understand quantum computers can be almost as hard to find. In 2022, McKinsey found about one qualified
            candidate for every three quantum job openings.{cite(5)}</p>
        <p>Most people don't meet quantum computing until college, if they meet it at all. Qubi starts it earlier: if
            you can add and multiply, you can learn how a qubit works, today and for free.</p>
        <p>Quantum skills lead to jobs like these:</p>
        <ul class="lp-jobs">{jobs}</ul>
    </div>
</section>''')

# ---------------- how Qubi teaches ----------------
steps = "".join(f'<li>{drawing}<div class="lp-step-title"><span class="lp-step-n">{number}</span>'
                f'<h3 class="lp-h3">{title}</h3></div><p class="lp-text">{text}</p></li>'
                for number, (title, text, drawing) in enumerate(STEPS, start=1))
features = "".join(f"<li><b>{title}</b><span>{text}</span></li>" for title, text in FEATURES)
st.html(f'''
<section id="how" class="lp-section">
    <h2 class="lp-h2">How Qubi teaches</h2>
    <p class="lp-intro">Every idea is a picture you can play with. No physics, no coding and no heavy math.</p>
    <ol class="lp-steps">{steps}</ol>
    <ul class="lp-features">{features}</ul>
</section>''')

# ---------------- the course ----------------
units = "".join(f'<li><span class="lp-stop" style="animation-range: contain {i * 10}% contain {i * 10 + 4}%">{i + 1}</span>'
                f'<div><b>{unit["title"]}</b><small>{len(unit["lessons"])} lessons</small></div></li>'
                for i, unit in enumerate(course.UNITS))
st.html(f'''
<section id="course" class="lp-section">
    <h2 class="lp-h2">From your first bit to teleportation</h2>
    <p class="lp-intro">{len(course.UNITS)} units and {course.TOTAL_LESSONS} lessons, about {course.MINUTES_PER_LESSON}
        minutes each. Every unit ends with a test, and a final test covers it all.</p>
    <div class="lp-track"><div class="lp-wire"><span></span></div><ol class="lp-units">{units}</ol></div>
</section>''')

# ---------------- sign up ----------------
needs = "".join(f'<li>{icon("check", "#FFFFFF", 20, 2.6)}{need}</li>' for need in NEEDS)
with st.container(key="lp_cta"):
    st.html(f'''
    <h2 class="lp-cta-title">Start with one bit.</h2>
    <p class="lp-cta-text">It's free, and there's nothing to buy or install. All you need:</p>
    <ul class="lp-needs">{needs}</ul>
    <div class="lp-bit">{as_image(draw_state(white, 120))}</div>''')
    if st.button("Create your free account", type="primary", key="bottom_sign_up"):
        open_account()

# ---------------- credits and sources ----------------
sources = "".join(f'<li id="source-{number}">{who}, "{title}," {date}. '
                  f'<a href="{link}" target="_blank">{link.split("/")[2].removeprefix("www.")}</a></li>'
                  for number, (who, title, date, link) in enumerate(SOURCES, start=1))
st.html(f'''
<footer class="lp-footer">
    <div>
        {logo(96)}
        <p class="lp-motto">Empowering the next generation to learn quantum computing.</p>
        <p style="margin-top:8px">Made for the 2026 Congressional App Challenge.</p>
    </div>
    <div>
        <p>{CREDIT}</p>
        <p style="margin-top:22px; color:var(--strong); font-weight:600">Sources</p>
        <ol class="lp-sources">{sources}</ol>
        <p style="margin-top:10px; font-size:13px">Snow leopard photo by {PHOTO_BY} on
            <a href="{PHOTO_PAGE}" target="_blank">Unsplash</a>.</p>
    </div>
</footer>''')