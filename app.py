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

# واجهة عربية كاملة، إخفاء شريط الاستضافة وقوائم النظام
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

st.markdown('<h1 class="main-title">🎬 استوديو تعديل وتجهيز الفيديوهات الفوري</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">معالجة صاروخية بدقة 720p، ملء ذكي، عناوين جذابة، ومولد محتوى متكامل</p>', unsafe_allow_html=True)

# خيارات المنصات بدقة 720p فائقة السرعة
PLATFORMS = {
    "تيك توك / سناب شات / شورتس (طولي 9:16)": {"w": 720, "h": 1280, "name": "9_16_Vertical"},
    "ريلز إنستقرام (طولي 9:16)": {"w": 720, "h": 1280, "name": "Reels_9_16"},
    "بوست إنستقرام عمودي (مقاس 4:5)": {"w": 720, "h": 900, "name": "IG_Feed_4_5"},
    "منشور إكس / تويتر (مربع 1:1)": {"w": 720, "h": 720, "name": "Square_1_1"},
    "يوتيوب كلاسيكي (أفقي 16:9)": {"w": 1280, "h": 720, "name": "Landscape_16_9"},
}

# أنماط العرض والتنسيق السريعة والخفيفة
STYLES = {
    "⚡ ملء الشاشة الذكي الكامل (بدون هوامش - الأسرع والأكثر انتشاراً)": "crop",
    "🎙️ إطار استوديو البودكاست الحديث (خلفية داكنة خفيفة)": "podcast_card",
    "⬛ إطار أسود كلاسيكي نقي (Fit)": "fit"
}

uploaded_file = st.file_uploader("اختر مقطع الفيديو من جهازك:", type=["mp4", "mov", "mkv"])

if uploaded_file is not None:
    st.video(uploaded_file)
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        selected_platform = st.selectbox("🎯 المنصة المستهدفة (دقة 720p HD):", list(PLATFORMS.keys()))
    with col2:
        selected_style = st.selectbox("🎨 نمط العرض والإخراج:", list(STYLES.keys()))

    target_w = PLATFORMS[selected_platform]["w"]
    target_h = PLATFORMS[selected_platform]["h"]
    style_code = STYLES[selected_style]

    st.divider()

    # 1. خيارات تنظيف النصوص والتعديل التلقائي
    st.markdown("### ⚡ المعالجة والقص الفوري")
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        enable_auto_trim = st.checkbox(
            "✂️ قص أوتوماتيكي ذكي (حذف البداية وخاتمة تيك توك)",
            value=True,
            help="يقتطع البداية البطيئة وآخر ثانيتين تلقائياً وبسرعة فائقة."
        )
    with col_opt2:
        clean_zoom = st.checkbox(
            "🔍 تكبير خفيف لطرد النصوص والشعارات بالأطراف (Smart Zoom)",
            value=True,
            help="يكبر المقطع بنسبة محسوبة لإخفاء الكتابات القديمة من حواف الفيديو."
        )

    enable_smart_compress = st.checkbox(
        "📦 ضغط الحجم بنسبة 70% وتجديد البصمة الرقمية (فيديو أصلي وخفيف)",
        value=True
    )

    st.divider()

    # 2. شريط العنوان الجذاب (Hook Bar)
    enable_hook = st.checkbox("🔥 إضافة شريط عنوان جذاب فوق الفيديو", value=True)
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
            hook_filter = f",drawtext=text='{clean_hook}':x=(w-text_w)/2:y=45:fontsize=26:fontcolor={hook_color}:box=1:boxcolor={hook_bg_val}:boxborderw=10"

    # 3. وضع وحماية الحساب وتغطية القديم
    enable_stamp = st.checkbox("✨ وضع حسابك وتغطية الشعار القديم أسفل اليمين", value=True)
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
                    "تغطية الشعار القديم + وضع حسابك في الأعلى بوضوح",
                    "أسفل اليمين فقط",
                    "أعلى المنتصف",
                    "أعلى اليسار"
                ]
            )

        final_text = saved_accounts[chosen_label].replace(":", "\\:").replace("'", "")
        box_style = "box=1:boxcolor=black@0.85:boxborderw=10:fontcolor=white:fontsize=22"
        
        if acc_pos == "تغطية الشعار القديم + وضع حسابك في الأعلى بوضوح":
            stamp_filter = (
                f",drawbox=x={target_w-360}:y={target_h-170}:w=360:h=160:color=black@0.90:t=fill"
                f",drawtext=text='{final_text}':x=(w-tw)/2:y=105:{box_style}"
            )
        elif acc_pos == "أسفل اليمين فقط":
            stamp_filter = f",drawtext=text='{final_text}':x=w-tw-25:y=h-th-50:{box_style}"
        elif acc_pos == "أعلى المنتصف":
            stamp_filter = f",drawtext=text='{final_text}':x=(w-tw)/2:y=105:{box_style}"
        elif acc_pos == "أعلى اليسار":
            stamp_filter = f",drawtext=text='{final_text}':x=25:y=30:{box_style}"

    all_text_filters = f"{hook_filter}{stamp_filter}"

    if st.button("🚀 بدء المعالجة الصاروخية وتجهيز الفيديو"):
        with st.spinner("جاري التجهيز السريع في ثانية إلى ثانيتين..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as in_temp:
                in_temp.write(uploaded_file.read())
                input_path = in_temp.name
            
            output_path = tempfile.mktemp(suffix=".mp4")

            # فحص فوري لمدة الفيديو عبر ffprobe
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

            # معامل التكبير السريع لطرد النصوص
            zoom_mult = 1.18 if clean_zoom else 1.0
            calc_w = int(target_w * zoom_mult)
            calc_h = int(target_h * zoom_mult)

            # بناء الفلاتر الخفيفة أحادية الطبقة (Single-Pass Light Chain)
            if style_code == "crop" or clean_zoom:
                filter_complex = (
                    f"[0:v]scale={calc_w}:{calc_h}:force_original_aspect_ratio=increase:flags=bicubic,"
                    f"crop={target_w}:{target_h}{all_text_filters}[outv]"
                )
            elif style_code == "podcast_card":
                filter_complex = (
                    f"color=c=#0B0F17:s={target_w}x{target_h}[bg];"
                    f"[0:v]scale={target_w}-40:{target_h}-180:force_original_aspect_ratio=decrease:flags=bicubic,"
                    f"scale=trunc(iw/2)*2:trunc(ih/2)*2[fg];"
                    f"[bg][fg]overlay=(W-w)/2:(H-h)/2{all_text_filters}[outv]"
                )
            else: # fit
                filter_complex = (
                    f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease:flags=bicubic,"
                    f"scale=trunc(iw/2)*2:trunc(ih/2)*2,"
                    f"pad={target_w}:{target_h}:(ow-iw)/2:(oh-ih)/2:black{all_text_filters}[outv]"
                )

            crf_val = "25" if enable_smart_compress else "22"

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
                "-preset", "ultrafast",
                "-tune", "zerolatency",
                "-movflags", "+faststart",
                "-pix_fmt", "yuv420p",
                "-crf", crf_val,
                "-c:a", "aac",
                "-b:a", "128k",
                output_path
            ])

            try:
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
                
                st.success(f"⚡ تمت المعالجة بسرعة قياسية! (حجم الملف: {file_size_mb:.2f} ميجابايت)")
                st.video(output_path)

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="⬇️ تحميل المقطع الجاهز للنشر فوراً",
                        data=f,
                        file_name=f"ready_{PLATFORMS[selected_platform]['name']}.mp4",
                        mime="video/mp4"
                    )

                # قسم المحتوى ونصوص النشر الجاهزة
                st.divider()
                st.markdown("### ✍️ نماذج محتوى ونصوص جاهزة للنشر (انسخ والصق بضغطة زر):")
                
                base_title = hook_text.strip() if hook_text.strip() else "شاهد هذا المقطع العجيب"
                account_mention = f"\nتابعني للمزيد: {chosen_account_text}" if chosen_account_text else ""
                
                tab1, tab2, tab3 = st.tabs(["🔥 نص تشويقي قوي", "💬 نص تفاعلي (تعليقات)", "🏷️ الهاشتاقات المتصدرة"])
                
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
