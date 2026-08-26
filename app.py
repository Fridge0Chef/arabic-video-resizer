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

# تصميم الواجهة ودعم اللغة العربية
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    html, body, [class*="css"], .stMarkdown, .stButton, .stSelectbox, .stCheckbox, .stSlider, .stRadio {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    .main-title { text-align: center; font-weight: 800; color: #1E293B; margin-bottom: 0.5rem; }
    .sub-title { text-align: center; color: #64748B; margin-bottom: 2rem; }
    div.stButton > button {
        width: 100%; background-color: #2563EB; color: white; font-weight: 700;
        border-radius: 10px; padding: 0.6rem 1rem; border: none; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #1D4ED8; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🎬 استوديو تعديل وضغط الفيديو الذكي</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">عدّل الأبعاد، أزل العلامات المائية، وقلل حجم الفيديو لأقل مساحة ممكنة</p>', unsafe_allow_html=True)

# أبعاد المنصات
PLATFORMS = {
    "تيك توك / سناب شات / شورتس (9:16)": {"w": 1080, "h": 1920, "w_low": 720, "h_low": 1280, "name": "9_16_Vertical"},
    "ريلز إنستقرام (9:16)": {"w": 1080, "h": 1920, "w_low": 720, "h_low": 1280, "name": "Reels_9_16"},
    "بوست إنستقرام عمودي (4:5)": {"w": 1080, "h": 1350, "w_low": 720, "h_low": 900, "name": "IG_Feed_4_5"},
    "منشور إكس / تويتر مربع (1:1)": {"w": 1080, "h": 1080, "w_low": 720, "h_low": 720, "name": "Square_1_1"},
    "يوتيوب كلاسيكي أفقي (16:9)": {"w": 1920, "h": 1080, "w_low": 1280, "h_low": 720, "name": "Landscape_16_9"},
}

STYLES = {
    "خلفية ضبابية ذكية (Blurred Background)": "blur",
    "قص وتكبير لملء الشاشة (Center Crop)": "crop",
    "إضافة إطار أسود كلاسيكي (Fit Black Bars)": "fit"
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

    # خيار ضغط وتقليل حجم الفيديو (القيقات والميجابايت)
    size_mode = st.radio(
        "📦 خيار حجم ومساحة الملف النهائي:",
        [
            "⚡ حجم خفيف جداً ومضغوط (توفير عالي للبيانات والمساحة وسرعة فائقة)",
            "⚖️ حجم متوازن (دقة 1080p قياسية)",
            "💎 أعلى دقة ممكنة (حجم أكبر)"
        ]
    )

    if "حجم خفيف جداً" in size_mode:
        target_w = PLATFORMS[selected_platform]["w_low"]
        target_h = PLATFORMS[selected_platform]["h_low"]
        crf_val = "28"
        audio_bitrate = "96k"
    elif "حجم متوازن" in size_mode:
        target_w = PLATFORMS[selected_platform]["w"]
        target_h = PLATFORMS[selected_platform]["h"]
        crf_val = "24"
        audio_bitrate = "128k"
    else:
        target_w = PLATFORMS[selected_platform]["w"]
        target_h = PLATFORMS[selected_platform]["h"]
        crf_val = "20"
        audio_bitrate = "192k"

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
            delogo_filter = f",delogo=x=15:y=20:w=220:h=90,delogo=x={target_w - 240}:y={target_h - 110}:w=220:h=90"
        elif wm_position == "أعلى اليسار":
            delogo_filter = ",delogo=x=15:y=20:w=240:h=100"
        elif wm_position == "أعلى اليمين":
            delogo_filter = f",delogo=x={target_w - 255}:y=20:w=240:h=100"
        elif wm_position == "أسفل اليسار":
            delogo_filter = f",delogo=x=15:y={target_h - 120}:w=240:h=100"
        elif wm_position == "أسفل اليمين":
            delogo_filter = f",delogo=x={target_w - 255}:y={target_h - 120}:w=240:h=100"
        else:
            col_x, col_y = st.columns(2)
            with col_x:
                custom_x = st.slider("الإحداثي الأفقي (X):", 0, target_w - 50, 40)
                custom_w = st.slider("عرض منطقة التمويه (W):", 30, 400, 180)
            with col_y:
                custom_y = st.slider("الإحداثي الرأسي (Y):", 0, target_h - 30, 40)
                custom_h = st.slider("ارتفاع منطقة التمويه (H):", 20, 250, 80)
            delogo_filter = f",delogo=x={custom_x}:y={custom_y}:w={custom_w}:h={custom_h}"

    if st.button("🚀 ابدأ المعالجة والضغط الآن"):
        with st.spinner("جاري الضغط والمعالجة السريعة..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as in_temp:
                in_temp.write(uploaded_file.read())
                input_path = in_temp.name
            
            output_path = tempfile.mktemp(suffix=".mp4")

            # فلاتر المعالجة السريعة
            if style_code == "blur":
                filter_complex = (
                    f"[0:v]scale=120:213:force_original_aspect_ratio=increase,boxblur=4:4,"
                    f"scale={target_w}:{target_h}[bg];"
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
                    f"scale=trunc(iw/2)*2:trunc(ih/2)*2[fg];"
                    f"[bg][fg]overlay=(W-w)/2:(H-h)/2{delogo_filter}[outv]"
                )
            elif style_code == "crop":
                filter_complex = (
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
                    f"crop={target_w}:{target_h}{delogo_filter}[outv]"
                )
            else:
                filter_complex = (
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
                    f"scale=trunc(iw/2)*2:trunc(ih/2)*2,"
                    f"pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2:black{delogo_filter}[outv]"
                )

            cmd = [
                "ffmpeg", "-y",
                "-threads", "0",
                "-i", input_path,
                "-filter_complex", filter_complex,
                "-map", "[outv]",
                "-map", "0:a?",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-tune", "fastdecode",
                "-pix_fmt", "yuv420p",
                "-crf", crf_val,
                "-c:a", "aac",
                "-b:a", audio_bitrate,
                output_path
            ]

            try:
                res = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # حساب حجم الملف بعد الضغط
                file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
                
                st.success(f"✅ تمت المعالجة والضغط بنجاح! (حجم الملف الناتج: {file_size_mb:.2f} ميجابايت فقط)")
                st.video(output_path)

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="⬇️ تحميل المقطع المضغوط",
                        data=f,
                        file_name=f"compressed_{PLATFORMS[selected_platform]['name']}.mp4",
                        mime="video/mp4"
                    )
            except subprocess.CalledProcessError as e:
                err_msg = e.stderr.decode('utf-8', errors='ignore')
                st.error("حدث خطأ أثناء معالجة الفيديو:")
                st.code(err_msg[-300:] if len(err_msg) > 300 else err_msg)
            finally:
                if os.path.exists(input_path):
                    os.remove(input_path)
