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

# تخصيص واجهة عصرية ودعم اللغة العربية
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    html, body, [class*="css"], .stMarkdown, .stButton, .stSelectbox, .stCheckbox, .stSlider, .stRadio, .stTextInput {
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

st.markdown('<h1 class="main-title">🎬 استوديو تعديل الفيديو واستبدال الحسابات</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">عدّل الأبعاد، احجب الحساب القديم، وضع معرّف حساباتك الشخصية مكانه</p>', unsafe_allow_html=True)

# أبعاد المنصات
PLATFORMS = {
    "تيك توك / سناب شات / شورتس (9:16)": {"w": 1080, "h": 1920, "w_low": 720, "h_low": 1280, "name": "9_16_Vertical"},
    "ريلز إنستقرام (9:16)": {"w": 1080, "h": 1920, "w_low": 720, "h_low": 1280, "name": "Reels_9_16"},
    "بوست إنستقرام عمودي (4:5)": {"w": 1080, "h": 1350, "w_low": 720, "h_low": 900, "name": "IG_Feed_4_5"},
    "منشور إكس / تويتر مربع (1:1)": {"w": 1080, "h": 1080, "w_low": 720, "h_low": 720, "name": "Square_1_1"},
    "يوتيوب كلاسيكي أفقي (16:9)": {"w": 1920, "h": 1080, "w_low": 1280, "h_low": 720, "name": "Landscape_16_9"},
}

STYLES = {
    "خلفية ضبابية سريعة (Blurred Background)": "blur",
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

    # خيار ضغط الحجم
    size_mode = st.radio(
        "📦 خيار حجم ومساحة الملف النهائي:",
        [
            "⚡ حجم خفيف جداً ومضغوط (توفير عالي للبيانات وسرعة فائقة)",
            "⚖️ حجم متوازن (دقة 1080p قياسية)",
            "💎 أعلى دقة ممكنة"
        ]
    )

    if "حجم خفيف جداً" in size_mode:
        target_w = PLATFORMS[selected_platform]["w_low"]
        target_h = PLATFORMS[selected_platform]["h_low"]
        crf_val = "28"
        font_size = "24"
    elif "حجم متوازن" in size_mode:
        target_w = PLATFORMS[selected_platform]["w"]
        target_h = PLATFORMS[selected_platform]["h"]
        crf_val = "24"
        font_size = "34"
    else:
        target_w = PLATFORMS[selected_platform]["w"]
        target_h = PLATFORMS[selected_platform]["h"]
        crf_val = "20"
        font_size = "34"

    style_code = STYLES[selected_style]

    st.divider()
    
    # 2. ميزة استبدال الشعار بحساباتك
    replace_account = st.checkbox("✨ استبدال الحساب / العلامة المائية بحساباتي الخاصة", value=True)
    
    extra_filters = ""
    if replace_account:
        st.write("📝 **أدخل حساباتك لتغطية الحساب القديم في المقطع:**")
        
        col_acc1, col_acc2 = st.columns(2)
        with col_acc1:
            platform_type = st.selectbox("نوع الحساب:", ["سناب شات 👻", "تيك توك 🎵", "يوتيوب ▶️", "إنستقرام 📸", "منصة إكس 𝕏", "معرّف مخصص 🏷️"])
            my_handle = st.text_input("اسم حسابك (مثال: @YourUser):", placeholder="@اسم_حسابك")
        with col_acc2:
            acc_pos = st.selectbox(
                "📍 مكان وضع حسابك:",
                [
                    "تغطية علامة تيك توك (أعلى اليسار)",
                    "تغطية علامة تيك توك السفلية (أسفل اليمين)",
                    "تغطية العلامتين معاً (أعلى اليسار وأسفل اليمين)",
                    "أعلى اليمين",
                    "أسفل اليسار"
                ]
            )

        # تجهيز النص المكتوب
        icon_prefix = {
            "سناب شات 👻": "Snap: ",
            "تيك توك 🎵": "TikTok: ",
            "يوتيوب ▶️": "YouTube: ",
            "إنستقرام 📸": "IG: ",
            "منصة إكس 𝕏": "X: ",
            "معرّف مخصص 🏷️": ""
        }[platform_type]

        final_text = f"{icon_prefix}{my_handle.strip()}" if my_handle.strip() else ""

        if final_text:
            # فلتر رسم شريط أسود أنيق وكتابة الحساب الجديد فوقه
            box_style = f"box=1:boxcolor=black@0.85:boxborderw=12:fontcolor=white:fontsize={font_size}"
            
            if acc_pos == "تغطية علامة تيك توك (أعلى اليسار)":
                extra_filters += f",drawtext=text='{final_text}':x=30:y=40:{box_style}"
            elif acc_pos == "تغطية علامة تيك توك السفلية (أسفل اليمين)":
                extra_filters += f",drawtext=text='{final_text}':x=w-tw-40:y=h-th-80:{box_style}"
            elif acc_pos == "تغطية العلامتين معاً (أعلى اليسار وأسفل اليمين)":
                extra_filters += f",drawtext=text='{final_text}':x=30:y=40:{box_style}"
                extra_filters += f",drawtext=text='{final_text}':x=w-tw-40:y=h-th-80:{box_style}"
            elif acc_pos == "أعلى اليمين":
                extra_filters += f",drawtext=text='{final_text}':x=w-tw-40:y=40:{box_style}"
            elif acc_pos == "أسفل اليسار":
                extra_filters += f",drawtext=text='{final_text}':x=30:y=h-th-80:{box_style}"

    if st.button("🚀 معالجة الفيديو ووضع حسابي الآن"):
        with st.spinner("جاري إخفاء الحساب القديم ووضع حسابك الجديد..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as in_temp:
                in_temp.write(uploaded_file.read())
                input_path = in_temp.name
            
            output_path = tempfile.mktemp(suffix=".mp4")

            # بناء الفلاتر
            if style_code == "blur":
                filter_complex = (
                    f"[0:v]scale=120:213:force_original_aspect_ratio=increase,boxblur=4:4,"
                    f"scale={target_w}:{target_h}[bg];"
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
                    f"scale=trunc(iw/2)*2:trunc(ih/2)*2[fg];"
                    f"[bg][fg]overlay=(W-w)/2:(H-h)/2{extra_filters}[outv]"
                )
            elif style_code == "crop":
                filter_complex = (
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
                    f"crop={target_w}:{target_h}{extra_filters}[outv]"
                )
            else:
                filter_complex = (
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
                    f"scale=trunc(iw/2)*2:trunc(ih/2)*2,"
                    f"pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2:black{extra_filters}[outv]"
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
                "-b:a", "128k",
                output_path
            ]

            try:
                res = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
                
                st.success(f"✅ تم وضع حسابك بنجاح! (حجم الملف: {file_size_mb:.2f} ميجابايت)")
                st.video(output_path)

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="⬇️ تحميل المقطع بحسابك الجديد",
                        data=f,
                        file_name=f"branded_{PLATFORMS[selected_platform]['name']}.mp4",
                        mime="video/mp4"
                    )
            except subprocess.CalledProcessError as e:
                err_msg = e.stderr.decode('utf-8', errors='ignore')
                st.error("حدث خطأ أثناء معالجة الفيديو:")
                st.code(err_msg[-300:] if len(err_msg) > 300 else err_msg)
            finally:
                if os.path.exists(input_path):
                    os.remove(input_path)
