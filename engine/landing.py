# The welcome page's look: its styles and the animated picture at the top.
# The words are in pages/welcome.py.

from engine.qubits import make, apply
from engine.ui import SVG, BLACK, as_image, draw_column, draw_state, theme

# The snow leopard photo, free to use under the Unsplash License. To swap it, change all three.
PHOTO = "https://images.unsplash.com/photo-1546977532-4a61683ea4a0?auto=format&fit=crop&w=1000&q=70"
PHOTO_BY = "Helena Lopes"
PHOTO_PAGE = "https://unsplash.com/photos/shallow-focus-photo-of-snow-leopard-YShS0gEZSB4"


# ================= the qubit's trip (top of the page) =================

def trip(vertical=False):
    """The moving picture, plus a still one for people whose device asks for less motion (the styles pick one)."""
    return (f'<span class="lp-moving">{journey(vertical)}</span>'
            f'<span class="lp-still">{journey(vertical, moving=False)}</span>')


def journey(vertical=False, moving=True):
    """A qubit's trip along a wire, on a loop: a white circle goes through the H gate and turns into a cloud
    (a superposition), the cloud gets measured, and the result is white the first time round and black the next.
    vertical=True draws it top to bottom, for phones. moving=False shows every step at once, standing still."""
    gap, start, middle = (160, 80, 110) if vertical else (200, 100, 80)
    width, height = (220, 800) if vertical else (1000, 160)

    def spot(stop):                                    # the middle of each stop on the wire, 0 to 4
        along = start + gap * stop
        return (middle, along) if vertical else (along, middle)

    def place(drawing, size, stop):                    # a drawing centered on a stop
        x, y = spot(stop)
        return f'<g transform="translate({x - size[0] / 2} {y - size[1] / 2})">{drawing}</g>'

    move = f"0px, {gap}px" if vertical else f"{gap}px, 0px"           # one stop further along
    move2 = f"0px, {2 * gap}px" if vertical else f"{2 * gap}px, 0px"   # two stops further along
    white, black = make("circle", "w"), make("circle", "b")
    cloud = apply(white, "H circle")
    (x0, y0), (x4, y4) = spot(0), spot(4)
    (x1, y1), (x3, y3) = spot(1), spot(3)

    still = f".b {{ transform: translate({move}); }} .k {{ opacity: 0; }}"   # circle, cloud and result all showing
    style = f"""
    .a, .b, .gate, .needle, .w, .k {{ transform-box: fill-box; transform-origin: center; }}
    .needle {{ transform-origin: 50% 100%; }}
    .a {{ animation: a 8s infinite both; }}       .b {{ animation: b 8s infinite both; }}
    .gate {{ animation: gate 8s infinite both; }} .needle {{ animation: needle 8s infinite both; }}
    .w {{ animation: w 16s infinite both; }}      .k {{ animation: k 16s infinite both; }}
    @keyframes a {{ 0% {{ opacity: 0; transform: translate(0px, 0px); }}  6% {{ opacity: 1; transform: translate(0px, 0px); }}
                   25% {{ opacity: 1; transform: translate({move}) scale(1); }}
                   29%, 100% {{ opacity: 0; transform: translate({move}) scale(.4); }} }}
    @keyframes gate {{ 0%, 23% {{ transform: scale(1); }} 28% {{ transform: scale(1.14); }} 34%, 100% {{ transform: scale(1); }} }}
    @keyframes b {{ 0%, 26% {{ opacity: 0; transform: translate(0px, 0px) scale(.5); }}
                   32% {{ opacity: 1; transform: translate(0px, 0px) scale(1); }}
                   45%, 56% {{ opacity: 1; transform: translate({move}) scale(1); }}
                   66% {{ opacity: 1; transform: translate({move2}) scale(1); }}
                   71%, 100% {{ opacity: 0; transform: translate({move2}) scale(.4); }} }}
    @keyframes needle {{ 0%, 64% {{ transform: rotate(-50deg); }} 69% {{ transform: rotate(48deg); }}
                        73% {{ transform: rotate(-16deg); }} 77%, 93% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(-50deg); }} }}
    @keyframes w {{ 0%, 35% {{ opacity: 0; transform: scale(.4); }} 38%, 46% {{ opacity: 1; transform: scale(1); }}
                   49%, 100% {{ opacity: 0; transform: scale(.4); }} }}
    @keyframes k {{ 0%, 85% {{ opacity: 0; transform: scale(.4); }} 88%, 96% {{ opacity: 1; transform: scale(1); }}
                   99%, 100% {{ opacity: 0; transform: scale(.4); }} }}
    """

    meter = (f'<g transform="translate({x3} {y3}) scale(1.6)">'
             f'<rect x="-17" y="-17" width="34" height="34" rx="7" fill="#3F3F46" stroke="{BLACK}"/>'
             f'<path d="M-9 5A9 9 0 0 1 9 5" fill="none" stroke="#F4F4F5" stroke-width="2"/>'
             f'<path class="needle" d="M0 5V-7" stroke="#F4F4F5" stroke-width="2" stroke-linecap="round"/></g>')
    slot = (f'<rect x="{x4 - 31}" y="{y4 - 31}" width="62" height="62" rx="14" fill="none" stroke="#71717A" '
            f'stroke-width="2.5" stroke-dasharray="7 6"/>'
            f'<text x="{x4}" y="{y4 + 9}" text-anchor="middle" font-family="sans-serif" font-size="26" '
            f'font-weight="700" fill="#71717A">?</text>')
    ends = (f"M{x0} {y0 - 60}L{x4} {y4 + 60}" if vertical else f"M{x0 - 70} {y0}L{x4 + 70} {y4}")
    parts = [
        f'<path d="{ends}" stroke="#52525B" stroke-width="2.5"/>',                     # the wire
        slot,
        place(f'<g class="a">{draw_state(white, 44)}</g>', (48, 48), 0),             # the white circle
        place(f'<g class="b">{draw_state(cloud, 44)}</g>', (166, 96), 1),            # the cloud, starting at the H gate
        f'<g transform="translate({x1} {y1}) scale(1.5)"><g class="gate">{draw_column("H", [(0, 0)])}</g></g>',
        meter,
        place(f'<g class="w">{draw_state(white, 44)}</g>', (48, 48), 4),             # first time round: white
        place(f'<g class="k">{draw_state(black, 44)}</g>', (48, 48), 4),             # second time round: black
    ]
    size = 'width="130" height="473"' if vertical else 'width="1000" height="160"'
    return as_image(f'<svg {SVG} viewBox="0 0 {width} {height}" {size}><style>{style if moving else still}</style>'
                    f'{"".join(parts)}</svg>',
                    alt="A white circle goes through an H gate and becomes a cloud of a white and a black circle. "
                        "Measuring the cloud gives white or black.")


# ================= styles (only on the welcome page) =================

ACCENTS = {   # colors that need to change with the theme to stay easy to read
    "dark": {"band": "#10151F", "fast": "#22D3EE", "link": "#A78BFA"},
    "light": {"band": "#FFFFFF", "fast": "#0E7490", "link": "#6D28D9"},
}


def accent(name):
    return ACCENTS[theme()][name]


def style():
    colors = "".join(f"--lp-{name}: {value}; " for name, value in ACCENTS[theme()].items())
    return "<style>:root { " + colors + "}" + CSS + "</style>"


CSS = """
/* page: dotted like graph paper, a little wider than other pages */
.stApp { background-image: radial-gradient(rgba(139,139,148,0.16) 1px, transparent 1.5px); background-size: 46px 46px; }
.stApp .block-container { max-width: 1220px; }
[data-testid="stMain"], [data-testid="stAppViewContainer"] { scroll-behavior: smooth; }
.stApp .lp-section a:focus-visible, .stApp .lp-links a:focus-visible { outline: 2px solid #22D3EE; outline-offset: 3px; border-radius: 6px; }

/* top bar */
.st-key-lp_nav { padding-bottom: 8px; }
.stApp .lp-links { display: flex; gap: 30px; margin-right: 12px; }
.stApp .lp-links a { color: var(--soft); font-size: 15px; font-weight: 500; }
.stApp .lp-links a:hover { color: var(--strong); }

/* words */
.stApp .lp-h1 { margin: 0; padding: 60px 0 0; color: var(--strong); font-size: clamp(42px, 5.6vw, 78px); font-weight: 700;
                line-height: 1.0; letter-spacing: -0.04em; text-wrap: balance; }
.stApp .lp-lead { margin: 0; padding-top: 22px; color: var(--soft); font-size: 19px; line-height: 1.6; max-width: 34em; }
.stApp .lp-point { font-weight: 700; }
.stApp .lp-h2 { margin: 0; padding: 0; color: var(--strong); font-size: clamp(32px, 3.8vw, 48px); font-weight: 700;
                line-height: 1.06; letter-spacing: -0.03em; text-wrap: balance; max-width: 17em; }
.stApp .lp-h3 { margin: 0; padding: 0; color: var(--strong); font-size: 20px; font-weight: 600; line-height: 1.3; }
.stApp .lp-intro { margin: 18px 0 0; color: var(--soft); font-size: 19px; line-height: 1.6; max-width: 34em; }
.stApp .lp-text { margin: 0; color: var(--text); font-size: 16px; line-height: 1.6; }
.stApp .lp-num { font-family: 'Doto', monospace !important; font-weight: 900; color: var(--strong); line-height: 1; }
.stApp .lp-section sup { font-size: 0.65em; line-height: 0; margin-left: 2px; }
.stApp .lp-section sup a { color: var(--lp-link); font-weight: 600; }
.stApp .lp-section { padding-top: 128px; scroll-margin-top: -64px; }      /* menu links land just above the heading */

/* the qubit's trip, on paper */
.stApp .lp-stage { margin-top: 26px; border-radius: 32px; padding: 30px 26px 24px; color: #18181B;
                   border: 1px solid rgba(24,24,27,0.07);
                   background: #F6F5F1 radial-gradient(rgba(24,24,27,0.09) 1px, transparent 1px); background-size: 18px 18px; }
.stApp .lp-stage img { display: block; width: 100%; height: auto; }
.stApp .lp-stops { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); margin-top: 8px; }
.stApp .lp-stops span { text-align: center; color: #3F3F46; font-size: 15px; font-weight: 500; padding: 0 6px; }
.stApp .lp-stage-note { margin: 20px 0 0; text-align: center; color: #52525B; font-size: 14px; }
.stApp .lp-tall, .stApp .lp-still { display: none; }
.stApp .lp-moving { display: block; }
@media (prefers-reduced-motion: reduce) { .stApp .lp-moving { display: none; } .stApp .lp-still { display: block; } }

/* why now: a darker stripe across the whole window */
.stApp .lp-band { margin-top: 128px; padding: 112px 0 116px; background: var(--lp-band);
                  box-shadow: 0 0 0 100vmax var(--lp-band); clip-path: inset(0 -100vmax); }
.stApp .lp-race { margin-top: 56px; display: flex; flex-direction: column; gap: 26px; }
.stApp .lp-race-row { display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 16px; }
.stApp .lp-race .lp-num { font-size: clamp(21px, 3.5vw, 46px); overflow-wrap: anywhere; color: var(--soft); }
.stApp .lp-race .lp-fast { color: var(--lp-fast); }
.stApp .lp-race-unit { color: var(--strong); font-size: clamp(18px, 2vw, 24px); font-weight: 600; }
.stApp .lp-race-row p { flex-basis: 100%; margin: 4px 0 0; color: var(--muted); font-size: 15px; }
.stApp .lp-fine { margin: 6px 0 0; color: var(--muted); font-size: 15px; line-height: 1.6; max-width: 46em; }
.stApp .lp-stats { margin-top: 72px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 32px 40px; }
.stApp .lp-stats > div { border-top: 1px solid var(--edge); padding-top: 24px; }
.stApp .lp-stats .lp-num { font-size: clamp(44px, 5vw, 64px); }
.stApp .lp-stats p { margin: 14px 0 0; color: var(--text); font-size: 16px; line-height: 1.55; max-width: 22em; }
.stApp .lp-uses { margin-top: 72px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 32px 40px; }
.stApp .lp-uses > div { display: flex; flex-direction: column; gap: 12px; }
.stApp .lp-icon { display: flex; }

/* mission, with the snow leopard */
.stApp .lp-split { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: 64px; align-items: center; }
.stApp .lp-photo { margin: 0; position: relative; aspect-ratio: 4 / 5; border-radius: 30px; overflow: hidden;
                   background: #273042 url("PHOTO") center / cover no-repeat; }
.stApp .lp-photo figcaption { position: absolute; left: 14px; bottom: 14px; padding: 6px 11px; border-radius: 10px;
                              background: rgba(17,17,19,0.6); color: #F4F4F5; font-size: 12px; }
.stApp .lp-mission p { margin: 20px 0 0; color: var(--text); font-size: 17px; line-height: 1.65; max-width: 34em; }
.stApp .lp-jobs { display: flex; flex-wrap: wrap; gap: 8px; margin: 14px 0 0; padding: 0; list-style: none; }
.stApp .lp-jobs li { padding: 8px 14px; border-radius: 99px; border: 1px solid var(--edge); color: var(--strong);
                     font-size: 14px; font-weight: 500; }

/* how Qubi teaches */
.stApp .lp-steps { margin: 52px 0 0; padding: 0; list-style: none; display: grid;
                   grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 36px 32px; }
.stApp .lp-steps li { display: flex; flex-direction: column; gap: 14px; }
.stApp .lp-steps .paper { min-height: 200px; justify-content: center; box-sizing: border-box; }
.stApp .lp-step-title { display: flex; align-items: center; gap: 12px; margin-top: 6px; }
.stApp .lp-step-n { flex: none; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center;
                    justify-content: center; background: #7C3AED; color: #FFFFFF; font-size: 15px; font-weight: 700; }
.stApp .lp-features { margin: 64px 0 0; padding: 28px 0 0; list-style: none; border-top: 1px solid var(--edge);
                      display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 24px 32px; }
.stApp .lp-features li { display: flex; flex-direction: column; gap: 6px; }
.stApp .lp-features b { color: var(--strong); font-size: 16px; font-weight: 600; }
.stApp .lp-features span { color: var(--muted); font-size: 15px; line-height: 1.5; }

/* the course, drawn as a wire with a stop for every unit */
.stApp .lp-track { position: relative; margin-top: 60px; view-timeline-name: --lp-track; }
.stApp .lp-wire { position: absolute; top: 21px; left: calc(100% / 14); right: calc(100% / 14); height: 3px;
                  border-radius: 3px; background: var(--track); overflow: hidden; }
.stApp .lp-wire span { display: block; width: 100%; height: 100%; background: #8B5CF6; transform-origin: left center; }
.stApp .lp-units { position: relative; margin: 0; padding: 0; list-style: none; display: grid;
                   grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 12px; }
.stApp .lp-units li { display: flex; flex-direction: column; align-items: center; text-align: center; gap: 14px; }
.stApp .lp-units li div { display: flex; flex-direction: column; gap: 4px; }
.stApp .lp-stop { width: 45px; height: 45px; border-radius: 50%; box-sizing: border-box; display: flex; align-items: center;
                  justify-content: center; background: #8B5CF6; border: 2px solid #8B5CF6; color: #FFFFFF;
                  font-size: 17px; font-weight: 700; }
.stApp .lp-units b { color: var(--strong); font-size: 15px; font-weight: 600; line-height: 1.3; }
.stApp .lp-units small { color: var(--muted); font-size: 13px; }

/* the last push */
.st-key-lp_cta { position: relative; margin-top: 136px; padding: 60px 56px 56px; border-radius: 36px; background: #6D28D9; }
.stApp .lp-cta-title { margin: 0; padding: 0; color: #FFFFFF; font-size: clamp(36px, 4.6vw, 60px); font-weight: 700;
                       line-height: 1.02; letter-spacing: -0.035em; }
.stApp .lp-cta-text { margin: 16px 0 0; color: #EDE4FF; font-size: 18px; line-height: 1.6; max-width: 30em; }
.stApp .lp-needs { display: flex; flex-wrap: wrap; gap: 10px 26px; margin: 22px 0 8px; padding: 0; list-style: none; }
.stApp .lp-needs li { display: flex; align-items: center; gap: 8px; color: #FFFFFF; font-size: 16px; font-weight: 500; }
.stApp .lp-bit { position: absolute; right: 64px; top: 50%; transform: translateY(-50%); }
.st-key-bottom_sign_up button { background: #FFFFFF; box-shadow: 0 4px 0 #3B1680; min-height: 54px; padding: 0 26px; }
.st-key-bottom_sign_up button:hover { background: #F3EEFF; }
.st-key-bottom_sign_up button p { color: #4C1D95; font-size: 17px; }

/* bottom of the page */
.stApp .lp-footer { margin-top: 96px; padding: 40px 0 16px; border-top: 1px solid var(--line); display: grid;
                    grid-template-columns: minmax(0, 1fr) minmax(0, 1.5fr); gap: 32px 64px; }
.stApp .lp-footer p { margin: 0; color: var(--muted); font-size: 14px; line-height: 1.6; }
.stApp .lp-footer .lp-motto { margin-top: 16px; color: var(--strong); font-size: 16px; font-weight: 600; }
.stApp .lp-sources { margin: 10px 0 0; padding-left: 22px; color: var(--muted); font-size: 13px; line-height: 1.55;
                     display: flex; flex-direction: column; gap: 6px; }
.stApp .lp-sources li { scroll-margin-top: 24px; }
.stApp .lp-footer a { color: var(--soft); text-decoration: underline !important; text-underline-offset: 2px; }

/* scrolling the course wire fills it in, one unit after another (only in browsers that can) */
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .stApp .lp-wire span { animation-name: lp-fill; animation-timing-function: linear; animation-fill-mode: both;
                           animation-timeline: --lp-track; animation-range: contain 0% contain 60%; }
    .stApp .lp-stop { animation-name: lp-stop; animation-timing-function: linear; animation-fill-mode: both;
                      animation-timeline: --lp-track; }
    @media (max-width: 760px) { .stApp .lp-wire span { animation-name: lp-fill-down; } }
  }
}
@keyframes lp-fill { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@keyframes lp-fill-down { from { transform: scaleY(0); } to { transform: scaleY(1); } }
@keyframes lp-stop { from { background: var(--page); border-color: var(--edge); color: var(--muted); }
                     to { background: #8B5CF6; border-color: #8B5CF6; color: #FFFFFF; } }

/* tablets and phones */
@media (max-width: 900px) {
  .stApp .lp-links { display: none; }
  .stApp .st-key-lp_start { justify-content: flex-start; }
  .stApp .lp-features { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .stApp .lp-steps, .stApp .lp-uses, .stApp .lp-stats { grid-template-columns: minmax(0, 1fr); }
  .stApp .lp-steps .paper { min-height: 0; }
  .stApp .lp-split { grid-template-columns: minmax(0, 1fr); gap: 36px; }
  .stApp .lp-photo { aspect-ratio: 16 / 10; }
  .stApp .lp-bit { display: none; }
  .stApp .lp-footer { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 760px) {
  .stApp .lp-lead, .stApp .lp-intro { font-size: 17px; }
  .stApp .lp-section { padding-top: 88px; }
  .stApp .lp-band { margin-top: 88px; padding: 80px 0; }
  .stApp .lp-wide { display: none; }
  .stApp .lp-tall { display: grid; grid-template-columns: 130px minmax(0, 1fr); gap: 10px; }
  .stApp .lp-tall .lp-stops { grid-template-columns: minmax(0, 1fr); grid-template-rows: repeat(5, minmax(0, 1fr)); margin: 0; }
  .stApp .lp-tall .lp-stops span { display: flex; align-items: center; text-align: left; }
  .stApp .lp-units { grid-template-columns: minmax(0, 1fr); gap: 20px; }
  .stApp .lp-units li { flex-direction: row; text-align: left; gap: 16px; }
  .stApp .lp-wire { top: 22px; bottom: 22px; left: 21px; width: 3px; height: auto; }
  .stApp .lp-wire span { transform-origin: center top; }
  .st-key-lp_cta { padding: 40px 26px 36px; border-radius: 28px; margin-top: 96px; }
}
@media (max-width: 560px) { .stApp .lp-features { grid-template-columns: minmax(0, 1fr); } }
""".replace("PHOTO", PHOTO)