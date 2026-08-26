import streamlit as st
import subprocess
import os
import tempfile

# إعدادات الصفحة
st.set_page_config(
    page_title="استوديو تعديل الفيديو الذكي",
    page_icon="🎬",
    layout="centered"
)

# تخصيص واجهة عربية كاملة، إخفاء القوائم الإنجليزية، وتصحيح الأيقونات
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"], .stMarkdown, .stButton, .stSelectbox, .stCheckbox, .stSlider, .stRadio, .stTextInput, label, p, span {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    /* إخفاء القوائم العلوية والسفلية الإنجليزية الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    [data-testid="stToolbar"] {display: none;}
    
    /* تعريب زر رفع الملفات */
    [data-testid="stFileUploader"] section button {
        font-size: 0 !important;
    }
    [data-testid="stFileUploader"] section button::after {
        content: "📁 اختر الفيديو من جهازك";
        font-size: 0.95rem !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: 700;
    }
    [data-testid="stFileUploader"] small {
        font-size: 0 !important;
    }
    [data-testid="stFileUploader"] small::after {
        content: "الحد الأقصى 200 ميجابايت • صيغ الفيديو: MP4, MOV, MKV";
        font-size: 0.8rem !important;
        font-family: 'Cairo', sans-serif !important;
        color: #94A3B8;
        display: block;
        margin-top: 5px;
    }
    
    .main-title { 
        text-align: center; 
        font-weight: 800; 
        color: #1E293B; 
        font-size: 1.5rem;
        margin-top: 0.5rem;
        margin-bottom: 0.2rem; 
    }
    .sub-title { 
        text-align: center; 
        color: #64748B; 
        font-size: 0.9rem;
        margin-bottom: 1.2rem; 
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

# ----------------- أيقونة الإعدادات العلوية وتثبيت الحسابات -----------------
with st.popover("⚙️ تعديل الحسابات المحفوظة"):
    st.markdown("#### ⚙️ الحسابات الافتراضية")
    snap_handle = st.text_input("👻 حساب سناب شات:", value="Fig.fig.", key="snap")
    tiktok_handle = st.text_input("🎵 حساب تيك توك:", value="arb.virtualventurex", key="tiktok")
    ig_handle = st.text_input("📸 حساب إنستقرام:", value="arb.virtualventurex", key="ig")
    x_handle = st.text_input("𝕏 حساب منصة إكس:", value="ahmadtawfir", key="x")
    yt_handle = st.text_input("▶️ حساب يوتيوب:", value="abu10shaher", key="yt")

# تجميع وتجهيز الحسابات
saved_accounts = {}
if st.session_state.get("snap", "Fig.fig.").strip():
    clean_snap = st.session_state.get("snap", "Fig.fig.").strip().lstrip('@')
    saved_accounts[f"👻 سناب شات (@{clean_snap})"] = f"Snap @{clean_snap}"

if st.session_state.get("tiktok", "arb.virtualventurex").strip():
    clean_tt = st.session_state.get("tiktok", "arb.virtualventurex").strip().lstrip('@')
    saved_accounts[f"🎵 تيك توك (@{clean_tt})"] = f"TikTok @{clean_tt}"

if st.session_state.get("ig", "arb.virtualventurex").strip():
    clean_ig = st.session_state.get("ig", "arb.virtualventurex").strip().lstrip('@')
    saved_accounts[f"📸 إنستقرام (@{clean_ig})"] = f"IG @{clean_ig}"

if st.session_state.get("x", "ahmadtawfir").strip():
    clean_x = st.session_state.get("x", "ahmadtawfir").strip().lstrip('@')
    saved_accounts[f"𝕏 منصة إكس (@{clean_x})"] = f"X @{clean_x}"

if st.session_state.get("yt", "abu10shaher").strip():
    clean_yt = st.session_state.get("yt", "abu10shaher").strip().lstrip('@')
    saved_accounts[f"▶️ يوتيوب (@{clean_yt})"] = f"YouTube @{clean_yt}"

st.markdown('<h1 class="main-title">🎬 استوديو تعديل وتجهيز الفيديوهات</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">عدّل الأبعاد، قص المقاطع، ضع عنواناً جذاباً، واستبدل الشعار بحساباتك</p>', unsafe_allow_html=True)

# ----------------- خيارات المنصات -----------------
PLATFORMS = {
    "تيك توك / سناب شات / شورتس (طولي 9:16)": {"w": 1080, "h": 1920, "w_low": 720, "h_low": 1280, "name": "9_16_Vertical"},
    "ريلز إنستقرام (طولي 9:16)": {"w": 1080, "h": 1920, "w_low": 720, "h_low": 1280, "name": "Reels_9_16"},
    "بوست إنستقرام عمودي (مقاس 4:5)": {"w": 1080, "h": 1350, "w_low": 720, "h_low": 900, "name": "IG_Feed_4_5"},
    "منشور إكس / تويتر (مربع 1:1)": {"w": 1080, "h": 1080, "w_low": 720, "h_low": 720, "name": "Square_1_1"},
    "يوتيوب كلاسيكي (أفقي 16:9)": {"w": 1920, "h": 1080, "w_low": 1280, "h_low": 720, "name": "Landscape_16_9"},
}

STYLES = {
    "خلفية ضبابية ذكية (تمويه سينمائي)": "blur",
    "قص وتكبير لملء كامل الشاشة": "crop",
    "إضافة إطار أسود كلاسيكي": "fit"
}

uploaded_file = st.file_uploader("اختر مقطع الفيديو أو اسحبه هنا:", type=["mp4", "mov", "mkv"])

if uploaded_file is not None:
    st.video(uploaded_file)
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        selected_platform = st.selectbox("🎯 اختر المنصة المستهدفة:", list(PLATFORMS.keys()))
    with col2:
        selected_style = st.selectbox("🎨 نمط العرض والتنسيق:", list(STYLES.keys()))

    size_mode = st.radio(
        "📦 خيارات المساحة وحجم الملف النهائي:",
        [
            "⚡ حجم خفيف جداً ومضغوط (توفير فائق للمساحة وسرعة في التنزيل)",
            "⚖️ حجم متوازن (دقة ممتازة وجودة قياسية)",
            "💎 أعلى دقة متوفرة"
        ]
    )

    if "حجم خفيف جداً" in size_mode:
        target_w = PLATFORMS[selected_platform]["w_low"]
        target_h = PLATFORMS[selected_platform]["h_low"]
        crf_val = "28"
        font_size = 26
    elif "حجم متوازن" in size_mode:
        target_w = PLATFORMS[selected_platform]["w"]
        target_h = PLATFORMS[selected_platform]["h"]
        crf_val = "24"
        font_size = 36
    else:
        target_w = PLATFORMS[selected_platform]["w"]
        target_h = PLATFORMS[selected_platform]["h"]
        crf_val = "20"
        font_size = 36

    style_code = STYLES[selected_style]

    st.divider()

    # 1. قص أطراف الفيديو (Trimming)
    enable_trim = st.checkbox("✂️ قص جزء من الفيديو (حذف البداية أو النهاية)")
    start_time, end_time = 0, 0
    if enable_trim:
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            start_time = st.number_input("وقت البداية (بالثواني):", min_value=0, value=0, step=1)
        with col_t2:
            end_time = st.number_input("وقت النهاية (بالثواني - ضع 0 للوصول إلى نهاية المقطع):", min_value=0, value=0, step=1)

    # 2. شريط العنوان الجذاب (Headline Bar)
    enable_hook = st.checkbox("🔥 إضافة شريط عنوان رئيسي جذاب فوق الفيديو")
    hook_filter = ""
    if enable_hook:
        hook_text = st.text_input("نص العنوان الرئيسي:", placeholder="مثال: شاهد للنهاية 😱🔥")
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            hook_bg = st.selectbox("لون خلفية الشريط:", ["أصفر 🟨", "أسود ⬛", "أحمر 🟥", "أبيض ⬜"])
        with col_h2:
            hook_color = "black" if hook_bg in ["أصفر 🟨", "أبيض ⬜"] else "white"
            st.info(f"🎨 لون الخط التلقائي: {hook_color}")

        if hook_text.strip():
            clean_hook = hook_text.strip().replace(":", "\\:").replace("'", "")
            bg_map = {
                "أصفر 🟨": "yellow@0.95",
                "أسود ⬛": "black@0.90",
                "أحمر 🟥": "red@0.90",
                "أبيض ⬜": "white@0.95"
            }
            hook_bg_val = bg_map[hook_bg]
            hook_font_size = font_size + 8
            hook_filter = f",drawtext=text='{clean_hook}':x=(w-text_w)/2:y=80:fontsize={hook_font_size}:fontcolor={hook_color}:box=1:boxcolor={hook_bg_val}:boxborderw=14"

    # 3. وضع الحساب المحفوظ
    enable_stamp = st.checkbox("✨ وضع أحد حساباتي لتغطية الشعار والحساب القديم", value=True)
    stamp_filter = ""
    if enable_stamp and saved_accounts:
        col_sel1, col_sel2 = st.columns(2)
        with col_sel1:
            chosen_label = st.selectbox("👤 اختر الحساب المراد إبرازه:", list(saved_accounts.keys()))
        with col_sel2:
            acc_pos = st.selectbox(
                "📍 موضع الشارة على الفيديو:",
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
            stamp_filter = f",drawtext=text='{final_text}':x=30:y=40:{box_style}"
        elif acc_pos == "تغطية علامة تيك توك السفلية (أسفل اليمين)":
            stamp_filter = f",drawtext=text='{final_text}':x=w-tw-40:y=h-th-80:{box_style}"
        elif acc_pos == "تغطية العلامتين معاً (أعلى اليسار وأسفل اليمين)":
            stamp_filter = f",drawtext=text='{final_text}':x=30:y=40:{box_style},drawtext=text='{final_text}':x=w-tw-40:y=h-th-80:{box_style}"
        elif acc_pos == "أعلى اليمين":
            stamp_filter = f",drawtext=text='{final_text}':x=w-tw-40:y=40:{box_style}"
        elif acc_pos == "أسفل اليسار":
            stamp_filter = f",drawtext=text='{final_text}':x=30:y=h-th-80:{box_style}"

    all_text_filters = f"{hook_filter}{stamp_filter}"

    if st.button("🚀 معالجة وتجهيز المقطع الآن"):
        with st.spinner("جاري المعالجة والتعديل فائق السرعة..."):
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
                    f"[bg][fg]overlay=(W-w)/2:(H-h)/2{all_text_filters}[outv]"
                )
            elif style_code == "crop":
                filter_complex = (
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
                    f"crop={target_w}:{target_h}{all_text_filters}[outv]"
                )
            else:
                filter_complex = (
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
                    f"scale=trunc(iw/2)*2:trunc(ih/2)*2,"
                    f"pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2:black{all_text_filters}[outv]"
                )

            cmd = ["ffmpeg", "-y"]
            if enable_trim and start_time > 0:
                cmd.extend(["-ss", str(start_time)])
            if enable_trim and end_time > start_time:
                cmd.extend(["-to", str(end_time)])

            cmd.extend([
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
            ])

            try:
                res = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
                
                st.success(f"✅ تمت المعالجة بنجاح! (حجم الملف الناتج: {file_size_mb:.2f} ميجابايت)")
                st.video(output_path)

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="⬇️ تحميل المقطع الجاهز للنشر",
                        data=f,
                        file_name=f"ready_{PLATFORMS[selected_platform]['name']}.mp4",
                        mime="video/mp4"
                    )
            except subprocess.CalledProcessError as e:
                err_msg = e.stderr.decode('utf-8', errors='ignore')
                st.error("حدث خطأ أثناء معالجة الفيديو:")
                st.code(err_msg[-300:] if len(err_msg) > 300 else err_msg)
            finally:
                if os.path.exists(input_path):
                    os.remove(input_path)
