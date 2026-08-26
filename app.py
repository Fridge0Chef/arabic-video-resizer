import streamlit as st
import subprocess
import os
import tempfile

# إعدادات الصفحة
st.set_page_config(
    page_title="مُحرر وقاص الفيديوهات الذكي",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="expanded"
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
    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- الشريط الجانبي لحفظ الحسابات لمرة واحدة -----------------
st.sidebar.markdown("### ⚙️ حفظ حساباتك (لمرة واحدة)")
st.sidebar.write("أدخل معرّفاتك هنا مرة واحدة وستجدها جاهزة للاختيار دائماً:")

snap_handle = st.sidebar.text_input("👻 سناب شات:", placeholder="@user_snap")
tiktok_handle = st.sidebar.text_input("🎵 تيك توك:", placeholder="@user_tiktok")
ig_handle = st.sidebar.text_input("📸 إنستقرام:", placeholder="@user_ig")
x_handle = st.sidebar.text_input("𝕏 منصة إكس:", placeholder="@user_x")
yt_handle = st.sidebar.text_input("▶️ يوتيوب:", placeholder="@channel_yt")

# تجميع الحسابات المحفوظة
saved_accounts = {}
if snap_handle.strip():
    saved_accounts[f"👻 سناب شات ({snap_handle.strip()})"] = f"Snap: {snap_handle.strip()}"
if tiktok_handle.strip():
    saved_accounts[f"🎵 تيك توك ({tiktok_handle.strip()})"] = f"TikTok: {tiktok_handle.strip()}"
if ig_handle.strip():
    saved_accounts[f"📸 إنستقرام ({ig_handle.strip()})"] = f"IG: {ig_handle.strip()}"
if x_handle.strip():
    saved_accounts[f"𝕏 منصة إكس ({x_handle.strip()})"] = f"X: {x_handle.strip()}"
if yt_handle.strip():
    saved_accounts[f"▶️ يوتيوب ({yt_handle.strip()})"] = f"YouTube: {yt_handle.strip()}"

# ----------------- الواجهة الرئيسية -----------------
st.markdown('<h1 class="main-title">🎬 استوديو تعديل الفيديو ووضع الحسابات</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">عدّل الأبعاد، احجب الشعار القديم، وضع حسابك المفضل بضغطة زر</p>', unsafe_allow_html=True)

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

uploaded_file = st.file_uploader("اختر مقطع الفيديو أو اسحبه هنا (MP4, MOV, MKV)", type=["mp4", "mov", "mkv"])

if uploaded_file is not None:
    st.video(uploaded_file)
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        selected_platform = st.selectbox("🎯 اختر المنصة المستهدفة:", list(PLATFORMS.keys()))
    with col2:
        selected_style = st.selectbox("🎨 نمط ملء الشاشة:", list(STYLES.keys()))

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
    
    # خيار وضع الحساب المحفوظ
    enable_stamp = st.checkbox("✨ وضع أحد حساباتي المحفوظة فوق الفيديو", value=True)
    
    extra_filters = ""
    if enable_stamp:
        if not saved_accounts:
            st.info("💡 اكتب معرّف حسابك أولاً في القائمة الجانبية (يمين الشاشة) ليظهر لك هنا.")
        else:
            col_sel1, col_sel2 = st.columns(2)
            with col_sel1:
                chosen_label = st.selectbox("👤 اختر الحساب المراد وضعه:", list(saved_accounts.keys()))
            with col_sel2:
                acc_pos = st.selectbox(
                    "📍 موضع وضع الحساب في المقطع:",
                    [
                        "تغطية علامة تيك توك (أعلى اليسار)",
                        "تغطية علامة تيك توك السفلية (أسفل اليمين)",
                        "تغطية العلامتين معاً (أعلى اليسار وأسفل اليمين)",
                        "أعلى اليمين",
                        "أسفل اليسار"
                    ]
                )

            final_text = saved_accounts[chosen_label]
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

    if st.button("🚀 معالجة وتثبيت الحساب على المقطع"):
        with st.spinner("جاري التعديل وإضافة الحساب..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as in_temp:
                in_temp.write(uploaded_file.read())
                input_path = in_temp.name
            
            output_path = tempfile.mktemp(suffix=".mp4")

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
                
                st.success(f"✅ تمت المعالجة بنجاح! (حجم الملف: {file_size_mb:.2f} ميجابايت)")
                st.video(output_path)

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="⬇️ تحميل المقطع بالحساب المحدد",
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
