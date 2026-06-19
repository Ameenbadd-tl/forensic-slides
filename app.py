import streamlit as st
import random
import time
import os
from PIL import Image

# ==========================================
# إعدادات الصفحة والتصميم الملون (CSS)
# ==========================================
st.set_page_config(
    page_title="Forensic Quiz Pro",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS ملون وحيوي جداً
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');

    /* الخلفية العامة */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* العناوين الملونة */
    .main-title {
        background: linear-gradient(90deg, #FF512F 0%, #DD2476 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.5em;
        font-weight: 900;
        margin-bottom: 10px;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .sub-title {
        color: #4B0082;
        text-align: center;
        font-size: 2.2em;
        font-weight: 700;
        margin-top: 0px;
        margin-bottom: 30px;
        font-family: 'Tajawal', sans-serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    /* صندوق السؤال الملون */
    .question-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        border-top: 10px solid #FF512F;
        box-shadow: 0 15px 35px rgba(255, 81, 47, 0.15);
        margin-bottom: 25px;
        direction: ltr;
        text-align: left;
    }
    
    .question-header {
        color: #FF512F;
        font-size: 1.5em;
        font-weight: 800;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
    }

    /* مربع النص الملون */
    .stTextArea textarea {
        background-color: #FFF9F9 !important;
        border: 2px solid #FF512F !important;
        border-radius: 15px !important;
        color: #333 !important;
        font-size: 1.1em !important;
        padding: 15px !important;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        box-shadow: 0 0 15px rgba(255, 81, 47, 0.3) !important;
        transform: scale(1.01);
    }

    /* الأزرار الملونة */
    div.stButton > button {
        width: 100%;
        border-radius: 50px !important;
        height: 3.5em !important;
        font-size: 1.2em !important;
        font-weight: 700 !important;
        color: white !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }

    /* زر البداية والتأكيد (برتقالي محمر) */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #FF512F, #DD2476) !important;
    }
    
    /* زر السؤال التالي (أخضر زاهي) */
    .next-btn div.stButton > button {
        background: linear-gradient(45deg, #00b09b, #96c93d) !important;
    }

    div.stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important;
        filter: brightness(1.1);
    }

    /* المؤقت الملون */
    .timer-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 25px;
        padding: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 20px rgba(118, 75, 162, 0.3);
        margin: 20px 0;
    }
    
    .timer-val {
        font-size: 4em;
        font-weight: 900;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
    }

    /* شريط التقدم الملون */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%) !important;
    }

    /* الإجابة الصحيحة */
    .correct-ans {
        background: #E8F5E9;
        border-right: 8px solid #2E7D32;
        border-radius: 15px;
        padding: 20px;
        color: #1B5E20;
        font-size: 1.2em;
        font-weight: 600;
        margin-top: 15px;
        direction: ltr;
        text-align: left;
    }

    /* إجابة المستخدم */
    .user-ans {
        background: #F3E5F5;
        border-right: 8px solid #7B1FA2;
        border-radius: 15px;
        padding: 20px;
        color: #4A148C;
        font-size: 1.1em;
        margin-top: 10px;
        direction: ltr;
        text-align: left;
    }
    
    /* تنسيق الصور */
    .stImage > img {
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border: 5px solid white;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 1. البيانات الصحيحة (الصور، الأسئلة، والإجابات)
# ==========================================
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
if 'stored_user_answer' not in st.session_state:
    st.session_state.stored_user_answer = ""
if 'timer_duration' not in st.session_state:
    st.session_state.timer_duration = 30

# عرض العنوان الثابت
st.markdown("<div class='main-title'>🔬 Forensic Quiz Pro</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>محاكي اختبار شرائح الطب الشرعي</div>", unsafe_allow_html=True)

# ==========================================
# 3. واجهة البداية (الإعدادات)
# ==========================================
if not st.session_state.quiz_started:
    
    with st.container():
        st.markdown("<div style='background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);'>", unsafe_allow_html=True)
        st.markdown("### 🛠️ تخصيص الاختبار")
        total_available = len(SLIDES_DATA)
        
        col1, col2 = st.columns(2)
        with col1:
            num_questions = st.number_input(
                f"كم شريحة تريد اختبارها؟ (الأقصى {total_available})", 
                min_value=1, 
                max_value=total_available, 
                value=min(10, total_available)
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True) 
            st.session_state.use_timer = st.toggle("🚀 تفعيل تحدي المؤقت السريع", value=True)
        
        if st.session_state.use_timer:
            st.session_state.timer_duration = st.slider("مدة التفكير لكل شريحة (ثانية)", 10, 60, 30)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔥 ابدأ التحدي الآن"):
            all_slides = list(SLIDES_DATA.keys())
            st.session_state.selected_slides = random.sample(all_slides, num_questions)
            st.session_state.quiz_started = True
            st.session_state.current_q_index = 0
            st.session_state.show_answer = False
            st.session_state.stored_user_answer = ""
            st.session_state.q_start_time = time.time()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. واجهة المراجعة والاختبار
# ==========================================
else:
    total_q = len(st.session_state.selected_slides)
    current_q = st.session_state.current_q_index
    
    if current_q >= total_q:
        st.balloons()
        st.markdown("<div style='text-align:center; padding:50px; background:white; border-radius:20px;'>", unsafe_allow_html=True)
        st.success("🎉 مبروك يا دكتور! لقد أكملت الاختبار بنجاح 🏆")
        if st.button("🔄 العودة للبداية"):
            st.session_state.quiz_started = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
            
    else:
        # شريط التقدم الملون
        st.progress(current_q / total_q)
        st.markdown(f"<p style='text-align:right; font-weight:bold; color:#4B0082;'>جاري العمل على الشريحة {current_q + 1} من {total_q}</p>", unsafe_allow_html=True)
        
        current_slide = st.session_state.selected_slides[current_q]
        slide_data = SLIDES_DATA[current_slide]
        question_text = slide_data["q"]
        correct_answer = slide_data["a"]
        
        # تقسيم الشاشة لجزئين: الصورة والبيانات
        col_img, col_data = st.columns([1.2, 1])
        
        with col_img:
            img_path = os.path.join(FOLDER_NAME, current_slide)
            try:
                image = Image.open(img_path)
                st.image(image, use_container_width=True)
            except FileNotFoundError:
                st.error(f"❌ مفقود: {current_slide}")
        
        with col_data:
            # السؤال
            st.markdown(f"""
                <div class='question-card'>
                    <div class='question-header'>❓ Question</div>
                    <div style='font-size: 1.3em; color: #333;'>{question_text}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # المؤقت
            if not st.session_state.show_answer and st.session_state.use_timer:
                elapsed = int(time.time() - st.session_state.q_start_time)
                remaining = max(0, st.session_state.timer_duration - elapsed)
                
                st.markdown(f"""
                    <div class='timer-container'>
                        <div class='timer-val'>{remaining}</div>
                        <div style='font-weight:bold;'>ثواني متبقية! أسرع!</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if remaining <= 0:
                    st.toast("⚠️ انتهى الوقت!", icon="⏰")
                    st.session_state.show_answer = True
                    st.session_state.time_taken = st.session_state.timer_duration
                    st.rerun()
                
                time.sleep(1)
                st.rerun()

            # منطقة الإجابة
            if not st.session_state.show_answer:
                user_input = st.text_area("⌨️ اكتب تشخيصك هنا:", placeholder="Type your answer in English...", height=150)
                
                if st.button("✅ تأكيد الإجابة"):
                    st.session_state.stored_user_answer = user_input
                    st.session_state.time_taken = time.time() - st.session_state.q_start_time
                    st.session_state.show_answer = True
                    st.rerun()
            else:
                # عرض النتائج بتنسيق ملون
                st.markdown("### 📊 التقييم:")
                st.markdown(f"<div class='user-ans'><b>📝 إجابتك:</b><br>{st.session_state.stored_user_answer or 'لا توجد إجابة'}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='correct-ans'><b>✅ الإجابة النموذجية:</b><br>{correct_answer}</div>", unsafe_allow_html=True)
                
                if st.session_state.use_timer:
                    t = int(st.session_state.time_taken)
                    if t <= st.session_state.timer_duration:
                        st.success(f"⚡ رائع! أجبت في {t} ثانية فقط.")
                    else:
                        st.warning(f"🐢 استغرقت {t} ثانية، حاول أن تكون أسرع!")
                
                st.markdown("<div class='next-btn'>", unsafe_allow_html=True)
                if st.button("➡️ الشريحة التالية"):
                    st.session_state.current_q_index += 1
                    st.session_state.show_answer = False
                    st.session_state.stored_user_answer = ""
                    st.session_state.q_start_time = time.time()
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🏠 العودة للقائمة الرئيسية"):
            st.session_state.quiz_started = False
            st.rerun()
