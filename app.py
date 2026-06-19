import streamlit as st
import random
import time
import os
from PIL import Image

# ==========================================
# 1. إعدادات الصفحة والتصميم الاحترافي (CSS)
# ==========================================
st.set_page_config(page_title="Forensic Slides Pro", page_icon="🔬", layout="centered")

def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
    }

    /* تصميم العنوان الاحترافي */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #b91c1c 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }

    /* كرت السؤال */
    .question-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-right: 5px solid #1e3a8a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* مؤقت الحماس */
    .timer-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    .timer-circle {
        font-size: 2.5rem;
        font-weight: bold;
        color: #b91c1c;
        border: 4px solid #b91c1c;
        border-radius: 50%;
        width: 90px;
        height: 90px;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: white;
        box-shadow: 0 0 15px rgba(185, 28, 28, 0.3);
    }

    /* تخصيص الأزرار */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #1e3a8a;
        color: white;
        font-weight: bold;
        font-size: 1.1em;
        transition: all 0.3s ease;
        border: none;
    }
    .stButton>button:hover {
        background-color: #b91c1c;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# ==========================================
# 2. البيانات (الصور والأسئلة)
# ==========================================
# مأخوذة من المصادر [4-6]
SLIDES_DATA = {
    "img35.jpg": {"q": "Identify the type of injury and its cause.", "a": "Extensive bruises/ contusions cause by blunt truma"},
    "img36.jpg": {"q": "Identify the type of fracture and the instrument used.", "a": "cut fracture done by a sharp heavy instrument"},
    "img46.jpg": {"q": "What is the finding, and what is the differential diagnosis (D.D)?", "a": "froth secretion from mouth & nostrils D.D 1 putrefaction 2- drowning"},
    "img97.jpg": {"q": "Identify the attitude, its cause, and the mechanism.", "a": "Boxer (Pugilistic) attitude. Cause: exposure to extreme heat. Mechanism: coagulation and contraction of muscle proteins"},
    "img123.jpg": {"q": "1- Identify the type of hanging. 2- Identify the phenomenon pointed by the arrow.", "a": "1- Incomplete hanging 2- Marbling phenomenon (48h in summer / 1 week in winter)"},
    # يمكنك إضافة باقي الصور هنا كما في المصادر
}

FOLDER_NAME = "forensic-slides"

# ==========================================
# 3. تهيئة الجلسة (Session State)
# ==========================================
if 'quiz_started' not in st.session_state: st.session_state.quiz_started = False
if 'current_q_index' not in st.session_state: st.session_state.current_q_index = 0
if 'selected_slides' not in st.session_state: st.session_state.selected_slides = []
if 'show_answer' not in st.session_state: st.session_state.show_answer = False
if 'use_timer' not in st.session_state: st.session_state.use_timer = True

# ==========================================
# 4. واجهة البداية
# ==========================================
st.markdown("""
<div class='main-header'>
    <h1 style='margin:0;'>🔬 Forensic Medicine Pro</h1>
    <p style='margin:0; opacity:0.8;'>محاكي اختبار شرائح الطب الشرعي التفاعلي</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.quiz_started:
    with st.container():
        st.subheader("⚙️ إعدادات الاختبار")
        num_slides = st.slider("اختر عدد الشرائح:", 1, len(SLIDES_DATA), min(10, len(SLIDES_DATA)))
        st.session_state.use_timer = st.checkbox("تفعيل مؤقت الحماس (30 ثانية لكل سؤال)", value=True)
        
        if st.button("🚀 ابدأ التحدي الآن"):
            all_keys = list(SLIDES_DATA.keys())
            st.session_state.selected_slides = random.sample(all_keys, num_slides)
            st.session_state.quiz_started = True
            st.session_state.current_q_index = 0
            st.session_state.show_answer = False
            st.rerun()

# ==========================================
# 5. واجهة الاختبار والمؤقت
# ==========================================
else:
    slides = st.session_state.selected_slides
    idx = st.session_state.current_q_index
    total = len(slides)
    img_name = slides[idx]
    
    # شريط التقدم
    st.write(f"الشريحة {idx+1} من {total}")
    st.progress((idx + 1) / total)

    # عرض الصورة
    img_path = os.path.join(FOLDER_NAME, img_name)
    try:
        image = Image.open(img_path)
        st.image(image, use_container_width=True)
    except:
        st.error(f"⚠️ الصورة {img_name} غير موجودة في مجلد {FOLDER_NAME}")

    # كرت السؤال
    st.markdown(f"""
    <div class='question-card'>
        <h3 style='color:#1e3a8a; margin-top:0;'>❓ السؤال:</h3>
        <p style='font-size:1.2em;'>{SLIDES_DATA[img_name]['q']}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- ميزة مؤقت الحماس ---
    if st.session_state.use_timer and not st.session_state.show_answer:
        timer_placeholder = st.empty()
        for seconds in range(30, -1, -1):
            timer_placeholder.markdown(f"""
                <div class='timer-container'>
                    <div class='timer-circle'>{seconds}</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
            if st.session_state.show_answer: 
                break
        if seconds == 0:
            st.warning("⚠️ انتهى الوقت! اضغط على 'إظهار الإجابة'.")

    # أزرار التحكم
    if not st.session_state.show_answer:
        if st.button("💡 إظهار الإجابة النموذجية"):
            st.session_state.show_answer = True
            st.rerun()
    else:
        st.success(f"✅ الإجابة: {SLIDES_DATA[img_name]['a']}")
        
        col1, col2 = st.columns(2)
        with col1:
            if idx + 1 < total:
                if st.button("➡️ السؤال التالي"):
                    st.session_state.current_q_index += 1
                    st.session_state.show_answer = False
                    st.rerun()
            else:
                if st.button("🏁 إنهاء المراجعة"):
                    st.session_state.quiz_started = False
                    st.rerun()
        with col2:
            if st.button("🔄 إعادة الاختبار"):
                st.session_state.quiz_started = False
                st.rerun()
