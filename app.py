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

# تنسيق الواجهة ودعم الجوال وRTL
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    * {
        font-family: 'Cairo', sans-serif !important;
    }
    .main-title { 
        text-align: center; 
        font-weight: 800; 
        color: #1E293B; 
        font-size: 1.5rem;
        margin-top: 0;
        margin-bottom: 0.2rem; 
    }
    .sub-title { 
        text-align: center; 
        color: #64748B; 
        font-size: 0.9rem;
        margin-bottom: 1.2rem; 
    }
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 42px !important;
        height: 42px !important;
        padding: 0 !important;
        font-size: 1.2rem !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    div.stButton > button {
        width: 100%; 
        background-color: #2563EB; 
        color: white; 
        font-weight: 700;
        border-radius: 10px; 
        padding: 0.6rem 1rem; 
        border: none; 
        transition: 0.3s;
    }
    div.stButton > button:hover { 
        background-color: #1D4ED8; 
        color: white; 
    }
</style>
""", unsafe_allow_html=True)

# ----------------- زر الإعدادات العلوي -----------------
head_col1, head_col2 = st.columns([1, 7])
with head_col1:
    with st.popover("⚙️"):
        st.markdown("#### ⚙️ حفظ حساباتك")
        snap_handle = st.text_input("👻 سناب شات:", key="snap", placeholder="shared.2017")
        tiktok_handle = st.text_input("🎵 تيك توك:", key="tiktok", placeholder="user_tiktok")
        ig_handle = st.text_input("📸 إنستقرام:", key="ig", placeholder="user_ig")
        x_handle = st.text_input("𝕏 منصة إكس:", key="x", placeholder="user_x")
        yt_handle = st.text_input("▶️ يوتيوب:", key="yt", placeholder="channel_yt")

# تجميع الحسابات المحفوظة
saved_accounts = {}
if st.session_state.get("snap", "").strip():
    clean_snap = st.session_state.snap.strip().lstrip('@')
    saved_accounts[f"👻 سناب شات (@{clean_snap})"] = f"Snap @{clean_snap}"
if st.session_state.get("tiktok", "").strip():
    clean_tt = st.session_state.tiktok.strip().lstrip('@')
    saved_accounts[f"🎵 تيك توك (@{clean_tt})"] = f"TikTok @{clean_tt}"
if st.session_state.get("ig", "").strip():
    clean_ig = st.session_state.ig.strip().lstrip('@')
    saved_accounts[f"📸 إنستقرام (@{clean_ig})"] = f"IG @{clean_ig}"
if st.session_state.get("x", "").strip():
    clean_x = st.session_state.x.strip().lstrip('@')
    saved_accounts[f"𝕏 منصة إكس (@{clean_x})"] = f"X @{clean_x}"
if st.session_state.get("yt", "").strip():
    clean_yt = st.session_state.yt.strip().lstrip('@')
    saved_accounts[f"▶️ يوتيوب (@{clean_yt})"] = f"YouTube @{clean_yt}"

st.markdown('<h1 class="main-title">🎬 استوديو تعديل الفيديو ووضع الحسابات</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">عدّل الأبعاد، احجب الشعار القديم، وضع حسابك المفضل بضغطة زر</p>', unsafe_allow_html=True)

# ----------------- خيارات المنصات والمعالجة -----------------
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
        "📦 حجم ومساحة الملف النهائي:",
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
        font_size = "26"
    elif "حجم متوازن" in size_mode:
        target_w = PLATFORMS[selected_platform]["w"]
        target_h = PLATFORMS[selected_platform]["h"]
        crf_val = "24"
        font_size = "36"
    else:
        target_w = PLATFORMS[selected_platform]["w"]
        target_h = PLATFORMS[selected_platform]["h"]
        crf_val = "20"
        font_size = "36"

    style_code = STYLES[selected_style]

    st.divider()
    
    enable_stamp = st.checkbox("✨ وضع أحد حساباتي المحفوظة فوق الفيديو", value=True)
    
    extra_filters = ""
    if enable_stamp:
        if not saved_accounts:
            st.info("💡 اضغط على أيقونة الترس ⚙️ في أعلى الصفحة واكتب حسابك ليظهر لك في القائمة.")
        else:
            col_sel1, col_sel2 = st.columns(2)
            with col_sel1:
                chosen_label = st.selectbox("👤 اختر الحساب:", list(saved_accounts.keys()))
            with col_sel2:
                acc_pos = st.selectbox(
                    "📍 موضع الشارة في المقطع:",
                    [
                        "تغطية علامة تيك توك (أعلى اليسار)",
                        "تغطية علامة تيك توك السفلية (أسفل اليمين)",
                        "تغطية العلامتين معاً (أعلى اليسار وأسفل اليمين)",
                        "أعلى اليمين",
                        "أسفل اليسار"
                    ]
                )

            final_text = saved_accounts[chosen_label].replace(":", "\\:").replace("'", "")
            box_style = f"box=1:boxcolor=black@0.85:boxborderw=12:fontcolor=white:fontsize={font_size}"
            
            if acc_pos == "تغطية علامة تيك توك (أعلى اليسار)":
                extra_filters = f",drawtext=text='{final_text}':x=30:y=40:{box_style}"
            elif acc_pos == "تغطية علامة تيك توك السفلية (أسفل اليمين)":
                extra_filters = f",drawtext=text='{final_text}':x=w-tw-40:y=h-th-80:{box_style}"
            elif acc_pos == "تغطية العلامتين معاً (أعلى اليسار وأسفل اليمين)":
                extra_filters = f",drawtext=text='{final_text}':x=30:y=40:{box_style},drawtext=text='{final_text}':x=w-tw-40:y=h-th-80:{box_style}"
            elif acc_pos == "أعلى اليمين":
                extra_filters = f",drawtext=text='{final_text}':x=w-tw-40:y=40:{box_style}"
            elif acc_pos == "أسفل اليسار":
                extra_filters = f",drawtext=text='{final_text}':x=30:y=h-th-80:{box_style}"

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
                "-i", input_path,
                "-filter_complex", filter_complex,
                "-map", "[outv]",
                "-map", "0:a?",
                "-c:v", "libx264",
                "-preset", "ultrafast",
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
