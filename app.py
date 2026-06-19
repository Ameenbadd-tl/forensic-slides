import streamlit as st
import random
import time
import os
from PIL import Image

# ==========================================
# إعدادات الصفحة والتصميم الاحترافي (CSS)
# ==========================================
st.set_page_config(page_title="Forensic Slides Quiz", page_icon="🔬", layout="centered")

st.markdown("""
    <style>
    /* تنسيق العناوين */
    .title-en { text-align: center; color: #1E3A8A; font-size: 2.2em; font-weight: bold; margin-bottom: 5px; font-family: 'Arial', sans-serif;}
    .title-ar { text-align: center; color: #B91C1C; font-size: 1.8em; font-weight: bold; margin-top: 0px; margin-bottom: 25px; font-family: 'Tajawal', sans-serif;}
    
    /* تنسيق بطاقة الإجابة */
    .answer-card { 
        background-color: #F0FDF4; 
        border-right: 6px solid #16A34A; /* خط أخضر على اليمين */
        padding: 20px; 
        border-radius: 10px; 
        color: #14532D; 
        font-size: 1.3em; 
        font-weight: bold; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: left;
        direction: ltr;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    
    /* تنسيق رسائل الوقت */
    .time-success { color: #16A34A; font-weight: bold; font-size: 1.1em; text-align: center;}
    .time-warning { color: #DC2626; font-weight: bold; font-size: 1.1em; text-align: center;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 1. البيانات (الصور والإجابات)
# ==========================================
SLIDES_DATA = {
    "img35.jpg": "Extensive bruises/ contusions cause by blunt truma",
    "img36.jpg": "cut fracture done by a sharp heavy instrument",
    "img37.jpg": "spleen laceration cause blunt trauma",
    "img45.jpg": "skin split of scalp casue exposure to extreme heat",
    "img46.jpg": "froth secretion from mouth & nostrils D.D 1 putrefaction foul smell + continent blood 2- drowing",
    "img47.jpg": "Aortic transaction between arch of aorta and descending due to steering wheel injury RTA",
    "img50.jpg": "Sever lacerated wound in liver due to sever blunt truma",
    "img51.jpg": "Depressed comminated fracture due to heavy blunt truma Wide surface area & high momentum",
    "img52.jpg": "Sternum MLI : Less than 40y b/c xiphoid cartilage and body not united and body and manubrium on 60y",
    "img60.jpg": "Gutter fracture due to bullet left inlet & right ex",
    "img61.jpg": "Firing bullet there is rifling marks",
    "img62.jpg": "Trench foot due to long immersion in cold water",
    "img72.jpg": "Racon eye & spectacle hem due to fracture of base of skull anterior cranial fossa c/p : rhinorrhea",
    "img73.jpg": "Animal hair – thick medulla & thin cortex",
    "img74.jpg": "Lacerated wound in kidney due to blunt trauma.",
    "img82.jpg": "Vault of skull Open anterior fontanelle indicating an age less than 1.5y",
    "img83.jpg": "Left pointer : contact pallor mech : compression in blod vessles",
    "img84.jpg": "Postmortem hypostasis (livor mortis mech : cessation of the circulation and relaxation of muscle tone leading gravitation",
    "img89.jpg": "Contact pallor indicating prone position at death.",
    "img90.jpg": "Skeletonization (indicated: more 6 months + less 1 year )",
    "img91.jpg": "Extradural (epidural) hemorrhage caused by trauma",
    "img96.jpg": "Hinge fracture , Cause: fall on the buttocks",
    "img97.jpg": "Boxer (Pugilistic) attitude. Cause: exposure to extreme heat. Mechanism: coagulation and contraction of muscle proteins",
    "img98.jpg": "right is Male skull. 2 Features: prominent supraorbital ridges, angular frontonasal junction left is Female skull. 2 Features: less prominent supraorbital ridges, smotth frontonasal junction",
    "img101.jpg": "Maceration. aseptic autolytic changes that occur in a fetus that died in utero",
    "img102.jpg": "Bulla (blister). Causes: putrefaction content gas material burns content albumin protein",
    "img103.jpg": "Cut defense wound",
    "img106.jpg": "Cadaveric spasm. Occurs in situations of extreme nervous tension such as suicide",
    "img107.jpg": "Petechial hemorrhages on the heart surface caused by asphyxia",
    "img108.jpg": "Whiplash injury. caused by hyperflexion and hyperextension of the neck",
    "img111.jpg": "suffocation by a plastic bag cause death asphyxia + or reflex carotid sinus cardiac arrest",
    "img112.jpg": "Close firearm injury. MLI: 1. Distance of firearm discharge. 2. Print of muzzle. 3. Type of weapon",
    "img113.jpg": "Lacerated wound of the scalp due to blunt trauma",
    "img116.jpg": "Scald burn. ( moist burn) Sharp demarcation edge .2. Reddening of the skin",
    "img117.jpg": "Rope burns (brush abrasion / ligature mark of hanging).",
    "img118.jpg": "Impaction of food in the oropharyngeal (Café Coronary). + choking death : asphyxia or cardiac arrest",
    "img119.jpg": "Petechial hemorrhages on the eyelid and Conjunctival in a case of manual strangulation or sneezing",
    "img122.jpg": "Scalp avulsion of left face (flaying injury) due to a rotating wheel.",
    "img123.jpg": "1- Incomplete hanging 2-arrow pointed to marbling phenonmen indicated time since of death is 48h in summer and 1 week un winter",
    "img124.jpg": "Suspension point of hanging at the occipital region",
    "img127.jpg": "Double running noose (Knot)",
    "img128.jpg": "Brain absess in cerebral hemospher",
    "img129.jpg": "Right side normal hyoid bone Left side : fracture of greater coroner of hyoid bone common in manual strangulation",
    "img132.jpg": "Soot particles in trachea indicate antemortem burn death",
    "img133.jpg": "Battles sign cause fracture of base of skull in middle cranial fossa otorrhea",
    "img134.jpg": "Gagging cause of death asphyxia",
    "img137.jpg": "smokeless powder content nitroglycerine or nitrocellulose one volume prodused 900 volumes of gases",
    "img138.jpg": "Keloid scars from extensive burns",
    "img139.jpg": "Suicidal hanging with dog lead , the mark rising to suspension point front the neck",
    "img142.jpg": "large extradural hemorrhage",
    "img143.jpg": "Ring fracture cause : falling from height on feet or boxer",
    "img144.jpg": "blue arrow Contact pallor due to compression of blood vessels red arrow : hypostasis chery red color due to CO posion or cynaid po or cold",
    "img147.jpg": "Typical railway-line' bruises caused by a wooden rod.",
    "img148.jpg": "Human hair – Absent medulla & thick cortex"
}

FOLDER_NAME = "forensic-slides"

# ==========================================
# 2. تهيئة المتغيرات (Session State)
# ==========================================
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'current_q_index' not in st.session_state:
    st.session_state.current_q_index = 0
if 'selected_slides' not in st.session_state:
    st.session_state.selected_slides = []
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'use_timer' not in st.session_state:
    st.session_state.use_timer = False
if 'q_start_time' not in st.session_state:
    st.session_state.q_start_time = 0.0
if 'time_taken' not in st.session_state:
    st.session_state.time_taken = 0.0

# عرض العنوان الثابت في كل الصفحات
st.markdown("<div class='title-en'>🔬 Forensic Medicine Slides Quiz</div>", unsafe_allow_html=True)
st.markdown("<div class='title-ar'>محاكي اختبار شرائح الطب الشرعي</div>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 3. واجهة البداية (الإعدادات)
# ==========================================
if not st.session_state.quiz_started:
    
    st.markdown("### ⚙️ إعدادات المراجعة:")
    total_available = len(SLIDES_DATA)
    
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.number_input(
            f"عدد الشرائح (الأقصى {total_available}):", 
            min_value=1, 
            max_value=total_available, 
            value=min(10, total_available)
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True) # مسافة فارغة لضبط المحاذاة
        st.session_state.use_timer = st.checkbox("⏳ تفعيل تحدي المؤقت (30 ثانية)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 ابدأ المراجعة الآن", use_container_width=True):
        all_slides = list(SLIDES_DATA.keys())
        st.session_state.selected_slides = random.sample(all_slides, num_questions)
        st.session_state.quiz_started = True
        st.session_state.current_q_index = 0
        st.session_state.show_answer = False
        st.session_state.q_start_time = time.time() # بدء حساب الوقت للسؤال الأول
        st.rerun()

# ==========================================
# 4. واجهة المراجعة (البطاقات)
# ==========================================
else:
    total_q = len(st.session_state.selected_slides)
    current_q = st.session_state.current_q_index
    
    if current_q >= total_q:
        st.balloons()
        st.success("🎉 لقد أنهيت جميع الشرائح المحددة، أحسنت يا دكتور! جاهز للامتحان إن شاء الله. 🥇")
            
        if st.button("🔄 بدء مراجعة جديدة", use_container_width=True):
            st.session_state.quiz_started = False
            st.rerun()
            
    else:
        # شريط التقدم
        progress_val = current_q / total_q
        st.progress(progress_val)
        
        current_slide = st.session_state.selected_slides[current_q]
        correct_answer = SLIDES_DATA[current_slide]
        
        st.markdown(f"**الشريحة {current_q + 1} من {total_q}**")
        
        # عرض الصورة
        img_path = os.path.join(FOLDER_NAME, current_slide)
        try:
            image = Image.open(img_path)
            st.image(image, use_container_width=True)
        except FileNotFoundError:
            st.error(f"❌ لم يتم العثور على الصورة: {current_slide}. تأكد من رفعها للمجلد الصحيح.")
            
        # منطقة الإجابة والمؤقت
        if not st.session_state.show_answer:
            if st.session_state.use_timer:
                st.info("⏳ فكر في التشخيص والميكانيكية بسرعة! لديك 30 ثانية...")
            else:
                st.info("🧠 فكر في التشخيص والميكانيكية، ثم تأكد من إجابتك.")
                
            if st.button("👁️ إظهار الإجابة الصحيحة", use_container_width=True):
                # حساب الوقت المستغرق بمجرد الضغط
                st.session_state.time_taken = time.time() - st.session_state.q_start_time
                st.session_state.show_answer = True
                st.rerun()
        else:
            # عرض الإجابة النموذجية في بطاقة احترافية
            st.markdown(f"<div class='answer-card'>{correct_answer}</div>", unsafe_allow_html=True)
            
            # عرض نتيجة المؤقت إن كان مفعلاً
            if st.session_state.use_timer:
                t = int(st.session_state.time_taken)
                if t <= 30:
                    st.markdown(f"<div class='time-success'>⏱️ رائع! استغرقت {t} ثانية فقط.</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='time-warning'>⚠️ استغرقت {t} ثانية. حاول أن تكون أسرع في الامتحان! (الهدف: 30 ثانية)</div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("➡️ الشريحة التالية", use_container_width=True, type="primary"):
                st.session_state.current_q_index += 1
                st.session_state.show_answer = False
                st.session_state.q_start_time = time.time() # إعادة ضبط المؤقت للسؤال القادم
                st.rerun()

        st.markdown("---")
        if st.button("🛑 إنهاء أو تغيير الإعدادات"):
            st.session_state.quiz_started = False
            st.rerun()
