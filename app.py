import streamlit as st
import subprocess
import os
import tempfile

# إعدادات الصفحة
st.set_page_config(
    page_title="استوديو تعديل وتجهيز الفيديوهات الذكي",
    page_icon="🎬",
    layout="centered"
)

# واجهة عربية كاملة، إخفاء شريط الاستضافة والأيقونات المتداخلة
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
        padding: 0.65rem 1rem; 
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

st.markdown('<h1 class="main-title">🎬 استوديو تعديل وتجهيز الفيديوهات الشامل</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">تنظيف النصوص القديمة، ملء الشاشة، ضغط ذكي 70%، وعناوين فيروسية</p>', unsafe_allow_html=True)

# خيارات المنصات
PLATFORMS = {
    "تيك توك / سناب شات / شورتس (طولي 9:16)": {"w": 720, "h": 1280, "name": "9_16_Vertical"},
    "ريلز إنستقرام (طولي 9:16)": {"w": 720, "h": 1280, "name": "Reels_9_16"},
    "بوست إنستقرام عمودي (مقاس 4:5)": {"w": 720, "h": 900, "name": "IG_Feed_4_5"},
    "منشور إكس / تويتر (مربع 1:1)": {"w": 720, "h": 720, "name": "Square_1_1"},
    "يوتيوب كلاسيكي (أفقي 16:9)": {"w": 1280, "h": 720, "name": "Landscape_16_9"},
}

# أنماط العرض والتنسيق
STYLES = {
    "⚡ ملء الشاشة الذكي الكامل (بدون هوامش سوداء)": "crop",
    "🌟 تمويه ضبابي سينمائي (سريع وخفيف)": "blur_fast",
    "🎙️ إطار استوديو البودكاست الحديث": "podcast_card",
    "⬛ إطار أسود كلاسيكي نقي": "fit"
}

uploaded_file = st.file_uploader("اختر مقطع الفيديو من جهازك:", type=["mp4", "mov", "mkv"])

if uploaded_file is not None:
    st.video(uploaded_file)
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        selected_platform = st.selectbox("🎯 المنصة المستهدفة:", list(PLATFORMS.keys()))
    with col2:
        selected_style = st.selectbox("🎨 نمط العرض والإخراج:", list(STYLES.keys()))

    target_w = PLATFORMS[selected_platform]["w"]
    target_h = PLATFORMS[selected_platform]["h"]
    style_code = STYLES[selected_style]

    st.divider()

    # 1. خيارات تنظيف الكلام والشعارات القديمة
    st.markdown("### 🧹 تنظيف وحذف الكتابات والعلامات القديمة")
    clean_mode = st.radio(
        "اختر طريقة التخلص من الكلام والعلامات في المقطع:",
        [
            "🔍 تكبير سينمائي ذكي (يقص ويطرد النصوص والعلامات الموجودة في أطراف الفيديو)",
            "⬛ تغطية علوية وسفلية شاملة (إخفاء كافة النصوص القديمة تحت أشرطة أنيقة)",
            "🔘 عادي (الاحتفاظ بكامل أبعاد المقطع الأصلي)"
        ]
    )

    st.divider()

    # 2. خيارات المعالجة والقص الأوتوماتيكي والضغط الذكي
    st.markdown("### ⚡ خيارات السرعة والتحسين التلقائي")
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        enable_auto_trim = st.checkbox(
            "✂️ قص أوتوماتيكي ذكي (حذف البداية وخاتمة تيك توك)",
            value=True,
            help="يقتطع البداية البطيئة وآخر ثانيتين تلقائياً دون أي تأخير."
        )
    with col_opt2:
        enable_freshness = st.checkbox(
            "🛡️ تجديد البصمة الرقمية (ألوان زاهية + وضوح فائق)",
            value=True,
            help="يمسح البيانات الوصفية ويضبط الألوان ليظهر كفيديو جديد أصلي."
        )

    enable_smart_compress = st.checkbox(
        "📦 ضغط الحجم بنسبة 70% مع الحفاظ التام على دقة ونقاء الشاشة",
        value=True
    )

    st.divider()

    # 3. شريط العنوان الجذاب (Hook Bar)
    enable_hook = st.checkbox("🔥 إضافة شريط عنوان رئيسي جذاب فوق الفيديو", value=True)
    hook_filter = ""
    hook_text = ""
    if enable_hook:
        hook_text = st.text_input("نص العنوان الجذاب (Hook):", placeholder="مثال: سر خطير لا يفوتك 😱🔥", value="شاهد القصة للنهاية 😱🔥")
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            hook_bg = st.selectbox("لون خلفية الشريط:", ["أصفر 🟨", "أسود ⬛", "أحمر 🟥", "أبيض ⬜"])
        with col_h2:
            hook_color = "black" if hook_bg in ["أصفر 🟨", "أبيض ⬜"] else "white"

        if hook_text.strip():
            clean_hook = hook_text.strip().replace(":", "\\:").replace("'", "")
            bg_map = {
                "أصفر 🟨": "yellow@0.95",
                "أسود ⬛": "black@0.90",
                "أحمر 🟥": "red@0.90",
                "أبيض ⬜": "white@0.95"
            }
            hook_bg_val = bg_map[hook_bg]
            hook_filter = f",drawtext=text='{clean_hook}':x=(w-text_w)/2:y=50:fontsize=26:fontcolor={hook_color}:box=1:boxcolor={hook_bg_val}:boxborderw=10"

    # 4. وضع وحماية الحساب
    enable_stamp = st.checkbox("✨ وضع حسابك في مكان بارز", value=True)
    stamp_filter = ""
    chosen_account_text = ""
    if enable_stamp and saved_accounts:
        col_sel1, col_sel2 = st.columns(2)
        with col_sel1:
            chosen_label = st.selectbox("👤 اختر حسابك:", list(saved_accounts.keys()))
            chosen_account_text = saved_accounts[chosen_label]
        with col_sel2:
            acc_pos = st.selectbox(
                "📍 موضع الشارة:",
                [
                    "أعلى المنتصف تحت العنوان",
                    "أسفل اليمين",
                    "أعلى اليسار",
                    "أسفل اليسار"
                ]
            )

        final_text = saved_accounts[chosen_label].replace(":", "\\:").replace("'", "")
        box_style = "box=1:boxcolor=black@0.85:boxborderw=10:fontcolor=white:fontsize=22"
        
        if acc_pos == "أعلى المنتصف تحت العنوان":
            stamp_filter = f",drawtext=text='{final_text}':x=(w-tw)/2:y=110:{box_style}"
        elif acc_pos == "أسفل اليمين":
            stamp_filter = f",drawtext=text='{final_text}':x=w-tw-25:y=h-th-50:{box_style}"
        elif acc_pos == "أعلى اليسار":
            stamp_filter = f",drawtext=text='{final_text}':x=25:y=30:{box_style}"
        elif acc_pos == "أسفل اليسار":
            stamp_filter = f",drawtext=text='{final_text}':x=25:y=h-th-50:{box_style}"

    # فلاتر تنظيف إضافية حسب الخيار
    clean_box_filter = ""
    if "تغطية علوية وسفلية شاملة" in clean_mode:
        clean_box_filter = f",drawbox=x=0:y=0:w={target_w}:h=170:color=black@0.95:t=fill,drawbox=x=0:y={target_h-160}:w={target_w}:h=160:color=black@0.95:t=fill"

    all_text_filters = f"{clean_box_filter}{hook_filter}{stamp_filter}"
    freshness_filter = ",eq=contrast=1.05:brightness=0.01:saturation=1.12,unsharp=3:3:0.5:3:3:0.0" if enable_freshness else ""
    full_effects = f"{freshness_filter}{all_text_filters}"

    if st.button("🚀 بدء المعالجة والتنظيف الفوري"):
        with st.spinner("جاري تنظيف المقطع ومعالجته بسرعة فائقة..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as in_temp:
                in_temp.write(uploaded_file.read())
                input_path = in_temp.name
            
            output_path = tempfile.mktemp(suffix=".mp4")

            total_duration = 0.0
            try:
                probe_cmd = [
                    "ffprobe", "-v", "error",
                    "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    input_path
                ]
                res_probe = subprocess.run(probe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=2)
                total_duration = float(res_probe.stdout.strip())
            except Exception:
                pass

            trim_start = 0.6 if enable_auto_trim else 0.0
            trim_end = 0.0
            if enable_auto_trim and total_duration > 3.5:
                trim_end = total_duration - 2.2

            # تطبيق التكبير الذكي لطرد النصوص خارج الشاشة إذا تم اختياره
            zoom_factor = "1.25" if "تكبير سينمائي ذكي" in clean_mode else "1.0"

            if style_code == "crop" or "تكبير سينمائي ذكي" in clean_mode:
                filter_complex = (
                    f"[0:v]scale={target_w}*{zoom_factor}:{target_h}*{zoom_factor}:force_original_aspect_ratio=increase,"
                    f"crop={target_w}:{target_h}{full_effects}[outv]"
                )
            elif style_code == "blur_fast":
                filter_complex = (
                    f"[0:v]scale=64:114,boxblur=2:2,scale={target_w}:{target_h}[bg];"
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
                    f"scale=trunc(iw/2)*2:trunc(ih/2)*2[fg];"
                    f"[bg][fg]overlay=(W-w)/2:(H-h)/2{full_effects}[outv]"
                )
            elif style_code == "podcast_card":
                filter_complex = (
                    f"color=c=#0B0F17:s={target_w}x{target_h}[bg];"
                    f"[0:v]scale={target_w}-40:{target_h}-180:force_original_aspect_ratio=decrease,"
                    f"scale=trunc(iw/2)*2:trunc(ih/2)*2[fg];"
                    f"[bg][fg]overlay=(W-w)/2:(H-h)/2{full_effects}[outv]"
                )
            else: # fit
                filter_complex = (
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease,"
                    f"scale=trunc(iw/2)*2:trunc(ih/2)*2,"
                    f"pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2:black{full_effects}[outv]"
                )

            crf_val = "25" if enable_smart_compress else "21"
            audio_bitrate = "128k"

            cmd = [
                "ffmpeg", "-y",
                "-threads", "0"
            ]
            
            if trim_start > 0:
                cmd.extend(["-ss", str(trim_start)])
            if trim_end > trim_start:
                cmd.extend(["-to", str(trim_end)])

            cmd.extend([
                "-i", input_path,
                "-filter_complex", filter_complex,
                "-map", "[outv]",
                "-map", "0:a?",
                "-map_metadata", "-1",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-movflags", "+faststart",
                "-pix_fmt", "yuv420p",
                "-crf", crf_val,
                "-c:a", "aac",
                "-b:a", audio_bitrate,
                output_path
            ])

            try:
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
                
                st.success(f"⚡ تم تنظيف وتجهيز المقطع بنجاح! (الحجم: {file_size_mb:.2f} ميجابايت)")
                st.video(output_path)

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="⬇️ تحميل المقطع الجاهز للنشر فوراً",
                        data=f,
                        file_name=f"cleaned_{PLATFORMS[selected_platform]['name']}.mp4",
                        mime="video/mp4"
                    )

                # قسم المحتوى والهاشتاقات الجاهزة
                st.divider()
                st.markdown("### ✍️ نماذج محتوى ونصوص جاهزة للنشر (انسخ والصق بضغطة زر):")
                
                base_title = hook_text.strip() if hook_text.strip() else "شاهد هذا المقطع العجيب"
                account_mention = f"\nتابعني للمزيد: {chosen_account_text}" if chosen_account_text else ""
                
                tab1, tab2, tab3 = st.tabs(["🔥 نص تشويقي قوي", "💬 نص تفاعلي", "🏷️ الهاشتاقات المتصدرة"])
                
                with tab1:
                    copy_text_1 = (
                        f"{base_title} 😱🔥\n\n"
                        f"شوفوا اللي صار للنهاية، والله ما توقعت كذا! 👀👇\n"
                        f"شارك المقطع مع اللي يعز عليك ❤️{account_mention}\n\n"
                        f"#اكسبلور #ترند #explore #fyp #السعودية"
                    )
                    st.text_area("انسخ النص التشويقي:", value=copy_text_1, height=140)
                
                with tab2:
                    copy_text_2 = (
                        f"{base_title} ✨\n\n"
                        f"لو كنت مكانه، وش كان بيكون تصرفك؟ 🤔💭\n"
                        f"اكتبوا لي رأيكم في التعليقات تحت 👇🔥{account_mention}\n\n"
                        f"#تيك_توك #ريلز #سناب #فيديو_اليوم #viral"
                    )
                    st.text_area("انسخ النص التفاعلي:", value=copy_text_2, height=140)
                
                with tab3:
                    hashtags = (
                        "#اكسبلور #explore #ترند #fypシ #viral #السعودية #الرياض #جدة "
                        "#تيك_توك #مقاطع_ضحك #قصص #شورتس #ريلز #foryoupage #trend"
                    )
                    st.text_area("انسخ حزمة الهاشتاقات المتصدرة:", value=hashtags, height=100)

            except subprocess.CalledProcessError as e:
                err_msg = e.stderr.decode('utf-8', errors='ignore')
                st.error("حدث خطأ أثناء معالجة الفيديو:")
                st.code(err_msg[-300:] if len(err_msg) > 300 else err_msg)
            finally:
                if os.path.exists(input_path):
                    os.remove(input_path)
