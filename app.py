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
# ==========================================
# 1. منطقة إدخال البيانات (قم بتعبئتها أنت)
# ==========================================
# اكتب اسم الشريحة أو التشخيص بين علامتي التنصيص
# ==========================================
# 1. منطقة إدخال البيانات
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
    "img97.jpg": "Boxer (Pugilistic) attitude. Cause: exposure to extreme heat. Mechanism: coagulation and contraction of muscle proteins مش نفسها لكن زي ها",
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
    "img144.jpg": "blue arrow Contact pallor due to compression of blood vessels red arrow : hypostasis chery red color due to CO posion or cynaid po or cold ى والح لكن نفس مع تمش نفس صورة بزبط ل",
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