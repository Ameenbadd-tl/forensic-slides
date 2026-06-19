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
    body {background-color: #F9FAFB;}
    .title-en { text-align: center; color: #1E3A8A; font-size: 2.4em; font-weight: bold; margin-bottom: 5px; font-family: 'Roboto', sans-serif;}
    .title-ar { text-align: center; color: #B91C1C; font-size: 2em; font-weight: bold; margin-top: 0px; margin-bottom: 25px; font-family: 'Tajawal', sans-serif;}
    
    .question-box {
        background-color: #EFF6FF;
        border-left: 6px solid #3B82F6;
        padding: 15px;
        border-radius: 8px;
        color: #1E3A8A;
        font-size: 1.2em;
        margin-bottom: 15px;
    }
    
    .user-answer-card {
        background-color: #F3F4F6;
        border-left: 6px solid #6B7280;
        padding: 15px;
        border-radius: 8px;
        color: #374151;
        font-size: 1.1em;
        margin-bottom: 10px;
    }

    .answer-card { 
        background-color: #F0FDF4; 
        border-left: 6px solid #16A34A; 
        padding: 15px; 
        border-radius: 8px; 
        color: #14532D; 
        font-size: 1.2em; 
        font-weight: bold; 
        margin-bottom: 20px;
    }
    
    .timer-box {
        text-align: center;
        font-size: 1.8em;
        font-weight: bold;
        color: #DC2626;
        margin: 10px 0;
    }

    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        font-size: 1.1em;
        padding: 10px 20px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1E40AF;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# البيانات (اختصار للتجربة)
# ==========================================
SLIDES_DATA = {
    "img35.jpg": {"q": "Identify the type of injury and its cause.", "a": "Extensive bruises/ contusions cause by blunt trauma"},
    "img36.jpg": {"q": "Identify the type of fracture and the instrument used.", "a": "Cut fracture done by a sharp heavy instrument"},
}

FOLDER_NAME = "forensic-slides"

# ==========================================
# Session State
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

# ==========================================
# العنوان
# ==========================================
st.markdown("<div class='title-en'>🔬 Forensic Medicine Slides Quiz</div>", unsafe_allow_html=True)
st.markdown("<div class='title-ar'>محاكي اختبار شرائح الطب الشرعي</div>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# واجهة البداية
# ==========================================
if not st.session_state.quiz_started:
    total_available = len(SLIDES_DATA)
    num_questions = st.number_input(
        f"عدد الشرائح (الأقصى {total_available}):", 
        min_value=1, 
        max_value=total_available, 
        value=min(2, total_available)
    )
    st.session_state.use_timer = st.checkbox("⏳ تفعيل تحدي المؤقت (30 ثانية)")
    
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
# واجهة الاختبار
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
        current_slide = st.session_state.selected_slides[current_q]
        slide_data = SLIDES_DATA[current_slide]
        question_text = slide_data["q"]
        correct_answer = slide_data["a"]
        
        st.markdown(f"<div class='question-box'>❓ <b>Question:</b> {question_text}</div>", unsafe_allow_html=True)
        
        img_path = os.path.join(FOLDER_NAME, current_slide)
        try:
            image = Image.open(img_path)
            st.image(image, use_container_width=True)
        except FileNotFoundError:
            st.error(f"❌ لم يتم العثور على الصورة: {current_slide}.")
        
        # المؤقت التفاعلي
        if st.session_state.use_timer and not st.session_state.show_answer:
            placeholder = st.empty()
            elapsed = int(time.time() - st.session_state.q_start_time)
            remaining = max(30 - elapsed, 0)
            placeholder.markdown(f"<div class='timer-box'>⏳ {remaining} ثانية متبقية</div>", unsafe_allow_html=True)
        
        if not st.session_state.show_answer:
            user_input = st.text_area("✍️ Write your answer here / اكتب إجابتك هنا:", height=100)
            if st.button("👁️ تأكيد وإظهار الإجابة الصحيحة", use_container_width=True):
                st.session_state.stored_user_answer = user_input
                st.session_state.time_taken = time.time() - st.session_state.q_start_time
                st.session_state.show_answer = True
                st.rerun()
        else:
            st.markdown("<b>📝 إجابتك:</b>", unsafe_allow_html=True)
            user_text = st.session_state.stored_user_answer if st.session_state.stored_user_answer.strip() else "لم تكتب شيئاً"
            st.markdown(f"<div class='user-answer-card'>{user_text}</div>", unsafe_allow_html=True)
            
            st.markdown("<b>✅ الإجابة النموذجية:</b>", unsafe_allow_html=True)
            st.markdown(f"<div class='answer-card'>{correct_answer}</div>", unsafe_allow_html=True)
            
            if st.session_state.use_timer:
                t = int(st.session_state.time_taken)
                if t <= 30:
                    st.success(f"⏱️ استغرقت {t} ثانية.")
                else:
                    st.warning(f"⚠️ استغرقت {t} ثانية (تجاوزت الـ 30 ثانية).")
            
            if st.button("➡️ السؤال التالي", use_container_width=True):
                st.session_state.current_q_index += 1
                st.session_state.show_answer = False
                st.session_state.stored_user_answer = ""
                st.session_state.q_start_time = time.time()
                st.rerun()
