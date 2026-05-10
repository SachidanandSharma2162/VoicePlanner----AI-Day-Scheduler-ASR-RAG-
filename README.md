# 🎙️ VoicePlanner — AI Day Scheduler

> **Speak your goals. Get a personalised, time-blocked day plan.**
> Voice → faster-whisper (local ASR) → FAISS RAG → Groq LLaMA 3.1 → Streamlit UI

---

## 🏗️ Architecture

```
Voice Input (upload WAV/MP3/M4A/OGG)
        ↓
  faster-whisper (local ASR — no API key needed)
        ↓
  Level Detector (keyword-based: School / College / Job-Seeker / General)
        ↓
  RAG Engine (FAISS + sentence-transformers, 80+ entries)
        ↓  retrieves top-6 relevant scheduling guidelines
  Groq LLM (LLaMA 3.1) — grounded schedule generation
        ↓
  Streamlit UI — display + PDF / text export
```

---

## 📁 Project Structure

```
VoicePlanner/
├── app.py                        # Main Streamlit application
├── requirements.txt
├── .env                          # Your API keys (never commit this)
├── .gitignore
├── README.md
├── knowledge_base/               # RAG knowledge base (JSON, 80+ entries)
│   ├── school.json               # 20 school / board exam guidelines
│   ├── college.json              # 22 college / placement guidelines
│   ├── job_seeker.json           # 22 job-seeker / interview prep guidelines
│   └── general.json              # 20 universal productivity guidelines
└── utils/
    ├── transcriber.py            # faster-whisper ASR wrapper
    ├── level_detector.py         # Keyword-based level detection
    ├── rag_engine.py             # FAISS + sentence-transformers RAG
    ├── planner.py                # Groq LLM schedule generator
    └── exporter.py               # PDF + text export via fpdf2
```

---

## ⚙️ Setup

### 1. Clone & create virtual environment
```bash
git clone https://github.com/SachidanandSharma2162/VoicePlanner----AI-Day-Scheduler-ASR-RAG-
cd VoicePlanner
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

> **Note:** `faster-whisper` requires `ffmpeg` installed on your system.
> ```bash
> # Linux
> sudo apt install ffmpeg
> # Mac
> brew install ffmpeg
> # Windows — download from https://ffmpeg.org/download.html
> ```

### 3. Add your Groq API key
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```
Get a **free** key at [console.groq.com](https://console.groq.com) — no credit card required.

### 4. Run the app
```bash
streamlit run app.py
```

---

## 🚀 Usage

| Step | Action |
|------|--------|
| **1** | Upload an audio file (WAV, MP3, M4A, OGG, FLAC) |
| **2** | Click **Transcribe Audio** — faster-whisper runs locally |
| **3** | Review transcription and detected level |
| **4** | Set wake/sleep time and any extra constraints |
| **5** | Click **Generate My Day Plan** |
| **6** | Export as **PDF** or **text** |

> 💡 No audio file? Type or paste your goals directly into the text box — the full RAG + LLM pipeline still runs.

---

## 🎤 What to Say

**School student:**
> "I have board exams in 3 weeks. I need to study Maths, Physics, and Chemistry. I wake up at 6am and sleep by 10. I also have tuition from 4 to 6."

**College student:**
> "I have a mid-sem next week for DBMS and OS. I also want to solve 2 LeetCode problems daily and finish my minor project. I wake up at 7 and have classes till 3pm."

**Job-Seeker:**
> "I'm preparing for software engineering interviews. I need to practice DSA, system design, and apply to 5 companies daily. I have a mock interview on Friday. Wake up at 6am."

---

## 🔧 Customisation

### Add more knowledge base entries
Add to any `.json` file in `knowledge_base/` following this format:
```json
{
  "level": "College",
  "text": "Your scheduling guideline or productivity tip here.",
  "source": "college.json"
}
```
Use `"level": "General"` for tips applicable to all levels. The FAISS index rebuilds automatically on next app start.

### Switch Whisper model size
In the sidebar or in `utils/transcriber.py`:

| Size | Speed | Accuracy | Model Size |
|------|-------|----------|------------|
| `tiny` | ⚡⚡⚡ | Low | ~75 MB |
| `base` | ⚡⚡ | Good | ~145 MB |
| `small` | ⚡ | Better | ~466 MB |
| `medium` | 🐢 | Best practical | ~1.5 GB |
| `large-v2` | 🐢🐢 | Highest | ~3 GB |

### Switch Groq model
In the sidebar or in `utils/planner.py`:

| Model | Best For |
|-------|----------|
| `llama-3.1-8b-instant` | Speed (default) |
| `llama-3.1-70b-versatile` | Smarter plans |
| `gemma2-9b-it` | Alternative |
| `mixtral-8x7b-32768` | Long/complex goals |

---

## 📦 Dependencies

| Library | Purpose |
|---------|---------|
| `faster-whisper` | Local speech-to-text (no OpenAI API needed) |
| `groq` | Groq LLM API — LLaMA 3.1 plan generation |
| `sentence-transformers` | Document & query embeddings |
| `faiss-cpu` | Fast vector similarity search |
| `streamlit` | Web UI |
| `fpdf2` | PDF export |
| `python-dotenv` | `.env` file loading |

---

## 🔑 Key Design Decisions

- **Local ASR** — faster-whisper runs entirely on your machine. No audio is sent to any API.
- **Custom RAG** — No LangChain dependency. Pure FAISS + sentence-transformers for full control and minimal overhead.
- **Level-aware retrieval** — RAG reranks results to prioritise entries matching the detected user level before passing context to the LLM.
- **Groq for speed** — LLaMA 3.1 on Groq's inference infrastructure is ~10x faster than equivalent hosted models, making the free tier practical for real-time use.

