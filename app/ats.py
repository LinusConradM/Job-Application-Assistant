"""
ATS assessment utilities: extract text from CV and compare against job requirements.
"""
import io
import re



def extract_text_from_bytes(data: bytes, file_name: str) -> str:
    """
    Extract plain text from uploaded CV file bytes. Supports PDF and plain text.

    :param data: File content as bytes
    :param file_name: Original file name to infer type
    :return: Extracted text
    """
    name = file_name.lower()
    if name.endswith(".pdf"):
        try:
            import PyPDF2
        except ImportError:
            return ""
        reader = PyPDF2.PdfReader(io.BytesIO(data))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    try:
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def assess_cv_against_job(cv_text: str, required_skills_str: str) -> tuple[int, list[str], list[str]]:
    """
    Compare CV text against required skills string and detect simple red flags.

    :param cv_text: Extracted CV text
    :param required_skills_str: Comma-separated required skills from job
    :return: Tuple of (match percentage, missing skills list, red flags list)
    """
    required = [s.strip().lower() for s in required_skills_str.split(",") if s.strip()]
    text = cv_text.lower()
    matched = [skill for skill in required if skill in text]
    missing = [skill for skill in required if skill not in text]
    percentage = int(len(matched) / len(required) * 100) if required else 0
    red_flags: list[str] = []
    for start, end in re.findall(r"(\d{4})\s*[-–]\s*(\d{4})", cv_text):
        try:
            if int(end) - int(start) > 1:
                red_flags.append("Employment gap > 12 months")
                break
        except ValueError:
            continue
    return percentage, missing, red_flags