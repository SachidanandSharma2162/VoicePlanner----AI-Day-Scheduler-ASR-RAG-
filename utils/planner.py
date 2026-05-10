"""
utils/planner.py
Day schedule generator using Groq LLM (Llama 3.1).
"""
import os
from typing import List, Dict

MODEL = "llama-3.1-8b-instant"  # Fast free-tier model; change as needed


def _build_prompt(
    transcription: str,
    level: str,
    rag_docs: List[Dict],
    wake_time: str = "6:00 AM",
    sleep_time: str = "10:00 PM",
    extra_constraints: str = "",
) -> str:
    context_blocks = "\n".join(
        f"- [{doc['level']}] {doc['text']}" for doc in rag_docs
    )

    constraints_section = f"\nAdditional constraints: {extra_constraints}" if extra_constraints.strip() else ""

    return f"""You are VoicePlanner, an expert AI day-planner for {level} students and job-seekers.

## User's Goals (voice transcription)
\"{transcription}\"

## Relevant Scheduling Guidelines (retrieved from knowledge base)
{context_blocks}

## Schedule Parameters
- Wake time: {wake_time}
- Sleep time: {sleep_time}{constraints_section}
- User level: {level}

## Your Task
Create a detailed, realistic, time-blocked day schedule. Follow these rules:
1. Start from wake time, end at sleep time.
2. Use the retrieved guidelines to justify your scheduling decisions.
3. Include study blocks, breaks, meals, exercise, and leisure.
4. Make blocks specific: not "study maths" but "Solve 10 differentiation problems from NCERT Ex 5.3".
5. Include brief rationale for 3–4 major blocks (why you scheduled it at that time).
6. Add a "Tips for Today" section with 3 personalised productivity tips based on the user's goals.
7. Format as a clean time-table with emojis for readability.

## Output Format
Use this structure:
---
## 📅 Your Personalised Day Plan — [{level}]

### ⏰ Time-Blocked Schedule
| Time | Activity | Duration | Notes |
|------|----------|----------|-------|
...

### 💡 Why This Schedule Works
(3–4 bullet points explaining the rationale)

### 🎯 Tips for Today
1. ...
2. ...
3. ...

### 📊 Day Overview
- Total study/work hours: X hrs
- Break time: Y mins
- Focus ratio: Z%
---
"""


def generate_plan(
    transcription: str,
    level: str,
    rag_docs: List[Dict],
    groq_api_key: str,
    wake_time: str = "6:00 AM",
    sleep_time: str = "10:00 PM",
    extra_constraints: str = "",
    model: str = MODEL,
) -> str:
    """
    Generate a personalised day plan using Groq LLM.

    Returns the raw plan text.
    """
    try:
        from groq import Groq
    except ImportError:
        raise ImportError("groq package not installed. Run: pip install groq")

    client = Groq(api_key=groq_api_key)
    prompt = _build_prompt(transcription, level, rag_docs, wake_time, sleep_time, extra_constraints)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()


def get_available_models() -> List[str]:
    return [
        "llama-3.1-8b-instant",
        "llama-3.1-70b-versatile",
        "llama3-8b-8192",
        "llama3-70b-8192",
        "gemma2-9b-it",
        "mixtral-8x7b-32768",
    ]