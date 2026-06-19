import streamlit as st
import random
import time
import os
from PIL import Image

# إعدادات الصفحة
st.set_page_config(page_title="Forensic Slides Quiz 24/25", page_icon="🔬", layout="centered")

# ==========================================
# 1. منطقة إدخال البيانات (قم بتعبئتها أنت)
# ==========================================
# ضع اسم الصورة (مع الامتداد) كـ Key، والإجابة الصحيحة كـ Value
SLIDES_DATA = {
    "slide1.jpg": "اسم الشريحة الأولى",
    "slide2.png": "اسم الشريحة الثانية",
    "slide3.jpg": "اسم الشريحة الثالثة",
    # أضف باقي الـ 50 شريحة هنا...
    # "اسم الصورة.jpg": "الإجابة الصحيحة",
}

FOLDER_NAME = "forensic-slides"

# ==========================================
# 2. تهيئة المتغيرات (Session State)
# ==========================================
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'current_q_index' not in st.session_state:
    st.session_state.current_q_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'selected_slides' not in st.session_state:
    st.session_state.selected_slides = []
if 'q_start_time' not in st.session_state:
    st.session_state.q_start_time = 0
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""

# ==========================================
# 3. واجهة البداية (الإعدادات)
# ==========================================
if not st.session_state.quiz_started:
    st.title("🔬 محاكي امتحان شرائح الطب الشرعي - دفعة 24/25")
    st.write("أهلاً بك! اختبر نفسك في شرائح العملي للفرونسك.")
    
    total_available = len(SLIDES_DATA)
    
    if total_available == 0:
        st.warning("⚠️ الرجاء إضافة أسماء الصور والإجابات في كود بايثون أولاً.")
    else:
        # اختيار عدد الأسئلة
        num_questions = st.number_input(
            f"كم عدد الشرائح التي تريد اختبار نفسك بها؟ (الحد الأقصى {total_available})", 
            min_value=1, 
            max_value=total_available, 
            value=min(10, total_available) # الافتراضي 10 كما طلبت
        )
        
        # اختيار نوع الاختبار
        test_mode = st.radio(
            "اختر نظام الاختبار:",
            ("اختبار عادي (بدون وقت)", "اختبار بمؤقت (30 ثانية لكل شريحة)")
        )
        
        # زر البدء
        if st.button("🚀 ابدأ الاختبار"):
            # اختيار شرائح عشوائية بناء على العدد المطلوب
            all_slides = list(SLIDES_DATA.keys())
            st.session_state.selected_slides = random.sample(all_slides, num_questions)
            
            st.session_state.is_timed = "بمؤقت" in test_mode
            st.session_state.quiz_started = True
            st.session_state.current_q_index = 0
            st.session_state.score = 0
            st.session_state.feedback = ""
            st.session_state.q_start_time = time.time()
            st.rerun()

# ==========================================
# 4. واجهة الاختبار
# ==========================================
else:
    # إذا انتهى الاختبار
    if st.session_state.current_q_index >= len(st.session_state.selected_slides):
        st.title("🎉 انتهى الاختبار!")
        st.subheader(f"نتيجتك النهائية: {st.session_state.score} من {len(st.session_state.selected_slides)}")
        
        # رسالة تشجيعية
        percentage = (st.session_state.score / len(st.session_state.selected_slides)) * 100
        if percentage == 100:
            st.success("ممتاز! أنت جاهز تماماً لامتحان الفرونسك، دكتور! 🥇")
        elif percentage >= 70:
            st.info("نتيجة جيدة جداً، راجع أخطائك البسيطة وستكون بأمان. 👍")
        else:
            st.warning("تحتاج إلى المزيد من المراجعة للشرائح، لا تستسلم! 💪")
            
        if st.button("🔄 إعادة الاختبار"):
            st.session_state.quiz_started = False
            st.rerun()
            
    # إذا كان الاختبار مستمراً
    else:
        current_slide = st.session_state.selected_slides[st.session_state.current_q_index]
        correct_answer = SLIDES_DATA[current_slide]
        
        # عرض معلومات السؤال
        st.markdown(f"### الشريحة {st.session_state.current_q_index + 1} من {len(st.session_state.selected_slides)}")
        
        if st.session_state.is_timed:
            st.error("⏳ تذكر: لديك 30 ثانية فقط لهذه الشريحة!")
            
        # عرض التغذية الراجعة للسؤال السابق (إن وجدت)
        if st.session_state.feedback:
            if "صحيحة" in st.session_state.feedback:
                st.success(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)
        
        # عرض الصورة
        img_path = os.path.join(FOLDER_NAME, current_slide)
        try:
            image = Image.open(img_path)
            st.image(image, use_container_width=True)
        except FileNotFoundError:
            st.error(f"❌ لم يتم العثور على الصورة: {img_path}. تأكد من وجودها في مجلد {FOLDER_NAME}.")
            
        # نموذج الإجابة
        with st.form(key='answer_form', clear_on_submit=True):
            user_answer = st.text_input("✍️ اكتب تشخيصك / اسم الشريحة هنا:")
            submit_btn = st.form_submit_button("تأكيد الإجابة")
            
            if submit_btn:
                time_taken = time.time() - st.session_state.q_start_time
                
                # التحقق من الوقت في حال كان الوضع مؤقت
                if st.session_state.is_timed and time_taken > 30:
                    st.session_state.feedback = f"⏰ انتهى الوقت (استغرقت {int(time_taken)} ثانية)! الإجابة الصحيحة كانت: {correct_answer}"
                else:
                    # مقارنة الإجابة (تتجاهل المسافات الزائدة وحالة الأحرف لو كانت إنجليزية)
                    if user_answer.strip().lower() == correct_answer.strip().lower():
                        st.session_state.score += 1
                        st.session_state.feedback = "✅ إجابة صحيحة!"
                    else:
                        st.session_state.feedback = f"❌ إجابة خاطئة! الإجابة الصحيحة هي: {correct_answer}"
                
                # الانتقال للسؤال التالي
                st.session_state.current_q_index += 1
                st.session_state.q_start_time = time.time() # إعادة ضبط المؤقت للسؤال القادم
                st.rerun()

        # زر إنهاء الاختبار مبكراً
        if st.button("🛑 إنهاء الاختبار الآن"):
            st.session_state.quiz_started = False
            st.rerun()