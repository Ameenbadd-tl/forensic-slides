import base64
import json
import mimetypes
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Forensic Slides Quiz",
    page_icon="🧠",
    layout="wide",
)

st.markdown(
    """
    <style>
      #MainMenu, header, footer {visibility: hidden;}
      .block-container {padding-top: 0.75rem; padding-bottom: 0.75rem; max-width: 100%;}
    </style>
    """,
    unsafe_allow_html=True,
)

FORENSIC_SLIDES = [
    {"id": "img35.jpg", "question": "Identify the type of injury and its cause.", "answer": "Extensive bruises/ contusions cause by blunt truma"},
    {"id": "img36.jpg", "question": "Identify the type of fracture and the instrument used.", "answer": "cut fracture done by a sharp heavy instrument"},
    {"id": "img37.jpg", "question": "Identify the organ injury and its cause.", "answer": "spleen laceration cause blunt trauma"},
    {"id": "img45.jpg", "question": "Identify the scalp injury and its cause.", "answer": "skin split of scalp casue exposure to extreme heat"},
    {"id": "img46.jpg", "question": "What is the finding, and what is the differential diagnosis (D.D)?", "answer": "froth secretion from mouth & nostrils D.D 1 putrefaction foul smell + continent blood 2- drowing"},
    {"id": "img47.jpg", "question": "Identify the vascular injury and its cause.", "answer": "Aortic transaction between arch of aorta and descending due to steering wheel injury RTA"},
    {"id": "img50.jpg", "question": "Identify the organ injury and its cause.", "answer": "Sever lacerated wound in liver due to sever blunt truma"},
    {"id": "img51.jpg", "question": "Identify the type of fracture and its cause.", "answer": "Depressed comminated fracture due to heavy blunt truma Wide surface area & high momentum"},
    {"id": "img52.jpg", "question": "What is the age estimation (MLI) from this sternum and why?", "answer": "Sternum MLI : Less than 40y b/c xiphoid cartilage and body not united and body and manubrium on 60y"},
    {"id": "img60.jpg", "question": "Identify the type of skull fracture and specify the inlet/outlet.", "answer": "Gutter fracture due to bullet left inlet & right ex"},
    {"id": "img61.jpg", "question": "What is the specific mark seen on this fired bullet?", "answer": "Firing bullet there is rifling marks"},
    {"id": "img62.jpg", "question": "Identify the condition and its cause.", "answer": "Trench foot due to long immersion in cold water"},
    {"id": "img72.jpg", "question": "Identify the signs, the underlying fracture, and the clinical presentation (C/P).", "answer": "Racon eye & spectacle hem due to fracture of base of skull anterior cranial fossa c/p : rhinorrhea"},
    {"id": "img73.jpg", "question": "Identify the type of hair and describe its medulla and cortex.", "answer": "Animal hair – thick medulla & thin cortex"},
    {"id": "img74.jpg", "question": "Identify the organ injury and its cause.", "answer": "Lacerated wound in kidney due to blunt trauma."},
    {"id": "img82.jpg", "question": "Estimate the age from this skull vault and state the reason.", "answer": "Vault of skull Open anterior fontanelle indicating an age less than 1.5y"},
    {"id": "img83.jpg", "question": "Identify the sign pointed by the left pointer and its mechanism.", "answer": "Left pointer : contact pallor mech : compression in blod vessles"},
    {"id": "img84.jpg", "question": "Identify the postmortem change and its mechanism.", "answer": "Postmortem hypostasis (livor mortis mech : cessation of the circulation and relaxation of muscle tone leading gravitation"},
    {"id": "img89.jpg", "question": "What does the contact pallor indicate in this case?", "answer": "Contact pallor indicating prone position at death."},
    {"id": "img90.jpg", "question": "Identify the postmortem change and estimate the time since death.", "answer": "Skeletonization (indicated: more 6 months + less 1 year )"},
    {"id": "img91.jpg", "question": "Identify the type of hemorrhage and its cause.", "answer": "Extradural (epidural) hemorrhage caused by trauma"},
    {"id": "img96.jpg", "question": "Identify the type of fracture and its cause.", "answer": "Hinge fracture , Cause: fall on the buttocks"},
    {"id": "img97.jpg", "question": "Identify the attitude, its cause, and the mechanism.", "answer": "Boxer (Pugilistic) attitude. Cause: exposure to extreme heat. Mechanism: coagulation and contraction of muscle proteins"},
    {"id": "img98.jpg", "question": "Determine the sex of the right and left skulls. Mention 2 features for each.", "answer": "right is Male skull. 2 Features: prominent supraorbital ridges, angular frontonasal junction left is Female skull. 2 Features: less prominent supraorbital ridges, smotth frontonasal junction"},
    {"id": "img101.jpg", "question": "Identify the postmortem change and its definition.", "answer": "Maceration. aseptic autolytic changes that occur in a fetus that died in utero"},
    {"id": "img102.jpg", "question": "Identify the skin lesion and mention its causes.", "answer": "Bulla (blister). Causes: putrefaction content gas material burns content albumin protein"},
    {"id": "img103.jpg", "question": "Identify the type of wound.", "answer": "Cut defense wound"},
    {"id": "img106.jpg", "question": "Identify the condition and mention when it occurs.", "answer": "Cadaveric spasm. Occurs in situations of extreme nervous tension such as suicide"},
    {"id": "img107.jpg", "question": "Identify the finding on the heart surface and its cause.", "answer": "Petechial hemorrhages on the heart surface caused by asphyxia"},
    {"id": "img108.jpg", "question": "Identify the injury and its cause.", "answer": "Whiplash injury. caused by hyperflexion and hyperextension of the neck"},
    {"id": "img111.jpg", "question": "Identify the condition and the mechanisms of death.", "answer": "suffocation by a plastic bag cause death asphyxia + or reflex carotid sinus cardiac arrest"},
    {"id": "img112.jpg", "question": "Identify the type of injury and mention its MLI (3 points).", "answer": "Close firearm injury. MLI: 1. Distance of firearm discharge. 2. Print of muzzle. 3. Type of weapon"},
    {"id": "img113.jpg", "question": "Identify the scalp wound and its cause.", "answer": "Lacerated wound of the scalp due to blunt trauma"},
    {"id": "img116.jpg", "question": "Identify the type of burn and mention 2 characteristics.", "answer": "Scald burn. ( moist burn) Sharp demarcation edge .2. Reddening of the skin"},
    {"id": "img117.jpg", "question": "Identify the type of mark/burn on the neck.", "answer": "Rope burns (brush abrasion / ligature mark of hanging)."},
    {"id": "img118.jpg", "question": "Identify the condition and the cause of death.", "answer": "Impaction of food in the oropharyngeal (Café Coronary). + choking death : asphyxia or cardiac arrest"},
    {"id": "img119.jpg", "question": "Identify the finding and its possible causes.", "answer": "Petechial hemorrhages on the eyelid and Conjunctival in a case of manual strangulation or sneezing"},
    {"id": "img122.jpg", "question": "Identify the scalp injury and its cause.", "answer": "Scalp avulsion of left face (flaying injury) due to a rotating wheel."},
    {"id": "img123.jpg", "question": "1- Identify the type of hanging. 2- Identify the phenomenon pointed by the arrow and its time indication.", "answer": "1- Incomplete hanging 2-arrow pointed to marbling phenonmen indicated time since of death is 48h in summer and 1 week un winter"},
    {"id": "img124.jpg", "question": "Identify the location of the suspension point.", "answer": "Suspension point of hanging at the occipital region"},
    {"id": "img127.jpg", "question": "Identify the type of knot/noose.", "answer": "Double running noose (Knot)"},
    {"id": "img128.jpg", "question": "Identify the brain pathology.", "answer": "Brain absess in cerebral hemospher"},
    {"id": "img129.jpg", "question": "Compare the right and left sides of the hyoid bone and mention the associated condition.", "answer": "Right side normal hyoid bone Left side : fracture of greater coroner of hyoid bone common in manual strangulation"},
    {"id": "img132.jpg", "question": "What do the soot particles in the trachea indicate?", "answer": "Soot particles in trachea indicate antemortem burn death"},
    {"id": "img133.jpg", "question": "Identify the sign, its cause, and the clinical presentation.", "answer": "Battles sign cause fracture of base of skull in middle cranial fossa otorrhea"},
    {"id": "img134.jpg", "question": "Identify the condition and the cause of death.", "answer": "Gagging cause of death asphyxia"},
    {"id": "img137.jpg", "question": "Identify the type of powder, its content, and gas production volume.", "answer": "smokeless powder content nitroglycerine or nitrocellulose one volume prodused 900 volumes of gases"},
    {"id": "img138.jpg", "question": "Identify the type of scars and their cause.", "answer": "Keloid scars from extensive burns"},
    {"id": "img139.jpg", "question": "Identify the condition, the material used, and the mark's direction.", "answer": "Suicidal hanging with dog lead , the mark rising to suspension point front the neck"},
    {"id": "img142.jpg", "question": "Identify the type of hemorrhage.", "answer": "large extradural hemorrhage"},
    {"id": "img143.jpg", "question": "Identify the type of fracture and its cause.", "answer": "Ring fracture cause : falling from height on feet or boxer"},
    {"id": "img144.jpg", "question": "Identify the findings indicated by the blue and red arrows and their causes.", "answer": "blue arrow Contact pallor due to compression of blood vessels red arrow : hypostasis chery red color due to CO posion or cynaid po or cold"},
    {"id": "img147.jpg", "question": "Identify the type of bruises and their cause.", "answer": "Typical railway-line' bruises caused by a wooden rod."},
    {"id": "img148.jpg", "question": "Identify the type of hair and describe its medulla and cortex.", "answer": "Human hair – Absent medulla & thick cortex"},
]


def file_to_data_url(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None

    mime_type, _ = mimetypes.guess_type(str(path))
    mime_type = mime_type or "application/octet-stream"

    raw = path.read_bytes()
    encoded = base64.b64encode(raw).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def resolve_image(slide_id: str) -> str | None:
    base_dir = Path(__file__).parent
    search_paths = [
        base_dir / "forensic-slides" / slide_id,
        base_dir / "static" / "forensic-slides" / slide_id,
        base_dir / "images" / slide_id,
        base_dir / slide_id,
    ]

    for path in search_paths:
        data_url = file_to_data_url(path)
        if data_url:
            return data_url
    return None


slides_with_images = []
for slide in FORENSIC_SLIDES:
    item = dict(slide)
    item["image"] = resolve_image(slide["id"])
    slides_with_images.append(item)

slides_json = json.dumps(slides_with_images, ensure_ascii=False)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Forensic Quiz</title>
  <style>
    :root{
      --bg:#f6f7fb;
      --card:#ffffff;
      --text:#111827;
      --muted:#6b7280;
      --line:#e5e7eb;
      --primary:#111827;
      --primary-2:#374151;
      --success:#166534;
      --success-bg:#ecfdf3;
      --danger:#b91c1c;
      --danger-bg:#fef2f2;
      --warning:#92400e;
      --warning-bg:#fff7ed;
      --shadow:0 12px 32px rgba(17,24,39,.08);
    }

    *{box-sizing:border-box}
    html,body{
      margin:0;
      padding:0;
      font-family:Inter,Segoe UI,Tahoma,Arial,sans-serif;
      background:
        radial-gradient(circle at top left, rgba(17,24,39,.06), transparent 30%),
        radial-gradient(circle at bottom right, rgba(99,102,241,.08), transparent 25%),
        var(--bg);
      color:var(--text);
    }

    body{padding:20px}

    .container{
      max-width:1280px;
      margin:0 auto;
    }

    .hero{
      display:grid;
      grid-template-columns:1.2fr .8fr;
      gap:24px;
      background:rgba(255,255,255,.92);
      border:1px solid var(--line);
      border-radius:32px;
      box-shadow:var(--shadow);
      padding:32px;
      overflow:hidden;
      position:relative;
    }

    .hero::before{
      content:"";
      position:absolute;
      inset:0;
      background:
        linear-gradient(135deg, rgba(17,24,39,.06), transparent 40%),
        linear-gradient(315deg, rgba(99,102,241,.08), transparent 45%);
      pointer-events:none;
    }

    .hero > *{position:relative; z-index:1}

    .badge{
      display:inline-flex;
      align-items:center;
      gap:8px;
      border:1px solid var(--line);
      background:rgba(255,255,255,.82);
      color:var(--muted);
      border-radius:999px;
      padding:10px 14px;
      font-size:14px;
      width:fit-content;
      backdrop-filter:blur(10px);
    }

    h1{
      margin:18px 0 12px;
      font-size:42px;
      line-height:1.15;
      letter-spacing:-.03em;
    }

    .sub{
      margin:0;
      color:var(--muted);
      font-size:17px;
      line-height:1.8;
      max-width:780px;
    }

    .features{
      display:grid;
      grid-template-columns:repeat(3,1fr);
      gap:14px;
      margin-top:24px;
    }

    .feature{
      background:rgba(255,255,255,.82);
      border:1px solid var(--line);
      border-radius:22px;
      padding:18px;
      box-shadow:0 6px 20px rgba(17,24,39,.04);
    }

    .feature .icon{
      width:42px;height:42px;border-radius:14px;
      display:flex;align-items:center;justify-content:center;
      background:#f3f4f6;
      font-size:18px;
      margin-bottom:12px;
    }

    .feature h3{
      margin:0 0 6px;
      font-size:16px;
    }

    .feature p{
      margin:0;
      color:var(--muted);
      font-size:13px;
      line-height:1.7;
    }

    .panel{
      background:rgba(255,255,255,.9);
      border:1px solid var(--line);
      border-radius:26px;
      padding:22px;
    }

    .panel h2{
      margin:0 0 8px;
      font-size:24px;
    }

    .panel .small{
      color:var(--muted);
      margin-bottom:22px;
      line-height:1.7;
      font-size:14px;
    }

    .field{margin-bottom:18px}
    .label{
      display:block;
      margin-bottom:8px;
      font-size:14px;
      font-weight:600;
    }

    input[type="number"], textarea{
      width:100%;
      border:1px solid var(--line);
      border-radius:16px;
      padding:14px 16px;
      font-size:16px;
      outline:none;
      background:#fff;
      color:var(--text);
    }

    input[type="number"]:focus, textarea:focus{
      border-color:#9ca3af;
      box-shadow:0 0 0 4px rgba(17,24,39,.06);
    }

    textarea{
      min-height:160px;
      resize:vertical;
      line-height:1.8;
    }

    .switch-row{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
      border:1px solid var(--line);
      border-radius:20px;
      padding:16px;
      margin-bottom:18px;
      background:#fafafa;
    }

    .meta-grid{
      display:grid;
      grid-template-columns:repeat(2,1fr);
      gap:12px;
      margin-bottom:18px;
    }

    .meta-box{
      border:1px solid var(--line);
      border-radius:18px;
      padding:14px;
      background:#fafafa;
    }

    .meta-box span{
      display:block;
      color:var(--muted);
      font-size:12px;
      margin-bottom:6px;
    }

    .meta-box strong{
      font-size:20px;
    }

    .btn{
      border:none;
      border-radius:18px;
      padding:14px 20px;
      font-size:15px;
      font-weight:700;
      cursor:pointer;
      transition:.2s ease;
    }

    .btn:hover{transform:translateY(-1px)}
    .btn-primary{
      background:var(--primary);
      color:#fff;
      width:100%;
    }
    .btn-primary:hover{background:var(--primary-2)}
    .btn-outline{
      background:#fff;
      color:var(--text);
      border:1px solid var(--line);
    }

    .main-grid{
      display:none;
      grid-template-columns:.74fr 1.26fr;
      gap:24px;
      margin-top:24px;
    }

    .card{
      background:var(--card);
      border:1px solid var(--line);
      border-radius:28px;
      box-shadow:var(--shadow);
      overflow:hidden;
    }

    .card-header{
      padding:24px;
      border-bottom:1px solid var(--line);
      background:#fafafa;
    }

    .card-body{
      padding:24px;
    }

    .section-title{
      margin:0 0 8px;
      font-size:24px;
    }

    .section-sub{
      margin:0;
      color:var(--muted);
      line-height:1.7;
      font-size:14px;
    }

    .timer-badge{
      display:inline-flex;
      align-items:center;
      justify-content:center;
      min-width:88px;
      height:42px;
      border-radius:999px;
      border:1px solid var(--line);
      background:#fff;
      font-weight:800;
      font-size:15px;
    }

    .progress-wrap{
      margin-top:18px;
    }

    .progress{
      width:100%;
      height:9px;
      border-radius:999px;
      background:#eceff4;
      overflow:hidden;
    }

    .progress-bar{
      height:100%;
      width:0%;
      background:linear-gradient(90deg,#111827,#4b5563);
      transition:.3s ease;
    }

    .progress-row{
      display:flex;
      justify-content:space-between;
      gap:12px;
      margin-top:10px;
      color:var(--muted);
      font-size:14px;
    }

    .stats{
      display:grid;
      grid-template-columns:repeat(2,1fr);
      gap:12px;
      margin-top:16px;
    }

    .stat{
      border:1px solid var(--line);
      background:#fff;
      border-radius:20px;
      padding:16px;
    }

    .stat span{
      display:block;
      color:var(--muted);
      font-size:12px;
      margin-bottom:8px;
      text-transform:uppercase;
      letter-spacing:.08em;
    }

    .stat strong{
      font-size:28px;
    }

    .tip{
      margin-top:16px;
      border:1px solid var(--line);
      background:#fafafa;
      border-radius:20px;
      padding:16px;
      color:var(--muted);
      line-height:1.8;
      font-size:14px;
    }

    .question-head{
      display:flex;
      justify-content:space-between;
      gap:16px;
      align-items:center;
      flex-wrap:wrap;
    }

    .pill{
      border:1px solid var(--line);
      padding:10px 14px;
      border-radius:999px;
      background:#fff;
      color:var(--muted);
      font-size:14px;
    }

    .question-box{
      margin-top:18px;
      border:1px solid var(--line);
      border-radius:22px;
      padding:18px;
      background:#fff;
    }

    .question-box small{
      color:var(--muted);
      text-transform:uppercase;
      letter-spacing:.12em;
      font-weight:700;
      font-size:11px;
    }

    .question-box p{
      margin:12px 0 0;
      font-size:20px;
      line-height:1.8;
    }

    .image-box{
      margin-top:22px;
      border:1px solid var(--line);
      border-radius:28px;
      overflow:hidden;
      background:#f8fafc;
      min-height:340px;
      display:flex;
      align-items:center;
      justify-content:center;
    }

    .image-box img{
      width:100%;
      max-height:560px;
      object-fit:contain;
      display:block;
      background:#f9fafb;
    }

    .image-fallback{
      text-align:center;
      padding:40px 24px;
      color:var(--muted);
      line-height:1.8;
    }

    .answer-tools{
      display:grid;
      grid-template-columns:1fr auto;
      gap:12px;
      margin-top:22px;
      align-items:start;
    }

    .countdown-box{
      border-radius:22px;
      border:1px solid var(--line);
      background:#fff;
      padding:14px 18px;
      min-width:120px;
      text-align:center;
    }

    .countdown-box small{
      display:block;
      color:var(--muted);
      text-transform:uppercase;
      letter-spacing:.14em;
      margin-bottom:6px;
      font-size:10px;
    }

    .countdown-box strong{
      font-size:38px;
      font-variant-numeric:tabular-nums;
    }

    .actions{
      display:flex;
      justify-content:flex-end;
      gap:12px;
      margin-top:16px;
      flex-wrap:wrap;
    }

    .answer-grid{
      display:grid;
      grid-template-columns:repeat(2,1fr);
      gap:16px;
      margin-top:22px;
    }

    .answer-card{
      border:1px solid var(--line);
      border-radius:22px;
      padding:18px;
      background:#fff;
    }

    .answer-card h4{
      margin:0 0 10px;
      font-size:16px;
    }

    .answer-card p{
      margin:0;
      line-height:1.9;
      color:#111827;
    }

    .answer-card.muted p{
      color:var(--muted);
    }

    .status-row{
      display:flex;
      flex-wrap:wrap;
      gap:10px;
      margin-top:16px;
    }

    .status{
      display:inline-flex;
      align-items:center;
      gap:8px;
      border-radius:999px;
      padding:10px 14px;
      border:1px solid var(--line);
      font-size:14px;
      background:#fff;
    }

    .status.success{
      border-color:#bbf7d0;
      background:var(--success-bg);
      color:var(--success);
    }

    .status.danger{
      border-color:#fecaca;
      background:var(--danger-bg);
      color:var(--danger);
    }

    .summary{
      display:grid;
      grid-template-columns:repeat(3,1fr);
      gap:12px;
      margin-top:18px;
    }

    .summary-box{
      border:1px solid var(--line);
      border-radius:20px;
      background:#fafafa;
      padding:16px;
    }

    .summary-box span{
      display:block;
      color:var(--muted);
      font-size:12px;
      margin-bottom:6px;
    }

    .summary-box strong{
      font-size:28px;
    }

    .success-note{
      margin-top:16px;
      border:1px solid #bbf7d0;
      background:var(--success-bg);
      color:var(--success);
      border-radius:20px;
      padding:16px;
      line-height:1.8;
    }

    .danger-timer{
      background:var(--danger-bg);
      color:var(--danger);
      border-color:#fecaca;
    }

    .warning-timer{
      background:var(--warning-bg);
      color:var(--warning);
      border-color:#fed7aa;
    }

    @media (max-width: 980px){
      .hero, .main-grid{
        grid-template-columns:1fr;
      }
      .features{
        grid-template-columns:1fr;
      }
      .answer-grid, .summary{
        grid-template-columns:1fr;
      }
      .answer-tools{
        grid-template-columns:1fr;
      }
      h1{font-size:34px}
    }
  </style>
</head>
<body>
  <div class="container">
    <section class="hero">
      <div>
        <div class="badge">Forensic Medicine Slides Quiz</div>
        <h1>واجهة أحدث وأكثر احترافية لاختبار الشرائح</h1>
        <p class="sub">
          تصميم أنظف، بطاقات أوضح، مؤقت تنازلي حيّ يظهر 30 ثم 29 ثم 28،
          وتجربة مراجعة سريعة تساعد الطالب يركز ويتحمس.
        </p>

        <div class="features">
          <div class="feature">
            <div class="icon">✨</div>
            <h3>واجهة نظيفة</h3>
            <p>ألوان هادئة وبطاقات مرتبة بدل شكل الأزرار القديم.</p>
          </div>
          <div class="feature">
            <div class="icon">⏱</div>
            <h3>مؤقت حي</h3>
            <p>عد تنازلي واضح يزيد الحماس في كل سؤال.</p>
          </div>
          <div class="feature">
            <div class="icon">🧠</div>
            <h3>مراجعة أسرع</h3>
            <p>إجابتك والنموذج جنب بعض بشكل منظم.</p>
          </div>
        </div>
      </div>

      <div class="panel">
        <h2>ابدأ الاختبار</h2>
        <div class="small">
          اختر عدد الشرائح وفعّل المؤقت لو تحب تجربة أسرع وأكثر حماس.
        </div>

        <div class="field">
          <label class="label" for="questionCount">عدد الشرائح</label>
          <input id="questionCount" type="number" min="1" value="10" />
          <div class="small" id="maxSlidesText" style="margin-top:8px;margin-bottom:0;"></div>
        </div>

        <div class="switch-row">
          <div>
            <div style="font-weight:700;margin-bottom:4px;">تحدي المؤقت</div>
            <div style="color:var(--muted);font-size:13px;">عرض العد التنازلي من 30 ثانية لكل سؤال.</div>
          </div>
          <label style="display:flex;align-items:center;gap:8px;font-weight:700;">
            <input id="useTimer" type="checkbox" checked />
            تشغيل
          </label>
        </div>

        <div class="meta-grid">
          <div class="meta-box">
            <span>إجمالي الشرائح</span>
            <strong id="totalSlidesValue">0</strong>
          </div>
          <div class="meta-box">
            <span>مدة السؤال</span>
            <strong>30 ثانية</strong>
          </div>
        </div>

        <button class="btn btn-primary" id="startBtn">ابدأ الاختبار الآن</button>
      </div>
    </section>

    <section class="main-grid" id="mainGrid">
      <div>
        <div class="card">
          <div class="card-header">
            <div style="display:flex;justify-content:space-between;gap:12px;align-items:center;flex-wrap:wrap;">
              <div>
                <h2 class="section-title" style="margin:0 0 6px;">لوحة المتابعة</h2>
                <p class="section-sub">راقب التقدم، السرعة، وحالة المؤقت أثناء الحل.</p>
              </div>
              <div class="timer-badge" id="sideTimerBadge">30s</div>
            </div>

            <div class="progress-wrap">
              <div class="progress">
                <div class="progress-bar" id="progressBar"></div>
              </div>
              <div class="progress-row">
                <span id="progressText">السؤال 1 / 1</span>
                <span id="progressPercent">0% مكتمل</span>
              </div>
            </div>
          </div>

          <div class="card-body">
            <div class="stats">
              <div class="stat">
                <span>تمت الإجابة</span>
                <strong id="answeredCount">0</strong>
              </div>
              <div class="stat">
                <span>متوسط الزمن</span>
                <strong id="avgTime">0s</strong>
              </div>
              <div class="stat">
                <span>انتهى المؤقت</span>
                <strong id="timedOutCount">0</strong>
              </div>
              <div class="stat">
                <span>النمط</span>
                <strong id="modeValue">Timed</strong>
              </div>
            </div>

            <div class="tip" id="tipBox">
              اكتب الكلمات المفتاحية أولاً، وبعدها راجع السبب أو الآلية قبل ما تظهر الإجابة النموذجية.
            </div>

            <div style="margin-top:16px;">
              <button class="btn btn-outline" style="width:100%;" id="resetBtn">إنهاء الاختبار والعودة للإعدادات</button>
            </div>
          </div>
        </div>
      </div>

      <div id="contentArea"></div>
    </section>
  </div>

  <script>
    const ALL_SLIDES = __SLIDES_JSON__;
    const TIMER_SECONDS = 30;

    let selectedSlides = [];
    let currentIndex = 0;
    let results = [];
    let answerStartTime = null;
    let countdownInterval = null;
    let timeLeft = TIMER_SECONDS;
    let quizState = "setup";

    const questionCountInput = document.getElementById("questionCount");
    const useTimerInput = document.getElementById("useTimer");
    const startBtn = document.getElementById("startBtn");
    const resetBtn = document.getElementById("resetBtn");
    const mainGrid = document.getElementById("mainGrid");
    const contentArea = document.getElementById("contentArea");

    const totalSlidesValue = document.getElementById("totalSlidesValue");
    const maxSlidesText = document.getElementById("maxSlidesText");
    const progressBar = document.getElementById("progressBar");
    const progressText = document.getElementById("progressText");
    const progressPercent = document.getElementById("progressPercent");
    const answeredCount = document.getElementById("answeredCount");
    const avgTime = document.getElementById("avgTime");
    const timedOutCount = document.getElementById("timedOutCount");
    const modeValue = document.getElementById("modeValue");
    const sideTimerBadge = document.getElementById("sideTimerBadge");
    const tipBox = document.getElementById("tipBox");

    totalSlidesValue.textContent = ALL_SLIDES.length;
    maxSlidesText.textContent = "الحد الأقصى " + ALL_SLIDES.length + " شريحة.";

    function shuffleArray(array) {
      const copy = [...array];
      for (let i = copy.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [copy[i], copy[j]] = [copy[j], copy[i]];
      }
      return copy;
    }

    function getQuestionCount() {
      let count = parseInt(questionCountInput.value || "1", 10);
      if (isNaN(count)) count = 1;
      if (count < 1) count = 1;
      if (count > ALL_SLIDES.length) count = ALL_SLIDES.length;
      questionCountInput.value = count;
      return count;
    }

    function startQuiz() {
      const count = getQuestionCount();
      selectedSlides = shuffleArray(ALL_SLIDES).slice(0, count);
      currentIndex = 0;
      results = [];
      quizState = "question";
      mainGrid.style.display = "grid";
      startQuestion();
      updateSidebar();
    }

    function startQuestion() {
      clearTimer();
      quizState = "question";
      timeLeft = TIMER_SECONDS;
      answerStartTime = Date.now();
      renderQuestion();
      updateSidebar();

      if (useTimerInput.checked) {
        startTimer();
      } else {
        sideTimerBadge.textContent = "No timer";
        sideTimerBadge.className = "timer-badge";
      }
    }

    function startTimer() {
      updateTimerUI();

      countdownInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - answerStartTime) / 1000);
        timeLeft = Math.max(TIMER_SECONDS - elapsed, 0);
        updateTimerUI();

        if (timeLeft <= 0) {
          clearTimer();
          revealAnswer(true);
        }
      }, 250);
    }

    function clearTimer() {
      if (countdownInterval) {
        clearInterval(countdownInterval);
        countdownInterval = null;
      }
    }

    function updateTimerUI() {
      const timerBox = document.getElementById("countdownValue");
      sideTimerBadge.className = "timer-badge";

      if (timeLeft <= 5) {
        sideTimerBadge.classList.add("danger-timer");
      } else if (timeLeft <= 10) {
        sideTimerBadge.classList.add("warning-timer");
      }

      sideTimerBadge.textContent = useTimerInput.checked ? (timeLeft + "s") : "No timer";

      if (timerBox) {
        const holder = timerBox.parentElement;
        holder.className = "countdown-box";
        if (timeLeft <= 5) {
          holder.classList.add("danger-timer");
        } else if (timeLeft <= 10) {
          holder.classList.add("warning-timer");
        }
        timerBox.textContent = timeLeft;
      }
    }

    function revealAnswer(timerExpired = false) {
      if (quizState !== "question") return;

      clearTimer();
      const textarea = document.getElementById("userAnswer");
      const userAnswer = textarea ? textarea.value.trim() : "";
      const elapsed = Math.max(0, Math.ceil((Date.now() - answerStartTime) / 1000));

      const slide = selectedSlides[currentIndex];
      results.push({
        slideId: slide.id,
        userAnswer,
        timeTakenSeconds: elapsed,
        timerExpired
      });

      quizState = "answer";
      renderAnswer(slide, results[results.length - 1]);
      updateSidebar();
    }

    function nextQuestion() {
      currentIndex += 1;
      if (currentIndex >= selectedSlides.length) {
        quizState = "complete";
        renderComplete();
        updateSidebar();
        return;
      }
      startQuestion();
    }

    function resetQuiz() {
      clearTimer();
      selectedSlides = [];
      currentIndex = 0;
      results = [];
      answerStartTime = null;
      timeLeft = TIMER_SECONDS;
      quizState = "setup";
      mainGrid.style.display = "none";
      contentArea.innerHTML = "";
      updateSidebar();
    }

    function updateSidebar() {
      const total = selectedSlides.length || 1;
      const answered = results.length;
      const percent = selectedSlides.length ? Math.round((answered / selectedSlides.length) * 100) : 0;
      const average = answered ? Math.round(results.reduce((sum, item) => sum + item.timeTakenSeconds, 0) / answered) : 0;
      const timedOut = results.filter(item => item.timerExpired).length;

      answeredCount.textContent = answered;
      avgTime.textContent = average + "s";
      timedOutCount.textContent = timedOut;
      modeValue.textContent = useTimerInput.checked ? "Timed" : "Practice";
      progressBar.style.width = percent + "%";
      progressText.textContent = "السؤال " + Math.min(currentIndex + 1, total) + " / " + total;
      progressPercent.textContent = percent + "% مكتمل";

      if (quizState === "complete") {
        tipBox.innerHTML = "ممتاز. خلصت كل الشرائح المحددة. تقدر تبدأ جولة جديدة أو تغيّر عدد الشرائح من الأعلى.";
        tipBox.className = "success-note";
      } else {
        tipBox.innerHTML = "اكتب الكلمات المفتاحية أولاً، وبعدها راجع السبب أو الآلية قبل ما تظهر الإجابة النموذجية.";
        tipBox.className = "tip";
      }

      if (!useTimerInput.checked) {
        sideTimerBadge.textContent = "No timer";
        sideTimerBadge.className = "timer-badge";
      }
    }

    function imageHtml(slide) {
      if (slide.image) {
        return '<img src="' + slide.image + '" alt="' + escapeHtml(slide.question) + '">';
      }
      return `
        <div class="image-fallback">
          <h3 style="margin:0 0 8px;color:#111827">الصورة غير متاحة حالياً</h3>
          <div>ضع الصور في forensic-slides أو static/forensic-slides بنفس الأسماء الحالية.</div>
        </div>
      `;
    }

    function renderQuestion() {
      const slide = selectedSlides[currentIndex];

      contentArea.innerHTML = `
        <div class="card">
          <div class="card-header">
            <div class="question-head">
              <div>
                <h2 class="section-title" style="margin:0 0 6px;">Slide ${currentIndex + 1}</h2>
                <p class="section-sub">${slide.id}</p>
              </div>
              <div class="pill">Forensic identification challenge</div>
            </div>

            <div class="question-box">
              <small>Question</small>
              <p>${escapeHtml(slide.question)}</p>
            </div>
          </div>

          <div class="card-body">
            <div class="image-box">
              ${imageHtml(slide)}
            </div>

            <div class="answer-tools">
              <div>
                <div class="question-box" style="margin-top:0;">
                  <small>Write your answer</small>
                  <p style="margin-top:10px;font-size:14px;color:var(--muted);">اكتب بحرية، وبعدها اعرض النموذج للمقارنة السريعة.</p>
                </div>
              </div>

              ${
                useTimerInput.checked
                  ? `<div class="countdown-box"><small>Countdown</small><strong id="countdownValue">${timeLeft}</strong></div>`
                  : ``
              }
            </div>

            <div style="margin-top:16px;">
              <textarea id="userAnswer" placeholder="Write your answer here..."></textarea>
            </div>

            <div class="actions">
              <button class="btn btn-primary" style="width:auto;" onclick="revealAnswer(false)">تأكيد وإظهار الإجابة</button>
            </div>
          </div>
        </div>
      `;

      updateTimerUI();
    }

    function renderAnswer(slide, result) {
      contentArea.innerHTML = `
        <div class="card">
          <div class="card-header">
            <div class="question-head">
              <div>
                <h2 class="section-title" style="margin:0 0 6px;">Slide ${currentIndex + 1}</h2>
                <p class="section-sub">${slide.id}</p>
              </div>
              <div class="pill">Answer review</div>
            </div>

            <div class="question-box">
              <small>Question</small>
              <p>${escapeHtml(slide.question)}</p>
            </div>
          </div>

          <div class="card-body">
            <div class="image-box">
              ${imageHtml(slide)}
            </div>

            <div class="answer-grid">
              <div class="answer-card ${result.userAnswer ? '' : 'muted'}">
                <h4>إجابتك</h4>
                <p>${result.userAnswer ? escapeHtml(result.userAnswer).replace(/\\n/g, "<br>") : "لم يتم إدخال إجابة."}</p>
              </div>

              <div class="answer-card">
                <h4>الإجابة النموذجية</h4>
                <p>${escapeHtml(slide.answer)}</p>
              </div>
            </div>

            <div class="status-row">
              <div class="status ${result.timerExpired ? 'danger' : 'success'}">
                ${result.timerExpired ? 'انتهى الوقت قبل إظهار الإجابة' : 'تم عرض الإجابة في الوقت المناسب'}
              </div>
              <div class="status">
                الزمن المستغرق ${result.timeTakenSeconds} ثانية
              </div>
            </div>

            <div class="actions">
              <button class="btn btn-primary" style="width:auto;" onclick="nextQuestion()">
                ${currentIndex + 1 >= selectedSlides.length ? 'إنهاء الجلسة' : 'السؤال التالي'}
              </button>
            </div>
          </div>
        </div>
      `;
    }

    function renderComplete() {
      const average = results.length ? Math.round(results.reduce((sum, item) => sum + item.timeTakenSeconds, 0) / results.length) : 0;
      const timedOut = results.filter(item => item.timerExpired).length;

      contentArea.innerHTML = `
        <div class="card">
          <div class="card-header">
            <h2 class="section-title" style="margin:0 0 8px;">Session complete</h2>
            <p class="section-sub">راجع أرقامك بسرعة ثم ابدأ اختبار جديد لو تحب.</p>
          </div>

          <div class="card-body">
            <div class="summary">
              <div class="summary-box">
                <span>الشرائح</span>
                <strong>${selectedSlides.length}</strong>
              </div>
              <div class="summary-box">
                <span>متوسط الزمن</span>
                <strong>${average}s</strong>
              </div>
              <div class="summary-box">
                <span>انتهاء المؤقت</span>
                <strong>${timedOut}</strong>
              </div>
            </div>

            <div class="success-note" style="margin-top:18px;">
              ممتاز. خلصت الجلسة بنجاح، وتقدر تبدأ اختبار جديد وقت ما تحب.
            </div>

            <div class="actions" style="margin-top:18px;">
              <button class="btn btn-primary" style="width:auto;" onclick="resetQuiz()">ابدأ اختبار جديد</button>
            </div>
          </div>
        </div>
      `;
    }

    function escapeHtml(text) {
      const div = document.createElement("div");
      div.textContent = text || "";
      return div.innerHTML;
    }

    startBtn.addEventListener("click", startQuiz);
    resetBtn.addEventListener("click", resetQuiz);
    window.revealAnswer = revealAnswer;
    window.nextQuestion = nextQuestion;
    window.resetQuiz = resetQuiz;
  </script>
</body>
</html>
"""

html_with_data = HTML.replace("__SLIDES_JSON__", slides_json)

components.html(html_with_data, height=2400, scrolling=True)
