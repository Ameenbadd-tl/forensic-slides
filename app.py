import html
import random
import time
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "forensic-slides"
TIMER_SECONDS = 30


SLIDES_DATA = {
    "img35.jpg": {"q": "Identify the type of injury and its cause.", "a": "Extensive bruises/ contusions cause by blunt truma"},
    "img36.jpg": {"q": "Identify the type of fracture and the instrument used.", "a": "cut fracture done by a sharp heavy instrument"},
    "img37.jpg": {"q": "Identify the organ injury and its cause.", "a": "spleen laceration cause blunt trauma"},
    "img45.jpg": {"q": "Identify the scalp injury and its cause.", "a": "skin split of scalp casue exposure to extreme heat"},
    "img46.jpg": {"q": "What is the finding, and what is the differential diagnosis (D.D)?", "a": "froth secretion from mouth & nostrils D.D 1 putrefaction foul smell + continent blood 2- drowing"},
    "img47.jpg": {"q": "Identify the vascular injury and its cause.", "a": "Aortic transaction between arch of aorta and descending due to steering wheel injury RTA"},
    "img50.jpg": {"q": "Identify the organ injury and its cause.", "a": "Sever lacerated wound in liver due to sever blunt truma"},
    "img51.jpg": {"q": "Identify the type of fracture and its cause.", "a": "Depressed comminated fracture due to heavy blunt truma Wide surface area & high momentum"},
    "img52.jpg": {"q": "What is the age estimation (MLI) from this sternum and why?", "a": "Sternum MLI : Less than 40y b/c xiphoid cartilage and body not united and body and manubrium on 60y"},
    "img60.jpg": {"q": "Identify the type of skull fracture and specify the inlet/outlet.", "a": "Gutter fracture due to bullet left inlet & right ex"},
    "img61.jpg": {"q": "What is the specific mark seen on this fired bullet?", "a": "Firing bullet there is rifling marks"},
    "img62.jpg": {"q": "Identify the condition and its cause.", "a": "Trench foot due to long immersion in wet water"},
    "img72.jpg": {"q": "Identify the signs, the underlying fracture, and the clinical presentation (C/P).", "a": "Racon eye & spectacle hem due to fracture of base of skull anterior cranial fossa c/p : rhinorrhea"},
    "img73.jpg": {"q": "Identify the type of hair and describe its medulla and cortex.", "a": "Animal hair – thick medulla & thin cortex"},
    "img74.jpg": {"q": "Identify the organ injury and its cause.", "a": "Lacerated wound in kidney due to blunt trauma."},
    "img82.jpg": {"q": "Estimate the age from this skull vault and state the reason.", "a": "Vault of skull Open anterior fontanelle indicating an age less than 1.5y"},
    "img83.jpg": {"q": "Identify the sign pointed by the left pointer and right postmortem change and its mechanism.", "a": "Left pointer : contact pallor mech : compression in blod vessles right Postmortem hypostasis (livor mortis mech : cessation of the circulation and relaxation of muscle tone leading gravitation"},
    "img84.jpg": {"q": "What does the contact pallor indicate in this case?", "a": "Contact pallor indicating prone position at death."},
    "img89.jpg": {"q": "Identify the postmortem change and estimate the time since death.", "a": "Skeletonization (indicated: more 6 months + less 1 year )"},
    "img90.jpg": {"q": "Identify the type of hemorrhage and its cause.", "a": "Extradural (epidural) hemorrhage caused by trauma"},
    "img91.jpg": {"q": "Identify the type of fracture and its cause.", "a": "Hinge fracture , Cause: fall on the buttocks"},
    "img96.jpg": {"q": "Identify the attitude, its cause, and the mechanism.", "a": "Boxer (Pugilistic) attitude. Cause: exposure to extreme heat. Mechanism: coagulation and contraction of muscle proteins"},
    "img97.jpg": {"q": "Determine the sex of the right and left skulls. Mention 2 features for each.", "a": "right is Male skull. 2 Features: prominent supraorbital ridges, angular frontonasal junction left is Female skull. 2 Features: less prominent supraorbital ridges, smotth frontonasal junction"},
    "img98.jpg": {"q": "Identify the postmortem change and its definition.", "a": "Maceration. aseptic autolytic changes that occur in a fetus that died in utero"},
    "img101.jpg": {"q": "Identify the skin lesion and mention its causes.", "a": "Bulla (blister). Causes: putrefaction content gas material burns content albumin protein"},
    "img102.jpg": {"q": "Identify the type of wound.", "a": "Cut defense wound"},
    "img103.jpg": {"q": "Identify the condition and mention when it occurs.", "a": "Cadaveric spasm. Occurs in situations of extreme nervous tension such as suicide"},
    "img106.jpg": {"q": "Identify the finding on the heart surface and its cause.", "a": "Petechial hemorrhages on the heart surface caused by asphyxia"},
    "img107.jpg": {"q": "Identify the injury and its cause.", "a": "Whiplash injury. caused by hyperflexion and hyperextension of the neck"},
    "img108.jpg": {"q": "Identify the condition and the mechanisms of death.", "a": "suffocation by a plastic bag cause death asphyxia + or reflex carotid sinus cardiac arrest"},
    "img111.jpg": {"q": "Identify the type of injury and mention its MLI (3 points).", "a": "Close firearm injury. MLI: 1. Distance of firearm discharge. 2. Print of muzzle. 3. Type of weapon"},
    "img112.jpg": {"q": "Identify the scalp wound and its cause.", "a": "Lacerated wound of the scalp due to blunt trauma"},
    "img113.jpg": {"q": "Identify the type of burn and mention 2 characteristics.", "a": "Scald burn. ( moist burn) Sharp demarcation edge .2. Reddening of the skin"},
    "img116.jpg": {"q": "Identify the type of mark/burn on the neck.", "a": "Rope burns (brush abrasion / ligature mark of hanging)."},
    "img117.jpg": {"q": "Identify the condition and the cause of death.", "a": "Impaction of food in the oropharyngeal (Café Coronary). + choking death : asphyxia or cardiac arrest"},
    "img118.jpg": {
    "q": "Identify the finding and its possible causes.",
    "a": "Petechial hemorrhages on the eyelid and Conjunctival in a case of manual strangulation or sneezing",
    "images": ["img118.jpg", "img119.jpg"],
},
    "img122.jpg": {"q": "Identify the scalp injury and its cause.", "a": "Scalp avulsion of left face (flaying injury) due to a rotating wheel."},
    "img123.jpg": {"q": "1- Identify the type of hanging. 2- Identify the phenomenon pointed by the arrow and its time indication.", "a": "1- Incomplete hanging 2-arrow pointed to marbling phenonmen indicated time since of death is 48h in summer and 1 week un winter"},
    "img124.jpg": {"q": "Identify the location of the suspension point.", "a": "Suspension point of hanging at the occipital region"},
    "img127.jpg": {"q": "Identify the type of knot/noose.", "a": "Double running noose (Knot)"},
    "img128.jpg": {"q": "Identify the brain pathology.", "a": "Brain absess in cerebral hemospher"},
    "img129.jpg": {"q": "Compare the right and left sides of the hyoid bone and mention the associated condition.", "a": "Right side normal hyoid bone Left side : fracture of greater coroner of hyoid bone common in manual strangulation"},
    "img132.jpg": {"q": "What do the soot particles in the trachea indicate?", "a": "Soot particles in trachea indicate antemortem burn death"},
    "img133.jpg": {"q": "Identify the sign, its cause, and the clinical presentation.", "a": "Battles sign cause fracture of base of skull in middle cranial fossa otorrhea"},
    "img134.jpg": {"q": "Identify the condition and the cause of death.", "a": "Gagging cause of death asphyxia"},
    "img137.jpg": {"q": "Identify the type of powder, its content, and gas production volume.", "a": "smokeless powder content nitroglycerine or nitrocellulose one volume prodused 900 volumes of gases"},
    "img138.jpg": {"q": "Identify the type of scars and their cause.", "a": "Keloid scars from extensive burns"},
    "img139.jpg": {"q": "Identify the condition, the material used, and the mark's direction.", "a": "Suicidal hanging with dog lead , the mark rising to suspension point front the neck"},
    "img142.jpg": {"q": "Identify the type of hemorrhage.", "a": "large extradural hemorrhage"},
    "img143.jpg": {"q": "Identify the type of fracture and its cause.", "a": "Ring fracture cause : falling from height on feet or boxer"},
    "img144.jpg": {"q": "Identify the findings indicated by the blue and red arrows and their causes.", "a": "blue arrow Contact pallor due to compression of blood vessels red arrow : hypostasis chery red color due to CO posion or cynaid po or cold"},
    "img147.jpg": {"q": "Identify the type of bruises and their cause.", "a": "Typical railway-line' bruises caused by a wooden rod."},
    "img148.jpg": {"q": "Identify the type of hair and describe its medulla and cortex.", "a": "Human hair – Absent medulla & thick cortex"}
}

FOLDER_NAME = "forensic-slides"

st.set_page_config(
    page_title="Forensic Slides Quiz",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
    <style>
    :root {
        --bg: #f3f6fb;
        --panel: rgba(255, 255, 255, 0.78);
        --panel-strong: rgba(255, 255, 255, 0.94);
        --border: rgba(15, 23, 42, 0.08);
        --text: #0f172a;
        --muted: #64748b;
        --accent: #0f766e;
        --accent-dark: #0b5b56;
        --accent-soft: rgba(15, 118, 110, 0.12);
        --warning: #d97706;
        --danger: #dc2626;
        --shadow: 0 18px 50px rgba(15, 23, 42, 0.10);
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(15, 118, 110, 0.12), transparent 34%),
            radial-gradient(circle at top right, rgba(59, 130, 246, 0.10), transparent 30%),
            linear-gradient(180deg, #eef3f9 0%, #f8fafc 45%, #eef2f7 100%);
        color: var(--text);
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 1180px;
    }

    .hero-shell,
    .panel-shell,
    .question-shell,
    .answer-shell,
    .timer-shell {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 24px;
        box-shadow: var(--shadow);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
    }

    .hero-shell {
        padding: 1.5rem 1.5rem 1.25rem 1.5rem;
        margin-bottom: 1rem;
    }

    .hero-kicker {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        background: var(--accent-soft);
        color: var(--accent-dark);
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin-bottom: 0.9rem;
    }

    .hero-title {
        font-size: clamp(2rem, 3vw, 3.2rem);
        font-weight: 900;
        line-height: 1.05;
        color: var(--text);
        margin-bottom: 0.45rem;
    }

    .hero-subtitle {
        color: var(--muted);
        font-size: 1.02rem;
        line-height: 1.8;
        margin-bottom: 0;
    }

    .mini-stat {
        display: flex;
        flex-direction: column;
        gap: 0.15rem;
        padding: 1rem 1rem 0.9rem 1rem;
        border-radius: 18px;
        background: rgba(15, 23, 42, 0.03);
        border: 1px solid rgba(15, 23, 42, 0.05);
    }

    .mini-stat .label {
        color: var(--muted);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .mini-stat .value {
        color: var(--text);
        font-size: 1.3rem;
        font-weight: 800;
    }

    .panel-shell {
        padding: 1.1rem;
        margin-bottom: 1rem;
    }

    .section-title {
        color: var(--text);
        font-size: 1.12rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }

    .section-caption {
        color: var(--muted);
        font-size: 0.92rem;
        line-height: 1.7;
        margin-bottom: 1rem;
    }

    .question-shell,
    .answer-shell {
        padding: 1.1rem 1.15rem;
    }

    .question-shell {
        border-left: 6px solid var(--accent);
        margin-bottom: 0.9rem;
    }

    .answer-shell {
        border-left: 6px solid #16a34a;
        background: rgba(240, 253, 244, 0.72);
        margin-bottom: 0.9rem;
    }

    .question-label,
    .answer-label {
        display: block;
        font-size: 0.8rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--muted);
        margin-bottom: 0.35rem;
    }

    .question-text,
    .answer-text,
    .user-text {
        font-size: 1.1rem;
        line-height: 1.8;
        color: var(--text);
        word-break: break-word;
    }

    .answer-text {
        font-weight: 700;
    }

    .user-shell {
        padding: 0.95rem 1.05rem;
        background: rgba(255, 255, 255, 0.75);
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 18px;
        margin-bottom: 0.9rem;
    }

    .timer-shell {
        padding: 1rem 1.1rem;
        margin-bottom: 1rem;
        background: rgba(15, 23, 42, 0.04);
    }

    .timer-top {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        gap: 1rem;
        margin-bottom: 0.55rem;
    }

    .timer-heading {
        font-size: 0.95rem;
        font-weight: 800;
        color: var(--text);
    }

    .timer-status {
        font-size: 0.82rem;
        color: var(--muted);
        font-weight: 600;
    }

    .timer-display {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }

    .timer-number {
        font-size: 2.4rem;
        font-weight: 900;
        letter-spacing: -0.05em;
        line-height: 1;
    }

    .timer-meta {
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
        align-items: flex-end;
    }

    .timer-meta .big {
        font-weight: 800;
        color: var(--text);
        font-size: 1rem;
    }

    .timer-meta .small {
        color: var(--muted);
        font-size: 0.86rem;
    }

    .timer-bar {
        width: 100%;
        height: 10px;
        border-radius: 999px;
        background: rgba(15, 23, 42, 0.08);
        overflow: hidden;
        margin-top: 0.85rem;
    }

    .timer-fill {
        height: 100%;
        border-radius: 999px;
        transition: width 0.9s linear, background 0.4s ease;
    }

    div[data-testid="stImage"] {
        display: flex;
        justify-content: center;
        margin: 0.2rem 0 1rem 0;
    }

    div[data-testid="stImage"] img {
        width: 100%;
        max-width: 100%;
        height: auto;
        object-fit: contain;
        border-radius: 18px;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.10);
    }

    @media (max-width: 640px) {
        .hero-title {
            font-size: 1.75rem;
        }

        .question-text,
        .answer-text,
        .user-text {
            font-size: 1rem;
            line-height: 1.7;
        }

        div[data-testid="stImage"] img {
            max-height: 46vh;
        }
    }

    @media (min-width: 641px) and (max-width: 1024px) {
        div[data-testid="stImage"] img {
            max-height: 58vh;
        }
    }

    @media (min-width: 1025px) {
        div[data-testid="stImage"] img {
            max-height: 68vh;
        }
    }

    .timer-safe .timer-number { color: var(--accent); }
    .timer-safe .timer-fill { background: linear-gradient(90deg, #14b8a6, #0f766e); }
    .timer-warning .timer-number { color: var(--warning); }
    .timer-warning .timer-fill { background: linear-gradient(90deg, #f59e0b, #d97706); }
    .timer-danger .timer-number { color: var(--danger); }
    .timer-danger .timer-fill { background: linear-gradient(90deg, #ef4444, #dc2626); }

    .time-result-safe {
        color: #0f766e;
        font-weight: 800;
        font-size: 1rem;
    }

    .time-result-warning {
        color: #b91c1c;
        font-weight: 800;
        font-size: 1rem;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 16px;
        border: 1px solid rgba(15, 23, 42, 0.10);
        padding: 0.82rem 1rem;
        font-weight: 800;
        transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 12px 24px rgba(15, 23, 42, 0.12);
    }

    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextArea"] textarea {
        border-radius: 16px;
        border: 1px solid rgba(15, 23, 42, 0.10);
        background: rgba(255, 255, 255, 0.95);
        color: var(--text);
    }

    div[data-testid="stCheckbox"] label {
        color: var(--text);
        font-weight: 600;
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, #14b8a6, #0f766e) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_state() -> None:
    defaults = {
        "quiz_started": False,
        "current_q_index": 0,
        "selected_slides": [],
        "show_answer": False,
        "use_timer": False,
        "q_start_time": 0.0,
        "time_taken": 0.0,
        "stored_user_answer": "",
        "num_questions": 10,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_quiz() -> None:
    st.session_state.quiz_started = False
    st.session_state.current_q_index = 0
    st.session_state.selected_slides = []
    st.session_state.show_answer = False
    st.session_state.stored_user_answer = ""
    st.session_state.time_taken = 0.0
    st.session_state.q_start_time = 0.0


def start_quiz(num_questions: int, use_timer: bool) -> None:
    all_slides = list(SLIDES_DATA.keys())
    st.session_state.selected_slides = random.sample(all_slides, num_questions)
    st.session_state.quiz_started = True
    st.session_state.current_q_index = 0
    st.session_state.show_answer = False
    st.session_state.stored_user_answer = ""
    st.session_state.time_taken = 0.0
    st.session_state.use_timer = use_timer
    st.session_state.q_start_time = time.time()


def render_timer_widget(start_ts: float, duration: int = TIMER_SECONDS) -> None:
    start_ms = int(start_ts * 1000)
    html_block = f"""
    <style>
      :root {{
        color-scheme: light;
      }}
      body {{
        margin: 0;
        background: transparent;
        font-family: Inter, "Segoe UI", Tahoma, sans-serif;
      }}
      .timer-shell {{
        box-sizing: border-box;
        width: 100%;
        padding: 1rem 1.1rem;
        border-radius: 22px;
        border: 1px solid rgba(15, 23, 42, 0.08);
        background: rgba(255, 255, 255, 0.92);
        box-shadow: 0 14px 40px rgba(15, 23, 42, 0.08);
      }}
      .timer-top {{
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        gap: 1rem;
        margin-bottom: 0.55rem;
      }}
      .timer-heading {{
        font-size: 0.95rem;
        font-weight: 800;
        color: #0f172a;
      }}
      .timer-status {{
        font-size: 0.82rem;
        color: #64748b;
        font-weight: 600;
      }}
      .timer-display {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
      }}
      .timer-number {{
        font-size: 2.4rem;
        font-weight: 900;
        letter-spacing: -0.05em;
        line-height: 1;
      }}
      .timer-meta {{
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
        align-items: flex-end;
      }}
      .timer-meta .big {{
        font-weight: 800;
        color: #0f172a;
        font-size: 1rem;
      }}
      .timer-meta .small {{
        color: #64748b;
        font-size: 0.86rem;
      }}
      .timer-bar {{
        width: 100%;
        height: 10px;
        border-radius: 999px;
        background: rgba(15, 23, 42, 0.08);
        overflow: hidden;
        margin-top: 0.85rem;
      }}
      .timer-fill {{
        height: 100%;
        border-radius: 999px;
        transition: width 0.9s linear, background 0.4s ease;
      }}
      .timer-safe .timer-number {{ color: #0f766e; }}
      .timer-safe .timer-fill {{ background: linear-gradient(90deg, #14b8a6, #0f766e); }}
      .timer-warning .timer-number {{ color: #d97706; }}
      .timer-warning .timer-fill {{ background: linear-gradient(90deg, #f59e0b, #d97706); }}
      .timer-danger .timer-number {{ color: #dc2626; }}
      .timer-danger .timer-fill {{ background: linear-gradient(90deg, #ef4444, #dc2626); }}
    </style>
    <div id="timer-root" class="timer-shell timer-safe">
      <div class="timer-top">
        <div class="timer-heading">Live timer / المؤقت المباشر</div>
        <div class="timer-status">Updated every second</div>
      </div>
      <div class="timer-display">
        <div id="timer-number" class="timer-number">{duration}</div>
        <div class="timer-meta">
          <div id="timer-big" class="big">Ready to answer</div>
          <div id="timer-small" class="small">30 second challenge</div>
        </div>
      </div>
      <div class="timer-bar">
        <div id="timer-fill" class="timer-fill" style="width: 100%;"></div>
      </div>
    </div>
    <script>
      const startMs = {start_ms};
      const duration = {duration};
      const root = document.getElementById("timer-root");
      const numberEl = document.getElementById("timer-number");
      const bigEl = document.getElementById("timer-big");
      const smallEl = document.getElementById("timer-small");
      const fillEl = document.getElementById("timer-fill");

      function tick() {{
        const elapsed = (Date.now() - startMs) / 1000;
        const remaining = Math.max(0, duration - elapsed);
        const remainingInt = Math.ceil(remaining);
        const ratio = Math.max(0, Math.min(1, remaining / duration));

        numberEl.textContent = remainingInt;
        fillEl.style.width = `${{Math.max(2, ratio * 100)}}%`;

        if (remainingInt <= 10) {{
          root.className = "timer-shell timer-danger";
          bigEl.textContent = remainingInt > 0 ? "Focus now" : "Time is up";
          smallEl.textContent = remainingInt > 0 ? "Last few seconds" : "Submit your answer";
        }} else if (remainingInt <= 20) {{
          root.className = "timer-shell timer-warning";
          bigEl.textContent = "Keep going";
          smallEl.textContent = "You are in the final stretch";
        }} else {{
          root.className = "timer-shell timer-safe";
          bigEl.textContent = "Ready to answer";
          smallEl.textContent = "30 second challenge";
        }}
      }}

      tick();
      setInterval(tick, 1000);
    </script>
    """
    components.html(html_block, height=155)


def render_top_hero() -> None:
    st.markdown(
        f"""
        <div class="hero-shell">
          <div class="hero-title">Forensic Slides Quiz</div>
          <div class="hero-subtitle">اختبار شرائح الطب الشرعي مع مؤقت 30 ثانية وعرض نظيف مناسب لكل الأجهزة.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_start_screen() -> None:
    total_available = len(SLIDES_DATA)
    render_top_hero()

    num_questions = st.number_input(
        "Number of slides",
        min_value=1,
        max_value=total_available,
        value=min(int(st.session_state.num_questions), total_available),
        step=1,
    )
    use_timer = st.checkbox("Enable live 30-second timer", value=True)

    st.session_state.num_questions = int(num_questions)

    st.markdown("<div style='height: 0.25rem;'></div>", unsafe_allow_html=True)
    if st.button("Start quiz", type="primary", use_container_width=True):
        start_quiz(int(num_questions), use_timer)
        st.rerun()


def render_image(slide_name: str) -> None:
    slide_path = IMAGE_DIR / slide_name
    if slide_path.exists():
        st.image(str(slide_path), use_container_width=True)
        return

    st.markdown(
        f"""
        <div class="panel-shell">
          <div class="section-title">Image not found</div>
          <div class="section-caption">
            Could not locate <code>{html.escape(slide_name)}</code> inside
            <code>{html.escape(str(IMAGE_DIR))}</code>.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_question_screen() -> None:
    total_q = len(st.session_state.selected_slides)
    current_q = st.session_state.current_q_index

    if current_q >= total_q:
        st.balloons()
        st.markdown(
            """
            <div class="hero-shell">
              <div class="hero-kicker">Completed</div>
              <div class="hero-title">You finished the quiz.</div>
              <div class="hero-subtitle">
                Excellent work. You reached the end of the selected slides, and your focus held up until the last question.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Start another round", type="primary", use_container_width=True):
            reset_quiz()
            st.rerun()
        return

    progress_value = (current_q + (1 if st.session_state.show_answer else 0)) / max(total_q, 1)
    st.progress(progress_value)
    st.caption(f"Question {current_q + 1} of {total_q}")

    current_slide = st.session_state.selected_slides[current_q]
    slide_data = SLIDES_DATA[current_slide]
    question_text = slide_data["q"]
    correct_answer = slide_data["a"]

    st.markdown(
        f"""
        <div class="question-shell">
          <span class="question-label">Question</span>
          <div class="question-text">{html.escape(question_text)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_image(current_slide)

    if not st.session_state.show_answer:
        if st.session_state.use_timer:
            render_timer_widget(st.session_state.q_start_time, TIMER_SECONDS)

        with st.form(key=f"answer_form_{current_q}", clear_on_submit=False):
            user_input = st.text_area(
                "Your answer",
                height=120,
                placeholder="Type your answer here...",
                key=f"answer_input_{current_q}",
                label_visibility="collapsed",
            )
            submit = st.form_submit_button("Show answer", type="primary", use_container_width=True)

        if submit:
            st.session_state.stored_user_answer = user_input
            st.session_state.time_taken = time.time() - st.session_state.q_start_time
            st.session_state.show_answer = True
            st.rerun()
    else:
        user_text = st.session_state.stored_user_answer.strip() or "No answer provided."
        safe_user_text = html.escape(user_text)
        safe_correct = html.escape(correct_answer)
        st.markdown(
            f"""
            <div class="panel-shell">
              <div class="section-title">Review</div>
              <div class="section-caption">Compare your answer with the model answer below.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="user-shell">
              <span class="question-label">Your answer</span>
              <div class="user-text">{safe_user_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="answer-shell">
              <span class="answer-label">Model answer</span>
              <div class="answer-text">{safe_correct}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        elapsed = int(round(st.session_state.time_taken))
        if st.session_state.use_timer:
            if elapsed <= TIMER_SECONDS:
                st.markdown(
                    f"<div class='time-result-safe'>Time used: {elapsed} seconds out of {TIMER_SECONDS}.</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div class='time-result-warning'>Time used: {elapsed} seconds, which is over the 30-second target.</div>",
                    unsafe_allow_html=True,
                )

        next_col, reset_col = st.columns(2)
        with next_col:
            if st.button("Next slide", type="primary", use_container_width=True):
                st.session_state.current_q_index += 1
                st.session_state.show_answer = False
                st.session_state.stored_user_answer = ""
                st.session_state.q_start_time = time.time()
                st.rerun()
        with reset_col:
            if st.button("End quiz", use_container_width=True):
                reset_quiz()
                st.rerun()


init_state()

if not st.session_state.quiz_started:
    render_start_screen()
else:
    render_question_screen()
