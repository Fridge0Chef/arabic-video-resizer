import streamlit as st
import subprocess
import os
import tempfile
import re

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
    
    html, body, p, h1, h2, h3, h4, h5, h6, span, label, input, select, textarea {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    #MainMenu, footer, header, [data-testid="stHeader"], [data-testid="stToolbar"], 
    [data-testid="stStatusWidget"], div[class^="viewerBadge"], [data-testid="stDeployButton"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    [data-testid="stIconMaterial"], .material-symbols-rounded, .material-symbols-outlined, [data-testid="stExpanderToggleIcon"] {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        direction: ltr !important;
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

# ----------------- الإعدادات الافتراضية للحسابات -----------------
with st.popover("⚙️ تعديل الحسابات المحفوظة"):
    st.markdown("#### ⚙️ الحسابات الافتراضية")
    snap_handle = st.text_input("👻 حساب سناب شات:", value="Fig.fig.", key="snap")
    tiktok_handle = st.text_input("🎵 حساب تيك توك:", value="arb.virtualventurex", key="tiktok")
    ig_handle = st.text_input("📸 حساب إنستقرام:", value="arb.virtualventurex", key="ig")
    x_handle = st.text_input("𝕏 حساب منصة إكس:", value="ahmadtawfir", key="x")
    yt_handle = st.text_input("▶️ حساب يوتيوب:", value="abu10shaher", key="yt")

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
st.markdown('<p class="sub-title">أنماط سينمائية، قص ذكي، وتغطية الشعارات بسرعة فائقة</p>', unsafe_allow_html=True)

PLATFORMS = {
    "تيك توك / سناب شات / شورتس (طولي 9:16)": {"w": 720, "h": 1280, "name": "9_16_Vertical"},
    "ريلز إنستقرام (طولي 9:16)": {"w": 720, "h": 1280, "name": "Reels_9_16"},
    "بوست إنستقرام عمودي (مقاس 4:5)": {"w": 720, "h": 900, "name": "IG_Feed_4_5"},
    "منشور إكس / تويتر (مربع 1:1)": {"w": 720, "h": 720, "name": "Square_1_1"},
    "يوتيوب كلاسيكي (أفقي 16:9)": {"w": 1280, "h": 720, "name": "Landscape_16_9"},
}

STYLES = {
    "🌟 تمويه ضبابي سينمائي (سريع وخفيف)": "blur_fast",
    "🎙️ إطار استوديو البودكاست الحديث": "podcast_card",
    "⚡ ملء الشاشة الذكي الكامل": "crop",
    "⬛ إطار أسود كلاسيكي نقي": "fit"
}

uploaded_file = st.file_uploader("اختر مقطع الفيديو من جهازك:", type=["mp4", "mov", "mkv"])

if uploaded_file is not None:
    st.video(uploaded_file)
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        selected_platform = st.selectbox("🎯 اختر المنصة المستهدفة:", list(PLATFORMS.keys()))
    with col2:
        selected_style = st.selectbox("🎨 نمط الإخراج والتنسيق:", list(STYLES.keys()))

    target_w = PLATFORMS[selected_platform]["w"]
    target_h = PLATFORMS[selected_platform]["h"]
    style_code = STYLES[selected_style]

    st.divider()

    # خيارات القص والزوائد (تم إرجاعها بالكامل)
    col_cut1, col_cut2 = st.columns(2)
    with col_cut1:
        enable_auto_trim = st.checkbox("✂️ قص الصمت والزوائد تلقائياً", value=True)
    with col_cut2:
        cut_outro = st.checkbox("🚫 حذف خاتمة تيك توك (آخر ثانيتين)", value=True)

    # شريط العنوان الجذاب
    enable_hook = st.checkbox("🔥 إضافة شريط عنوان رئيسي جذاب فوق الفيديو")
    hook_filter = ""
    if enable_hook:
        hook_text = st.text_input("نص العنوان الرئيسي:", placeholder="مثال: سر خطير لا يفوتك 😱🔥")
        if hook_text.strip():
            clean_hook = hook_text.strip().replace(":", "\\:").replace("'", "")
            hook_filter = f",drawtext=text='{clean_hook}':x=(w-text_w)/2:y=60:fontsize=28:fontcolor=black:box=1:boxcolor=yellow@0.95:boxborderw=10"

    # وضع وحماية الحساب
    enable_stamp = st.checkbox("✨ وضع حسابي وتغطية الشعار القديم", value=True)
    stamp_filter = ""
    if enable_stamp and saved_accounts:
        col_sel1, col_sel2 = st.columns(2)
        with col_sel1:
            chosen_label = st.selectbox("👤 اختر حسابك:", list(saved_accounts.keys()))
        with col_sel2:
            acc_pos = st.selectbox(
                "📍 موضع الشارة:",
                [
                    "تغطية ذكية سريعة (أعلى اليسار + أسفل اليمين)",
                    "أعلى اليسار",
                    "أسفل اليمين",
                    "أعلى اليمين",
                    "أسفل اليسار"
                ]
            )

        final_text = saved_accounts[chosen_label].replace(":", "\\:").replace("'", "")
        box_style = "box=1:boxcolor=black@0.85:boxborderw=10:fontcolor=white:fontsize=24"
        
        if acc_pos == "تغطية ذكية سريعة (أعلى اليسار + أسفل اليمين)":
            stamp_filter = (
                f",drawbox=x=15:y=20:w=200:h=70:color=black@0.75:t=fill"
                f",drawbox=x={target_w-215}:y={target_h-90}:w=200:h=70:color=black@0.75:t=fill"
                f",drawtext=text='{final_text}':x=(w-tw)/2:y=120:{box_style}"
            )
        elif acc_pos == "أعلى اليسار":
            stamp_filter = f",drawtext=text='{final_text}':x=25:y=30:{box_style}"
        elif acc_pos == "أسفل اليمين":
            stamp_filter = f",drawtext=text='{final_text}':x=w-tw-25:y=h-th-50:{box_style}"
        elif acc_pos == "أعلى اليمين":
            stamp_filter = f",drawtext=text='{final_text}':x=w-tw-25:y=30:{box_style}"
        elif acc_pos == "أسفل اليسار":
            stamp_filter = f",drawtext=text='{final_text}':x=25:y=h-th-50:{box_style}"

    all_text_filters = f"{hook_filter}{stamp_filter}"

    if st.button("🚀 معالجة فائقة السرعة وتجهيز المقطع"):
        with st.spinner("جاري التحليل السريع وقص الزوائد وتجهيز الفيديو..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as in_temp:
                in_temp.write(uploaded_file.read())
                input_path = in_temp.name
            
            output_path = tempfile.mktemp(suffix=".mp4")

            # تحليل سريع للقص التلقائي والخاتمة
            trim_start = 0.0
            trim_end = 0.0
            try:
                detect_cmd = [
                    "ffmpeg", "-i", input_path,
                    "-af", "silencedetect=noise=-35dB:d=0.8",
                    "-f", "null", "-"
                ]
                res_detect = subprocess.run(detect_cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, timeout=10)
                out_text = res_detect.stderr
                
                dur_match = re.search(r'Duration:\s*(\d{2}):(\d{2}):([\d.]+)', out_text)
                total_dur = 0.0
                if dur_match:
                    h, m, s = dur_match.groups()
                    total_dur = int(h) * 3600 + int(m) * 60 + float(s)

                if cut_outro and total_dur > 3.0:
                    trim_end = total_dur - 2.2
                    
                if enable_auto_trim:
                    s_starts = [float(x) for x in re.findall(r'silence_start:\s*([0-9.]+)', out_text)]
                    s_ends = [float(x) for x in re.findall(r'silence_end:\s*([0-9.]+)', out_text)]
                    if s_starts and s_starts[0] < 1.5 and s_ends:
                        trim_start = s_ends[0]
            except Exception:
                pass

            # فلاتر الإخراج
            if style_code == "blur_fast":
                filter_complex = (
                    f"[0:v]scale=90:160,boxblur=3:3,scale={target_w}:{target_h}[bg];"
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
                    f"scale=trunc(iw/2)*2:trunc(ih/2)*2[fg];"
                    f"[bg][fg]overlay=(W-w)/2:(H-h)/2{all_text_filters}[outv]"
                )
            elif style_code == "podcast_card":
                filter_complex = (
                    f"color=c=#0B0F17:s={target_w}x{target_h}[bg];"
                    f"[0:v]scale={target_w}-40:{target_h}-180:force_original_aspect_ratio=decrease,"
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
            if trim_start > 0:
                cmd.extend(["-ss", str(trim_start)])
            if trim_end > trim_start:
                cmd.extend(["-to", str(trim_end)])

            cmd.extend([
                "-i", input_path,
                "-filter_complex", filter_complex,
                "-map", "[outv]",
                "-map", "0:a?",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-tune", "zerolatency",
                "-pix_fmt", "yuv420p",
                "-crf", "28",
                "-c:a", "aac",
                "-b:a", "96k",
                output_path
            ])

            try:
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
                
                st.success(f"⚡ تمت المعالجة بنجاح وسرعة فائقة! (حجم الملف: {file_size_mb:.2f} ميجابايت)")
                st.video(output_path)

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="⬇️ تحميل المقطع الجاهز",
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
