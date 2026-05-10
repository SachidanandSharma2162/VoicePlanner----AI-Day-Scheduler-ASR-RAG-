"""
utils/exporter.py
Export day plan as PDF or plain text.
"""
import io
import re
from datetime import datetime


def export_as_text(plan: str, transcription: str, level: str) -> str:
    """Return a clean text version of the plan."""
    header = (
        f"VoicePlanner — AI Day Schedule\n"
        f"{'=' * 50}\n"
        f"Generated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n"
        f"Level: {level}\n"
        f"{'=' * 50}\n\n"
        f"Your Goals:\n{transcription}\n\n"
        f"{'=' * 50}\n\n"
    )
    return header + plan


def export_as_pdf(plan: str, transcription: str, level: str) -> bytes:
    """
    Generate a PDF from the plan and return raw bytes.
    Requires fpdf2: pip install fpdf2
    """
    try:
        from fpdf import FPDF
    except ImportError:
        raise ImportError("fpdf2 not installed. Run: pip install fpdf2")

    class PDF(FPDF):
        def header(self):
            self.set_font("Helvetica", "B", 14)
            self.set_text_color(30, 30, 30)
            self.cell(0, 10, "VoicePlanner — AI Day Schedule", align="C", new_x="LMARGIN", new_y="NEXT")
            self.set_font("Helvetica", "", 9)
            self.set_text_color(100, 100, 100)
            self.cell(0, 6, f"Generated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}  |  Level: {level}", align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(2)
            self.set_draw_color(200, 200, 200)
            self.set_line_width(0.5)
            self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
            self.ln(4)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, f"Page {self.page_no()} | VoicePlanner", align="C")

    pdf = PDF()
    pdf.set_margins(20, 20, 20)
    pdf.add_page()

    # Goals section
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 8, "Your Goals:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(80, 80, 80)
    # Strip emojis for PDF (fpdf2 basic mode doesn't support all unicode)
    clean_transcription = _strip_emojis(transcription)
    pdf.multi_cell(0, 6, clean_transcription)
    pdf.ln(4)

    # Plan content
    clean_plan = _strip_emojis(plan)
    lines = clean_plan.split("\n")

    for line in lines:
        stripped = line.strip()
        if not stripped:
            pdf.ln(2)
            continue

        if stripped.startswith("## "):
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(30, 80, 160)
            pdf.multi_cell(0, 8, stripped[3:])
            pdf.ln(1)
        elif stripped.startswith("### "):
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(50, 50, 120)
            pdf.multi_cell(0, 7, stripped[4:])
            pdf.ln(1)
        elif stripped.startswith("|"):
            pdf.set_font("Courier", "", 8)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(0, 5, stripped)
        elif stripped.startswith(("- ", "* ", "1.", "2.", "3.")):
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 6, "  " + stripped)
        else:
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 6, stripped)

    buf = io.BytesIO()
    pdf.output(buf)
    return buf.getvalue()


def _strip_emojis(text: str) -> str:
    """Remove emoji characters that fpdf2 basic mode can't render."""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002700-\U000027BF"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text)