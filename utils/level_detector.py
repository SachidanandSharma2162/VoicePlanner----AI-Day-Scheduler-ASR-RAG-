"""
utils/level_detector.py
Keyword-based detection of user level: School | College | Job-Seeker | General
"""
import re

SCHOOL_KEYWORDS = [
    "board exam", "class 10", "class 12", "10th", "12th", "cbse", "icse",
    "ncert", "school", "tuition", "coaching", "jee", "neet", "maths",
    "physics", "chemistry", "biology", "social science", "english grammar",
    "history", "geography", "civics", "economics", "board", "matriculation",
    "intermediate", "high school", "secondary", "higher secondary",
]

COLLEGE_KEYWORDS = [
    "college", "university", "semester", "mid-sem", "end-sem", "internship",
    "leetcode", "competitive programming", "dbms", "operating system", "os",
    "computer networks", "cn", "data structures", "dsa", "algorithms",
    "minor project", "major project", "capstone", "viva", "practical",
    "lab", "assignment", "placement", "campus placement", "btech", "be",
    "mtech", "mca", "bca", "engineering", "degree", "graduation", "bachelors",
    "masters", "gate", "cse", "ece", "it",
]

JOB_SEEKER_KEYWORDS = [
    "job", "interview", "resume", "cv", "apply", "application", "company",
    "mock interview", "system design", "faang", "google", "amazon", "microsoft",
    "meta", "flipkart", "infosys", "tcs", "wipro", "accenture", "startup",
    "offer", "salary", "hired", "job search", "linkedin", "networking",
    "referral", "recruiter", "hr", "technical interview", "behavioral",
    "data science", "machine learning", "backend", "frontend", "full stack",
    "software engineer", "swe", "sde", "product manager", "pm", "qa",
    "devops", "cloud", "aws", "azure", "gcp",
]


def detect_level(text: str) -> dict:
    """
    Detect the user's study/career level from transcribed text.

    Returns:
        dict with keys: level (str), confidence (str), matched_keywords (list)
    """
    text_lower = text.lower()

    school_score = sum(1 for kw in SCHOOL_KEYWORDS if re.search(r"\b" + re.escape(kw) + r"\b", text_lower))
    college_score = sum(1 for kw in COLLEGE_KEYWORDS if re.search(r"\b" + re.escape(kw) + r"\b", text_lower))
    job_score = sum(1 for kw in JOB_SEEKER_KEYWORDS if re.search(r"\b" + re.escape(kw) + r"\b", text_lower))

    scores = {
        "School": school_score,
        "College": college_score,
        "Job-Seeker": job_score,
    }

    best_level = max(scores, key=scores.get)
    best_score = scores[best_level]

    if best_score == 0:
        return {
            "level": "General",
            "confidence": "low",
            "matched_keywords": [],
            "scores": scores,
        }

    total = sum(scores.values())
    confidence = (
        "high" if best_score / max(total, 1) >= 0.6
        else "medium" if best_score / max(total, 1) >= 0.4
        else "low"
    )

    matched = (
        SCHOOL_KEYWORDS if best_level == "School"
        else COLLEGE_KEYWORDS if best_level == "College"
        else JOB_SEEKER_KEYWORDS
    )
    matched_kws = [kw for kw in matched if re.search(r"\b" + re.escape(kw) + r"\b", text_lower)]

    return {
        "level": best_level,
        "confidence": confidence,
        "matched_keywords": matched_kws[:8],  # top 8
        "scores": scores,
    }