import streamlit as st
import subprocess
import os
import tempfile

# إعدادات الصفحة
st.set_page_config(
    page_title="مُحرر وقاص الفيديوهات الذكي",
    page_icon="🎬",
    layout="centered"
)

# تخصيص واجهة عربية حديثة ودعم RTL
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"], .stMarkdown, .stButton, .stSelectbox, .stCheckbox, .stSlider {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    .main-title {
        text-align: center;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        text-align: center;
        color: #64748B;
        margin-bottom: 2rem;
    }
    div.stButton > button {
        width: 100%;
        background-color: #2563EB;
        color: white;
        font-weight: 700;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        border: none;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background-color: #1D4ED8;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🎬 استوديو تعديل الفيديو وإزالة العلامات المائية</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">عدّل مقاطعك للمنصات وأزل الشعارات والعلامات المائية بضغطة زر واحدة</p>', unsafe_allow_html=True)

# أبعاد المنصات
PLATFORMS = {
    "تيك توك / سناب شات / يوتيوب شورتس (9:16)": {"w": 1080, "h": 1920, "name": "9_16_Vertical"},
    "ريلز إنستقرام (9:16)": {"w": 1080, "h": 1920, "name": "Reels_9_16"},
    "بوست إنستقرام عمودي (4:5)": {"w": 1080, "h": 1350, "name": "IG_Feed_4_5"},
    "منشور إكس / تويتر مربع (1:1)": {"w": 1080, "h": 1080, "name": "Square_1_1"},
    "يوتيوب كلاسيكي أفقي (16:9)": {"w": 1920, "h": 1080, "name": "Landscape_16_9"},
}

# أنماط ملء الشاشة
STYLES = {
    "خلفية ضبابية ذكية (Blurred Background)": "blur",
    "قص وتكبير لملء الشاشة (Center Crop)": "crop",
    "إضافة إطار أسود كلاسيكي (Fit with Black Bars)": "fit"
}

# 1. رفع المقطع
uploaded_file = st.file_uploader("اختر مقطع الفيديو أو اسحبه هنا (MP4, MOV, MKV)", type=["mp4", "mov", "mkv"])

if uploaded_file is not None:
    st.video(uploaded_file)
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        selected_platform = st.selectbox("🎯 اختر المنصة المستهدفة:", list(PLATFORMS.keys()))
    with col2:
        selected_style = st.selectbox("🎨 نمط ملء الشاشة:", list(STYLES.keys()))

    target_w = PLATFORMS[selected_platform]["w"]
    target_h = PLATFORMS[selected_platform]["h"]
    style_code = STYLES[selected_style]

    st.divider()
    
    # خيارات إزالة العلامة المائية
    remove_wm = st.checkbox("🧹 تفعيل ميزة إزالة / تمويه العلامة المائية (Delogo)")
    
    delogo_filter = ""
    if remove_wm:
        wm_position = st.selectbox(
            "📍 اختر موضع الشعار أو العلامة المائية:",
            [
                "علامة تيك توك التلقائية (أعلى اليسار + أسفل اليمين)",
                "أعلى اليسار",
                "أعلى اليمين",
                "أسفل اليسار",
                "أسفل اليمين",
                "موضع مخصص (تحديد يدوي)"
            ]
        )
        
        if wm_position == "علامة تيك توك التلقائية (أعلى اليسار + أسفل اليمين)":
            delogo_filter = f",delogo=x=20:y=30:w=260:h=110,delogo=x={target_w - 280}:y={target_h - 140}:w=260:h=110"
        elif wm_position == "أعلى اليسار":
            delogo_filter = ",delogo=x=20:y=30:w=280:h=120"
        elif wm_position == "أعلى اليمين":
            delogo_filter = f",delogo=x={target_w - 300}:y=30:w=280:h=120"
        elif wm_position == "أسفل اليسار":
            delogo_filter = f",delogo=x=20:y={target_h - 150}:w=280:h=120"
        elif wm_position == "أسفل اليمين":
            delogo_filter = f",delogo=x={target_w - 300}:y={target_h - 150}:w=280:h=120"
        else:
            col_x, col_y = st.columns(2)
            with col_x:
                custom_x = st.slider("الإحداثي الأفقي (X):", 0, target_w - 100, 50)
                custom_w = st.slider("عرض منطقة التمويه (W):", 50, 500, 200)
            with col_y:
                custom_y = st.slider("الإحداثي الرأسي (Y):", 0, target_h - 50, 50)
                custom_h = st.slider("ارتفاع منطقة التمويه (H):", 30, 300, 100)
            delogo_filter = f",delogo=x={custom_x}:y={custom_y}:w={custom_w}:h={custom_h}"

    if st.button("🚀 ابدأ المعالجة وإزالة العلامة المائية الآن"):
        with st.spinner("جاري المعالجة وإعادة التشكيل... يرجى الانتظار ثوانٍ"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as in_temp:
                in_temp.write(uploaded_file.read())
                input_path = in_temp.name
            
            output_path = tempfile.mktemp(suffix=".mp4")

            # بناء الفلاتر مع تصحيح الأبعاد الزوجية التلقائي
            if style_code == "blur":
                vf_filter = (
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
                    f"crop={target_w}:{target_h},boxblur=20:20[bg];"
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
                    f"scale=trunc(iw/2)*2:trunc(ih/2)*2[fg];"
                    f"[bg][fg]overlay=(W-w)/2:(H-h)/2{delogo_filter}"
                )
            elif style_code == "crop":
                vf_filter = (
                    f"scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
                    f"crop={target_w}:{target_h}{delogo_filter}"
                )
            else: # fit
                vf_filter = (
                    f"scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
                    f"scale=trunc(iw/2)*2:trunc(ih/2)*2,"
                    f"pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2:black{delogo_filter}"
                )

            cmd = [
                "ffmpeg", "-y",
                "-i", input_path,
                "-vf", vf_filter,
                "-map", "0:v:0",
                "-map", "0:a:0?",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-preset", "veryfast",
                "-crf", "22",
                "-c:a", "aac",
                "-b:a", "128k",
                output_path
            ]

            try:
                res = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                st.success("✅ تمت المعالجة وإزالة الشعار بنجاح!")
                st.video(output_path)

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="⬇️ تحميل المقطع بدون علامة مائية",
                        data=f,
                        file_name=f"clean_{PLATFORMS[selected_platform]['name']}.mp4",
                        mime="video/mp4"
                    )
            except subprocess.CalledProcessError as e:
                err_msg = e.stderr.decode('utf-8', errors='ignore')
                st.error("حدث خطأ أثناء معالجة الفيديو بواسطة FFmpeg:")
                st.code(err_msg[-400:] if len(err_msg) > 400 else err_msg)
            finally:
                if os.path.exists(input_path):
                    os.remove(input_path)
