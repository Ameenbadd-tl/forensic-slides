import streamlit as st
import random
import time
import os
from PIL import Image

# إعدادات الصفحة
st.set_page_config(page_title="Forensic Quiz 24/25", page_icon="🔬", layout="centered")

# CSS لتصميم احترافي (الواجهة الرسومية)
st.markdown("""
    <style>
    .main-title { text-align: center; color: #1e3a8a; font-size: 2.5em; font-weight: 800; }
    .timer-box { font-size: 3em; font-weight: bold; color: #ef4444; text-align: center; background: #fee2e2; border-radius: 15px; padding: 10px; margin: 20px 0; }
    .q-box { background: #f1f5f9; padding: 20px; border-radius: 10px; border-left: 5px solid #2563eb; margin-bottom: 20px; font-size: 1.2em; }
    .ans-box { background: #f0fdf4; padding: 20px; border-radius: 10px; border-left: 5px solid #16a34a; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# قاعدة البيانات (الـ 54 شريحة)
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
    "img62.jpg": {"q": "Identify the condition and its cause.", "a": "Trench foot due to long immersion in cold water"},
    "img72.jpg": {"q": "Identify the signs, the underlying fracture, and the clinical presentation (C/P).", "a": "Racon eye & spectacle hem due to fracture of base of skull anterior cranial fossa c/p : rhinorrhea"},
    "img73.jpg": {"q": "Identify the type of hair and describe its medulla and cortex.", "a": "Animal hair – thick medulla & thin cortex"},
    "img74.jpg": {"q": "Identify the organ injury and its cause.", "a": "Lacerated wound in kidney due to blunt trauma."},
    "img82.jpg": {"q": "Estimate the age from this skull vault and state the reason.", "a": "Vault of skull Open anterior fontanelle indicating an age less than 1.5y"},
    "img83.jpg": {"q": "Identify the sign pointed by the left pointer and its mechanism.", "a": "Left pointer : contact pallor mech : compression in blod vessles"},
    "img84.jpg": {"q": "Identify the postmortem change and its mechanism.", "a": "Postmortem hypostasis (livor mortis mech : cessation of the circulation and relaxation of muscle tone leading gravitation"},
    "img89.jpg": {"q": "What does the contact pallor indicate in this case?", "a": "Contact pallor indicating prone position at death."},
    "img90.jpg": {"q": "Identify the postmortem change and estimate the time since death.", "a": "Skeletonization (indicated: more 6 months + less 1 year )"},
    "img91.jpg": {"q": "Identify the type of hemorrhage and its cause.", "a": "Extradural (epidural) hemorrhage caused by trauma"},
    "img96.jpg": {"q": "Identify the type of fracture and its cause.", "a": "Hinge fracture , Cause: fall on the buttocks"},
    "img97.jpg": {"q": "Identify the attitude, its cause, and the mechanism.", "a": "Boxer (Pugilistic) attitude. Cause: exposure to extreme heat. Mechanism: coagulation and contraction of muscle proteins"},
    "img98.jpg": {"q": "Determine the sex of the right and left skulls. Mention 2 features for each.", "a": "right is Male skull. 2 Features: prominent supraorbital ridges, angular frontonasal junction left is Female skull. 2 Features: less prominent supraorbital ridges, smotth frontonasal junction"},
    "img101.jpg": {"q": "Identify the postmortem change and its definition.", "a": "Maceration. aseptic autolytic changes that occur in a fetus that died in utero"},
    "img102.jpg": {"q": "Identify the skin lesion and mention its causes.", "a": "Bulla (blister). Causes: putrefaction content gas material burns content albumin protein"},
    "img103.jpg": {"q": "Identify the type of wound.", "a": "Cut defense wound"},
    "img106.jpg": {"q": "Identify the condition and mention when it occurs.", "a": "Cadaveric spasm. Occurs in situations of extreme nervous tension such as suicide"},
    "img107.jpg": {"q": "Identify the finding on the heart surface and its cause.", "a": "Petechial hemorrhages on the heart surface caused by asphyxia"},
    "img108.jpg": {"q": "Identify the injury and its cause.", "a": "Whiplash injury. caused by hyperflexion and hyperextension of the neck"},
    "img111.jpg": {"q": "Identify the condition and the mechanisms of death.", "a": "suffocation by a plastic bag cause death asphyxia + or reflex carotid sinus cardiac arrest"},
    "img112.jpg": {"q": "Identify the type of injury and mention its MLI (3 points).", "a": "Close firearm injury. MLI: 1. Distance of firearm discharge. 2. Print of muzzle. 3. Type of weapon"},
    "img113.jpg": {"q": "Identify the scalp wound and its cause.", "a": "Lacerated wound of the scalp due to blunt trauma"},
    "img116.jpg": {"q": "Identify the type of burn and mention 2 characteristics.", "a": "Scald burn. ( moist burn) Sharp demarcation edge .2. Reddening of the skin"},
    "img117.jpg": {"q": "Identify the type of mark/burn on the neck.", "a": "Rope burns (brush abrasion / ligature mark of hanging)."},
    "img118.jpg": {"q": "Identify the condition and the cause of death.", "a": "Impaction of food in the oropharyngeal (Café Coronary). + choking death : asphyxia or cardiac arrest"},
    "img119.jpg": {"q": "Identify the finding and its possible causes.", "a": "Petechial hemorrhages on the eyelid and Conjunctival in a case of manual strangulation or sneezing"},
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

# التهيئة
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'started' not in st.session_state: st.session_state.started = False

st.markdown("<h1 class='main-title'>🔬 Forensic Master</h1>", unsafe_allow_html=True)

if not st.session_state.started:
    if st.button("🚀 ابدأ التحدي الآن"):
        st.session_state.started = True
        st.session_state.slides = random.sample(list(SLIDES_DATA.keys()), len(SLIDES_DATA))
        st.rerun()
else:
    idx = st.session_state.q_idx
    if idx < len(st.session_state.slides):
        img = st.session_state.slides[idx]
        st.markdown(f"<div class='q-box'>❓ {SLIDES_DATA[img]['q']}</div>", unsafe_allow_html=True)
        
        # المؤقت
        timer_placeholder = st.empty()
        for i in range(30, 0, -1):
            timer_placeholder.markdown(f"<div class='timer-box'>⏳ {i}</div>", unsafe_allow_html=True)
            time.sleep(1)
        
        st.image(os.path.join("forensic-slides", img), use_container_width=True)
        ans = st.text_area("اكتب إجابتك هنا:")
        
        if st.button("تأكيد"):
            st.markdown(f"<div class='ans-box'>✅ <b>الإجابة الصحيحة:</b> {SLIDES_DATA[img]['a']}</div>", unsafe_allow_html=True)
            if st.button("السؤال التالي"):
                st.session_state.q_idx += 1
                st.rerun()
    else:
        st.success("🎉 انتهيت من جميع الأسئلة!")
