import re
from pathlib import Path

from PyPDF2 import PdfReader
from docx import Document


def parse_cv_file(file_path: str) -> dict:
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    elif ext == ".docx":
        doc = Document(file_path)
        text = "\n".join(p.text for p in doc.paragraphs)
    elif ext == ".txt":
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
    else:
        text = ""
    return _parse_cv_text(text)


def _parse_cv_text(text: str) -> dict:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    sections = {}
    keys = {
        "professional_summary": ["professional summary", "summary"],
        "skills": ["skills"],
        "work_history": ["work experience", "professional experience", "experience"],
        "education": ["education"],
    }
    indices = {}
    for i, line in enumerate(lines):
        key = line.lower().rstrip(":").strip()
        for section, titles in keys.items():
            if key in titles:
                indices[section] = i
    sorted_sections = sorted(indices.items(), key=lambda x: x[1])
    for idx, (section, start) in enumerate(sorted_sections):
        end = sorted_sections[idx + 1][1] if idx + 1 < len(sorted_sections) else len(lines)
        sections[section] = lines[start + 1 : end]
    header_end = sorted_sections[0][1] if sorted_sections else 0
    header = lines[:header_end]
    name = header[0] if header else None
    email = None
    phone = None
    linkedin = None
    address_parts = []
    for line in header[1:]:
        if re.search(r"[\w\.+-]+@[\w\.-]+", line):
            email = line
        elif re.search(r"\+?\d[\d\-\.\s\(\)]{7,}\d", line):
            phone = line
        elif "linkedin.com" in line.lower():
            linkedin = line
        else:
            address_parts.append(line)
    address = ", ".join(address_parts) if address_parts else None
    def parse_experience(lines_block):
        text_block = "\n".join(lines_block) if lines_block else ""
        entries = [p.strip() for p in re.split(r"\n{2,}", text_block) if p.strip()]
        result = []
        date_pattern = re.compile(r"(\w+ \d{4}\s*-\s*(?:Present|\w+ \d{4}))")
        for entry in entries:
            parts = entry.split("\n")
            period = None
            for p in parts:
                m = date_pattern.search(p)
                if m:
                    period = m.group(0)
                    parts.remove(p)
                    break
            first = parts[0] if parts else ""
            comp_loc = [x.strip() for x in first.split(",", 1)]
            company = comp_loc[0] if comp_loc else None
            location = comp_loc[1] if len(comp_loc) > 1 else None
            roles = "\n".join(parts[1:]) if len(parts) > 1 else None
            result.append({"company": company, "location": location, "period": period, "roles": roles})
        return result or None
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "address": address,
        "professional_summary": " ".join(sections.get("professional_summary", [])) or None,
        "skills": " ".join(sections.get("skills", [])) or None,
        "work_history": parse_experience(sections.get("work_history")),
        "education": parse_experience(sections.get("education")),
    }