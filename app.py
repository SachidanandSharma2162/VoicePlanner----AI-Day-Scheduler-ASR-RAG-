"""
app.py — VoicePlanner: AI-Powered Voice Day Scheduler
Run: streamlit run app.py
"""
import os
import sys
import time
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# ── Load .env ───────────────────────────────────────────────────────────────
load_dotenv()

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VoicePlanner — AI Day Scheduler",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@400;700;800&display=swap');

/* Root variables */
:root {
    --bg-dark: #0d0f17;
    --bg-card: #13161f;
    --bg-card2: #1a1d2b;
    --accent: #7c6af7;
    --accent2: #5ef8c5;
    --accent3: #f7c35e;
    --text-primary: #e8eaf2;
    --text-muted: #7b7f9a;
    --border: rgba(124, 106, 247, 0.2);
    --glow: 0 0 30px rgba(124, 106, 247, 0.15);
}

/* Base */
.stApp {
    background: var(--bg-dark);
    font-family: 'Space Grotesk', sans-serif;
    color: var(--text-primary);
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #1a1038 0%, #0d1528 50%, #0f2028 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 40px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--glow);
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(124,106,247,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 100px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(94,248,197,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #e8eaf2 0%, #7c6af7 50%, #5ef8c5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 8px 0;
    line-height: 1.2;
}
.hero-subtitle {
    color: var(--text-muted);
    font-size: 1.05rem;
    font-weight: 400;
    margin: 0;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(124,106,247,0.15);
    border: 1px solid rgba(124,106,247,0.3);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #a89fff;
    letter-spacing: 0.05em;
    margin-bottom: 16px;
    text-transform: uppercase;
}

/* Step cards */
.step-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 20px;
    position: relative;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.step-card:hover {
    border-color: rgba(124,106,247,0.4);
    box-shadow: 0 4px 24px rgba(124,106,247,0.1);
}
.step-label {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px; height: 28px;
    background: linear-gradient(135deg, var(--accent), #5540cc);
    border-radius: 8px;
    font-size: 0.8rem;
    font-weight: 700;
    color: white;
    margin-bottom: 12px;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 4px 0;
}
.step-desc {
    color: var(--text-muted);
    font-size: 0.88rem;
    margin: 0 0 16px 0;
}

/* Status pills */
.pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.82rem;
    font-weight: 600;
}
.pill-school { background: rgba(94,248,197,0.12); border: 1px solid rgba(94,248,197,0.3); color: #5ef8c5; }
.pill-college { background: rgba(124,106,247,0.12); border: 1px solid rgba(124,106,247,0.3); color: #a89fff; }
.pill-job { background: rgba(247,195,94,0.12); border: 1px solid rgba(247,195,94,0.3); color: var(--accent3); }
.pill-general { background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.15); color: var(--text-muted); }

/* Transcription box */
.transcription-box {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 22px;
    font-size: 0.98rem;
    line-height: 1.7;
    color: var(--text-primary);
    white-space: pre-wrap;
    font-family: 'Space Grotesk', sans-serif;
}

/* Plan output */
.plan-container {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 32px;
    box-shadow: var(--glow);
}
.plan-container h2 { color: var(--accent); font-family: 'Syne', sans-serif; }
.plan-container h3 { color: #5ef8c5; }
.plan-container table { width: 100%; border-collapse: collapse; }
.plan-container th { background: rgba(124,106,247,0.15); color: var(--accent); padding: 8px 12px; text-align: left; }
.plan-container td { padding: 7px 12px; border-bottom: 1px solid rgba(255,255,255,0.05); }
.plan-container tr:hover td { background: rgba(124,106,247,0.05); }

/* Info cards */
.info-strip {
    display: flex;
    gap: 12px;
    margin: 16px 0;
    flex-wrap: wrap;
}
.info-chip {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 8px 16px;
    font-size: 0.85rem;
    color: var(--text-muted);
}
.info-chip span { color: var(--text-primary); font-weight: 600; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text-primary);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #5540cc) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: opacity 0.2s, transform 0.1s !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

/* Inputs */
.stTextArea textarea, .stTextInput input, .stSelectbox select {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stFileUploader {
    background: var(--bg-card2);
    border: 1px dashed rgba(124,106,247,0.35);
    border-radius: 12px;
}

/* Dividers */
hr { border-color: var(--border) !important; }

/* Success/info/warning/error */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 10px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-dark); }
::-webkit-scrollbar-thumb { background: rgba(124,106,247,0.4); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Imports (lazy-friendly) ──────────────────────────────────────────────────
from utils.level_detector import detect_level
from utils.exporter import export_as_text, export_as_pdf

# ── Helper: cached RAG build ─────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_rag_engine():
    from utils.rag_engine import build_index
    count = build_index()
    return count

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")

    # API key — prefer .env, allow override
    env_key = os.getenv("GROQ_API_KEY", "")
    groq_key_input = st.text_input(
        "Groq API Key",
        value=env_key,
        type="password",
        placeholder="gsk_...",
        help="Get a free key at console.groq.com"
    )
    groq_api_key = groq_key_input or env_key

    st.markdown("---")
    st.markdown("### 🤖 Model Settings")

    from utils.planner import get_available_models
    model_choice = st.selectbox(
        "LLM Model",
        options=get_available_models(),
        index=0,
        help="llama-3.1-8b-instant is fastest on free tier"
    )

    from utils.transcriber import get_available_model_sizes
    whisper_size = st.selectbox(
        "Whisper Model Size",
        options=get_available_model_sizes(),
        index=1,
        help="larger = more accurate, slower"
    )

    st.markdown("---")
    st.markdown("### 📅 Schedule Settings")
    wake_time = st.text_input("Wake Time", value="6:00 AM")
    sleep_time = st.text_input("Sleep Time", value="10:00 PM")

    st.markdown("---")
    st.markdown("### 🏷️ Level Override")
    level_override = st.selectbox(
        "Force Level (optional)",
        ["Auto-Detect", "School", "College", "Job-Seeker", "General"]
    )

    st.markdown("---")
    # RAG status
    try:
        doc_count = load_rag_engine()
        st.success(f"✅ Knowledge base: {doc_count} entries indexed")
    except Exception as e:
        st.error(f"❌ RAG Error: {e}")

    st.markdown("---")
    st.markdown("""
<div style='color: var(--text-muted); font-size: 0.8rem;'>
<b>VoicePlanner</b> v1.0<br>
Powered by faster-whisper + FAISS + Groq LLaMA 3.1<br><br>
Built with ❤️ for students & job-seekers
</div>
""", unsafe_allow_html=True)

# ── Main area ────────────────────────────────────────────────────────────────

# Hero
st.markdown("""
<div class="hero-banner">
  <div class="hero-badge">🎙️ Voice-Powered AI Planner</div>
  <div class="hero-title">VoicePlanner</div>
  <p class="hero-subtitle">Speak your goals → Whisper transcribes → RAG retrieves → LLaMA plans your perfect day</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for key in ["transcription", "level_info", "plan_text", "audio_bytes", "audio_name"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ═══════════════════════════════════════════════════════════════════════════
# STEP 1: Voice Input
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="step-card">
  <div class="step-label">1</div>
  <div class="step-title">🎤 Upload Your Voice Recording</div>
  <div class="step-desc">Record yourself describing your goals, subjects, schedule, and any constraints. Upload the file below.</div>
</div>
""", unsafe_allow_html=True)

col_upload, col_example = st.columns([2, 1])

with col_upload:
    uploaded_file = st.file_uploader(
        "Upload audio file",
        type=["wav", "mp3", "m4a", "ogg", "flac", "webm"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.audio(uploaded_file)
        st.session_state.audio_bytes = uploaded_file.read()
        st.session_state.audio_name = uploaded_file.name

with col_example:
    st.markdown("**💬 What to say:**")
    with st.expander("Example phrases"):
        st.markdown("""
**School:**
> "Board exams in 3 weeks. Maths, Physics, Chemistry. Wake 6am, tuition 4–6pm."

**College:**
> "Mid-sem next week, DBMS and OS. Also 2 LeetCode problems daily. Classes till 3pm."

**Job-Seeker:**
> "Preparing for software interviews. DSA, system design, apply to 5 companies daily. Mock interview Friday."
""")

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 2: Transcription
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="step-card">
  <div class="step-label">2</div>
  <div class="step-title">📝 Transcribe Audio</div>
  <div class="step-desc">faster-whisper converts your speech to text locally — no audio ever leaves your machine.</div>
</div>
""", unsafe_allow_html=True)

col_trans_btn, col_or, col_manual = st.columns([1, 0.1, 2])

with col_trans_btn:
    transcribe_clicked = st.button(
        "🎙️ Transcribe Audio",
        disabled=not st.session_state.audio_bytes,
        use_container_width=True,
    )

with col_manual:
    manual_text = st.text_area(
        "Or type/paste your goals directly:",
        placeholder="E.g. I have board exams in 3 weeks. I need to study Maths, Physics and Chemistry...",
        height=100,
        label_visibility="collapsed"
    )

if transcribe_clicked and st.session_state.audio_bytes:
    with st.spinner("🔊 Transcribing with Whisper... (first run downloads model ~70MB)"):
        try:
            from utils.transcriber import transcribe_audio
            result = transcribe_audio(
                st.session_state.audio_bytes,
                filename=st.session_state.audio_name or "audio.wav",
                model_size=whisper_size,
            )
            st.session_state.transcription = result["text"]
            st.success(f"✅ Transcribed! Language: **{result['language'].upper()}** | Duration: **{result['duration_seconds']}s**")
        except Exception as e:
            st.error(f"❌ Transcription failed: {e}")
            st.info("💡 Make sure ffmpeg is installed: `sudo apt install ffmpeg`")

# Use manual text if no transcription
if manual_text.strip() and not st.session_state.transcription:
    st.session_state.transcription = manual_text.strip()

if st.session_state.transcription:
    st.markdown("**Transcription:**")
    st.markdown(f'<div class="transcription-box">{st.session_state.transcription}</div>', unsafe_allow_html=True)

    # Edit button
    if st.checkbox("✏️ Edit transcription"):
        edited = st.text_area(
            "Edit:",
            value=st.session_state.transcription,
            height=120,
            label_visibility="collapsed"
        )
        if edited.strip():
            st.session_state.transcription = edited.strip()

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 3: Level Detection
# ═══════════════════════════════════════════════════════════════════════════
if st.session_state.transcription:
    st.markdown("""
<div class="step-card">
  <div class="step-label">3</div>
  <div class="step-title">🔍 Level Detection & Constraints</div>
  <div class="step-desc">AI detects whether you're a school student, college student, or job-seeker to personalise your plan.</div>
</div>
""", unsafe_allow_html=True)

    level_info = detect_level(st.session_state.transcription)
    detected_level = level_info["level"]

    # Apply override
    final_level = level_override if level_override != "Auto-Detect" else detected_level
    st.session_state.level_info = {**level_info, "final_level": final_level}

    # Display detection result
    pill_class = {
        "School": "pill-school",
        "College": "pill-college",
        "Job-Seeker": "pill-job",
        "General": "pill-general",
    }.get(final_level, "pill-general")

    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        st.markdown(f'<div class="info-chip">Detected Level: <span>{detected_level}</span></div>', unsafe_allow_html=True)
    with col_d2:
        st.markdown(f'<div class="info-chip">Confidence: <span>{level_info["confidence"].title()}</span></div>', unsafe_allow_html=True)
    with col_d3:
        st.markdown(f'<div class="info-chip">Using: <span>{final_level}</span></div>', unsafe_allow_html=True)

    if level_info["matched_keywords"]:
        kw_str = " • ".join(level_info["matched_keywords"])
        st.caption(f"Matched keywords: {kw_str}")

    extra_constraints = st.text_input(
        "📌 Additional constraints (optional)",
        placeholder="E.g. No study after 9 PM, vegetarian meal breaks, weekend hackathon on Saturday",
    )
    st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 4: Generate Plan
# ═══════════════════════════════════════════════════════════════════════════
if st.session_state.transcription and st.session_state.level_info:
    st.markdown("""
<div class="step-card">
  <div class="step-label">4</div>
  <div class="step-title">⚡ Generate Your Day Plan</div>
  <div class="step-desc">RAG retrieves the best scheduling guidelines, then Groq LLaMA 3.1 crafts your personalised time-blocked schedule.</div>
</div>
""", unsafe_allow_html=True)

    if not groq_api_key:
        st.warning("⚠️ Enter your Groq API key in the sidebar to generate a plan. Get one free at console.groq.com")
    else:
        generate_clicked = st.button("🚀 Generate My Day Plan", use_container_width=False)

        if generate_clicked:
            final_level = st.session_state.level_info["final_level"]

            with st.status("🧠 Generating your plan...", expanded=True) as status:
                st.write("🔍 Retrieving relevant scheduling guidelines from knowledge base...")
                try:
                    from utils.rag_engine import retrieve
                    rag_docs = retrieve(st.session_state.transcription, final_level, top_k=6)
                    st.write(f"✅ Retrieved {len(rag_docs)} relevant guidelines")

                    st.write("🤖 LLaMA 3.1 is crafting your personalised schedule...")
                    from utils.planner import generate_plan
                    plan = generate_plan(
                        transcription=st.session_state.transcription,
                        level=final_level,
                        rag_docs=rag_docs,
                        groq_api_key=groq_api_key,
                        wake_time=wake_time,
                        sleep_time=sleep_time,
                        extra_constraints=extra_constraints if 'extra_constraints' in dir() else "",
                        model=model_choice,
                    )
                    st.session_state.plan_text = plan
                    st.write("✅ Day plan ready!")
                    status.update(label="✅ Plan generated!", state="complete", expanded=False)
                except Exception as e:
                    status.update(label="❌ Error", state="error")
                    st.error(f"Generation failed: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 5: Display & Export
# ═══════════════════════════════════════════════════════════════════════════
if st.session_state.plan_text:
    st.markdown("---")
    st.markdown("""
<div class="step-card">
  <div class="step-label">5</div>
  <div class="step-title">📋 Your Personalised Day Plan</div>
  <div class="step-desc">Here is your AI-generated, research-backed, time-blocked schedule.</div>
</div>
""", unsafe_allow_html=True)

    # Render plan
    st.markdown(
        f'<div class="plan-container">{st.session_state.plan_text}</div>',
        unsafe_allow_html=True
    )

    # Export buttons
    st.markdown("### 💾 Export")
    col_e1, col_e2, col_e3 = st.columns([1, 1, 2])

    with col_e1:
        txt_content = export_as_text(
            st.session_state.plan_text,
            st.session_state.transcription,
            st.session_state.level_info["final_level"]
        )
        st.download_button(
            "📄 Download as Text",
            data=txt_content,
            file_name="voiceplanner_schedule.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col_e2:
        try:
            pdf_bytes = export_as_pdf(
                st.session_state.plan_text,
                st.session_state.transcription,
                st.session_state.level_info["final_level"]
            )
            st.download_button(
                "📑 Download as PDF",
                data=pdf_bytes,
                file_name="voiceplanner_schedule.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as e:
            st.caption(f"PDF export unavailable: {e}")

    with col_e3:
        if st.button("🔄 Generate New Plan", use_container_width=True):
            st.session_state.plan_text = None
            st.rerun()

    st.markdown("---")

# ── Empty state ───────────────────────────────────────────────────────────────
if not st.session_state.transcription and not st.session_state.audio_bytes:
    st.markdown("""
<div style='text-align:center; padding: 48px 24px; color: var(--text-muted);'>
  <div style='font-size: 3rem; margin-bottom: 16px;'>🎙️</div>
  <div style='font-size: 1.1rem; font-weight: 600; color: var(--text-primary); margin-bottom: 8px;'>Ready to plan your perfect day?</div>
  <div style='font-size: 0.9rem;'>Upload a voice recording above, or type your goals directly in the text box.</div>
</div>
""", unsafe_allow_html=True)