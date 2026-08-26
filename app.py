import streamlit as st
import subprocess
import os
import tempfile
import random

# إعدادات الصفحة
st.set_page_config(
    page_title="استوديو الفيديو الذكي - الفيروسي",
    page_icon="🎬",
    layout="centered"
)

# تخصيص واجهة عربية كاملة وحماية الأيقونات
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

st.markdown('<h1 class="main-title">🎬 استوديو النشر الفيروسي وتجهيز المقاطع</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">كسر بصمة التكرار، فيسات تفاعلية تلقائية، وتغطية الشعارات بسرعة فائقة</p>', unsafe_allow_html=True)

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

    # خيارات كسر البصمة والفيسات التلقائية (مفعلة تلقائياً لراحتك)
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        enable_anti_copy = st.checkbox("🛡️ كسر بصمة التكرار (تخطي حظر النسخ والإكسبلور)", value=True)
    with col_v2:
        enable_auto_emojis = st.checkbox("🎭 وضع فيسات تفاعلية تلقائياً على المقطع", value=True)

    # اختيار نمط الفيسات التلقائي
    chosen_emoji_set = "😂 🔥"
    if enable_auto_emojis:
        emoji_options = {
            "🎲 عشوائي ذكي (تلقائي)": random.choice(["😂 🔥", "😱 🤯", "👀 💯", "👏 😂", "⚡ 💥"]),
            "😂 ضحك وتفاعل (😂 🔥)": "😂 🔥",
            "😱 صدمة وإثارة (😱 🤯)": "😱 🤯",
            "👀 انتباه وتركيز (👀 💯)": "👀 💯",
            "⚡ حماس وسرعة (⚡ 💥)": "⚡ 💥"
        }
        emoji_choice = st.selectbox("نوع الفيسات التفاعلية:", list(emoji_options.keys()))
        chosen_emoji_set = emoji_options[emoji_choice]

    st.divider()

    # شريط العنوان الجذاب
    enable_hook = st.checkbox("🔥 إضافة شريط عنوان رئيسي جذاب فوق الفيديو")
    hook_filter = ""
    if enable_hook:
        hook_text = st.text_input("نص العنوان الرئيسي:", placeholder="مثال: شاهد للنهاية 😱🔥")
        if hook_text.strip():
            clean_hook = hook_text.strip().replace(":", "\\:").replace("'", "")
            hook_filter = f",drawtext=text='{clean_hook}':x=(w-text_w)/2:y=60:fontsize=28:fontcolor=black:box=1:boxcolor=yellow@0.95:boxborderw=10"

    # وضع وحماية الحساب مع التغطية الواسعة
    enable_stamp = st.checkbox("✨ وضع حسابي وتغطية الشعار القديم تماماً", value=True)
    stamp_filter = ""
    if enable_stamp and saved_accounts:
        col_sel1, col_sel2 = st.columns(2)
        with col_sel1:
            chosen_label = st.selectbox("👤 اختر حسابك:", list(saved_accounts.keys()))
        with col_sel2:
            acc_pos = st.selectbox(
                "📍 موضع الشارة:",
                [
                    "تغطية ذكية واسعة (إخفاء تام للشعارات في الزوايا)",
                    "أعلى اليسار",
                    "أسفل اليمين",
                    "أعلى اليمين",
                    "أسفل اليسار"
                ]
            )

        final_text = saved_accounts[chosen_label].replace(":", "\\:").replace("'", "")
        box_style = "box=1:boxcolor=black@0.90:boxborderw=10:fontcolor=white:fontsize=24"
        
        if acc_pos == "تغطية ذكية واسعة (إخفاء تام للشعارات في الزوايا)":
            stamp_filter = (
                f",drawbox=x=0:y=0:w=320:h=110:color=black@0.90:t=fill"
                f",drawbox=x={target_w-380}:y={target_h-160}:w=380:h=160:color=black@0.90:t=fill"
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

    # إضافة شارة الفيسات البصرية
    emoji_filter = ""
    if enable_auto_emojis and chosen_emoji_set:
        emoji_filter = f",drawtext=text='{chosen_emoji_set}':x=w-tw-30:y=40:fontsize=34:box=1:boxcolor=black@0.75:boxborderw=8"

    all_text_filters = f"{hook_filter}{stamp_filter}{emoji_filter}"

    if st.button("🚀 معالجة فورية وكسر البصمة للنشر"):
        with st.spinner("جاري كسر البصمة وإضافة التفاعلات وتجهيز المقطع للنشر..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as in_temp:
                in_temp.write(uploaded_file.read())
                input_path = in_temp.name
            
            output_path = tempfile.mktemp(suffix=".mp4")

            # تعديلات كسر البصمة اللونية للمحتوى
            color_grade = ",eq=saturation=1.04:contrast=1.03:brightness=0.01" if enable_anti_copy else ""

            if style_code == "blur_fast":
                filter_complex = (
                    f"[0:v]scale=90:160,boxblur=3:3,scale={target_w}:{target_h}[bg];"
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
                    f"scale=trunc(iw/2)*2:trunc(ih/2)*2{color_grade}[fg];"
                    f"[bg][fg]overlay=(W-w)/2:(H-h)/2{all_text_filters}[outv]"
                )
            elif style_code == "podcast_card":
                filter_complex = (
                    f"color=c=#0B0F17:s={target_w}x{target_h}[bg];"
                    f"[0:v]scale={target_w}-40:{target_h}-180:force_original_aspect_ratio=decrease,"
                    f"scale=trunc(iw/2)*2:trunc(ih/2)*2{color_grade}[fg];"
                    f"[bg][fg]overlay=(W-w)/2:(H-h)/2{all_text_filters}[outv]"
                )
            elif style_code == "crop":
                filter_complex = (
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
                    f"crop={target_w}:{target_h}{color_grade}{all_text_filters}[outv]"
                )
            else:
                filter_complex = (
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
                    f"scale=trunc(iw/2)*2:trunc(ih/2)*2{color_grade},"
                    f"pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2:black{all_text_filters}[outv]"
                )

            # تجهيز أمر FFmpeg وحذف البيانات القديمة مع تعديل السرعة الخفي
            cmd = [
                "ffmpeg", "-y",
                "-threads", "0",
                "-i", input_path,
                "-filter_complex", filter_complex,
                "-map", "[outv]",
                "-map", "0:a?",
                "-map_metadata", "-1",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-tune", "zerolatency",
                "-pix_fmt", "yuv420p",
                "-crf", "28",
                "-c:a", "aac",
                "-b:a", "96k",
                output_path
            ]

            try:
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
                
                st.success(f"🎉 تم تجهيز الفيديو وكسر بصمته بنجاح! (حجم الملف: {file_size_mb:.2f} ميجابايت)")
                st.video(output_path)

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="⬇️ تحميل المقطع الحصري الجاهز للنشر",
                        data=f,
                        file_name=f"viral_unique_{PLATFORMS[selected_platform]['name']}.mp4",
                        mime="video/mp4"
                    )
            except subprocess.CalledProcessError as e:
                err_msg = e.stderr.decode('utf-8', errors='ignore')
                st.error("حدث خطأ أثناء معالجة الفيديو:")
                st.code(err_msg[-300:] if len(err_msg) > 300 else err_msg)
            finally:
                if os.path.exists(input_path):
                    os.remove(input_path)
