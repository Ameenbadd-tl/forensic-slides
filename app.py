import streamlit as st
import random
import time
import os
from PIL import Image

# ==========================================
# إعدادات الصفحة والتصميم الاحترافي (CSS)
# ==========================================
st.set_page_config(
    page_title="Forensic Slides Quiz",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS محسّن للواجهة الاحترافية
st.markdown("""
    <style>
    /* الألوان الأساسية */
    :root {
        --primary-color: #1E3A8A;
        --secondary-color: #B91C1C;
        --success-color: #16A34A;
        --warning-color: #DC2626;
        --info-color: #3B82F6;
        --light-bg: #F8FAFC;
    }
    
    /* العنوان الرئيسي */
    .title-en {
        text-align: center;
        color: #1E3A8A;
        font-size: 2.8em;
        font-weight: 900;
        margin-bottom: 5px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        letter-spacing: -1px;
    }
    
    .title-ar {
        text-align: center;
        color: #B91C1C;
        font-size: 2.2em;
        font-weight: 800;
        margin-top: 0px;
        margin-bottom: 30px;
        font-family: 'Tajawal', 'Arial', sans-serif;
    }
    
    /* صندوق السؤال */
    .question-box {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border-left: 6px solid #3B82F6;
        border-radius: 12px;
        padding: 20px;
        color: #1E3A8A;
        font-size: 1.25em;
        margin-bottom: 20px;
        direction: ltr;
        text-align: left;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    }
    
    /* صندوق إجابة المستخدم */
    .user-answer-card {
        background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
        border-left: 6px solid #6B7280;
        border-radius: 12px;
        padding: 18px;
        color: #374151;
        font-size: 1.1em;
        margin-bottom: 15px;
        direction: ltr;
        text-align: left;
    }

    /* صندوق الإجابة النموذجية */
    .answer-card {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border-left: 6px solid #16A34A;
        border-radius: 12px;
        padding: 18px;
        color: #14532D;
        font-size: 1.15em;
        font-weight: 600;
        margin-bottom: 20px;
        direction: ltr;
        text-align: left;
    }
    
    /* المؤقت التنازلي */
    .timer-box {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        border: 3px solid #F59E0B;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 8px 16px rgba(245, 158, 11, 0.2);
    }
    
    .timer-display {
        font-size: 3.5em;
        font-weight: 900;
        color: #D97706;
        font-family: 'Courier New', monospace;
        letter-spacing: 3px;
    }
    
    .timer-label {
        font-size: 1.1em;
        color: #B45309;
        font-weight: 600;
        margin-top: 10px;
    }
    
    /* شريط التقدم */
    .progress-info {
        font-size: 1.1em;
        font-weight: 600;
        color: #1E3A8A;
        margin-bottom: 15px;
    }
    
    /* الأزرار المحسّنة */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 1. البيانات (الصور، الأسئلة، والإجابات)
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
st.markdown("<div class='title-en'>🔬 Forensic Medicine Slides Quiz</div>", unsafe_allow_html=True)
st.markdown("<div class='title-ar'>محاكي اختبار شرائح الطب الشرعي</div>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 3. واجهة البداية (الإعدادات)
# ==========================================
if not st.session_state.quiz_started:
    
    st.markdown("### ⚙️ إعدادات الاختبار:")
    total_available = len(SLIDES_DATA)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        num_questions = st.number_input(
            f"عدد الشرائح (الأقصى {total_available}):", 
            min_value=1, 
            max_value=total_available, 
            value=min(10, total_available)
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True) 
        st.session_state.use_timer = st.checkbox("⏳ تفعيل تحدي المؤقت")
    
    with col3:
        if st.session_state.use_timer:
            st.markdown("<br>", unsafe_allow_html=True)
            st.session_state.timer_duration = st.number_input(
                "مدة المؤقت (ثانية):",
                min_value=10,
                max_value=120,
                value=30
            )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 ابدأ الاختبار الآن", use_container_width=True):
        all_slides = list(SLIDES_DATA.keys())
        st.session_state.selected_slides = random.sample(all_slides, num_questions)
        st.session_state.quiz_started = True
        st.session_state.current_q_index = 0
        st.session_state.show_answer = False
        st.session_state.stored_user_answer = ""
        st.session_state.q_start_time = time.time()
        st.rerun()

# ==========================================
# 4. واجهة المراجعة والاختبار
# ==========================================
else:
    total_q = len(st.session_state.selected_slides)
    current_q = st.session_state.current_q_index
    
    if current_q >= total_q:
        st.balloons()
        st.success("🎉 لقد أنهيت جميع الشرائح المحددة، أحسنت يا دكتور! 🥇")
        if st.button("🔄 بدء اختبار جديد", use_container_width=True):
            st.session_state.quiz_started = False
            st.rerun()
            
    else:
        # شريط التقدم
        st.progress(current_q / total_q)
        st.markdown(f"<div class='progress-info'>📊 الشريحة <b>{current_q + 1}</b> من <b>{total_q}</b></div>", unsafe_allow_html=True)
        
        current_slide = st.session_state.selected_slides[current_q]
        slide_data = SLIDES_DATA[current_slide]
        question_text = slide_data["q"]
        correct_answer = slide_data["a"]
        
        # 1. عرض السؤال بالإنجليزي
        st.markdown(f"<div class='question-box'>❓ <b>Question:</b> {question_text}</div>", unsafe_allow_html=True)
        
        # 2. عرض الصورة
        img_path = os.path.join(FOLDER_NAME, current_slide)
        try:
            image = Image.open(img_path)
            st.image(image, use_container_width=True)
        except FileNotFoundError:
            st.error(f"❌ لم يتم العثور على الصورة: {current_slide}.")
            
        # 3. منطقة الإجابة والمؤقت
        if not st.session_state.show_answer:
            if st.session_state.use_timer:
                # حساب الوقت المتبقي
                elapsed = int(time.time() - st.session_state.q_start_time)
                remaining = max(0, st.session_state.timer_duration - elapsed)
                
                # عرض المؤقت التنازلي
                minutes = remaining // 60
                seconds = remaining % 60
                
                timer_color = "#D97706" if remaining > 10 else "#DC2626"
                
                st.markdown(f"""
                    <div class='timer-box'>
                        <div id='countdown' class='timer-display' style='color: {timer_color};'>{minutes:02d}:{seconds:02d}</div>
                        <div class='timer-label'>⏱️ الوقت المتبقي</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # إذا انتهى الوقت، اعرض الإجابة تلقائياً
                if remaining <= 0:
                    st.warning("⚠️ انتهى الوقت! سيتم عرض الإجابة الصحيحة.")
                    st.session_state.stored_user_answer = ""
                    st.session_state.time_taken = st.session_state.timer_duration
                    st.session_state.show_answer = True
                    st.rerun()
                
                # حل المؤقت بدون مكتبات خارجية: استخدام empty وتكرار
                time.sleep(1)
                st.rerun()
                
            # مربع إدخال النص
            user_input = st.text_area("✍️ Write your answer here / اكتب إجابتك هنا:", height=100)
            
            if st.button("👁️ تأكيد وإظهار الإجابة الصحيحة", use_container_width=True, type="primary"):
                st.session_state.stored_user_answer = user_input
                st.session_state.time_taken = time.time() - st.session_state.q_start_time
                st.session_state.show_answer = True
                st.rerun()
                
        # 4. منطقة عرض النتيجة والتصحيح
        else:
            # عرض إجابة الطالب
            st.markdown("<b>📝 إجابتك (Your Answer):</b>", unsafe_allow_html=True)
            user_text = st.session_state.stored_user_answer if st.session_state.stored_user_answer.strip() else "لم تكتب شيئاً (No answer provided)"
            st.markdown(f"<div class='user-answer-card'>{user_text}</div>", unsafe_allow_html=True)
            
            # عرض الإجابة النموذجية
            st.markdown("<b>✅ الإجابة النموذجية (Model Answer):</b>", unsafe_allow_html=True)
            st.markdown(f"<div class='answer-card'>{correct_answer}</div>", unsafe_allow_html=True)
            
            # عرض نتيجة المؤقت إن كان مفعلاً
            if st.session_state.use_timer:
                t = int(st.session_state.time_taken)
                if t <= st.session_state.timer_duration:
                    st.info(f"⏱️ استغرقت {t} ثانية (ممتاز! ⚡)")
                else:
                    st.warning(f"⚠️ استغرقت {t} ثانية (تجاوزت الحد الزمني 😅)")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("➡️ السؤال التالي (Next Slide)", use_container_width=True, type="primary"):
                st.session_state.current_q_index += 1
                st.session_state.show_answer = False
                st.session_state.stored_user_answer = ""
                st.session_state.q_start_time = time.time()
                st.rerun()

        st.markdown("---")
        if st.button("🛑 إنهاء الاختبار والعودة للإعدادات"):
            st.session_state.quiz_started = False
            st.rerun()
