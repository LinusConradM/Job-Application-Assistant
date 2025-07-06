#!/usr/bin/env python3
"""
Gradio-based UI for Job Application Assistant
"""
import os
from dotenv import load_dotenv

load_dotenv()

import gradio as gr

from app.tasks import scrape_and_store
from app.database import SessionLocal
from app.models import Job
from app.ats import extract_text_from_bytes, assess_cv_against_job


def fetch_and_list():
    """Trigger a scraping run and return all stored jobs and dropdown options."""
    scrape_and_store()
    db = SessionLocal()
    jobs = db.query(Job).all()
    db.close()
    data = [
        [
            job.title,
            job.company,
            job.description,
            job.location,
            job.skills,
            job.salary or "",
        ]
        for job in jobs
    ]
    options = [f"{job.id}: {job.title}" for job in jobs]
    return data, options


def run_assessment(cv_file, selected_job):
    """
    Process uploaded CV file and selected job to produce ATS assessment outputs.
    """
    if cv_file is None or not selected_job:
        return "", "", ""
    try:
        content = cv_file.read()
    except Exception:
        return "", "", ""
    text = extract_text_from_bytes(content, getattr(cv_file, "name", ""))
    try:
        job_id = int(selected_job.split(":", 1)[0])
    except Exception:
        return "", "", ""
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    db.close()
    if not job:
        return "", "", ""
    percentage, missing_skills, red_flags = assess_cv_against_job(text, job.skills or "")
    match_str = f"Match: {percentage}%"
    missing_str = ", ".join(missing_skills) if missing_skills else "None"
    redflags_str = ", ".join(red_flags) if red_flags else "None"
    return match_str, missing_str, redflags_str


def main():
    with gr.Blocks() as demo:
        gr.Markdown("# Job Listings")
        btn = gr.Button("Fetch Jobs Now")
        table = gr.Dataframe(
            headers=["Title", "Company", "Description", "Location", "Skills", "Salary"],
            row_count=(0, None),
            col_count=6,
        )
        job_dropdown = gr.Dropdown(label="Select a Job for ATS Assessment", choices=[])
        gr.Markdown("## ATS Assessment")
        cv_file = gr.File(label="Upload your CV (PDF or TXT)", file_count="single", type="file")
        assess_btn = gr.Button("Assess CV")
        match_out = gr.Textbox(label="Match", interactive=False)
        missing_out = gr.Textbox(label="Missing Skills", interactive=False)
        redflags_out = gr.Textbox(label="Red Flags", interactive=False)
        btn.click(fn=fetch_and_list, inputs=None, outputs=[table, job_dropdown])
        assess_btn.click(
            fn=run_assessment,
            inputs=[cv_file, job_dropdown],
            outputs=[match_out, missing_out, redflags_out],
        )
    demo.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", 7860)))


if __name__ == "__main__":
    main()