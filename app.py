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

# تخصيص واجهة عربية حديثة ودعم الاتجاه من اليمين لليسار (RTL)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"], .stMarkdown, .stButton, .stSelectbox {
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

st.markdown('<h1 class="main-title">🎬 استوديو تعديل أبعاد الفيديو للمنصات</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">عدّل مقاطعك لتناسب تيك توك، سناب شات، ريلز، وتويتر بضغطة زر مع الحفاظ على الجودة</p>', unsafe_allow_html=True)

# خيارات المنصات والأبعاد
PLATFORMS = {
    "تيك توك / سناب شات / يوتيوب شورتس (9:16)": {"w": 1080, "h": 1920, "name": "9_16_Vertical"},
    "ريلز إنستقرام (9:16)": {"w": 1080, "h": 1920, "name": "Reels_9_16"},
    "بوست إنستقرام عمودي (4:5)": {"w": 1080, "h": 1350, "name": "IG_Feed_4_5"},
    "منشور إكس / تويتر مربع (1:1)": {"w": 1080, "h": 1080, "name": "Square_1_1"},
    "يوتيوب كلاسيكي أفقي (16:9)": {"w": 1920, "h": 1080, "name": "Landscape_16_9"},
}

# خيارات أسلوب المعالجة (مثل GhostCut)
STYLES = {
    "خلفية ضبابية ذكية (Blurred Background - الأفضل للفيديوهات الأفقية)": "blur",
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

    if st.button("🚀 ابدأ المعالجة والتحويل الآن"):
        with st.spinner("جاري معالجة الفيديو بدقة عالية... يرجى الانتظار ثوانٍ معدودة"):
            # حفظ الفيديو المؤقت
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as in_temp:
                in_temp.write(uploaded_file.read())
                input_path = in_temp.name
            
            output_path = tempfile.mktemp(suffix=".mp4")

            # بناء فلتر FFmpeg حسب النمط المختار
            if style_code == "blur":
                # GhostCut Blur style: خلفية مكبرة ومموهة + الفيديو الأصلي فوقها بالمنتصف
                vf_filter = (
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
                    f"crop={target_w}:{target_h},gblur=sigma=25[bg];"
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease[fg];"
                    f"[bg][fg]overlay=(W-w)/2:(H-h)/2"
                )
            elif style_code == "crop":
                # قص ملء الشاشة مع التوسيط
                vf_filter = (
                    f"scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
                    f"crop={target_w}:{target_h}"
                )
            else: # fit / black bars
                vf_filter = (
                    f"scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
                    f"pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2:black"
                )

            # أمر FFmpeg للمعالجة السريعة
            cmd = [
                "ffmpeg", "-y",
                "-i", input_path,
                "-vf", vf_filter,
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "20",
                "-c:a", "aac",
                "-b:a", "192k",
                output_path
            ]

            try:
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                st.success("✅ تمت معالجة الفيديو بنجاح!")
                st.video(output_path)

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="⬇️ تحميل المقطع الجاهز",
                        data=f,
                        file_name=f"processed_{PLATFORMS[selected_platform]['name']}.mp4",
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error("حدث خطأ أثناء المعالجة. تأكد من سلامة ملف الفيديو.")
            finally:
                # تنظيف الملفات المؤقتة
                if os.path.exists(input_path):
                    os.remove(input_path)