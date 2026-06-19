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
        text-align: right;
    }

    /* تصميم العنوان الاحترافي المدمج من المصادر */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #b91c1c 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }

    /* كرت السؤال - تصميم نظيف */
    .question-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border-right: 6px solid #1e3a8a;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    /* مؤقت الحماس التنازلي */
    .timer-box {
        font-size: 2.2rem;
        font-weight: bold;
        color: #b91c1c;
        text-align: center;
        border: 3px solid #b91c1c;
        border-radius: 50%;
        width: 85px;
        height: 85px;
        margin: 10px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: white;
        box-shadow: 0 0 10px rgba(185, 28, 28, 0.2);
    }

    /* تنسيق الأزرار لتكون احترافية */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #1e3a8a;
        color: white;
        font-weight: bold;
        transition: 0.3s;
        border: none;
    }
    .stButton>button:hover {
        background-color: #b91c1c;
        color: white;
        transform: scale(1.01);
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# ==========================================
# 2. البيانات (الصور والأسئلة من المصادر)
# ==========================================
SLIDES_DATA = {
    "img35.jpg": {"q": "Identify the type of injury and its cause.", "a": "Extensive bruises/ contusions cause by blunt truma"},
    "img36.jpg": {"q": "Identify the type of fracture and the instrument used.", "a": "cut fracture done by a sharp heavy instrument"},
    "img46.jpg": {"q": "What is the finding, and what is the differential diagnosis (D.D)?", "a": "froth secretion from mouth & nostrils D.D 1 putrefaction 2- drowning"},
    "img97.jpg": {"q": "Identify the attitude, its cause, and the mechanism.", "a": "Boxer (Pugilistic) attitude. Cause: exposure to extreme heat. Mechanism: coagulation and contraction of muscle proteins"},
    "img123.jpg": {"q": "1- Identify the type of hanging. 2- Identify the phenomenon pointed by the arrow.", "a": "1- Incomplete hanging 2- Marbling phenomenon (48h in summer / 1 week in winter)"},
    # يمكنك إضافة باقي البيانات من المصادر هنا [2, 5, 6]
}

FOLDER_NAME = "forensic-slides" # [3, 4]

# ==========================================
# 3. تهيئة حالة الجلسة (Session State)
# ==========================================
if 'quiz_started' not in st.session_state: st.session_state.quiz_started = False
if 'current_q_index' not in st.session_state: st.session_state.current_q_index = 0
if 'selected_slides' not in st.session_state: st.session_state.selected_slides = []
if 'show_answer' not in st.session_state: st.session_state.show_answer = False
if 'use_timer' not in st.session_state: st.session_state.use_timer = True

# ==========================================
# 4. واجهة البداية (الإعدادات)
# ==========================================
st.markdown("""
<div class='main-header'>
    <h1 style='margin:0; font-size:2em;'>🔬 Forensic Medicine Pro</h1>
    <p style='margin:0; opacity:0.9;'>نظام محاكاة اختبار الشرائح التفاعلي</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.quiz_started:
    st.subheader("🛠️ إعدادات الجلسة")
    
    # اختيار عدد السلايدات
    max_slides = len(SLIDES_DATA)
    num_to_test = st.slider("كم عدد الشرائح التي تود اختبار نفسك فيها؟", 1, max_slides, min(5, max_slides))
    
    # اختيار تفعيل المؤقت
    st.session_state.use_timer = st.toggle("تفعيل مؤقت الحماس (30 ثانية لكل سؤال)", value=True)
    
    if st.button("🚀 ابدأ الاختبار الآن"):
        all_keys = list(SLIDES_DATA.keys())
        st.session_state.selected_slides = random.sample(all_keys, num_to_test)
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
    img_name = slides[idx]
    
    # معلومات التقدم
    st.write(f"التقدم: {idx + 1} / {len(slides)}")
    st.progress((idx + 1) / len(slides))

    # عرض الصورة
    img_path = os.path.join(FOLDER_NAME, img_name)
    try:
        image = Image.open(img_path)
        st.image(image, use_container_width=True)
    except:
        st.error(f"الصورة {img_name} غير موجودة في المجلد [3].")

    # كرت السؤال
    st.markdown(f"""
    <div class='question-card'>
        <h4 style='color:#1e3a8a; margin:0;'>❓ السؤال:</h4>
        <p style='font-size:1.1em;'>{SLIDES_DATA[img_name]['q']}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- منطق المؤقت التنازلي ---
    if st.session_state.use_timer and not st.session_state.show_answer:
        timer_placeholder = st.empty()
        for seconds in range(30, -1, -1):
            timer_placeholder.markdown(f"<div class='timer-box'>{seconds}</div>", unsafe_allow_html=True)
            time.sleep(1)
            if st.session_state.show_answer: # توقف إذا ضغط المستخدم على إظهار الإجابة
                break
        if seconds == 0:
            st.warning("⚠️ انتهى الوقت! قم بإظهار الإجابة الآن.")

    # أزرار التحكم
    if not st.session_state.show_answer:
        if st.button("💡 إظهار الإجابة"):
            st.session_state.show_answer = True
            st.rerun()
    else:
        st.info(f"✅ الإجابة النموذجية: {SLIDES_DATA[img_name]['a']}")
        
        col1, col2 = st.columns(2)
        with col1:
            if idx + 1 < len(slides):
                if st.button("السؤال التالي ➡️"):
                    st.session_state.current_q_index += 1
                    st.session_state.show_answer = False
                    st.rerun()
            else:
                if st.button("🏁 إنهاء الاختبار"):
                    st.session_state.quiz_started = False
                    st.rerun()
        with col2:
            if st.button("🔄 إعادة من البداية"):
                st.session_state.quiz_started = False
                st.rerun()
